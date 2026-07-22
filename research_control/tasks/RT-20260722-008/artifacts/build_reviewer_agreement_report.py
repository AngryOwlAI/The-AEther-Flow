#!/usr/bin/env python3
"""Build and validate the v21 P11-T06 reviewer-agreement calibration report."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260722-008"
ART = TASK / "artifacts"
SPEC_PATH = ART / "reviewer_agreement_metric_specification.md"
FIXTURES_PATH = ART / "reviewer_metric_calibration_fixtures.json"
REPORT_PATH = ART / "reviewer_agreement_calibration_report.json"
RECEIPT_PATH = ART / "reviewer_agreement_compact_receipt.json"
GENERATOR_PATH = Path(__file__).resolve()

SCHEMA_ID = "v21_reviewer_agreement_metric_report_v1"
SUITE_ID = "v21_reviewer_metric_fixture_suite_v1"
AXES = (
    "theorem_validity",
    "assumptions",
    "countermodels",
    "physical_interpretation",
    "claim_scope",
)
CONTEXT_CLASSES = (
    "same_context_role_review",
    "blind_same_model_review",
    "different_model_review",
    "human_expert_review",
    "independent_replication",
    "unknown",
)
DIMENSIONS = (
    "model_family",
    "prompt_context",
    "data_access",
    "institution",
    "human_authorship",
    "code_base",
    "method",
)
CATEGORIES = {
    "no_finding",
    "omission",
    "ambiguity",
    "unsupported_step",
    "counterexample",
    "scope_overreach",
    "interpretation_mismatch",
    "evidence_gap",
    "not_assessed",
}
SEVERITIES = {"none", "low", "medium", "high", "critical", "unknown"}
VERDICTS = {"clear", "concern", "repair_required", "blocking", "not_assessed"}
RESOLUTION_STATES = {"no_finding", "resolved", "unresolved", "not_assessed"}
RELATIONSHIPS = {"same", "different", "independent", "not_applicable", "unknown"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CONFIG_RE = re.compile(r"^cfg-[a-z][a-z0-9-]*$")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_suite(path: Path = FIXTURES_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("fixture suite must be a JSON object")
    return value


def repo_source(ref: str) -> Path | None:
    if not isinstance(ref, str) or not ref or ref.startswith(("/", ".local/", "wiki/")):
        return None
    relative = ref.split("#", 1)[0]
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return path


def add_error(errors: list[dict[str, str]], rule_id: str, detail: str) -> None:
    errors.append({"rule_id": rule_id, "detail": detail})


def validate_suite(suite: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    expected_suite_fields = {"schema_id", "fixture_mode", "authority_boundary", "reviews", "expectations"}
    if set(suite) != expected_suite_fields:
        add_error(errors, "metric_suite_exact_shape", f"suite field difference: {sorted(set(suite) ^ expected_suite_fields)}")
    if suite.get("schema_id") != SUITE_ID or suite.get("fixture_mode") != "synthetic_calibration":
        add_error(errors, "metric_suite_identity", "fixture suite identity or mode is invalid")
    authority = suite.get("authority_boundary")
    if not isinstance(authority, dict) or authority.get("review_executed_by_task") is not False or authority.get("physics_promotion_authorized") is not False or authority.get("proof_authority") is not False or authority.get("consensus_sets_scientific_status") is not False:
        add_error(errors, "metric_suite_authority_boundary", "fixture authority flags must all remain false")

    reviews = suite.get("reviews")
    if not isinstance(reviews, list) or len(reviews) < 2:
        add_error(errors, "metric_suite_reviews", "at least two review records are required")
        return errors

    expected_review_fields = {
        "review_id",
        "record_mode",
        "reviewed_object_id",
        "source_object_path",
        "source_object_sha256",
        "source_review_artifact_id",
        "blind_packet_id",
        "configuration_blind_id",
        "review_context",
        "axis_assessments",
        "physics_promotion_authorized",
        "scientific_status_inference",
        "truth_status_inference",
        "forbidden_conclusions",
    }
    seen_review_ids: set[str] = set()
    object_hashes: dict[str, tuple[str, str]] = {}
    for index, review in enumerate(reviews):
        label = f"reviews[{index}]"
        if not isinstance(review, dict):
            add_error(errors, "metric_review_shape", f"{label} must be an object")
            continue
        if set(review) != expected_review_fields:
            add_error(errors, "metric_review_shape", f"{label} field difference: {sorted(set(review) ^ expected_review_fields)}")
        review_id = review.get("review_id")
        if not isinstance(review_id, str) or not review_id.strip() or review_id in seen_review_ids:
            add_error(errors, "metric_review_identity", f"{label} has a blank or duplicate review_id")
        elif isinstance(review_id, str):
            seen_review_ids.add(review_id)
        if review.get("record_mode") != "synthetic_calibration":
            add_error(errors, "metric_review_mode", f"{label} is not a synthetic calibration record")
        object_id = review.get("reviewed_object_id")
        if not isinstance(object_id, str) or not object_id.strip():
            add_error(errors, "metric_source_lineage", f"{label} has no reviewed_object_id")
        source_ref = review.get("source_object_path")
        source_hash = review.get("source_object_sha256")
        source_path = repo_source(source_ref) if isinstance(source_ref, str) else None
        if source_path is None or not source_path.is_file() or not isinstance(source_hash, str) or not SHA256_RE.fullmatch(source_hash):
            add_error(errors, "metric_source_lineage", f"{label} has an invalid canonical source path or hash")
        elif sha256(source_path) != source_hash:
            add_error(errors, "metric_source_hash", f"{label} source hash does not match {source_ref}")
        elif isinstance(object_id, str):
            lineage = (source_ref, source_hash)
            prior = object_hashes.setdefault(object_id, lineage)
            if prior != lineage:
                add_error(errors, "metric_source_lineage", f"{object_id} maps to more than one source lineage")
        if not isinstance(review.get("source_review_artifact_id"), str) or not review.get("source_review_artifact_id", "").strip():
            add_error(errors, "metric_review_identity", f"{label} has no source review-artifact identity")
        if not isinstance(review.get("blind_packet_id"), str) or not review.get("blind_packet_id", "").strip():
            add_error(errors, "metric_review_identity", f"{label} has no blind-packet identity")
        config = review.get("configuration_blind_id")
        if not isinstance(config, str) or not CONFIG_RE.fullmatch(config):
            add_error(errors, "metric_blinded_configuration", f"{label} configuration ID is not opaque and valid")

        context = review.get("review_context")
        if not isinstance(context, dict):
            add_error(errors, "metric_review_context", f"{label} review_context must be an object")
            context = {}
        expected_context_fields = {"schema_id", "classification", "review_executed", "replication_executed", "dimensions", "evidence_paths", "limitations", "claims"}
        if set(context) != expected_context_fields:
            add_error(errors, "metric_review_context", f"{label} context field difference: {sorted(set(context) ^ expected_context_fields)}")
        classification = context.get("classification")
        if context.get("schema_id") != "v21_review_context_v1" or classification not in CONTEXT_CLASSES:
            add_error(errors, "metric_review_context", f"{label} has an invalid P11-T02 context class")
        if context.get("review_executed") is not False or context.get("replication_executed") is not False:
            add_error(errors, "metric_synthetic_no_review", f"{label} synthetic record cannot claim review or replication execution")
        claims = context.get("claims")
        if not isinstance(claims, dict) or set(claims) != {"external_review_completed", "human_expert_review_completed", "independent_replication_completed"} or any(value is not False for value in claims.values()):
            add_error(errors, "metric_synthetic_no_review", f"{label} completion claims must all be false")
        dimensions = context.get("dimensions")
        if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
            observed = set(dimensions) if isinstance(dimensions, dict) else set()
            add_error(errors, "metric_review_context", f"{label} dimension difference: {sorted(observed ^ set(DIMENSIONS))}")
            dimensions = dimensions if isinstance(dimensions, dict) else {}
        for dimension in DIMENSIONS:
            value = dimensions.get(dimension)
            if not isinstance(value, dict) or set(value) != {"relationship", "evidence"} or value.get("relationship") not in RELATIONSHIPS or not isinstance(value.get("evidence"), str) or not value.get("evidence", "").strip():
                add_error(errors, "metric_review_context", f"{label} has an invalid {dimension} dimension")
        if classification == "unknown" and not any(value.get("relationship") == "unknown" for value in dimensions.values() if isinstance(value, dict)):
            add_error(errors, "metric_unknown_independence_explicit", f"{label} unknown class has no unknown dimension")
        evidence_paths = context.get("evidence_paths")
        if not isinstance(evidence_paths, list) or not evidence_paths:
            add_error(errors, "metric_review_context", f"{label} needs canonical context evidence paths")
        else:
            for evidence_ref in evidence_paths:
                evidence_path = repo_source(evidence_ref) if isinstance(evidence_ref, str) else None
                if evidence_path is None or not evidence_path.is_file():
                    add_error(errors, "metric_review_context", f"{label} has invalid context evidence {evidence_ref}")

        assessments = review.get("axis_assessments")
        if not isinstance(assessments, dict) or set(assessments) != set(AXES):
            observed = set(assessments) if isinstance(assessments, dict) else set()
            add_error(errors, "metric_axis_shape", f"{label} axis difference: {sorted(observed ^ set(AXES))}")
            assessments = assessments if isinstance(assessments, dict) else {}
        for axis in AXES:
            assessment = assessments.get(axis)
            if not isinstance(assessment, dict) or set(assessment) != {"finding_category", "severity", "verdict", "finding_ids", "resolution_status", "evidence_refs"}:
                add_error(errors, "metric_axis_shape", f"{label}.{axis} has an invalid shape")
                continue
            category = assessment.get("finding_category")
            severity = assessment.get("severity")
            verdict = assessment.get("verdict")
            resolution = assessment.get("resolution_status")
            finding_ids = assessment.get("finding_ids")
            evidence_refs = assessment.get("evidence_refs")
            if category not in CATEGORIES or severity not in SEVERITIES or verdict not in VERDICTS or resolution not in RESOLUTION_STATES:
                add_error(errors, "metric_axis_enum", f"{label}.{axis} has an unknown enum value")
                continue
            if not isinstance(finding_ids, list) or not all(isinstance(item, str) and item.strip() for item in finding_ids):
                add_error(errors, "metric_finding_lineage", f"{label}.{axis} finding IDs are invalid")
            if not isinstance(evidence_refs, list) or not all(isinstance(item, str) and item.strip() for item in evidence_refs):
                add_error(errors, "metric_finding_lineage", f"{label}.{axis} evidence refs are invalid")
            else:
                for evidence_ref in evidence_refs:
                    evidence_path = repo_source(evidence_ref)
                    if evidence_path is None or not evidence_path.is_file():
                        add_error(errors, "metric_finding_lineage", f"{label}.{axis} has invalid evidence {evidence_ref}")
            if category == "no_finding" and not (severity == "none" and verdict == "clear" and resolution == "no_finding" and finding_ids == []):
                add_error(errors, "metric_axis_coherence", f"{label}.{axis} no_finding fields disagree")
            elif category == "not_assessed" and not (severity == "unknown" and verdict == "not_assessed" and resolution == "not_assessed" and finding_ids == []):
                add_error(errors, "metric_axis_coherence", f"{label}.{axis} not_assessed fields disagree")
            elif category not in {"no_finding", "not_assessed"} and (severity in {"none"} or verdict in {"clear", "not_assessed"} or resolution not in {"resolved", "unresolved"} or not finding_ids or not evidence_refs):
                add_error(errors, "metric_axis_coherence", f"{label}.{axis} finding fields disagree")

        if review.get("physics_promotion_authorized") is not False or review.get("scientific_status_inference") != "forbidden" or review.get("truth_status_inference") != "forbidden":
            add_error(errors, "metric_no_truth_or_promotion", f"{label} attempts authority or truth inference")
        forbidden = review.get("forbidden_conclusions")
        if not isinstance(forbidden, list) or not forbidden or not all(isinstance(item, str) and item.strip() for item in forbidden):
            add_error(errors, "metric_no_truth_or_promotion", f"{label} lacks explicit forbidden conclusions")
    return errors


def assessment_signature(assessment: dict[str, Any]) -> tuple[str, str, str]:
    return (
        assessment["finding_category"],
        assessment["severity"],
        assessment["verdict"],
    )


def aggregate(reviews: list[dict[str, Any]]) -> dict[str, Any]:
    by_object: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_config: dict[str, list[dict[str, Any]]] = defaultdict(list)
    class_review_counts = Counter()
    for review in reviews:
        by_object[review["reviewed_object_id"]].append(review)
        by_config[review["configuration_blind_id"]].append(review)
        class_review_counts[review["review_context"]["classification"]] += 1

    eligible = 0
    exact = 0
    coverage_gaps = 0
    conflicts: list[dict[str, Any]] = []
    pair_class_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"eligible": 0, "exact": 0, "disagreement": 0})
    within_class_counts: dict[str, dict[str, int]] = {
        classification: {"review_count": class_review_counts[classification], "eligible": 0, "exact": 0, "disagreement": 0}
        for classification in CONTEXT_CLASSES
    }

    for object_id in sorted(by_object):
        object_reviews = sorted(by_object[object_id], key=lambda item: item["review_id"])
        for left, right in itertools.combinations(object_reviews, 2):
            left_class = left["review_context"]["classification"]
            right_class = right["review_context"]["classification"]
            pair_key = "__x__".join(sorted((left_class, right_class)))
            for axis in AXES:
                left_assessment = left["axis_assessments"][axis]
                right_assessment = right["axis_assessments"][axis]
                if "not_assessed" in {left_assessment["verdict"], right_assessment["verdict"]}:
                    coverage_gaps += 1
                    continue
                eligible += 1
                pair_class_counts[pair_key]["eligible"] += 1
                if left_class == right_class:
                    within_class_counts[left_class]["eligible"] += 1
                is_exact = assessment_signature(left_assessment) == assessment_signature(right_assessment)
                if is_exact:
                    exact += 1
                    pair_class_counts[pair_key]["exact"] += 1
                    if left_class == right_class:
                        within_class_counts[left_class]["exact"] += 1
                else:
                    pair_class_counts[pair_key]["disagreement"] += 1
                    if left_class == right_class:
                        within_class_counts[left_class]["disagreement"] += 1
                    unresolved = "unresolved" in {left_assessment["resolution_status"], right_assessment["resolution_status"]}
                    conflicts.append(
                        {
                            "conflict_id": f"{object_id}:{axis}:{left['review_id']}:{right['review_id']}",
                            "reviewed_object_id": object_id,
                            "axis": axis,
                            "left_review_id": left["review_id"],
                            "right_review_id": right["review_id"],
                            "left_context_class": left_class,
                            "right_context_class": right_class,
                            "left_configuration_blind_id": left["configuration_blind_id"],
                            "right_configuration_blind_id": right["configuration_blind_id"],
                            "left_assessment": {key: left_assessment[key] for key in ("finding_category", "severity", "verdict", "resolution_status")},
                            "right_assessment": {key: right_assessment[key] for key in ("finding_category", "severity", "verdict", "resolution_status")},
                            "unresolved": unresolved,
                        }
                    )

    false_consensus: list[dict[str, Any]] = []
    strong_classes = {"human_expert_review", "independent_replication"}
    for object_id in sorted(by_object):
        object_reviews = sorted(by_object[object_id], key=lambda item: item["review_id"])
        for axis in AXES:
            assessed = [review for review in object_reviews if review["axis_assessments"][axis]["verdict"] != "not_assessed"]
            if len(assessed) < 2:
                continue
            signatures = {assessment_signature(review["axis_assessments"][axis]) for review in assessed}
            classes = {review["review_context"]["classification"] for review in assessed}
            if len(signatures) != 1 or classes & strong_classes:
                continue
            correlated_dimensions: list[str] = []
            for dimension in DIMENSIONS:
                relationships = {review["review_context"]["dimensions"][dimension]["relationship"] for review in assessed}
                if relationships <= {"same", "unknown", "not_applicable"}:
                    correlated_dimensions.append(dimension)
            if correlated_dimensions:
                false_consensus.append(
                    {
                        "risk_id": f"FALSE-CONSENSUS:{object_id}:{axis}",
                        "reviewed_object_id": object_id,
                        "axis": axis,
                        "review_ids": [review["review_id"] for review in assessed],
                        "review_context_classes": sorted(classes),
                        "correlated_or_unknown_dimensions": correlated_dimensions,
                        "reason": "Exact agreement is present but no human-expert or independent-replication record breaks the recorded shared or unknown dependency structure.",
                        "scientific_status_effect": "none",
                    }
                )

    configuration_summaries: list[dict[str, Any]] = []
    for config_id in sorted(by_config):
        config_reviews = sorted(by_config[config_id], key=lambda item: item["review_id"])
        assessed_rows = [assessment for review in config_reviews for assessment in review["axis_assessments"].values() if assessment["verdict"] != "not_assessed"]
        configuration_summaries.append(
            {
                "configuration_blind_id": config_id,
                "review_count": len(config_reviews),
                "reviewed_object_count": len({review["reviewed_object_id"] for review in config_reviews}),
                "assessed_axis_count": len(assessed_rows),
                "not_assessed_axis_count": len(config_reviews) * len(AXES) - len(assessed_rows),
                "finding_axis_count": sum(row["finding_category"] != "no_finding" for row in assessed_rows),
                "unresolved_finding_axis_count": sum(row["resolution_status"] == "unresolved" for row in assessed_rows),
                "high_or_critical_axis_count": sum(row["severity"] in {"high", "critical"} for row in assessed_rows),
                "unique_finding_categories": sorted({row["finding_category"] for row in assessed_rows if row["finding_category"] != "no_finding"}),
                "review_context_classes": sorted({review["review_context"]["classification"] for review in config_reviews}),
            }
        )

    disagreements = eligible - exact
    unresolved_conflicts = [conflict for conflict in conflicts if conflict["unresolved"]]
    return {
        "metrics": {
            "review_record_count": len(reviews),
            "synthetic_calibration_record_count": sum(review["record_mode"] == "synthetic_calibration" for review in reviews),
            "review_execution_count": sum(review["review_context"]["review_executed"] is True for review in reviews),
            "reviewed_object_count": len(by_object),
            "axis_count": len(AXES),
            "eligible_pair_axis_comparison_count": eligible,
            "exact_assessment_agreement_count": exact,
            "assessment_disagreement_count": disagreements,
            "exact_assessment_agreement_rate": round(exact / eligible, 6) if eligible else None,
            "coverage_gap_pair_axis_count": coverage_gaps,
            "unresolved_conflict_count": len(unresolved_conflicts),
            "false_consensus_risk_count": len(false_consensus),
            "unknown_independence_record_count": class_review_counts["unknown"],
        },
        "review_context_class_summaries": [
            {
                "classification": classification,
                **within_class_counts[classification],
                "exact_agreement_rate": round(within_class_counts[classification]["exact"] / within_class_counts[classification]["eligible"], 6) if within_class_counts[classification]["eligible"] else None,
            }
            for classification in CONTEXT_CLASSES
        ],
        "review_context_pair_summaries": [
            {
                "pair_class": pair_class,
                **counts,
                "exact_agreement_rate": round(counts["exact"] / counts["eligible"], 6) if counts["eligible"] else None,
            }
            for pair_class, counts in sorted(pair_class_counts.items())
        ],
        "unresolved_conflicts": unresolved_conflicts,
        "false_consensus_risks": false_consensus,
        "blinded_configuration_comparison": {
            "ranking_forbidden": True,
            "winner": None,
            "agreement_optimization_forbidden": True,
            "configuration_summaries": configuration_summaries,
        },
    }


def build_report(suite: dict[str, Any] | None = None) -> dict[str, Any]:
    suite = load_suite() if suite is None else suite
    errors = validate_suite(suite)
    aggregate_result = aggregate(suite.get("reviews", [])) if not errors else {
        "metrics": {},
        "review_context_class_summaries": [],
        "review_context_pair_summaries": [],
        "unresolved_conflicts": [],
        "false_consensus_risks": [],
        "blinded_configuration_comparison": {"ranking_forbidden": True, "winner": None, "agreement_optimization_forbidden": True, "configuration_summaries": []},
    }
    expectation_map = {
        "review_record_count": "review_record_count",
        "reviewed_object_count": "reviewed_object_count",
        "eligible_pair_axis_comparison_count": "eligible_pair_axis_comparison_count",
        "exact_assessment_agreement_count": "exact_assessment_agreement_count",
        "assessment_disagreement_count": "assessment_disagreement_count",
        "unresolved_conflict_count": "unresolved_conflict_count",
        "false_consensus_risk_count": "false_consensus_risk_count",
        "unknown_independence_record_count": "unknown_independence_record_count",
    }
    expectations = suite.get("expectations", {})
    for expectation_key, metric_key in expectation_map.items():
        if expectations.get(expectation_key) != aggregate_result["metrics"].get(metric_key):
            add_error(errors, "metric_calibration_expectation", f"{expectation_key} expected {expectations.get(expectation_key)} but observed {aggregate_result['metrics'].get(metric_key)}")
    return {
        "schema_id": SCHEMA_ID,
        "status": "PASS" if not errors else "FAIL",
        "calibration_mode": "synthetic_calibration",
        "review_axes": list(AXES),
        "source_hashes": {
            str(SPEC_PATH.relative_to(ROOT)): sha256(SPEC_PATH),
            str(FIXTURES_PATH.relative_to(ROOT)): sha256(FIXTURES_PATH),
            str(GENERATOR_PATH.relative_to(ROOT)): sha256(GENERATOR_PATH),
            "research_control/tasks/RT-20260722-005/artifacts/review_independence_taxonomy.md": sha256(ROOT / "research_control/tasks/RT-20260722-005/artifacts/review_independence_taxonomy.md"),
            "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md": sha256(ROOT / "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md"),
            ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md": sha256(ROOT / ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md"),
        },
        **aggregate_result,
        "authority_boundary": {
            "consensus_sets_scientific_status": False,
            "metric_threshold_sets_scientific_status": False,
            "review_executed_by_task": False,
            "external_review_completed_by_task": False,
            "independent_replication_completed_by_task": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authority": False,
        },
        "errors": errors,
    }


def generated_outputs() -> tuple[bytes, bytes, dict[str, Any]]:
    report = build_report()
    report_bytes = canonical_bytes(report)
    receipt = {
        "schema_id": "v21_reviewer_agreement_compact_receipt_v1",
        "status": report["status"],
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "report_sha256": sha256_bytes(report_bytes),
        "source_hashes": report["source_hashes"],
        "metrics": report["metrics"],
        "validator_ids": [
            "metric_source_lineage",
            "metric_review_context",
            "metric_unknown_independence_explicit",
            "metric_axis_shape",
            "metric_axis_coherence",
            "metric_false_consensus_risk",
            "metric_blinded_configuration",
            "metric_no_truth_or_promotion",
        ],
        "claim_boundary_summary": "Synthetic calibration only; agreement is descriptive, disagreement remains visible, consensus is not proof, and no review, truth inference, scientific status change, or physics promotion is authorized.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    return report_bytes, canonical_bytes(receipt), report


def write_outputs() -> dict[str, Any]:
    report_bytes, receipt_bytes, report = generated_outputs()
    REPORT_PATH.write_bytes(report_bytes)
    RECEIPT_PATH.write_bytes(receipt_bytes)
    return {
        "status": report["status"],
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "receipt_path": str(RECEIPT_PATH.relative_to(ROOT)),
        "metrics": report["metrics"],
        "error_count": len(report["errors"]),
    }


def check_outputs() -> dict[str, Any]:
    report_bytes, receipt_bytes, report = generated_outputs()
    drift: list[str] = []
    for path, expected in ((REPORT_PATH, report_bytes), (RECEIPT_PATH, receipt_bytes)):
        if not path.is_file() or path.read_bytes() != expected:
            drift.append(str(path.relative_to(ROOT)))
    return {
        "status": "PASS" if report["status"] == "PASS" and not drift else "FAIL",
        "drift_paths": drift,
        "metrics": report["metrics"],
        "error_count": len(report["errors"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = write_outputs() if args.write else check_outputs()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
