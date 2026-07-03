#!/usr/bin/env python3
"""Report operational scientific-payload density from tracked control records."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


PAYLOAD_CLASS_LABELS = {
    "new_definition": "new definition",
    "new_theorem_statement": "new theorem statement",
    "proof_attempt": "proof attempt",
    "proved_theorem": "proved theorem",
    "conditional_theorem": "conditional theorem",
    "countermodel": "countermodel",
    "obstruction": "obstruction",
    "finite_witness": "finite witness",
    "dependency_map_update": "dependency-map update",
    "source_extension_classification": "source-extension classification",
    "route_selector_only": "route selector only",
    "validator_tooling_only": "validator/tooling only",
    "documentation_only": "documentation only",
}

PROCESS_ONLY_CLASSES = {
    "route_selector_only",
    "validator_tooling_only",
    "documentation_only",
}
MATHEMATICAL_PAYLOAD_CLASSES = set(PAYLOAD_CLASS_LABELS) - PROCESS_ONLY_CLASSES


def read_csv_rows(repo_root: Path, registry_name: str) -> list[dict[str, str]]:
    path = repo_root / "registries" / registry_name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_yaml_or_empty(repo_root: Path, path_text: str) -> dict[str, Any]:
    if not path_text:
        return {}
    path = repo_root / path_text
    if not path.exists():
        return {}
    try:
        return load_yaml(path)
    except StrictYamlError:
        return {}


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def first_nonblank(*values: Any, fallback: str = "unknown") -> str:
    for value in values:
        text = text_value(value)
        if text:
            return text
    return fallback


def normalize_family(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_") or "unknown"


def task_phase(task: dict[str, Any], completion: dict[str, Any]) -> str:
    receipt = dict_value(completion.get("implementation_plan_receipt"))
    plan = dict_value(task.get("implementation_plan"))
    return first_nonblank(
        receipt.get("plan_phase_id"),
        plan.get("plan_phase_id"),
        fallback="unknown",
    )


def task_family(row: dict[str, str], task: dict[str, Any], job: dict[str, Any]) -> str:
    return normalize_family(
        first_nonblank(
            task.get("task_type"),
            job.get("route_label"),
            row.get("role_id", ""),
            fallback="unknown",
        )
    )


def milestone(job: dict[str, Any], completion: dict[str, Any]) -> str:
    progress = dict_value(completion.get("physics_progress_status"))
    delta = dict_value(completion.get("distance_to_gr_delta"))
    return first_nonblank(
        progress.get("target_derivation_milestone"),
        delta.get("milestone"),
        job.get("target_derivation_milestone"),
        fallback="none",
    )


def payload_text(item: Any) -> str:
    if isinstance(item, dict):
        fields = [
            "payload_type",
            "type",
            "kind",
            "object_name",
            "claim_status",
            "status",
            "summary",
        ]
        return " ".join(text_value(item.get(field)) for field in fields).lower()
    return text_value(item).lower()


def classify_payload_item(item: Any) -> str:
    text = payload_text(item)
    if "countermodel" in text:
        return "countermodel"
    if "obstruction" in text:
        return "obstruction"
    if "finite" in text or "witness" in text:
        return "finite_witness"
    if "dependency_map_update" in text or "dependency map" in text or "route_elimination" in text:
        return "dependency_map_update"
    if "source_extension" in text and "classification" in text:
        return "source_extension_classification"
    if "packet_selection" in text or "route selection" in text or "selector" in text:
        return "route_selector_only"
    if "definition" in text or "primitive" in text:
        return "new_definition"
    if "proof attempt" in text or "attempt" in text:
        return "proof_attempt"
    if "conditional" in text or "hypotheses" in text:
        return "conditional_theorem"
    if "proof" in text and "theorem" in text:
        return "proved_theorem"
    if "theorem" in text or "lemma" in text or "proposition" in text:
        return "new_theorem_statement"
    return "validator_tooling_only"


def payload_items(completion: dict[str, Any]) -> list[Any]:
    manifest = list_value(completion.get("mathematical_payload_manifest"))
    if manifest:
        return manifest
    return list_value(completion.get("new_mathematical_payload"))


def fallback_class(row: dict[str, str], task: dict[str, Any], job: dict[str, Any], completion: dict[str, Any]) -> str:
    role_id = row.get("role_id", "")
    family = " ".join(
        [
            text_value(task.get("task_type")),
            text_value(job.get("route_label")),
            text_value(dict_value(completion.get("implementation_plan_receipt")).get("implemented_task_scope")),
        ]
    ).lower()

    if role_id == "documentation-curator" or "documentation" in family:
        return "documentation_only"
    if role_id == "theoretical-continuation-selector" or "selector" in family:
        return "route_selector_only"
    if "source_extension_classification" in family or completion.get("source_extension_category"):
        return "source_extension_classification"
    if "dependency_dag" in family or "dependency dag" in family or "dependency map" in family:
        return "dependency_map_update"
    if any(token in family for token in ("countermodel", "witness", "finite")):
        return "finite_witness"
    return "validator_tooling_only"


def class_counts_for_record(
    row: dict[str, str],
    task: dict[str, Any],
    job: dict[str, Any],
    completion: dict[str, Any],
) -> Counter[str]:
    counts: Counter[str] = Counter()
    items = payload_items(completion)
    if items:
        for item in items:
            counts[classify_payload_item(item)] += 1
        return counts
    counts[fallback_class(row, task, job, completion)] += 1
    return counts


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    class_counts: Counter[str] = Counter()
    task_count = len(records)
    mathematical_task_count = 0
    process_only_task_count = 0

    for record in records:
        counts = Counter(record["payload_class_counts"])
        class_counts.update(counts)
        if sum(counts[class_id] for class_id in MATHEMATICAL_PAYLOAD_CLASSES) > 0:
            mathematical_task_count += 1
        else:
            process_only_task_count += 1

    mathematical_items = sum(class_counts[class_id] for class_id in MATHEMATICAL_PAYLOAD_CLASSES)
    process_only_items = sum(class_counts[class_id] for class_id in PROCESS_ONLY_CLASSES)
    classified_items = sum(class_counts.values())
    payload_density = mathematical_items / classified_items if classified_items else 0.0
    task_payload_density = mathematical_task_count / task_count if task_count else 0.0

    return {
        "task_count": task_count,
        "classified_item_count": classified_items,
        "mathematical_payload_item_count": mathematical_items,
        "process_only_item_count": process_only_items,
        "mathematical_payload_task_count": mathematical_task_count,
        "process_only_task_count": process_only_task_count,
        "payload_density": round(payload_density, 6),
        "task_payload_density": round(task_payload_density, 6),
        "payload_class_counts": {key: class_counts.get(key, 0) for key in PAYLOAD_CLASS_LABELS},
    }


def grouped_summary(records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault(record[key], []).append(record)
    return {group: summarize_records(rows) for group, rows in sorted(groups.items())}


def build_record(
    repo_root: Path,
    row: dict[str, str],
    task_rows: dict[str, dict[str, str]],
) -> dict[str, Any]:
    task_id = row.get("task_id", "")
    task_row = task_rows.get(task_id, {})
    task = load_yaml_or_empty(repo_root, f"{task_row.get('task_path', '')}/00_TASK.yaml")
    job = load_yaml_or_empty(repo_root, row.get("job_path", ""))
    completion = load_yaml_or_empty(repo_root, row.get("completion_path", ""))
    counts = class_counts_for_record(row, task, job, completion)
    math_items = sum(counts[class_id] for class_id in MATHEMATICAL_PAYLOAD_CLASSES)
    process_items = sum(counts[class_id] for class_id in PROCESS_ONLY_CLASSES)
    return {
        "task_id": task_id,
        "job_id": row.get("job_id", ""),
        "completion_path": row.get("completion_path", ""),
        "phase": task_phase(task, completion),
        "task_family": task_family(row, task, job),
        "role": first_nonblank(row.get("role_id", ""), fallback="unknown"),
        "milestone": milestone(job, completion),
        "classification": "mathematical_payload" if math_items else "process_only",
        "mathematical_payload_items": math_items,
        "process_only_items": process_items,
        "payload_class_counts": {key: counts.get(key, 0) for key in PAYLOAD_CLASS_LABELS},
    }


def build_report(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    repo_root = Path(repo_root)
    job_rows = [
        row
        for row in read_csv_rows(repo_root, "AGENT_JOB_REGISTRY.csv")
        if row.get("status") == "completed" and row.get("completion_path")
    ]
    task_rows = {
        row.get("task_id", ""): row
        for row in read_csv_rows(repo_root, "RESEARCH_TASK_REGISTRY.csv")
        if row.get("task_id")
    }
    records = [build_record(repo_root, row, task_rows) for row in job_rows]
    records.sort(key=lambda item: (item["phase"], item["task_family"], item["task_id"], item["job_id"]))

    return {
        "schema_id": "scientific_payload_density_metric_report_v1",
        "generated_by": "scripts/research_control/report_scientific_payload_density.py",
        "authority_boundary": {
            "metrics_are_operational_diagnostics_only": True,
            "not_physics_proof": True,
            "physics_claim_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "statement": "Scientific payload density is an operational diagnostic only; it is not physics proof, claim promotion, benchmark promotion, or completed-derivation authority.",
        },
        "payload_class_contract": [
            {
                "class_id": class_id,
                "label": label,
                "process_only": class_id in PROCESS_ONLY_CLASSES,
            }
            for class_id, label in PAYLOAD_CLASS_LABELS.items()
        ],
        "metric_can_report_by": ["phase", "task_family", "role", "milestone"],
        "overall": summarize_records(records),
        "by_phase": grouped_summary(records, "phase"),
        "by_task_family": grouped_summary(records, "task_family"),
        "by_role": grouped_summary(records, "role"),
        "by_milestone": grouped_summary(records, "milestone"),
        "task_rows": records,
    }


def render_markdown(report: dict[str, Any]) -> str:
    boundary = report["authority_boundary"]
    lines = [
        "# Scientific Payload Density Metric",
        "",
        boundary["statement"],
        "",
        "## Overall",
        "",
        f"- Tasks read: {report['overall']['task_count']}",
        f"- Mathematical payload items: {report['overall']['mathematical_payload_item_count']}",
        f"- Process-only items: {report['overall']['process_only_item_count']}",
        f"- Payload density: {report['overall']['payload_density']}",
        f"- Task payload density: {report['overall']['task_payload_density']}",
        "",
        "## Grouping Dimensions",
        "",
    ]
    for key in report["metric_can_report_by"]:
        lines.append(f"- {key}")
    lines.extend(["", "## Authority Boundary", ""])
    lines.append(f"- Operational diagnostics only: {boundary['metrics_are_operational_diagnostics_only']}")
    lines.append(f"- Not physics proof: {boundary['not_physics_proof']}")
    lines.append(f"- Physics claim promotion authorized: {boundary['physics_claim_promotion_authorized']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Repository root to scan.")
    parser.add_argument("--markdown", action="store_true", help="Render Markdown instead of JSON.")
    args = parser.parse_args(argv)

    report = build_report(Path(args.repo_root))
    if args.markdown:
        print(render_markdown(report), end="")
    else:
        json.dump(report, sys.stdout, indent=2, sort_keys=True)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
