#!/usr/bin/env python3
"""Validate and summarize the bounded P6-T08 Gate B review packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260727-004"
ART = TASK / "artifacts"
VALIDATOR_PATH = Path(__file__).resolve()
REVIEW_PATH = ART / "p6_t08_gate_b_external_red_team_review_v1.yaml"
CERTIFICATE_PATH = ART / "p6_t08_gate_b_separating_certificate_v1.yaml"
PROVENANCE_PATH = ART / "p6_t08_gate_b_positive_provenance_record_v1.yaml"
INVENTORY_PATH = ART / "p6_t08_theorem_inventory_and_route_v1.yaml"
CHILD_MATH_PATH = ART / "child_phys_math_p6_t08_gate_b_review.yaml"
CHILD_PHIL_PATH = ART / "child_phys_phil_p6_t08_gate_b_review.yaml"
CONFLICT_PATH = ART / "parent_conflict_review_p6_t08_gate_b_review.yaml"
FUSION_PATH = ART / "parent_fusion_notes_p6_t08_gate_b_review.md"
RECEIPT_MD_PATH = ART / "p6_t08_gate_b_review_receipt.md"
COMPACT_PATH = ART / "p6_t08_gate_b_review_compact_receipt_v1.json"
REPORT_PATH = ART / "p6_t08_gate_b_review_validation_v1.json"
POSITIVE_VALIDATOR_PATH = (
    ROOT
    / "research_control/tasks/RT-20260722-007/artifacts/validate_positive_provenance_gate.py"
)

FIXED_SOURCES = {
    "research_control/tasks/RT-20260726-002/artifacts/causal_characteristic_target_v1.tex": "32a055bc5c851f0a36d726343cb5be1f1d68cf72a5a32fccead12b3488f04273",
    "research_control/tasks/RT-20260726-003/artifacts/source_local_transport_candidate_v1.tex": "7b446c8660410e655166c0b3124fc37aad9edb8e49b7df2afdc9911c6f560958",
    "research_control/tasks/RT-20260726-005/artifacts/one_ray_conformal_insufficiency_v1.tex": "007ae324872868b9eb9cdf0ebc4f1131737c71eda9ce301c805acd5041a52bac",
    "research_control/tasks/RT-20260726-007/artifacts/source_scale_calibration_nonselection_v1.tex": "96a527cccb8e7a6a614debc5110902b1587848178af8444fc02acda52caf4d28",
    "research_control/tasks/RT-20260726-009/artifacts/signature_covariance_naturality_obstruction_v1.tex": "d7e116d553b1d8a28d5168d7f268c86301161493d08f50a4741573e154e7d4b4",
    "research_control/tasks/RT-20260726-010/artifacts/uniqueness_covariance_robustness_admissibility_obstruction_v1.tex": "a9c307207ede1d04825c73d5f3ff7e081f27ce15ebf4aac4d6041aae4873aa8a",
    "research_control/tasks/RT-20260726-010/artifacts/physical_admissibility_matrix_v1.yaml": "7a083affc67510b21186a4474f2404898803dd187fe0c342090e4eb81362e298",
    "research_control/tasks/RT-20260726-011/artifacts/gate_b_readiness_verdict_v1.yaml": "f62e03fe10610cbe0f37c4160e95ac7631f3c75c090ab5c2f6af1fb53babace9",
    "research_control/tasks/RT-20260726-011/artifacts/metric_object_naming_decision_v1.yaml": "4d67563b2444cfed2bd430e9d027337f26656701624d532f7cb2e357cbac2452",
    "research_control/tasks/RT-20260726-011/jobs/completions/AJC-AJ-RT-20260726-011-001.yaml": "1f3f63be970233ed14924d262239016dac93c58feb25884b93717f36b361f51c",
    "research_control/handoffs/handoff-0885.yaml": "52aec390648b2afeec93ba8a5cbf3030efd7bb95ac823da7c3eab6f656f33b38",
    "research_control/tasks/RT-20260614-216/artifacts/245_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_OR_OBSTRUCTION.tex": "dd30573519ed1df66b3800d29ee0adc9fcc94d9c8d3b9b5a7fcffde503d5f0ef",
    "research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex": "3ce8cbc6cd79c6852d78f81045633beea44c4dfc6e2912c604b08e3c8bdb0257",
    "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md": "7d679cbcbc05bf771333ba7d3afddb351159b87d0edd92e720942428389b62c6",
    "ontology/tex/aether_flow_geometry.tex": "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a YAML map")
    return value


def load_positive_validator() -> Any:
    spec = importlib.util.spec_from_file_location(
        "validate_positive_provenance_gate", POSITIVE_VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load positive-provenance validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate() -> tuple[dict[str, Any], dict[str, Any]]:
    review = load_yaml(REVIEW_PATH)
    certificate = load_yaml(CERTIFICATE_PATH)
    provenance = load_yaml(PROVENANCE_PATH)
    inventory = load_yaml(INVENTORY_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)

    checks: list[dict[str, str]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for relative, expected in FIXED_SOURCES.items():
        path = ROOT / relative
        check(
            f"fixed_source_hash:{relative}",
            path.is_file() and sha256(path) == expected,
            f"expected_sha256={expected}",
        )

    check(
        "review_verdict",
        review.get("verdict") == "freeze_recommended",
        "The fused route verdict is freeze_recommended.",
    )
    check(
        "review_route",
        review.get("recommended_next_route")
        == "P15-T04 publication-preparation-packet",
        "P15-T04 is selected and P7 is not entered.",
    )
    context = review.get("review_context", {})
    claims = context.get("claims", {}) if isinstance(context, dict) else {}
    check(
        "review_context",
        context.get("classification") == "same_context_role_review"
        and context.get("review_executed") is True
        and context.get("replication_executed") is False,
        "Review provenance is calibrated as executed same-context role review.",
    )
    check(
        "independence_nonclaim",
        claims.get("external_review_completed") is False
        and claims.get("human_expert_review_completed") is False
        and claims.get("independent_replication_completed") is False,
        "No external, human-expert, or independent-replication claim is made.",
    )
    check(
        "process_evidence_excluded",
        review.get("workflow_success_disregarded_as_evidence") is True
        and review.get("validator_success_disregarded_as_evidence") is True,
        "Workflow and validator success are excluded from scientific evidence.",
    )
    countermodel = review.get("minimal_countermodel_attempt", {})
    check(
        "minimal_countermodel",
        countermodel.get("attempted") is True
        and countermodel.get("result") == "countermodel_found"
        and countermodel.get("artifact_path")
        == "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml",
        "The fixed-source separating family pressures the readiness implication.",
    )

    matrix = certificate.get("gate_b_matrix", {})
    p7 = certificate.get("p7_input_disposition", {})
    check(
        "gate_b_matrix",
        matrix.get("criterion_count") == 8
        and matrix.get("met_count") == 0
        and len(matrix.get("unmet", [])) == 8,
        "All eight Gate B criteria are explicitly evaluated and unmet.",
    )
    check(
        "p7_input_absent",
        p7.get("lawful_effective_geometry_input_exists") is False
        and p7.get("p7_t01_selected") is False,
        "No lawful P7 effective-geometry input is recorded.",
    )
    integrated = certificate.get("integrated_statement", {})
    check(
        "scoped_obstruction",
        certificate.get("obstruction_id")
        == "OBST-P6T08-LAWFUL-EFFECTIVE-GEOMETRY-INPUT-ABSENT-001"
        and integrated.get("global_no_go_claimed") is False
        and integrated.get("future_source_extension_impossibility_claimed")
        is False,
        "The obstruction remains exact, scoped, and non-global.",
    )
    check(
        "reopening_classes",
        len(certificate.get("freeze", {}).get("reopening_classes", [])) == 4,
        "The local freeze preserves four materially distinct reopening classes.",
    )

    positive_module = load_positive_validator()
    contract = positive_module.extract_contract()
    positive_result = positive_module.validate_record(provenance, contract)
    check(
        "positive_provenance_shape",
        positive_result.get("valid") is True,
        f"errors={positive_result.get('errors', [])}",
    )
    check(
        "positive_provenance_not_ready",
        positive_result.get("evidence_complete") is False
        and provenance.get("outcome") == "not_ready",
        f"blockers={positive_result.get('blocker_ids', [])}",
    )
    independent = provenance.get("dimensions", {}).get("independent_review", {})
    check(
        "positive_provenance_review_class",
        independent.get("status") == "same_context_role_review",
        "Same-context review cannot complete the independent-review dimension.",
    )

    check(
        "child_math",
        child_math.get("verdict") == "not_enough_assumptions"
        and child_math.get("gate_b_result", {}).get("met_count") == 0,
        "The mathematical arm records exact missing assumptions.",
    )
    check(
        "child_phil",
        child_phil.get("verdict") == "freeze_recommended"
        and child_phil.get("review_provenance_finding", {}).get(
            "gate_b_independent_review_dimension_met"
        )
        is False,
        "The interpretation arm records the local freeze and provenance limit.",
    )
    check(
        "conflict_resolution",
        conflict.get("status") == "resolved"
        and conflict.get("resolution_rounds") == 1
        and conflict.get("unresolved_conflicts") == []
        and conflict.get("selected_next_plan_task_id") == "P15-T04",
        "Parent synthesis preserves and resolves both child dispositions.",
    )
    route = inventory.get("route", {})
    check(
        "inventory_route",
        len(inventory.get("inventory", [])) == 8
        and route.get("selected_plan_task_id") == "P15-T04"
        and route.get("p7_t01_selected") is False,
        "The theorem inventory records eight objects and the lawful route.",
    )

    false_flags = [
        "physics_promotion_authorized",
        "gate_chair_authority_created",
        "source_law_adopted",
        "metric_data_adopted",
        "geff_adopted_or_expanded",
        "coupling_law_adopted",
        "matter_coupling_derived_or_adopted",
        "stress_energy_semantics_imported",
        "detector_semantics_imported",
        "matter_action_imported",
        "einstein_equations_derived",
        "benchmark_promoted",
        "completed_derivation_claimed",
    ]
    check(
        "authority_flags",
        all(review.get(key) is False for key in false_flags),
        "Every protected and promotion authority flag remains false.",
    )
    check(
        "support_files",
        FUSION_PATH.is_file() and RECEIPT_MD_PATH.is_file(),
        "Parent fusion and compact human-readable receipt exist.",
    )

    failures = [row for row in checks if row["status"] != "PASS"]
    task_artifact_paths = [
        REVIEW_PATH,
        CERTIFICATE_PATH,
        PROVENANCE_PATH,
        INVENTORY_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
        RECEIPT_MD_PATH,
    ]
    artifact_hashes = {
        str(path.relative_to(ROOT)): sha256(path) for path in task_artifact_paths
    }
    status = "PASS" if not failures else "FAIL"
    compact = {
        "schema_id": "v21_p6_t08_gate_b_review_compact_receipt_v1",
        "status": status,
        "task_id": "RT-20260727-004",
        "job_id": "AJ-RT-20260727-004-001",
        "plan_task_id": "P6-T08",
        "result_status": "gate_b_not_ready_local_freeze_p15_t04_selected",
        "review_verdict": review.get("verdict"),
        "review_context_classification": context.get("classification"),
        "gate_b_criterion_count": matrix.get("criterion_count"),
        "gate_b_met_count": matrix.get("met_count"),
        "gate_b_unmet_count": len(matrix.get("unmet", [])),
        "separating_witness_count": len(certificate.get("separating_witnesses", [])),
        "theorem_inventory_count": len(inventory.get("inventory", [])),
        "child_review_count": 2,
        "resolved_difference_count": len(conflict.get("preserved_differences", [])),
        "unresolved_conflict_count": len(conflict.get("unresolved_conflicts", [])),
        "lawful_p7_effective_geometry_input_exists": p7.get(
            "lawful_effective_geometry_input_exists"
        ),
        "selected_next_plan_task_id": route.get("selected_plan_task_id"),
        "source_hashes": {**FIXED_SOURCES, **artifact_hashes},
        "validator_ids": [
            "validate_p6_t08_gate_b_review",
            "validate_red_team_review_artifact",
            "v21_positive_provenance_operational_meaning_gate_v1",
        ],
        "validator_sha256": sha256(VALIDATOR_PATH),
        "claim_boundary_summary": "Same-context internal review confirms a precise scoped obstruction and local freeze of the unchanged P6 package as P7 input; it creates no external-review, ontology, metric, coupling, field-equation, benchmark, proof, publication, global-no-go, or completed-derivation authority.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    report = {
        "schema_id": "v21_p6_t08_gate_b_review_validation_v1",
        "status": status,
        "task_id": "RT-20260727-004",
        "job_id": "AJ-RT-20260727-004-001",
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "checks": checks,
        "failures": failures,
        "positive_provenance": {
            "valid": positive_result.get("valid"),
            "evidence_complete": positive_result.get("evidence_complete"),
            "blocker_ids": positive_result.get("blocker_ids", []),
            "errors": positive_result.get("errors", []),
        },
        "compact_receipt_sha256": hashlib.sha256(
            canonical_bytes(compact)
        ).hexdigest(),
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    return compact, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    compact, report = evaluate()
    if args.write_report:
        COMPACT_PATH.write_bytes(canonical_bytes(compact))
        REPORT_PATH.write_bytes(canonical_bytes(report))
    output = {
        "status": report["status"],
        "mode": "write" if args.write_report else "check",
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "compact_receipt_path": str(COMPACT_PATH.relative_to(ROOT)),
        "validation_report_path": str(REPORT_PATH.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(output)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
