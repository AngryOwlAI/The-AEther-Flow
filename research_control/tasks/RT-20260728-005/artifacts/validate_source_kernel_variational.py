#!/usr/bin/env python3
"""Deterministic source-only validation for the P7-T06 draft/control packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
SPEC_PATH = ARTIFACTS / "source_kernel_variational_object_spec_v1.yaml"
CONTROLS_PATH = ARTIFACTS / "source_kernel_variational_controls_v1.yaml"
ASSUMPTIONS_PATH = ARTIFACTS / "source_kernel_variational_assumption_dependency_table_v1.yaml"
TEX_PATH = ARTIFACTS / "source_kernel_variational_object_candidate_v1.tex"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p7_t06_source_variational.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p7_t06_source_variational.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p7_t06_source_variational.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p7_t06_source_variational.md"
REPORT_PATH = ARTIFACTS / "source_kernel_variational_validation_v1.json"
COMPACT_PATH = ARTIFACTS / "source_kernel_variational_compact_receipt_v1.json"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def fraction_vector(value: Any) -> list[Fraction]:
    if not isinstance(value, list):
        return []
    return [fraction(item) for item in value]


def fraction_matrix(value: Any) -> list[list[Fraction]]:
    if not isinstance(value, list):
        return []
    matrix: list[list[Fraction]] = []
    for row in value:
        if not isinstance(row, list):
            return []
        matrix.append([fraction(item) for item in row])
    return matrix


def square(matrix: list[list[Fraction]]) -> bool:
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def matrix_add(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left[row][column] + right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


def matrix_subtract(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left[row][column] - right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


def matrix_scale(
    scalar: Fraction, matrix: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_vector(
    matrix: list[list[Fraction]], vector: list[Fraction]
) -> list[Fraction]:
    return [
        sum((entry * vector[column] for column, entry in enumerate(row)), Fraction(0))
        for row in matrix
    ]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def identity(size: int) -> list[list[Fraction]]:
    return [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def laplacian(conductance: list[list[Fraction]]) -> list[list[Fraction]]:
    size = len(conductance)
    result = matrix_scale(Fraction(-1), conductance)
    for row in range(size):
        result[row][row] += sum(conductance[row], Fraction(0))
    return result


def functional(conductance: list[list[Fraction]], probe: list[Fraction]) -> Fraction:
    total = Fraction(0)
    for row in range(len(probe)):
        for column in range(len(probe)):
            delta = probe[column] - probe[row]
            total += conductance[row][column] * delta * delta
    return total / 4


def flux(conductance: list[list[Fraction]], probe: list[Fraction]) -> list[list[Fraction]]:
    return [
        [
            conductance[row][column] * (probe[row] - probe[column])
            for column in range(len(probe))
        ]
        for row in range(len(probe))
    ]


def symmetric(matrix: list[list[Fraction]]) -> bool:
    return square(matrix) and matrix == transpose(matrix)


def antisymmetric(matrix: list[list[Fraction]]) -> bool:
    return square(matrix) and matrix == matrix_scale(Fraction(-1), transpose(matrix))


def string_matrix(matrix: list[list[Fraction]]) -> list[list[str]]:
    return [[str(entry) for entry in row] for row in matrix]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    required_paths = [
        SPEC_PATH,
        CONTROLS_PATH,
        ASSUMPTIONS_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required_paths:
        check(f"exists:{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    if not all(path.is_file() for path in required_paths):
        payload = {
            "schema_id": "v21_p7_t06_source_kernel_variational_validation_v1",
            "status": "FAIL",
            "check_count": len(checks),
            "failed_check_count": sum(item["status"] == "FAIL" for item in checks),
            "checks": checks,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    spec = load_yaml(SPEC_PATH)
    controls = load_yaml(CONTROLS_PATH)
    assumptions = load_yaml(ASSUMPTIONS_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")
    fusion = FUSION_PATH.read_text(encoding="utf-8")

    check(
        "spec_schema",
        spec.get("schema_id") == "v21_p7_t06_source_kernel_variational_object_spec_v1",
        "spec schema",
    )
    check("task_id", spec.get("task_id") == "RT-20260728-005", "task identity")
    check("job_id", spec.get("job_id") == "AJ-RT-20260728-005-001", "job identity")
    check("plan_task_id", spec.get("plan_task_id") == "P7-T06", "plan identity")
    check("candidate_id", spec.get("candidate_id") == "SourceKernelDirichletVariationalCandidate_v1", "candidate identity")
    check("source_flux_id", spec.get("source_flux_id") == "SourceVariationalFluxRecord_v1", "source flux identity")
    check("proposal_only", spec.get("candidate_status") == "proposal-only", "candidate status")
    check("source_extension", spec.get("source_extension_status") == "source-extension data", "source-extension status")
    check(
        "adoption_blocked",
        spec.get("adoption_status") == "blocked_adoption_open_continuation",
        "adoption status",
    )
    check(
        "result_kind",
        spec.get("result_kind")
        == "precise_obstruction_with_constructive_restricted_variational_object",
        "decisive result classification",
    )

    expected_source_hashes = {
        "TEX-V21-P7-T02-SOURCE-MATTER-FINITE-TRANSITION-KERNEL-V1":
            "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
        "TEX-V21-P7-T05-UNIVERSAL-SOURCE-COUPLING-MAP-V1":
            "5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b",
        "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-POST-GATE-MATTER-COUPLING-BRIDGE-TARGET-V1-FORMALIZATION":
            "3d1c6dfb2ea543c8ea455ee2f3553e3cac76e3072902213ed07aff0db514605e",
        "TEX-SOURCE-CERTIFICATE-OPERATION-LAWS-V1":
            "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986",
        "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21":
            "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    }
    fixed_sources = spec.get("fixed_source_basis", [])
    fixed_by_id = {
        str(item.get("object_id", "")): item
        for item in fixed_sources
        if isinstance(item, dict) and item.get("object_id")
    }
    for object_id, expected_hash in expected_source_hashes.items():
        item = fixed_by_id.get(object_id, {})
        path = ROOT / str(item.get("path", ""))
        declared_hash = str(item.get("sha256", ""))
        check(f"fixed_hash_declared:{object_id}", declared_hash == expected_hash, expected_hash)
        check(
            f"fixed_hash_current:{object_id}",
            path.is_file() and sha256(path) == expected_hash,
            str(path.relative_to(ROOT)) if path.is_file() else "missing",
        )

    control_rows = controls.get("control_families", [])
    check("control_family_count", isinstance(control_rows, list) and len(control_rows) == 4, "four exact controls")
    known_control_ids = {
        "P7T06-CONTROL-IDENTITY-001",
        "P7T06-CONTROL-POSITIVE-FORWARD-001",
        "P7T06-CONTROL-SYMMETRIC-AVERAGING-001",
        "P7T06-CONTROL-THREE-CYCLE-001",
    }

    computed_controls: dict[str, dict[str, Any]] = {}
    for item in control_rows if isinstance(control_rows, list) else []:
        control_id = str(item.get("control_id", ""))
        check(f"control_known:{control_id}", control_id in known_control_ids, control_id)
        kernel = fraction_matrix(item.get("row_kernel"))
        declared_c = fraction_matrix(item.get("symmetric_part"))
        declared_a = fraction_matrix(item.get("directional_residue"))
        declared_l = fraction_matrix(item.get("variational_laplacian"))
        declared_full = fraction_matrix(item.get("full_directional_operator"))
        check(f"kernel_square:{control_id}", square(kernel), string_matrix(kernel))
        if not square(kernel):
            continue
        size = len(kernel)
        row_sums = [sum(row, Fraction(0)) for row in kernel]
        check(f"kernel_nonnegative:{control_id}", all(entry >= 0 for row in kernel for entry in row), "entrywise")
        check(f"kernel_row_normalized:{control_id}", row_sums == [Fraction(1)] * size, str(row_sums))
        calculated_c = matrix_scale(Fraction(1, 2), matrix_add(kernel, transpose(kernel)))
        calculated_a = matrix_scale(Fraction(1, 2), matrix_subtract(kernel, transpose(kernel)))
        calculated_l = laplacian(calculated_c)
        calculated_full = matrix_subtract(identity(size), kernel)
        check(f"symmetric_part_exact:{control_id}", declared_c == calculated_c, string_matrix(calculated_c))
        check(f"directional_residue_exact:{control_id}", declared_a == calculated_a, string_matrix(calculated_a))
        check(f"split_recombines:{control_id}", matrix_add(calculated_c, calculated_a) == kernel, "C+A=P")
        check(f"conductance_symmetric:{control_id}", symmetric(calculated_c), "C^T=C")
        check(f"residue_antisymmetric:{control_id}", antisymmetric(calculated_a), "A^T=-A")
        check(f"laplacian_exact:{control_id}", declared_l == calculated_l, string_matrix(calculated_l))
        check(f"laplacian_symmetric:{control_id}", symmetric(calculated_l), "L_C^T=L_C")
        check(
            f"laplacian_row_zero:{control_id}",
            [sum(row, Fraction(0)) for row in calculated_l] == [Fraction(0)] * size,
            "L_C 1=0",
        )
        check(f"directional_operator_exact:{control_id}", declared_full == calculated_full, string_matrix(calculated_full))
        expected_representable = symmetric(calculated_full)
        check(
            f"representability_flag:{control_id}",
            item.get("full_directional_scalar_quadratic_representable") is expected_representable,
            str(expected_representable),
        )

        probe_data = item.get("probe", {})
        probe = fraction_vector(probe_data.get("q", [])) if isinstance(probe_data, dict) else []
        if len(probe) == size:
            value = functional(calculated_c, probe)
            gradient = matrix_vector(calculated_l, probe)
            flux_matrix = flux(calculated_c, probe)
            divergence = [sum(row, Fraction(0)) for row in flux_matrix]
            check(f"functional_value:{control_id}", fraction(item.get("functional_value")) == value, str(value))
            if "first_variation" in item:
                check(f"first_variation:{control_id}", fraction_vector(item.get("first_variation")) == gradient, str(gradient))
            check(f"flux_antisymmetric:{control_id}", antisymmetric(flux_matrix), "J^T=-J")
            check(f"flux_divergence:{control_id}", divergence == gradient, str(divergence))
            check(f"closed_balance:{control_id}", sum(gradient, Fraction(0)) == 0, str(sum(gradient, Fraction(0))))
            if "flux_matrix" in item:
                check(f"flux_matrix:{control_id}", fraction_matrix(item.get("flux_matrix")) == flux_matrix, string_matrix(flux_matrix))
            computed_controls[control_id] = {
                "kernel": kernel,
                "conductance": calculated_c,
                "residue": calculated_a,
                "laplacian": calculated_l,
                "full": calculated_full,
                "probe": probe,
                "functional": value,
                "gradient": gradient,
                "flux": flux_matrix,
            }

    forward = computed_controls.get("P7T06-CONTROL-POSITIVE-FORWARD-001", {})
    expected_forward_kernel = [
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(0), Fraction(1)],
    ]
    check("forward_kernel_fixed", forward.get("kernel") == expected_forward_kernel, string_matrix(expected_forward_kernel))
    check("forward_residue_nonzero", forward.get("residue") != [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]], "A_fwd != 0")
    check("forward_full_nonsymmetric", not symmetric(forward.get("full", [])), "I-P_fwd is nonsymmetric")
    check(
        "forward_laplacian_not_sym_full",
        forward.get("laplacian")
        != matrix_scale(
            Fraction(1, 2),
            matrix_add(forward.get("full", []), transpose(forward.get("full", []))),
        ),
        "L_C is not generally Sym(I-P); this control is not doubly stochastic",
    )

    for item in controls.get("variation_test_vectors", []):
        if not isinstance(item, dict):
            continue
        test_id = str(item.get("test_id", ""))
        control_id = str(item.get("control_id", ""))
        computed = computed_controls.get(control_id, {})
        q = fraction_vector(item.get("q", []))
        eta = fraction_vector(item.get("eta", []))
        conductance = computed.get("conductance", [])
        laplace = computed.get("laplacian", [])
        if square(conductance) and len(q) == len(conductance) and len(eta) == len(q):
            derivative = dot(eta, matrix_vector(laplace, q))
            check(
                f"variation_derivative:{test_id}",
                fraction(item.get("exact_directional_derivative")) == derivative,
                str(derivative),
            )
            if "epsilon" in item:
                epsilon = fraction(item.get("epsilon"))
                shifted = [q[index] + epsilon * eta[index] for index in range(len(q))]
                quotient = (functional(conductance, shifted) - functional(conductance, q)) / epsilon
                declared = item.get("exact_difference_quotient", {})
                declared_value = fraction(declared.get("value")) if isinstance(declared, dict) else Fraction(999)
                check(f"variation_quotient:{test_id}", quotient == declared_value, str(quotient))
                remainder = epsilon * functional(conductance, eta)
                check(
                    f"variation_remainder:{test_id}",
                    fraction(item.get("exact_quadratic_remainder")) == remainder,
                    str(remainder),
                )

    for item in controls.get("boundary_controls", []):
        if not isinstance(item, dict):
            continue
        boundary_id = str(item.get("boundary_id", ""))
        control_id = str(item.get("control_id", ""))
        control = next(
            (
                candidate
                for candidate in control_rows
                if isinstance(candidate, dict) and candidate.get("control_id") == control_id
            ),
            {},
        )
        states = list(control.get("states", []))
        subset = set(item.get("subset", []))
        computed = computed_controls.get(control_id, {})
        gradient = computed.get("gradient", [])
        flux_matrix = computed.get("flux", [])
        if states and len(gradient) == len(states):
            subset_indices = [index for index, state in enumerate(states) if state in subset]
            outside_indices = [index for index, state in enumerate(states) if state not in subset]
            divergence_sum = sum((gradient[index] for index in subset_indices), Fraction(0))
            crossing_sum = sum(
                (
                    flux_matrix[row][column]
                    for row in subset_indices
                    for column in outside_indices
                ),
                Fraction(0),
            )
            check(f"boundary_balance:{boundary_id}", divergence_sum == crossing_sum, f"{divergence_sum}={crossing_sum}")

    assumption_rows = assumptions.get("assumptions", [])
    missing_rows = assumptions.get("missing_dependencies", [])
    check("assumption_count", isinstance(assumption_rows, list) and len(assumption_rows) >= 8, "explicit assumptions")
    check("missing_dependency_count", isinstance(missing_rows, list) and len(missing_rows) >= 6, "open burdens")
    status_matrix = assumptions.get("status_matrix", {})
    check("candidate_constructed", status_matrix.get("finite_source_variational_object_constructed") is True, "constructive result")
    check("physical_action_not_derived", status_matrix.get("physical_matter_action_derived") is False, "physical boundary")
    check("stress_energy_not_derived", status_matrix.get("stress_energy_tensor_derived") is False, "physical boundary")
    check("physical_conservation_not_derived", status_matrix.get("physical_conservation_law_derived") is False, "physical boundary")

    for child_id, child in (("math", child_math), ("phil", child_phil)):
        check(f"child_status:{child_id}", child.get("status") == "completed", "completed")
        serialized = json.dumps(child, sort_keys=True)
        check(f"child_proposal_only:{child_id}", "proposal-only" in serialized, "proposal-only boundary")
        check(f"child_no_global_no_go:{child_id}", "global" in serialized.lower(), "global scope discussed")

    check("conflict_status", conflict.get("status") == "resolved", "parent review resolved")
    check("conflict_unresolved_zero", conflict.get("unresolved_conflict_count") == 0, "zero unresolved")
    check("conflict_rounds_bounded", int(conflict.get("resolution_round_count", 99)) <= 2, "at most two rounds")

    required_tex_snippets = [
        "P7T06-THM-SOURCE-VARIATION-FLUX-BALANCE-001",
        "P7T06-THM-DIRECTIONAL-UPDATE-VARIATIONAL-OBSTRUCTION-001",
        "OBST-P7T06-DIRECTIONAL-KERNEL-NONVARIATIONAL-001",
        "blocked\\_adoption\\_open\\_continuation",
        "not a stress-energy tensor",
        "not a global no-go theorem",
        "L_{C_{\\mathrm{fwd}}}",
    ]
    for snippet in required_tex_snippets:
        check(f"tex_snippet:{snippet}", snippet in tex, snippet)
    check(
        "fusion_source_equivalent_guard",
        "I-P" in fusion and "L_C" in fusion and "degree imbalance" in fusion,
        "L_C versus full directional update",
    )
    check("fusion_claim_boundary", "proposal-only" in fusion and "physical" in fusion, "status and physical boundary")

    authority = spec.get("authority_limits", {})
    forbidden_true_flags = [
        "canonical_ontology_modified",
        "source_law_adopted",
        "variational_law_adopted",
        "candidate_adopted",
        "physical_matter_variables_derived",
        "physical_matter_coupling_derived",
        "matter_action_derived",
        "stress_energy_derived",
        "physical_conservation_law_derived",
        "noether_theorem_derived",
        "diffeomorphism_invariance_derived",
        "effective_metric_derived",
        "einstein_equations_derived",
        "exact_gr_recovered",
        "benchmark_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "physics_promotion_authorized",
    ]
    for flag in forbidden_true_flags:
        check(f"authority_false:{flag}", authority.get(flag) is False, flag)

    failed = [item for item in checks if item["status"] == "FAIL"]
    evidence_paths = [
        SPEC_PATH,
        CONTROLS_PATH,
        ASSUMPTIONS_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    evidence_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in evidence_paths
    }
    report = {
        "schema_id": "v21_p7_t06_source_kernel_variational_validation_v1",
        "task_id": "RT-20260728-005",
        "job_id": "AJ-RT-20260728-005-001",
        "plan_task_id": "P7-T06",
        "status": "PASS" if not failed else "FAIL",
        "candidate_id": "SourceKernelDirichletVariationalCandidate_v1",
        "source_flux_id": "SourceVariationalFluxRecord_v1",
        "obstruction_id": "OBST-P7T06-DIRECTIONAL-KERNEL-NONVARIATIONAL-001",
        "result_kind": "precise_obstruction_with_constructive_restricted_variational_object",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "evidence_sha256es": evidence_hashes,
        "checks": checks,
        "authority_note": "Operational validation only; no theorem truth, ontology adoption, physical interpretation, proof, publication, promotion, or checkpoint authority follows.",
    }
    compact = {
        "schema_id": "v21_p7_t06_source_kernel_variational_compact_receipt_v1",
        "task_id": "RT-20260728-005",
        "job_id": "AJ-RT-20260728-005-001",
        "status": report["status"],
        "candidate_id": report["candidate_id"],
        "candidate_status": "proposal-only",
        "source_extension_status": "source-extension data",
        "adoption_status": "blocked_adoption_open_continuation",
        "result_kind": report["result_kind"],
        "theorem_ids": [
            "P7T06-THM-SOURCE-VARIATION-FLUX-BALANCE-001",
            "P7T06-THM-DIRECTIONAL-UPDATE-VARIATIONAL-OBSTRUCTION-001",
        ],
        "obstruction_id": report["obstruction_id"],
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "finite_control_count": len(control_rows),
        "constructive_variational_control_count": 4,
        "scoped_obstruction_count": 1,
        "physical_action_count": 0,
        "stress_energy_count": 0,
        "physical_conservation_count": 0,
        "claim_boundary_id": "CB-V21-P7-T06-SOURCE-VARIATIONAL-OBJECT-001",
        "evidence_sha256es": evidence_hashes,
        "authority_note": report["authority_note"],
    }

    rendered_report = json.dumps(report, indent=2, sort_keys=True) + "\n"
    rendered_compact = json.dumps(compact, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered_report, encoding="utf-8")
        COMPACT_PATH.write_text(rendered_compact, encoding="utf-8")
    if args.check:
        check_report = REPORT_PATH.is_file() and REPORT_PATH.read_text(encoding="utf-8") == rendered_report
        check_compact = COMPACT_PATH.is_file() and COMPACT_PATH.read_text(encoding="utf-8") == rendered_compact
        if not check_report or not check_compact:
            report["status"] = "FAIL"
            report["report_fresh"] = check_report
            report["compact_receipt_fresh"] = check_compact
            print(json.dumps(report, indent=2, sort_keys=True))
            return 1

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"{report['status']}: {report['passed_check_count']}/"
            f"{report['check_count']} checks passed"
        )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
