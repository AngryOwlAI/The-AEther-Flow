#!/usr/bin/env python3
"""Extract route signatures from tracked research-control task records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_strict_yaml  # noqa: E402


SIGNATURE_SCHEMA_ID = "route_signature_definition_v1"
EXTRACTOR_SCHEMA_ID = "route_history_extractor_v1"

SIGNATURE_FIELDS = [
    "signature_schema_id",
    "signature_id",
    "source_task_id",
    "source_job_id",
    "source_completion_path",
    "implementation_plan_id",
    "plan_task_id",
    "target_derivation_milestone",
    "milestone_burden",
    "object_family",
    "object_name",
    "task_type",
    "role_id",
    "execution_role_ref",
    "source_extension_category",
    "selected_route",
    "missing_primitive",
    "payload_type",
    "obstruction_label",
    "freeze_candidate",
    "boundary_synchronization_state",
    "gate_chair_state",
    "previous_task_ids",
    "new_mathematical_payload_exists",
    "exact_repair_attempted",
    "freeze_criteria_evaluated",
    "new_source_evidence_exists",
    "signature_hash",
]

COMPARISON_FIELDS = [
    "implementation_plan_id",
    "plan_task_id",
    "target_derivation_milestone",
    "milestone_burden",
    "object_family",
    "object_name",
    "task_type",
    "role_id",
    "source_extension_category",
    "selected_route",
    "missing_primitive",
    "payload_type",
    "obstruction_label",
    "freeze_candidate",
    "boundary_synchronization_state",
    "gate_chair_state",
    "new_mathematical_payload_exists",
    "exact_repair_attempted",
    "freeze_criteria_evaluated",
    "new_source_evidence_exists",
]

RECENT_MATTER_RR_E_SAMPLE_TASK_IDS = [
    "RT-20260701-001",
    "RT-20260701-002",
    "RT-20260701-007",
    "RT-20260701-008",
    "RT-20260701-009",
    "RT-20260701-010",
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

KNOWN_OBJECT_PATTERNS = [
    "SourceMatterSemanticsAdoptionReadinessLaw_v1",
    "PositiveSourceMatterSemanticsTarget_v1",
    "PositiveMSProfile_v1",
    "RR_ETransportCompletenessOrInvarianceLaw_v1",
    "RR_ETheoremTarget_v1",
    "RR_E_underdetermination_obstruction",
    "RR_ESeparationObstructionWitness_v1",
    "route_signature_definition_v1",
    "frontier_theorem_inventory",
]


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_lower(value: Any, default: str = "unknown") -> str:
    text = compact_text(value)
    return text.lower() if text else default


def normalize_compact(value: Any, default: str = "unknown") -> str:
    text = compact_text(value)
    if not text:
        return default
    text = text.lower()
    text = re.sub(r"[^a-z0-9_./@:+()^-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or default


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1"}


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in ("", None):
        return []
    return [value]


def text_blob(*values: Any) -> str:
    chunks: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                chunks.append(str(key))
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif value not in ("", None):
            chunks.append(str(value))

    for value in values:
        visit(value)
    return " ".join(chunks)


def nested_get(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return ""
        current = current[part]
    return current


def first_nonempty(*values: Any) -> Any:
    for value in values:
        if isinstance(value, list) and value:
            return value
        if compact_text(value):
            return value
    return ""


def load_yaml_record(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, f"missing:{path}"
    try:
        return load_strict_yaml(path), ""
    except StrictYamlError as exc:
        return {}, f"{repo_relative(path, REPO_ROOT)}:{exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key, "")}


def choose_with_source(
    evidence: dict[str, list[str]],
    field: str,
    candidates: list[tuple[Any, str]],
    default: Any,
) -> Any:
    for value, source in candidates:
        if isinstance(value, list):
            if value:
                evidence.setdefault(field, []).append(source)
                return value
        elif compact_text(value):
            evidence.setdefault(field, []).append(source)
            return value
    return default


def first_payload(completion: dict[str, Any]) -> tuple[dict[str, Any], str]:
    for field_name in ("mathematical_payload_manifest", "new_mathematical_payload"):
        payloads = completion.get(field_name)
        if isinstance(payloads, list):
            for payload in payloads:
                if isinstance(payload, dict):
                    return payload, f"completion.{field_name}[0]"
    return {}, ""


def infer_object_name(
    task: dict[str, Any],
    job: dict[str, Any],
    completion: dict[str, Any],
    evidence: dict[str, list[str]],
) -> str:
    payload, payload_source = first_payload(completion)
    candidates: list[tuple[Any, str]] = [
        (payload.get("object_name", ""), f"{payload_source}.object_name" if payload_source else ""),
        (
            nested_get(completion, "candidate_constructor_result.formal_objects"),
            "completion.candidate_constructor_result.formal_objects",
        ),
        (
            nested_get(completion, "ontology_law_research_packet.candidate_law_payload.formal_objects"),
            "completion.ontology_law_research_packet.candidate_law_payload.formal_objects",
        ),
    ]
    accepted = completion.get("three_tier_claim_summary", {})
    if isinstance(accepted, dict):
        for section_name in ("accepted_evidence_preconditions", "adopted_objects"):
            section = accepted.get(section_name)
            if isinstance(section, list) and section and isinstance(section[0], dict):
                candidates.append(
                    (
                        section[0].get("object", ""),
                        f"completion.three_tier_claim_summary.{section_name}[0].object",
                    )
                )
    for value, source in candidates:
        if isinstance(value, list) and value:
            first = compact_text(value[0])
            if first:
                evidence.setdefault("object_name", []).append(source)
                return first
        text = compact_text(value)
        if text:
            evidence.setdefault("object_name", []).append(source)
            return text

    blob = text_blob(task, job, completion)
    for pattern in KNOWN_OBJECT_PATTERNS:
        if pattern in blob:
            evidence.setdefault("object_name", []).append("text_pattern")
            return pattern
    return "none"


def infer_object_family(object_name: str, task: dict[str, Any], job: dict[str, Any]) -> str:
    lower = object_name.lower()
    if "route_signature" in lower:
        return "route_orbit_control"
    if "frontier_theorem_inventory" in lower:
        return "frontier_theorem_inventory"
    if "rr_e" in lower:
        return "rr_e"
    if "mattersemantics" in object_name or "PositiveMSProfile" in object_name:
        return "matter_coupling"
    if object_name != "none":
        return normalize_compact(object_name, default="unknown")
    milestone = first_nonempty(
        job.get("target_derivation_milestone", ""),
        task.get("target_derivation_milestone", ""),
    )
    return normalize_compact(milestone, default="none")


def infer_source_extension_category(task_type: str, role_id: str, route_label: str) -> str:
    text = f"{task_type} {role_id} {route_label}".lower()
    if "human_gate" in text or "gate-chair" in text or "gate_chair" in text:
        return "source_extension_human_gate"
    if "refuter" in text or "stress" in text:
        return "source_extension_refuter_stress"
    if "smuggling" in text or "audit" in text:
        return "source_extension_smuggling_audit"
    if "candidate" in text or "formalizer" in text or "ontology_law" in text or "ontology-law" in text:
        return "source_extension_candidate"
    if "adopted_or_rejected" in text:
        return "source_extension_adopted_or_rejected"
    return "none"


def infer_gate_chair_state(role_id: str, task: dict[str, Any], job: dict[str, Any], completion: dict[str, Any]) -> str:
    milestone = compact_text(first_nonempty(job.get("target_derivation_milestone", ""), task.get("target_derivation_milestone", "")))
    if role_id != "gate-chair":
        return "not_requested" if milestone and milestone != "none" else "not_applicable"
    blob = text_blob(task, job, completion).lower()
    if "adoption_authorized" in blob or "adoption authorized" in blob:
        return "adoption_authorized"
    if ("accepted" in blob or "accepts" in blob) and ("scoped" in blob or "precondition" in blob):
        return "scoped_evidence_or_precondition_accepted"
    if "rejected" in blob or "blocked" in blob:
        return "adoption_rejected_or_blocked"
    return "unknown"


def infer_boundary_sync_state(
    task_type: str,
    route_label: str,
    plan_task_id: str,
    gate_state: str,
) -> str:
    text = f"{task_type} {route_label} {plan_task_id}".lower()
    if "boundary" in text or "sync" in text or "synchronization" in text:
        return "synchronized"
    if gate_state == "scoped_evidence_or_precondition_accepted":
        return "pending"
    return "not_applicable"


def infer_missing_primitive(completion: dict[str, Any], evidence: dict[str, list[str]]) -> str:
    candidates = [
        (nested_get(completion, "bridge_attempt_status.missing_primitive"), "completion.bridge_attempt_status.missing_primitive"),
        (nested_get(completion, "ontology_law_research_packet.missing_source_law"), "completion.ontology_law_research_packet.missing_source_law"),
        (nested_get(completion, "route_cycle_control.missing_primitive"), "completion.route_cycle_control.missing_primitive"),
        (nested_get(completion, "loop_risk_decision.missing_primitive"), "completion.loop_risk_decision.missing_primitive"),
    ]
    value = choose_with_source(evidence, "missing_primitive", candidates, "none")
    return compact_text(value) or "none"


def infer_obstruction_label(completion: dict[str, Any], object_name: str, evidence: dict[str, list[str]]) -> str:
    candidates = [
        (nested_get(completion, "obstruction_record.obstruction_id"), "completion.obstruction_record.obstruction_id"),
        (nested_get(completion, "obstruction_record.label"), "completion.obstruction_record.label"),
        (nested_get(completion, "candidate_constructor_result.obstruction_id"), "completion.candidate_constructor_result.obstruction_id"),
    ]
    value = choose_with_source(evidence, "obstruction_label", candidates, "")
    if compact_text(value):
        return compact_text(value)
    if "obstruction" in object_name.lower():
        evidence.setdefault("obstruction_label", []).append("object_name")
        return object_name
    return "none"


def infer_freeze_candidate(completion: dict[str, Any], evidence: dict[str, list[str]]) -> str:
    freeze = completion.get("freeze_criteria_status")
    if isinstance(freeze, dict):
        value = first_nonempty(
            freeze.get("active_freeze_label", ""),
            freeze.get("candidate_freeze_label", ""),
            freeze.get("freeze_decision", ""),
        )
        if compact_text(value):
            evidence.setdefault("freeze_candidate", []).append("completion.freeze_criteria_status")
            return compact_text(value)
        return "true"
    return "none"


def has_nested_key(data: Any, key_fragment: str) -> bool:
    if isinstance(data, dict):
        for key, value in data.items():
            if key_fragment in str(key).lower() or has_nested_key(value, key_fragment):
                return True
    if isinstance(data, list):
        return any(has_nested_key(value, key_fragment) for value in data)
    return False


def infer_new_source_evidence(completion: dict[str, Any]) -> bool:
    payload, _ = first_payload(completion)
    if compact_text(payload.get("source_path", "")):
        return True
    output_paths = [str(path) for path in as_list(completion.get("output_paths", []))]
    if any(path.endswith(".tex") for path in output_paths):
        return True
    inspections = nested_get(completion, "memory_preflight.canonical_inspections")
    if isinstance(inspections, list):
        for item in inspections:
            if isinstance(item, dict) and item.get("source_registry") == "TEX_SOURCE_REGISTRY.csv":
                return True
    return False


def compute_signature_hash(signature: dict[str, Any]) -> str:
    comparison = {field: signature[field] for field in COMPARISON_FIELDS}
    payload = json.dumps(comparison, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_signature(
    task_row: dict[str, str],
    job_row: dict[str, str],
    task: dict[str, Any],
    job: dict[str, Any],
    completion: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    evidence: dict[str, list[str]] = {}
    source_task_id = compact_text(first_nonempty(task.get("task_id", ""), task_row.get("task_id", ""))) or "unknown"
    source_job_id = compact_text(first_nonempty(job.get("job_id", ""), task_row.get("current_job_id", ""), job_row.get("job_id", ""))) or "unknown"
    completion_path = compact_text(first_nonempty(job_row.get("completion_path", ""), ""))

    implementation_plan = task.get("implementation_plan", {})
    if not isinstance(implementation_plan, dict):
        implementation_plan = {}

    plan_task_id = compact_text(
        first_nonempty(
            implementation_plan.get("task_id", ""),
            implementation_plan.get("plan_task_id", ""),
            job.get("plan_task_id", ""),
            nested_get(completion, "implementation_plan_receipt.related_plan_task_id"),
        )
    ) or "none"
    task_type = normalize_lower(first_nonempty(task.get("task_type", ""), task_row.get("task_type", "")), default="unknown")
    role_id = normalize_lower(first_nonempty(job.get("role_id", ""), job_row.get("role_id", "")), default="unknown")
    route_label = compact_text(first_nonempty(job.get("route_label", ""), nested_get(completion, "verdict"), task_row.get("closure_status", "")))
    selected_route = normalize_compact(route_label, default="unknown")
    object_name = infer_object_name(task, job, completion, evidence)
    object_family = infer_object_family(object_name, task, job)
    gate_state = infer_gate_chair_state(role_id, task, job, completion)
    boundary_state = infer_boundary_sync_state(task_type, route_label, plan_task_id, gate_state)
    payload, payload_source = first_payload(completion)
    payload_type = compact_text(payload.get("payload_type", "")) if payload else ""
    if payload_type:
        evidence.setdefault("payload_type", []).append(f"{payload_source}.payload_type")

    previous_task_ids = sorted(
        {
            compact_text(value)
            for value in [
                task_row.get("parent_task_id", ""),
                task.get("parent_task_id", ""),
                task.get("previous_task_id", ""),
            ]
            + [
                compact_text(item)
                for item in as_list(nested_get(completion, "route_cycle_control.prior_related_tasks"))
            ]
            if compact_text(value)
        }
    )

    signature = {
        "signature_schema_id": SIGNATURE_SCHEMA_ID,
        "signature_id": f"route-sig-{source_task_id}",
        "source_task_id": source_task_id,
        "source_job_id": source_job_id,
        "source_completion_path": completion_path,
        "implementation_plan_id": normalize_lower(implementation_plan.get("plan_id", ""), default="none"),
        "plan_task_id": plan_task_id,
        "target_derivation_milestone": normalize_compact(
            first_nonempty(job.get("target_derivation_milestone", ""), task.get("target_derivation_milestone", "")),
            default="none",
        ),
        "milestone_burden": normalize_compact(
            first_nonempty(
                nested_get(completion, "distance_to_gr_delta.burden_id"),
                job.get("milestone_burden", ""),
                task.get("milestone_burden", ""),
            ),
            default="none",
        ),
        "object_family": object_family,
        "object_name": object_name,
        "task_type": task_type,
        "role_id": role_id,
        "execution_role_ref": compact_text(job.get("execution_role_ref", "")),
        "source_extension_category": infer_source_extension_category(task_type, role_id, route_label),
        "selected_route": selected_route,
        "missing_primitive": infer_missing_primitive(completion, evidence),
        "payload_type": payload_type or "none",
        "obstruction_label": infer_obstruction_label(completion, object_name, evidence),
        "freeze_candidate": infer_freeze_candidate(completion, evidence),
        "boundary_synchronization_state": boundary_state,
        "gate_chair_state": gate_state,
        "previous_task_ids": previous_task_ids,
        "new_mathematical_payload_exists": bool(
            as_list(completion.get("new_mathematical_payload", []))
            or as_list(completion.get("mathematical_payload_manifest", []))
        ),
        "exact_repair_attempted": (
            has_nested_key(completion, "repair_attempt")
            or "repair" in task_type
            or "repair" in selected_route
        ),
        "freeze_criteria_evaluated": isinstance(completion.get("freeze_criteria_status"), dict),
        "new_source_evidence_exists": infer_new_source_evidence(completion),
        "source_evidence": evidence,
    }
    signature["signature_hash"] = compute_signature_hash(signature)
    return signature


def load_records(repo_root: Path) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    task_rows = read_csv_rows(repo_root / "registries" / "RESEARCH_TASK_REGISTRY.csv")
    job_rows = index_by(read_csv_rows(repo_root / "registries" / "AGENT_JOB_REGISTRY.csv"), "task_id")
    return task_rows, job_rows


def select_task_rows(
    rows: list[dict[str, str]],
    task_ids: list[str] | None = None,
    sample: str = "",
    limit: int = 0,
) -> list[dict[str, str]]:
    selected_ids = list(task_ids or [])
    if sample == "recent-matter-rr-e":
        selected_ids.extend(RECENT_MATTER_RR_E_SAMPLE_TASK_IDS)
    if selected_ids:
        wanted = set(selected_ids)
        selected = [row for row in rows if row.get("task_id", "") in wanted]
        order = {task_id: index for index, task_id in enumerate(selected_ids)}
        selected.sort(key=lambda row: order.get(row.get("task_id", ""), len(order)))
    else:
        selected = list(rows)
    if limit > 0:
        selected = selected[:limit]
    return selected


def build_route_history(
    repo_root: Path = REPO_ROOT,
    task_ids: list[str] | None = None,
    sample: str = "",
    limit: int = 0,
) -> dict[str, Any]:
    task_rows, job_rows = load_records(repo_root)
    selected_rows = select_task_rows(task_rows, task_ids=task_ids, sample=sample, limit=limit)
    signatures: list[dict[str, Any]] = []
    extraction_errors: list[str] = []

    for task_row in selected_rows:
        task_id = task_row.get("task_id", "")
        task_dir = repo_root / task_row.get("task_path", "")
        task, task_error = load_yaml_record(task_dir / "00_TASK.yaml")
        if task_error:
            extraction_errors.append(task_error)
        job_row = job_rows.get(task_id, {})
        job_path = repo_root / job_row.get("job_path", "")
        job, job_error = load_yaml_record(job_path) if job_path != repo_root else ({}, "missing:job_path")
        if job_error:
            extraction_errors.append(job_error)
        completion_path = repo_root / job_row.get("completion_path", "")
        completion, completion_error = (
            load_yaml_record(completion_path) if completion_path != repo_root else ({}, "missing:completion_path")
        )
        if completion_error:
            extraction_errors.append(completion_error)
        signatures.append(build_signature(task_row, job_row, task, job, completion, repo_root))

    return {
        "schema_id": EXTRACTOR_SCHEMA_ID,
        "signature_schema_id": SIGNATURE_SCHEMA_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_registries": [
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
        ],
        "task_count": len(selected_rows),
        "signature_count": len(signatures),
        "sample": sample or "",
        "signatures": signatures,
        "extraction_errors": extraction_errors,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--task-id", action="append", default=[], help="Restrict extraction to a task ID; repeatable.")
    parser.add_argument("--sample", choices=["recent-matter-rr-e"], default="", help="Emit a built-in task sample.")
    parser.add_argument("--limit", type=int, default=0, help="Limit selected rows after filtering.")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    repo_root = args.repo_root.resolve()
    report = build_route_history(
        repo_root=repo_root,
        task_ids=args.task_id,
        sample=args.sample,
        limit=args.limit,
    )
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output is not None:
        output_path = args.output
        if not output_path.is_absolute():
            output_path = repo_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    if args.json or args.output is None:
        print(payload, end="")
    return 0 if not report["extraction_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
