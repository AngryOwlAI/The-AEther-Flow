#!/usr/bin/env python3
"""Render generated research-control task indexes from tracked task records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402
import generated_report_provenance as report_provenance  # noqa: E402
import task_taxonomy  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "research_control_task_index_v2"
SCHEMA_PATH = "research_control/design/task_index_schema_v2.md"
TASKS_ROOT = "research_control/tasks"
RESEARCH_TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
AGENT_JOB_REGISTRY_PATH = "registries/AGENT_JOB_REGISTRY.csv"
DIRECTOR_DECISION_REGISTRY_PATH = "registries/DIRECTOR_DECISION_REGISTRY.csv"
AGENT_ROLE_REGISTRY_PATH = "registries/AGENT_ROLE_REGISTRY.csv"
DEFAULT_CSV_PATH = "research_control/tasks/TASK_INDEX.csv"
DEFAULT_MARKDOWN_PATH = "research_control/tasks/TASK_INDEX.md"
DEFAULT_WIKI_MARKDOWN_PATH = "wiki/indexes/research_control_task_index.md"
RENDERER_PATH = "scripts/research_control/render_task_index.py"
RENDERER_SHA256 = report_provenance.sha256_file(REPO_ROOT, RENDERER_PATH)
AUTHORITY_NOTICE = (
    "Generated navigation support only. This index is not task authority, "
    "physics proof authority, benchmark authority, Gate Chair authority, or "
    "completed-derivation evidence."
)
HEADER = [
    "task_id",
    "parent_task_id",
    "created_at",
    "closed_at",
    "title",
    "task_type",
    "work_kind",
    "milestone",
    "candidate_family",
    "result_kind",
    "authority",
    "scope",
    "taxonomy_source",
    "taxonomy_confidence",
    "status",
    "target_derivation_milestone",
    "milestone_burden",
    "role_family",
    "physics_delta",
    "ledger_rows_changed",
    "artifact_count",
    "next_recommended_action",
    "validation_status",
    "completion_path",
]
STATUS_VALUES = {"pending", "active", "completed", "blocked", "human_gated", "superseded"}
CURRENT_INTERNAL_REVIEW_ROLE_ID = "external-red-team-reviewer"
CURRENT_INTERNAL_REVIEW_ROLE_VERSION = "0.1.0"
CURRENT_INTERNAL_REVIEW_ROLE_NAME = "Internal Skeptical Reviewer"
CURRENT_INTERNAL_REVIEW_ROLE_KIND = "scientific_adversarial_internal_review"


class TaskIndexError(RuntimeError):
    """Raised when task-index rendering cannot continue."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def rel_path(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def bool_text(value: Any, default: str = "false") -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = text_value(value).lower()
    if text in {"true", "false"}:
        return text
    return default


def first_text(*values: Any) -> str:
    for value in values:
        text = text_value(value)
        if text:
            return text
    return ""


