#!/usr/bin/env python3
"""Extract v15 route signatures and run an advisory route-orbit pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from extract_route_history import (  # noqa: E402
    as_bool,
    build_route_history,
    compact_text,
    load_yaml_record,
    normalize_compact,
)
from validate_route_orbits import validate_route_history  # noqa: E402


SIGNATURE_SCHEMA_ID = "route_signature_schema_v1"
REPORT_SCHEMA_ID = "route_signature_pilot_report_v1"

RECENT_MATTER_COUPLING_TASK_IDS = [
    "RT-20260701-001",
    "RT-20260701-002",
    "RT-20260701-007",
    "RT-20260701-008",
    "RT-20260701-009",
    "RT-20260701-010",
    "RT-20260701-015",
    "RT-20260701-016",
    "RT-20260701-017",
    "RT-20260701-018",
    "RT-20260701-019",
    "RT-20260701-020",
    "RT-20260701-021",
    "RT-20260701-022",
    "RT-20260701-023",
    "RT-20260701-024",
    "RT-20260701-025",
    "RT-20260701-026",
    "RT-20260701-027",
    "RT-20260701-028",
    "RT-20260701-029",
    "RT-20260701-030",
    "RT-20260701-031",
]

COMPARISON_FIELDS = [
    "target_derivation_milestone",
    "milestone_burden",
    "object_or_claim_name",
    "route_family",
    "role_family",
    "mathematical_payload_class",
    "distance_to_gr_delta.effect",
    "source_extension_classification",
    "obstruction_id",
    "freeze_criteria_status.decision",
    "next_route_selected",
]

REQUIRED_V15_FIELDS = [
    "target_derivation_milestone",
    "milestone_burden",
    "object_or_claim_name",
    "route_family",
    "role_family",
    "mathematical_payload_class",
    "distance_to_gr_delta",
    "source_extension_classification",
    "obstruction_id",
    "freeze_criteria_status",
    "next_route_selected",
]

NEW_MATH_CLASSES = {
    "new_definition",
    "new_theorem_statement",
    "proved_theorem",
    "conditional_theorem",
    "proof_attempt",
    "countermodel",
    "finite_witness",
    "construction",
    "obstruction",
    "source_extension_candidate",
    "source_extension_audit_result",
    "source_extension_refuter_result",
    "scoped_evidence_status_review",
}

PROCESS_REFRESH_CLASSES = {
    "route_selector_only",
    "validator_tooling_only",
    "metrics_only",
    "documentation_only",
    "registry_only",
    "handoff_only",
    "boundary_synchronization_only",
    "unknown_process",
}


def nested_get(data: dict[str, Any], path: str, default: Any = "") -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def normalize_route(value: Any, default: str = "unknown") -> str:
    return normalize_compact(value, default=default)


def signature_value(signature: dict[str, Any], field: str) -> Any:
    if "." not in field:
        return signature.get(field, "")
    return nested_get(signature, field)


def signature_key(signature: dict[str, Any]) -> str:
    return "|".join(compact_text(signature_value(signature, field)) for field in COMPARISON_FIELDS)


def signature_hash(signature: dict[str, Any]) -> str:
    return hashlib.sha256(signature_key(signature).encode("utf-8")).hexdigest()


def load_completion(repo_root: Path, completion_path: str) -> tuple[dict[str, Any], str]:
    if not completion_path:
        return {}, "missing:completion_path"
    path = repo_root / completion_path
    return load_yaml_record(path)


def infer_route_family(v14_signature: dict[str, Any]) -> str:
    role_id = compact_text(v14_signature.get("role_id", "")).lower()
    source_category = compact_text(v14_signature.get("source_extension_category", "")).lower()
    selected_route = compact_text(v14_signature.get("selected_route", "")).lower()
    task_type = compact_text(v14_signature.get("task_type", "")).lower()
    text = f"{role_id} {source_category} {selected_route} {task_type}"

    if "boundary" in text or "sync" in text or "synchronization" in text:
        return "boundary_synchronization"
    if "selector" in role_id or "selector" in task_type:
        return "selector"
    if role_id == "gate-chair" or "human_gate" in source_category or "gate_chair" in text:
        return "source_extension_gate"
    if "smuggling" in text or "audit" in text:
        return "source_extension_audit"
    if "refuter" in role_id or "stress" in text:
        return "source_extension_stress"
    if "countermodel" in text:
        return "countermodel"
    if "obstruction" in text:
        return "obstruction"
    if "theorem" in text:
        return "theorem"
    if "validator" in text:
        return "validator"
    if "metrics" in text:
        return "metrics_control"
    if role_id in {"project-control-maintainer", "process-integrity-auditor"}:
        return "project_control"
    if "candidate" in text or "formalizer" in role_id or "ontology" in text:
        return "source_extension_candidate"
    return "unknown"


def infer_source_extension_classification(v14_signature: dict[str, Any], route_family: str) -> str:
    if route_family == "boundary_synchronization":
        return "source_extension_boundary_sync"
    if route_family == "obstruction":
        return "source_extension_obstruction"
    category = compact_text(v14_signature.get("source_extension_category", ""))
    allowed = {
        "none",
        "source_extension_candidate",
        "source_extension_smuggling_audit",
        "source_extension_refuter_stress",
        "source_extension_human_gate",
        "source_extension_adopted_or_rejected",
    }
    if category in allowed:
        return category
    return "none"


def infer_mathematical_payload_class(
    v14_signature: dict[str, Any],
    route_family: str,
    source_extension_classification: str,
) -> str:
    role_id = compact_text(v14_signature.get("role_id", "")).lower()
    task_type = compact_text(v14_signature.get("task_type", "")).lower()
    payload_type = compact_text(v14_signature.get("payload_type", "")).lower()
    text = f"{role_id} {task_type} {payload_type}"

    if route_family == "selector":
        return "route_selector_only"
    if route_family == "boundary_synchronization":
        return "boundary_synchronization_only"
    if route_family == "validator":
        return "validator_tooling_only"
    if route_family == "metrics_control":
        return "metrics_only"
    if route_family == "project_control" and not as_bool(v14_signature.get("new_mathematical_payload_exists", False)):
        return "registry_only"
    if source_extension_classification == "source_extension_human_gate":
        return "scoped_evidence_status_review"
    if source_extension_classification == "source_extension_smuggling_audit":
        return "source_extension_audit_result"
    if source_extension_classification == "source_extension_refuter_stress":
        return "source_extension_refuter_result"
    if route_family == "countermodel":
        return "countermodel"
    if route_family == "obstruction" or compact_text(v14_signature.get("obstruction_label", "")) != "none":
        return "obstruction"
    if "finite" in text and "witness" in text:
        return "finite_witness"
    if "construct" in text or "candidate-constructor" in text:
        return "construction"
    if "proof" in text:
        return "proof_attempt"
    if "theorem" in text:
        return "conditional_theorem"
    if "definition" in text or "target" in text or "formalizer" in text:
        return "new_definition"
    if source_extension_classification == "source_extension_candidate":
        return "source_extension_candidate"
    if as_bool(v14_signature.get("new_mathematical_payload_exists", False)):
        return "source_extension_candidate"
    return "unknown_process"


def read_distance_to_gr_delta(completion: dict[str, Any]) -> dict[str, Any]:
    delta = completion.get("distance_to_gr_delta")
    if not isinstance(delta, dict):
        return {
            "effect": "no_distance_delta",
            "changed": False,
            "burden_id": "",
            "milestone": "",
        }
    return {
        "effect": compact_text(delta.get("effect", "")) or "no_distance_delta",
        "changed": as_bool(delta.get("changed", False)),
        "burden_id": compact_text(delta.get("burden_id", "")),
        "milestone": compact_text(delta.get("milestone", "")),
    }


def read_freeze_criteria_status(completion: dict[str, Any], v14_signature: dict[str, Any]) -> dict[str, Any]:
    freeze = completion.get("freeze_criteria_status")
    if isinstance(freeze, dict):
        evaluated = True
        triggered = as_bool(
            freeze.get("triggered", freeze.get("freeze_triggered", freeze.get("hard_freeze_triggered", False)))
        )
        decision = compact_text(
            freeze.get(
                "decision",
                freeze.get("freeze_decision", "freeze_candidate" if triggered else "evaluated_no_freeze"),
            )
        )
        return {
            "evaluated": evaluated,
            "triggered": triggered,
            "decision": decision or "unknown",
            "freeze_scope": compact_text(
                freeze.get("freeze_scope", freeze.get("active_freeze_label", freeze.get("candidate_freeze_label", "")))
            )
            or "none",
        }

    evaluated = as_bool(v14_signature.get("freeze_criteria_evaluated", False))
    candidate = compact_text(v14_signature.get("freeze_candidate", "none")) or "none"
    candidate_known = candidate not in {"none", "false", "unknown"}
    return {
        "evaluated": evaluated,
        "triggered": False,
        "decision": "freeze_candidate" if candidate_known else ("evaluated_no_freeze" if evaluated else "not_applicable"),
        "freeze_scope": candidate if candidate_known else "none",
    }


def infer_next_route(completion: dict[str, Any], v14_signature: dict[str, Any]) -> str:
    next_text = compact_text(completion.get("next_recommendation", ""))
    if not next_text:
        next_text = compact_text(nested_get(completion, "distance_to_gr_delta.downstream_unlocked.0"))
    if not next_text:
        next_text = compact_text(v14_signature.get("selected_route", ""))
    return normalize_route(next_text)


def classify_signature_kind(signature: dict[str, Any]) -> tuple[bool, bool]:
    payload_class = compact_text(signature["mathematical_payload_class"])
    distance_delta = signature["distance_to_gr_delta"]
    freeze_status = signature["freeze_criteria_status"]
    source_extension = compact_text(signature["source_extension_classification"])
    obstruction_id = compact_text(signature["obstruction_id"])

    source_extension_payload = source_extension in {
        "source_extension_candidate",
        "source_extension_smuggling_audit",
        "source_extension_refuter_stress",
        "source_extension_human_gate",
        "source_extension_obstruction",
    }
    new_math = (
        payload_class in NEW_MATH_CLASSES
        or as_bool(distance_delta.get("changed", False))
        or obstruction_id != "none"
        or as_bool(freeze_status.get("evaluated", False))
        or source_extension_payload
    )
    process_refresh = (
        payload_class in PROCESS_REFRESH_CLASSES
        and distance_delta.get("effect") == "no_distance_delta"
        and not as_bool(distance_delta.get("changed", False))
        and source_extension == "none"
        and obstruction_id == "none"
        and not as_bool(freeze_status.get("evaluated", False))
        and not as_bool(freeze_status.get("triggered", False))
    )
    return new_math, process_refresh


def project_v15_signature(v14_signature: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    completion, completion_error = load_completion(repo_root, compact_text(v14_signature.get("source_completion_path", "")))
    route_family = infer_route_family(v14_signature)
    source_extension = infer_source_extension_classification(v14_signature, route_family)
    payload_class = infer_mathematical_payload_class(v14_signature, route_family, source_extension)
    distance_delta = read_distance_to_gr_delta(completion)
    freeze_status = read_freeze_criteria_status(completion, v14_signature)
    signature = {
        "signature_schema_id": SIGNATURE_SCHEMA_ID,
        "source_signature_schema_id": v14_signature.get("signature_schema_id", ""),
        "source_signature_hash": v14_signature.get("signature_hash", ""),
        "source_task_id": v14_signature.get("source_task_id", "unknown"),
        "source_job_id": v14_signature.get("source_job_id", "unknown"),
        "source_completion_path": v14_signature.get("source_completion_path", ""),
        "target_derivation_milestone": v14_signature.get("target_derivation_milestone", "none"),
        "milestone_burden": v14_signature.get("milestone_burden", "none"),
        "object_or_claim_name": v14_signature.get("object_name", "none"),
        "route_family": route_family,
        "role_family": v14_signature.get("role_id", "unknown"),
        "mathematical_payload_class": payload_class,
        "distance_to_gr_delta": distance_delta,
        "source_extension_classification": source_extension,
        "obstruction_id": v14_signature.get("obstruction_label", "none") or "none",
        "freeze_criteria_status": freeze_status,
        "next_route_selected": infer_next_route(completion, v14_signature),
        "source_created_at": v14_signature.get("source_created_at", ""),
        "source_evidence": {
            "projection_source": [
                "scripts/research_control/extract_route_history.py",
                "research_control/design/route_signature_schema_v1.md",
            ],
            "v14_source_evidence": sorted(v14_signature.get("source_evidence", {}).keys()),
        },
    }
    if completion_error:
        signature["source_evidence"]["completion_warning"] = [completion_error]
    new_math, process_refresh = classify_signature_kind(signature)
    signature["new_mathematics_signature"] = new_math
    signature["process_refresh_signature"] = process_refresh
    signature["route_signature_key"] = signature_key(signature)
    signature["route_signature_hash"] = signature_hash(signature)
    return signature


def burden_cycle_key(signature: dict[str, Any]) -> tuple[str, str, str]:
    return (
        compact_text(signature["target_derivation_milestone"]) or "none",
        compact_text(signature["milestone_burden"]) or "none",
        compact_text(signature["object_or_claim_name"]) or "none",
    )


def summarize_route_orbits(signatures: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for signature in signatures:
        key = burden_cycle_key(signature)
        if key[0] == "none" or key[1] == "none":
            continue
        groups.setdefault(key, []).append(signature)

    repeated_cycles: list[dict[str, Any]] = []
    warning_cycles: list[dict[str, Any]] = []
    for key, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        no_new_payload = [member for member in members if not member.get("new_mathematics_signature", False)]
        process_refresh = [member for member in members if member.get("process_refresh_signature", False)]
        boundary_sync = [
            member for member in members if member.get("route_family") == "boundary_synchronization"
        ]
        cycle = {
            "cycle_key": "|".join(key),
            "target_derivation_milestone": key[0],
            "milestone_burden": key[1],
            "object_or_claim_name": key[2],
            "task_ids": [member["source_task_id"] for member in members],
            "signature_count": len(members),
            "new_mathematics_signature_count": len(members) - len(no_new_payload),
            "no_new_mathematical_payload_task_ids": [member["source_task_id"] for member in no_new_payload],
            "process_refresh_task_ids": [member["source_task_id"] for member in process_refresh],
            "boundary_synchronization_task_ids": [member["source_task_id"] for member in boundary_sync],
            "route_families": sorted({member["route_family"] for member in members}),
        }
        cycle["suggested_consequence"] = (
            "emit_advisory_route_orbit_warning_and_route_p10_t03_freeze_threshold_review"
            if len(process_refresh) >= 2 and not boundary_sync
            else "continue_without_freeze_from_pilot_record_cycle_for_p10_t03_policy"
        )
        repeated_cycles.append(cycle)
        if len(process_refresh) >= 2 and not boundary_sync:
            warning_cycles.append(cycle)

    no_new_math_tasks = [
        {
            "task_id": signature["source_task_id"],
            "object_or_claim_name": signature["object_or_claim_name"],
            "route_family": signature["route_family"],
            "mathematical_payload_class": signature["mathematical_payload_class"],
            "process_refresh_signature": signature["process_refresh_signature"],
            "suggested_consequence": "retain_as_control_evidence_not_new_mathematical_payload",
        }
        for signature in signatures
        if not signature.get("new_mathematics_signature", False)
    ]
    warning_should_emit = bool(warning_cycles)
    return {
        "repeated_burden_cycle_count": len(repeated_cycles),
        "repeated_no_new_payload_cycle_count": len(warning_cycles),
        "repeated_burden_cycles": repeated_cycles,
        "no_new_mathematical_payload_tasks": no_new_math_tasks,
        "route_orbit_warning_should_emit": warning_should_emit,
        "suggested_freeze_or_continuation_consequence": (
            "emit_advisory_route_orbit_warning_and_route_p10_t03_freeze_threshold_review"
            if warning_should_emit
            else "no_freeze_from_pilot_continue_to_p10_t03_freeze_threshold_policy"
        ),
    }


def task_ids_for_sample(sample: str, explicit_task_ids: list[str]) -> list[str]:
    if explicit_task_ids:
        return explicit_task_ids
    if sample == "recent-matter-coupling":
        return RECENT_MATTER_COUPLING_TASK_IDS
    return []


def build_report(
    repo_root: Path = REPO_ROOT,
    task_ids: list[str] | None = None,
    sample: str = "recent-matter-coupling",
) -> dict[str, Any]:
    selected_task_ids = task_ids_for_sample(sample, list(task_ids or []))
    route_history = build_route_history(repo_root, task_ids=selected_task_ids)
    legacy_validation = validate_route_history(route_history)
    signatures = [project_v15_signature(signature, repo_root) for signature in route_history["signatures"]]
    analysis = summarize_route_orbits(signatures)
    extraction_errors = list(route_history.get("extraction_errors", []))
    status = "PASS" if not extraction_errors else "FAIL"
    return {
        "schema_id": REPORT_SCHEMA_ID,
        "signature_schema_id": SIGNATURE_SCHEMA_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "sample": sample,
        "source_route_history_schema_id": route_history.get("schema_id", ""),
        "source_signature_schema_id": route_history.get("signature_schema_id", ""),
        "task_ids": selected_task_ids,
        "task_count": route_history.get("task_count", 0),
        "route_signature_count": len(signatures),
        "required_v15_fields": REQUIRED_V15_FIELDS,
        "comparison_fields": COMPARISON_FIELDS,
        "repeated_burden_cycle_count": analysis["repeated_burden_cycle_count"],
        "repeated_no_new_payload_cycle_count": analysis["repeated_no_new_payload_cycle_count"],
        "repeated_burden_cycles": analysis["repeated_burden_cycles"],
        "no_new_mathematical_payload_tasks": analysis["no_new_mathematical_payload_tasks"],
        "route_orbit_warning_should_emit": analysis["route_orbit_warning_should_emit"],
        "suggested_freeze_or_continuation_consequence": analysis[
            "suggested_freeze_or_continuation_consequence"
        ],
        "pilot_blocks_research": False,
        "advisory_only": True,
        "legacy_route_orbit_validation": {
            "status": legacy_validation["status"],
            "hard_failure_count": legacy_validation["hard_failure_count"],
            "warning_count": legacy_validation["warning_count"],
        },
        "route_signatures": signatures,
        "extraction_errors": extraction_errors,
        "status": status,
        "claim_boundary": {
            "operational_diagnostic_only": True,
            "route_freeze_authorized": False,
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--sample", choices=["recent-matter-coupling"], default="recent-matter-coupling")
    parser.add_argument("--task-id", action="append", default=[], help="Restrict extraction to a task ID; repeatable.")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    repo_root = args.repo_root.resolve()
    report = build_report(repo_root=repo_root, task_ids=args.task_id, sample=args.sample)
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output is not None:
        output_path = args.output if args.output.is_absolute() else repo_root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    if args.json or args.output is None:
        print(payload, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
