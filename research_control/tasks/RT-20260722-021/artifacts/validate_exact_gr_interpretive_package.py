#!/usr/bin/env python3
"""Validate the bounded P15-T01 exact-GR interpretive package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
MANUSCRIPT = ARTIFACT_DIR / "exact_gr_interpretive_manuscript_v1.md"
CLAIM_MAP = ARTIFACT_DIR / "exact_gr_claim_map_v1.yaml"
SOURCE_PACKAGE = ARTIFACT_DIR / "exact_gr_reproducibility_source_package_v1.yaml"
REVIEW_PACKET = ARTIFACT_DIR / "exact_gr_internal_review_packet_v1.md"
REPORT = ARTIFACT_DIR / "exact_gr_interpretive_package_validation.json"

REQUIRED_FILES = (MANUSCRIPT, CLAIM_MAP, SOURCE_PACKAGE, REVIEW_PACKET)
REQUIRED_BOUNDARY_PHRASES = (
    "adopted effective law",
    "first-principles substrate derivation remains open",
    "no independent low-energy non-GR signature",
    "not blind independent human review",
    "explicit human authorization",
)
FORBIDDEN_PATTERNS = {
    "completed_source_derivation": re.compile(
        r"\b(?:we|this (?:paper|manuscript|work|project)) (?:have )?(?:derive|derived|proves?|proved) GR from",
        re.IGNORECASE,
    ),
    "ontology_established": re.compile(
        r"\b(?:the )?(?:AEther|Æther)(?:-flow)? ontology (?:is|has been) (?:established|confirmed|proven)\b",
        re.IGNORECASE,
    ),
    "independent_prediction_claim": re.compile(
        r"\b(?:predicts?|discovers?|confirms?) (?:a |an )?(?:new|independent) low-energy deviation\b",
        re.IGNORECASE,
    ),
    "false_external_review": re.compile(
        r"\b(?:independently peer reviewed|external human review completed|independent replication completed)\b",
        re.IGNORECASE,
    ),
    "publication_authority": re.compile(
        r"\b(?:approved for publication|authorized for submission|publication is authorized)\b",
        re.IGNORECASE,
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def validate() -> dict[str, object]:
    errors: list[str] = []
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "pass": bool(condition), "detail": detail})
        if not condition:
            errors.append(f"{check_id}: {detail}")

    for path in REQUIRED_FILES:
        check(f"file_exists:{path.name}", path.is_file(), "required package file must exist")
    if errors:
        return build_report(checks, errors, {}, {}, {})

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    review = REVIEW_PACKET.read_text(encoding="utf-8")
    claim_map = load_yaml(CLAIM_MAP)
    source_package = load_yaml(SOURCE_PACKAGE)

    combined = manuscript + "\n" + review
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        check(
            f"required_boundary:{phrase}",
            phrase.lower() in combined.lower(),
            f"required boundary phrase missing: {phrase}",
        )
    for pattern_id, pattern in FORBIDDEN_PATTERNS.items():
        check(
            f"forbidden_phrase:{pattern_id}",
            pattern.search(combined) is None,
            f"forbidden positive overclaim matched: {pattern_id}",
        )

    claims = claim_map.get("claims", [])
    traces = claim_map.get("equation_traces", [])
    check("claims_are_list", isinstance(claims, list), "claims must be a list")
    check("traces_are_list", isinstance(traces, list), "equation_traces must be a list")
    claims = claims if isinstance(claims, list) else []
    traces = traces if isinstance(traces, list) else []
    check("claim_count", len(claims) == 13, "claim map must contain exactly 13 claims")
    check("trace_count", len(traces) == 6, "claim map must contain exactly six equation traces")

    claim_ids = [str(item.get("claim_id", "")) for item in claims if isinstance(item, dict)]
    trace_ids = [str(item.get("equation_id", "")) for item in traces if isinstance(item, dict)]
    check("claim_ids_unique", len(claim_ids) == len(set(claim_ids)), "claim IDs must be unique")
    check("trace_ids_unique", len(trace_ids) == len(set(trace_ids)), "equation trace IDs must be unique")
    check(
        "claim_declared_count",
        claim_map.get("claim_count") == len(claims),
        "declared claim_count must equal actual claims",
    )
    check(
        "trace_declared_count",
        claim_map.get("equation_trace_count") == len(traces),
        "declared equation_trace_count must equal actual traces",
    )

    for claim in claims:
        if not isinstance(claim, dict):
            check("claim_mapping", False, "every claim entry must be a mapping")
            continue
        claim_id = str(claim.get("claim_id", "missing"))
        check(f"claim_statement:{claim_id}", bool(str(claim.get("statement", "")).strip()), "claim needs a statement")
        check(f"claim_status:{claim_id}", bool(str(claim.get("status", "")).strip()), "claim needs a status")
        check(f"claim_allowed:{claim_id}", bool(str(claim.get("allowed_use", "")).strip()), "claim needs allowed_use")
        check(f"claim_forbidden:{claim_id}", bool(str(claim.get("forbidden_overread", "")).strip()), "claim needs forbidden_overread")
        source_ids = claim.get("source_object_ids", [])
        check(
            f"claim_sources:{claim_id}",
            isinstance(source_ids, list) and bool(source_ids),
            "claim needs at least one source object ID",
        )

    displayed_equation_count = manuscript.count("$$") // 2
    manuscript_trace_ids = re.findall(r"<!-- equation-trace: (EQ-\d{3}) -->", manuscript)
    check("displayed_equation_count", displayed_equation_count == 6, "manuscript must contain six displayed equations")
    check("manuscript_trace_count", len(manuscript_trace_ids) == 6, "each displayed equation needs one trace marker")
    check("manuscript_trace_unique", len(manuscript_trace_ids) == len(set(manuscript_trace_ids)), "trace markers must be unique")
    check("trace_sets_match", set(manuscript_trace_ids) == set(trace_ids), "manuscript and claim-map trace IDs must match")
    for trace in traces:
        if not isinstance(trace, dict):
            check("trace_mapping", False, "every trace entry must be a mapping")
            continue
        trace_id = str(trace.get("equation_id", "missing"))
        source_ids = trace.get("source_object_ids", [])
        source_labels = trace.get("source_labels", [])
        check(f"trace_sources:{trace_id}", isinstance(source_ids, list) and bool(source_ids), "trace needs sources")
        check(f"trace_labels:{trace_id}", isinstance(source_labels, list) and bool(source_labels), "trace needs labels")
        check(f"trace_boundary:{trace_id}", trace.get("adoption_not_derivation") is True, "trace must preserve adoption boundary")

    canonical_sources = source_package.get("canonical_sources", [])
    dependency_sources = source_package.get("dependency_sources", [])
    check("canonical_sources_list", isinstance(canonical_sources, list) and len(canonical_sources) >= 8, "canonical source list incomplete")
    check("dependency_sources_list", isinstance(dependency_sources, list) and len(dependency_sources) == 3, "three P14 dependencies required")
    canonical_sources = canonical_sources if isinstance(canonical_sources, list) else []
    dependency_sources = dependency_sources if isinstance(dependency_sources, list) else []

    for item in canonical_sources:
        if not isinstance(item, dict):
            check("canonical_source_mapping", False, "canonical source must be a mapping")
            continue
        source_id = str(item.get("object_id", "missing"))
        rel_path = str(item.get("path", ""))
        expected = str(item.get("sha256", ""))
        path = REPO_ROOT / rel_path
        check(f"canonical_exists:{source_id}", path.is_file(), f"canonical source missing: {rel_path}")
        if path.is_file():
            check(f"canonical_hash:{source_id}", sha256(path) == expected, f"canonical source hash mismatch: {rel_path}")

    for item in dependency_sources:
        if not isinstance(item, dict):
            check("dependency_mapping", False, "dependency source must be a mapping")
            continue
        task_id = str(item.get("plan_task_id", "missing"))
        for path_key, hash_key in (("artifact_path", "artifact_sha256"), ("completion_path", "completion_sha256")):
            rel_path = str(item.get(path_key, ""))
            expected = str(item.get(hash_key, ""))
            path = REPO_ROOT / rel_path
            check(f"dependency_exists:{task_id}:{path_key}", path.is_file(), f"dependency file missing: {rel_path}")
            if path.is_file():
                check(f"dependency_hash:{task_id}:{path_key}", sha256(path) == expected, f"dependency hash mismatch: {rel_path}")

    global_boundary = claim_map.get("global_boundary", {})
    authority_limits = source_package.get("authority_limits", {})
    check("global_boundary_mapping", isinstance(global_boundary, dict), "global_boundary must be a mapping")
    check("authority_limits_mapping", isinstance(authority_limits, dict), "authority_limits must be a mapping")
    if isinstance(global_boundary, dict):
        for key in (
            "first_principles_substrate_derivation_established",
            "ontology_established_as_physical_fact",
            "independent_low_energy_novelty_present",
            "external_human_review_present",
            "publication_authorized",
            "benchmark_promotion_authorized",
            "physics_promotion_authorized",
        ):
            check(f"global_false:{key}", global_boundary.get(key) is False, f"{key} must be false")
    if isinstance(authority_limits, dict):
        for key, value in authority_limits.items():
            check(f"authority_false:{key}", value is False, f"authority limit {key} must be false")

    review_false_markers = (
        "blind_review: false",
        "independent_review: false",
        "external_human_review: false",
        "peer_review: false",
        "publication_authorized: false",
    )
    for marker in review_false_markers:
        check(f"review_marker:{marker}", marker in review, f"review packet missing {marker}")

    return build_report(checks, errors, claim_map, source_package, {
        "manuscript_sha256": sha256(MANUSCRIPT),
        "claim_map_sha256": sha256(CLAIM_MAP),
        "source_package_sha256": sha256(SOURCE_PACKAGE),
        "review_packet_sha256": sha256(REVIEW_PACKET),
    })


def build_report(
    checks: list[dict[str, object]],
    errors: list[str],
    claim_map: dict[str, object],
    source_package: dict[str, object],
    artifact_hashes: dict[str, str],
) -> dict[str, object]:
    passed = sum(1 for item in checks if item.get("pass") is True)
    return {
        "schema_id": "exact_gr_interpretive_package_validation_v1",
        "status": f"PASS_{passed}_CHECKS" if not errors else "FAIL",
        "validation_passed": not errors,
        "check_count": len(checks),
        "passed_check_count": passed,
        "failed_check_count": len(errors),
        "errors": errors,
        "claim_count": len(claim_map.get("claims", [])) if isinstance(claim_map.get("claims", []), list) else 0,
        "equation_trace_count": len(claim_map.get("equation_traces", [])) if isinstance(claim_map.get("equation_traces", []), list) else 0,
        "canonical_source_count": len(source_package.get("canonical_sources", [])) if isinstance(source_package.get("canonical_sources", []), list) else 0,
        "dependency_source_count": len(source_package.get("dependency_sources", [])) if isinstance(source_package.get("dependency_sources", []), list) else 0,
        "artifact_hashes": artifact_hashes,
        "authority_effect": "operational_validation_only_no_scientific_or_publication_authority",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        REPORT.write_text(serialized, encoding="utf-8")
    elif not REPORT.is_file():
        report["validation_passed"] = False
        report["status"] = "FAIL"
        report.setdefault("errors", []).append("validation report is missing")
        serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != serialized:
            report["validation_passed"] = False
            report["status"] = "FAIL"
            report.setdefault("errors", []).append("validation report is stale")
            serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.json:
        print(serialized, end="")
    else:
        print(report["status"])
    return 0 if report.get("validation_passed") is True else 1


if __name__ == "__main__":
    sys.exit(main())

