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
REPORT_PATH = ARTIFACT_DIR / "success_categories_validation_report.json"
CATEGORIES = (
    "interpretive_redescription",
    "formal_or_categorical_equivalence",
    "genuine_emergence",
    "empirical_novelty",
)
STATUS_DOMAIN = {"met", "not_met", "indeterminate"}
FALSE_AUTHORITY_KEYS = (
    "canonical_ontology_modified",
    "physical_interpretation_established",
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


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    tex_path = ARTIFACT_DIR / "four_project_success_categories_v1.tex"
    examples_path = ARTIFACT_DIR / "claim_boundary_examples_v1.yaml"
    mapping_path = ARTIFACT_DIR / "current_status_mapping_v1.yaml"
    math_path = ARTIFACT_DIR / "child_phys_math_success_categories.yaml"
    phil_path = ARTIFACT_DIR / "child_phys_phil_success_categories.yaml"
    review_path = ARTIFACT_DIR / "parent_conflict_review_success_categories.yaml"
    fusion_path = ARTIFACT_DIR / "parent_fusion_notes_success_categories.md"
    required = (tex_path, examples_path, mapping_path, math_path, phil_path, review_path, fusion_path)
    for path in required:
        check(f"exists:{path.name}", path.is_file() and not path.is_symlink(), "required regular task-local artifact")
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
        "Interpretive redescription",
        "Formal or categorical equivalence",
        "Genuine emergence",
        "Empirical novelty",
        "SC4-NONIMPLICATION-THEOREM-V1",
        "All twelve directed implications",
        "does not establish a physical gauge interpretation",
    ):
        check(f"tex_marker:{marker}", marker in tex, "exact formalization marker")

    category_examples = examples.get("category_examples", {})
    check("example_category_set", set(category_examples) == set(CATEGORIES), "exact four category keys")
    for category in CATEGORIES:
        block = category_examples.get(category, {}) if isinstance(category_examples, dict) else {}
        check(f"allowed_examples:{category}", len(block.get("allowed", [])) >= 2, "at least two allowed examples")
        check(f"disallowed_examples:{category}", len(block.get("disallowed", [])) >= 2, "at least two disallowed examples")
    check("cross_category_guard", "no directed cross-category implication is automatic" in examples.get("cross_category_guards", []), "explicit global non-implication guard")

    mappings = {item.get("mapping_id"): item for item in mapping.get("mappings", []) if isinstance(item, dict)}
    exact = mappings.get("CURRENT-EXACT-GR-BENCHMARK-LINE", {})
    quotient = mappings.get("GENERAL-QUOTIENT-EQSRC-EQUIVALENCE", {})
    exact_vector = exact.get("status_vector", {})
    quotient_vector = quotient.get("status_vector", {})
    check("mapping_component_order", tuple(mapping.get("component_order", [])) == CATEGORIES, "status vector uses exact category order")
    check("mapping_status_domain", set(mapping.get("status_domain", [])) == STATUS_DOMAIN, "tri-valued domain exact")
    check("exact_gr_interpretive_only", exact_vector == {CATEGORIES[0]: "met", CATEGORIES[1]: "indeterminate", CATEGORIES[2]: "not_met", CATEGORIES[3]: "not_met"}, "current exact-GR line has only interpretive redescription met")
    check("quotient_eqsrc_conditional", quotient_vector.get("formal_or_categorical_equivalence") == "indeterminate" and "only" in quotient.get("conditional_upgrade_rule", ""), "general EqSrc equivalence remains conditional on proof")
    check("all_status_values_valid", all(value in STATUS_DOMAIN for item in mappings.values() for value in item.get("status_vector", {}).values()), "all components are tri-valued")
    check("no_distance_delta", mapping.get("distance_to_gr", {}).get("changed") is False and mapping.get("distance_to_gr", {}).get("ledger_row_updated") is False, "mapping changes no Distance-to-GR row")

    for label, child in (("math", math_child), ("phil", phil_child)):
        check(f"child_task:{label}", child.get("task_id") == "RT-20260722-016", "child bound to outer task")
        check(
            f"child_status:{label}",
            child.get("status") in {"draft/control", "completed"}
            and (child.get("authority") in {"draft/control", "task_local_science_draft"}),
            "child completed at draft/control authority",
        )
    check("math_nonimplication", "SC4-NONIMPLICATION-THEOREM-V1" in json.dumps(math_child, sort_keys=True), "mathematical child supplies theorem identity")
    check("phil_overread_guards", "overread" in json.dumps(phil_child, sort_keys=True).lower() or "disallowed" in json.dumps(phil_child, sort_keys=True).lower(), "philosophical child supplies overread guards")
    check("conflict_review_pass", review.get("status") == "PASS" and review.get("unresolved_blocking_conflicts") == 0, "parent resolved no blocking conflict")
    check("fusion_names_children", "child_phys_math" in fusion and "child_phys_phil" in fusion, "fusion notes identify both children")

    for source, expected in (
        (REPO_ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md", "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"),
        (REPO_ROOT / "research_control/handoffs/handoff-0825.yaml", "b70e5909d7e0ea8b6d259e488c5a34718dcba2a78960f0794349bd8cd8147148"),
        (REPO_ROOT / "research_control/tasks/RT-20260720-008/jobs/completions/AJC-AJ-RT-20260720-008-001.yaml", "58f143cce059bb0d28c19f2542b3f7d7892e04c3b7573c468220c41dc932d2fc"),
        (REPO_ROOT / "research_control/tasks/RT-20260721-003/jobs/completions/AJC-AJ-RT-20260721-003-001.yaml", "28ea88fbfbecd144b7b742152be0fab44cafd0b8ac21869d9ad6be105f2f7305"),
    ):
        check(f"source_hash:{source.name}:{expected[:8]}", source.is_file() and sha256(source) == expected, "exact source or dependency identity")

    for label, block in (("examples", examples.get("authority_limits", {})), ("mapping", mapping.get("authority_limits", {}))):
        for key in FALSE_AUTHORITY_KEYS:
            check(f"authority_false:{label}:{key}", block.get(key) is False, "protected authority remains false")

    registry = (REPO_ROOT / "registries/TEX_SOURCE_REGISTRY.csv").read_text(encoding="utf-8")
    check("tex_registered", "TEX-V21-P14-T01-PROJECT-SUCCESS-CATEGORIES" in registry and str(tex_path.relative_to(REPO_ROOT)) in registry, "fused TeX has a source-registry row")
    return finish(checks)


def finish(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "p14_t01_success_categories_validation_report_v1",
        "task_id": "RT-20260722-016",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "authority_boundary": "Operational validation does not establish ontology adoption theorem truth physical interpretation Distance-to-GR progress promotion publication or completed derivation.",
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
