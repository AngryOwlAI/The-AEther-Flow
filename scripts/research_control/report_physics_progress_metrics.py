#!/usr/bin/env python3
"""Report operational physics-progress metrics from tracked control records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402
import report_scientific_payload_density as scientific_payload_density  # noqa: E402
import scientific_quality_metrics  # noqa: E402
import task_taxonomy  # noqa: E402


PHYSICS_AUTHORITY_LEVELS = {"science_draft", "human_gated"}
PHYSICS_ROLE_KIND_PREFIX = "scientific_"
ROLE_METRIC_KEYS = {
    "theoretical-continuation-selector": "selector_tasks",
    "candidate-constructor": "candidate_constructor_tasks",
    "smuggling-auditor": "smuggling_auditor_tasks",
    "refuter": "refuter_tasks",
    "gate-chair": "gate_chair_tasks",
}
OPERATIONAL_METRIC_KEY_TOKENS = {
    "checker",
    "diagnostic_warning",
    "methodology",
    "ai_methodology",
    "proof_to_process",
    "validator",
    "validation",
    "registry",
    "generated",
    "memory",
    "payload_density",
    "payload_ratio",
    "route_orbit",
    "wiki",
    "receipt",
    "role_schema",
    "handoff_continuity",
}
PROJECT_SYSTEM_AUTHORITY_LEVELS = {
    "project_control",
    "process_control",
    "routing_control",
}
PROJECT_SYSTEM_TASK_TOKENS = (
    "audit",
    "checkpoint",
    "control",
    "dashboard",
    "documentation",
    "handoff",
    "ledger",
    "memory",
    "metrics",
    "policy",
    "process",
    "ratio",
    "registry",
    "route_history",
    "route_orbit",
    "schema",
    "support",
    "validator",
)
THEOREM_COUNTERMODEL_CLASSES = {
    "new_theorem_statement",
    "proved_theorem",
    "conditional_theorem",
    "proof_attempt",
    "countermodel",
    "obstruction",
}
PHYSICS_BEARING_PAYLOAD_CLASSES = THEOREM_COUNTERMODEL_CLASSES | {
    "new_definition",
    "finite_witness",
    "dependency_map_update",
    "source_extension_classification",
}
SUPPORT_ONLY_CHECKER_ID = "finite_local_candidate_checker"
SUPPORT_ONLY_CHECKER_REPORT_GLOB = "research_control/tasks/*/artifacts/*checker_report.json"
SUPPORT_ONLY_BOUNDARY_REQUIRED_PHRASES = ("support-only", "not proof authority")
AI_METHODOLOGY_TAXONOMY_PATH = "research_control/design/ai_research_agent_metrics_taxonomy_v1.md"
PHYSICS_PAYLOAD_RATIO_POLICY_PATH = "research_control/design/physics_payload_ratio_policy_v1.md"
DUAL_BUDGET_POLICY_PATH = (
    "research_control/tasks/RT-20260722-014/artifacts/dual_budget_policy_v1.md"
)
DUAL_BUDGET_DASHBOARD_SCHEMA_PATH = (
    "research_control/tasks/RT-20260722-014/artifacts/budget_dashboard_schema_v1.md"
)
ORDINARY_ROUTE_GUARD_POLICY_PATH = (
    "research_control/tasks/RT-20260722-015/artifacts/ordinary_route_guard_policy_v1.md"
)
CANDIDATE_LINEAGE_REGISTRY_PATH = (
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json"
)
AI_METHODOLOGY_REQUIRED_METRICS = (
    "overclaim_catch_rate",
    "underclaim_warning_rate",
    "obstruction_precision",
    "route_orbit_rate",
    "candidate_to_audit_conversion",
    "audit_to_stress_survival",
    "stress_survival_rate",
    "human_gate_load",
    "proof_to_process_ratio",
)
AI_METHODOLOGY_METRIC_SPECS: dict[str, dict[str, str]] = {
    "overclaim_catch_rate": {
        "family": "Claim-boundary control",
        "definition": "Fraction of seeded or real overclaim surfaces caught before checkpoint.",
        "numerator": "Count of overclaim surfaces flagged before checkpoint.",
        "denominator": "Count of overclaim surfaces eligible for detection in the reviewed scope.",
        "guardrail": "A high rate means better boundary control; it does not prove any physics claim.",
    },
    "underclaim_warning_rate": {
        "family": "Claim-boundary control",
        "definition": "Fraction of high-risk summaries missing positive scoped status that were warned or corrected.",
        "numerator": "Count of eligible summaries where missing positive scoped status was flagged or corrected.",
        "denominator": "Count of high-risk summaries whose tracked evidence included scoped positive status and whose summary could omit it.",
        "guardrail": "This metric prevents pessimistic status collapse; it does not promote scoped evidence into adoption.",
    },
    "obstruction_precision": {
        "family": "Obstruction quality",
        "definition": "Fraction of obstruction records scoped with a non-global boundary.",
        "numerator": "Count of obstruction or negative-result records naming object, assumptions, route, and downstream blocked claim without globalizing.",
        "denominator": "Count of obstruction or negative-result records produced or reviewed in the measurement window.",
        "guardrail": "A precise obstruction remains local unless a separate theorem and protected authority establish a stronger no-go result.",
    },
    "route_orbit_rate": {
        "family": "Route dynamics",
        "definition": "Frequency of repeated-burden cycles without new payload.",
        "numerator": "Count of route cycles returning to the same burden or equivalent continuation family without new mathematical payload.",
        "denominator": "Count of bounded continuation packets in the measurement window.",
        "guardrail": "This is a process-warning metric; it is advisory unless a separate validator or policy makes a gate.",
    },
    "candidate_to_audit_conversion": {
        "family": "Candidate life cycle",
        "definition": "Fraction of candidate-constructor outputs that become eligible for audit.",
        "numerator": "Count of candidate-constructor outputs with enough declared scope, assumptions, and artifacts to route to audit.",
        "denominator": "Count of candidate-constructor outputs in the window.",
        "guardrail": "Eligibility for audit is not audit survival, adoption, or matter-coupling derivation.",
    },
    "audit_to_stress_survival": {
        "family": "Candidate life cycle",
        "definition": "Fraction of audited candidates that reach stress.",
        "numerator": "Count of audited candidates routed to Refuter stress or equivalent stress packet.",
        "denominator": "Count of audited candidates with completed audit disposition.",
        "guardrail": "Reaching stress means the candidate remains testable; it does not mean the candidate is true or adopted.",
    },
    "stress_survival_rate": {
        "family": "Candidate life cycle",
        "definition": "Fraction of stressed candidates that survive as draft/control.",
        "numerator": "Count of stressed candidates whose post-stress status remains draft/control or equivalent non-promotional survivor status.",
        "denominator": "Count of stressed candidates with completed stress disposition.",
        "guardrail": "Survival is candidate-status only; it does not authorize canonical ontology, source-law, metric, or coupling adoption.",
    },
    "human_gate_load": {
        "family": "Governance load",
        "definition": "Number of protected authority requests per phase.",
        "numerator": "Count of human-gated authority requests, Gate Chair requests, or protected adoption requests in a phase.",
        "denominator": "Phase identifier and completed packet count, not a physics-progress denominator.",
        "guardrail": "Human authorization for a task is not a Gate Chair verdict unless the protected gate itself states that verdict.",
    },
    "proof_to_process_ratio": {
        "family": "Payload balance",
        "definition": "Mathematical payload artifacts compared with process receipts.",
        "numerator": "Count of new mathematical payload artifacts.",
        "denominator": "Count of process receipts.",
        "guardrail": "This ratio is a productivity and balance signal; neither numerator nor denominator creates proof authority by itself.",
    },
}


@dataclass
class MetricsBuildInstrumentation:
    """Mutable counters scoped to one metrics build."""

    completion_files_read: int = 0


@dataclass(frozen=True)
class MetricsSnapshot:
    """Immutable serialized outputs and instrumentation from one live build."""

    report_json: str
    report_markdown: str
    completion_files_read: int
    snapshot_builds: int = 1

    def materialize_report(self) -> dict[str, Any]:
        report = json.loads(self.report_json)
        if not isinstance(report, dict):
            raise ValueError("metrics snapshot report must be a mapping")
        return report


def read_csv_rows(repo_root: Path, registry_name: str) -> list[dict[str, str]]:
    path = repo_root / "registries" / registry_name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return [value] if value else []
    return []


def bool_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return None


def role_key(role_id: str, version: str) -> tuple[str, str]:
    return role_id, version


def is_physics_role(role: dict[str, str] | None) -> bool:
    if not role:
        return False
    return (
        role.get("authority_level", "") in PHYSICS_AUTHORITY_LEVELS
        or role.get("role_kind", "").startswith(PHYSICS_ROLE_KIND_PREFIX)
    )


def completion_text(
    repo_root: Path,
    path_text: str,
    instrumentation: MetricsBuildInstrumentation | None = None,
) -> str:
    path = repo_root / path_text
    if not path.exists():
        return ""
    if instrumentation is not None:
        instrumentation.completion_files_read += 1
    return path.read_text(encoding="utf-8")


def load_yaml_document(repo_root: Path, path_text: str) -> dict[str, Any]:
    if not path_text:
        return {}
    path = repo_root / path_text
    if not path.exists():
        return {}
    try:
        return load_yaml(path)
    except StrictYamlError:
        return {}


def load_completion(
    repo_root: Path,
    path_text: str,
    instrumentation: MetricsBuildInstrumentation | None = None,
) -> dict[str, Any]:
    path = repo_root / path_text
    if path_text and path.exists() and instrumentation is not None:
        instrumentation.completion_files_read += 1
    return load_yaml_document(repo_root, path_text)


def status_from_progress(completion: dict[str, Any]) -> str:
    progress = completion.get("physics_progress_status")
    if isinstance(progress, dict):
        return str(progress.get("status", "")).strip()
    return ""


def changed_from_delta(completion: dict[str, Any]) -> bool | None:
    delta = completion.get("distance_to_gr_delta")
    if isinstance(delta, dict):
        return bool_value(delta.get("changed"))
    return None


def obstruction_id(completion: dict[str, Any]) -> str:
    record = completion.get("obstruction_record")
    if not isinstance(record, dict) or bool_value(record.get("present")) is not True:
        return ""
    return str(record.get("obstruction_id", "")).strip()


def freeze_decision(completion: dict[str, Any]) -> str:
    record = completion.get("freeze_criteria_status")
    if not isinstance(record, dict):
        return ""
    return str(record.get("freeze_decision", "")).strip()


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def string_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def int_value(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def payload_count(completion: dict[str, Any]) -> int:
    manifest = completion.get("mathematical_payload_manifest")
    if isinstance(manifest, list):
        return len(manifest)
    legacy = completion.get("new_mathematical_payload")
    if isinstance(legacy, list):
        return len(legacy)
    return 0


def first_nonblank(*values: Any) -> str:
    for value in values:
        text = string_value(value)
        if text:
            return text
    return ""


def selected_packet_type(completion: dict[str, Any]) -> str:
    decision = dict_value(completion.get("theoretical_decision_output"))
    return first_nonblank(
        decision.get("selected_next_packet_type"),
        decision.get("selected_packet_type_for_validator"),
        decision.get("selected_next_packet_family"),
        decision.get("packet_type"),
    )


def selected_role_hint(completion: dict[str, Any]) -> str:
    decision = dict_value(completion.get("theoretical_decision_output"))
    return first_nonblank(
        decision.get("selected_next_role"),
        decision.get("next_execution_role_family"),
        decision.get("selected_next_role_family"),
    )


def source_extension_category(completion: dict[str, Any]) -> str:
    return string_value(completion.get("source_extension_category"))


def burden_key(completion: dict[str, Any]) -> tuple[str, str]:
    progress = dict_value(completion.get("physics_progress_status"))
    delta = dict_value(completion.get("distance_to_gr_delta"))
    milestone = first_nonblank(
        progress.get("target_derivation_milestone"),
        delta.get("milestone"),
    )
    burden = first_nonblank(
        progress.get("milestone_burden"),
        delta.get("burden_id"),
    )
    if not milestone and not burden:
        return "", ""
    return milestone, burden


def bridge_attempt_present(completion: dict[str, Any]) -> bool:
    bridge = dict_value(completion.get("bridge_attempt_status"))
    if any(string_value(value) for value in bridge.values()):
        return True
    category = source_extension_category(completion)
    return "candidate" in category or "construction" in category


def completion_record(
    repo_root: Path,
    row: dict[str, str],
    completion: dict[str, Any],
    is_physics: bool,
    instrumentation: MetricsBuildInstrumentation | None = None,
) -> dict[str, Any]:
    progress = dict_value(completion.get("physics_progress_status"))
    delta = dict_value(completion.get("distance_to_gr_delta"))
    route = dict_value(completion.get("route_cycle_control"))
    freeze = dict_value(completion.get("freeze_criteria_status"))
    candidate = dict_value(completion.get("candidate_constructor_result"))
    obstruction = dict_value(completion.get("obstruction_record"))
    forbidden = dict_value(completion.get("forbidden_conclusion_summary"))
    completion_path = row.get("completion_path", "")
    job_doc = load_yaml_document(repo_root, row.get("job_path", ""))

    return {
        "task_id": first_nonblank(completion.get("task_id"), row.get("task_id", "")),
        "job_id": row.get("job_id", ""),
        "role_id": row.get("role_id", ""),
        "role_version": row.get("role_version", ""),
        "job_path": row.get("job_path", ""),
        "completion_path": completion_path,
        "created_at": row.get("created_at", ""),
        "completed_at": row.get("completed_at", ""),
        "is_physics": is_physics,
        "text": completion_text(repo_root, completion_path, instrumentation),
        "progress_status": string_value(progress.get("status")),
        "milestone": first_nonblank(progress.get("target_derivation_milestone"), delta.get("milestone")),
        "burden_id": first_nonblank(progress.get("milestone_burden"), delta.get("burden_id")),
        "burden_key": burden_key(completion),
        "delta_effect": string_value(delta.get("effect")),
        "delta_changed": changed_from_delta(completion),
        "payload_count": payload_count(completion),
        "cycle_family": string_value(route.get("cycle_family")),
        "cycle_step": string_value(route.get("current_cycle_step")),
        "cycle_risk": string_value(route.get("cycle_risk")),
        "candidate_result_type": string_value(candidate.get("result_type")),
        "selected_next_packet_type": selected_packet_type(completion),
        "selected_role_hint": selected_role_hint(completion),
        "freeze_repeated_burden": bool_value(freeze.get("repeated_burden")) is True,
        "freeze_evaluation_required": bool_value(freeze.get("freeze_evaluation_required")) is True,
        "freeze_decision": string_value(freeze.get("freeze_decision")),
        "obstruction_present": bool_value(obstruction.get("present")) is True,
        "obstruction_id": string_value(obstruction.get("obstruction_id")),
        "physics_promotion_authorized": bool_value(
            forbidden.get("physics_promotion_authorized")
        ) is True,
        "has_forbidden_conclusion_summary": isinstance(
            completion.get("forbidden_conclusion_summary"),
            dict,
        ),
        "bridge_attempt_present": bridge_attempt_present(completion),
        "source_extension_category": source_extension_category(completion),
        "job_support_only": bool_value(job_doc.get("support_only")) is True,
        "dual_budget_allocation": dict_value(job_doc.get("dual_budget_allocation")),
        "dual_budget_result": dict_value(completion.get("dual_budget_result")),
    }


def has_candidate_signal(record: dict[str, Any]) -> bool:
    status = record.get("progress_status", "")
    return (
        record.get("role_id") == "candidate-constructor"
        or bool(record.get("candidate_result_type"))
        or status.startswith("candidate_")
        or record.get("bridge_attempt_present") is True
    )


def has_obstruction_signal(record: dict[str, Any]) -> bool:
    return (
        record.get("obstruction_present") is True
        or record.get("candidate_result_type") in {"precise_obstruction", "minimal_countermodel"}
        or record.get("progress_status") == "precise_obstruction_found"
    )


def has_freeze_signal(record: dict[str, Any]) -> bool:
    return (
        record.get("freeze_repeated_burden") is True
        or record.get("freeze_evaluation_required") is True
        or bool(record.get("freeze_decision"))
        or record.get("progress_status") == "route_frozen"
    )


def task_has_payload_classes(task_row: dict[str, Any], classes: set[str]) -> bool:
    counts = task_row.get("payload_class_counts")
    if not isinstance(counts, dict):
        return False
    return sum(int(counts.get(class_id, 0)) for class_id in classes) > 0


def collect_physics_progress_integration_metrics(
    completion_records: list[dict[str, Any]],
    payload_report: dict[str, Any],
) -> dict[str, Any]:
    """Integrate distance-delta and payload-density diagnostics for P9-T03."""
    distance_effect_counts: Counter[str] = Counter()
    candidate_result_counts: Counter[str] = Counter()

    for record in completion_records:
        effect = record.get("delta_effect") or "missing_effect"
        distance_effect_counts[effect] += 1
        result_type = record.get("candidate_result_type")
        if result_type:
            candidate_result_counts[result_type] += 1

    theorem_classes = {
        "new_theorem_statement",
        "proved_theorem",
        "conditional_theorem",
        "proof_attempt",
    }
    task_rows = payload_report.get("task_rows") if isinstance(payload_report, dict) else []
    if not isinstance(task_rows, list):
        task_rows = []
    theorem_task_count = sum(
        1
        for task_row in task_rows
        if isinstance(task_row, dict) and task_has_payload_classes(task_row, theorem_classes)
    )

    overall_payload = (
        payload_report.get("overall", {})
        if isinstance(payload_report.get("overall"), dict)
        else {}
    )
    payload_class_counts = (
        overall_payload.get("payload_class_counts", {})
        if isinstance(overall_payload.get("payload_class_counts"), dict)
        else {}
    )

    return {
        "status": "pass",
        "authority_boundary": "operational_summary_only_not_physics_proof",
        "not_physics_proof": True,
        "physics_claim_promotion_authorized": False,
        "reporting_role": "raw_volume_operational_context_only",
        "primary_scientific_quality_surface": False,
        "distance_delta": {
            "records_read": len(completion_records),
            "effect_counts": dict(sorted(distance_effect_counts.items())),
            "changed_true_count": sum(1 for record in completion_records if record.get("delta_changed") is True),
            "changed_false_count": sum(1 for record in completion_records if record.get("delta_changed") is False),
        },
        "separate_packet_counts": {
            "candidate_packet_count": sum(1 for record in completion_records if has_candidate_signal(record)),
            "obstruction_packet_count": sum(1 for record in completion_records if has_obstruction_signal(record)),
            "freeze_packet_count": sum(1 for record in completion_records if has_freeze_signal(record)),
            "theorem_packet_count": theorem_task_count,
            "process_only_packet_count": int(overall_payload.get("process_only_task_count", 0)),
        },
        "candidate_result_counts": dict(sorted(candidate_result_counts.items())),
        "payload_density_summary": {
            "task_count": int(overall_payload.get("task_count", 0)),
            "classified_item_count": int(overall_payload.get("classified_item_count", 0)),
            "mathematical_payload_item_count": int(
                overall_payload.get("mathematical_payload_item_count", 0)
            ),
            "process_only_item_count": int(overall_payload.get("process_only_item_count", 0)),
            "mathematical_payload_task_count": int(
                overall_payload.get("mathematical_payload_task_count", 0)
            ),
            "process_only_task_count": int(overall_payload.get("process_only_task_count", 0)),
            "payload_density": float(overall_payload.get("payload_density", 0.0)),
            "task_payload_density": float(overall_payload.get("task_payload_density", 0.0)),
            "payload_class_counts": dict(sorted(payload_class_counts.items())),
        },
    }


def has_payload_classes(task_row: dict[str, Any], classes: set[str]) -> bool:
    counts = task_row.get("payload_class_counts")
    if not isinstance(counts, dict):
        return False
    return sum(int_value(counts.get(class_id, 0)) for class_id in classes) > 0


def is_project_system_role(role: dict[str, str] | None) -> bool:
    if not role:
        return False
    role_kind = role.get("role_kind", "").lower()
    authority = role.get("authority_level", "").lower()
    return (
        authority in PROJECT_SYSTEM_AUTHORITY_LEVELS
        or role_kind.startswith(("project_", "process_", "routing_"))
        or "validation" in role_kind
        or "documentation" in role_kind
    )


def is_project_system_task(
    task_row: dict[str, str],
    task_doc: dict[str, Any],
    job_doc: dict[str, Any],
    role: dict[str, str] | None,
    plan_item: dict[str, Any] | None = None,
) -> bool:
    normalized = task_taxonomy.classify_task(
        task_doc,
        task_row,
        job_doc,
        role or {},
        plan_item or {},
    )
    if normalized["scope"] in {"project_system", "routing"}:
        return True
    if normalized["authority"] in PROJECT_SYSTEM_AUTHORITY_LEVELS:
        return True
    if normalized["scope"] in {"scientific", "scientific_audit", "human_gate"}:
        return False
    task_type = " ".join(
        [
            task_row.get("task_type", ""),
            string_value(task_doc.get("task_type")),
            string_value(job_doc.get("route_label")),
        ]
    ).lower()
    milestone = first_nonblank(
        task_doc.get("target_derivation_milestone"),
        job_doc.get("target_derivation_milestone"),
    ).lower()
    project_boundary = bool_value(job_doc.get("project_system_boundary_authorized_by_plan")) is True
    support_only = bool_value(job_doc.get("support_only")) is True
    return (
        is_project_system_role(role)
        or milestone == "none"
        or project_boundary
        or support_only
        or any(token in task_type for token in PROJECT_SYSTEM_TASK_TOKENS)
    )


def task_payload_row_by_task_id(payload_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload_report.get("task_rows") if isinstance(payload_report, dict) else []
    if not isinstance(rows, list):
        return {}
    return {
        string_value(row.get("task_id")): row
        for row in rows
        if isinstance(row, dict) and string_value(row.get("task_id"))
    }


def task_payload_item_count(record: dict[str, Any], payload_row: dict[str, Any]) -> int:
    del payload_row
    return int_value(record.get("payload_count", 0))


def task_has_theorem_countermodel_candidate_signal(
    record: dict[str, Any],
    task_row: dict[str, str],
    task_doc: dict[str, Any],
    payload_row: dict[str, Any],
    job_doc: dict[str, Any] | None = None,
    role: dict[str, str] | None = None,
    plan_item: dict[str, Any] | None = None,
) -> bool:
    normalized = task_taxonomy.classify_task(
        task_doc,
        task_row,
        job_doc or {},
        role or {},
        plan_item or {},
    )
    normalized_signal = (
        normalized["scope"] in {"scientific", "scientific_audit", "human_gate", "mixed"}
        and (
            normalized["work_kind"] == "formalization_or_theorem"
            or normalized["result_kind"] in {
                "candidate_or_precise_obstruction",
                "theorem_or_precise_obstruction",
            }
            or normalized["candidate_family"] not in {"not_applicable", "unknown"}
        )
    )
    task_text = " ".join(
        [
            task_row.get("task_type", ""),
            string_value(task_doc.get("task_type")),
            record.get("progress_status", ""),
            record.get("candidate_result_type", ""),
            record.get("text", ""),
        ]
    ).lower()
    structured_signal = (
        normalized_signal
        or has_payload_classes(payload_row, THEOREM_COUNTERMODEL_CLASSES)
        or has_candidate_signal(record)
        or has_obstruction_signal(record)
    )
    if normalized["taxonomy_source"] in {"explicit", "plan_metadata"}:
        return structured_signal
    return structured_signal or any(
        token in task_text
        for token in ("theorem", "lemma", "proposition", "countermodel", "candidate")
    )


def classify_payload_ratio_route_history(
    repo_root: Path,
    completion_records: list[dict[str, Any]],
    task_rows: list[dict[str, str]],
    roles: dict[tuple[str, str], dict[str, str]],
    payload_report: dict[str, Any],
) -> list[dict[str, Any]]:
    task_registry_by_id = {
        row.get("task_id", ""): row
        for row in task_rows
        if row.get("task_id")
    }
    payload_by_task_id = task_payload_row_by_task_id(payload_report)
    try:
        plan_items = task_taxonomy.load_plan_items(repo_root)
    except task_taxonomy.TaskTaxonomyError:
        plan_items = {}

    rows: list[dict[str, Any]] = []
    for record in sorted(completion_records, key=lambda item: (item.get("created_at", ""), item.get("job_id", ""))):
        task_id = record.get("task_id", "")
        task_row = task_registry_by_id.get(task_id, {})
        task_path = task_row.get("task_path", "")
        task_doc = load_yaml_document(repo_root, f"{task_path}/00_TASK.yaml") if task_path else {}
        job_doc = load_yaml_document(repo_root, record.get("job_path", ""))
        role = roles.get(role_key(record.get("role_id", ""), record.get("role_version", "")))
        plan_item = plan_items.get(task_taxonomy.plan_task_id(task_doc), {})
        payload_row = payload_by_task_id.get(task_id, {})
        math_payload_count = task_payload_item_count(record, payload_row)
        candidate_signal = has_candidate_signal(record)
        theorem_countermodel_candidate_signal = task_has_theorem_countermodel_candidate_signal(
            record,
            task_row,
            task_doc,
            payload_row,
            job_doc,
            role,
            plan_item,
        )
        physics_bearing = (
            record.get("is_physics") is True
            and (
                math_payload_count > 0
                or has_payload_classes(payload_row, PHYSICS_BEARING_PAYLOAD_CLASSES)
                or candidate_signal
                or has_obstruction_signal(record)
            )
        )
        normalized = task_taxonomy.classify_task(
            task_doc,
            task_row,
            job_doc,
            role or {},
            plan_item,
        )
        project_system = is_project_system_task(
            task_row,
            task_doc,
            job_doc,
            role,
            plan_item,
        ) and not physics_bearing
        support_only = project_system or bool_value(job_doc.get("support_only")) is True

        rows.append(
            {
                "task_id": task_id,
                "job_id": record.get("job_id", ""),
                "role_id": record.get("role_id", ""),
                "task_type": first_nonblank(task_row.get("task_type", ""), task_doc.get("task_type")),
                "work_kind": normalized["work_kind"],
                "milestone": normalized["milestone"],
                "candidate_family": normalized["candidate_family"],
                "result_kind": normalized["result_kind"],
                "authority": normalized["authority"],
                "scope": normalized["scope"],
                "taxonomy_source": normalized["taxonomy_source"],
                "taxonomy_confidence": normalized["taxonomy_confidence"],
                "completed_at": record.get("completed_at", ""),
                "project_system_task": project_system,
                "physics_bearing_task": physics_bearing,
                "support_only_task": support_only,
                "mathematical_payload_items": math_payload_count,
                "theorem_countermodel_candidate_signal": theorem_countermodel_candidate_signal,
                "candidate_construction_signal": candidate_signal,
                "completion_path": record.get("completion_path", ""),
            }
        )
    return rows


def trailing_run_length(rows: list[dict[str, Any]], key: str) -> int:
    run_length = 0
    for row in reversed(rows):
        if row.get(key) is True:
            run_length += 1
            continue
        break
    return run_length


def count_since_last_physics_payload(rows: list[dict[str, Any]]) -> int:
    count = 0
    for row in reversed(rows):
        if row.get("physics_bearing_task") is True:
            break
        if row.get("support_only_task") is True:
            count += 1
    return count


def route_orbit_warning_status(diagnostic_warnings: list[dict[str, Any]]) -> dict[str, Any]:
    route_warnings = [
        warning
        for warning in diagnostic_warnings
        if "route" in string_value(warning.get("warning_id")).lower()
        or "burden" in string_value(warning.get("warning_id")).lower()
        or "cycle" in string_value(warning.get("metric_key")).lower()
    ]
    return {
        "status": "warning" if route_warnings else "clear",
        "warning_ids": [string_value(warning.get("warning_id")) for warning in route_warnings],
        "hard_gate": any(bool_value(warning.get("hard_gate")) is True for warning in route_warnings),
        "physics_claim_authority": any(
            bool_value(warning.get("physics_claim_authority")) is True
            for warning in route_warnings
        ),
        "advisory_only": True,
    }


def collect_physics_payload_ratio_diagnostics(
    repo_root: Path,
    completion_records: list[dict[str, Any]],
    task_rows: list[dict[str, str]],
    roles: dict[tuple[str, str], dict[str, str]],
    payload_report: dict[str, Any],
    route_orbit_risk_metrics: dict[str, Any],
    diagnostic_warnings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute P8-T02 support-only route-history and payload-ratio diagnostics."""
    route_history = classify_payload_ratio_route_history(
        repo_root,
        completion_records,
        task_rows,
        roles,
        payload_report,
    )
    project_system_task_count = sum(1 for row in route_history if row["project_system_task"])
    physics_bearing_task_count = sum(1 for row in route_history if row["physics_bearing_task"])
    support_only_task_count = sum(1 for row in route_history if row["support_only_task"])
    new_mathematical_payload_count = sum(
        int_value(row["mathematical_payload_items"])
        for row in route_history
    )
    theorem_countermodel_candidate_count = sum(
        1 for row in route_history if row["theorem_countermodel_candidate_signal"]
    )
    candidate_construction_count = sum(
        1 for row in route_history if row["candidate_construction_signal"]
    )

    diagnostics = {
        "project_system_task_run_length": trailing_run_length(route_history, "project_system_task"),
        "physics_bearing_task_run_length": trailing_run_length(route_history, "physics_bearing_task"),
        "new_mathematical_payload_count": new_mathematical_payload_count,
        "theorem_countermodel_candidate_count": theorem_countermodel_candidate_count,
        "candidate_construction_count": candidate_construction_count,
        "support_only_task_count_since_last_physics_payload": count_since_last_physics_payload(route_history),
        "route_orbit_warning_status": route_orbit_warning_status(diagnostic_warnings),
        "project_system_task_count": project_system_task_count,
        "physics_bearing_task_count": physics_bearing_task_count,
        "support_only_task_count": support_only_task_count,
        "physics_bearing_to_project_system_task_ratio": ratio(
            physics_bearing_task_count,
            project_system_task_count,
        ),
        "new_mathematical_payload_to_support_only_task_ratio": ratio(
            new_mathematical_payload_count,
            support_only_task_count,
        ),
        "route_orbit_same_burden_repetition_count": int_value(
            route_orbit_risk_metrics.get("same_burden_repetition_count", 0)
        ),
    }
    diagnostics["ordinary_route_guard_status"] = {
        "policy_id": "ordinary_route_guard_policy_v1",
        "policy_source_path": ORDINARY_ROUTE_GUARD_POLICY_PATH,
        "warning_at": 2,
        "hard_threshold": 3,
        "prospective_hard_gate_active": True,
        "current_run_requires_physics_route_or_exception": (
            diagnostics["project_system_task_run_length"] >= 3
        ),
        "system_work_counts_as_physics": False,
    }

    return {
        "schema_id": "physics_payload_ratio_route_history_metrics_v1",
        "status": "measured",
        "policy_source_path": PHYSICS_PAYLOAD_RATIO_POLICY_PATH,
        "calculation_window": "all tracked completion records available at report generation",
        "metrics": diagnostics,
        "route_history_tail": route_history[-10:],
        "classification_counts": {
            "route_history_records": len(route_history),
            "project_system_task_count": project_system_task_count,
            "physics_bearing_task_count": physics_bearing_task_count,
            "support_only_task_count": support_only_task_count,
        },
        "authority_boundary": {
            "ai_system_diagnostics_only": True,
            "does_not_rank_physics_truth": True,
            "not_physics_proof": True,
            "physics_claim_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "gate_chair_verdict_created": False,
            "completed_derivation_authorized": False,
        },
    }


