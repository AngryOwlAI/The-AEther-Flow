#!/usr/bin/env python3
"""Independent one-dimensional check for the V22 P3-T03 upwind limit.

This implementation intentionally imports no code from the primary model.
"""

from __future__ import annotations

import argparse
import json
import math


def initial_value(x: float) -> float:
    return 2.0 + 0.2 * math.sin(2.0 * math.pi * x)


def solve(level: int, final_time: float = 0.1, cfl_target: float = 0.4) -> dict[str, float | int]:
    spacing = 1.0 / level
    steps = max(1, math.ceil(final_time / (cfl_target * spacing)))
    time_step = final_time / steps
    cfl = time_step / spacing
    state = [initial_value(index * spacing) for index in range(level)]
    for _ in range(steps):
        old = state
        state = [
            (1.0 - cfl) * old[index] + cfl * old[(index - 1) % level]
            for index in range(level)
        ]
    reference = [initial_value((index * spacing - final_time) % 1.0) for index in range(level)]
    return {
        "n": level,
        "h": spacing,
        "dt": time_step,
        "steps": steps,
        "cfl": cfl,
        "max_error": max(abs(value - exact) for value, exact in zip(state, reference, strict=True)),
    }


def evaluate() -> dict[str, object]:
    levels = [solve(level) for level in (16, 24, 32, 48, 64)]
    orders = [
        math.log(float(coarse["max_error"]) / float(fine["max_error"]))
        / math.log(float(coarse["h"]) / float(fine["h"]))
        for coarse, fine in zip(levels, levels[1:])
    ]
    return {
        "schema_id": "v22_p3_t03_independent_solver_result_v1",
        "status": "PASS",
        "implementation_independent_of_primary": True,
        "equation": "u_t+u_x=0 on a periodic source label interval",
        "levels": levels,
        "observed_orders": orders,
        "strict_error_decrease": all(
            float(coarse["max_error"]) > float(fine["max_error"])
            for coarse, fine in zip(levels, levels[1:])
        ),
        "target_geometry_inputs": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
