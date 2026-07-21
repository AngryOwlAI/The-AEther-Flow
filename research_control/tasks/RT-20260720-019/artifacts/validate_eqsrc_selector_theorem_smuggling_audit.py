#!/usr/bin/env python3
"""Validate the bounded P2-T06 EqSrc selector-theorem smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260720-019"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_smuggling_audit_validation.json"

EXPECTED_HASHES = {
    "research_control/tasks/RT-20260720-014/artifacts/eqsrc_source_category_definition_v1.tex": "00d7e14b76ac4fa01b834739646fe03012c2b82326a158064b27cdbe916be268",
    "research_control/tasks/RT-20260720-014/artifacts/eqsrc_source_morphism_variation_schema.yaml": "963520b97b25fc3f7406ae7729c98966a6676c583dae60dd101d0b0d32e5d227",
    "research_control/tasks/RT-20260720-015/artifacts/eqsrc_natural_selector_fixed_point_condition_v1.tex": "7611533f40b61b8a32da327add3646b95c604f858adba54c40378b6f29d5067a",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_assumptions.yaml": "f043a5998bb180ad4bca7037f1f7def836a156d009a69bfaf1304eb86bc390cf",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_v1.tex": "4a7c84ecf769b19e92b2b2dffd7224ddd4e1e02e4cc93cff797d01fa0e1bc62b",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_fixtures.json": "e8ced96541fa941e5a3b4ceaa8d7b48204acf7ca8ec342ac6b23dbbf5c470a73",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_theorem_instance_map.yaml": "7fbd64b7f0fbcc474b32c85da68a7c4bb841f824edfdbbbd25d116da7ba2c5be",
    "research_control/tasks/RT-20260720-018/artifacts/proof/SelectorKernel.lean": "6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356",
    "research_control/tasks/RT-20260720-018/artifacts/eqsrc_selector_formal_proof_validation.json": "9628e6ca789aff6df0da5039f51f3661ce50cab0461927650fe4b49f5aec9932",
}

VERDICT = "conditional_source_purity_pass_with_precise_p2_t04_k_metric_scope_defect"
ASSUMPTION_IDS = {f"NS-A{i:02d}" for i in range(1, 11)}
DEFINITION_IDS = {
    "DEF-OBJECT-ADMISSION",
    "DEF-MORPHISM",
    "DEF-CERTIFIED-ISOMORPHISM",
    "DEF-STRUCTURAL-AUTOMORPHISM",
    "DEF-CANDIDATE-UNIVERSE-D",
    "DEF-ELIGIBILITY-CHI",
    "DEF-ELIGIBLE-CHOICE-S-CHI",
    "DEF-RELATION-MAP-K",
}
LEAN_THEOREMS = {
    "empty_fixed_iff_no_invariant_selector",
    "fixed_choice_unique_of_transitive",
    "no_invariant_selector_of_transitive_distinct",
    "multiple_fixed_gives_multiple_selectors",
    "historical_sign_swap_no_invariant_selector",
    "trivial_action_has_multiple_selectors",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def check(checks: list[dict], check_id: str, ok: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail})


def validate() -> dict:
    checks: list[dict] = []

    for rel, expected in EXPECTED_HASHES.items():
        path = ROOT / rel
        observed = sha256(path) if path.is_file() else "missing"
        check(checks, f"hash:{rel}", observed == expected, f"expected={expected} observed={observed}")

    matrix = load_yaml(ARTIFACT_DIR / "eqsrc_selector_theorem_assumption_provenance_matrix.yaml")
    verdict = load_yaml(ARTIFACT_DIR / "eqsrc_selector_theorem_audit_verdict.yaml")
    compact = json.loads((ARTIFACT_DIR / "eqsrc_selector_theorem_audit_compact_receipt.json").read_text(encoding="utf-8"))
    audit_text = (ARTIFACT_DIR / "eqsrc_selector_theorem_smuggling_audit_v1.tex").read_text(encoding="utf-8")
    lean_text = (ROOT / "research_control/tasks/RT-20260720-018/artifacts/proof/SelectorKernel.lean").read_text(encoding="utf-8")

    observed_assumptions = {row.get("assumption_id") for row in matrix.get("assumption_coverage", [])}
    observed_definitions = {row.get("definition_id") for row in matrix.get("definition_coverage", [])}
    alias_rows = matrix.get("semantic_alias_tests", [])
    translation_rows = matrix.get("translation_coverage", [])
    faithful = [row for row in translation_rows if row.get("status") == "faithful_mechanization"]
    unmechanized = [row for row in translation_rows if row.get("status") == "not_mechanized_explicitly_out_of_scope"]

    check(checks, "assumption_coverage", observed_assumptions == ASSUMPTION_IDS, f"count={len(observed_assumptions)}")
    check(checks, "definition_coverage", observed_definitions == DEFINITION_IDS, f"count={len(observed_definitions)}")
    check(checks, "semantic_alias_count", len(alias_rows) == 10, f"count={len(alias_rows)}")
    check(checks, "semantic_alias_results", all(row.get("result") == "REJECTED" for row in alias_rows), "all aliases must be rejected")
    check(checks, "translation_faithful_count", len(faithful) == 4, f"count={len(faithful)}")
    check(checks, "translation_unmechanized_count", len(unmechanized) == 4, f"count={len(unmechanized)}")
    check(checks, "lean_theorem_presence", all(name in lean_text for name in LEAN_THEOREMS), f"count={sum(name in lean_text for name in LEAN_THEOREMS)}")
    check(checks, "lean_scope_boundary", "only the one-object group-action core" in lean_text, "bounded scope statement present")

    check(checks, "verdict_identity", verdict.get("audit_verdict") == VERDICT == compact.get("verdict"), "verdicts agree")
    check(checks, "source_pure_as_written", verdict.get("source_pure_as_written") is True, "source-purity result")
    check(checks, "theorem_repair_not_required", verdict.get("theorem_repair_required") is False, "no theorem repair")
    check(checks, "atlas_metric_repair_required", verdict.get("p2_t04_metric_repair_required_before_reuse") is True, "scoped metric repair recorded")
    check(checks, "zero_blocking_defects", verdict.get("blocking_defect_count") == 0, "blocking defects=0")
    counts = verdict.get("finding_counts", {})
    check(checks, "zero_target_imports", counts.get("explicit_target_import_count") == 0, "target imports=0")
    check(checks, "zero_process_imports", counts.get("explicit_process_import_count") == 0, "process imports=0")
    check(checks, "four_material_limits", counts.get("material_nonblocking_limitation_count") == 4, "material limits=4")
    check(checks, "two_scoped_metric_defects", counts.get("scoped_p2_t04_metric_defect_count") == 2, "scoped metric defects=2")

    category = verdict.get("category_engineering", {})
    selection = verdict.get("selection_space", {})
    interpretation = verdict.get("automorphism_interpretation", {})
    authority = verdict.get("authority", {})
    check(checks, "no_post_hoc_category", category.get("post_hoc_selector_preserving_morphism_definition_found") is False, "no post-hoc selector-preserving arrows")
    check(checks, "category_provenance_open", category.get("independently_derived_morphism_class_established") is False, "independent category provenance absent")
    check(checks, "selection_not_circular", selection.get("intended_eqsrc_relation_used_to_define_S_chi") is False and selection.get("benchmark_outcome_used_to_define_S_chi") is False, "S_chi excludes relation and benchmark inputs")
    check(checks, "structural_not_physical_gauge", interpretation.get("structural_automorphism_equals_physical_gauge") is False, "gauge alias rejected")
    check(checks, "p2_t07_not_executed", authority.get("P2_T07_executed") is False, "P2-T07 retained")
    check(checks, "authority_boundary", all(authority.get(key) is False for key in ("canonical_ontology_edit_authorized", "source_law_adoption_authorized", "proof_authority", "physics_promotion_authorized", "external_publication_authorized")), "all protected authority flags false")

    normalized_audit = " ".join(audit_text.split())
    required_phrases = [
        "source-pure as written",
        "not a selector",
        "not physical gauge",
        "full-category equalizer",
        "No repair",
        "K(D)",
        "selector-induced",
        "P2-T07",
    ]
    check(checks, "audit_boundary_language", all(phrase in normalized_audit for phrase in required_phrases), "required scope language present")

    failures = [row for row in checks if row["status"] != "PASS"]
    return {
        "schema_id": "eqsrc-selector-theorem-smuggling-audit-validation.v1",
        "task_id": "RT-20260720-019",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "verdict": VERDICT,
        "source_hash_count": len(EXPECTED_HASHES),
        "assumption_count": len(observed_assumptions),
        "definition_count": len(observed_definitions),
        "semantic_alias_test_count": len(alias_rows),
        "faithful_mechanization_count": len(faithful),
        "explicitly_unmechanized_count": len(unmechanized),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']} {report['passed_check_count']}/{report['check_count']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