def _dual_budget_timestamp(value: object) -> datetime | None:
    text = string_value(value)
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _dual_budget_elapsed_seconds(record: dict[str, Any]) -> float | None:
    started = _dual_budget_timestamp(record.get("created_at"))
    completed = _dual_budget_timestamp(record.get("completed_at"))
    if not started or not completed or completed < started:
        return None
    return round((completed - started).total_seconds(), 3)


def _dual_budget_lane_lists(value: object) -> dict[str, list[str]]:
    source = value if isinstance(value, dict) else {}
    result: dict[str, list[str]] = {}
    for budget in ("physics", "project_system"):
        items = source.get(budget, [])
        result[budget] = (
            [string_value(item) for item in items if string_value(item)]
            if isinstance(items, list)
            else []
        )
    return result


def _dual_budget_measurement_status(measured: int, missing: int) -> str:
    if measured and missing:
        return "partially_measured"
    if measured:
        return "measured"
    return "not_measured"


def _dual_budget_number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def collect_dual_budget_dashboard(
    completion_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build separate support-only accounting lanes without inferring physics truth."""

    categories: Counter[str] = Counter()
    explicit_count = 0
    legacy_count = 0
    blocked_exception_count = 0
    single_credit_ok = True
    mixed_outputs_ok = True
    mixed_criteria_ok = True
    missing_compute_zero_ok = True
    system_science_authority_ok = True
    lanes: dict[str, dict[str, Any]] = {
        budget: {
            "task_count_credit": 0,
            "elapsed_measured_record_count": 0,
            "elapsed_not_measured_record_count": 0,
            "elapsed_seconds": 0.0,
            "compute_measured_record_count": 0,
            "compute_not_measured_record_count": 0,
            "compute_values_by_unit": defaultdict(float),
            "declared_durable_output_count": 0,
            "durable_output_measured_record_count": 0,
            "durable_output_not_measured_record_count": 0,
            "declared_acceptance_criterion_count": 0,
            "acceptance_measured_record_count": 0,
            "acceptance_not_measured_record_count": 0,
        }
        for budget in ("physics", "project_system")
    }

    for record in completion_records:
        allocation = dict_value(record.get("dual_budget_allocation"))
        result = dict_value(record.get("dual_budget_result"))
        explicit = bool(allocation)
        if explicit:
            explicit_count += 1
            category = string_value(allocation.get("category")) or "unclassified"
            primary = string_value(allocation.get("primary_budget"))
            credits_source = dict_value(allocation.get("task_count_credit"))
            credits = {
                budget: int_value(credits_source.get(budget), -1)
                for budget in ("physics", "project_system")
            }
            outputs = _dual_budget_lane_lists(
                result.get("observed_durable_outputs")
                if result
                else allocation.get("expected_durable_outputs")
            )
            criteria = _dual_budget_lane_lists(
                result.get("accepted_criteria")
                if result
                else allocation.get("acceptance_criteria")
            )
            measurements = dict_value(
                result.get("resource_measurement")
                if result
                else allocation.get("resource_measurement")
            )
            exception = dict_value(allocation.get("blocked_physics_exception"))
            if exception.get("active") is True:
                blocked_exception_count += 1
        else:
            legacy_count += 1
            category = "physics_bearing" if record.get("is_physics") is True else "system_bearing"
            if record.get("job_support_only") is True and record.get("is_physics") is not True:
                category = "support_only"
            primary = "physics" if category == "physics_bearing" else "project_system"
            credits = {
                "physics": 1 if primary == "physics" else 0,
                "project_system": 1 if primary == "project_system" else 0,
            }
            outputs = {"physics": [], "project_system": []}
            criteria = {"physics": [], "project_system": []}
            measurements = {}

        categories[category] += 1
        if (
            any(value not in {0, 1} for value in credits.values())
            or sum(credits.values()) != 1
            or primary not in credits
            or credits.get(primary) != 1
        ):
            single_credit_ok = False
        if set(outputs["physics"]) & set(outputs["project_system"]):
            mixed_outputs_ok = False
        if set(criteria["physics"]) & set(criteria["project_system"]):
            mixed_criteria_ok = False
        if category in {"system_bearing", "support_only"} and (
            outputs["physics"]
            or criteria["physics"]
            or record.get("delta_changed") is True
        ):
            system_science_authority_ok = False

        for budget in ("physics", "project_system"):
            lane = lanes[budget]
            credit = credits.get(budget, 0)
            if credit in {0, 1}:
                lane["task_count_credit"] += credit

            if explicit:
                lane["declared_durable_output_count"] += len(outputs[budget])
                lane["durable_output_measured_record_count"] += 1
                lane["declared_acceptance_criterion_count"] += len(criteria[budget])
                lane["acceptance_measured_record_count"] += 1
                lane_measurements = dict_value(measurements.get(budget))
                elapsed = dict_value(lane_measurements.get("elapsed_effort"))
                compute = dict_value(lane_measurements.get("compute"))
                elapsed_value = _dual_budget_number(elapsed.get("value"))
                compute_value = _dual_budget_number(compute.get("value"))
                if string_value(elapsed.get("status")) == "measured" and elapsed_value is not None:
                    lane["elapsed_measured_record_count"] += 1
                    lane["elapsed_seconds"] += elapsed_value
                else:
                    lane["elapsed_not_measured_record_count"] += 1
                if string_value(compute.get("status")) == "measured" and compute_value is not None:
                    lane["compute_measured_record_count"] += 1
                    unit = string_value(compute.get("unit")) or "unspecified"
                    lane["compute_values_by_unit"][unit] += compute_value
                else:
                    lane["compute_not_measured_record_count"] += 1
                    if string_value(compute.get("status")) == "not_measured" and compute.get(
                        "value"
                    ) is not None:
                        missing_compute_zero_ok = False
            elif credit == 1:
                elapsed_seconds = _dual_budget_elapsed_seconds(record)
                if elapsed_seconds is None:
                    lane["elapsed_not_measured_record_count"] += 1
                else:
                    lane["elapsed_measured_record_count"] += 1
                    lane["elapsed_seconds"] += elapsed_seconds
                lane["compute_not_measured_record_count"] += 1
                lane["durable_output_not_measured_record_count"] += 1
                lane["acceptance_not_measured_record_count"] += 1

    rendered_lanes: dict[str, Any] = {}
    for budget, lane in lanes.items():
        elapsed_measured = lane.pop("elapsed_measured_record_count")
        elapsed_missing = lane.pop("elapsed_not_measured_record_count")
        elapsed_seconds = round(lane.pop("elapsed_seconds"), 3)
        compute_measured = lane.pop("compute_measured_record_count")
        compute_missing = lane.pop("compute_not_measured_record_count")
        compute_values = {
            key: round(value, 6)
            for key, value in sorted(lane.pop("compute_values_by_unit").items())
        }
        output_measured = lane.pop("durable_output_measured_record_count")
        output_missing = lane.pop("durable_output_not_measured_record_count")
        acceptance_measured = lane.pop("acceptance_measured_record_count")
        acceptance_missing = lane.pop("acceptance_not_measured_record_count")
        rendered_lanes[budget] = {
            **lane,
            "elapsed_effort": {
                "status": _dual_budget_measurement_status(elapsed_measured, elapsed_missing),
                "value_seconds": elapsed_seconds if elapsed_measured else None,
                "measured_record_count": elapsed_measured,
                "not_measured_record_count": elapsed_missing,
            },
            "compute": {
                "status": _dual_budget_measurement_status(compute_measured, compute_missing),
                "values_by_unit": compute_values,
                "measured_record_count": compute_measured,
                "not_measured_record_count": compute_missing,
            },
            "durable_outputs": {
                "status": _dual_budget_measurement_status(output_measured, output_missing),
                "declared_count": lane["declared_durable_output_count"],
                "measured_record_count": output_measured,
                "not_measured_record_count": output_missing,
            },
            "acceptance_criteria": {
                "status": _dual_budget_measurement_status(
                    acceptance_measured, acceptance_missing
                ),
                "declared_count": lane["declared_acceptance_criterion_count"],
                "measured_record_count": acceptance_measured,
                "not_measured_record_count": acceptance_missing,
            },
        }

    return {
        "schema_id": "dual_budget_dashboard_v1",
        "status": "measured",
        "policy_source_path": DUAL_BUDGET_POLICY_PATH,
        "dashboard_schema_path": DUAL_BUDGET_DASHBOARD_SCHEMA_PATH,
        "record_count": len(completion_records),
        "prospective_allocation_record_count": explicit_count,
        "legacy_classified_record_count": legacy_count,
        "category_counts": dict(sorted(categories.items())),
        "lanes": rendered_lanes,
        "blocked_physics_exception_count": blocked_exception_count,
        "integrity": {
            "single_primary_credit_status": "pass" if single_credit_ok else "fail",
            "mixed_output_disjointness_status": "pass" if mixed_outputs_ok else "fail",
            "mixed_acceptance_disjointness_status": "pass" if mixed_criteria_ok else "fail",
            "missing_compute_zero_coercion_status": (
                "pass" if missing_compute_zero_ok else "fail"
            ),
            "system_science_authority_separation_status": (
                "pass" if system_science_authority_ok else "fail"
            ),
        },
        "advisory_route_ratio": {
            "project_system_run_threshold": 3,
            "threshold_is_hard_gate_in_this_policy": False,
            "ordinary_route_guard_owner": "P12-T04",
            "separate_prospective_hard_guard_active": True,
            "separate_guard_policy_id": "ordinary_route_guard_policy_v1",
            "separate_guard_policy_path": ORDINARY_ROUTE_GUARD_POLICY_PATH,
        },
        "authority_boundary": {
            "dashboard_is_support_only": True,
            "does_not_rank_physics_truth": True,
            "system_success_counts_as_physics": False,
            "system_success_counts_as_distance_to_gr": False,
            "physics_claim_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "gate_chair_verdict_created": False,
            "completed_derivation_authorized": False,
        },
    }


def ai_methodology_authority_boundary() -> dict[str, bool]:
    return {
        "physics_claim_authority_created": False,
        "physics_promotion_authorized": False,
        "gate_chair_verdict_created": False,
        "benchmark_promotion_authorized": False,
        "metrics_report_not_physics_proof": True,
    }


def ratio(numerator: Any, denominator: Any) -> float | None:
    if not isinstance(numerator, (int, float)) or not isinstance(denominator, (int, float)):
        return None
    if denominator == 0:
        return None
    return round(float(numerator) / float(denominator), 4)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def collect_candidate_lineage_metrics(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Read validated immutable candidate IDs as support-only lifecycle evidence."""

    repo_root = Path(repo_root)
    registry_path = repo_root / CANDIDATE_LINEAGE_REGISTRY_PATH
    authority_boundary = {
        "record_kind": "project_control",
        "candidate_lifecycle_metrics_are_support_only": True,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "candidate_adoption_authorized": False,
        "candidate_rejection_authorized": False,
        "physics_promotion_authorized": False,
        "metrics_report_not_physics_proof": True,
    }
    unavailable = {
        "schema_id": "candidate_lineage_metrics_v1",
        "status": "not_measured",
        "registry_path": CANDIDATE_LINEAGE_REGISTRY_PATH,
        "historical_seed_path": "",
        "candidate_ids": [],
        "candidate_lifecycle": {},
        "metrics": {},
        "explicit_absences": [],
        "errors": [],
        "authority_boundary": authority_boundary,
    }
    if not registry_path.is_file():
        unavailable["errors"] = ["candidate lineage registry is not present"]
        return unavailable

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        seed_relative = str(registry.get("historical_seed_path", ""))
        seed_path = repo_root / seed_relative
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        unavailable["status"] = "invalid"
        unavailable["errors"] = [f"candidate lineage registry could not be loaded: {exc}"]
        return unavailable

    errors: list[str] = []
    if hashlib.sha256(seed_path.read_bytes()).hexdigest() != registry.get(
        "historical_seed_sha256"
    ):
        errors.append("historical seed hash mismatch")

    collection_key_map = {
        "families_sha256": "families",
        "candidates_sha256": "candidates",
        "lineage_edges_sha256": "lineage_edges",
        "stage_records_sha256": "stage_records",
        "family_events_sha256": "family_events",
        "explicit_absences_sha256": "explicit_absences",
    }
    collection_hashes = registry.get("collection_hashes", {})
    for hash_key, seed_key in collection_key_map.items():
        if canonical_json_sha256(seed.get(seed_key, [])) != collection_hashes.get(hash_key):
            errors.append(f"{seed_key} collection hash mismatch")

    candidates = seed.get("candidates", [])
    stages = seed.get("stage_records", [])
    edges = seed.get("lineage_edges", [])
    family_events = seed.get("family_events", [])
    explicit_absences = seed.get("explicit_absences", [])
    if not all(
        isinstance(value, list)
        for value in (candidates, stages, edges, family_events, explicit_absences)
    ):
        errors.append("lineage seed collections must be arrays")
        candidates, stages, edges, family_events, explicit_absences = [], [], [], [], []

    candidate_index = registry.get("candidate_identity_index", {})
    candidate_by_id = {
        str(candidate.get("immutable_candidate_id", "")): candidate
        for candidate in candidates
        if candidate.get("immutable_candidate_id")
    }
    if set(candidate_by_id) != set(candidate_index):
        errors.append("candidate identity index does not cover the seed exactly")
    for candidate_id, candidate in candidate_by_id.items():
        if candidate.get("candidate_identity_sha256") != candidate_index.get(candidate_id):
            errors.append(f"candidate identity binding mismatch for {candidate_id}")

    stages_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for stage in stages:
        candidate_id = str(stage.get("candidate_id", ""))
        if candidate_id not in candidate_by_id:
            errors.append(f"stage references unknown candidate {candidate_id}")
            continue
        if stage.get("candidate_identity_sha256") != candidate_index.get(candidate_id):
            errors.append(f"stage identity binding mismatch for {stage.get('stage_id', '')}")
        stages_by_candidate[candidate_id].append(stage)

    superseded_by: dict[str, str] = {}
    for edge in edges:
        source = str(edge.get("from_candidate_id", ""))
        target = str(edge.get("to_candidate_id", ""))
        if source not in candidate_by_id or target not in candidate_by_id:
            errors.append(f"lineage edge {edge.get('edge_id', '')} has an unknown endpoint")
            continue
        if edge.get("supersedes") is True:
            superseded_by[source] = target

    frozen_terminal_ids = {
        str(candidate_id)
        for event in family_events
        if event.get("event_kind") == "freeze"
        for candidate_id in event.get("terminal_candidate_ids", [])
    }
    candidate_lifecycle: dict[str, dict[str, Any]] = {}
    constructed_ids: list[str] = []
    audited_ids: list[str] = []
    stressed_ids: list[str] = []
    stress_survivor_ids: list[str] = []
    for candidate_id in sorted(candidate_by_id):
        candidate_stages = sorted(
            stages_by_candidate.get(candidate_id, []),
            key=lambda stage: int(stage.get("sequence", 0)),
        )
        stage_ids_by_kind: dict[str, list[str]] = defaultdict(list)
        for stage in candidate_stages:
            stage_ids_by_kind[str(stage.get("stage_kind", ""))].append(
                str(stage.get("stage_id", ""))
            )
        has_construction = bool(
            stage_ids_by_kind.get("construction") or stage_ids_by_kind.get("repair")
        )
        has_audit = bool(stage_ids_by_kind.get("audit"))
        has_stress = bool(stage_ids_by_kind.get("stress"))
        stress_survived = any(
            stage.get("stage_kind") == "stress"
            and "obstruction" not in str(stage.get("source_stage_type", ""))
            and "obstruction" not in str(stage.get("disposition", ""))
            for stage in candidate_stages
        )
        if has_construction:
            constructed_ids.append(candidate_id)
        if has_audit:
            audited_ids.append(candidate_id)
        if has_stress:
            stressed_ids.append(candidate_id)
        if stress_survived:
            stress_survivor_ids.append(candidate_id)
        candidate_lifecycle[candidate_id] = {
            "candidate_identity_sha256": candidate_index.get(candidate_id, ""),
            "family_id": candidate_by_id[candidate_id].get("family_id", ""),
            "stage_ids_by_kind": dict(sorted(stage_ids_by_kind.items())),
            "superseded_by_candidate_id": superseded_by.get(candidate_id),
            "family_freeze_recorded": candidate_id in frozen_terminal_ids,
            "stress_survived_as_draft_control": stress_survived,
        }

    metric_values = {
        "candidate_to_audit_conversion": {
            "numerator_candidate_ids": sorted(audited_ids),
            "denominator_candidate_ids": sorted(constructed_ids),
            "value": ratio(len(audited_ids), len(constructed_ids)),
        },
        "audit_to_stress_survival": {
            "numerator_candidate_ids": sorted(stressed_ids),
            "denominator_candidate_ids": sorted(audited_ids),
            "value": ratio(len(stressed_ids), len(audited_ids)),
        },
        "stress_survival_rate": {
            "numerator_candidate_ids": sorted(stress_survivor_ids),
            "denominator_candidate_ids": sorted(stressed_ids),
            "value": ratio(len(stress_survivor_ids), len(stressed_ids)),
        },
    }
    return {
        "schema_id": "candidate_lineage_metrics_v1",
        "status": "invalid" if errors else "measured",
        "registry_path": CANDIDATE_LINEAGE_REGISTRY_PATH,
        "historical_seed_path": seed_relative,
        "candidate_ids": sorted(candidate_by_id),
        "candidate_lifecycle": candidate_lifecycle,
        "metrics": metric_values,
        "explicit_absences": explicit_absences,
        "errors": errors,
        "authority_boundary": authority_boundary,
    }


def ai_metric_record(
    metric_id: str,
    status: str,
    numerator_value: Any,
    denominator_value: Any,
    calculation_window: str,
    evidence_paths: list[str],
    diagnostic_interpretation: str,
    value: Any = None,
    uncertainty_note: str = "",
    breakdown: dict[str, Any] | None = None,
) -> dict[str, Any]:
    spec = AI_METHODOLOGY_METRIC_SPECS[metric_id]
    return {
        "metric_id": metric_id,
        "family": spec["family"],
        "status": status,
        "definition": spec["definition"],
        "value": value,
        "numerator": {
            "label": spec["numerator"],
            "value": numerator_value,
            "evidence_paths": sorted(set(path for path in evidence_paths if path)),
        },
        "denominator": {
            "label": spec["denominator"],
            "value": denominator_value,
            "evidence_paths": sorted(set(path for path in evidence_paths if path)),
        },
        "calculation_window": calculation_window,
        "diagnostic_interpretation": diagnostic_interpretation,
        "interpretation_guardrail": spec["guardrail"],
        "uncertainty_note": uncertainty_note,
        "breakdown": breakdown or {},
        "authority_boundary": ai_methodology_authority_boundary(),
    }


def plan_phase_from_task(row: dict[str, str]) -> str:
    closure_status = row.get("closure_status", "").lower()
    for part in closure_status.split("_"):
        if part.startswith("p") and part[1:].isdigit():
            return part.upper()
    return "unclassified"


def counted_status(numerator: int, denominator: int, partial: bool = False) -> str:
    if denominator <= 0:
        return "not_measured"
    if partial:
        return "partial"
    return "measured"


def collect_ai_research_agent_methodology_metrics(
    completion_records: list[dict[str, Any]],
    task_rows: list[dict[str, str]],
    payload_report: dict[str, Any],
    payload_density_metrics: dict[str, Any],
    route_orbit_risk_metrics: dict[str, Any],
    diagnostic_warnings: list[dict[str, Any]],
    candidate_lineage_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build support-only AI research-agent methodology diagnostics for v17 P12-T02."""
    calculation_window = "all tracked completion records and task registry rows available at report generation"
    taxonomy_evidence = [AI_METHODOLOGY_TAXONOMY_PATH]
    completion_paths = [
        record.get("completion_path", "")
        for record in completion_records
        if record.get("completion_path")
    ]

    overclaim_records = [
        record for record in completion_records if record.get("has_forbidden_conclusion_summary")
    ]
    overclaim_caught = [
        record for record in overclaim_records if record.get("physics_promotion_authorized") is False
    ]

    obstruction_records = [record for record in completion_records if has_obstruction_signal(record)]
    precise_obstructions = [
        record
        for record in obstruction_records
        if record.get("obstruction_id")
        and (record.get("milestone") or record.get("burden_id") or record.get("progress_status"))
    ]

    candidate_outputs = [
        record
        for record in completion_records
        if record.get("role_id") == "candidate-constructor" or record.get("candidate_result_type")
    ]
    audit_eligible = [
        record
        for record in candidate_outputs
        if record.get("candidate_result_type")
        or record.get("progress_status") == "candidate_constructed_pending_audit"
    ]
    audit_records = [
        record
        for record in completion_records
        if record.get("role_id") == "smuggling-auditor"
        or record.get("progress_status") == "candidate_audited_pending_stress"
    ]
    stress_records = [
        record
        for record in completion_records
        if record.get("role_id") == "refuter"
        or record.get("progress_status") == "candidate_stress_passed_pending_gate"
    ]
    stress_survivors = [
        record
        for record in stress_records
        if record.get("progress_status") == "candidate_stress_passed_pending_gate"
    ]

    task_gate_rows = [
        row for row in task_rows if str(row.get("requires_human_gate", "")).lower() == "true"
    ]
    gate_chair_records = [
        record for record in completion_records if record.get("role_id") == "gate-chair"
    ]
    phase_gate_counts: Counter[str] = Counter()
    phase_task_counts: Counter[str] = Counter()
    for row in task_rows:
        phase = plan_phase_from_task(row)
        phase_task_counts[phase] += 1
        if str(row.get("requires_human_gate", "")).lower() == "true":
            phase_gate_counts[phase] += 1

    overall_payload = (
        payload_report.get("overall", {})
        if isinstance(payload_report.get("overall"), dict)
        else {}
    )
    mathematical_payload_items = int(overall_payload.get("mathematical_payload_item_count", 0))
    process_receipt_items = int(overall_payload.get("process_only_item_count", 0))

    lineage = candidate_lineage_metrics or {}
    lineage_ready = lineage.get("status") == "measured"
    lineage_metric_values = lineage.get("metrics", {}) if lineage_ready else {}
    lineage_evidence = [
        str(lineage.get("registry_path", "")),
        str(lineage.get("historical_seed_path", "")),
    ]
    absence_ids = [
        str(item.get("absence_id", ""))
        for item in lineage.get("explicit_absences", [])
        if isinstance(item, dict) and item.get("absence_id")
    ]

    if lineage_ready:
        candidate_to_audit = lineage_metric_values["candidate_to_audit_conversion"]
        audited_candidate_ids = candidate_to_audit["numerator_candidate_ids"]
        constructed_candidate_ids = candidate_to_audit["denominator_candidate_ids"]
        candidate_to_audit_record = ai_metric_record(
            "candidate_to_audit_conversion",
            counted_status(len(audited_candidate_ids), len(constructed_candidate_ids)),
            len(audited_candidate_ids),
            len(constructed_candidate_ids),
            "P10-T03 immutable EqSrc historical seed",
            lineage_evidence,
            "Exact immutable candidate IDs replace the former aggregate completion-stage proxy; an audit stage is counted only when bound to the same candidate identity hash.",
            candidate_to_audit["value"],
            breakdown={
                "numerator_candidate_ids": audited_candidate_ids,
                "denominator_candidate_ids": constructed_candidate_ids,
                "explicit_absence_ids": absence_ids,
            },
        )

        audit_to_stress = lineage_metric_values["audit_to_stress_survival"]
        stressed_candidate_ids = audit_to_stress["numerator_candidate_ids"]
        audit_denominator_ids = audit_to_stress["denominator_candidate_ids"]
        audit_to_stress_record = ai_metric_record(
            "audit_to_stress_survival",
            counted_status(len(stressed_candidate_ids), len(audit_denominator_ids)),
            len(stressed_candidate_ids),
            len(audit_denominator_ids),
            "P10-T03 immutable EqSrc historical seed",
            lineage_evidence,
            "Exact candidate-keyed lineage counts only observed stress stages; the explicit graded-orbit stress absence is not inferred as a pass or failure.",
            audit_to_stress["value"],
            breakdown={
                "numerator_candidate_ids": stressed_candidate_ids,
                "denominator_candidate_ids": audit_denominator_ids,
                "explicit_absence_ids": absence_ids,
            },
        )

        stress_survival = lineage_metric_values["stress_survival_rate"]
        stress_survivor_ids = stress_survival["numerator_candidate_ids"]
        stress_denominator_ids = stress_survival["denominator_candidate_ids"]
        stress_survival_record = ai_metric_record(
            "stress_survival_rate",
            counted_status(len(stress_survivor_ids), len(stress_denominator_ids)),
            len(stress_survivor_ids),
            len(stress_denominator_ids),
            "P10-T03 immutable EqSrc historical seed",
            lineage_evidence,
            "The seeded stressed candidates all carry scoped obstruction dispositions; local freeze remains preserved and is not relabeled as survival adoption rejection or global no-go.",
            stress_survival["value"],
            breakdown={
                "numerator_candidate_ids": stress_survivor_ids,
                "denominator_candidate_ids": stress_denominator_ids,
                "explicit_absence_ids": absence_ids,
            },
        )
    else:
        candidate_to_audit_record = ai_metric_record(
            "candidate_to_audit_conversion",
            counted_status(len(audit_eligible), len(candidate_outputs)),
            len(audit_eligible) if candidate_outputs else None,
            len(candidate_outputs) if candidate_outputs else None,
            calculation_window,
            taxonomy_evidence + [
                record.get("completion_path", "")
                for record in candidate_outputs
                if record.get("completion_path")
            ],
            "Candidate outputs are counted as audit-eligible only when tracked fields expose candidate result or pending-audit status.",
            ratio(len(audit_eligible), len(candidate_outputs)),
        )
        audit_to_stress_record = ai_metric_record(
            "audit_to_stress_survival",
            counted_status(len(stress_records), len(audit_records), partial=True),
            len(stress_records) if audit_records else None,
            len(audit_records) if audit_records else None,
            calculation_window,
            taxonomy_evidence + [
                record.get("completion_path", "")
                for record in audit_records + stress_records
                if record.get("completion_path")
            ],
            "This is an aggregate route-stage proxy because no valid immutable candidate-lineage snapshot is available.",
            ratio(len(stress_records), len(audit_records)),
            "Partial because the current completion records count stage occurrences, not candidate-linked transitions.",
        )
        stress_survival_record = ai_metric_record(
            "stress_survival_rate",
            counted_status(len(stress_survivors), len(stress_records), partial=True),
            len(stress_survivors) if stress_records else None,
            len(stress_records) if stress_records else None,
            calculation_window,
            taxonomy_evidence + [
                record.get("completion_path", "")
                for record in stress_records
                if record.get("completion_path")
            ],
            "Stress survival is counted only as a non-promotional candidate-status outcome.",
            ratio(len(stress_survivors), len(stress_records)),
            "Partial because no valid immutable candidate-lineage snapshot is available.",
        )

    metric_records = {
        "overclaim_catch_rate": ai_metric_record(
            "overclaim_catch_rate",
            counted_status(len(overclaim_caught), len(overclaim_records)),
            len(overclaim_caught) if overclaim_records else None,
            len(overclaim_records) if overclaim_records else None,
            calculation_window,
            taxonomy_evidence + [
                record.get("completion_path", "")
                for record in overclaim_records
                if record.get("completion_path")
            ],
            "Forbidden-conclusion summaries are counted as eligible overclaim-control surfaces; caught means no physics promotion was authorized.",
            ratio(len(overclaim_caught), len(overclaim_records)),
        ),
        "underclaim_warning_rate": ai_metric_record(
            "underclaim_warning_rate",
            "not_measured",
            None,
            None,
            calculation_window,
            taxonomy_evidence,
            "The current registries do not deterministically encode high-risk positive scoped-status omission events.",
            None,
            "Needs a future extraction rule for accepted-scoped evidence omitted from summaries.",
        ),
        "obstruction_precision": ai_metric_record(
            "obstruction_precision",
            counted_status(len(precise_obstructions), len(obstruction_records)),
            len(precise_obstructions) if obstruction_records else None,
            len(obstruction_records) if obstruction_records else None,
            calculation_window,
            taxonomy_evidence + [
                record.get("completion_path", "")
                for record in obstruction_records
                if record.get("completion_path")
            ],
            "This deterministic proxy counts obstruction records with IDs plus milestone, burden, or status context as locally scoped.",
            ratio(len(precise_obstructions), len(obstruction_records)),
        ),
        "route_orbit_rate": ai_metric_record(
            "route_orbit_rate",
            counted_status(
                int(route_orbit_risk_metrics.get("same_burden_repetition_count", 0)),
                int(payload_density_metrics.get("physics_completions_read", 0)),
            ),
            int(route_orbit_risk_metrics.get("same_burden_repetition_count", 0)),
            int(payload_density_metrics.get("physics_completions_read", 0)),
            calculation_window,
            taxonomy_evidence + [
                path
                for warning in diagnostic_warnings
                if warning.get("warning_id") == "same_burden_repetition"
                for path in list_value(warning.get("evidence_paths"))
            ],
            "Repeated-burden streaks are process warnings only and do not change Distance-to-GR status.",
            ratio(
                int(route_orbit_risk_metrics.get("same_burden_repetition_count", 0)),
                int(payload_density_metrics.get("physics_completions_read", 0)),
            ),
        ),
        "candidate_to_audit_conversion": candidate_to_audit_record,
        "audit_to_stress_survival": audit_to_stress_record,
        "stress_survival_rate": stress_survival_record,
        "human_gate_load": ai_metric_record(
            "human_gate_load",
            "measured",
            {
                "task_rows_requiring_human_gate": len(task_gate_rows),
                "gate_chair_completion_records": len(gate_chair_records),
                "total_gate_load_signals": len(task_gate_rows) + len(gate_chair_records),
                "per_phase_task_rows_requiring_human_gate": dict(sorted(phase_gate_counts.items())),
            },
            {
                "registered_task_rows": len(task_rows),
                "per_phase_registered_task_rows": dict(sorted(phase_task_counts.items())),
            },
            calculation_window,
            taxonomy_evidence
            + [row.get("task_path", "") for row in task_gate_rows if row.get("task_path")]
            + [
                record.get("completion_path", "")
                for record in gate_chair_records
                if record.get("completion_path")
            ],
            "Gate-load signals are governance workload diagnostics, not Gate Chair scientific verdicts.",
            None,
        ),
        "proof_to_process_ratio": ai_metric_record(
            "proof_to_process_ratio",
            counted_status(mathematical_payload_items, process_receipt_items),
            mathematical_payload_items if process_receipt_items else None,
            process_receipt_items if process_receipt_items else None,
            calculation_window,
            taxonomy_evidence + completion_paths,
            "Payload balance compares mathematical payload items to process-only items; it is not proof authority.",
            ratio(mathematical_payload_items, process_receipt_items),
        ),
    }

    calibrated_warnings: list[dict[str, Any]] = []
    for metric_id in AI_METHODOLOGY_REQUIRED_METRICS:
        record = metric_records[metric_id]
        if record["status"] == "measured":
            continue
        calibrated_warnings.append(
            {
                "warning_id": f"{metric_id}_{record['status']}",
                "severity": "warning",
                "metric_id": metric_id,
                "status": record["status"],
                "reason": record["uncertainty_note"] or record["diagnostic_interpretation"],
                "hard_gate": False,
                "physics_claim_authority": False,
                "recommended_guard_action": "Treat this methodology metric as diagnostic only; refine extraction before using it for routing thresholds.",
                "authority_boundary": ai_methodology_authority_boundary(),
            }
        )

    return {
        "schema_id": "ai_research_agent_methodology_metrics_v1",
        "taxonomy_source_path": AI_METHODOLOGY_TAXONOMY_PATH,
        "status": "partial" if calibrated_warnings else "measured",
        "calculation_window": calculation_window,
        "required_metric_ids": list(AI_METHODOLOGY_REQUIRED_METRICS),
        "metric_count": len(metric_records),
        "metrics": metric_records,
        "calibrated_acceptance_warnings": calibrated_warnings,
        "separation_guard": {
            "status": "pass",
            "kept_out_of_scientific_progress_metrics": True,
            "not_physics_proof": True,
        },
        "authority_boundary": ai_methodology_authority_boundary(),
    }


def collect_support_only_checker_metrics(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Count support-only checker reports as operational tooling evidence."""
    repo_root = Path(repo_root)
    status_counts: Counter[str] = Counter()
    report_files_scanned = 0
    reports_found = 0
    parse_errors = 0
    forbidden_overread_reports = 0
    physics_obstruction_reports = 0
    boundary_mismatch_reports = 0
    tooling_error_reports = 0

    for path in sorted(repo_root.glob(SUPPORT_ONLY_CHECKER_REPORT_GLOB)):
        report_files_scanned += 1
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            parse_errors += 1
            continue

        if report.get("checker_id") != SUPPORT_ONLY_CHECKER_ID:
            continue

        reports_found += 1
        status = str(report.get("status", "")).strip() or "unknown"
        status_counts[status] += 1

        if list_value(report.get("forbidden_overread_flags")):
            forbidden_overread_reports += 1
        if str(report.get("physics_obstruction", "")).strip():
            physics_obstruction_reports += 1

        boundary = str(report.get("boundary_statement", ""))
        if any(phrase not in boundary for phrase in SUPPORT_ONLY_BOUNDARY_REQUIRED_PHRASES):
            boundary_mismatch_reports += 1

        if bool_value(report.get("tooling_error")) is True:
            tooling_error_reports += 1

    return {
        "support_only_checker_report_files_scanned": report_files_scanned,
        "support_only_checker_report_parse_errors": parse_errors,
        "support_only_checker_reports_found": reports_found,
        "support_only_checker_status_counts": dict(sorted(status_counts.items())),
        "support_only_checker_forbidden_overread_reports": forbidden_overread_reports,
        "support_only_checker_physics_obstruction_reports": physics_obstruction_reports,
        "support_only_checker_boundary_mismatch_reports": boundary_mismatch_reports,
        "support_only_checker_tooling_error_reports": tooling_error_reports,
    }


def scientific_metric_key_violations(metrics: dict[str, Any]) -> list[str]:
    """Return scientific scoreboard keys that look operational-only."""
    violations: list[str] = []
    for key in metrics:
        normalized = key.lower()
        if any(token in normalized for token in OPERATIONAL_METRIC_KEY_TOKENS):
            violations.append(key)
    return violations


def cycle_step_bucket(record: dict[str, Any]) -> str:
    step = record.get("cycle_step", "").lower()
    role_id = record.get("role_id", "")
    if "candidate" in step or "constructor" in step or role_id == "candidate-constructor":
        return "construct"
    if "audit" in step or "smuggling" in step or role_id == "smuggling-auditor":
        return "audit"
    if "stress" in step or "refuter" in step or role_id == "refuter":
        return "stress"
    if "selector" in step or role_id == "theoretical-continuation-selector":
        return "selector"
    return ""


def complete_legacy_cycle_count(records: list[dict[str, Any]]) -> tuple[int, list[list[dict[str, Any]]]]:
    cycles: list[list[dict[str, Any]]] = []
    expected = [
        "candidate-constructor",
        "smuggling-auditor",
        "refuter",
        "theoretical-continuation-selector",
    ]
    index = 0
    while index <= len(records) - len(expected):
        window = records[index : index + len(expected)]
        if [record["role_id"] for record in window] == expected:
            cycles.append(window)
            index += len(expected)
            continue
        index += 1
    return len(cycles), cycles


def explicit_cycle_summary(records: list[dict[str, Any]]) -> tuple[int, int, set[str]]:
    families: dict[str, dict[str, Any]] = {}
    for record in records:
        family = record.get("cycle_family", "")
        if not family:
            continue
        entry = families.setdefault(family, {"steps": set(), "payload": 0})
        bucket = cycle_step_bucket(record)
        if bucket:
            entry["steps"].add(bucket)
        entry["payload"] += int(record.get("payload_count", 0))

    cycle_count = 0
    payload_total = 0
    complete_families: set[str] = set()
    for family, entry in families.items():
        steps = entry["steps"]
        if len(steps) >= 2:
            cycle_count += 1
            payload_total += int(entry["payload"])
        if {"construct", "audit", "stress", "selector"}.issubset(steps):
            complete_families.add(family)
    return cycle_count, payload_total, complete_families


def selector_has_constructive_consequence(
    record: dict[str, Any],
    next_record: dict[str, Any] | None,
) -> bool:
    selected = " ".join(
        [
            record.get("selected_next_packet_type", ""),
            record.get("selected_role_hint", ""),
            record.get("text", ""),
        ]
    ).lower()
    constructive_tokens = (
        "candidate-constructor",
        "candidate constructor",
        "refuter",
        "obstruction",
        "no-go",
        "no_go",
        "gate-chair",
        "gate chair",
        "human_gate",
        "freeze",
    )
    if any(token in selected for token in constructive_tokens):
        return True
    return bool(
        next_record
        and next_record.get("role_id") in {"candidate-constructor", "refuter", "gate-chair"}
    )


def warning_record(
    warning_id: str,
    metric_key: str,
    observed_value: Any,
    threshold: Any,
    evidence_paths: list[str],
    recommended_guard_action: str,
) -> dict[str, Any]:
    return {
        "warning_id": warning_id,
        "severity": "warning",
        "metric_key": metric_key,
        "observed_value": observed_value,
        "threshold": threshold,
        "evidence_paths": sorted(set(path for path in evidence_paths if path)),
        "recommended_guard_action": recommended_guard_action,
        "hard_gate": False,
        "physics_claim_authority": False,
    }


def collect_payload_density_metrics(
    records: list[dict[str, Any]],
    support_metrics: dict[str, Any],
    referenced_obstructions: int,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    if not records:
        return (
            {
                "physics_completions_read": 0,
                "total_payload_items": 0,
                "tasks_since_last_distance_to_gr_delta": 0,
                "tasks_since_last_burden_discharged": 0,
                "new_payload_items_per_physics_task": 0,
                "new_payload_items_per_cycle": 0,
                "selector_cycles_without_new_payload": 0,
            },
            {
                "same_burden_repetition_count": 0,
                "freeze_reviews_triggered_by_repetition": 0,
                "bridge_attempts_since_last_gate": 0,
                "obstructions_created": 0,
                "obstructions_created_missing_id": 0,
                "obstructions_reused": 0,
                "candidate_construct_audit_stress_selector_cycles": 0,
                "gate_ready_cycles_without_gate_verdict": 0,
                "support_only_tooling_reports": support_metrics.get(
                    "support_only_checker_reports_found",
                    0,
                ),
                "physics_promotion_authorized_true_count": 0,
                "physics_promotion_authorized_false_count": 0,
            },
            [],
        )

    total_payload = sum(int(record.get("payload_count", 0)) for record in records)

    since_delta = 0
    for record in records:
        if record.get("delta_changed") is True:
            since_delta = 0
        else:
            since_delta += 1

    since_burden = 0
    for record in records:
        if record.get("progress_status") == "burden_discharged":
            since_burden = 0
        else:
            since_burden += 1

    explicit_cycle_count, explicit_cycle_payload, complete_families = explicit_cycle_summary(records)
    legacy_cycle_count, legacy_cycles = complete_legacy_cycle_count(
        [record for record in records if not record.get("cycle_family")]
    )
    legacy_cycle_payload = sum(
        int(record.get("payload_count", 0))
        for cycle in legacy_cycles
        for record in cycle
    )
    cycle_count = explicit_cycle_count + legacy_cycle_count
    cycle_payload = explicit_cycle_payload + legacy_cycle_payload

    selector_without_payload = 0
    selector_without_payload_paths: list[str] = []
    for index, record in enumerate(records):
        if record.get("role_id") != "theoretical-continuation-selector":
            continue
        if int(record.get("payload_count", 0)) > 0:
            continue
        next_record = records[index + 1] if index + 1 < len(records) else None
        if not selector_has_constructive_consequence(record, next_record):
            selector_without_payload += 1
            selector_without_payload_paths.append(record.get("completion_path", ""))

    same_burden_max = 0
    same_burden_streak = 0
    current_burden_key = ("", "")
    same_burden_paths: list[str] = []
    current_streak_paths: list[str] = []
    for record in records:
        key = record.get("burden_key", ("", ""))
        has_progress = int(record.get("payload_count", 0)) > 0 or record.get("delta_changed") is True
        if not key or key == ("", ""):
            same_burden_streak = 0
            current_burden_key = ("", "")
            current_streak_paths = []
            continue
        if has_progress:
            same_burden_streak = 0
            current_burden_key = key
            current_streak_paths = []
            continue
        if key != current_burden_key:
            current_burden_key = key
            same_burden_streak = 1
            current_streak_paths = [record.get("completion_path", "")]
        else:
            same_burden_streak += 1
            current_streak_paths.append(record.get("completion_path", ""))
        if same_burden_streak > same_burden_max:
            same_burden_max = same_burden_streak
            same_burden_paths = list(current_streak_paths)

    freeze_reviews = sum(
        1
        for record in records
        if record.get("freeze_repeated_burden") or record.get("freeze_evaluation_required")
    )

    gate_indices = [index for index, record in enumerate(records) if record.get("role_id") == "gate-chair"]
    start_index = gate_indices[-1] + 1 if gate_indices else 0
    bridge_attempts = sum(
        1
        for record in records[start_index:]
        if (
            record.get("role_id") == "candidate-constructor"
            and record.get("candidate_result_type") == "constructed_candidate"
        )
        or record.get("bridge_attempt_present")
    )

    obstruction_ids = {
        record.get("obstruction_id")
        for record in records
        if record.get("obstruction_present") and record.get("obstruction_id")
    }
    missing_obstruction_paths = [
        record.get("completion_path", "")
        for record in records
        if record.get("obstruction_present") and not record.get("obstruction_id")
    ]

    complete_route_cycles = len(complete_families) + legacy_cycle_count
    latest_gate_index = gate_indices[-1] if gate_indices else -1
    post_gate_complete_cycles = 0
    if latest_gate_index >= 0:
        post_gate_records = records[latest_gate_index + 1 :]
        post_gate_complete_cycles = explicit_cycle_summary(post_gate_records)[2].__len__()
        post_gate_complete_cycles += complete_legacy_cycle_count(
            [record for record in post_gate_records if not record.get("cycle_family")]
        )[0]

    gate_ready_without_gate = 0
    gate_ready_paths: list[str] = []
    for index, record in enumerate(records):
        selected = record.get("selected_next_packet_type", "").lower()
        text = record.get("text", "").lower()
        gate_ready = (
            record.get("progress_status") == "candidate_stress_passed_pending_gate"
            or "human_gate" in selected
            or "gate chair" in selected
            or "gate chair" in text and "next" in text
        )
        if not gate_ready:
            continue
        verdict_seen = False
        for next_record in records[index + 1 :]:
            if next_record.get("role_id") == "gate-chair":
                verdict_seen = True
                break
            if next_record.get("role_id") == "candidate-constructor":
                break
        if not verdict_seen:
            gate_ready_without_gate += 1
            gate_ready_paths.append(record.get("completion_path", ""))

    missing_candidate_paths = [
        record.get("completion_path", "")
        for record in records
        if record.get("role_id") == "candidate-constructor"
        and not record.get("candidate_result_type")
    ]

    bridge_no_delta_records = [
        record
        for record in records
        if "bridge" in record.get("text", "").lower()
        and record.get("delta_changed") is False
        and int(record.get("payload_count", 0)) == 0
    ]

    promotion_true = sum(1 for record in records if record.get("physics_promotion_authorized"))
    promotion_false = sum(
        1
        for record in records
        if record.get("has_forbidden_conclusion_summary")
        and not record.get("physics_promotion_authorized")
    )

    payload_density_metrics = {
        "physics_completions_read": len(records),
        "total_payload_items": total_payload,
        "tasks_since_last_distance_to_gr_delta": since_delta,
        "tasks_since_last_burden_discharged": since_burden,
        "new_payload_items_per_physics_task": round(total_payload / len(records), 2),
        "new_payload_items_per_cycle": round(cycle_payload / cycle_count, 2) if cycle_count else 0,
        "selector_cycles_without_new_payload": selector_without_payload,
    }
    route_orbit_risk_metrics = {
        "same_burden_repetition_count": same_burden_max,
        "freeze_reviews_triggered_by_repetition": freeze_reviews,
        "bridge_attempts_since_last_gate": bridge_attempts,
        "obstructions_created": len(obstruction_ids),
        "obstructions_created_missing_id": len(missing_obstruction_paths),
        "obstructions_reused": referenced_obstructions,
        "candidate_construct_audit_stress_selector_cycles": complete_route_cycles,
        "gate_ready_cycles_without_gate_verdict": gate_ready_without_gate,
        "support_only_tooling_reports": support_metrics.get("support_only_checker_reports_found", 0),
        "physics_promotion_authorized_true_count": promotion_true,
        "physics_promotion_authorized_false_count": promotion_false,
    }

    warnings: list[dict[str, Any]] = []
    if same_burden_max > 4:
        warnings.append(
            warning_record(
                "same_burden_repetition",
                "same_burden_repetition_count",
                same_burden_max,
                4,
                same_burden_paths,
                "Require construction, obstruction, gate, freeze review, or a sharper target before another same-burden selector/control-only packet.",
            )
        )
    if selector_without_payload > 2:
        warnings.append(
            warning_record(
                "selector_without_payload_or_consequence",
                "selector_cycles_without_new_payload",
                selector_without_payload,
                2,
                selector_without_payload_paths,
                "Prefer Candidate Constructor, Refuter obstruction/no-go, Gate Chair, or freeze review over another selector-only packet.",
            )
        )
    if post_gate_complete_cycles > 0:
        warnings.append(
            warning_record(
                "post_gate_cycle_repeat",
                "candidate_construct_audit_stress_selector_cycles",
                post_gate_complete_cycles,
                0,
                [record.get("completion_path", "") for record in records[latest_gate_index + 1 :]],
                "Require a harder target, broader finite family, explicit bridge attempt, or freeze-review rationale.",
            )
        )
    if len(bridge_no_delta_records) > 2:
        warnings.append(
            warning_record(
                "claimed_bridge_no_delta",
                "tasks_since_last_distance_to_gr_delta",
                len(bridge_no_delta_records),
                2,
                [record.get("completion_path", "") for record in bridge_no_delta_records],
                "Require payload or narrow the claim language to control-only routing.",
            )
        )
    if missing_candidate_paths:
        warnings.append(
            warning_record(
                "candidate_missing_result",
                "candidate_constructor_result_missing_count",
                len(missing_candidate_paths),
                0,
                missing_candidate_paths,
                "Require a completion receipt repair or a future validator task to make the field mandatory.",
            )
        )
    if gate_ready_without_gate > 0:
        warnings.append(
            warning_record(
                "gate_ready_without_gate",
                "gate_ready_cycles_without_gate_verdict",
                gate_ready_without_gate,
                0,
                gate_ready_paths,
                "Route the next packet to Gate Chair, explain why Gate Chair is not yet lawful, or withdraw gate-ready wording.",
            )
        )
    if missing_obstruction_paths:
        warnings.append(
            warning_record(
                "obstruction_without_id",
                "obstructions_created_missing_id",
                len(missing_obstruction_paths),
                0,
                missing_obstruction_paths,
                "Repair future receipt templates; do not rewrite historical artifacts in this task.",
            )
        )

    support_overread_count = sum(
        int(support_metrics.get(key, 0))
        for key in (
            "support_only_checker_forbidden_overread_reports",
            "support_only_checker_physics_obstruction_reports",
            "support_only_checker_boundary_mismatch_reports",
        )
    )
    if support_overread_count:
        warnings.append(
            warning_record(
                "support_tooling_overread",
                "support_only_tooling_reports",
                support_overread_count,
                0,
                [],
                "Treat as tooling or fixture-quality issue unless a later physics packet lawfully interprets it.",
            )
        )

    return payload_density_metrics, route_orbit_risk_metrics, warnings


def build_report(
    repo_root: Path = REPO_ROOT,
    *,
    instrumentation: MetricsBuildInstrumentation | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    task_rows = read_csv_rows(repo_root, "RESEARCH_TASK_REGISTRY.csv")
    job_rows = read_csv_rows(repo_root, "AGENT_JOB_REGISTRY.csv")
    role_rows = read_csv_rows(repo_root, "AGENT_ROLE_REGISTRY.csv")
    claim_rows = read_csv_rows(repo_root, "CLAIM_BOUNDARY_REGISTRY.csv")

    roles = {
        role_key(row.get("role_id", ""), row.get("version", "")): row
        for row in role_rows
    }

    completion_records: list[dict[str, Any]] = []
    completion_status_counts: Counter[str] = Counter()
    physics_progress_counts: Counter[str] = Counter()
    candidate_result_counts: Counter[str] = Counter()
    physics_role_counts: Counter[str] = Counter()

    distance_true = 0
    distance_false = 0
    forbidden_summary_count = 0
    promotion_authorized_count = 0
    obstruction_records: list[dict[str, str]] = []
    freeze_review_count = 0
    human_gate_freeze_count = 0

    sorted_jobs = sorted(
        job_rows,
        key=lambda row: (row.get("created_at", ""), row.get("job_id", "")),
    )

    for row in sorted_jobs:
        completion_path = row.get("completion_path", "")
        completion = load_completion(repo_root, completion_path, instrumentation)
        if not completion:
            continue

        role = roles.get(role_key(row.get("role_id", ""), row.get("role_version", "")))
        is_physics = is_physics_role(role)
        role_id = row.get("role_id", "")
        if is_physics:
            physics_role_counts[role_id] += 1

        completion_status_counts[str(completion.get("validation_status", "")).strip() or "unknown"] += 1
        progress_status = status_from_progress(completion)
        if progress_status:
            physics_progress_counts[progress_status] += 1

        delta_changed = changed_from_delta(completion)
        if delta_changed is True:
            distance_true += 1
        elif delta_changed is False:
            distance_false += 1

        forbidden = completion.get("forbidden_conclusion_summary")
        if isinstance(forbidden, dict):
            forbidden_summary_count += 1
            if bool_value(forbidden.get("physics_promotion_authorized")) is True:
                promotion_authorized_count += 1

        candidate = completion.get("candidate_constructor_result")
        if isinstance(candidate, dict):
            result_type = str(candidate.get("result_type", "")).strip()
            if result_type:
                candidate_result_counts[result_type] += 1

        oid = obstruction_id(completion)
        if oid:
            obstruction_records.append(
                {
                    "obstruction_id": oid,
                    "completion_path": completion_path,
                    "completed_at": row.get("completed_at", ""),
                }
            )

        freeze = completion.get("freeze_criteria_status")
        if isinstance(freeze, dict):
            repeated = bool_value(freeze.get("repeated_burden")) is True
            required = bool_value(freeze.get("freeze_evaluation_required")) is True
            if repeated or required:
                freeze_review_count += 1
            if freeze_decision(completion) == "human_gate_required":
                human_gate_freeze_count += 1

        completion_records.append(
            completion_record(repo_root, row, completion, is_physics, instrumentation)
        )

    referenced_obstructions = 0
    for record in obstruction_records:
        oid = record["obstruction_id"]
        source_path = record["completion_path"]
        source_time = record["completed_at"]
        for later in completion_records:
            if later["completion_path"] == source_path:
                continue
            if source_time and later["completed_at"] and later["completed_at"] <= source_time:
                continue
            if oid and oid in completion_text(repo_root, later["completion_path"], instrumentation):
                referenced_obstructions += 1
                break

    physics_sequence = [
        row["role_id"]
        for row in completion_records
        if row["is_physics"] and row["role_id"]
    ]
    cycle_lengths: list[int] = []
    selector_without_construction = 0
    index = 0
    while index < len(physics_sequence):
        role_id = physics_sequence[index]
        if role_id == "candidate-constructor":
            length = 1
            if index + length < len(physics_sequence) and physics_sequence[index + length] == "smuggling-auditor":
                length += 1
            if index + length < len(physics_sequence) and physics_sequence[index + length] == "refuter":
                length += 1
            if length > 1:
                cycle_lengths.append(length)
            index += length
            continue
        if role_id == "theoretical-continuation-selector":
            next_role = physics_sequence[index + 1] if index + 1 < len(physics_sequence) else ""
            if next_role != "candidate-constructor":
                selector_without_construction += 1
        index += 1

    average_cycle = round(sum(cycle_lengths) / len(cycle_lengths), 2) if cycle_lengths else 0
    role_metrics = {key: 0 for key in ROLE_METRIC_KEYS.values()}
    for role_id, metric_key in ROLE_METRIC_KEYS.items():
        role_metrics[metric_key] = physics_role_counts.get(role_id, 0)

    input_counts = {
        "tasks_registered": len(task_rows),
        "jobs_registered": len(job_rows),
        "completions_read": len(completion_records),
        "physics_completions_read": sum(1 for row in completion_records if row["is_physics"]),
        "claim_boundary_rows": len(claim_rows),
        "active_claim_boundary_rows": sum(1 for row in claim_rows if row.get("status") == "active"),
    }
    claim_hygiene_metrics = {
        "tasks_with_forbidden_conclusion_summary": forbidden_summary_count,
        "physics_promotion_authorized_true": promotion_authorized_count,
        "physics_promotion_authorized_false": max(0, forbidden_summary_count - promotion_authorized_count),
        "claim_boundary_rows_active": sum(1 for row in claim_rows if row.get("status") == "active"),
    }
    agent_workflow_metrics = {
        **role_metrics,
        "average_tasks_per_construct_audit_stress_cycle": average_cycle,
        "construct_audit_stress_cycle_count": len(cycle_lengths),
        "selector_cycles_without_construction": selector_without_construction,
    }
    support_metrics = collect_support_only_checker_metrics(repo_root)
    operational_validation_metrics = {
        **input_counts,
        "completion_validation_status_counts": dict(sorted(completion_status_counts.items())),
        **claim_hygiene_metrics,
        **agent_workflow_metrics,
        **support_metrics,
    }
    scientific_progress_metrics = {
        "distance_to_gr_delta_true_count": distance_true,
        "distance_to_gr_delta_false_count": distance_false,
        "burden_discharged_count": physics_progress_counts.get("burden_discharged", 0),
        "constructed_candidate_count": (
            physics_progress_counts.get("candidate_constructed_pending_audit", 0)
            + candidate_result_counts.get("constructed_candidate", 0)
        ),
        "candidate_smuggling_audit_pass_count": physics_progress_counts.get(
            "candidate_audited_pending_stress",
            0,
        ),
        "candidate_refuter_stress_pass_count": physics_progress_counts.get(
            "candidate_stress_passed_pending_gate",
            0,
        ),
        "precise_obstruction_count": (
            physics_progress_counts.get("precise_obstruction_found", 0)
            + candidate_result_counts.get("precise_obstruction", 0)
        ),
        "minimal_countermodel_count": candidate_result_counts.get("minimal_countermodel", 0),
        "route_frozen_count": physics_progress_counts.get("route_frozen", 0),
        "human_gate_required_count": physics_progress_counts.get("human_gate_required", 0),
        "obstruction_records_created": len(obstruction_records),
        "obstruction_records_referenced_by_later_tasks": referenced_obstructions,
        "repeated_obstructions_triggering_freeze_review": freeze_review_count,
        "frozen_routes_reopened_by_human_gate": human_gate_freeze_count,
        "physics_progress_status_counts": dict(sorted(physics_progress_counts.items())),
    }
    physics_records = [row for row in completion_records if row["is_physics"]]
    (
        payload_density_metrics,
        route_orbit_risk_metrics,
        diagnostic_warnings,
    ) = collect_payload_density_metrics(
        physics_records,
        support_metrics,
        referenced_obstructions,
    )
    scientific_payload_density_report = scientific_payload_density.build_report(repo_root)
    physics_progress_integration_metrics = collect_physics_progress_integration_metrics(
        completion_records,
        scientific_payload_density_report,
    )
    candidate_lineage_metrics = collect_candidate_lineage_metrics(repo_root)
    durable_scientific_quality_metrics = (
        scientific_quality_metrics.build_repository_report(
            repo_root,
            completion_records=completion_records,
        )
    )
    ai_research_agent_methodology_metrics = collect_ai_research_agent_methodology_metrics(
        completion_records,
        task_rows,
        scientific_payload_density_report,
        payload_density_metrics,
        route_orbit_risk_metrics,
        diagnostic_warnings,
        candidate_lineage_metrics,
    )
    physics_payload_ratio_diagnostics = collect_physics_payload_ratio_diagnostics(
        repo_root,
        completion_records,
        task_rows,
        roles,
        scientific_payload_density_report,
        route_orbit_risk_metrics,
        diagnostic_warnings,
    )
    dual_budget_dashboard = collect_dual_budget_dashboard(completion_records)
    separation_violations = scientific_metric_key_violations(scientific_progress_metrics)
    metrics = {
        "operational_validation_metrics": operational_validation_metrics,
        "scientific_progress_metrics": scientific_progress_metrics,
        "payload_density_metrics": payload_density_metrics,
        "route_orbit_risk_metrics": route_orbit_risk_metrics,
        "candidate_lineage_metrics": candidate_lineage_metrics,
        "durable_scientific_quality_metrics": durable_scientific_quality_metrics,
        "physics_payload_ratio_diagnostics": physics_payload_ratio_diagnostics,
        "dual_budget_dashboard": dual_budget_dashboard,
        "physics_progress_integration_metrics": physics_progress_integration_metrics,
        "ai_research_agent_methodology_metrics": ai_research_agent_methodology_metrics,
        "diagnostic_warnings": diagnostic_warnings,
        "metric_separation_guard": {
            "status": "pass" if not separation_violations else "fail",
            "operational_metric_key_tokens": sorted(OPERATIONAL_METRIC_KEY_TOKENS),
            "scientific_key_violations": separation_violations,
            "rule": "Operational checker validation registry generated memory wiki receipt role-schema handoff-continuity payload-density route-orbit and diagnostic-warning metrics stay out of scientific_progress_metrics.",
        },
        "input_counts": input_counts,
        "claim_hygiene_metrics": claim_hygiene_metrics,
        "physics_progress_metrics": scientific_progress_metrics,
        "obstruction_reuse_metrics": {
            "obstruction_records_created": len(obstruction_records),
            "obstruction_records_referenced_by_later_tasks": referenced_obstructions,
            "repeated_obstructions_triggering_freeze_review": freeze_review_count,
            "frozen_routes_reopened_by_human_gate": human_gate_freeze_count,
        },
        "agent_workflow_metrics": agent_workflow_metrics,
    }

    return {
        "report_id": "research_control_metrics_separation",
        "as_of": max(
            [row.get("updated_at", "") for row in task_rows]
            + [row.get("completed_at", "") for row in job_rows]
            + [""]
        ),
        "source_basis": [
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
            "registries/AGENT_ROLE_REGISTRY.csv",
            "registries/CLAIM_BOUNDARY_REGISTRY.csv",
            "research_control/tasks/*/jobs/completions/*.yaml",
            AI_METHODOLOGY_TAXONOMY_PATH,
            PHYSICS_PAYLOAD_RATIO_POLICY_PATH,
            DUAL_BUDGET_POLICY_PATH,
            DUAL_BUDGET_DASHBOARD_SCHEMA_PATH,
            ORDINARY_ROUTE_GUARD_POLICY_PATH,
            CANDIDATE_LINEAGE_REGISTRY_PATH,
            scientific_quality_metrics.QUALITY_TAXONOMY_PATH,
            scientific_quality_metrics.CALIBRATION_POLICY_PATH,
            scientific_quality_metrics.ATTEMPT_LEDGER_PATH,
        ]
        + (
            [str(candidate_lineage_metrics["historical_seed_path"])]
            if candidate_lineage_metrics.get("historical_seed_path")
            else []
        ),
        "authority_boundary": {
            "metrics_are_operational": True,
            "scoreboards_are_separated": True,
            "ai_methodology_metrics_are_support_only": True,
            "durable_scientific_quality_metrics_are_advisory": True,
            "durable_scientific_quality_metrics_are_primary_quality_surface": True,
            "raw_volume_is_primary_scientific_quality": False,
            "physics_payload_ratio_diagnostics_are_support_only": True,
            "dual_budget_dashboard_is_support_only": True,
            "physics_claim_promotion_authorized": False,
            "metrics_report_not_physics_proof": True,
            "validation_status_is_not_physics_evidence": True,
        },
        "metrics": metrics,
        "limitations": [
            "Operational validation metrics are workflow diagnostics and not physics evidence.",
            "Support-only checker report counts are operational tooling diagnostics; checker syntax or boundary failures are not physics failures.",
            "Scientific progress metrics are counts of tracked science-claim fields and must still cite source artifacts before any claim is reused.",
            "Obstruction reuse is measured by completion-level obstruction IDs and later completion references.",
            "AI research-agent methodology metrics are support-only diagnostics and cannot be used as proof, source-law adoption, benchmark promotion, or Gate Chair verdicts.",
            "Candidate-lineage metrics are keyed by immutable candidate IDs and preserve explicit historical absences; they remain support-only project-control evidence and do not adopt or reject a candidate.",
            "Durable scientific-quality diagnostics use explicit eligible sets and immutable identities, leave absent denominators not_measured, and never aggregate scientific truth into one score.",
            "Raw packet, artifact, task, and payload counts remain operational context only; they are not the primary scientific-quality surface.",
            "Physics-payload ratio diagnostics are AI-system diagnostics only; they do not rank physics truth.",
            "Dual-budget dashboard values are operational accounting; system success, missing-resource markers, and lane counts are not physics evidence or Distance-to-GR progress.",
            "Validator failure history is not a durable event log, so this report does not infer blocked violation counts from past terminal output.",
        ],
    }


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def render_table(mapping: dict[str, Any]) -> list[str]:
    lines = ["| Metric | Value |", "| --- | --- |"]
    for key, value in mapping.items():
        rendered = json.dumps(value, sort_keys=True) if isinstance(value, dict) else str(value)
        lines.append(f"| `{key}` | `{rendered}` |")
    return lines


def render_warning_table(warnings: list[dict[str, Any]]) -> list[str]:
    if not warnings:
        return ["No diagnostic warnings were emitted."]
    lines = [
        "| Warning | Metric | Observed | Threshold | Hard Gate | Physics Authority |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for warning in warnings:
        lines.append(
            "| `{warning_id}` | `{metric_key}` | `{observed}` | `{threshold}` | `{hard_gate}` | `{authority}` |".format(
                warning_id=warning.get("warning_id", ""),
                metric_key=warning.get("metric_key") or warning.get("metric_id", ""),
                observed=warning.get("observed_value", ""),
                threshold=warning.get("threshold", ""),
                hard_gate=warning.get("hard_gate", False),
                authority=warning.get("physics_claim_authority", False),
            )
        )
    return lines


def render_durable_quality_table(report: dict[str, Any]) -> list[str]:
    lines = [
        "| Metric | Family | Status | Numerator | Denominator | Value | Warning count |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    records = report.get("metrics", {})
    for metric_id in scientific_quality_metrics.REQUIRED_METRIC_IDS:
        record = records.get(metric_id, {})
        numerator = record.get("numerator", {})
        denominator = record.get("denominator", {})
        value = record.get("value")
        lines.append(
            "| `{metric_id}` | {family} | {status} | {numerator} | "
            "{denominator} | {value} | {warnings} |".format(
                metric_id=markdown_cell(metric_id),
                family=markdown_cell(record.get("family", "")),
                status=markdown_cell(record.get("status", "")),
                numerator=markdown_cell(numerator.get("value")),
                denominator=markdown_cell(denominator.get("value")),
                value=markdown_cell(value),
                warnings=markdown_cell(len(record.get("warnings", []))),
            )
        )
    return lines


def markdown_cell(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True) if isinstance(value, dict) else str(value)
    return rendered.replace("|", "\\|")


def render_ai_methodology_table(report: dict[str, Any]) -> list[str]:
    records = report.get("metrics", {})
    if not isinstance(records, dict):
        return ["AI methodology metric records were not available."]
    lines = [
        "| Metric | Family | Status | Value | Interpretation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for metric_id in report.get("required_metric_ids", AI_METHODOLOGY_REQUIRED_METRICS):
        record = records.get(metric_id)
        if not isinstance(record, dict):
            lines.append(f"| `{metric_id}` | missing | not_measured |  | Metric record missing. |")
            continue
        lines.append(
            "| `{metric_id}` | {family} | `{status}` | `{value}` | {interpretation} |".format(
                metric_id=metric_id,
                family=markdown_cell(record.get("family", "")),
                status=record.get("status", ""),
                value=markdown_cell(record.get("value", "")),
                interpretation=markdown_cell(record.get("diagnostic_interpretation", "")),
            )
        )
    return lines


def render_ai_methodology_warnings(report: dict[str, Any]) -> list[str]:
    warnings = report.get("calibrated_acceptance_warnings", [])
    if not isinstance(warnings, list) or not warnings:
        return ["No AI methodology acceptance warnings were emitted."]
    lines = [
        "| Warning | Metric | Status | Hard Gate | Physics Authority | Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for warning in warnings:
        lines.append(
            "| `{warning_id}` | `{metric_id}` | `{status}` | `{hard_gate}` | `{authority}` | {reason} |".format(
                warning_id=warning.get("warning_id", ""),
                metric_id=warning.get("metric_id", ""),
                status=warning.get("status", ""),
                hard_gate=warning.get("hard_gate", False),
                authority=warning.get("physics_claim_authority", False),
                reason=markdown_cell(warning.get("reason", "")),
            )
        )
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    ai_methodology = metrics["ai_research_agent_methodology_metrics"]
    lines: list[str] = [
        "<!-- authority: control -->",
        "",
        "# Research-Control Metrics Separation Report",
        "",
        "## Analysis",
        "",
        "This report is generated from tracked research-control registries and completion YAML files. It evaluates the AI research-agent system as an operational system. It does not promote a physics claim, adopt a source law, construct `M_src`, or treat validator success as physics evidence.",
        "",
        "## Source Basis",
        "",
    ]
    lines.extend(f"- `{path}`" for path in report["source_basis"])
    lines.extend(
        [
            "",
            "## Operational Validation Metrics",
            "",
            *render_table(metrics["operational_validation_metrics"]),
            "",
            "## Scientific Progress Metrics",
            "",
            *render_table(metrics["scientific_progress_metrics"]),
            "",
            "## Durable Scientific-Quality Diagnostics",
            "",
            "This is the primary scientific-quality diagnostic surface. Every measured value has an explicit eligible-set denominator and immutable identities. Unknown populations remain `not_measured`; the eight indicators are not combined into a scientific-truth score.",
            "",
            *render_durable_quality_table(
                metrics["durable_scientific_quality_metrics"]
            ),
            "",
            "### Durable-Quality Calibration Warnings",
            "",
            *render_warning_table(
                metrics["durable_scientific_quality_metrics"]["warnings"]
            ),
            "",
            "## Payload-Density Metrics",
            "",
            "Raw volume is operational context only and is not the primary scientific-quality surface.",
            "",
            *render_table(metrics["payload_density_metrics"]),
            "",
            "## Route-Orbit Risk Metrics",
            "",
            *render_table(metrics["route_orbit_risk_metrics"]),
            "",
            "## Candidate Lineage Metrics",
            "",
            "These lifecycle metrics are keyed by immutable candidate IDs and preserve explicit historical absences. They are project-control diagnostics only and do not adopt, reject, or promote a candidate.",
            "",
            *render_table(metrics["candidate_lineage_metrics"]["metrics"]),
            "",
            "## Physics-Payload Ratio Diagnostics",
            "",
            "These metrics are AI-system diagnostics only. They do not rank physics truth, authorize proof, promote a benchmark, create a Gate Chair verdict, or complete a derivation.",
            "",
            *render_table(metrics["physics_payload_ratio_diagnostics"]["metrics"]),
            "",
            "## Dual-Budget Dashboard",
            "",
            "This dashboard separates physics and project-system task credit, elapsed effort, compute, durable outputs, and acceptance accounting. It is support-only and system success never creates physics or Distance-to-GR credit.",
            "",
            *render_table(
                {
                    "physics": metrics["dual_budget_dashboard"]["lanes"]["physics"],
                    "project_system": metrics["dual_budget_dashboard"]["lanes"]["project_system"],
                    "integrity": metrics["dual_budget_dashboard"]["integrity"],
                    "category_counts": metrics["dual_budget_dashboard"]["category_counts"],
                }
            ),
            "",
            "## Physics-Progress Integration Metrics",
            "",
            "The packet, artifact, and payload counts in this section are retained only as raw operational context. They do not measure scientific quality or create physics progress.",
            "",
            *render_table(metrics["physics_progress_integration_metrics"]),
            "",
            "## AI Research-Agent Methodology Metrics",
            "",
            "These diagnostics are support-only AI-system methodology metrics. They are separated from scientific progress metrics and do not authorize physics proof, source-law adoption, benchmark promotion, Gate Chair verdicts, or completed-derivation claims.",
            "",
            *render_ai_methodology_table(ai_methodology),
            "",
            "## AI Methodology Acceptance Warnings",
            "",
            *render_ai_methodology_warnings(ai_methodology),
            "",
            "## Diagnostic Warnings",
            "",
            *render_warning_table(metrics["diagnostic_warnings"]),
            "",
            "## Separation Guard",
            "",
            *render_table(metrics["metric_separation_guard"]),
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "This report provides separated operational and scientific scoreboards for future evaluation. The metrics show workflow health separately from tracked science-result fields. They do not change the authority of any scientific artifact.",
            "",
            "## References",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *AEther recommendations implementation plan* [Local implementation plan].",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *Agent job registry* [Project-control registry].",
            "",
            "The AEther-Flow Research Project. (2026, June 21). *Claim boundary registry* [Project-control registry].",
            "",
        ]
    )
    return "\n".join(lines)


def build_metrics_snapshot(repo_root: Path = REPO_ROOT) -> MetricsSnapshot:
    """Build one report and freeze its canonical JSON and Markdown outputs."""

    instrumentation = MetricsBuildInstrumentation()
    report = build_report(repo_root, instrumentation=instrumentation)
    return MetricsSnapshot(
        report_json=render_json(report),
        report_markdown=render_markdown(report),
        completion_files_read=instrumentation.completion_files_read,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument("--output", help="Write output to a repository-relative path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    snapshot = build_metrics_snapshot(REPO_ROOT)
    if args.format == "markdown":
        output = snapshot.report_markdown
    else:
        output = snapshot.report_json

    if args.output:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
