#!/usr/bin/env python3
"""Exact finite model for the RT014 proposal-only oriented-matroid bridge."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from typing import Iterable, Sequence


Q = Fraction
SIGNS = (-1, 0, 1)
SYMBOL = {-1: "-", 0: "0", 1: "+"}


def qvec(values: Iterable[int | Fraction]) -> tuple[Fraction, ...]:
    return tuple(Q(value) for value in values)


def transpose(rows: Sequence[Sequence[Fraction]], ncols: int) -> list[list[Fraction]]:
    return [[Q(rows[i][j]) for i in range(len(rows))] for j in range(ncols)]


def rref(
    rows: Sequence[Sequence[Fraction]], ncols: int
) -> tuple[list[list[Fraction]], list[int]]:
    matrix = [[Q(value) for value in row] for row in rows]
    if any(len(row) != ncols for row in matrix):
        raise ValueError("ragged exact matrix")
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(ncols):
        candidate = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if candidate is None:
            continue
        matrix[pivot_row], matrix[candidate] = matrix[candidate], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    value - factor * base
                    for value, base in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivot_columns


def rank(rows: Sequence[Sequence[Fraction]], ncols: int) -> int:
    return len(rref(rows, ncols)[1])


def nullspace(
    rows: Sequence[Sequence[Fraction]], ncols: int
) -> list[tuple[Fraction, ...]]:
    reduced, pivots = rref(rows, ncols)
    free = [column for column in range(ncols) if column not in pivots]
    basis: list[tuple[Fraction, ...]] = []
    for free_column in free:
        vector = [Q(0) for _ in range(ncols)]
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return basis


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Q(0))


def integer_ray(vector: Sequence[Fraction], positive: bool = False) -> tuple[int, ...]:
    denominators = [value.denominator for value in vector]
    scale = math.lcm(*denominators) if denominators else 1
    integers = [int(value * scale) for value in vector]
    common = math.gcd(*(abs(value) for value in integers if value)) if any(integers) else 1
    integers = [value // common for value in integers]
    if positive and next((value for value in integers if value), 1) < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def matrix_rows(columns: Sequence[Sequence[Fraction]]) -> list[list[Fraction]]:
    dimension = len(columns[0]) if columns else 0
    return transpose(columns, dimension)


def positive_circuits(
    columns: Sequence[Sequence[Fraction]], labels: Sequence[str] | None = None
) -> list[dict[str, object]]:
    if not columns:
        return []
    dimension = len(columns[0])
    names = list(labels or [str(index) for index in range(len(columns))])
    output: list[dict[str, object]] = []
    max_size = min(len(columns), dimension + 1)
    for size in range(1, max_size + 1):
        for support in itertools.combinations(range(len(columns)), size):
            selected = [columns[index] for index in support]
            rows = matrix_rows(selected)
            basis = nullspace(rows, size)
            if len(basis) != 1:
                continue
            generator = basis[0]
            if any(value == 0 for value in generator):
                continue
            if not (all(value > 0 for value in generator) or all(value < 0 for value in generator)):
                continue
            coefficients = integer_ray(generator, positive=True)
            output.append(
                {
                    "support_indices": list(support),
                    "support": [names[index] for index in support],
                    "coefficients": list(coefficients),
                    "rank": rank(rows, size),
                    "kernel_dimension": len(basis),
                }
            )
    return output


def sign_of(value: Fraction) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def sign_string(values: Sequence[Fraction]) -> str:
    return "".join(SYMBOL[sign_of(value)] for value in values)


def exact_sign_feasibility(
    columns: Sequence[Sequence[Fraction]], sigma: Sequence[int]
) -> tuple[bool, tuple[Fraction, ...] | None, list[dict[str, object]]]:
    dimension = len(columns[0])
    equality_rows = [list(columns[index]) for index, sign in enumerate(sigma) if sign == 0]
    equality_basis = nullspace(equality_rows, dimension)
    inequality_vectors: list[tuple[Fraction, ...]] = []
    for index, sign in enumerate(sigma):
        if sign == 0:
            continue
        inequality_vectors.append(
            tuple(Q(sign) * dot(base, columns[index]) for base in equality_basis)
        )
    obstruction = positive_circuits(inequality_vectors)
    if obstruction:
        return False, None, obstruction
    if not inequality_vectors:
        return True, tuple(Q(0) for _ in range(dimension)), []
    variable_dimension = len(equality_basis)
    for bound in range(1, 13):
        for coefficients in itertools.product(range(-bound, bound + 1), repeat=variable_dimension):
            if not any(coefficients):
                continue
            if all(dot(vector, coefficients) > 0 for vector in inequality_vectors):
                witness = tuple(
                    sum((Q(coefficients[j]) * equality_basis[j][i] for j in range(variable_dimension)), Q(0))
                    for i in range(dimension)
                )
                evaluations = [dot(witness, column) for column in columns]
                if tuple(sign_of(value) for value in evaluations) != tuple(sigma):
                    raise AssertionError("exact witness does not realize requested sign pattern")
                return True, witness, []
    raise AssertionError("Gordan-feasible exact sign cell lacks a bounded-search witness")


def covector_inventory(
    name: str, labels: Sequence[str], columns: Sequence[Sequence[Fraction]]
) -> dict[str, object]:
    realized: list[str] = []
    witnesses: dict[str, list[str]] = {}
    infeasible_count = 0
    for sigma in itertools.product(SIGNS, repeat=len(columns)):
        feasible, witness, _ = exact_sign_feasibility(columns, sigma)
        if feasible:
            key = "".join(SYMBOL[value] for value in sigma)
            realized.append(key)
            witnesses[key] = [str(value) for value in witness or ()]
        else:
            infeasible_count += 1
    circuits = positive_circuits(columns, labels)
    plus_key = "+" * len(columns)
    feasible_branch = plus_key in realized
    if feasible_branch == bool(circuits):
        raise AssertionError("strict alternative is not exclusive")
    if feasible_branch:
        certificate: dict[str, object] = {
            "tag": "Feasible",
            "witness": witnesses[plus_key],
            "evaluation_signs": plus_key,
        }
    else:
        certificate = {"tag": "Obstructed", "positive_circuit": circuits[0]}
    rows = matrix_rows(columns)
    return {
        "configuration_id": name,
        "labels": list(labels),
        "columns": [[str(value) for value in column] for column in columns],
        "rank": rank(rows, len(columns)),
        "kernel_dimension": len(nullspace(rows, len(columns))),
        "sign_cube_size": 3 ** len(columns),
        "realized_covector_count": len(realized),
        "unrealized_sign_count": infeasible_count,
        "tope_count": sum("0" not in value for value in realized),
        "realized_covectors": sorted(realized),
        "covector_witnesses": {key: witnesses[key] for key in sorted(witnesses)},
        "minimal_positive_circuit_count": len(circuits),
        "minimal_positive_circuits": circuits,
        "total_certificate": certificate,
        "totality_exclusive": True,
    }


def restrict_covector(covector: str, indices: Sequence[int]) -> str:
    return "".join(covector[index] for index in indices)


def refinement_check(small: dict[str, object], large: dict[str, object]) -> dict[str, object]:
    small_covectors = set(small["realized_covectors"])
    large_covectors = set(large["realized_covectors"])
    indices = list(range(len(small["labels"])))
    restricted = {restrict_covector(value, indices) for value in large_covectors}
    old_circuits = {
        tuple(circuit["support"]) for circuit in small["minimal_positive_circuits"]
    }
    new_circuits = {
        tuple(circuit["support"]) for circuit in large["minimal_positive_circuits"]
    }
    return {
        "small": small["configuration_id"],
        "large": large["configuration_id"],
        "restriction_surjective": restricted == small_covectors,
        "restricted_covector_count": len(restricted),
        "small_covector_count": len(small_covectors),
        "strict_chamber_inclusion_verified_by_branch": (
            large["total_certificate"]["tag"] == "Obstructed"
            or small["total_certificate"]["tag"] == "Feasible"
        ),
        "old_positive_circuit_supports": [list(value) for value in sorted(old_circuits)],
        "old_positive_circuits_persist": old_circuits.issubset(new_circuits),
    }


def mat_vec(matrix: Sequence[Sequence[Fraction]], vector: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(dot(row, vector) for row in matrix)


def solve_square(
    matrix: Sequence[Sequence[Fraction]], right_hand_side: Sequence[Fraction]
) -> tuple[Fraction, ...]:
    size = len(matrix)
    augmented = [list(row) + [Q(right_hand_side[index])] for index, row in enumerate(matrix)]
    reduced, pivots = rref(augmented, size + 1)
    if pivots != list(range(size)):
        raise ValueError("matrix is not invertible")
    return tuple(reduced[index][-1] for index in range(size))


def presentation_check(
    labels: Sequence[str], columns: Sequence[Sequence[Fraction]], inventory: dict[str, object]
) -> dict[str, object]:
    transform = [qvec((1, 1, 0)), qvec((0, 1, 1)), qvec((1, 0, 1))]
    scales = [Q(2), Q(3), Q(5), Q(7)]
    permutation = [2, 0, 3, 1]
    scaled = [tuple(scales[i] * value for value in mat_vec(transform, columns[i])) for i in range(4)]
    transported_columns = [scaled[index] for index in permutation]
    transported_labels = [labels[index] for index in permutation]
    transported = covector_inventory("A_F4_PRESENTED", transported_labels, transported_columns)
    expected_covectors = {
        restrict_covector(value, permutation) for value in inventory["realized_covectors"]
    }
    actual_covectors = set(transported["realized_covectors"])
    old_supports = {
        tuple(sorted(circuit["support"])) for circuit in inventory["minimal_positive_circuits"]
    }
    new_supports = {
        tuple(sorted(circuit["support"])) for circuit in transported["minimal_positive_circuits"]
    }
    expected_coefficient_rays: dict[tuple[str, ...], tuple[int, ...]] = {}
    for circuit in inventory["minimal_positive_circuits"]:
        coefficient_by_label = dict(zip(circuit["support"], circuit["coefficients"]))
        support_labels = tuple(sorted(circuit["support"]))
        transported_coefficients: list[Fraction] = []
        ordered_support: list[str] = []
        for new_index, old_index in enumerate(permutation):
            label = labels[old_index]
            if label in coefficient_by_label:
                ordered_support.append(label)
                transported_coefficients.append(Q(coefficient_by_label[label], 1) / scales[old_index])
        coefficient_by_transported_label = dict(
            zip(ordered_support, integer_ray(transported_coefficients, positive=True))
        )
        expected_coefficient_rays[support_labels] = tuple(
            coefficient_by_transported_label[label] for label in support_labels
        )
    actual_coefficient_rays: dict[tuple[str, ...], tuple[int, ...]] = {}
    for circuit in transported["minimal_positive_circuits"]:
        coefficient_by_label = dict(zip(circuit["support"], circuit["coefficients"]))
        support_labels = tuple(sorted(circuit["support"]))
        actual_coefficient_rays[support_labels] = tuple(
            coefficient_by_label[label] for label in support_labels
        )
    raw_certificate_transport_verified = True
    transported_feasible_witness: list[str] = []
    if inventory["total_certificate"]["tag"] == "Feasible":
        witness = tuple(Q(value) for value in inventory["total_certificate"]["witness"])
        transform_transpose = transpose(transform, len(transform))
        transported_witness = solve_square(transform_transpose, witness)
        transported_feasible_witness = [str(value) for value in transported_witness]
        raw_certificate_transport_verified = all(
            dot(transported_witness, column) > 0 for column in transported_columns
        )
    else:
        raw_certificate_transport_verified = expected_coefficient_rays == actual_coefficient_rays
    return {
        "source_linear_transform": [[str(value) for value in row] for row in transform],
        "source_linear_transform_determinant": "2",
        "positive_diagonal": [str(value) for value in scales],
        "permutation_new_to_old": permutation,
        "transported_covectors_match": actual_covectors == expected_covectors,
        "transported_covector_count": len(actual_covectors),
        "circuit_supports_match_by_labels": old_supports == new_supports,
        "circuit_coefficient_rays_transport": expected_coefficient_rays == actual_coefficient_rays,
        "transported_feasible_witness": transported_feasible_witness,
        "raw_certificate_transport_verified": raw_certificate_transport_verified,
        "quotient_value_kind": "isomorphism_class_plus_certificate_orbit",
        "raw_witnesses_are_not_quotient_values": True,
        "rank_preserved": transported["rank"] == inventory["rank"],
        "branch_preserved": transported["total_certificate"]["tag"] == inventory["total_certificate"]["tag"],
        "negative_reorientation_is_excluded": True,
    }


def determinant3(columns: Sequence[Sequence[Fraction]]) -> Fraction:
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def variation_record() -> dict[str, object]:
    labels = ("s1", "s2", "s3", "s4")
    samples: dict[str, dict[str, object]] = {}
    minor_values: dict[str, dict[str, str]] = {}
    for parameter in (Q(-1), Q(0), Q(1)):
        columns = (
            qvec((1, 0, 0)),
            qvec((0, 1, 0)),
            qvec((0, 0, 1)),
            qvec((1, 1, parameter)),
        )
        inventory = covector_inventory(f"A_W({parameter})", labels, columns)
        samples[str(parameter)] = {
            "rank": inventory["rank"],
            "realized_covector_count": inventory["realized_covector_count"],
            "tope_count": inventory["tope_count"],
            "branch": inventory["total_certificate"]["tag"],
            "covector_hash": hashlib.sha256(
                "\n".join(inventory["realized_covectors"]).encode("utf-8")
            ).hexdigest(),
        }
        values: dict[str, str] = {}
        for support in itertools.combinations(range(4), 3):
            key = "".join(str(index + 1) for index in support)
            values[key] = str(determinant3([columns[index] for index in support]))
        minor_values[str(parameter)] = values
    return {
        "path": "v1=e1, v2=e2, v3=e3, v4(t)=(1,1,t), t in [-1,1]",
        "admitted_path_class": "predeclared finite semialgebraic piecewise-rational paths over an exact ordered field with root isolation",
        "arbitrary_continuous_paths_admitted": False,
        "finite_wall_enumeration_scope": "the admitted finite-complexity path class only",
        "zero_vector_walls": [],
        "full_rank_walls": [],
        "determinant_minor_walls": [
            {
                "minor_support": ["s1", "s2", "s4"],
                "polynomial": "t",
                "crossing_parameter": "0",
                "left_sign": "-",
                "wall_sign": "0",
                "right_sign": "+",
            }
        ],
        "minor_samples": minor_values,
        "inventory_samples": samples,
        "wall_free_intervals": ["[-1,0)", "(0,1]"],
        "stratumwise_stability_only": True,
        "continuum_robustness_claimed": False,
    }


def build() -> dict[str, object]:
    labels4 = ("s1", "s2", "s3", "s4")
    labels5 = labels4 + ("s5",)
    labels6 = labels5 + ("s6",)
    base = (
        qvec((1, 0, 0)),
        qvec((0, 1, 0)),
        qvec((0, 0, 1)),
    )
    extra5 = qvec((1, -1, 1))
    extra6 = qvec((2, 1, -1))
    feasible4 = base + (qvec((1, 1, 1)),)
    obstructed4 = base + (qvec((-1, -1, -1)),)
    configurations = {
        "A_F4": (labels4, feasible4),
        "A_F5": (labels5, feasible4 + (extra5,)),
        "A_F6": (labels6, feasible4 + (extra5, extra6)),
        "A_O4": (labels4, obstructed4),
        "A_O5": (labels5, obstructed4 + (extra5,)),
        "A_O6": (labels6, obstructed4 + (extra5, extra6)),
    }
    inventories = {
        name: covector_inventory(name, labels, columns)
        for name, (labels, columns) in configurations.items()
    }
    refinements = [
        refinement_check(inventories["A_F4"], inventories["A_F5"]),
        refinement_check(inventories["A_F5"], inventories["A_F6"]),
        refinement_check(inventories["A_F4"], inventories["A_F6"]),
        refinement_check(inventories["A_O4"], inventories["A_O5"]),
        refinement_check(inventories["A_O5"], inventories["A_O6"]),
        refinement_check(inventories["A_O4"], inventories["A_O6"]),
    ]
    direct_f = {
        restrict_covector(value, range(4))
        for value in inventories["A_F6"]["realized_covectors"]
    }
    composed_f = {
        restrict_covector(restrict_covector(value, range(5)), range(4))
        for value in inventories["A_F6"]["realized_covectors"]
    }
    direct_o = {
        restrict_covector(value, range(4))
        for value in inventories["A_O6"]["realized_covectors"]
    }
    composed_o = {
        restrict_covector(restrict_covector(value, range(5)), range(4))
        for value in inventories["A_O6"]["realized_covectors"]
    }
    presentation_feasible = presentation_check(labels4, feasible4, inventories["A_F4"])
    presentation_obstructed = presentation_check(labels4, obstructed4, inventories["A_O4"])
    negative_flip = {
        "covectors_flip_fourth_coordinate": {
            value[:3] + {"+": "-", "-": "+", "0": "0"}[value[3]]
            for value in inventories["A_F4"]["realized_covectors"]
        }
        == set(inventories["A_O4"]["realized_covectors"]),
        "feasible_branch_before": inventories["A_F4"]["total_certificate"]["tag"],
        "feasible_branch_after": inventories["A_O4"]["total_certificate"]["tag"],
        "negative_reorientation_changes_source_data": True,
    }
    all_checks = {
        "every_covector_has_exact_witness": all(
            len(inventory["covector_witnesses"]) == inventory["realized_covector_count"]
            for inventory in inventories.values()
        ),
        "all_total_certificates_exclusive": all(
            inventory["totality_exclusive"] for inventory in inventories.values()
        ),
        "both_total_branches_exercised": {
            inventory["total_certificate"]["tag"] for inventory in inventories.values()
        }
        == {"Feasible", "Obstructed"},
        "all_circuit_supports_bounded_by_rank_plus_one": all(
            len(circuit["support"]) <= inventory["rank"] + 1
            for inventory in inventories.values()
            for circuit in inventory["minimal_positive_circuits"]
        ),
        "all_circuit_rank_kernel_claims": all(
            circuit["rank"] == len(circuit["support"]) - 1
            and circuit["kernel_dimension"] == 1
            and all(value > 0 for value in circuit["coefficients"])
            for inventory in inventories.values()
            for circuit in inventory["minimal_positive_circuits"]
        ),
        "all_refinement_restrictions_surjective": all(
            record["restriction_surjective"] for record in refinements
        ),
        "all_old_positive_circuits_persist": all(
            record["old_positive_circuits_persist"] for record in refinements
        ),
        "nested_refinement_composition": direct_f == composed_f and direct_o == composed_o,
        "presentation_transport": all(
            presentation[key]
            for presentation in (presentation_feasible, presentation_obstructed)
            for key in (
                "transported_covectors_match",
                "circuit_supports_match_by_labels",
                "circuit_coefficient_rays_transport",
                "raw_certificate_transport_verified",
                "rank_preserved",
                "branch_preserved",
            )
        ),
        "negative_reorientation_control": all(negative_flip.values()),
    }
    if not all(all_checks.values()):
        raise AssertionError(f"exact Bridge_OM check failed: {all_checks}")
    result = {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_exact_model_v1",
        "status": "PASS",
        "candidate_map": "Bridge_OM(A)=(Cstar(A),Cir_plus(A),Tot(A),Ref(A),Strat(A))",
        "exact_number_field": "Q",
        "admissible_general_exact_domain": "ordered exact fields with decidable sign, rank, homogeneous linear feasibility, and path-root isolation",
        "primary_configuration": "A_F4",
        "declared_refinement_towers": ["A_F4->A_F5->A_F6", "A_O4->A_O5->A_O6"],
        "negative_reorientation_control": negative_flip,
        "inventories": inventories,
        "refinements": refinements,
        "nested_refinement_composition": {
            "feasible_tower": direct_f == composed_f,
            "obstructed_tower": direct_o == composed_o,
        },
        "presentation_transport": {
            "feasible_fixture": presentation_feasible,
            "obstructed_fixture": presentation_obstructed,
            "descent_type": "equivariant configuration groupoid whose quotient value is an isomorphism class with certificate orbit",
            "raw_certificate_quotient_map_claimed": False,
        },
        "variation_stratification": variation_record(),
        "checks": all_checks,
        "authority_limits": {
            "proposal_only": True,
            "finite_declared_sector_scope_only": True,
            "physical_causality_constructed": False,
            "empirical_response_constructed": False,
            "universal_p7_coverage_constructed": False,
            "conformal_geometry_constructed": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["model_payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.compact:
        compact = {
            "schema_id": result["schema_id"],
            "status": result["status"],
            "candidate_map": result["candidate_map"],
            "model_payload_sha256": result["model_payload_sha256"],
            "configuration_summaries": {
                name: {
                    key: inventory[key]
                    for key in (
                        "rank",
                        "kernel_dimension",
                        "realized_covector_count",
                        "tope_count",
                        "minimal_positive_circuit_count",
                        "total_certificate",
                    )
                }
                for name, inventory in result["inventories"].items()
            },
            "checks": result["checks"],
        }
        print(json.dumps(compact, indent=2, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
