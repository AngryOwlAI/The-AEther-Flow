#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "non_empirical_ontology_success_criteria_validation.json"
CRITERIA = (
    "assumption_compression",
    "unification",
    "inevitability",
    "explanatory_depth",
    "dimension_and_signature_explanation",
    "matter_or_quantum_connection",
    "problem_solving_fertility",
)
STATUS_DOMAIN = {"met", "not_met", "indeterminate"}
FALSE_AUTHORITY_KEYS = (
    "canonical_ontology_modified",
    "ontology_selected",
    "ontology_adopted",
    "ontology_rejected",
    "scientific_status_changed",
    "distance_to_gr_changed",
    "physics_promotion_authorized",
    "proof_authority",
    "publication_authority",
    "gate_chair_authority",
    "p14_t03_executed",
    "completed_derivation_claimed",
)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append(
            {"check": name, "status": "PASS" if condition else "FAIL", "detail": detail}
        )

    tex_path = ARTIFACT_DIR / "non_empirical_ontology_success_criteria_v1.tex"
    guide_path = ARTIFACT_DIR / "ontology_success_scoring_prohibition_and_evidence_guide_v1.yaml"
    assessment_path = ARTIFACT_DIR / "current_non_empirical_ontology_assessment_v1.yaml"
    math_path = ARTIFACT_DIR / "child_phys_math_non_empirical_ontology_success_criteria.yaml"
    phil_path = ARTIFACT_DIR / "child_phys_phil_non_empirical_ontology_success_criteria.yaml"
    review_path = ARTIFACT_DIR / "parent_conflict_review_non_empirical_ontology_success_criteria.yaml"
    fusion_path = ARTIFACT_DIR / "parent_fusion_notes_non_empirical_ontology_success_criteria.md"
    required = (
        tex_path,
        guide_path,
        assessment_path,
        math_path,
        phil_path,
        review_path,
        fusion_path,
    )
    for path in required:
        check(
            f"exists:{path.name}",
            path.is_file() and not path.is_symlink(),
            "required regular task-local artifact",
        )
    if not all(path.is_file() for path in required):
        return finish(checks)

    tex = tex_path.read_text(encoding="utf-8")
    guide = load_yaml(guide_path)
    assessment = load_yaml(assessment_path)
    math_child = load_yaml(math_path)
    phil_child = load_yaml(phil_path)
    review = load_yaml(review_path)
    fusion = fusion_path.read_text(encoding="utf-8")

    for marker in (
        "Assumption compression",
        "Unification",
        "Inevitability",
        "Explanatory depth",
        "Dimension-and-signature explanation",
        "Matter-or-quantum connection",
        "Problem-solving fertility",
        "NEO-NONCOMPENSATION-PROPOSITION-V1",
        "workflow output",
        "not a theorem of impossibility",
    ):
        check(f"tex_marker:{marker}", marker in tex, "required formalization marker")

    check(
        "guide_criterion_order",
        tuple(guide.get("criterion_order", [])) == CRITERIA,
        "exact seven criterion families",
    )
    check(
        "guide_status_domain",
        set(guide.get("status_domain", [])) == STATUS_DOMAIN,
        "exact tri-valued status domain",
    )
    criteria = guide.get("criteria", {})
    check(
        "guide_criteria_exact",
        isinstance(criteria, dict) and set(criteria) == set(CRITERIA),
        "guide has exact criterion keys",
    )
    for criterion in CRITERIA:
        block = criteria.get(criterion, {}) if isinstance(criteria, dict) else {}
        for field in (
            "operational_definition",
            "required_evidence",
            "evidence_example",
            "counterexample",
            "aesthetic_or_process_trap",
            "future_material_evidence",
        ):
            value = block.get(field)
            check(
                f"guide_field:{criterion}:{field}",
                bool(value) and (not isinstance(value, list) or len(value) >= 2),
                "criterion includes evidence example counterexample and improvement path",
            )
    prohibition = guide.get("scoring_prohibition", {})
    for key in (
        "scalar_score_authorized",
        "weighted_sum_authorized",
        "total_ranking_authorized",
        "compensatory_tradeoff_authorized",
    ):
        check(f"scoring_false:{key}", prohibition.get(key) is False, "no scalar collapse")

    vector = assessment.get("current_vector", {})
    check(
        "assessment_component_order",
        tuple(vector.get("component_order", [])) == CRITERIA,
        "assessment uses exact criterion order",
    )
    values = vector.get("values", {})
    check(
        "assessment_vector_exact",
        isinstance(values, dict)
        and set(values) == set(CRITERIA)
        and all(value in STATUS_DOMAIN for value in values.values()),
        "current vector is complete and tri-valued",
    )
    check(
        "assessment_current_boundary",
        values
        == {
            "assumption_compression": "not_met",
            "unification": "not_met",
            "inevitability": "not_met",
            "explanatory_depth": "not_met",
            "dimension_and_signature_explanation": "not_met",
            "matter_or_quantum_connection": "not_met",
            "problem_solving_fertility": "indeterminate",
        },
        "current assessment preserves the source-grounded evidence boundary",
    )
    for criterion in CRITERIA:
        block = assessment.get("criteria_assessment", {}).get(criterion, {})
        check(
            f"assessment_evidence:{criterion}",
            len(block.get("evidence", [])) >= 2
            and bool(block.get("limitation"))
            and bool(block.get("material_improvement")),
            "assessment cites evidence limitation and material improvement",
        )
    check(
        "alternatives_not_selected",
        assessment.get("alternative_comparison", {})
        .get("continuum_first_premetric", {})
        .get("selected_or_adopted")
        is False
        and assessment.get("alternative_comparison", {})
        .get("emergence_first_process_order", {})
        .get("selected_or_adopted")
        is False,
        "fixed alternatives remain proposal-only and unselected",
    )
    check(
        "distance_no_delta",
        assessment.get("distance_to_gr_status", {}).get("ledger_changed") is False,
        "no Distance-to-GR mutation",
    )
    payload_ids = {
        item.get("payload_id")
        for item in assessment.get("new_mathematical_payload", [])
        if isinstance(item, dict)
    }
    check(
        "new_payloads",
        {
            "NEO-EVIDENCE-CERTIFICATE-V1",
            "NEO-SEVEN-COORDINATE-STATUS-VECTOR-V1",
            "NEO-NONCOMPENSATION-PROPOSITION-V1",
        }.issubset(payload_ids),
        "completion has new mathematical payload",
    )

    for label, child in (("math", math_child), ("phil", phil_child)):
        check(
            f"child_task:{label}",
            child.get("task_id") == "RT-20260722-018",
            "child is bound to the single outer task",
        )
        child_text = json.dumps(child, sort_keys=True).lower()
        check(
            f"child_scope:{label}",
            "draft/control" in child_text
            and "physics_promotion_authorized" in child_text,
            "child preserves draft/control authority",
        )
    check(
        "math_noncompensation",
        "noncompensation" in json.dumps(math_child, sort_keys=True).lower()
        or "no_compensation" in json.dumps(math_child, sort_keys=True).lower(),
        "mathematical child contributes non-compensation analysis",
    )
    check(
        "phil_metric_guard",
        "workflow" in json.dumps(phil_child, sort_keys=True).lower()
        and "aesthetic" in json.dumps(phil_child, sort_keys=True).lower(),
        "philosophical child separates ontology value from aesthetics and workflow",
    )
    check(
        "conflict_review_pass",
        review.get("status") == "PASS"
        and review.get("unresolved_blocking_conflicts") == 0,
        "parent fusion has no unresolved blocking conflict",
    )
    check(
        "fusion_names_children",
        "child_phys_math" in fusion and "child_phys_phil" in fusion,
        "fusion notes preserve both internal units",
    )

    for source, expected in (
        (
            REPO_ROOT
            / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
            "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
        ),
        (
            REPO_ROOT / "research_control/handoffs/handoff-0826.yaml",
            "35359a4a2c10b3cc9209a00ed1725ca940406c2aea4cbd44d55420cb4ea860a0",
        ),
        (
            REPO_ROOT
            / "research_control/tasks/RT-20260722-016/artifacts/four_project_success_categories_v1.tex",
            "03d2658ad7a1508776ed25f1b00b7446c04f8c76e16b2f1acfd7e6c06ddaf00e",
        ),
        (
            REPO_ROOT
            / "research_control/tasks/RT-20260720-030/artifacts/comprehensive_source_assumption_ledger_v1.tex",
            "e50fb9458ee601563a0decc8dc809e719ec4e1d6b62c0682d1175ad2f91a1d90",
        ),
        (
            REPO_ROOT
            / "research_control/tasks/RT-20260721-002/artifacts/ontology_regime_comparison_report_v1.md",
            "5dd5526ebdce949ff121f4aa2785e665e006b5e9fec5f8b1d72877d7da26b7ae",
        ),
    ):
        check(
            f"source_hash:{source.name}:{expected[:8]}",
            source.is_file() and sha256(source) == expected,
            "exact source or dependency identity",
        )

    for label, block in (
        ("guide", guide.get("authority_limits", {})),
        ("assessment", assessment.get("claim_boundary", {})),
    ):
        for key in FALSE_AUTHORITY_KEYS:
            check(
                f"authority_false:{label}:{key}",
                block.get(key) is False,
                "protected authority remains false",
            )

    tex_registry = (REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv").read_text(
        encoding="utf-8"
    )
    check(
        "tex_registered",
        "TEX-V21-P14-T02-NON-EMPIRICAL-ONTOLOGY-SUCCESS-CRITERIA-V1"
        in tex_registry
        and str(tex_path.relative_to(REPO_ROOT)) in tex_registry,
        "fused TeX has a source-registry row",
    )
    return finish(checks)


def finish(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "p14_t02_non_empirical_ontology_success_criteria_validation_v1",
        "task_id": "RT-20260722-018",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "authority_boundary": "Operational validation does not establish ontology value ontology adoption physical interpretation Distance-to-GR progress promotion publication or completed derivation.",
    }


def canonical_text(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    rendered = canonical_text(result)
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    if args.check:
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != rendered:
            result = dict(result)
            result["status"] = "FAIL"
            result["report_fresh"] = False
        else:
            result = dict(result)
            result["report_fresh"] = True
    if args.json or not (args.write_report or args.check):
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
