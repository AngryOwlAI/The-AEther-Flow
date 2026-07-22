#!/usr/bin/env python3
"""Classify task records into the v21 orthogonal project-control taxonomy.

The adapter is additive and read-only with respect to task source records. Its
classifications are routing and analytics metadata, never scientific status or
promotion authority.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = "research_control/design/v21_task_taxonomy_policy.md"
BACKLOG_PATH = "research_control/design/v21_recommendation_backlog.yaml"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"
ROLE_REGISTRY_PATH = "registries/AGENT_ROLE_REGISTRY.csv"
TASKS_ROOT = "research_control/tasks"
CONTRACT_START = "<!-- v21-task-taxonomy-contract:start -->"
CONTRACT_END = "<!-- v21-task-taxonomy-contract:end -->"
SCHEMA_ID = "v21_task_taxonomy_v1"
EFFECTIVE_AT = "2026-07-22T01:19:45Z"
FIELDS = (
    "work_kind",
    "milestone",
    "candidate_family",
    "result_kind",
    "authority",
    "scope",
)
WORK_KINDS = {
    "audit_or_review",
    "benchmark_or_recovery",
    "construction_or_implementation",
    "formalization_or_theorem",
    "integration_or_selection",
    "protected_gate_review",
    "publication_preparation",
    "unknown",
}
MILESTONES = {
    "source_ontology",
    "source_equivalence_eqsrc",
    "effective_metric_g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
    "not_applicable",
    "unknown",
}
RESULT_KINDS = {
    "audit_verdict_or_precise_repair",
    "candidate_or_precise_obstruction",
    "completed_or_precisely_blocked",
    "implemented_and_validated_or_precisely_blocked",
    "protected_verdict_or_deferred_human_gate",
    "theorem_or_precise_obstruction",
    "not_applicable",
    "unknown",
}
AUTHORITIES = {
    "human_gated",
    "process_control",
    "project_control",
    "routing_control",
    "science_draft",
    "unknown",
}
SCOPES = {
    "human_gate",
    "project_system",
    "routing",
    "scientific",
    "scientific_audit",
    "mixed",
    "unknown",
}
CANDIDATE_FAMILY_RE = re.compile(r"^[a-z0-9][a-z0-9_]{0,95}$")
VOCABULARIES = {
    "work_kind": WORK_KINDS,
    "milestone": MILESTONES,
    "result_kind": RESULT_KINDS,
    "authority": AUTHORITIES,
    "scope": SCOPES,
}
DEFAULT_POLICY = {
    "schema_id": SCHEMA_ID,
    "effective_at": EFFECTIVE_AT,
    "required_top_level_fields": ["title", "task_type", "task_taxonomy"],
    "required_taxonomy_fields": list(FIELDS),
    "vocabularies": {
        "work_kind": [
            "audit_or_review",
            "benchmark_or_recovery",
            "construction_or_implementation",
            "formalization_or_theorem",
            "integration_or_selection",
            "protected_gate_review",
            "publication_preparation",
            "unknown",
        ],
        "milestone": [
            "source_ontology",
            "source_equivalence_eqsrc",
            "effective_metric_g_eff",
            "matter_coupling",
            "einstein_equations",
            "benchmark_promotion",
            "not_applicable",
            "unknown",
        ],
        "result_kind": [
            "audit_verdict_or_precise_repair",
            "candidate_or_precise_obstruction",
            "completed_or_precisely_blocked",
            "implemented_and_validated_or_precisely_blocked",
            "protected_verdict_or_deferred_human_gate",
            "theorem_or_precise_obstruction",
            "not_applicable",
            "unknown",
        ],
        "authority": [
            "human_gated",
            "process_control",
            "project_control",
            "routing_control",
            "science_draft",
            "unknown",
        ],
        "scope": [
            "human_gate",
            "project_system",
            "routing",
            "scientific",
            "scientific_audit",
            "mixed",
            "unknown",
        ],
    },
    "candidate_family_contract": {
        "pattern": CANDIDATE_FAMILY_RE.pattern,
        "reserved_values": ["not_applicable", "unknown"],
    },
    "confidence_values": ["high", "medium", "low", "unknown"],
    "source_values": ["explicit", "plan_metadata", "legacy_compatibility", "unknown"],
    "authority_boundaries": {
        "classification_is_scientific_status": False,
        "classification_can_strengthen_science": False,
        "classification_can_promote_claims": False,
        "classification_can_adopt_ontology_or_law": False,
        "classification_can_supply_human_authority": False,
        "raw_historical_records_may_be_mutated": False,
        "unknown_must_be_retained_on_ambiguity": True,
    },
}


class TaskTaxonomyError(RuntimeError):
    """Raised when the taxonomy contract or repository sources are invalid."""


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_policy(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    path = repo_root / POLICY_PATH
    if not path.exists():
        raise TaskTaxonomyError(f"missing taxonomy policy: {POLICY_PATH}")
    text = path.read_text(encoding="utf-8")
    if text.count(CONTRACT_START) != 1 or text.count(CONTRACT_END) != 1:
        raise TaskTaxonomyError("taxonomy policy must contain exactly one machine-contract marker pair")
    body = text.split(CONTRACT_START, 1)[1].split(CONTRACT_END, 1)[0].strip()
    match = re.fullmatch(r"```json\s*(\{.*\})\s*```", body, flags=re.DOTALL)
    if not match:
        raise TaskTaxonomyError("taxonomy policy machine contract is not one fenced JSON object")
    try:
        policy = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise TaskTaxonomyError(f"taxonomy policy JSON is malformed: {exc}") from exc
    if policy != DEFAULT_POLICY:
        raise TaskTaxonomyError("taxonomy policy machine contract differs from the executable v1 contract")
    return policy


def read_csv(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    path = repo_root / rel_path
    if not path.exists():
        raise TaskTaxonomyError(f"missing required registry: {rel_path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def load_optional_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = load_yaml(path)
    except StrictYamlError as exc:
        raise TaskTaxonomyError(f"malformed YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TaskTaxonomyError(f"top-level YAML value is not a mapping: {path}")
    return value


def role_key(role_id: Any, role_version: Any) -> tuple[str, str]:
    return text_value(role_id), text_value(role_version)


def plan_task_id(task: dict[str, Any]) -> str:
    plan = dict_value(task.get("implementation_plan"))
    return text_value(plan.get("plan_task_id") or task.get("plan_task_id"))


def load_plan_items(repo_root: Path = REPO_ROOT) -> dict[str, dict[str, Any]]:
    path = repo_root / BACKLOG_PATH
    if not path.exists():
        raise TaskTaxonomyError(f"missing v21 backlog: {BACKLOG_PATH}")
    try:
        backlog = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise TaskTaxonomyError(f"malformed YAML {path}: {exc}") from exc
    if not isinstance(backlog, dict):
        raise TaskTaxonomyError(f"top-level YAML value is not a mapping: {path}")
    items = backlog.get("items")
    if not isinstance(items, list):
        raise TaskTaxonomyError(f"{BACKLOG_PATH} does not contain an items list")
    output: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = text_value(item.get("plan_task_id"))
        if item_id:
            output[item_id] = item
    return output


def explicit_required(task: dict[str, Any]) -> bool:
    created_at = text_value(task.get("created_at"))
    return bool(created_at and created_at >= EFFECTIVE_AT)


def validate_explicit(task: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    raw = task.get("task_taxonomy")
    errors: list[str] = []
    if not isinstance(raw, dict):
        return {field: "unknown" for field in FIELDS}, ["task_taxonomy_missing_or_not_mapping"]
    allowed_keys = {"schema_id", *FIELDS}
    extra = sorted(set(raw) - allowed_keys)
    missing = [field for field in FIELDS if not text_value(raw.get(field))]
    if text_value(raw.get("schema_id")) != SCHEMA_ID:
        errors.append("task_taxonomy_schema_id_invalid")
    if extra:
        errors.append("task_taxonomy_extra_fields:" + ";".join(extra))
    if missing:
        errors.append("task_taxonomy_missing_fields:" + ";".join(missing))
    fields = {field: text_value(raw.get(field)) or "unknown" for field in FIELDS}
    for field, vocabulary in VOCABULARIES.items():
        if fields[field] not in vocabulary:
            errors.append(f"task_taxonomy_invalid_{field}:{fields[field]}")
    candidate_family = fields["candidate_family"]
    if not CANDIDATE_FAMILY_RE.fullmatch(candidate_family):
        errors.append(f"task_taxonomy_invalid_candidate_family:{candidate_family}")
    return fields, errors


def scope_from(task_class: str, authority: str, work_kind: str) -> str:
    if authority == "human_gated" or work_kind == "protected_gate_review":
        return "human_gate"
    if task_class in {"project_system", "control"} or authority in {"project_control", "process_control"}:
        return "project_system"
    if authority == "routing_control":
        return "routing"
    if task_class == "audit" or work_kind == "audit_or_review":
        return "scientific_audit"
    if task_class == "science" or authority == "science_draft":
        return "scientific"
    return "unknown"


def authority_from(role: dict[str, Any], task_class: str) -> str:
    registered = text_value(role.get("authority_level"))
    if registered in AUTHORITIES:
        return registered
    return {
        "project_system": "project_control",
        "control": "routing_control",
        "audit": "science_draft",
        "science": "science_draft",
    }.get(task_class, "unknown")


def legacy_work_kind(text: str) -> str:
    if any(token in text for token in ("gate_chair", "protected_gate", "human_gate", "gate_review")):
        return "protected_gate_review"
    if any(token in text for token in ("publication", "outreach", "submission", "release")):
        return "publication_preparation"
    if any(token in text for token in ("smuggling_audit", "audit", "review", "refuter", "stress_test", "red_team")):
        return "audit_or_review"
    if any(token in text for token in ("theorem", "formalization", "lemma", "proof")):
        return "formalization_or_theorem"
    if any(token in text for token in ("benchmark", "recovery", "regression")):
        return "benchmark_or_recovery"
    if any(token in text for token in ("selector", "integration", "synthesis", "taxonomy", "routing")):
        return "integration_or_selection"
    if any(token in text for token in ("candidate", "construct", "implement", "schema", "validator", "renderer", "repair", "fixture")):
        return "construction_or_implementation"
    return "unknown"


def result_from_work_kind(work_kind: str) -> str:
    return {
        "audit_or_review": "audit_verdict_or_precise_repair",
        "benchmark_or_recovery": "completed_or_precisely_blocked",
        "construction_or_implementation": "implemented_and_validated_or_precisely_blocked",
        "formalization_or_theorem": "theorem_or_precise_obstruction",
        "integration_or_selection": "completed_or_precisely_blocked",
        "protected_gate_review": "protected_verdict_or_deferred_human_gate",
        "publication_preparation": "completed_or_precisely_blocked",
    }.get(work_kind, "unknown")


def classify_task(
    task: dict[str, Any],
    registry_row: dict[str, Any] | None = None,
    job: dict[str, Any] | None = None,
    role: dict[str, Any] | None = None,
    plan_item: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return one non-mutating normalized view of a task record."""

    registry_row = registry_row or {}
    job = job or {}
    role = role or {}
    plan_item = plan_item or {}
    task_id = text_value(task.get("task_id") or registry_row.get("task_id"))
    title = text_value(task.get("title") or plan_item.get("title"))
    raw_task_type = text_value(task.get("task_type") or registry_row.get("task_type"))
    required = explicit_required(task)
    explicit = task.get("task_taxonomy")
    errors: list[str] = []

    if isinstance(explicit, dict):
        fields, errors = validate_explicit(task)
        source = "explicit"
        confidence = "high" if not errors and "unknown" not in fields.values() else "low"
        field_sources = {field: "explicit" for field in FIELDS}
    elif plan_item:
        task_class = text_value(plan_item.get("task_class"))
        work_kind = text_value(plan_item.get("work_kind"))
        milestone = text_value(plan_item.get("target_derivation_milestone"))
        result_kind = text_value(plan_item.get("expected_result_kind"))
        authority = authority_from(role, task_class)
        scope = scope_from(task_class, authority, work_kind)
        candidate_family = "not_applicable" if scope in {"project_system", "routing", "human_gate"} else "unknown"
        fields = {
            "work_kind": work_kind if work_kind in WORK_KINDS else "unknown",
            "milestone": milestone if milestone in MILESTONES else "unknown",
            "candidate_family": candidate_family,
            "result_kind": result_kind if result_kind in RESULT_KINDS else "unknown",
            "authority": authority,
            "scope": scope,
        }
        source = "plan_metadata"
        confidence = "medium" if "unknown" in fields.values() else "high"
        field_sources = {
            "work_kind": "plan_metadata",
            "milestone": "plan_metadata",
            "candidate_family": "plan_metadata",
            "result_kind": "plan_metadata",
            "authority": "registered_role" if text_value(role.get("authority_level")) else "plan_metadata",
            "scope": "plan_metadata",
        }
    else:
        authority = authority_from(role, "")
        route_text = " ".join(
            [
                raw_task_type,
                title,
                text_value(task.get("route_label")),
                text_value(job.get("route_label")),
            ]
        ).lower()
        work_kind = legacy_work_kind(route_text)
        milestone_raw = text_value(
            task.get("target_derivation_milestone")
            or job.get("target_derivation_milestone")
        )
        milestone = milestone_raw if milestone_raw in MILESTONES else "unknown"
        scope = scope_from("", authority, work_kind)
        if text_value(job.get("project_system_boundary_authorized_by_plan")).lower() == "true":
            scope = "project_system"
            if authority == "unknown":
                authority = "project_control"
        fields = {
            "work_kind": work_kind,
            "milestone": milestone,
            "candidate_family": "not_applicable" if scope in {"project_system", "routing", "human_gate"} else "unknown",
            "result_kind": result_from_work_kind(work_kind),
            "authority": authority,
            "scope": scope,
        }
        source = "legacy_compatibility" if any(value != "unknown" for value in fields.values()) else "unknown"
        confidence = "low" if source == "legacy_compatibility" else "unknown"
        field_sources = {field: source for field in FIELDS}
        if authority != "unknown" and text_value(role.get("authority_level")):
            field_sources["authority"] = "registered_role"

    if required:
        for top_level in ("title", "task_type"):
            if not text_value(task.get(top_level)):
                errors.append(f"required_top_level_field_missing:{top_level}")
        if not isinstance(explicit, dict):
            errors.append("required_explicit_task_taxonomy_missing")

    unknown_fields = [field for field in FIELDS if fields.get(field) == "unknown"]
    return {
        "task_id": task_id,
        "title": title,
        "raw_task_type": raw_task_type,
        **fields,
        "taxonomy_source": source,
        "taxonomy_confidence": confidence,
        "field_sources": field_sources,
        "unknown_fields": unknown_fields,
        "explicit_required": required,
        "errors": sorted(set(errors)),
        "historical_source_mutated": False,
        "stronger_science_inferred": False,
        "classification_is_scientific_status": False,
        "physics_promotion_authorized": False,
    }


