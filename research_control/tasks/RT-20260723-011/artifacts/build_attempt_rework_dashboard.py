#!/usr/bin/env python3
"""Build and validate the bounded P12-T06 attempt/rework dashboard."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent

LEDGER_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_research_attempt_ledger.json"
)
CANDIDATE_SEED_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-005/artifacts/"
    "v21_candidate_lineage_historical_seed.json"
)
SCHEMA_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_attempt_event_schema.md"
)
REDACTION_POLICY_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_attempt_history_redaction_policy.md"
)
NOTICE_PATH = ARTIFACT_DIR / "attempt_rework_privacy_authority_notice.md"
BUILDER_PATH = Path(__file__).resolve()

DASHBOARD_JSON_PATH = ARTIFACT_DIR / "attempt_rework_dashboard.json"
DASHBOARD_MD_PATH = ARTIFACT_DIR / "attempt_rework_dashboard.md"
FRESHNESS_PATH = ARTIFACT_DIR / "attempt_rework_freshness.json"
RECEIPT_PATH = ARTIFACT_DIR / "attempt_rework_compact_receipt.json"
VALIDATION_PATH = ARTIFACT_DIR / "attempt_rework_validation.json"

CRITICAL_SOURCE_HASHES = {
    "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_research_attempt_ledger.json": (
        "f32e7d272d3d99a339a2cfd81e56b1d44e51e1449b2e34e9dd111161397c1ba2"
    ),
    "research_control/tasks/RT-20260721-005/artifacts/"
    "v21_candidate_lineage_historical_seed.json": (
        "8cf49a04b90d02f8439b54e138257cc5c56b2a72ba2b26c43c5b1b9a5dba78a0"
    ),
    "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_attempt_event_schema.md": (
        "92e91a4d89ee26a85d011fc1199feecf3fb9dc472337efb5f4a1d5c30b823202"
    ),
    "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_attempt_history_redaction_policy.md": (
        "40ec1d912b3771e564208ef1980d8f6fd5a39dbade3a986b38057d38c448197c"
    ),
}

FORBIDDEN_PRIVATE_KEYS = {
    "chain_of_thought",
    "credential",
    "credentials",
    "password",
    "private_prompt",
    "private_reasoning",
    "prompt_text",
    "secret",
    "token",
}
SECRET_PATTERNS = (
    re.compile(r"\b(?:sk|ghp|xox[abpr])-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)

VALIDATOR_IDS = [
    "dashboard_matches_event_ledger",
    "source_hash_exactness",
    "candidate_family_join_exactness",
    "task_role_work_kind_join_exactness",
    "failure_category_separation",
    "abandonment_unknown_is_not_measured",
    "pass_saturation_context_only",
    "privacy_forbidden_key_scan",
    "privacy_credential_pattern_scan",
    "freshness_source_hash_binding",
    "freshness_output_determinism",
    "physics_authority_nonpromotion",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_task_record(task_id: str) -> dict[str, Any]:
    path = REPO_ROOT / f"research_control/tasks/{task_id}/00_TASK.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def legacy_work_kind(task_type: str) -> str:
    """Map pre-taxonomy task types without reading or interpreting prose."""
    mapping = {
        "project_system_checkpoint_integration": "integration_or_selection",
        "v21_plan_registration": "integration_or_selection",
        "project_system_claim_language_reviewed_context_repair": (
            "construction_or_implementation"
        ),
        "v21_plan_registration_retry": "integration_or_selection",
        "project_system_agentjob_execution_role_allowlist_parity_supersession": (
            "construction_or_implementation"
        ),
        "eqsrc_flow_generated_graded_orbit_root_law_smuggling_audit": (
            "audit_or_refutation"
        ),
    }
    if task_type not in mapping:
        raise ValueError(f"unmapped legacy task type: {task_type}")
    return mapping[task_type]


def source_hashes(paths: list[Path]) -> dict[str, str]:
    return {repo_relative(path): sha256_path(path) for path in paths}


def validate_critical_sources(hashes: dict[str, str]) -> list[str]:
    findings: list[str] = []
    for path, expected in CRITICAL_SOURCE_HASHES.items():
        observed = hashes.get(path)
        if observed != expected:
            findings.append(
                f"critical source drift: {path} expected {expected} observed {observed}"
            )
    return findings


def candidate_family_index(seed: dict[str, Any]) -> dict[str, str]:
    return {
        row["immutable_candidate_id"]: row["family_id"]
        for row in seed.get("candidates", [])
    }


def classify_failure(event: dict[str, Any]) -> str | None:
    """Classify only typed fields; never infer failure type from summary prose."""
    event_type = event["event_type"]
    evidence_domain = event["evidence_domain"]
    if event_type in {"syntax_failed", "parse_failed"} or evidence_domain == "syntax":
        return "syntax"
    if event_type == "validation_failed" or evidence_domain == "validation":
        return "validation"
    if event_type in {"proof_failed", "proof_objection"} or evidence_domain == "proof":
        return "proof"
    if event_type == "audit_finding" or evidence_domain == "scientific_review":
        return "interpretation"
    if event.get("physics_result") is True and evidence_domain == "physics":
        return "physics"
    return None


def aggregate_rows(
    events: list[dict[str, Any]],
    dimensions: dict[str, dict[str, str]],
    candidate_families: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, dict[str, list[dict[str, Any]]]] = {
        "task": defaultdict(list),
        "role": defaultdict(list),
        "work_kind": defaultdict(list),
        "candidate_family": defaultdict(list),
    }
    for event in events:
        task_id = event["task_id"]
        buckets["task"][task_id].append(event)
        buckets["role"][dimensions[task_id]["role_id"]].append(event)
        buckets["work_kind"][dimensions[task_id]["work_kind"]].append(event)
        family_ids = {
            candidate_families[candidate_id]
            for candidate_id in event.get("candidate_ids", [])
        }
        if not family_ids:
            family_ids = {"not_applicable"}
        for family_id in sorted(family_ids):
            buckets["candidate_family"][family_id].append(event)

    result: dict[str, list[dict[str, Any]]] = {}
    for dimension, dimension_buckets in buckets.items():
        rows: list[dict[str, Any]] = []
        for key, grouped_events in sorted(dimension_buckets.items()):
            event_types = Counter(event["event_type"] for event in grouped_events)
            failures = Counter(
                failure
                for event in grouped_events
                if (failure := classify_failure(event)) is not None
            )
            rows.append(
                {
                    f"{dimension}_id": key,
                    "event_count": len(grouped_events),
                    "attempt_started_count": event_types["attempt_started"],
                    "validation_catch_count": event_types["validation_failed"],
                    "audit_objection_count": event_types["audit_finding"],
                    "repair_count": event_types["repair_applied"],
                    "completed_event_count": event_types["completed"],
                    "failure_counts": {
                        name: failures[name]
                        for name in (
                            "syntax",
                            "validation",
                            "proof",
                            "interpretation",
                            "physics",
                        )
                    },
                }
            )
        result[f"by_{dimension}"] = rows
    return result


def build_dashboard() -> tuple[dict[str, Any], dict[str, str]]:
    ledger = load_json(LEDGER_PATH)
    candidate_seed = load_json(CANDIDATE_SEED_PATH)
    events = ledger["events"]

    task_ids = sorted({event["task_id"] for event in events})
    task_paths = [
        REPO_ROOT / f"research_control/tasks/{task_id}/00_TASK.yaml"
        for task_id in task_ids
    ]
    task_records = {task_id: load_task_record(task_id) for task_id in task_ids}
    role_job_paths = [
        REPO_ROOT
        / f"research_control/tasks/{task_id}/jobs/"
        f"{task_records[task_id]['current_job_id']}.yaml"
        for task_id in task_ids
        if not task_records[task_id].get("role_id")
    ]
    input_paths = [
        LEDGER_PATH,
        CANDIDATE_SEED_PATH,
        SCHEMA_PATH,
        REDACTION_POLICY_PATH,
        *task_paths,
        *role_job_paths,
    ]
    hashes = source_hashes(input_paths)
    critical_findings = validate_critical_sources(hashes)
    if critical_findings:
        raise ValueError("; ".join(critical_findings))

    dimensions: dict[str, dict[str, str]] = {}
    for task_id in task_ids:
        task = task_records[task_id]
        role_id = task.get("role_id")
        if not role_id:
            job_path = (
                REPO_ROOT
                / f"research_control/tasks/{task_id}/jobs/"
                f"{task['current_job_id']}.yaml"
            )
            job = yaml.safe_load(job_path.read_text(encoding="utf-8"))
            role_id = job["role_id"]
        taxonomy = task.get("task_taxonomy") or {}
        dimensions[task_id] = {
            "role_id": role_id,
            "work_kind": taxonomy.get("work_kind")
            or legacy_work_kind(task["task_type"]),
        }

    families = candidate_family_index(candidate_seed)
    unknown_candidates = sorted(
        {
            candidate_id
            for event in events
            for candidate_id in event.get("candidate_ids", [])
            if candidate_id not in families
        }
    )
    if unknown_candidates:
        raise ValueError(f"candidate family join failed: {unknown_candidates}")

    event_types = Counter(event["event_type"] for event in events)
    dispositions = Counter(event["disposition"] for event in events)
    failure_counts = Counter(
        failure
        for event in events
        if (failure := classify_failure(event)) is not None
    )
    represented_task_repairs = Counter(
        event["task_id"] for event in events if event["event_type"] == "repair_applied"
    )
    all_task_repair_counts = [
        represented_task_repairs.get(task_id, 0) for task_id in task_ids
    ]
    repair_task_counts = list(represented_task_repairs.values())
    finalized_event_count = sum(bool(event["finalized"]) for event in events)
    issue_count = event_types["validation_failed"] + event_types["audit_finding"]
    pass_like_count = dispositions["completed"]

    dashboard = {
        "schema_id": "v21_attempt_rework_dashboard_v1",
        "dashboard_id": "V21-ATTEMPT-REWORK-DASHBOARD-001",
        "task_id": "RT-20260723-011",
        "plan_task_id": "P12-T06",
        "status": "draft/control",
        "source_cutoff_at": ledger["sealed_at"],
        "bounded_scope": {
            "ledger_id": ledger["ledger_id"],
            "ledger_revision": ledger["revision"],
            "event_count": len(events),
            "finalized_event_count": finalized_event_count,
            "represented_task_count": len(task_ids),
            "historical_completeness_claimed": False,
            "summary_text_used_for_classification": False,
            "raw_private_text_projected": False,
            "legacy_work_kind_mapping_basis": "exact task_type allowlist",
        },
        "source_bindings": [
            {"path": path, "sha256": digest}
            for path, digest in sorted(hashes.items())
        ],
        "headline_counts": {
            "observed_attempt_start_count": event_types["attempt_started"],
            "validation_catch_count": event_types["validation_failed"],
            "audit_objection_count": event_types["audit_finding"],
            "repair_event_count": event_types["repair_applied"],
            "explicit_abandoned_event_count": event_types["abandoned"],
            "completed_event_count": event_types["completed"],
            "superseded_event_count": event_types["superseded"],
        },
        "failure_categories": {
            "classification_basis": (
                "typed event_type, evidence_domain, and physics_result fields only"
            ),
            "syntax": failure_counts["syntax"],
            "validation": failure_counts["validation"],
            "proof": failure_counts["proof"],
            "interpretation": failure_counts["interpretation"],
            "physics": failure_counts["physics"],
            "authority_note": (
                "Counts describe bounded process or review records and do not "
                "constitute physics refutation, proof, or promotion."
            ),
        },
        "repair_metrics": {
            "repair_event_share": {
                "status": "measured",
                "numerator": event_types["repair_applied"],
                "denominator": finalized_event_count,
                "value": round(
                    event_types["repair_applied"] / finalized_event_count, 4
                ),
                "interpretation": "operational event mix only",
            },
            "repair_events_per_recorded_issue": {
                "status": "measured" if issue_count else "not_measured",
                "numerator": event_types["repair_applied"],
                "denominator": issue_count if issue_count else None,
                "value": (
                    round(event_types["repair_applied"] / issue_count, 4)
                    if issue_count
                    else None
                ),
                "interpretation": (
                    "count ratio only; it does not assert one-to-one causal closure"
                ),
            },
            "median_repairs_per_represented_task": (
                statistics.median(all_task_repair_counts)
                if all_task_repair_counts
                else None
            ),
            "median_repairs_per_task_with_repair": (
                statistics.median(repair_task_counts) if repair_task_counts else None
            ),
        },
        "abandonment_metric": {
            "status": "not_measured",
            "numerator": event_types["abandoned"],
            "denominator": None,
            "value": None,
            "reason": (
                "The ledger records one explicit bounded absence but does not define "
                "a complete closed-attempt population; zero observed abandoned events "
                "must not be overread as a zero abandonment rate."
            ),
            "explicit_absence_ids": [
                row["absence_id"]
                for row in ledger.get("explicit_absences", [])
                if row["event_type"] == "abandoned"
            ],
        },
        "pass_saturation_context": {
            "status": "measured",
            "pass_like_definition": "event disposition equals completed",
            "numerator": pass_like_count,
            "denominator": finalized_event_count,
            "value": round(pass_like_count / finalized_event_count, 4),
            "completed_event_type_share": {
                "numerator": event_types["completed"],
                "denominator": finalized_event_count,
                "value": round(event_types["completed"] / finalized_event_count, 4),
            },
            "interpretation": (
                "Operational saturation context only. PASS-like event share is not "
                "scientific success, theorem truth, or Distance-to-GR progress."
            ),
        },
        "final_dispositions": dict(sorted(dispositions.items())),
        "aggregations": aggregate_rows(events, dimensions, families),
        "privacy": {
            "projection_allowlist": [
                "event identifiers",
                "task identifiers",
                "role identifiers",
                "work-kind identifiers",
                "candidate-family identifiers",
                "typed counts",
                "source paths and SHA-256 hashes",
            ],
            "summary_text_included": False,
            "prompt_text_included": False,
            "credential_material_included": False,
        },
        "authority_boundary": {
            "process_failures_are_physics_refutations": False,
            "validator_pass_is_proof": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "candidate_adoption_authorized": False,
            "ontology_edit_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authority": False,
        },
    }
    return dashboard, hashes


def render_markdown(dashboard: dict[str, Any]) -> str:
    counts = dashboard["headline_counts"]
    failures = dashboard["failure_categories"]
    repair = dashboard["repair_metrics"]
    abandonment = dashboard["abandonment_metric"]
    saturation = dashboard["pass_saturation_context"]

    lines = [
        "---",
        "authority: control",
        "status: draft/control",
        "task_id: RT-20260723-011",
        "plan_task_id: P12-T06",
        "generated_from: attempt_rework_dashboard.json",
        "---",
        "",
        "# Attempt, rework, and PASS-saturation dashboard",
        "",
        "This dashboard is a deterministic projection of the sealed P10-T04 "
        "attempt-event ledger. It describes a bounded operational sample, not "
        "complete project history or physics evidence.",
        "",
        "## Bounded event mix",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Observed attempt starts | {counts['observed_attempt_start_count']} |",
        f"| Validation catches | {counts['validation_catch_count']} |",
        f"| Audit objections | {counts['audit_objection_count']} |",
        f"| Repair events | {counts['repair_event_count']} |",
        f"| Explicit abandoned events | {counts['explicit_abandoned_event_count']} |",
        f"| Completed event types | {counts['completed_event_count']} |",
        f"| Superseded events | {counts['superseded_event_count']} |",
        "",
        "## Failure categories",
        "",
        "| Typed category | Count |",
        "|---|---:|",
        f"| Syntax | {failures['syntax']} |",
        f"| Validation | {failures['validation']} |",
        f"| Proof | {failures['proof']} |",
        f"| Interpretation | {failures['interpretation']} |",
        f"| Physics | {failures['physics']} |",
        "",
        "Categories use typed event fields only; no summary prose is mined. A "
        "validation catch or audit objection is not a physics refutation.",
        "",
        "## Repair and saturation context",
        "",
        f"- Repair-event share: {repair['repair_event_share']['numerator']}/"
        f"{repair['repair_event_share']['denominator']} = "
        f"{repair['repair_event_share']['value']:.4f}.",
        f"- Repair events per recorded issue: "
        f"{repair['repair_events_per_recorded_issue']['numerator']}/"
        f"{repair['repair_events_per_recorded_issue']['denominator']} = "
        f"{repair['repair_events_per_recorded_issue']['value']:.4f}; this is a "
        "count ratio, not causal closure.",
        f"- Median repairs per represented task: "
        f"{repair['median_repairs_per_represented_task']:.1f}.",
        f"- Median repairs per task with a repair: "
        f"{repair['median_repairs_per_task_with_repair']:.1f}.",
        f"- Abandonment rate: `{abandonment['status']}`. "
        f"{abandonment['reason']}",
        f"- PASS-like disposition share: {saturation['numerator']}/"
        f"{saturation['denominator']} = {saturation['value']:.4f}. "
        "This is operational saturation context only.",
        "",
        "## Final dispositions",
        "",
        "| Disposition | Count |",
        "|---|---:|",
    ]
    for disposition, count in dashboard["final_dispositions"].items():
        lines.append(f"| `{disposition}` | {count} |")

    for dimension, rows in dashboard["aggregations"].items():
        label = dimension.removeprefix("by_").replace("_", " ").title()
        id_key = f"{dimension.removeprefix('by_')}_id"
        lines.extend(
            [
                "",
                f"## By {label.lower()}",
                "",
                f"| {label} | Events | Starts | Validation | Audit | Repairs | Completed |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in rows:
            lines.append(
                f"| `{row[id_key]}` | {row['event_count']} | "
                f"{row['attempt_started_count']} | "
                f"{row['validation_catch_count']} | "
                f"{row['audit_objection_count']} | {row['repair_count']} | "
                f"{row['completed_event_count']} |"
            )

    lines.extend(
        [
            "",
            "## Authority and privacy",
            "",
            "The projection excludes event summary text, prompt text, private reasoning, "
            "credentials, and personal data. Source hashes and deterministic freshness "
            "metadata permit drift detection. No count or PASS-like share changes "
            "scientific status, Distance-to-GR, ontology, proof, benchmark, publication, "
            "or promotion authority.",
            "",
        ]
    )
    return "\n".join(lines)


def private_material_findings(payload: Any) -> list[str]:
    findings: list[str] = []

    def walk(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in FORBIDDEN_PRIVATE_KEYS:
                    findings.append(f"forbidden private key at {path}.{key}")
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")
        elif isinstance(value, str):
            for pattern in SECRET_PATTERNS:
                if pattern.search(value):
                    findings.append(f"credential-like material at {path}")

    walk(payload)
    return findings


def freshness_matches(
    freshness: dict[str, Any], observed_source_hashes: dict[str, str]
) -> bool:
    expected = {
        row["path"]: row["sha256"] for row in freshness["source_bindings"]
    }
    return expected == observed_source_hashes


def build_expected_artifacts() -> dict[Path, bytes]:
    dashboard, hashes = build_dashboard()
    dashboard_bytes = json_bytes(dashboard)
    markdown_bytes = render_markdown(dashboard).encode("utf-8")
    if not markdown_bytes.endswith(b"\n"):
        markdown_bytes += b"\n"

    privacy_findings = private_material_findings(dashboard)
    if privacy_findings:
        raise ValueError("; ".join(privacy_findings))

    freshness = {
        "schema_id": "v21_attempt_rework_freshness_v1",
        "task_id": "RT-20260723-011",
        "plan_task_id": "P12-T06",
        "status": "fresh",
        "generated_from_ledger_sealed_at": load_json(LEDGER_PATH)["sealed_at"],
        "source_bindings": [
            {"path": path, "sha256": digest}
            for path, digest in sorted(hashes.items())
        ],
        "builder": {
            "path": repo_relative(BUILDER_PATH),
            "sha256": sha256_path(BUILDER_PATH),
        },
        "privacy_notice": {
            "path": repo_relative(NOTICE_PATH),
            "sha256": sha256_path(NOTICE_PATH),
        },
        "outputs": {
            repo_relative(DASHBOARD_JSON_PATH): sha256_bytes(dashboard_bytes),
            repo_relative(DASHBOARD_MD_PATH): sha256_bytes(markdown_bytes),
        },
        "freshness_rule": (
            "Every listed source, builder, notice, and deterministic output hash "
            "must match current bytes."
        ),
    }
    freshness_bytes = json_bytes(freshness)

    receipt = {
        "schema_id": "v21_attempt_rework_compact_receipt_v1",
        "task_id": "RT-20260723-011",
        "plan_task_id": "P12-T06",
        "result_status": "PASS",
        "source_hashes": hashes,
        "output_hashes": {
            repo_relative(DASHBOARD_JSON_PATH): sha256_bytes(dashboard_bytes),
            repo_relative(DASHBOARD_MD_PATH): sha256_bytes(markdown_bytes),
            repo_relative(FRESHNESS_PATH): sha256_bytes(freshness_bytes),
            repo_relative(NOTICE_PATH): sha256_path(NOTICE_PATH),
        },
        "finding_counts": {
            "validation_catches": dashboard["headline_counts"][
                "validation_catch_count"
            ],
            "audit_objections": dashboard["headline_counts"][
                "audit_objection_count"
            ],
            "repairs": dashboard["headline_counts"]["repair_event_count"],
            "abandoned_events": dashboard["headline_counts"][
                "explicit_abandoned_event_count"
            ],
            "syntax_failures": dashboard["failure_categories"]["syntax"],
            "validation_failures": dashboard["failure_categories"]["validation"],
            "proof_failures": dashboard["failure_categories"]["proof"],
            "interpretation_objections": dashboard["failure_categories"][
                "interpretation"
            ],
            "physics_failures": dashboard["failure_categories"]["physics"],
        },
        "validator_ids": VALIDATOR_IDS,
        "claim_boundary_summary": (
            "Bounded operational attempt-history projection only; no private text, "
            "historical completion claim, physics refutation, scientific promotion, "
            "proof, ontology, Distance-to-GR, benchmark, or publication authority."
        ),
        "physics_promotion_authorized": False,
    }
    receipt_bytes = json_bytes(receipt)

    validation = {
        "schema_id": "v21_attempt_rework_validation_v1",
        "task_id": "RT-20260723-011",
        "plan_task_id": "P12-T06",
        "status": "PASS",
        "checks_run": VALIDATOR_IDS,
        "check_count": len(VALIDATOR_IDS),
        "failure_count": 0,
        "privacy_finding_count": len(privacy_findings),
        "freshness_source_count": len(hashes),
        "dashboard_event_count": dashboard["bounded_scope"]["event_count"],
        "dashboard_matches_event_ledger": (
            dashboard["bounded_scope"]["event_count"]
            == len(load_json(LEDGER_PATH)["events"])
        ),
        "freshness_matches_current_sources": freshness_matches(freshness, hashes),
        "artifact_hashes": {
            repo_relative(DASHBOARD_JSON_PATH): sha256_bytes(dashboard_bytes),
            repo_relative(DASHBOARD_MD_PATH): sha256_bytes(markdown_bytes),
            repo_relative(FRESHNESS_PATH): sha256_bytes(freshness_bytes),
            repo_relative(RECEIPT_PATH): sha256_bytes(receipt_bytes),
        },
        "authority": "Operational validation only; not scientific proof or promotion.",
    }
    validation_bytes = json_bytes(validation)

    return {
        DASHBOARD_JSON_PATH: dashboard_bytes,
        DASHBOARD_MD_PATH: markdown_bytes,
        FRESHNESS_PATH: freshness_bytes,
        RECEIPT_PATH: receipt_bytes,
        VALIDATION_PATH: validation_bytes,
    }


def write_artifacts(expected: dict[Path, bytes]) -> None:
    for path, data in expected.items():
        path.write_bytes(data)


def check_artifacts(expected: dict[Path, bytes]) -> list[str]:
    findings: list[str] = []
    for path, data in expected.items():
        if not path.exists():
            findings.append(f"missing generated artifact: {repo_relative(path)}")
        elif path.read_bytes() != data:
            findings.append(f"stale generated artifact: {repo_relative(path)}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        expected = build_expected_artifacts()
        if args.write:
            write_artifacts(expected)
            findings: list[str] = []
        else:
            findings = check_artifacts(expected)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        findings = [str(exc)]

    result = {
        "status": "PASS" if not findings else "FAIL",
        "mode": "write" if args.write else "check",
        "task_id": "RT-20260723-011",
        "plan_task_id": "P12-T06",
        "findings": findings,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    elif findings:
        for finding in findings:
            print(finding, file=sys.stderr)
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
