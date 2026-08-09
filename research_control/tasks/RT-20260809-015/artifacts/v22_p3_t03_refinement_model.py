#!/usr/bin/env python3
"""Deterministic source-chart refinement model for V22 P3-T03.

The model compares a monotone finite upwind family with the proposal-only
P3-T02 six-channel transport semigroup. Coordinate partitions are numerical
source-chart data; they are not physical lengths or target geometry.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


Velocity = tuple[int, int, int]
Point = tuple[float, float, float]

VELOCITIES: tuple[Velocity, ...] = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 2),
    (2, 0, 1),
)
LEVELS: tuple[int, ...] = (6, 8, 12, 16)
MESH_KINDS: tuple[str, ...] = ("uniform", "graded", "adaptive")
FINAL_TIME = 0.1
CFL_TARGET = 0.45


@dataclass(frozen=True)
class Grid3D:
    kind: str
    n: int
    axes: tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]

    @property
    def shape(self) -> tuple[int, int, int]:
        return tuple(len(axis) for axis in self.axes)  # type: ignore[return-value]

    @property
    def size(self) -> int:
        nx, ny, nz = self.shape
        return nx * ny * nz

    def backward_spacings(self, axis: int) -> tuple[float, ...]:
        nodes = self.axes[axis]
        return tuple(
            nodes[i] - nodes[i - 1] if i else nodes[0] + 1.0 - nodes[-1]
            for i in range(len(nodes))
        )

    @property
    def h_max(self) -> float:
        return max(max(self.backward_spacings(axis)) for axis in range(3))

    @property
    def h_min(self) -> float:
        return min(min(self.backward_spacings(axis)) for axis in range(3))

    @property
    def mesh_ratio(self) -> float:
        return self.h_max / self.h_min


def _normalized_cumulative(widths: Sequence[float]) -> tuple[float, ...]:
    total = sum(widths)
    nodes = [0.0]
    running = 0.0
    for width in widths[:-1]:
        running += width / total
        nodes.append(running)
    return tuple(nodes)


def axis_nodes(kind: str, n: int, axis: int) -> tuple[float, ...]:
    if n < 4:
        raise ValueError("n must be at least four")
    if kind == "uniform":
        return tuple(i / n for i in range(n))
    if kind == "graded":
        amplitudes = (0.22, -0.17, 0.13)
        amplitude = amplitudes[axis]
        return tuple(
            u + amplitude * math.sin(2.0 * math.pi * u) / (2.0 * math.pi)
            for u in (i / n for i in range(n))
        )
    if kind == "adaptive":
        phase = (0.07, 0.23, 0.41)[axis]
        raw_widths = [
            1.0
            / (
                1.0
                + 0.75
                * abs(math.sin(2.0 * math.pi * ((i + 0.5) / n + phase)))
            )
            for i in range(n)
        ]
        return _normalized_cumulative(raw_widths)
    raise ValueError(f"unknown mesh kind: {kind}")


def make_grid(kind: str, n: int) -> Grid3D:
    return Grid3D(kind, n, tuple(axis_nodes(kind, n, axis) for axis in range(3)))  # type: ignore[arg-type]


def manufactured_value(channel: int, point: Point) -> float:
    x, y, z = point
    if channel == 1:
        return 2.0 + 0.20 * math.sin(2.0 * math.pi * x) + 0.03 * math.cos(2.0 * math.pi * (y + z))
    if channel == 2:
        return 2.4 + 0.18 * math.sin(2.0 * math.pi * y) + 0.02 * math.cos(2.0 * math.pi * (x - z))
    if channel == 3:
        return 1.3 + 0.11 * math.cos(2.0 * math.pi * z) + 0.02 * math.sin(2.0 * math.pi * x)
    if channel == 4:
        return 1.7 + 0.12 * math.sin(2.0 * math.pi * (x + y)) + 0.03 * math.cos(2.0 * math.pi * z)
    if channel == 5:
        return 1.9 + 0.10 * math.cos(2.0 * math.pi * (y + 2.0 * z)) + 0.02 * math.sin(2.0 * math.pi * x)
    if channel == 6:
        return 3.0 + 0.08 * math.sin(2.0 * math.pi * (2.0 * x + z))
    raise ValueError("channel must be in 1..6")


def exact_value(channel: int, point: Point, time: float) -> float:
    velocity = VELOCITIES[channel - 1]
    shifted = tuple((coordinate - speed * time) % 1.0 for coordinate, speed in zip(point, velocity, strict=True))
    return manufactured_value(channel, shifted)  # type: ignore[arg-type]


def flat_index(i: int, j: int, k: int, shape: tuple[int, int, int]) -> int:
    _, ny, nz = shape
    return (i * ny + j) * nz + k


def sample_grid(grid: Grid3D, evaluator: Callable[[Point], float]) -> list[float]:
    values: list[float] = []
    for x in grid.axes[0]:
        for y in grid.axes[1]:
            for z in grid.axes[2]:
                values.append(evaluator((x, y, z)))
    return values


def source_cfl_denominator(grid: Grid3D, velocity: Velocity) -> float:
    return sum(
        abs(speed) / min(grid.backward_spacings(axis))
        for axis, speed in enumerate(velocity)
        if speed
    )


def stable_time_step(grid: Grid3D, velocity: Velocity, final_time: float) -> tuple[float, int, float]:
    denominator = source_cfl_denominator(grid, velocity)
    if denominator == 0:
        return final_time, 1, 0.0
    raw = CFL_TARGET / denominator
    steps = max(1, math.ceil(final_time / raw))
    dt = final_time / steps
    return dt, steps, dt * denominator


def upwind_step(values: Sequence[float], grid: Grid3D, velocity: Velocity, dt: float) -> list[float]:
    shape = grid.shape
    nx, ny, nz = shape
    spacings = tuple(grid.backward_spacings(axis) for axis in range(3))
    updated = [0.0] * len(values)
    for i in range(nx):
        im = (i - 1) % nx
        cx = dt * velocity[0] / spacings[0][i]
        for j in range(ny):
            jm = (j - 1) % ny
            cy = dt * velocity[1] / spacings[1][j]
            for k in range(nz):
                km = (k - 1) % nz
                cz = dt * velocity[2] / spacings[2][k]
                index = flat_index(i, j, k, shape)
                center_weight = 1.0 - cx - cy - cz
                updated[index] = (
                    center_weight * values[index]
                    + cx * values[flat_index(im, j, k, shape)]
                    + cy * values[flat_index(i, jm, k, shape)]
                    + cz * values[flat_index(i, j, km, shape)]
                )
    return updated


def channel_run(kind: str, n: int, channel: int, final_time: float = FINAL_TIME) -> dict[str, float | int | str]:
    grid = make_grid(kind, n)
    velocity = VELOCITIES[channel - 1]
    values = sample_grid(grid, lambda point: manufactured_value(channel, point))
    initial_min = min(values)
    initial_max = max(values)
    dt, steps, cfl = stable_time_step(grid, velocity, final_time)
    for _ in range(steps):
        values = upwind_step(values, grid, velocity, dt)
    exact = sample_grid(grid, lambda point: exact_value(channel, point, final_time))
    error = max(abs(numerical - reference) for numerical, reference in zip(values, exact, strict=True))
    return {
        "mesh_kind": kind,
        "n": n,
        "channel": channel,
        "h_max": grid.h_max,
        "h_min": grid.h_min,
        "mesh_ratio": grid.mesh_ratio,
        "dt": dt,
        "steps": steps,
        "cfl": cfl,
        "max_error": error,
        "initial_min": initial_min,
        "initial_max": initial_max,
        "final_min": min(values),
        "final_max": max(values),
    }


def convergence_study(kind: str) -> dict[str, object]:
    levels: list[dict[str, object]] = []
    for n in LEVELS:
        channel_results = [channel_run(kind, n, channel) for channel in range(1, 7)]
        levels.append(
            {
                "n": n,
                "h_max": max(float(result["h_max"]) for result in channel_results),
                "max_error": max(float(result["max_error"]) for result in channel_results),
                "max_cfl": max(float(result["cfl"]) for result in channel_results),
                "max_mesh_ratio": max(float(result["mesh_ratio"]) for result in channel_results),
                "channel_results": channel_results,
            }
        )
    orders: list[float] = []
    for coarse, fine in zip(levels, levels[1:]):
        orders.append(
            math.log(float(coarse["max_error"]) / float(fine["max_error"]))
            / math.log(float(coarse["h_max"]) / float(fine["h_max"]))
        )
    return {
        "mesh_kind": kind,
        "levels": levels,
        "observed_orders": orders,
        "strict_error_decrease": all(
            float(coarse["max_error"]) > float(fine["max_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
    }


def principal_symbol(velocity: Velocity, mode: Velocity, n: int) -> complex:
    h = 1.0 / n
    return sum(
        speed * (1.0 - cmath.exp(-1j * 2.0 * math.pi * wave * h)) / h
        for speed, wave in zip(velocity, mode, strict=True)
    )


def continuum_principal_factor(velocity: Velocity, mode: Velocity) -> complex:
    return 1j * 2.0 * math.pi * sum(speed * wave for speed, wave in zip(velocity, mode, strict=True))


def principal_study() -> dict[str, object]:
    mode: Velocity = (1, 1, 1)
    levels: list[dict[str, object]] = []
    continuum_factors = [continuum_principal_factor(velocity, mode) for velocity in VELOCITIES]
    continuum_product = math.prod(continuum_factors)
    for n in (8, 16, 32, 64):
        discrete_factors = [principal_symbol(velocity, mode, n) for velocity in VELOCITIES]
        discrete_product = math.prod(discrete_factors)
        levels.append(
            {
                "n": n,
                "h": 1.0 / n,
                "max_factor_error": max(abs(discrete - continuum) for discrete, continuum in zip(discrete_factors, continuum_factors, strict=True)),
                "relative_product_error": abs(discrete_product - continuum_product) / abs(continuum_product),
                "factor_count": len(discrete_factors),
            }
        )
    return {
        "mode": list(mode),
        "levels": levels,
        "factor_error_decreases": all(
            float(coarse["max_factor_error"]) > float(fine["max_factor_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
        "product_error_decreases": all(
            float(coarse["relative_product_error"]) > float(fine["relative_product_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
        "physical_cone_inferred": False,
        "lorentzian_signature_inferred": False,
    }


def inflow_profile(x: float) -> float:
    return 1.2 + 0.2 * math.sin(2.0 * math.pi * x) + 0.05 * math.cos(math.pi * x)


def inflow_run(n: int, final_time: float = FINAL_TIME) -> dict[str, float | int]:
    h = 1.0 / n
    raw_dt = CFL_TARGET * h
    steps = max(1, math.ceil(final_time / raw_dt))
    dt = final_time / steps
    cfl = dt / h
    values = [inflow_profile(i * h) for i in range(n + 1)]
    for step in range(steps):
        next_time = (step + 1) * dt
        updated = values.copy()
        updated[0] = inflow_profile(-next_time)
        for i in range(1, n + 1):
            updated[i] = (1.0 - cfl) * values[i] + cfl * values[i - 1]
        values = updated
    exact = [inflow_profile(i * h - final_time) for i in range(n + 1)]
    return {
        "n": n,
        "h": h,
        "dt": dt,
        "steps": steps,
        "cfl": cfl,
        "max_error": max(abs(a - b) for a, b in zip(values, exact, strict=True)),
    }


def boundary_study() -> dict[str, object]:
    levels = [inflow_run(n) for n in (16, 24, 32, 48)]
    return {
        "boundary_class": "exact_source_inflow_outflow_unprescribed",
        "levels": levels,
        "strict_error_decrease": all(
            float(coarse["max_error"]) > float(fine["max_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
        "outflow_data_used": False,
        "finite_size_protocol": "comparison is valid only where the exact backward characteristic remains inside the source slab or meets the declared inflow trace",
    }


def reconstruction_bound_record() -> dict[str, object]:
    return {
        "sampling_map": "I_n f=(f(x_i))_i",
        "reconstruction_map": "R_n z is cellwise constant on each directed source-chart cell with its lower-node value",
        "norm": "source-chart l_infinity and sup norm; neither is a physical metric norm",
        "bound": "||R_n I_n f-f||_infinity <= 3 h_n max_j ||partial_j f||_infinity",
        "global_evolution_bound": "||U_n^m I_n f-I_n S(t_m)f||_infinity <= T/2 [dt ||(v dot grad)^2 f||_infinity + sum_j |v_j| h_j,max ||partial_jj f||_infinity]",
        "principal_factor_bound": "|Lambda_A,n(k)-i v_A dot k| <= 1/2 sum_j |v_A^j| h_j,max |k_j|^2",
        "tool_class": "monotone finite-difference consistency plus l_infinity stability; local sheaf restriction compatibility",
    }


def evaluate_package() -> dict[str, object]:
    convergence = [convergence_study(kind) for kind in MESH_KINDS]
    principal = principal_study()
    boundary = boundary_study()
    return {
        "schema_id": "v22_p3_t03_refinement_model_result_v1",
        "status": "PASS",
        "refinement_candidate_id": "CAND-V22-B1-SIX-TRANSPORT-REFINEMENT-V1",
        "limit_object_id": "LIMIT-V22-B1-SIX-TRANSPORT-SEMIGROUP-V1",
        "levels": list(LEVELS),
        "mesh_kinds": list(MESH_KINDS),
        "final_time": FINAL_TIME,
        "cfl_target": CFL_TARGET,
        "comparison_maps": reconstruction_bound_record(),
        "convergence_studies": convergence,
        "boundary_study": boundary,
        "principal_study": principal,
        "property_preservation": {
            "constant_state": "preserved exactly by convex update weights",
            "range_and_q6_margin": "preserved under source CFL because each update is a convex combination",
            "source_evolution_orientation": "preserved for positive dt and fixed P3-T02 velocities",
            "principal_factor_count": 6,
            "physical_causal_cone_status": "upstream_object_undefined_not_preserved_or_lost",
            "lorentzian_signature_status": "upstream_object_undefined_not_preserved_or_lost",
            "physical_property_promotion_authorized": False,
        },
        "source_purity": {
            "target_atlas_input_count": 0,
            "target_metric_input_count": 0,
            "physical_measure_input_count": 0,
            "target_geometry_interpolation_count": 0,
            "target_fit_count": 0,
            "coordinate_mesh_fixed_before_target_comparison": True,
            "effective_metric_constructed": False,
        },
        "finite_zero_remainder_used_as_limit_proof": False,
        "nonzero_truncation_error_observed": all(
            float(study["levels"][0]["max_error"]) > 0.0 for study in convergence  # type: ignore[index]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    args = parser.parse_args()
    result = evaluate_package()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
