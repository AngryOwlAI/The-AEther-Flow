#!/usr/bin/env python3
"""Validate the bounded V22 P2-T01 local information-capacity package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260809-005"
ART = TASK / "artifacts"
VALIDATION = ART / "v22_p2_t01_capacity_validation.json"
RECEIPT = ART / "v22_p2_t01_compact_receipt.json"

REQUIRED_CLASSES = {
    "deterministic",
    "stochastic",
    "quotient_observable",
    "partial_domain",
    "marked_domain",
}
REQUIRED_PROBES = {
    "cone_deformation",
    "anisotropic_tidal_response",
    "polarization_response",
    "clock_rate_shift",
    "volume_shear_variation",
    "curvature_response",
}
REQUIRED_THEOREMS = {
    "V22-P2-T01-QUOTIENT-LOCAL-INFORMATION-CAPACITY-THEOREM-V1",
    "V22-P2-T01-STOCHASTIC-FACTOR-THROUGH-CAPACITY-PROPOSITION-V1",
    "V22-P2-T01-P5-SCALAR-AMPLITUDE-COROLLARY-V1",
    "V22-P2-T01-FINITE-DISTINGUISHABILITY-LEMMA-V1",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def matrix_rank(raw: list[list[Any]]) -> int:
    if not raw:
        return 0
    width = len(raw[0])
    if any(len(row) != width for row in raw):
        raise ValueError("ragged matrix")
    matrix = [[Fraction(value) for value in row] for row in raw]
    rows = len(matrix)
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, rows) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def multiply(left: list[list[Any]], right: list[list[Any]]) -> list[list[Fraction]]:
    if not left or not right:
        return []
    left_width = len(left[0])
    if left_width != len(right):
        raise ValueError(f"incompatible matrix shapes {len(left)}x{left_width} and {len(right)}x{len(right[0])}")
    right_width = len(right[0])
    return [
        [
            sum(Fraction(left[i][k]) * Fraction(right[k][j]) for k in range(left_width))
            for j in range(right_width)
        ]
        for i in range(len(left))
    ]


def nondifferential_verdict(case: dict[str, Any]) -> str:
    if case.get("nondifferential_test") == "finite_distinguishability":
        source_count = int(case.get("discrete_source_class_count", 0))
        required_count = int(case.get("required_output_class_count", 0))
        return (
            "necessary_condition_met_not_sufficient"
            if source_count >= required_count
            else "scoped_obstruction"
        )
    failure = str(case.get("scope_failure", ""))
    if failure in {
        "kernel_has_undeclared_source_dependent_latent_channel",
        "reconstruction_undefined",
    }:
        return "outside_differential_scope"
    return "insufficient_equivalence_or_domain_data"


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    paths = {
        "definitions": ART / "v22_p2_t01_local_state_quotient_definitions_v1.yaml",
        "proof_archive": ART / "v22_p2_t01_proof_countermodel_archive_v1.yaml",
        "checklist": ART / "v22_p2_t01_source_adequacy_checklist_v1.yaml",
        "fixtures": ART / "fixtures/v22_p2_t01_information_capacity_cases.yaml",
        "math_child": ART / "child_phys_math_p2_t01_capacity_theorem.yaml",
        "refuter_child": ART / "child_refuter_p2_t01_scope_audit.yaml",
        "conflict": ART / "parent_conflict_review_p2_t01_capacity.yaml",
        "fusion": ART / "parent_fusion_notes_p2_t01_capacity.md",
        "tex": ART / "v22_p2_t01_local_source_information_capacity_theorem_v1.tex",
    }
    for name, path in paths.items():
        check(f"PATH-{name.upper()}", path.is_file(), str(path.relative_to(ROOT)))

    definitions = load_yaml(paths["definitions"])
    proof_archive = load_yaml(paths["proof_archive"])
    checklist = load_yaml(paths["checklist"])
    fixtures = load_yaml(paths["fixtures"])
    math_child = load_yaml(paths["math_child"])
    refuter_child = load_yaml(paths["refuter_child"])
    conflict = load_yaml(paths["conflict"])
    tex_text = paths["tex"].read_text(encoding="utf-8")
    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    tex_flat = re.sub(r"\s+", " ", tex_text)
    fusion_flat = re.sub(r"\s+", " ", fusion_text)

    snapshot_failures: list[str] = []
    snapshots = definitions.get("source_basis", [])
    for item in snapshots:
        source_path = ROOT / str(item.get("path", ""))
        expected = str(item.get("sha256", ""))
        if not source_path.is_file() or sha256(source_path) != expected:
            snapshot_failures.append(str(item.get("object_id", source_path)))
    check(
        "SOURCE-HASHES",
        not snapshot_failures and len(snapshots) == 5,
        f"snapshot_count={len(snapshots)} failures={snapshot_failures}",
    )

    definition_items = definitions.get("definitions", [])
    definition_ids = {str(item.get("definition_id", "")) for item in definition_items}
    check("DEFINITION-COUNT", len(definition_items) == 11, f"actual={len(definition_items)}")
    check(
        "DEFINITION-QUOTIENTS",
        {"DEF-P2-T01-SOURCE-VERTICAL", "DEF-P2-T01-OUTPUT-VERTICAL", "DEF-P2-T01-QUOTIENT-TANGENTS"} <= definition_ids,
        "source and output quotient objects present",
    )
    incomplete_definitions = [
        item.get("definition_id")
        for item in definition_items
        if not all(item.get(field) for field in ("definition_id", "symbol", "kind", "regularity", "authority", "forbidden_overread"))
    ]
    check("DEFINITION-FIELDS", not incomplete_definitions, f"incomplete={incomplete_definitions}")
    locality = definitions.get("locality_contract", {})
    check(
        "LOCALITY-CONTRACT",
        locality.get("global_quotient_required") is False
        and locality.get("global_section_required") is False
        and locality.get("representative_selection_allowed") is False
        and locality.get("singular_strata_require_separate_analysis") is True,
        "no global quotient or representative assumption",
    )

    physical = definitions.get("physical_distinguishability_contract", {})
    probes = physical.get("probe_slots", [])
    probe_ids = {str(item.get("probe_id", "")) for item in probes}
    check("PROBE-COVERAGE", probe_ids == REQUIRED_PROBES, f"actual={sorted(probe_ids)}")
    check(
        "PROBE-FAIL-CLOSED",
        len(probes) == 6
        and all(item.get("status") == "conditional_not_established" for item in probes)
        and physical.get("admitted_probe_count_in_this_packet") == 0,
        "six conditional slots and zero admitted probes",
    )
    check(
        "PHYSICAL-WITNESSES",
        len(physical.get("common_required_witnesses", [])) == 6,
        "six common witness classes",
    )
    stochastic = definitions.get("stochastic_contract", {})
    check(
        "STOCHASTIC-CONTRACT",
        stochastic.get("regular_dominated_family_required") is True
        and stochastic.get("source_independent_kernel_after_statistic") is True
        and stochastic.get("source_dependent_latent_channel_classification") == "explicit_added_source_capacity"
        and stochastic.get("entropy_or_sample_dimension_claimed") is False,
        "regular tangent-rank scope",
    )

    theorem_items = proof_archive.get("theorems", [])
    theorem_ids = {str(item.get("theorem_id", "")) for item in theorem_items}
    check("THEOREM-COVERAGE", theorem_ids == REQUIRED_THEOREMS, f"actual={sorted(theorem_ids)}")
    check(
        "THEOREM-HYPOTHESES",
        all(item.get("hypotheses") and item.get("conclusion") and item.get("proof_steps") and item.get("forbidden_overread") for item in theorem_items),
        "all results have assumptions proof and scope",
    )
    countermodels = proof_archive.get("countermodels", [])
    escapes = proof_archive.get("escape_route_classification", [])
    check("COUNTERMODEL-COUNT", len(countermodels) == 10, f"actual={len(countermodels)}")
    check("ESCAPE-COUNT", len(escapes) == 9, f"actual={len(escapes)}")
    check(
        "PROOF-ASSISTANT-SCOPE",
        proof_archive.get("proof_assistant", {}).get("used") is False
        and proof_archive.get("proof_assistant", {}).get("build_status") == "not_applicable",
        "no proof-assistant kernel used",
    )
    check(
        "INTERNAL-REVIEW-ONLY",
        proof_archive.get("formal_derivation_review", {}).get("class") == "same_context_internal_ai_review_only"
        and proof_archive.get("formal_derivation_review", {}).get("external_review_completed") is False,
        "same-context nonexternal review",
    )

    checklist_fields = checklist.get("candidate_required_fields", [])
    check("CHECKLIST-FIELDS", len(checklist_fields) == 10 and all(item.get("fail_closed_if_missing") is True for item in checklist_fields), f"actual={len(checklist_fields)}")
    check(
        "CHECKLIST-CASE-COVERAGE",
        set(checklist.get("scope_cases_required", [])) == REQUIRED_CLASSES,
        f"actual={checklist.get('scope_cases_required', [])}",
    )
    check(
        "CHECKLIST-AUTHORITY",
        checklist.get("authority_limits", {}).get("passage_is_sufficient") is False
        and checklist.get("authority_limits", {}).get("hard_candidate_filter_authorized") is False,
        "necessary condition only",
    )

    cases = fixtures.get("cases", [])
    case_failures: list[dict[str, Any]] = []
    class_counts: dict[str, int] = {}
    factor_rank_violations: list[str] = []
    for case in cases:
        case_id = str(case.get("case_id", ""))
        case_class = str(case.get("case_class", ""))
        class_counts[case_class] = class_counts.get(case_class, 0) + 1
        if case.get("theorem_applicable"):
            statistic = case.get("statistic_matrix", [])
            post = case.get("score_post_matrix", case.get("post_matrix", []))
            statistic_rank = matrix_rank(statistic)
            composite_rank = matrix_rank(multiply(post, statistic))
            expected_statistic = int(case.get("expected_statistic_rank", -1))
            expected_composite = int(case.get("expected_score_rank", case.get("expected_composite_rank", -1)))
            required_rank = int(case.get("required_operational_rank", 0))
            actual_verdict = (
                "scoped_obstruction"
                if required_rank > statistic_rank
                else "necessary_condition_met_not_sufficient"
            )
            if composite_rank > statistic_rank:
                factor_rank_violations.append(case_id)
            if statistic_rank != expected_statistic or composite_rank != expected_composite:
                case_failures.append(
                    {
                        "case_id": case_id,
                        "failure": "rank_mismatch",
                        "actual_statistic_rank": statistic_rank,
                        "expected_statistic_rank": expected_statistic,
                        "actual_composite_rank": composite_rank,
                        "expected_composite_rank": expected_composite,
                    }
                )
        else:
            actual_verdict = nondifferential_verdict(case)
        if actual_verdict != case.get("expected_verdict"):
            case_failures.append(
                {
                    "case_id": case_id,
                    "failure": "verdict_mismatch",
                    "actual": actual_verdict,
                    "expected": case.get("expected_verdict"),
                }
            )
        if case_class == "partial_domain" and case.get("global_conclusion_allowed") is not False:
            case_failures.append({"case_id": case_id, "failure": "partial_domain_globalization"})
        if case_class == "marked_domain" and case.get("theorem_applicable") and case.get("mark_is_explicit_source_data") is not True:
            case_failures.append({"case_id": case_id, "failure": "undeclared_mark_counted"})

    expected_counts = fixtures.get("expected_counts", {})
    check("FIXTURE-TOTAL", len(cases) == expected_counts.get("total") == 17, f"actual={len(cases)}")
    check(
        "FIXTURE-CLASS-COVERAGE",
        set(class_counts) == REQUIRED_CLASSES
        and all(class_counts.get(key) == expected_counts.get(key) for key in REQUIRED_CLASSES),
        f"actual={class_counts}",
    )
    check("FACTOR-RANK-BOUND", not factor_rank_violations, f"violations={factor_rank_violations}")
    check("FIXTURE-VERDICTS", not case_failures, f"failures={case_failures}")

    check(
        "MATH-CHILD",
        math_child.get("status") == "completed"
        and math_child.get("review_provenance", {}).get("class") == "same_context_internal_ai_review_only"
        and len(math_child.get("new_mathematical_payload", [])) == 4
        and math_child.get("checks", {}).get("ten_component_argument_used") is False,
        "formal theorem child complete",
    )
    check(
        "REFUTER-CHILD",
        refuter_child.get("status") == "completed"
        and refuter_child.get("review_provenance", {}).get("class") == "same_context_internal_ai_review_only"
        and len(refuter_child.get("attacks", [])) == 9
        and refuter_child.get("result", {}).get("unresolved_blocking_attack_count") == 0,
        "scope audit complete",
    )
    check(
        "PARENT-CONFLICT",
        conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("unresolved_conflicts") == []
        and len(conflict.get("conflicts", [])) == 4,
        "four tensions resolved",
    )
    check(
        "PARENT-FUSION",
        "No blocking conflict remains." in fusion_flat
        and "same-context internal AI review only" in fusion_flat
        and "P2-T03 may be selected" in fusion_flat,
        "fusion preserves consensus novelty and scope",
    )

    required_tex_phrases = [
        "Quotient-local source information-capacity theorem",
        "Source-independent stochastic postprocessing",
        "Protected P5 scalar-amplitude result",
        "Finite distinguishability bound",
        "Expanded Distance-to-GR matrix",
        "physical Distance-to-GR delta is zero",
        "same-context internal AI review only",
        "P2-T03 may separately",
    ]
    missing_tex = [phrase for phrase in required_tex_phrases if phrase not in tex_flat]
    check("TEX-CONTENT", not missing_tex, f"missing={missing_tex}")
    check(
        "TEX-NO-REPRESENTATIVE-ASSUMPTION",
        "This definition never selects a representative" in tex_text
        and "no orbit representative is selected" in tex_text,
        "representative-free induced map",
    )
    check(
        "TEX-P5-SCOPE",
        "scoped local obstruction to that exact" in tex_text
        and "not to all possible source extensions" in tex_text,
        "no global scalar overread",
    )
    check(
        "ZERO-DISTANCE-DELTA",
        proof_archive.get("counts", {}).get("distance_to_gr_delta_count") == 0
        and definitions.get("authority_limits", {}).get("distance_to_gr_changed") is False,
        "no ledger delta",
    )
    check(
        "ZERO-ADOPTION",
        proof_archive.get("counts", {}).get("ontology_adoption_count") == 0
        and definitions.get("authority_limits", {}).get("ontology_or_source_law_adopted") is False,
        "no ontology or source-law adoption",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v22_p2_t01_capacity_validation_v1",
        "task_id": "RT-20260809-005",
        "job_id": "AJ-RT-20260809-005-001",
        "generated_at": "2026-08-09T05:23:44Z",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "source_snapshot_count": len(snapshots),
        "definition_count": len(definition_items),
        "probe_slot_count": len(probes),
        "admitted_probe_count": physical.get("admitted_probe_count_in_this_packet", 0),
        "theorem_count": len(theorem_items),
        "countermodel_count": len(countermodels),
        "escape_route_count": len(escapes),
        "fixture_count": len(cases),
        "fixture_class_counts": class_counts,
        "new_mathematical_payload_count": len(math_child.get("new_mathematical_payload", [])),
        "proof_assistant_kernel_used": False,
        "ontology_adoption_count": 0,
        "distance_to_gr_delta_changed": False,
        "external_review_completed": False,
        "independent_replication_completed": False,
        "checks": checks,
        "failures": failures,
    }


def compact_receipt(result: dict[str, Any], validation_sha256: str) -> dict[str, Any]:
    artifact_paths = [
        ART / "v22_p2_t01_local_source_information_capacity_theorem_v1.tex",
        ART / "v22_p2_t01_local_state_quotient_definitions_v1.yaml",
        ART / "v22_p2_t01_proof_countermodel_archive_v1.yaml",
        ART / "v22_p2_t01_source_adequacy_checklist_v1.yaml",
        ART / "fixtures/v22_p2_t01_information_capacity_cases.yaml",
        ART / "child_phys_math_p2_t01_capacity_theorem.yaml",
        ART / "child_refuter_p2_t01_scope_audit.yaml",
        ART / "parent_conflict_review_p2_t01_capacity.yaml",
        ART / "parent_fusion_notes_p2_t01_capacity.md",
    ]
    return {
        "schema_id": "v22_p2_t01_compact_receipt_v1",
        "task_id": result["task_id"],
        "job_id": result["job_id"],
        "status": result["status"],
        "result": "PASS_V22_P2_T01_LOCAL_SOURCE_INFORMATION_CAPACITY_THEOREM"
        if result["status"] == "PASS"
        else "FAIL_V22_P2_T01_LOCAL_SOURCE_INFORMATION_CAPACITY_THEOREM",
        "validation_sha256": validation_sha256,
        "counts": {
            "check_count": result["check_count"],
            "failed_check_count": result["failed_check_count"],
            "theorem_count": result["theorem_count"],
            "countermodel_count": result["countermodel_count"],
            "escape_route_count": result["escape_route_count"],
            "fixture_count": result["fixture_count"],
            "probe_slot_count": result["probe_slot_count"],
            "admitted_probe_count": result["admitted_probe_count"],
        },
        "artifact_sha256es": {
            str(path.relative_to(ROOT)): sha256(path) for path in artifact_paths
        },
        "authority_limits": {
            "validator_pass_counts_as_physics": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "external_review_completed": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write:
        validation_bytes = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
        VALIDATION.write_bytes(validation_bytes)
        validation_hash = hashlib.sha256(validation_bytes).hexdigest()
        receipt = compact_receipt(result, validation_hash)
        RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
