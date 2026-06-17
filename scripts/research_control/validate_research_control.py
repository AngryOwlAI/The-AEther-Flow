#!/usr/bin/env python3
"""Validate the tracked research-control spine."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter
except ImportError:  # pragma: no cover - package import path for tests
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = REPO_ROOT / "registries"
CONTROL_DIR = REPO_ROOT / "research_control"

RESOLVER_SNAPSHOT_REQUIRED_FIELDS = (
    "status",
    "boundary",
    "reason",
    "resolver_is_advisory",
    "hard_checkpoint_gate",
    "checkpoint_gate_source",
    "selected_signal",
    "open_signals",
    "change_classification",
)

ROLE_COLUMNS = [
    "role_id",
    "version",
    "role_name",
    "role_kind",
    "role_contract_path",
    "authority_level",
    "status",
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
    "default_output_format",
    "default_validators",
    "created_at",
    "updated_at",
    "notes",
]

DECISION_COLUMNS = [
    "decision_id",
    "task_id",
    "decision_path",
    "director_version",
    "decision_type",
    "selected_role_id",
    "selected_role_version",
    "agent_job_id",
    "status",
    "supersedes_decision_id",
    "requires_human_gate",
    "created_at",
    "activated_at",
    "completed_at",
    "validation_status",
    "notes",
]

JOB_COLUMNS = [
    "job_id",
    "task_id",
    "decision_id",
    "role_id",
    "role_version",
    "job_path",
    "completion_path",
    "status",
    "allowed_write_paths",
    "output_paths",
    "validation_status",
    "created_at",
    "started_at",
    "completed_at",
    "requires_human_gate",
    "notes",
]

ROLE_EXECUTION_COLUMNS = [
    "execution_role_ref",
    "role_execution_kind",
    "task_id",
    "agent_job_id",
    "record_path",
    "base_role_id",
    "base_role_version",
    "provisional_role_name",
    "authority_delta_summary",
    "added_constraints",
    "removed_permissions",
    "expanded_permissions",
    "allowed_write_paths",
    "requires_human_gate",
    "expires_after",
    "justification",
    "non_reusable_until_registered",
    "validation_status",
    "created_at",
    "updated_at",
    "notes",
]

TASK_COLUMNS = [
    "task_id",
    "task_path",
    "task_type",
    "status",
    "current_decision_id",
    "current_job_id",
    "parent_task_id",
    "created_at",
    "updated_at",
    "closed_at",
    "closure_status",
    "requires_human_gate",
    "notes",
]

CLAIM_COLUMNS = [
    "claim_boundary_id",
    "scope",
    "applies_to_path",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "authority_source_path",
    "status",
    "created_at",
    "updated_at",
    "notes",
]

REGISTRY_COLUMNS = {
    "AGENT_ROLE_REGISTRY.csv": ROLE_COLUMNS,
    "ROLE_EXECUTION_REGISTRY.csv": ROLE_EXECUTION_COLUMNS,
    "DIRECTOR_DECISION_REGISTRY.csv": DECISION_COLUMNS,
    "AGENT_JOB_REGISTRY.csv": JOB_COLUMNS,
    "RESEARCH_TASK_REGISTRY.csv": TASK_COLUMNS,
    "CLAIM_BOUNDARY_REGISTRY.csv": CLAIM_COLUMNS,
}

BOOLEAN_FIELDS = {
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
    "non_reusable_until_registered",
}

SEMICOLON_FIELDS = {
    "default_validators",
    "allowed_write_paths",
    "output_paths",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "added_constraints",
    "removed_permissions",
    "expanded_permissions",
}

ROLE_EXECUTION_KINDS = {
    "registered_role",
    "task_overlay",
    "one_job_provisional_role",
}

PROTECTED_AUTHORITY_MARKERS = (
    "claim promotion",
    "promote claims",
    "physics claim promotion",
    "canonical ontology",
    "ontology edit",
    "benchmark promotion",
    "benchmark status",
    "gate chair",
    "gate verdict",
    "permanent role registration",
    "role registration",
    "register as a permanent role",
    "register as permanent role",
)

GLOBALLY_BROAD_PATTERNS = {
    "*",
    "**",
    "**/*",
    ".agents/**",
    "html/**",
    "ontology/**",
    "research_control/**",
    "research_control/tasks/**",
    "wiki/**",
}
MIXED_MARKDOWN_PATHS = {
    "README.md",
    "AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
}
CONTROL_MARKDOWN_PATTERNS = (
    ".agents/roles/**/*.md",
    ".agents/schemas/*.md",
    ".agents/schemas/**/*.md",
    ".codex/skills/*/SKILL.md",
)
AUTHORITY_MARKER_RE = re.compile(r"<!--\s*authority:\s*(explanatory|control)\s*-->")
HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

FORBIDDEN_PHRASES = [
    "GR derived from ontology",
    "exact GR recovered from ontology",
    "GR_DERIVED_FROM_ANTHOLOGY",
]

SAFE_BOUNDARY_MARKERS = (
    "forbidden",
    "not established",
    "not authorized",
    "without gate",
    "compatibility-only",
    "claim boundary",
    "blocked claim",
    "open derivation",
)

LOOP_CONTROL_POLICY_ACTIVATED_AT = "2026-06-16T19:17:22Z"
PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT = "2026-06-17T04:08:16Z"
THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT = "2026-06-17T04:29:31Z"

PHYSICS_ROLE_IDS = {
    "ontology-formalizer",
    "candidate-constructor",
    "refuter",
    "smuggling-auditor",
    "theoretical-continuation-selector",
}

PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES = {
    "canonical_ontology_write",
    "benchmark_promotion",
    "candidate_reconstruction",
    "gate_chair_verdict",
    "completed_derivation_claim",
    "global_theory_rejection",
    "generated_derivative_authority",
}

PHYSICS_JOB_FORBIDDEN_WRITE_PREFIXES = (
    "ontology/",
    "manuscripts/",
    "html/",
)

DISTANCE_TO_GR_REQUIRED_BURDENS = (
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "Finite variation robustness",
    "Concrete negative witnesses",
    "Observer normal/readout orbit",
    "Effective Lorentzian metric",
    "Universal matter coupling",
    "Einstein equations",
    "Benchmark promotion",
    "Gate Chair review",
    "Current line hard-fail",
)

LOOP_RISK_DECISION_CATEGORIES = {
    "concrete_witness_path",
    "source_side_irrelevance_theorem_path",
    "bridge_facing_candidate_path",
    "repeated_unmet_burdens_no_new_payload",
    "scoped_obstruction",
}

BRIDGE_OR_FAIL_ROUTES = {
    "candidate_constructor_bridge_attempt",
    "ontology_formalizer_concrete_witness_construction",
    "refuter_scoped_no_go_or_obstruction",
    "gate_chair_closure_or_suspension_proposal",
    "human_gated_ontology_change_required",
    "theoretical_decision_role_selection",
}

LEGACY_BRIDGE_OR_FAIL_ROUTES = {
    "controlled_pause",
}

LOOP_RISK_SUCCESS_ROUTES = {
    "continue_concrete_witness_path",
    "continue_source_side_irrelevance_theorem_path",
    "continue_bridge_facing_candidate_path",
}

ONTOLOGY_FORMALIZER_PAYLOAD_TYPES = {
    "finite_concrete_source_object_witnesses",
    "concrete_certificate_step_families",
    "explicit_inverse_provenance_tokens",
    "source_side_irrelevance_proof",
    "bridge_map_candidate",
    "theorem_with_hypotheses_and_proof",
    "countermodel_or_obstruction",
}

ONTOLOGY_PAYLOAD_TEXT_MARKERS = (
    "finite concrete",
    "concrete witness",
    "certificate-step",
    "certificate step",
    "inverse-provenance",
    "inverse provenance",
    "source-side irrelevance",
    "bridge map",
    "bridge candidate",
    "theorem",
    "countermodel",
    "obstruction",
)

THEORETICAL_DECISION_PACKET_TYPES = {
    "source_side_selector_primitive",
    "source_side_irrelevance_theorem",
    "concrete_resp_lc_witness",
    "distinct_scoped_no_go_question",
    "bounded_theoretical_calculation",
    "human_gated_ontology_change_required",
}

THEORETICAL_DECISION_TEXT_MARKERS = (
    "theoretical-continuation-selector",
    "theoretical continuation selector",
    "source-side selector",
    "selector primitive",
    "source-side irrelevance",
    "irrelevance theorem",
    "concrete resp_lc",
    "concrete resp lc",
    "resp_lc witness",
    "scoped no-go",
    "new mathematical payload",
    "bounded theoretical calculation",
)

PARENT_CHILD_SYNTHESIS_MODE = "parent_child_parallel_synthesis"
PARENT_CHILD_SYNTHESIS_VERSION = "0.1.0"
PARENT_CHILD_PARENT_UNIT_ID = "parent"
PARENT_CHILD_PARENT_PERSPECTIVE = "physicist_mathematician_philosopher"
PARENT_CHILD_REQUIRED_CHILDREN = {
    "child_phys_math": "physicist_mathematician",
    "child_phys_phil": "physicist_philosopher",
}
PARENT_CHILD_CONFLICT_TYPES = {
    "mathematical",
    "physical",
    "ontological",
    "claim_boundary",
    "source_or_citation",
    "terminology",
    "next_route",
    "validator_or_schema",
}
PARENT_CHILD_CONFLICT_SEVERITIES = {"blocking", "nonblocking"}
PARENT_CHILD_CONFLICT_STATUSES = {
    "no_conflict",
    "resolved",
    "unresolved_nonblocking",
    "unresolved_blocking",
    "blocked",
}
PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS = {
    "allowed_generated_paths",
    "allowed_read_paths",
    "allowed_source_classes",
    "allowed_write_paths",
    "authority_delta_summary",
    "base_role_id",
    "base_role_version",
    "claim_boundary",
    "expanded_permissions",
    "forbidden_paths",
    "forbidden_source_classes",
    "provisional_role_contract",
    "requires_human_gate",
    "role_id",
    "role_version",
}


def loop_control_policy() -> dict[str, object]:
    return {
        "policy_id": "bridge_or_fail_loop_control_v1",
        "activated_at": LOOP_CONTROL_POLICY_ACTIVATED_AT,
        "theoretical_continuation_policy_activated_at": THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT,
        "distance_to_gr_required_burdens": list(DISTANCE_TO_GR_REQUIRED_BURDENS),
        "refuter_decision_categories": sorted(LOOP_RISK_DECISION_CATEGORIES),
        "bridge_or_fail_routes": sorted(BRIDGE_OR_FAIL_ROUTES),
        "legacy_bridge_or_fail_routes": sorted(LEGACY_BRIDGE_OR_FAIL_ROUTES),
        "ontology_formalizer_payload_types": sorted(ONTOLOGY_FORMALIZER_PAYLOAD_TYPES),
        "theoretical_decision_packet_types": sorted(THEORETICAL_DECISION_PACKET_TYPES),
    }


def theoretical_continuation_policy() -> dict[str, object]:
    return {
        "policy_id": "theoretical_continuation_pause_gate_v1",
        "activated_at": THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT,
        "pause_route": "human_gated_ontology_change_required",
        "decision_role_id": "theoretical-continuation-selector",
        "generic_controlled_pause_allowed_for_future_physics": False,
        "allowed_theoretical_packet_types": sorted(THEORETICAL_DECISION_PACKET_TYPES),
    }


def parent_child_decomposition_policy() -> dict[str, object]:
    return {
        "policy_id": "parent_child_parallel_synthesis_v1",
        "mode": PARENT_CHILD_SYNTHESIS_MODE,
        "decomposition_version": PARENT_CHILD_SYNTHESIS_VERSION,
        "activated_at": PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT,
        "required_for_future_physics_agent_jobs": True,
        "execution_boundary": "one outer AgentJob with internal execution units",
        "parent": {
            "execution_unit_id": PARENT_CHILD_PARENT_UNIT_ID,
            "perspective": PARENT_CHILD_PARENT_PERSPECTIVE,
        },
        "children": [
            {"execution_unit_id": unit_id, "perspective": perspective}
            for unit_id, perspective in sorted(PARENT_CHILD_REQUIRED_CHILDREN.items())
        ],
        "conflict_types": sorted(PARENT_CHILD_CONFLICT_TYPES),
        "conflict_severities": sorted(PARENT_CHILD_CONFLICT_SEVERITIES),
        "forbidden_authority_expansion_keys": sorted(PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS),
    }


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self) -> bool:
        return not self.errors


def repo_path(relative_path: str) -> Path:
    return REPO_ROOT / relative_path


def validate_relative_path(path_text: str) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path.is_absolute():
        return "absolute paths are not allowed"
    if any(part == ".." for part in path.parts):
        return "path traversal is not allowed"
    return None


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def _clean_timestamp(value: Any) -> str:
    text = str(value or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", text):
        return text
    return ""


def timestamp_at_or_after(value: Any, threshold: str = LOOP_CONTROL_POLICY_ACTIVATED_AT) -> bool:
    text = _clean_timestamp(value)
    return bool(text and text >= threshold)


def job_policy_active(job_row: dict[str, str], completion: dict[str, Any] | None = None) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(timestamp_at_or_after(value) for value in timestamps)


def theoretical_continuation_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT)
        for value in timestamps
    )


def parent_child_required_for_job(job_row: dict[str, str]) -> bool:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return False
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    return any(
        timestamp_at_or_after(value, PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT)
        for value in timestamps
    )


def _collect_text(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        text: list[str] = []
        for child in value.values():
            text.extend(_collect_text(child))
        return text
    if isinstance(value, list):
        text = []
        for child in value:
            text.extend(_collect_text(child))
        return text
    return []


def text_blob(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        parts.extend(_collect_text(value))
    return "\n".join(parts).lower()


def read_csv_rows(name: str) -> list[dict[str, str]]:
    path = REGISTRY_DIR / name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def existing_by_id(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def role_key(role_id: str, version: str) -> str:
    return f"{role_id}@{version}"


def role_row_key(row: dict[str, str]) -> str:
    return role_key(row.get("role_id", ""), row.get("version", ""))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def validate_registry_columns(report: ValidationReport) -> None:
    for name, expected in REGISTRY_COLUMNS.items():
        path = REGISTRY_DIR / name
        if not path.exists():
            report.error(f"missing registry: registries/{name}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
        if header != expected:
            report.error(f"{name}: expected columns {expected}, found {header}")


def validate_registry_values(report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    seen: set[tuple[str, str]] = set()
    id_fields = {
        "AGENT_ROLE_REGISTRY.csv": "role_id",
        "ROLE_EXECUTION_REGISTRY.csv": "execution_role_ref",
        "DIRECTOR_DECISION_REGISTRY.csv": "decision_id",
        "AGENT_JOB_REGISTRY.csv": "job_id",
        "RESEARCH_TASK_REGISTRY.csv": "task_id",
        "CLAIM_BOUNDARY_REGISTRY.csv": "claim_boundary_id",
    }
    for registry_name, rows in rows_by_registry.items():
        id_field = id_fields[registry_name]
        local_ids: set[str] = set()
        for row_number, row in enumerate(rows, start=2):
            if registry_name == "AGENT_ROLE_REGISTRY.csv":
                missing = [
                    field_name
                    for field_name in ("role_id", "version")
                    if not row.get(field_name, "")
                ]
                for field_name in missing:
                    report.error(f"{registry_name}:{row_number}: missing {field_name}")
                row_id = role_row_key(row)
            else:
                row_id = row.get(id_field, "")
            if not row_id:
                report.error(f"{registry_name}:{row_number}: missing {id_field}")
            if row_id in local_ids:
                report.error(f"{registry_name}:{row_number}: duplicate {id_field} {row_id}")
            local_ids.add(row_id)
            seen.add((registry_name, row_id))
            for field_name in BOOLEAN_FIELDS & set(row):
                if row[field_name] not in {"true", "false"}:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must be lowercase true/false"
                    )
            for field_name in SEMICOLON_FIELDS & set(row):
                if "," in row[field_name]:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must use semicolons, not commas"
                    )


def _frontmatter_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def validate_roles(report: ValidationReport, role_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    roles = {role_row_key(row): row for row in role_rows if row.get("role_id") and row.get("version")}
    active_by_role_id: dict[str, str] = {}
    for row in role_rows:
        if row.get("status") == "active":
            previous = active_by_role_id.get(row["role_id"])
            if previous:
                report.error(
                    f"{row['role_id']}: multiple active role versions {previous} and {row['version']}"
                )
            active_by_role_id[row["role_id"]] = row["version"]
        path_text = row["role_contract_path"]
        reason = validate_relative_path(path_text)
        if reason:
            report.error(f"{role_row_key(row)}: invalid role_contract_path: {reason}")
            continue
        path = repo_path(path_text)
        if not path.exists():
            report.error(f"{role_row_key(row)}: missing role contract {path_text}")
            continue
        try:
            frontmatter, _ = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{path_text}: {exc}")
            continue
        for field_name in [
            "role_id",
            "version",
            "role_kind",
            "authority_level",
            "status",
            "may_execute_autonomously",
            "may_create_outputs",
            "may_modify_sources",
            "may_promote_claims",
            "requires_human_gate",
            "default_output_format",
            "default_validators",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{path_text}: frontmatter {field_name} does not match AGENT_ROLE_REGISTRY.csv"
                )
    return roles


def validate_tasks(
    report: ValidationReport,
    task_rows: list[dict[str, str]],
    decision_rows: dict[str, dict[str, str]],
    job_rows: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    tasks = existing_by_id(task_rows, "task_id")
    for row in task_rows:
        reason = validate_relative_path(row["task_path"])
        if reason:
            report.error(f"{row['task_id']}: invalid task_path: {reason}")
            continue
        task_dir = repo_path(row["task_path"])
        task_yaml = task_dir / "00_TASK.yaml"
        if not task_yaml.exists():
            report.error(f"{row['task_id']}: missing 00_TASK.yaml")
            continue
        try:
            task_data = load_yaml(task_yaml)
        except StrictYamlError as exc:
            report.error(f"{task_yaml.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        if str(task_data.get("task_id", "")) != row["task_id"]:
            report.error(f"{row['task_id']}: 00_TASK.yaml task_id mismatch")
        if row["current_decision_id"] and row["current_decision_id"] not in decision_rows:
            report.error(f"{row['task_id']}: current_decision_id is not registered")
        if row["current_job_id"] and row["current_job_id"] not in job_rows:
            report.error(f"{row['task_id']}: current_job_id is not registered")
    return tasks


def validate_director_decisions(
    report: ValidationReport,
    decision_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    decisions = existing_by_id(decision_rows, "decision_id")
    for row in decision_rows:
        reason = validate_relative_path(row["decision_path"])
        if reason:
            report.error(f"{row['decision_id']}: invalid decision_path: {reason}")
            continue
        path = repo_path(row["decision_path"])
        if not path.exists():
            report.error(f"{row['decision_id']}: missing DDR {row['decision_path']}")
            continue
        try:
            frontmatter, body = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{row['decision_path']}: {exc}")
            continue
        for field_name in [
            "decision_id",
            "task_id",
            "director_version",
            "decision_type",
            "selected_role_id",
            "selected_role_version",
            "agent_job_id",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['decision_path']}: frontmatter {field_name} does not match DIRECTOR_DECISION_REGISTRY.csv"
                )
        if row["decision_type"] != "provisional_role" and role_key(
            row["selected_role_id"], row["selected_role_version"]
        ) not in roles:
            report.error(f"{row['decision_id']}: selected role is not registered")
        if "## Role-Fit Matrix" not in body:
            report.error(f"{row['decision_path']}: missing ## Role-Fit Matrix")
    return decisions


def validate_agent_jobs(
    report: ValidationReport,
    job_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
    decisions: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    jobs = existing_by_id(job_rows, "job_id")
    for row in job_rows:
        reason = validate_relative_path(row["job_path"])
        if reason:
            report.error(f"{row['job_id']}: invalid job_path: {reason}")
            continue
        path = repo_path(row["job_path"])
        if not path.exists():
            report.error(f"{row['job_id']}: missing AgentJob {row['job_path']}")
            continue
        try:
            job = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{row['job_path']}: {exc}")
            continue
        for field_name in [
            "job_id",
            "task_id",
            "decision_id",
            "role_id",
            "role_version",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(job.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['job_path']}: {field_name} does not match AGENT_JOB_REGISTRY.csv"
                )
        if row["decision_id"] not in decisions:
            report.error(f"{row['job_id']}: decision_id is not registered")
        if role_key(row["role_id"], row["role_version"]) not in roles:
            provisional = job.get("provisional_role_contract")
            if not isinstance(provisional, dict):
                report.error(f"{row['job_id']}: unregistered role lacks provisional_role_contract")
            elif str(provisional.get("role_id", "")) != row["role_id"]:
                report.error(f"{row['job_id']}: provisional role_id mismatch")
            elif str(provisional.get("expires_after_job_id", "")) != row["job_id"]:
                report.error(f"{row['job_id']}: provisional role must expire after this job")
        for field_name in ["allowed_write_paths", "allowed_generated_paths", "forbidden_paths"]:
            value = job.get(field_name, [])
            if not isinstance(value, list):
                report.error(f"{row['job_path']}: {field_name} must be a list")
                continue
            for item in value:
                if not isinstance(item, str):
                    report.error(f"{row['job_path']}: {field_name} entries must be strings")
                    continue
                reason = validate_relative_path(item.replace("**", "x").replace("*", "x"))
                if reason:
                    report.error(f"{row['job_path']}: invalid {field_name} entry {item}: {reason}")
        validate_parent_child_decomposition(report, row, job)
        validate_future_physics_job_authority(report, row, job)
        if row["completion_path"]:
            completion_path = repo_path(row["completion_path"])
            if not completion_path.exists():
                report.error(f"{row['job_id']}: missing completion {row['completion_path']}")
            else:
                validate_completion(report, row, completion_path)
    return jobs


def validate_future_physics_job_authority(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
) -> None:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return
    if not job_policy_active(job_row):
        return

    path_text = job_row.get("job_path", job_row.get("job_id", ""))
    if parent_child_required_for_job(job_row) and not isinstance(
        job_contract.get("role_decomposition"), dict
    ):
        report.error(
            f"{path_text}: future physics AgentJob must declare "
            f"role_decomposition.mode={PARENT_CHILD_SYNTHESIS_MODE}"
        )

    forbidden_classes = set(_listish_values(job_contract.get("forbidden_source_classes", [])))
    missing = sorted(PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES - forbidden_classes)
    if missing:
        report.error(
            f"{path_text}: future physics AgentJob missing forbidden_source_classes {missing}"
        )

    for item in _listish_values(job_contract.get("allowed_write_paths", [])):
        normalized = item.strip().lstrip("./")
        if any(normalized.startswith(prefix) for prefix in PHYSICS_JOB_FORBIDDEN_WRITE_PREFIXES):
            report.error(
                f"{path_text}: future physics AgentJob may not allow direct write path {item}"
            )


def _listish_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return split_semicolon(value)
    return []


def _has_substantive_value(value: Any) -> bool:
    return any(item.strip().lower() not in {"", "none"} for item in _listish_values(value))


def _protected_authority_expansions(value: Any) -> list[str]:
    protected: list[str] = []
    for item in _listish_values(value):
        lowered = item.strip().lower()
        if lowered in {"", "none"}:
            continue
        if any(marker in lowered for marker in PROTECTED_AUTHORITY_MARKERS):
            protected.append(item)
    return protected


def _path_allowed_by_patterns(path_text: str, patterns: list[str]) -> bool:
    normalized = path_text.strip().lstrip("./")
    return any(_path_matches(normalized, pattern.strip().lstrip("./")) for pattern in patterns)


def _parent_child_authority_keys(value: Any, prefix: str = "role_decomposition") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}"
            if str(key) in PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS:
                found.append(child_prefix)
            found.extend(_parent_child_authority_keys(child, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_parent_child_authority_keys(child, f"{prefix}[{index}]"))
    return found


def _validate_decomposition_path(
    report: ValidationReport,
    *,
    path_text: str,
    owner_path: str,
    field_name: str,
    allowed_patterns: list[str],
) -> None:
    if not path_text:
        report.error(f"{owner_path}: role_decomposition.{field_name} is required")
        return
    reason = validate_relative_path(path_text)
    if reason:
        report.error(f"{owner_path}: invalid role_decomposition.{field_name}: {reason}")
        return
    if not _path_allowed_by_patterns(path_text, allowed_patterns):
        report.error(
            f"{owner_path}: role_decomposition.{field_name} is outside AgentJob allowlist: {path_text}"
        )


def _nonnegative_int(value: Any) -> int | None:
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, str) and value.strip().isdigit():
        parsed = int(value.strip())
        return parsed if parsed >= 0 else None
    return None


def _parent_child_job_paths(decomposition: dict[str, Any]) -> dict[str, str]:
    paths: dict[str, str] = {}
    children = decomposition.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                unit_id = str(child.get("execution_unit_id", "")).strip()
                output_path = str(child.get("output_path", "")).strip()
                if unit_id and output_path:
                    paths[f"children.{unit_id}.output_path"] = output_path
    conflict_policy = decomposition.get("conflict_policy", {})
    if isinstance(conflict_policy, dict):
        review_path = str(conflict_policy.get("review_path", "")).strip()
        if review_path:
            paths["conflict_policy.review_path"] = review_path
    fusion_policy = decomposition.get("fusion_policy", {})
    if isinstance(fusion_policy, dict):
        fusion_notes_path = str(fusion_policy.get("fusion_notes_path", "")).strip()
        if fusion_notes_path:
            paths["fusion_policy.fusion_notes_path"] = fusion_notes_path
        fused_output_path = str(fusion_policy.get("fused_output_path", "")).strip()
        if fused_output_path:
            paths["fusion_policy.fused_output_path"] = fused_output_path
    return paths


def validate_parent_child_decomposition(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
) -> None:
    decomposition = job_contract.get("role_decomposition")
    if decomposition in (None, "", []):
        return
    owner_path = job_row.get("job_path", job_row.get("job_id", "AgentJob"))
    if not isinstance(decomposition, dict):
        report.error(f"{owner_path}: role_decomposition must be a map")
        return

    if str(decomposition.get("mode", "")).strip() != PARENT_CHILD_SYNTHESIS_MODE:
        report.error(
            f"{owner_path}: role_decomposition.mode must be {PARENT_CHILD_SYNTHESIS_MODE}"
        )
    if str(decomposition.get("decomposition_version", "")).strip() != PARENT_CHILD_SYNTHESIS_VERSION:
        report.error(
            f"{owner_path}: role_decomposition.decomposition_version must be {PARENT_CHILD_SYNTHESIS_VERSION}"
        )

    authority_keys = _parent_child_authority_keys(decomposition)
    if authority_keys:
        report.error(
            f"{owner_path}: role_decomposition may not declare authority fields {sorted(authority_keys)}"
        )

    parent = decomposition.get("parent")
    if not isinstance(parent, dict):
        report.error(f"{owner_path}: role_decomposition.parent must be a map")
    else:
        if str(parent.get("execution_unit_id", "")).strip() != PARENT_CHILD_PARENT_UNIT_ID:
            report.error(
                f"{owner_path}: parent execution_unit_id must be {PARENT_CHILD_PARENT_UNIT_ID}"
            )
        if str(parent.get("perspective", "")).strip() != PARENT_CHILD_PARENT_PERSPECTIVE:
            report.error(
                f"{owner_path}: parent perspective must be {PARENT_CHILD_PARENT_PERSPECTIVE}"
            )

    children = decomposition.get("children")
    seen_children: dict[str, str] = {}
    if not isinstance(children, list) or len(children) != 2:
        report.error(f"{owner_path}: role_decomposition.children must contain exactly two children")
    else:
        for child in children:
            if not isinstance(child, dict):
                report.error(f"{owner_path}: role_decomposition.children entries must be maps")
                continue
            unit_id = str(child.get("execution_unit_id", "")).strip()
            perspective = str(child.get("perspective", "")).strip()
            expected_perspective = PARENT_CHILD_REQUIRED_CHILDREN.get(unit_id)
            if expected_perspective is None:
                report.error(f"{owner_path}: unsupported child execution_unit_id {unit_id}")
            elif perspective != expected_perspective:
                report.error(
                    f"{owner_path}: child {unit_id} perspective must be {expected_perspective}"
                )
            output_path = str(child.get("output_path", "")).strip()
            if not output_path:
                report.error(f"{owner_path}: child {unit_id} output_path is required")
            seen_children[unit_id] = perspective
        missing = sorted(set(PARENT_CHILD_REQUIRED_CHILDREN) - set(seen_children))
        if missing:
            report.error(f"{owner_path}: role_decomposition missing children {missing}")

    conflict_policy = decomposition.get("conflict_policy")
    if not isinstance(conflict_policy, dict):
        report.error(f"{owner_path}: role_decomposition.conflict_policy must be a map")
    else:
        if "review_path" not in conflict_policy:
            report.error(f"{owner_path}: conflict_policy.review_path is required")
        max_rounds = _nonnegative_int(conflict_policy.get("max_resolution_rounds"))
        if max_rounds is None:
            report.error(f"{owner_path}: conflict_policy.max_resolution_rounds must be a nonnegative integer")
        if conflict_policy.get("require_parallel_child_revision") is not True:
            report.error(f"{owner_path}: conflict_policy.require_parallel_child_revision must be true")
        if str(conflict_policy.get("unresolved_conflict_status", "")).strip() != "blocked":
            report.error(f"{owner_path}: conflict_policy.unresolved_conflict_status must be blocked")

    fusion_policy = decomposition.get("fusion_policy")
    fused_output_path = ""
    if not isinstance(fusion_policy, dict):
        report.error(f"{owner_path}: role_decomposition.fusion_policy must be a map")
    else:
        if "fusion_notes_path" not in fusion_policy:
            report.error(f"{owner_path}: fusion_policy.fusion_notes_path is required")
        fused_output_path = str(fusion_policy.get("fused_output_path", "")).strip()
        if not fused_output_path:
            report.error(f"{owner_path}: fusion_policy.fused_output_path is required")
        for field_name in [
            "preserve_shared_consensus",
            "preserve_unique_contributions",
            "preserve_unresolved_limitations",
            "final_output_replaces_old_single_role_artifact",
        ]:
            if fusion_policy.get(field_name) is not True:
                report.error(f"{owner_path}: fusion_policy.{field_name} must be true")

    allowed_patterns = _listish_values(job_contract.get("allowed_write_paths", []))
    if not allowed_patterns:
        report.error(f"{owner_path}: role_decomposition requires AgentJob allowed_write_paths")
    for field_name, path_text in _parent_child_job_paths(decomposition).items():
        _validate_decomposition_path(
            report,
            path_text=path_text,
            owner_path=owner_path,
            field_name=field_name,
            allowed_patterns=allowed_patterns,
        )

    expected_outputs = set(_listish_values(job_contract.get("expected_outputs", [])))
    registry_outputs = set(split_semicolon(job_row.get("output_paths", "")))
    if fused_output_path:
        if fused_output_path not in expected_outputs:
            report.error(
                f"{owner_path}: fusion_policy.fused_output_path must appear in expected_outputs"
            )
        if fused_output_path not in registry_outputs:
            report.error(
                f"{owner_path}: fusion_policy.fused_output_path must appear in AGENT_JOB_REGISTRY output_paths"
            )


def _completion_child_outputs_by_id(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        return {}
    by_unit: dict[str, dict[str, Any]] = {}
    for item in value:
        if isinstance(item, dict):
            unit_id = str(item.get("execution_unit_id", "")).strip()
            if unit_id:
                by_unit[unit_id] = item
    return by_unit


def _has_unresolved_blocking_conflict(conflict_review: dict[str, Any]) -> bool:
    status = str(conflict_review.get("status", "")).strip()
    if status in {"blocked", "unresolved_blocking"}:
        return True
    conflicts = conflict_review.get("unresolved_conflicts", [])
    if not isinstance(conflicts, list):
        return False
    for conflict in conflicts:
        if isinstance(conflict, str) and conflict.strip():
            return True
        if isinstance(conflict, dict) and str(conflict.get("severity", "")).strip() == "blocking":
            return True
    return False


def validate_parent_child_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    decomposition = job_contract.get("role_decomposition")
    if not isinstance(decomposition, dict):
        return
    path_text = path.relative_to(REPO_ROOT).as_posix()
    synthesis = completion.get("parent_child_synthesis")
    if not isinstance(synthesis, dict):
        report.error(f"{path_text}: parent-child AgentJob completion missing parent_child_synthesis")
        return
    if str(synthesis.get("mode", "")).strip() != PARENT_CHILD_SYNTHESIS_MODE:
        report.error(f"{path_text}: parent_child_synthesis.mode must be {PARENT_CHILD_SYNTHESIS_MODE}")
    if str(synthesis.get("decomposition_version", "")).strip() != PARENT_CHILD_SYNTHESIS_VERSION:
        report.error(
            f"{path_text}: parent_child_synthesis.decomposition_version must be {PARENT_CHILD_SYNTHESIS_VERSION}"
        )

    job_children = {
        str(child.get("execution_unit_id", "")).strip(): child
        for child in decomposition.get("children", [])
        if isinstance(child, dict)
    }
    completion_children = _completion_child_outputs_by_id(synthesis.get("child_outputs"))
    if set(completion_children) != set(PARENT_CHILD_REQUIRED_CHILDREN):
        report.error(
            f"{path_text}: parent_child_synthesis.child_outputs must name exactly {sorted(PARENT_CHILD_REQUIRED_CHILDREN)}"
        )
    for unit_id, expected_perspective in PARENT_CHILD_REQUIRED_CHILDREN.items():
        child = completion_children.get(unit_id)
        job_child = job_children.get(unit_id, {})
        if not child:
            continue
        if str(child.get("perspective", "")).strip() != expected_perspective:
            report.error(f"{path_text}: child output {unit_id} perspective must be {expected_perspective}")
        if str(child.get("output_path", "")).strip() != str(job_child.get("output_path", "")).strip():
            report.error(f"{path_text}: child output {unit_id} path must match AgentJob role_decomposition")
        if completion.get("validation_status") == "PASS" and str(child.get("status", "")).strip() != "completed":
            report.error(f"{path_text}: PASS parent-child completion requires child {unit_id} status completed")

    conflict_review = synthesis.get("conflict_review")
    if not isinstance(conflict_review, dict):
        report.error(f"{path_text}: parent_child_synthesis.conflict_review must be a map")
    else:
        status = str(conflict_review.get("status", "")).strip()
        if status not in PARENT_CHILD_CONFLICT_STATUSES:
            report.error(f"{path_text}: conflict_review.status is not allowed: {status}")
        job_review_path = str(
            decomposition.get("conflict_policy", {}).get("review_path", "")
            if isinstance(decomposition.get("conflict_policy"), dict)
            else ""
        ).strip()
        if str(conflict_review.get("review_path", "")).strip() != job_review_path:
            report.error(f"{path_text}: conflict_review.review_path must match AgentJob role_decomposition")
        rounds = _nonnegative_int(conflict_review.get("resolution_rounds"))
        max_rounds = _nonnegative_int(
            decomposition.get("conflict_policy", {}).get("max_resolution_rounds")
            if isinstance(decomposition.get("conflict_policy"), dict)
            else None
        )
        if rounds is None:
            report.error(f"{path_text}: conflict_review.resolution_rounds must be a nonnegative integer")
        elif max_rounds is not None and rounds > max_rounds:
            report.error(f"{path_text}: conflict_review.resolution_rounds exceeds AgentJob max_resolution_rounds")
        for conflict in conflict_review.get("unresolved_conflicts", []):
            if not isinstance(conflict, dict):
                continue
            conflict_type = str(conflict.get("type", "")).strip()
            severity = str(conflict.get("severity", "")).strip()
            if conflict_type and conflict_type not in PARENT_CHILD_CONFLICT_TYPES:
                report.error(f"{path_text}: unresolved conflict type is not allowed: {conflict_type}")
            if severity and severity not in PARENT_CHILD_CONFLICT_SEVERITIES:
                report.error(f"{path_text}: unresolved conflict severity is not allowed: {severity}")
        if completion.get("validation_status") == "PASS" and _has_unresolved_blocking_conflict(conflict_review):
            report.error(f"{path_text}: PASS parent-child completion may not contain unresolved blocking conflicts")

    fusion = synthesis.get("fusion")
    fusion_policy = decomposition.get("fusion_policy", {})
    fused_output_path = (
        str(fusion_policy.get("fused_output_path", "")).strip()
        if isinstance(fusion_policy, dict)
        else ""
    )
    if not isinstance(fusion, dict):
        report.error(f"{path_text}: parent_child_synthesis.fusion must be a map")
    else:
        if str(fusion.get("fused_output_path", "")).strip() != fused_output_path:
            report.error(f"{path_text}: fusion.fused_output_path must match AgentJob role_decomposition")
        completion_outputs = set(_listish_values(completion.get("output_paths", [])))
        if completion.get("validation_status") == "PASS" and fused_output_path not in completion_outputs:
            report.error(f"{path_text}: fused output path must appear in completion.output_paths")


def validate_execution_roles(
    report: ValidationReport,
    execution_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
    jobs: dict[str, dict[str, str]],
    tasks: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    executions = existing_by_id(execution_rows, "execution_role_ref")
    jobs_to_execution_refs: dict[str, list[str]] = {}
    for row in execution_rows:
        execution_ref = row["execution_role_ref"]
        kind = row["role_execution_kind"]
        if kind not in ROLE_EXECUTION_KINDS:
            report.error(f"{execution_ref}: invalid role_execution_kind {kind}")
        reason = validate_relative_path(row["record_path"])
        if reason:
            report.error(f"{execution_ref}: invalid record_path: {reason}")
            continue
        path = repo_path(row["record_path"])
        if not path.exists():
            report.error(f"{execution_ref}: missing execution-role record {row['record_path']}")
            continue
        try:
            record = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{row['record_path']}: {exc}")
            continue
        for field_name in [
            "execution_role_ref",
            "role_execution_kind",
            "task_id",
            "agent_job_id",
            "base_role_id",
            "base_role_version",
            "provisional_role_name",
            "authority_delta_summary",
            "requires_human_gate",
            "expires_after",
            "justification",
            "non_reusable_until_registered",
        ]:
            if _frontmatter_value(record.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['record_path']}: {field_name} does not match ROLE_EXECUTION_REGISTRY.csv"
                )
        for field_name in [
            "allowed_write_paths",
            "added_constraints",
            "removed_permissions",
            "expanded_permissions",
        ]:
            if _frontmatter_value(record.get(field_name, [])) != row[field_name]:
                report.error(
                    f"{row['record_path']}: {field_name} does not match ROLE_EXECUTION_REGISTRY.csv"
                )
        if row["task_id"] not in tasks:
            report.error(f"{execution_ref}: task_id is not registered")
        job = jobs.get(row["agent_job_id"])
        if not job:
            report.error(f"{execution_ref}: agent_job_id is not registered")
        elif job["task_id"] != row["task_id"]:
            report.error(f"{execution_ref}: task_id does not match AgentJob task_id")
        jobs_to_execution_refs.setdefault(row["agent_job_id"], []).append(execution_ref)

        for item in _listish_values(record.get("allowed_write_paths", [])):
            reason = validate_relative_path(item.replace("**", "x").replace("*", "x"))
            if reason:
                report.error(f"{row['record_path']}: invalid allowed_write_paths entry {item}: {reason}")

        if kind in {"registered_role", "task_overlay"}:
            base_role = row["base_role_id"]
            base_role_ref = role_key(base_role, row["base_role_version"])
            if not base_role:
                report.error(f"{execution_ref}: {kind} requires base_role_id")
            elif base_role_ref not in roles:
                report.error(f"{execution_ref}: base_role_id is not registered")
        if kind == "registered_role":
            if _has_substantive_value(record.get("expanded_permissions", [])):
                report.error(f"{execution_ref}: registered_role may not expand permissions")
            if row["non_reusable_until_registered"] != "false":
                report.error(f"{execution_ref}: registered_role must be reusable")
        if kind == "task_overlay":
            if not _has_substantive_value(record.get("added_constraints", [])) and not _has_substantive_value(
                record.get("removed_permissions", [])
            ) and not _has_substantive_value(record.get("expanded_permissions", [])):
                report.error(f"{execution_ref}: task_overlay must declare an authority delta")
            protected = _protected_authority_expansions(record.get("expanded_permissions", []))
            if protected and row["requires_human_gate"] != "true":
                report.error(
                    f"{execution_ref}: protected expanded_permissions require a human gate"
                )
        if kind == "one_job_provisional_role":
            base_role = row["base_role_id"]
            base_version = row["base_role_version"]
            if bool(base_role) != bool(base_version):
                report.error(
                    f"{execution_ref}: provisional role base_role_id and base_role_version must be provided together"
                )
            elif base_role:
                base_role_ref = role_key(base_role, base_version)
                if base_role_ref not in roles:
                    report.error(f"{execution_ref}: provisional base_role_id is not registered")
            if not row["provisional_role_name"]:
                report.error(f"{execution_ref}: provisional role requires provisional_role_name")
            if not row["justification"]:
                report.error(f"{execution_ref}: provisional role requires justification")
            if row["non_reusable_until_registered"] != "true":
                report.error(f"{execution_ref}: provisional role must be non-reusable until registered")
            if row["expires_after"] != row["agent_job_id"]:
                report.error(f"{execution_ref}: provisional role must expire after its AgentJob")
            protected = _protected_authority_expansions(record.get("expanded_permissions", []))
            if protected and row["requires_human_gate"] != "true":
                report.error(
                    f"{execution_ref}: protected expanded_permissions require a human gate"
                )

    for job_id, job in jobs.items():
        execution_refs = jobs_to_execution_refs.get(job_id, [])
        if len(execution_refs) != 1:
            report.error(f"{job_id}: expected exactly one execution-role record, found {len(execution_refs)}")
            continue
        job_path_text = job.get("job_path", "")
        if not job_path_text:
            continue
        job_path = repo_path(job_path_text)
        if not job_path.exists():
            continue
        try:
            job_contract = load_yaml(job_path)
        except StrictYamlError:
            continue
        execution_role_ref = str(job_contract.get("execution_role_ref", ""))
        if execution_role_ref and execution_role_ref != execution_refs[0]:
            report.error(f"{job_path_text}: execution_role_ref does not match ROLE_EXECUTION_REGISTRY.csv")
        if not execution_role_ref and job["status"] in {"pending", "active"}:
            report.error(f"{job_path_text}: pending or active AgentJob must declare execution_role_ref")
    return executions


def validate_completion(report: ValidationReport, job_row: dict[str, str], path: Path) -> None:
    try:
        completion = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
        return
    expected_id = f"AJC-{job_row['job_id']}"
    if str(completion.get("completion_id", "")) != expected_id:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: completion_id must be {expected_id}")
    if str(completion.get("job_id", "")) != job_row["job_id"]:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: job_id mismatch")
    command_results = completion.get("command_results", [])
    if not isinstance(command_results, list) or not command_results:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: missing command_results")

    job_path_text = job_row.get("job_path", "")
    if not job_path_text:
        return
    try:
        job_contract = load_yaml(repo_path(job_path_text))
    except StrictYamlError as exc:
        report.error(f"{job_path_text}: {exc}")
        return
    validate_parent_child_completion(report, job_row, job_contract, completion, path)
    validate_loop_control_completion(report, job_row, job_contract, completion, path)
    validate_completion_resolver_snapshots(report, completion, job_contract, path)


def validate_loop_control_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    role_id = job_row.get("role_id", "")
    if role_id not in PHYSICS_ROLE_IDS:
        return
    if not job_policy_active(job_row, completion):
        return

    path_text = path.relative_to(REPO_ROOT).as_posix()
    validate_distance_to_gr_status(report, completion, path_text)

    if role_id == "refuter" and "stress" in text_blob(job_contract, completion):
        validate_refuter_loop_decision(report, job_row, completion, path_text)
    if role_id == "ontology-formalizer":
        validate_ontology_formalizer_payload(report, completion, path_text)
    if role_id == "candidate-constructor" and any(
        marker in text_blob(job_contract, completion)
        for marker in ("bridge", "observer-readout", "observer readout", "([n]_u", "g_eff")
    ):
        validate_candidate_bridge_attempt(report, completion, path_text)
    if role_id == "theoretical-continuation-selector":
        validate_theoretical_continuation_decision(report, completion, path_text)


def validate_distance_to_gr_status(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    matrix = completion.get("distance_to_gr_status")
    if not isinstance(matrix, list) or not matrix:
        report.error(f"{path_text}: future physics completion missing distance_to_gr_status matrix")
        return

    seen: dict[str, str] = {}
    for item in matrix:
        if not isinstance(item, dict):
            report.error(f"{path_text}: distance_to_gr_status entries must be maps")
            continue
        burden = str(item.get("burden", "")).strip()
        status = str(item.get("status", "")).strip()
        if not burden or not status:
            report.error(f"{path_text}: distance_to_gr_status entries require burden and status")
            continue
        seen[burden] = status
    missing = [burden for burden in DISTANCE_TO_GR_REQUIRED_BURDENS if burden not in seen]
    if missing:
        report.error(f"{path_text}: distance_to_gr_status missing burdens {missing}")


def validate_refuter_loop_decision(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    decision = completion.get("loop_risk_decision")
    if not isinstance(decision, dict):
        report.error(f"{path_text}: Refuter stress completion missing loop_risk_decision")
        return
    category = str(decision.get("category", "")).strip()
    next_route = str(decision.get("next_route", "")).strip()
    rationale = str(decision.get("rationale", "")).strip()
    if category not in LOOP_RISK_DECISION_CATEGORIES:
        report.error(f"{path_text}: loop_risk_decision.category is not registered: {category}")
    future_pause_policy = theoretical_continuation_policy_active(job_row, completion)
    allowed_bridge_routes = set(BRIDGE_OR_FAIL_ROUTES)
    if not future_pause_policy:
        allowed_bridge_routes |= LEGACY_BRIDGE_OR_FAIL_ROUTES
    allowed_routes = allowed_bridge_routes | LOOP_RISK_SUCCESS_ROUTES
    if next_route not in allowed_routes:
        report.error(f"{path_text}: loop_risk_decision.next_route is not allowed: {next_route}")
    if not rationale:
        report.error(f"{path_text}: loop_risk_decision.rationale is required")
    if future_pause_policy and next_route in LEGACY_BRIDGE_OR_FAIL_ROUTES:
        report.error(
            f"{path_text}: future physics routing may not use generic controlled_pause; "
            "use theoretical_decision_role_selection or human_gated_ontology_change_required"
        )
    next_text = text_blob(completion.get("next_recommendation", ""), decision)
    if next_route == "human_gated_ontology_change_required":
        if "ontology" not in next_text or not any(marker in next_text for marker in ("human", "gate")):
            report.error(
                f"{path_text}: human_gated_ontology_change_required requires ontology and human-gate rationale"
            )
    if next_route == "theoretical_decision_role_selection" and not any(
        marker in next_text for marker in THEORETICAL_DECISION_TEXT_MARKERS
    ):
        report.error(
            f"{path_text}: theoretical_decision_role_selection requires a concrete theoretical payload marker"
        )

    if category == "repeated_unmet_burdens_no_new_payload":
        burdens = _listish_values(decision.get("repeated_burdens", []))
        if not burdens:
            report.error(f"{path_text}: repeated burden decisions must list repeated_burdens")
    if category == "scoped_obstruction" and not str(decision.get("obstruction_summary", "")).strip():
        report.error(f"{path_text}: scoped_obstruction decisions require obstruction_summary")
    if category in {"repeated_unmet_burdens_no_new_payload", "scoped_obstruction"}:
        if next_route not in allowed_bridge_routes:
            report.error(
                f"{path_text}: {category} must route through bridge_or_fail escalation"
            )
        if (
            "ontology formalizer" in next_text
            and any(marker in next_text for marker in ("obligation packet", "generic repair", "repair packet"))
            and not any(marker in next_text for marker in ONTOLOGY_PAYLOAD_TEXT_MARKERS)
        ):
            report.error(
                f"{path_text}: bridge_or_fail escalation may not route to a generic Ontology Formalizer packet"
            )


def validate_ontology_formalizer_payload(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    payloads = completion.get("new_mathematical_payload")
    if not isinstance(payloads, list) or not payloads:
        report.error(f"{path_text}: Ontology Formalizer completion missing new_mathematical_payload")
        return
    accepted = False
    for item in payloads:
        if not isinstance(item, dict):
            report.error(f"{path_text}: new_mathematical_payload entries must be maps")
            continue
        payload_type = str(item.get("payload_type", item.get("type", ""))).strip()
        summary = str(item.get("summary", "")).strip()
        if payload_type not in ONTOLOGY_FORMALIZER_PAYLOAD_TYPES:
            report.error(f"{path_text}: unsupported new_mathematical_payload type {payload_type}")
        elif summary:
            accepted = True
        else:
            report.error(f"{path_text}: new_mathematical_payload entries require summary")
    if not accepted:
        report.error(f"{path_text}: Ontology Formalizer completion has no accepted new mathematical payload")


def validate_candidate_bridge_attempt(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    bridge = completion.get("bridge_attempt_status")
    if not isinstance(bridge, dict):
        report.error(f"{path_text}: Candidate Constructor bridge completion missing bridge_attempt_status")
        return
    candidate_map = str(bridge.get("candidate_map", "")).strip()
    missing_primitive = str(bridge.get("missing_primitive", "")).strip()
    preserves_blocks = str(bridge.get("preserves_blocks", "")).strip()
    if not candidate_map and not missing_primitive:
        report.error(
            f"{path_text}: bridge_attempt_status requires candidate_map or missing_primitive"
        )
    if not preserves_blocks:
        report.error(f"{path_text}: bridge_attempt_status.preserves_blocks is required")


def validate_theoretical_continuation_decision(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    decision = completion.get("theoretical_decision_output")
    if not isinstance(decision, dict):
        report.error(f"{path_text}: theoretical-continuation-selector completion missing theoretical_decision_output")
        return
    packet_type = str(decision.get("selected_next_packet_type", "")).strip()
    basis = str(decision.get("decision_basis", "")).strip()
    method = str(decision.get("theoretical_method", "")).strip()
    preserves_blocks = str(decision.get("preserves_claim_blocks", "")).strip()
    requires_human_gate = bool_value(decision.get("requires_human_gate", False))
    human_gate_reason = str(decision.get("human_gate_reason", "")).strip()

    if packet_type not in THEORETICAL_DECISION_PACKET_TYPES:
        report.error(
            f"{path_text}: theoretical_decision_output.selected_next_packet_type is not allowed: {packet_type}"
        )
    if not basis:
        report.error(f"{path_text}: theoretical_decision_output.decision_basis is required")
    if not method:
        report.error(f"{path_text}: theoretical_decision_output.theoretical_method is required")
    if not preserves_blocks:
        report.error(f"{path_text}: theoretical_decision_output.preserves_claim_blocks is required")
    if packet_type == "human_gated_ontology_change_required":
        gate_text = text_blob(decision)
        if not requires_human_gate:
            report.error(
                f"{path_text}: human-gated ontology decision must set requires_human_gate true"
            )
        if "ontology" not in gate_text or not any(marker in gate_text for marker in ("human", "gate")):
            report.error(
                f"{path_text}: human-gated ontology decision requires ontology and human-gate rationale"
            )
        if not human_gate_reason:
            report.error(
                f"{path_text}: human-gated ontology decision requires human_gate_reason"
            )
    elif requires_human_gate:
        report.error(
            f"{path_text}: theoretical continuation decisions may require a human gate only for ontology-change authority"
        )


def validate_completion_resolver_snapshots(
    report: ValidationReport,
    completion: dict[str, Any],
    job_contract: dict[str, Any],
    path: Path,
) -> None:
    if not bool_value(job_contract.get("resolves_signal_routing", False)):
        return
    path_text = path.relative_to(REPO_ROOT).as_posix()
    routing_delta_summary = completion.get("routing_delta_summary", "")
    if not isinstance(routing_delta_summary, str) or not routing_delta_summary.strip():
        report.error(f"{path_text}: routing-resolution completion missing routing_delta_summary")
    snapshots = completion.get("resolver_snapshots")
    if not isinstance(snapshots, dict):
        report.error(
            f"{path_text}: routing-resolution completion must declare resolver_snapshots.before and resolver_snapshots.after"
        )
        return
    for key in ["before", "after"]:
        value = snapshots.get(key, "")
        if not isinstance(value, str) or not value.strip():
            report.error(f"{path_text}: routing-resolution completion missing resolver_snapshots.{key}")
            continue
        reason = validate_relative_path(value)
        if reason:
            report.error(f"{path_text}: invalid resolver_snapshots.{key}: {reason}")
            continue
        snapshot_path = repo_path(value)
        if snapshot_path.suffix != ".json":
            report.error(f"{path_text}: resolver_snapshots.{key} must point to a .json file: {value}")
            continue
        if not snapshot_path.exists():
            report.error(f"{path_text}: resolver_snapshots.{key} path does not exist: {value}")
            continue
        validate_resolver_snapshot_json(report, path_text, key, snapshot_path)


def validate_resolver_snapshot_json(
    report: ValidationReport,
    completion_path_text: str,
    key: str,
    snapshot_path: Path,
) -> None:
    try:
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} is not valid JSON: {exc.msg}")
        return
    if not isinstance(data, dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must contain a JSON object")
        return

    for field_name in RESOLVER_SNAPSHOT_REQUIRED_FIELDS:
        if field_name not in data:
            report.error(
                f"{completion_path_text}: resolver_snapshots.{key} missing resolver field {field_name}"
            )
    for field_name in ["status", "boundary", "reason"]:
        if field_name in data and not isinstance(data[field_name], str):
            report.error(
                f"{completion_path_text}: resolver_snapshots.{key} field {field_name} must be a string"
            )
    if data.get("resolver_is_advisory") is not True:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must preserve resolver_is_advisory=true")
    if data.get("hard_checkpoint_gate") is not False:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must preserve hard_checkpoint_gate=false")
    if data.get("checkpoint_gate_source") != "validators":
        report.error(
            f"{completion_path_text}: resolver_snapshots.{key} must preserve checkpoint_gate_source=validators"
        )
    if "selected_signal" in data and not isinstance(data["selected_signal"], dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} selected_signal must be an object")
    if "open_signals" in data and not isinstance(data["open_signals"], list):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} open_signals must be a list")
    if "change_classification" in data and not isinstance(data["change_classification"], dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} change_classification must be an object")


def validate_program_state(report: ValidationReport, tasks: dict[str, dict[str, str]]) -> None:
    path = CONTROL_DIR / "program_state.yaml"
    if not path.exists():
        report.error("missing research_control/program_state.yaml")
        return
    try:
        state = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"research_control/program_state.yaml: {exc}")
        return
    active_task_id = str(state.get("active_task_id", ""))
    if active_task_id and active_task_id not in tasks:
        report.error("program_state.yaml: active_task_id is not registered")
    if "gr_derived" in state:
        report.error("program_state.yaml: bootstrap must not define gr_derived")


def handoff_number(path: Path) -> int | None:
    match = re.fullmatch(r"handoff-(\d{4})\.yaml", path.name)
    return int(match.group(1)) if match else None


def validate_handoffs(
    report: ValidationReport,
    tasks: dict[str, dict[str, str]],
    jobs: dict[str, dict[str, str]],
) -> None:
    handoff_dir = CONTROL_DIR / "handoffs"
    if not handoff_dir.exists():
        report.error("missing research_control/handoffs")
        return
    numbers: list[int] = []
    for yaml_path in sorted(handoff_dir.glob("handoff-*.yaml")):
        number = handoff_number(yaml_path)
        if number is None:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: invalid handoff filename")
            continue
        numbers.append(number)
        md_path = yaml_path.with_suffix(".md")
        if not md_path.exists():
            report.error(f"{yaml_path.name}: missing Markdown mirror")
        try:
            data = load_yaml(yaml_path)
        except StrictYamlError as exc:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        for field_name in ["handoff_id", "created_at", "task_id", "job_id", "completion_path", "next_action"]:
            if not data.get(field_name):
                report.error(f"{yaml_path.name}: missing {field_name}")
        if str(data.get("task_id", "")) not in tasks:
            report.error(f"{yaml_path.name}: task_id is not registered")
        if str(data.get("job_id", "")) and str(data.get("job_id", "")) not in jobs:
            report.error(f"{yaml_path.name}: job_id is not registered")
        if ".local/" in yaml_path.read_text(encoding="utf-8"):
            report.error(f"{yaml_path.name}: tracked handoff YAML must not use .local/ as authority")
        validate_loop_control_handoff(report, data, jobs, yaml_path)
    if numbers and numbers != list(range(min(numbers), max(numbers) + 1)):
        report.error("handoff IDs must be monotonic without gaps")


def validate_loop_control_handoff(
    report: ValidationReport,
    data: dict[str, Any],
    jobs: dict[str, dict[str, str]],
    yaml_path: Path,
) -> None:
    if not timestamp_at_or_after(data.get("created_at", "")):
        return
    job_id = str(data.get("job_id", ""))
    job = jobs.get(job_id, {})
    if job.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return

    path_text = yaml_path.relative_to(REPO_ROOT).as_posix()
    handoff_text = text_blob(data.get("summary", ""), data.get("next_action", ""))
    future_pause_policy = theoretical_continuation_policy_active(job, data)
    route = str(data.get("loop_risk_route", "")).strip()
    if future_pause_policy and route in LEGACY_BRIDGE_OR_FAIL_ROUTES:
        report.error(
            f"{path_text}: future physics handoff may not set loop_risk_route=controlled_pause; "
            "use theoretical_decision_role_selection or human_gated_ontology_change_required"
        )
    if (
        "ontology formalizer" in handoff_text
        and any(marker in handoff_text for marker in ("obligation packet", "generic repair", "repair packet"))
        and not any(marker in handoff_text for marker in ONTOLOGY_PAYLOAD_TEXT_MARKERS)
    ):
        report.error(
            f"{path_text}: future handoff may not route to a generic Ontology Formalizer packet"
        )

    if any(
        marker in handoff_text
        for marker in (
            "same burdens persist",
            "repeated unmet burdens",
            "no new mathematical payload",
            "scoped obstruction",
        )
    ):
        route_markers = (
            "candidate constructor",
            "concrete witness",
            "controlled pause",
            "gate chair",
            "human-gated ontology",
            "human gated ontology",
            "scoped no-go",
            "obstruction",
            "source-side selector",
            "source-side irrelevance",
            "theoretical decision",
            "theoretical-continuation-selector",
        )
        if future_pause_policy:
            route_markers = tuple(
                marker for marker in route_markers if marker != "controlled pause"
            )
        if not any(marker in handoff_text for marker in route_markers):
            report.error(
                f"{path_text}: repeated-burden or obstruction handoff must route through bridge_or_fail escalation"
            )


def validate_approvals(report: ValidationReport, decisions: dict[str, dict[str, str]]) -> None:
    approval_dir = CONTROL_DIR / "approvals"
    if not approval_dir.exists():
        report.error("missing research_control/approvals")
        return
    for path in approval_dir.glob("approval-*.yaml"):
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        decision_id = str(data.get("decision_id", ""))
        if decision_id and decision_id not in decisions:
            report.error(f"{path.name}: decision_id is not registered")


def _safe_claim_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in SAFE_BOUNDARY_MARKERS)


def validate_claim_boundaries(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    for row in claim_rows:
        if row["authority_source_path"]:
            reason = validate_relative_path(row["authority_source_path"])
            if reason:
                report.error(f"{row['claim_boundary_id']}: invalid authority_source_path: {reason}")
            elif not repo_path(row["authority_source_path"]).exists():
                report.error(f"{row['claim_boundary_id']}: missing authority_source_path")


def scan_for_forbidden_claims(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    scan_roots = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / ".agents",
        CONTROL_DIR,
        REPO_ROOT / ".codex" / "skills" / "continue-research",
    ]
    registry_path = REGISTRY_DIR / "CLAIM_BOUNDARY_REGISTRY.csv"
    for root in scan_roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                continue
            relative = path.relative_to(REPO_ROOT).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for phrase in FORBIDDEN_PHRASES:
                    if phrase in line and not _safe_claim_context(line):
                        report.error(f"{relative}:{line_number}: forbidden claim phrase outside boundary context: {phrase}")
    # The registry itself is allowed to contain forbidden phrases in forbidden_claims.
    if registry_path.exists():
        _ = claim_rows


def changed_paths(base_ref: str, staged_only: bool) -> list[str]:
    if staged_only:
        diff_cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", base_ref]
    else:
        diff_cmd = ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref]
    diff = subprocess.run(diff_cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if diff.returncode != 0:
        raise RuntimeError(diff.stderr)
    paths = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    if not staged_only:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if untracked.returncode != 0:
            raise RuntimeError(untracked.stderr)
        paths.extend(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return sorted(set(paths))


def changed_line_numbers_from_diff(diff_text: str) -> set[int]:
    lines: set[int] = set()
    for raw_line in diff_text.splitlines():
        match = HUNK_RE.search(raw_line)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        if count > 0:
            lines.update(range(start, start + count))
    return lines


def changed_line_numbers(path: str, base_ref: str, staged_only: bool) -> set[int]:
    if staged_only:
        command = ["git", "diff", "--cached", "--unified=0", base_ref, "--", path]
    else:
        command = ["git", "diff", "--unified=0", base_ref, "--", path]
    diff = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if diff.returncode != 0:
        return set()
    return changed_line_numbers_from_diff(diff.stdout)


def markdown_authority_by_line(text: str) -> dict[int, str]:
    active = ""
    authorities: dict[int, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        marker = AUTHORITY_MARKER_RE.search(line)
        if marker:
            active = marker.group(1)
        authorities[line_number] = active or "unmarked"
    return authorities


def markdown_authorities_for_changed_lines(
    path_text: str,
    base_ref: str,
    staged_only: bool,
) -> set[str]:
    path = repo_path(path_text)
    if not path.exists() or not path.is_file():
        return {"unmarked"}
    text = path.read_text(encoding="utf-8")
    authorities_by_line = markdown_authority_by_line(text)
    lines = changed_line_numbers(path_text, base_ref, staged_only)
    if lines:
        return {authorities_by_line.get(line_number, "unmarked") for line_number in lines}
    markers = set(AUTHORITY_MARKER_RE.findall(text))
    return markers or {"unmarked"}


def _pattern_is_too_broad(pattern: str) -> bool:
    return (
        pattern in GLOBALLY_BROAD_PATTERNS
        or pattern.startswith("*/")
        or pattern.startswith("**/")
    )


def _path_matches(path: str, pattern: str) -> bool:
    if _pattern_is_too_broad(pattern):
        return False
    return path == pattern or fnmatch.fnmatch(path, pattern)


def is_control_markdown_path(path: str) -> bool:
    return any(_path_matches(path, pattern) for pattern in CONTROL_MARKDOWN_PATTERNS)


def role_execution_row_for_job(job_id: str) -> dict[str, str]:
    try:
        rows = read_csv_rows("ROLE_EXECUTION_REGISTRY.csv")
    except FileNotFoundError:
        return {}
    for row in rows:
        if row.get("agent_job_id") == job_id:
            return row
    return {}


def allows_explanatory_markdown_overlay(job: dict[str, str]) -> bool:
    row = role_execution_row_for_job(job.get("job_id", ""))
    if row.get("role_execution_kind") != "task_overlay":
        return False
    tokens = split_semicolon(row.get("expanded_permissions", ""))
    tokens.extend(split_semicolon(row.get("added_constraints", "")))
    return any("explanatory_markdown" in token for token in tokens)


def validate_markdown_authority_boundaries(
    report: ValidationReport,
    job: dict[str, str],
    paths: Iterable[str],
    base_ref: str,
    staged_only: bool,
) -> None:
    role_id = job.get("role_id", "")
    explanatory_overlay = allows_explanatory_markdown_overlay(job)
    for changed in paths:
        if is_control_markdown_path(changed):
            if role_id == "documentation-curator":
                report.error(f"{changed}: documentation-curator cannot edit control markdown")
            continue
        if changed not in MIXED_MARKDOWN_PATHS:
            continue
        authorities = markdown_authorities_for_changed_lines(changed, base_ref, staged_only)
        if "unmarked" in authorities:
            report.error(f"{changed}: mixed markdown change is outside an authority marker")
        if role_id == "documentation-curator" and "control" in authorities:
            report.error(f"{changed}: documentation-curator cannot edit control-marked section")
        if (
            role_id == "project-control-maintainer"
            and "explanatory" in authorities
            and not explanatory_overlay
        ):
            report.error(
                f"{changed}: project-control-maintainer cannot edit explanatory section without task_overlay explanatory_markdown permission"
            )


def validate_diff(
    report: ValidationReport,
    job_rows: dict[str, dict[str, str]],
    base_ref: str,
    staged_only: bool,
) -> None:
    active_jobs = [row for row in job_rows.values() if row["status"] in {"active", "completed"}]
    if not active_jobs:
        report.error("--check-diff requires an active or completed AgentJob")
        return
    job = sorted(active_jobs, key=lambda row: row["created_at"])[-1]
    allowed = split_semicolon(job["allowed_write_paths"])
    output_paths = split_semicolon(job["output_paths"])
    allowed.extend(output_paths)
    job_path_text = job.get("job_path", "")
    job_path = repo_path(job_path_text) if job_path_text else None
    if job_path and job_path.exists():
        try:
            job_contract = load_yaml(job_path)
        except StrictYamlError as exc:
            report.error(f"{job_path_text}: {exc}")
            job_contract = {}
        generated_paths = job_contract.get("allowed_generated_paths", [])
        if isinstance(generated_paths, list):
            allowed.extend(str(path) for path in generated_paths if str(path))
    try:
        paths = changed_paths(base_ref, staged_only)
    except RuntimeError as exc:
        report.error(str(exc))
        return
    for pattern in allowed:
        if _pattern_is_too_broad(pattern):
            report.error(f"{job['job_id']}: overly broad allowlist pattern {pattern}")
    for changed in paths:
        if changed.startswith(".local/"):
            continue
        if not any(_path_matches(changed, pattern) for pattern in allowed):
            report.error(f"{changed}: changed path is not allowed by {job['job_id']}")
    validate_markdown_authority_boundaries(report, job, paths, base_ref, staged_only)


def validate_all(
    *,
    check_diff: bool = False,
    base_ref: str = "HEAD",
    staged_only: bool = False,
) -> ValidationReport:
    report = ValidationReport()
    validate_registry_columns(report)
    rows_by_registry = {
        name: read_csv_rows(name)
        for name in REGISTRY_COLUMNS
        if (REGISTRY_DIR / name).exists()
    }
    if len(rows_by_registry) != len(REGISTRY_COLUMNS):
        return report
    validate_registry_values(report, rows_by_registry)
    roles = validate_roles(report, rows_by_registry["AGENT_ROLE_REGISTRY.csv"])
    decisions = validate_director_decisions(
        report, rows_by_registry["DIRECTOR_DECISION_REGISTRY.csv"], roles
    )
    jobs = validate_agent_jobs(
        report, rows_by_registry["AGENT_JOB_REGISTRY.csv"], roles, decisions
    )
    tasks = validate_tasks(
        report,
        rows_by_registry["RESEARCH_TASK_REGISTRY.csv"],
        decisions,
        jobs,
    )
    validate_execution_roles(
        report,
        rows_by_registry["ROLE_EXECUTION_REGISTRY.csv"],
        roles,
        jobs,
        tasks,
    )
    validate_program_state(report, tasks)
    validate_handoffs(report, tasks, jobs)
    validate_approvals(report, decisions)
    validate_claim_boundaries(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    scan_for_forbidden_claims(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    if check_diff:
        validate_diff(report, jobs, base_ref, staged_only)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results.")
    parser.add_argument("--check-diff", action="store_true", help="Check current git diff against the latest active/completed AgentJob.")
    parser.add_argument("--staged-only", action="store_true", help="Check staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base ref for --check-diff.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = validate_all(
        check_diff=args.check_diff,
        base_ref=args.base_ref,
        staged_only=args.staged_only,
    )
    if args.json:
        print(json.dumps({"errors": report.errors, "warnings": report.warnings}, indent=2))
    else:
        if report.errors:
            print("Research-control validation failed:")
            for error in report.errors:
                print(f"- {error}")
        else:
            print("Research-control validation passed.")
        for warning in report.warnings:
            print(f"Warning: {warning}")
    return 0 if report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