def repository_context(repo_root: Path) -> tuple[
    list[dict[str, str]],
    dict[str, dict[str, str]],
    dict[tuple[str, str], dict[str, str]],
    dict[str, dict[str, Any]],
]:
    task_rows = read_csv(repo_root, TASK_REGISTRY_PATH)
    registered_ids = {row.get("task_id", "") for row in task_rows}
    tasks_root = repo_root / TASKS_ROOT
    if tasks_root.exists():
        for task_dir in sorted(tasks_root.iterdir()):
            if not task_dir.is_dir() or not task_dir.name.startswith("RT-"):
                continue
            if task_dir.name in registered_ids:
                continue
            task_rows.append(
                {
                    "task_id": task_dir.name,
                    "task_path": task_dir.relative_to(repo_root).as_posix(),
                }
            )
    job_rows = read_csv(repo_root, JOB_REGISTRY_PATH)
    role_rows = read_csv(repo_root, ROLE_REGISTRY_PATH)
    jobs = {row.get("job_id", ""): row for row in job_rows if row.get("job_id")}
    roles = {
        role_key(row.get("role_id"), row.get("version")): row
        for row in role_rows
        if row.get("role_id") and row.get("version")
    }
    return task_rows, jobs, roles, load_plan_items(repo_root)


def historical_source_hashes(repo_root: Path, task_rows: list[dict[str, str]]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for row in task_rows:
        task_path = text_value(row.get("task_path"))
        if not task_path:
            continue
        path = repo_root / task_path / "00_TASK.yaml"
        task = load_optional_yaml(path)
        if explicit_required(task):
            continue
        hashes[path.relative_to(repo_root).as_posix()] = file_hash(path)
    return hashes


def build_repository_report(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    policy = load_policy(repo_root)
    task_rows, jobs, roles, plan_items = repository_context(repo_root)
    before_hashes = historical_source_hashes(repo_root, task_rows)
    classifications: list[dict[str, Any]] = []
    for row in task_rows:
        task_path = text_value(row.get("task_path"))
        task = load_optional_yaml(repo_root / task_path / "00_TASK.yaml") if task_path else {}
        job_id = text_value(task.get("current_job_id") or row.get("current_job_id"))
        job_row = jobs.get(job_id, {})
        job_path = text_value(job_row.get("job_path"))
        job = load_optional_yaml(repo_root / job_path) if job_path else {}
        role = roles.get(role_key(job.get("role_id") or job_row.get("role_id"), job.get("role_version") or job_row.get("role_version")), {})
        item = plan_items.get(plan_task_id(task), {})
        classifications.append(classify_task(task, row, job, role, item))
    after_hashes = historical_source_hashes(repo_root, task_rows)

    source_counts = Counter(item["taxonomy_source"] for item in classifications)
    confidence_counts = Counter(item["taxonomy_confidence"] for item in classifications)
    unknown_counts = {
        field: sum(1 for item in classifications if item[field] == "unknown")
        for field in FIELDS
    }
    required = [item for item in classifications if item["explicit_required"]]
    required_errors = [item for item in required if item["errors"]]
    mutated_paths = sorted(path for path in before_hashes if before_hashes[path] != after_hashes.get(path, ""))
    stronger = [item["task_id"] for item in classifications if item["stronger_science_inferred"]]
    status = "PASS" if not required_errors and not mutated_paths and not stronger else "FAIL"
    generated_at = max(
        (
            text_value(load_optional_yaml(repo_root / row.get("task_path", "") / "00_TASK.yaml").get("updated_at")
            or load_optional_yaml(repo_root / row.get("task_path", "") / "00_TASK.yaml").get("created_at"))
            for row in task_rows
            if row.get("task_path")
        ),
        default=EFFECTIVE_AT,
    )
    return {
        "schema_id": "v21_task_taxonomy_historical_classification_report_v1",
        "taxonomy_schema_id": policy["schema_id"],
        "generated_at": generated_at,
        "status": status,
        "authority_boundary": {
            "operational_classification_only": True,
            "historical_records_mutated": False,
            "scientific_status_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
        "source_hashes": {
            POLICY_PATH: file_hash(repo_root / POLICY_PATH),
            BACKLOG_PATH: file_hash(repo_root / BACKLOG_PATH),
            TASK_REGISTRY_PATH: file_hash(repo_root / TASK_REGISTRY_PATH),
            JOB_REGISTRY_PATH: file_hash(repo_root / JOB_REGISTRY_PATH),
            ROLE_REGISTRY_PATH: file_hash(repo_root / ROLE_REGISTRY_PATH),
        },
        "counts": {
            "task_count": len(classifications),
            "historical_task_count": len(classifications) - len(required),
            "explicit_required_task_count": len(required),
            "explicit_required_error_count": len(required_errors),
            "source_counts": dict(sorted(source_counts.items())),
            "confidence_counts": dict(sorted(confidence_counts.items())),
            "unknown_field_counts": unknown_counts,
            "historical_source_mutation_count": len(mutated_paths),
            "stronger_science_inference_count": len(stronger),
            "raw_task_type_preserved_count": sum(bool(item["raw_task_type"]) for item in classifications),
            "readable_title_count": sum(bool(item["title"]) for item in classifications),
        },
        "required_task_errors": [
            {"task_id": item["task_id"], "errors": item["errors"]}
            for item in required_errors
        ],
        "historical_mutated_paths": mutated_paths,
        "stronger_science_inference_task_ids": stronger,
        "classifications": classifications,
    }


def compact_receipt(report: dict[str, Any]) -> dict[str, Any]:
    counts = report["counts"]
    return {
        "schema_id": "v21_task_taxonomy_compact_receipt_v1",
        "taxonomy_schema_id": report["taxonomy_schema_id"],
        "status": report["status"],
        "generated_at": report["generated_at"],
        "report_sha256": canonical_hash(report),
        "task_count": counts["task_count"],
        "historical_task_count": counts["historical_task_count"],
        "explicit_required_task_count": counts["explicit_required_task_count"],
        "explicit_required_error_count": counts["explicit_required_error_count"],
        "unknown_field_counts": counts["unknown_field_counts"],
        "low_confidence_count": counts["confidence_counts"].get("low", 0),
        "historical_source_mutation_count": counts["historical_source_mutation_count"],
        "stronger_science_inference_count": counts["stronger_science_inference_count"],
        "validator_ids": [
            "v21_task_taxonomy_schema",
            "v21_new_task_normalized_fields",
            "v21_historical_parse_coverage",
            "v21_no_historical_mutation",
            "v21_no_science_strengthening",
        ],
        "claim_boundary_summary": "Operational task classification only; no historical rewrite scientific-status change promotion proof or protected authority.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-repository", action="store_true", required=True)
    parser.add_argument("--write-report")
    parser.add_argument("--write-receipt")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root).resolve()
    try:
        report = build_repository_report(repo_root)
    except TaskTaxonomyError as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    receipt = compact_receipt(report)
    if args.write_report:
        path = Path(args.write_report)
        write_json(path if path.is_absolute() else repo_root / path, report)
    if args.write_receipt:
        path = Path(args.write_receipt)
        write_json(path if path.is_absolute() else repo_root / path, receipt)
    payload = receipt if args.json else {
        "status": report["status"],
        "task_count": report["counts"]["task_count"],
        "explicit_required_error_count": report["counts"]["explicit_required_error_count"],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