def md_cell(value: Any) -> str:
    text = text_value(value).replace("\n", " ")
    return text.replace("|", r"\|")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv_rows(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise TaskIndexError(f"missing required CSV source: {rel_path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def load_optional_yaml(repo_root: Path, rel_path: str, issues: list[dict[str, str]]) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        issues.append(issue("missing_source", rel_path, "", "missing structured YAML source"))
        return {}
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        issues.append(issue("malformed_yaml", rel_path, "", str(exc)))
        return {}
    if not isinstance(data, dict):
        issues.append(issue("malformed_yaml", rel_path, "", "top-level YAML value is not a mapping"))
        return {}
    return data


def issue(kind: str, source_path: str, task_id: str, message: str) -> dict[str, str]:
    return {
        "issue_kind": kind,
        "source_path": source_path,
        "task_id": task_id,
        "message": message,
    }


def row_by_key(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    return next((row for row in rows if row.get(key) == value), {})


def rows_by_task(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        task_id = text_value(row.get("task_id"))
        if task_id and task_id not in output:
            output[task_id] = row
    return output


def rows_by_role(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (text_value(row.get("role_id")), text_value(row.get("version"))): row
        for row in rows
        if text_value(row.get("role_id")) and text_value(row.get("version"))
    }


def registry_task_ids(task_registry_rows: list[dict[str, str]]) -> set[str]:
    return {text_value(row.get("task_id")) for row in task_registry_rows if text_value(row.get("task_id"))}


def task_dir_ids(repo_root: Path) -> set[str]:
    root = repo_path(repo_root, TASKS_ROOT)
    if not root.exists():
        return set()
    return {path.name for path in root.iterdir() if path.is_dir() and path.name.startswith("RT-")}


def completion_files(repo_root: Path, task_id: str) -> list[Path]:
    task_root = repo_path(repo_root, f"{TASKS_ROOT}/{task_id}/jobs/completions")
    if not task_root.exists():
        return []
    return sorted(task_root.glob("AJC-*.yaml"))


def artifact_count(repo_root: Path, task_id: str) -> int:
    artifact_root = repo_path(repo_root, f"{TASKS_ROOT}/{task_id}/artifacts")
    if not artifact_root.exists():
        return 0
    return sum(1 for path in artifact_root.rglob("*") if path.is_file())


def normalize_status(raw: str, task_id: str, source_path: str, issues: list[dict[str, str]]) -> str:
    status = raw or "pending"
    if status not in STATUS_VALUES:
        issues.append(issue("invalid_status", source_path, task_id, f"unsupported task status: {status}"))
    return status


def ledger_rows_changed(completion: dict[str, Any]) -> str:
    delta = completion.get("distance_to_gr_delta")
    if not isinstance(delta, dict):
        return "false"
    changed = bool_text(delta.get("ledger_row_updated") or delta.get("changed"))
    if changed != "true":
        return "false"
    burden_id = text_value(delta.get("burden_id") or delta.get("milestone"))
    return burden_id or "true"


def physics_delta(completion: dict[str, Any], task: dict[str, Any]) -> str:
    delta = completion.get("distance_to_gr_delta")
    if isinstance(delta, dict):
        return bool_text(delta.get("changed"))
    return bool_text(task.get("scientific_claims_changed") or task.get("physics_delta"), "false")


def role_family(
    job: dict[str, Any],
    job_registry: dict[str, str],
    task: dict[str, Any],
    role_registry_row: dict[str, str] | None = None,
    *,
    issues: list[dict[str, str]] | None = None,
    task_id: str = "",
    source_path: str = AGENT_ROLE_REGISTRY_PATH,
) -> str:
    role_id = first_text(job.get("role_id"), job_registry.get("role_id"), task.get("role_id"))
    role_version = first_text(job.get("role_version"), job_registry.get("role_version"), task.get("role_version"))
    if role_id and role_version:
        stable_ref = f"{role_id}@{role_version}"
        if (
            role_id == CURRENT_INTERNAL_REVIEW_ROLE_ID
            and role_version == CURRENT_INTERNAL_REVIEW_ROLE_VERSION
        ):
            registry_row = role_registry_row or {}
            if (
                text_value(registry_row.get("role_name")) != CURRENT_INTERNAL_REVIEW_ROLE_NAME
                or text_value(registry_row.get("role_kind")) != CURRENT_INTERNAL_REVIEW_ROLE_KIND
            ):
                if issues is not None:
                    issues.append(
                        issue(
                            "current_review_role_projection_invalid",
                            source_path,
                            task_id,
                            "stable reviewer role ID lacks the exact internal display name and kind",
                        )
                    )
                return f"INTERNAL REVIEW LABEL CONTRACT INVALID [{stable_ref}]"
            return f"{CURRENT_INTERNAL_REVIEW_ROLE_NAME} [{stable_ref}; legacy identifier]"
        return stable_ref
    return role_id


def completion_path_for(
    repo_root: Path,
    task_id: str,
    current_job_id: str,
    job_registry: dict[str, str],
    issues: list[dict[str, str]],
) -> tuple[str, dict[str, Any]]:
    path_text = text_value(job_registry.get("completion_path"))
    if path_text and repo_path(repo_root, path_text).exists():
        return path_text, load_optional_yaml(repo_root, path_text, issues)
    completions = completion_files(repo_root, task_id)
    if completions:
        path = completions[-1]
        path_text = rel_path(repo_root, path)
        return path_text, load_optional_yaml(repo_root, path_text, issues)
    if current_job_id and text_value(job_registry.get("status")) == "completed":
        issues.append(issue("missing_completion", f"{TASKS_ROOT}/{task_id}", task_id, "completed job has no completion record"))
    return "", {}


def source_fingerprint(repo_root: Path, source_paths: list[str], rows: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for rel in sorted(set(source_paths)):
        parts.append(f"{rel}:{file_hash(repo_path(repo_root, rel))}")
    parts.append(json.dumps(rows, sort_keys=True, ensure_ascii=False))
    return sha256_text("\n".join(parts))


def build_index(
    repo_root: Path,
    *,
    source_commit: str | None = None,
    strict_provenance: bool | None = None,
) -> dict[str, Any]:
    if not repo_path(repo_root, SCHEMA_PATH).exists():
        raise TaskIndexError(f"missing task-index schema: {SCHEMA_PATH}")

    issues: list[dict[str, str]] = []
    task_registry_rows = read_csv_rows(repo_root, RESEARCH_TASK_REGISTRY_PATH)
    job_registry_rows = read_csv_rows(repo_root, AGENT_JOB_REGISTRY_PATH)
    decision_registry_rows = read_csv_rows(repo_root, DIRECTOR_DECISION_REGISTRY_PATH)
    role_registry_rows = read_csv_rows(repo_root, AGENT_ROLE_REGISTRY_PATH)
    task_registry = rows_by_task(task_registry_rows)
    role_registry = rows_by_role(role_registry_rows)
    try:
        plan_items = task_taxonomy.load_plan_items(repo_root)
        task_taxonomy.load_policy(repo_root)
    except task_taxonomy.TaskTaxonomyError as exc:
        raise TaskIndexError(str(exc)) from exc
    source_paths = [
        SCHEMA_PATH,
        task_taxonomy.POLICY_PATH,
        task_taxonomy.BACKLOG_PATH,
        RESEARCH_TASK_REGISTRY_PATH,
        AGENT_JOB_REGISTRY_PATH,
        DIRECTOR_DECISION_REGISTRY_PATH,
        AGENT_ROLE_REGISTRY_PATH,
    ]
    task_ids = sorted(registry_task_ids(task_registry_rows) | task_dir_ids(repo_root))
    rows: list[dict[str, str]] = []

    for task_id in task_ids:
        registry_row = task_registry.get(task_id, {})
        task_path = first_text(registry_row.get("task_path"), f"{TASKS_ROOT}/{task_id}")
        task_yaml_path = f"{task_path}/00_TASK.yaml"
        task = load_optional_yaml(repo_root, task_yaml_path, issues)
        source_paths.append(task_yaml_path)

        current_job_id = first_text(task.get("current_job_id"), task.get("job_id"), registry_row.get("current_job_id"))
        job_registry = row_by_key(job_registry_rows, "job_id", current_job_id) if current_job_id else {}
        job_path = first_text(job_registry.get("job_path"), f"{task_path}/jobs/{current_job_id}.yaml" if current_job_id else "")
        job = load_optional_yaml(repo_root, job_path, issues) if job_path else {}
        if job_path:
            source_paths.append(job_path)

        completion_path, completion = completion_path_for(repo_root, task_id, current_job_id, job_registry, issues)
        if completion_path:
            source_paths.append(completion_path)

        decision_id = first_text(task.get("current_decision_id"), task.get("decision_id"), registry_row.get("current_decision_id"))
        decision_row = row_by_key(decision_registry_rows, "decision_id", decision_id) if decision_id else {}
        if decision_row.get("decision_path"):
            source_paths.append(decision_row["decision_path"])

        status = normalize_status(
            first_text(task.get("status"), registry_row.get("status")),
            task_id,
            task_yaml_path,
            issues,
        )
        if registry_row.get("status") and task.get("status") and registry_row.get("status") != task.get("status"):
            issues.append(issue("status_conflict", task_yaml_path, task_id, "00_TASK.yaml and registry status differ"))

        role_id = first_text(job.get("role_id"), job_registry.get("role_id"), task.get("role_id"))
        role_version = first_text(
            job.get("role_version"),
            job_registry.get("role_version"),
            task.get("role_version"),
        )
        taxonomy = task_taxonomy.classify_task(
            task,
            registry_row,
            job,
            role_registry.get((role_id, role_version), {}),
            plan_items.get(task_taxonomy.plan_task_id(task), {}),
        )
        for error in taxonomy["errors"]:
            issues.append(
                issue(
                    "taxonomy_invalid"
                    if isinstance(task.get("task_taxonomy"), dict)
                    else "taxonomy_required_missing",
                    task_yaml_path,
                    task_id,
                    error,
                )
            )

        row = {
            "task_id": task_id,
            "parent_task_id": first_text(task.get("parent_task_id"), registry_row.get("parent_task_id")),
            "created_at": first_text(task.get("created_at"), registry_row.get("created_at")),
            "closed_at": first_text(task.get("closed_at"), registry_row.get("closed_at")),
            "title": taxonomy["title"],
            "task_type": first_text(task.get("task_type"), registry_row.get("task_type")),
            "work_kind": taxonomy["work_kind"],
            "milestone": taxonomy["milestone"],
            "candidate_family": taxonomy["candidate_family"],
            "result_kind": taxonomy["result_kind"],
            "authority": taxonomy["authority"],
            "scope": taxonomy["scope"],
            "taxonomy_source": taxonomy["taxonomy_source"],
            "taxonomy_confidence": taxonomy["taxonomy_confidence"],
            "status": status,
            "target_derivation_milestone": first_text(
                task.get("target_derivation_milestone"),
                job.get("target_derivation_milestone"),
                completion.get("target_derivation_milestone"),
                "none",
            ),
            "milestone_burden": first_text(
                task.get("milestone_burden"),
                job.get("milestone_burden"),
                completion.get("milestone_burden"),
            ),
            "role_family": role_family(
                job,
                job_registry,
                task,
                role_registry.get((role_id, role_version), {}),
                issues=issues,
                task_id=task_id,
            ),
            "physics_delta": physics_delta(completion, task),
            "ledger_rows_changed": ledger_rows_changed(completion),
            "artifact_count": str(artifact_count(repo_root, task_id)),
            "next_recommended_action": first_text(
                task.get("next_recommended_action"),
                completion.get("next_recommendation"),
            ),
            "validation_status": first_text(completion.get("validation_status"), job_registry.get("validation_status"), "not_applicable"),
            "completion_path": completion_path,
        }
        for field in HEADER:
            if field not in row:
                row[field] = ""
        if not row["created_at"]:
            issues.append(issue("missing_field", task_yaml_path, task_id, "created_at is missing"))
        if not row["task_type"]:
            issues.append(issue("missing_field", task_yaml_path, task_id, "task_type is missing"))
        if not row["milestone_burden"]:
            issues.append(issue("missing_field", task_yaml_path, task_id, "milestone_burden is missing"))
        if status == "completed" and current_job_id and not completion_path:
            issues.append(issue("missing_completion", task_yaml_path, task_id, "completed task has a job but no completion path"))
        rows.append(row)

    rows.sort(key=lambda item: (item["created_at"], item["task_id"]), reverse=True)
    latest_timestamp = max((row["created_at"] for row in rows if row["created_at"]), default="")
    source_paths = sorted(set(source_paths))
    source_hashes = {
        path: digest
        for path in source_paths
        if (digest := file_hash(repo_path(repo_root, path)))
    }
    if source_commit is None:
        existing = report_provenance.metadata_from_markdown_file(
            repo_root, DEFAULT_MARKDOWN_PATH
        )
        source_commit = report_provenance.source_commit_from_metadata(
            existing, report_provenance.git_head(repo_root)
        )
    strict = repo_root.resolve() == REPO_ROOT.resolve() if strict_provenance is None else strict_provenance
    provenance = report_provenance.build_metadata(
        report_class="research_task_index",
        source_commit=source_commit,
        source_hashes=source_hashes,
        primary_source_paths=[
            SCHEMA_PATH,
            task_taxonomy.POLICY_PATH,
            task_taxonomy.BACKLOG_PATH,
            RESEARCH_TASK_REGISTRY_PATH,
            AGENT_JOB_REGISTRY_PATH,
            DIRECTOR_DECISION_REGISTRY_PATH,
            AGENT_ROLE_REGISTRY_PATH,
        ],
        generation_time=latest_timestamp,
        task_count=len(rows),
        renderer_path=RENDERER_PATH,
        renderer_sha256=RENDERER_SHA256,
        strict=strict,
    )
    return {
        "schema_id": SCHEMA_ID,
        "generated_at": latest_timestamp,
        "source_paths": source_paths,
        "source_fingerprint": source_fingerprint(repo_root, source_paths, rows),
        "report_provenance": provenance,
        "authority_notice": AUTHORITY_NOTICE,
        "header": HEADER,
        "row_count": len(rows),
        "issue_count": len(issues),
        "issues": issues,
        "rows": rows,
    }


def render_csv(index: dict[str, Any]) -> str:
    from io import StringIO

    handle = StringIO()
    writer = csv.DictWriter(handle, fieldnames=HEADER, lineterminator="\n")
    writer.writeheader()
    for row in index["rows"]:
        writer.writerow({field: row.get(field, "") for field in HEADER})
    return handle.getvalue()


def render_rows_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "|" + "|".join(HEADER) + "|",
        "|" + "|".join("---" for _ in HEADER) + "|",
    ]
    for row in rows:
        lines.append("|" + "|".join(md_cell(row.get(field, "")) for field in HEADER) + "|")
    return "\n".join(lines)


def render_issue_table(issues: list[dict[str, str]]) -> str:
    if not issues:
        return "No missing or malformed task records were detected by the renderer."
    header = ["issue_kind", "task_id", "source_path", "message"]
    lines = [
        "|" + "|".join(header) + "|",
        "|" + "|".join("---" for _ in header) + "|",
    ]
    for item in issues:
        lines.append("|" + "|".join(md_cell(item.get(field, "")) for field in header) + "|")
    return "\n".join(lines)


def render_markdown(index: dict[str, Any], title: str = "Research-Control Task Index") -> str:
    provenance = "\n".join(
        report_provenance.markdown_provenance_lines(index["report_provenance"])
    )
    return (
        f"# {title}\n\n"
        f"{AUTHORITY_NOTICE}\n\n"
        f"{provenance}\n"
        "## Generation Receipt\n\n"
        f"- Schema: `{SCHEMA_ID}`\n"
        f"- Schema source: `{SCHEMA_PATH}`\n"
        f"- Source fingerprint: `{index['source_fingerprint']}`\n"
        f"- Generated-at source timestamp: `{index['generated_at'] or 'none'}`\n"
        f"- Row count: `{index['row_count']}`\n"
        f"- Issue count: `{index['issue_count']}`\n"
        f"- CSV output: `{DEFAULT_CSV_PATH}`\n\n"
        "## Task Rows\n\n"
        f"{render_rows_table(index['rows'])}\n\n"
        "## Missing Or Malformed Records\n\n"
        f"{render_issue_table(index['issues'])}\n"
    )


def rendered_texts(index: dict[str, Any]) -> tuple[str, str, str]:
    csv_text = render_csv(index)
    markdown_text = render_markdown(index, "Research-Control Task Index")
    wiki_markdown_text = render_markdown(index, "Research-Control Task Index")
    return csv_text, markdown_text, wiki_markdown_text


def write_text(repo_root: Path, rel_path: str, text: str) -> None:
    path = repo_path(repo_root, rel_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def compare_text(repo_root: Path, rel_path: str, expected: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    expected_hash = sha256_text(expected)
    if not path.exists():
        return {
            "path": rel_path,
            "fresh": False,
            "status": "missing",
            "actual_hash": "",
            "expected_hash": expected_hash,
        }
    actual = path.read_text(encoding="utf-8")
    actual_hash = sha256_text(actual)
    fresh = actual == expected
    return {
        "path": rel_path,
        "fresh": fresh,
        "status": "fresh" if fresh else "stale",
        "actual_hash": actual_hash,
        "expected_hash": expected_hash,
    }


def status_payload(index: dict[str, Any], output_status: str, checks: dict[str, Any]) -> dict[str, Any]:
    csv_text, markdown_text, wiki_markdown_text = rendered_texts(index)
    return {
        "schema_id": SCHEMA_ID,
        "status": output_status,
        "csv_path": DEFAULT_CSV_PATH,
        "markdown_path": DEFAULT_MARKDOWN_PATH,
        "wiki_markdown_path": DEFAULT_WIKI_MARKDOWN_PATH,
        "csv_sha256": sha256_text(csv_text),
        "markdown_sha256": sha256_text(markdown_text),
        "wiki_markdown_sha256": sha256_text(wiki_markdown_text),
        "row_count": index["row_count"],
        "issue_count": index["issue_count"],
        "source_fingerprint": index["source_fingerprint"],
        "report_provenance": index["report_provenance"],
        "authority_notice": AUTHORITY_NOTICE,
        "artifacts": checks,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write CSV and Markdown task-index outputs")
    mode.add_argument("--check", action="store_true", help="fail if task-index outputs are stale")
    mode.add_argument("--json", action="store_true", help="emit task-index data as JSON")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(args.repo_root).resolve()
    existing_metadata = report_provenance.metadata_from_markdown_file(
        repo_root, DEFAULT_MARKDOWN_PATH
    )
    source_commit = (
        report_provenance.git_head(repo_root)
        if args.write
        else report_provenance.source_commit_from_metadata(
            existing_metadata, report_provenance.git_head(repo_root)
        )
    )
    try:
        index = build_index(repo_root, source_commit=source_commit)
    except (TaskIndexError, report_provenance.GeneratedReportProvenanceError) as exc:
        print(f"render_task_index: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(index, indent=2, sort_keys=True))
        return 0

    csv_text, markdown_text, wiki_markdown_text = rendered_texts(index)
    checks = {
        "csv": compare_text(repo_root, DEFAULT_CSV_PATH, csv_text),
        "markdown": compare_text(repo_root, DEFAULT_MARKDOWN_PATH, markdown_text),
        "wiki_markdown": compare_text(repo_root, DEFAULT_WIKI_MARKDOWN_PATH, wiki_markdown_text),
    }
    provenance_validation = report_provenance.validate_metadata(
        repo_root=repo_root,
        observed=existing_metadata or {},
        expected=index["report_provenance"],
        strict=repo_root == REPO_ROOT,
    )

    if args.write:
        write_text(repo_root, DEFAULT_CSV_PATH, csv_text)
        write_text(repo_root, DEFAULT_MARKDOWN_PATH, markdown_text)
        write_text(repo_root, DEFAULT_WIKI_MARKDOWN_PATH, wiki_markdown_text)
        checks = {
            "csv": compare_text(repo_root, DEFAULT_CSV_PATH, csv_text),
            "markdown": compare_text(repo_root, DEFAULT_MARKDOWN_PATH, markdown_text),
            "wiki_markdown": compare_text(repo_root, DEFAULT_WIKI_MARKDOWN_PATH, wiki_markdown_text),
        }
        written_metadata = report_provenance.metadata_from_markdown_file(
            repo_root, DEFAULT_MARKDOWN_PATH
        ) or {}
        provenance_validation = report_provenance.validate_metadata(
            repo_root=repo_root,
            observed=written_metadata,
            expected=index["report_provenance"],
            strict=repo_root == REPO_ROOT,
        )
        payload = status_payload(index, "written", checks)
        payload["provenance_validation"] = provenance_validation
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    fresh = (
        all(item["fresh"] for item in checks.values())
        and provenance_validation["status"] == "PASS"
    )
    payload = status_payload(index, "pass" if fresh else "stale", checks)
    payload["provenance_validation"] = provenance_validation
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if fresh else 1


if __name__ == "__main__":
    raise SystemExit(main())
