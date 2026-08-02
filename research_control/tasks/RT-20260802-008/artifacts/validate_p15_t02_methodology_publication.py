#!/usr/bin/env python3
"""Validate the bounded P15-T02 methodology-publication packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = ROOT / "research_control/tasks/RT-20260802-008/artifacts"
BUILDER_PATH = ARTIFACT_DIR / "build_p15_t02_methodology_publication.py"
REPORT_PATH = ARTIFACT_DIR / "p15_t02_methodology_validation.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("p15_t02_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate() -> dict[str, Any]:
    builder = load_builder()
    expected = builder.build_outputs()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, evidence: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "evidence": evidence})

    for name, text in expected.items():
        path = ARTIFACT_DIR / name
        add(f"deterministic_output::{name}", path.is_file() and path.read_text(encoding="utf-8") == text, "exact builder bytes")

    experiment = json.loads(expected[builder.OUTPUT_PATHS["experiment"]])
    dictionary = json.loads(expected[builder.OUTPUT_PATHS["dictionary"]])
    receipt = json.loads(expected[builder.OUTPUT_PATHS["receipt"]])
    manuscript = expected[builder.OUTPUT_PATHS["manuscript"]]
    arm_status = {item["arm_id"]: item["observation_status"] for item in experiment["comparison_arms"]}
    add("five_requested_arms_classified", set(arm_status) == {"unstructured", "single_agent", "role_structured", "blind_review", "diverse_review"}, str(arm_status))
    add("missing_arms_not_zero_filled", arm_status["unstructured"] == "not_observed" and arm_status["single_agent"] == "not_observed_as_control_arm", str(arm_status))
    add("blind_review_same_model_only", arm_status["blind_review"] == "observed_same_model_context_only", arm_status["blind_review"])
    add("diverse_review_not_independent", arm_status["diverse_review"] == "partially_observed_context_diversity_only", arm_status["diverse_review"])
    add("causal_identification_guard", experiment["design"]["causal_identification"] == "not_identified", experiment["design"]["causal_identification"])

    ratios_valid = True
    for item in experiment["mechanism_results"]:
        numerator = item["numerator"]
        denominator = item["denominator"]
        value = item["value"]
        ratios_valid = ratios_valid and isinstance(numerator, int) and isinstance(denominator, int) and denominator > 0 and abs(value - numerator / denominator) < 1e-12
    add("all_reported_ratios_have_valid_denominators", ratios_valid, f"metric_count={len(experiment['mechanism_results'])}")
    add("unknown_denominator_policy", "numeric zero is prohibited" in dictionary["missingness_policy"], dictionary["missingness_policy"])
    add("cost_not_fabricated", receipt["cost_status"] in {"not_available", "not_recorded"}, receipt["cost_status"])

    source_hashes_valid = True
    for item in experiment["source_bindings"]:
        path = ROOT / item["path"]
        source_hashes_valid = source_hashes_valid and path.is_file() and sha256_bytes(path.read_bytes()) == item["sha256"]
    add("source_hash_exactness", source_hashes_valid, f"source_count={len(experiment['source_bindings'])}")

    false_authority = all(value is False for value in experiment["authority_boundary"].values())
    add("authority_flags_all_false", false_authority, json.dumps(experiment["authority_boundary"], sort_keys=True))
    add("manuscript_internal_draft", 'status: "draft/control"' in manuscript and "publication_authorized: false" in manuscript, "frontmatter")
    add("manuscript_causal_limit", "does not identify causal improvement" in manuscript, "causal boundary sentence")
    add("manuscript_external_review_limit", "does not mean an external person reviewed" in manuscript, "role-name boundary sentence")
    add("operational_evidence_separated", "They do not estimate scientific outcome quality" in manuscript, "P13 boundary sentence")
    add("parent_child_outputs_present", all((ARTIFACT_DIR / builder.OUTPUT_PATHS[key]).is_file() for key in ("child_math", "child_phil", "conflict", "fusion")), "four synthesis artifacts")
    add("parent_conflict_resolved", "unresolved_conflicts: []" in expected[builder.OUTPUT_PATHS["conflict"]], "no unresolved conflict")
    add("recommendation_coverage", set(experiment["governance_reform_mapping"]["recommendation_ids"]) == {"V21-R36", "V21-R37", "V21-R38", "V21-R42", "V21-R43", "V21-R44", "V21-R45", "V21-R51", "V21-R52", "V21-R53", "V21-R65", "V21-R66", "V21-R69"}, "13 exact recommendation IDs")

    failed = [item["check_id"] for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v21_p15_t02_methodology_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "task_id": "RT-20260802-008",
        "plan_task_id": "P15-T02",
        "check_count": len(checks),
        "failed_check_ids": failed,
        "checks": checks,
        "authority_boundary": experiment["authority_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
