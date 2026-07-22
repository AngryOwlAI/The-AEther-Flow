#!/usr/bin/env python3
"""Render the deterministic v21 P10-T04 attempt-history report."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
LEDGER_PATH = ARTIFACT_DIR / "v21_research_attempt_ledger.json"
REPORT_PATH = ARTIFACT_DIR / "v21_attempt_history_report.md"
VALIDATOR_PATH = ARTIFACT_DIR / "validate_v21_attempt_ledger.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("v21_attempt_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load attempt-history validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render(ledger: dict, metrics: dict) -> str:
    counts = Counter(event["event_type"] for event in ledger["events"])
    failure_count = counts["validation_failed"]
    repair_count = counts["repair_applied"]
    completion_count = counts["completed"]
    supersession_count = counts["superseded"]
    audit_count = counts["audit_finding"]
    historic_compute_missing = sum(
        event["compute_metadata"]["availability"] == "not_recorded"
        for event in ledger["events"]
    )

    lines = [
        "---",
        'authority: "generated-control-report"',
        'task_id: "RT-20260721-006"',
        'plan_task_id: "P10-T04"',
        'status: "draft/control"',
        "---",
        "",
        "# V21 research-attempt and rework report",
        "",
        "## Boundary",
        "",
        "This deterministic report summarizes the task-local, source-linked attempt ledger. Process or review evidence is not physics evidence. The report grants no candidate, ontology, promotion, proof, publication, or completed-derivation authority.",
        "",
        "## Compact receipt",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| Finalized events | {metrics['event_count']} |",
        f"| Source references | {metrics['source_ref_count']} |",
        f"| Validation failures | {failure_count} |",
        f"| Repairs applied | {repair_count} |",
        f"| Audit findings | {audit_count} |",
        f"| Supersessions | {supersession_count} |",
        f"| Completions | {completion_count} |",
        f"| Historic events with compute metadata not recorded | {historic_compute_missing} |",
        f"| Explicit absences | {metrics['explicit_absence_count']} |",
        f"| Privacy findings | {metrics['privacy_finding_count']} |",
        "| Physics results | 0 |",
        "",
        "## Event history",
        "",
        "| Seq. | Event | Task | Domain | Disposition | Related | Source count |",
        "| ---: | --- | --- | --- | --- | --- | ---: |",
    ]
    for event in ledger["events"]:
        related = ", ".join(event["related_event_ids"]) or "none"
        lines.append(
            f"| {event['sequence']} | `{event['event_type']}` | `{event['task_id']}` | `{event['evidence_domain']}` | `{event['disposition']}` | {related} | {len(event['source_refs'])} |"
        )

    lines.extend(
        [
            "",
            "## Explicit absences",
            "",
        ]
    )
    for absence in ledger["explicit_absences"]:
        lines.append(
            f"- `{absence['event_type']}`: {absence['reason']} Scope: {absence['source_search_scope']} No inference was performed."
        )

    lines.extend(
        [
            "",
            "## Rework interpretation",
            "",
            f"The source set records {failure_count} validation failure, {repair_count} applied repairs, {supersession_count} supersession, and {completion_count} completion events. These counts expose process evolution; they do not measure Distance-to-GR progress or scientific truth.",
            "",
            "## Chain receipt",
            "",
            f"- Algorithm: `{ledger['chain_algorithm']}`",
            f"- Revision: `{ledger['revision']}`",
            f"- Final event hash: `{metrics['head_event_hash']}`",
            f"- Preserved `HEAD` prefix events: `{metrics['head_prefix_count']}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        validator = load_validator()
        ledger = validator.load_json(LEDGER_PATH)
        metrics = validator.validate_ledger_data(ledger)
        content = render(ledger, metrics)
        if args.write:
            REPORT_PATH.write_text(content, encoding="utf-8")
        elif not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != content:
            raise RuntimeError("generated attempt-history report is stale")
    except Exception as exc:
        result = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1

    result = {
        "status": "PASS",
        "report_path": REPORT_PATH.relative_to(REPO_ROOT).as_posix(),
        "event_count": metrics["event_count"],
        "head_event_hash": metrics["head_event_hash"],
    }
    print(json.dumps(result, sort_keys=True) if args.json else "PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
