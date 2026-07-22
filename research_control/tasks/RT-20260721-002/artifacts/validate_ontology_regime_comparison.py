#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260721-002"
ARTIFACTS = TASK / "artifacts"
REPORT = ARTIFACTS / "ontology_regime_comparison_validation_v1.json"
EXPECTED_IMMUTABLE_HASHES = {
    "research_control/tasks/RT-20260720-030/artifacts/comprehensive_source_assumption_ledger_v1.tex": "e50fb9458ee601563a0decc8dc809e719ec4e1d6b62c0682d1175ad2f91a1d90",
    "research_control/tasks/RT-20260720-031/artifacts/continuum_first_premetric_ontology_option_v1.tex": "7d408e527015f4e7c09df90277282c284f299fb705cbd4917a22e62ab3e0d1f8",
    "research_control/tasks/RT-20260720-032/artifacts/emergence_first_process_order_ontology_option_v1.tex": "121e86bd8609863ca79fd21d1cf9b5ee855057bc5a0804927946911f1222d6f5",
    "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
    "ontology/tex/aether_flow_dynamics.tex": "ee3ae3298ab45111235388b305cbda2143b0314cb90f9b652115f71eb2fb8c6d",
    "ontology/tex/aether_flow_geometry.tex": "ad43e3408fe2d9686a52a71de7ab8326668e8f04ebe2d2845986898b7d2c000f",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "registries/METRIC_USE_LEDGER.csv": "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf",
}
CRITERION_ORDER = [
    "assumption_economy",
    "formalization_tractability",
    "explanatory_power",
    "primary_literature_maturity",
    "downstream_compatibility",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})
        if not condition:
            failures.append(f"{check_id}: {detail}")

    bibliography = load_yaml(ARTIFACTS / "ontology_regime_primary_literature_bibliography_v1.yaml")
    entries = bibliography.get("source_entries", [])
    check("primary_source_count", len(entries) == 10, f"observed={len(entries)} expected=10")
    check("all_sources_primary", all(item.get("primary_source") is True for item in entries), "every source must be primary")
    check("balanced_source_sides", sum(item.get("comparison_side") == "continuum_first" for item in entries) == 5 and sum(item.get("comparison_side") == "emergence_first" for item in entries) == 5, "expected five sources per comparison side")
    check("apa7_metadata", all("https://" in item.get("citation_apa7", "") for item in entries), "every APA 7 entry must include a stable HTTPS locator")
    check("exact_scope_fields", all(item.get("exact_hypotheses") and item.get("established_conclusion") and item.get("transfer_boundary") for item in entries), "hypotheses conclusion and transfer boundary are required")
    check("no_quotations", bibliography.get("quotation_count") == 0, "review must use scoped paraphrase rather than quotations")

    with (ARTIFACTS / "ontology_regime_external_literature_matrix_v1.csv").open(newline="", encoding="utf-8") as handle:
        matrix = list(csv.DictReader(handle))
    required_columns = {"source_id", "comparison_side", "exact_hypotheses", "established_conclusion", "reuse_class", "aeether_flow_adaptation_needed", "forbidden_overread", "source_url"}
    check("matrix_row_count", len(matrix) == 10, f"observed={len(matrix)} expected=10")
    check("matrix_schema", bool(matrix) and required_columns <= set(matrix[0]), f"columns={sorted(matrix[0]) if matrix else []}")
    check("matrix_source_parity", {row["source_id"] for row in matrix} == {item["source_id"] for item in entries}, "bibliography and matrix source IDs must match")
    check("matrix_side_parity", sum(row["comparison_side"] == "continuum_first" for row in matrix) == 5 and sum(row["comparison_side"] == "emergence_first" for row in matrix) == 5, "matrix must remain balanced")

    sensitivity = load_yaml(ARTIFACTS / "ontology_regime_criteria_weight_sensitivity_v1.yaml")
    criteria = sensitivity.get("criteria", [])
    check("criterion_count", len(criteria) == 5, f"observed={len(criteria)} expected=5")
    check("criterion_order", [item.get("criterion_id") for item in criteria] == CRITERION_ORDER, "criterion order must be fixed")
    cf_scores = [float(item["continuum_first_score"]) for item in criteria]
    ef_scores = [float(item["emergence_first_score"]) for item in criteria]
    differences = [cf - ef for cf, ef in zip(cf_scores, ef_scores)]
    declared_differences = [float(value) for value in sensitivity["score_difference_model"]["difference_vector"]]
    check("difference_vector", all(abs(a - b) < 1e-12 for a, b in zip(differences, declared_differences)), f"computed={differences} declared={declared_differences}")
    check("mixed_sign_non_dominance", min(differences) < 0 < max(differences), f"difference_vector={differences}")

    rankings: set[str] = set()
    for scenario in sensitivity.get("scenarios", []):
        weights_map = scenario.get("weights", {})
        weights = [float(weights_map[key]) for key in CRITERION_ORDER]
        cf_total = sum(weight * score for weight, score in zip(weights, cf_scores))
        ef_total = sum(weight * score for weight, score in zip(weights, ef_scores))
        difference = cf_total - ef_total
        ranking = "continuum_first" if difference > 1e-12 else "emergence_first" if difference < -1e-12 else "tie"
        rankings.add(ranking)
        scenario_id = scenario.get("scenario_id", "unknown")
        check(f"{scenario_id}_weight_sum", abs(sum(weights) - 1.0) < 1e-12, f"sum={sum(weights)}")
        check(f"{scenario_id}_cf_total", abs(cf_total - float(scenario["continuum_first_total"])) < 1e-9, f"computed={cf_total} declared={scenario['continuum_first_total']}")
        check(f"{scenario_id}_ef_total", abs(ef_total - float(scenario["emergence_first_total"])) < 1e-9, f"computed={ef_total} declared={scenario['emergence_first_total']}")
        check(f"{scenario_id}_difference", abs(difference - float(scenario["difference"])) < 1e-9, f"computed={difference} declared={scenario['difference']}")
        check(f"{scenario_id}_ranking", ranking == scenario["ranking"], f"computed={ranking} declared={scenario['ranking']}")
    check("ranking_flip_coverage", {"continuum_first", "emergence_first"} <= rankings, f"rankings={sorted(rankings)}")
    check("nonrobust_conclusion", sensitivity.get("sensitivity_conclusion", {}).get("robust_preference") is False, "aggregate preference must be marked nonrobust")

    math_child = load_yaml(ARTIFACTS / "child_phys_math_ontology_regime_comparison.yaml")
    phil_child = load_yaml(ARTIFACTS / "child_phys_phil_ontology_regime_comparison.yaml")
    conflict = load_yaml(ARTIFACTS / "parent_conflict_review_ontology_regime_comparison.yaml")
    fusion = (ARTIFACTS / "parent_fusion_notes_ontology_regime_comparison.md").read_text(encoding="utf-8")
    check("math_child_ready", math_child.get("child_disposition", {}).get("result") == "PASS_AT_COMPARATIVE_DECISION_EVIDENCE_SCOPE", "math child must pass at comparative-decision-evidence scope")
    check("phil_child_ready", phil_child.get("validation_status") == "READY_FOR_PARENT_FUSION", "philosophy child must be ready for fusion")
    check("phil_revision_review", phil_child.get("revision_review", {}).get("status") == "complete", "philosophy child must record focused revision review")
    check("child_fixed_hash_p4t02", math_child.get("fixed_source_basis", [])[0].get("observed_sha256") == EXPECTED_IMMUTABLE_HASHES["research_control/tasks/RT-20260720-031/artifacts/continuum_first_premetric_ontology_option_v1.tex"], "math child P4-T02 source hash must be current")
    check("child_fixed_hash_p4t03", math_child.get("fixed_source_basis", [])[1].get("observed_sha256") == EXPECTED_IMMUTABLE_HASHES["research_control/tasks/RT-20260720-032/artifacts/emergence_first_process_order_ontology_option_v1.tex"], "math child P4-T03 source hash must be current")
    check("conflict_resolution", conflict.get("status") == "resolved" and conflict.get("unresolved_conflicts") == [], "parent conflict review must resolve all conflicts")
    check("parallel_revision", conflict.get("parallel_child_revision_completed") is True, "focused child revision round must be complete")
    check("fusion_boundary", "does not select, adopt, reject" in fusion and "no robust winner exists" in fusion, "fusion must preserve non-selection and non-dominance")

    review = (ARTIFACTS / "ontology_regime_comparison_report_v1.md").read_text(encoding="utf-8")
    required_review_phrases = (
        "Neither fixed option scientifically dominates the other",
        "engineering compatibility only",
        "Source dynamics is the common decisive absence",
        "does not execute it",
        "Distance-to-GR ledger",
        "blocked_adoption_open_continuation",
    )
    for phrase in required_review_phrases:
        check(f"review_phrase_{hashlib.sha256(phrase.encode()).hexdigest()[:8]}", phrase.casefold() in review.casefold(), phrase)
    for surname in ("Ehlers", "Hawking", "Malament", "Connes", "Brunetti", "Bombelli", "Rideout", "Major", "Benincasa", "Ambjørn"):
        check(f"review_reference_{surname.casefold()}", surname in review, f"missing reference surname {surname}")

    immutable_hashes: dict[str, str] = {}
    for relative, expected in EXPECTED_IMMUTABLE_HASHES.items():
        observed = sha256(ROOT / relative)
        immutable_hashes[relative] = observed
        check(f"immutable_{hashlib.sha256(relative.encode()).hexdigest()[:8]}", observed == expected, f"observed={observed} expected={expected}")

    artifact_paths = [
        ARTIFACTS / "ontology_regime_primary_literature_bibliography_v1.yaml",
        ARTIFACTS / "ontology_regime_external_literature_matrix_v1.csv",
        ARTIFACTS / "ontology_regime_criteria_weight_sensitivity_v1.yaml",
        ARTIFACTS / "ontology_regime_comparison_report_v1.md",
        ARTIFACTS / "child_phys_math_ontology_regime_comparison.yaml",
        ARTIFACTS / "child_phys_phil_ontology_regime_comparison.yaml",
        ARTIFACTS / "parent_conflict_review_ontology_regime_comparison.yaml",
        ARTIFACTS / "parent_fusion_notes_ontology_regime_comparison.md",
    ]
    report = {
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260721-002",
        "plan_task_id": "P4-T04",
        "checks": checks,
        "metrics": {
            "check_count": len(checks),
            "primary_source_count": len(entries),
            "matrix_row_count": len(matrix),
            "criterion_count": len(criteria),
            "scenario_count": len(sensitivity.get("scenarios", [])),
            "ranking_set": sorted(rankings),
            "baseline_difference": sensitivity.get("sensitivity_conclusion", {}).get("baseline_margin"),
            "robust_preference": sensitivity.get("sensitivity_conclusion", {}).get("robust_preference"),
        },
        "artifact_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in artifact_paths},
        "immutable_surface_hashes": immutable_hashes,
        "failures": failures,
        "claim_boundary": "Operational validation of P4-T04 comparative decision evidence only; no ontology-regime selection adoption rejection canonical edit Distance-to-GR delta or promotion authority.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
