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
REPORT_PATH = ARTIFACT_DIR / "no_target_sufficiency_validation_report.json"
DIMENSIONS = (
    "source_derivation",
    "uniqueness_or_quotient",
    "naturality",
    "dynamics",
    "operational_systems",
    "robustness",
    "independent_review",
)
GATES = ("gate_a", "gate_b", "gate_c", "gate_d")
FALSE_AUTHORITY_KEYS = (
    "canonical_ontology_modified",
    "scientific_status_changed",
    "distance_to_gr_changed",
    "physics_promotion_authorized",
    "proof_authority",
    "publication_authority",
    "completed_derivation_claimed",
)


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finish(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "v21_p14_t03_no_target_sufficiency_validation_v1",
        "task_id": "RT-20260722-019",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "authority_boundary": (
            "Operational validation does not establish theorem truth, physical "
            "meaning, gate readiness, ontology adoption, Distance-to-GR progress, "
            "promotion, publication, or completed derivation."
        ),
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append(
            {"check": name, "status": "PASS" if condition else "FAIL", "detail": detail}
        )

    tex_path = ARTIFACT_DIR / "no_target_positive_provenance_sufficiency_policy_v1.tex"
    examples_path = ARTIFACT_DIR / "worked_candidate_examples_v1.yaml"
    mapping_path = ARTIFACT_DIR / "gate_a_d_positive_evidence_mapping_v1.yaml"
    math_path = ARTIFACT_DIR / "child_phys_math_no_target_sufficiency.yaml"
    phil_path = ARTIFACT_DIR / "child_phys_phil_no_target_sufficiency.yaml"
    review_path = ARTIFACT_DIR / "parent_conflict_review_no_target_sufficiency.yaml"
    fusion_path = ARTIFACT_DIR / "parent_fusion_notes_no_target_sufficiency.md"
    required = (
        tex_path,
        examples_path,
        mapping_path,
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
    examples = load_yaml(examples_path)
    mapping = load_yaml(mapping_path)
    math_child = load_yaml(math_path)
    phil_child = load_yaml(phil_path)
    review = load_yaml(review_path)
    fusion = fusion_path.read_text(encoding="utf-8")

    for marker in (
        "NT-POSITIVE-SUFFICIENCY-THEOREM-V1",
        "Source-pure mathematics remains admissible",
        "Gate A through D evidence mapping",
        "Status-preserving applications",
        "theorem-inventory guidance",
        "not a new physical law",
    ):
        check(f"tex_marker:{marker}", marker in tex, "required policy marker")
    for symbol in ("\\Ready_g(x) :=", "\\Promote_g(x) :=", "w_{\\NT}", "w_{\\Review}"):
        check(f"tex_formal:{symbol}", symbol in tex, "formal theorem and countermodel marker")

    check(
        "example_dimension_order",
        tuple(examples.get("dimension_order", [])) == DIMENSIONS,
        "exact seven positive-evidence dimensions",
    )
    example_rows = examples.get("examples", [])
    check(
        "example_count",
        isinstance(example_rows, list) and len(example_rows) >= 6,
        "worked examples include current objects and finite countermodels",
    )
    expected_classes = {
        "finite source-pure mathematical candidate",
        "M_src",
        "scoped metric structure record",
        "matter profile",
        "selector or quotient candidate family",
        "finite policy countermodel",
    }
    check(
        "example_classes",
        {row.get("object_class") for row in example_rows if isinstance(row, dict)}
        == expected_classes,
        "exact required worked example classes",
    )
    for index, row in enumerate(example_rows):
        if not isinstance(row, dict):
            check(f"example_mapping:{index}", False, "each example is a mapping")
            continue
        check(
            f"status_preserved:{row.get('example_id', index)}",
            row.get("source_status_before") == row.get("source_status_after"),
            "current scoped status is preserved",
        )
        check(
            f"promotion_false:{row.get('example_id', index)}",
            row.get("physical_promotion_authorized") is False,
            "no example grants physical promotion",
        )
        dimensions = row.get("positive_dimensions", {})
        check(
            f"dimensions_exact:{row.get('example_id', index)}",
            isinstance(dimensions, dict) and set(dimensions) == set(DIMENSIONS),
            "each example exposes every positive dimension",
        )
        check(
            f"outcome_and_overread:{row.get('example_id', index)}",
            bool(row.get("policy_outcome")) and bool(row.get("forbidden_overread")),
            "each example records a policy outcome and blocked overread",
        )
    guidance = examples.get("inventory_guidance", {})
    check(
        "inventory_no_autofill",
        guidance.get("auto_fill_positive_dimensions_from_no_target") is False
        and guidance.get("globalize_scoped_obstruction") is False,
        "theorem inventory keeps purity and positive evidence separate",
    )
    check(
        "source_pure_math_retained",
        examples.get("claim_boundary", {}).get("source_pure_mathematics_rejected")
        is False,
        "source-pure mathematics is not rejected",
    )

    check(
        "mapping_dimensions",
        tuple(mapping.get("positive_dimension_order", [])) == DIMENSIONS,
        "gate map uses exact seven dimensions",
    )
    shared = mapping.get("shared_policy", {})
    for key, expected in (
        ("no_target_purity_required_for_evidence_complete", True),
        ("no_target_purity_sufficient_for_evidence_complete", False),
        ("validator_receipt_sufficient_for_evidence_complete", False),
        ("evidence_complete_is_protected_verdict", False),
        ("protected_verdict_required_after_evidence_completion", True),
        ("one_gate_auto_satisfies_downstream_gate", False),
    ):
        check(f"shared_policy:{key}", shared.get(key) is expected, "exact policy flag")
    gates = mapping.get("gates", {})
    check(
        "gate_keys",
        isinstance(gates, dict) and tuple(gates) == GATES,
        "exact ordered Gate A through D map",
    )
    for gate in GATES:
        block = gates.get(gate, {}) if isinstance(gates, dict) else {}
        check(
            f"gate_dimensions:{gate}",
            set(block.get("positive_dimension_application", {})) == set(DIMENSIONS),
            "each gate maps all seven positive dimensions",
        )
        check(
            f"gate_no_verdict:{gate}",
            block.get("current_verdict") == "not_issued_by_p14_t03",
            "P14-T03 issues no gate verdict",
        )
        check(
            f"gate_minimum_and_block:{gate}",
            len(block.get("minimum_evidence", [])) >= 5 and bool(block.get("blocked_overread")),
            "gate retains minimum evidence and downstream block",
        )

    for label, child in (("math", math_child), ("phil", phil_child)):
        child_text = json.dumps(child, sort_keys=True).lower()
        check(
            f"child_task:{label}",
            child.get("task_id") == "RT-20260722-019",
            "child is bound to the one outer task",
        )
        check(
            f"child_scope:{label}",
            "draft/control" in child_text
            and "physics_promotion_authorized" in child_text,
            "child preserves draft/control authority",
        )
    math_text = json.dumps(math_child, sort_keys=True).lower()
    check(
        "math_theorem_and_countermodel",
        "necessary" in math_text
        and ("insufficient" in math_text or "not-sufficient" in math_text)
        and "countermodel" in math_text,
        "mathematical child supplies theorem and countermodels",
    )
    phil_text = json.dumps(phil_child, sort_keys=True).lower()
    check(
        "phil_overread_and_gate_mapping",
        "overread" in phil_text
        and all(gate.replace("_", " ") in phil_text or gate in phil_text for gate in GATES),
        "philosophical child separates overreads across Gate A through D",
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
            REPO_ROOT / "research_control/handoffs/handoff-0827.yaml",
            "3d658113c6eaf10210c50a55aa5ac8acfdfd9aa1bb30b3ffdc71a7231f1d5b66",
        ),
        (
            REPO_ROOT
            / "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md",
            "7d679cbcbc05bf771333ba7d3afddb351159b87d0edd92e720942428389b62c6",
        ),
        (
            REPO_ROOT
            / "research_control/tasks/RT-20260722-016/artifacts/four_project_success_categories_v1.tex",
            "03d2658ad7a1508776ed25f1b00b7446c04f8c76e16b2f1acfd7e6c06ddaf00e",
        ),
        (
            REPO_ROOT / "ontology/tex/aether_flow_foundations.tex",
            "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
        ),
        (
            REPO_ROOT / "ontology/tex/aether_flow_geometry.tex",
            "ad43e3408fe2d9686a52a71de7ab8326668e8f04ebe2d2845986898b7d2c000f",
        ),
        (
            REPO_ROOT / "research_control/design/epistemic_category_glossary.md",
            "036596ccc2f35b3e0693b08e0968e1ca212b032b426c4f7106e6c766f92bb4a3",
        ),
        (
            REPO_ROOT
            / "research_control/design/public_status_exists_does_not_exist_source_spec.md",
            "394442ee1f03cf1d6578f777fa4f56a68e110989365ff936e54058cb5d3ff126",
        ),
        (
            REPO_ROOT / "research_control/design/scoped_positive_claim_vocabulary.md",
            "d588561071cce453663dbbb29a38e1befa9a95dd179c438a63c17ab9a6961193",
        ),
    ):
        check(
            f"source_hash:{source.name}:{expected[:8]}",
            source.is_file() and sha256(source) == expected,
            "exact source or dependency identity",
        )

    for label, block in (
        ("examples", examples.get("claim_boundary", {})),
        ("mapping", mapping.get("authority_limits", {})),
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
        "TEX-V21-P14-T03-NO-TARGET-POSITIVE-SUFFICIENCY-POLICY-V1"
        in tex_registry
        and str(tex_path.relative_to(REPO_ROOT)) in tex_registry,
        "fused TeX has a source-registry row",
    )
    return finish(checks)


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
