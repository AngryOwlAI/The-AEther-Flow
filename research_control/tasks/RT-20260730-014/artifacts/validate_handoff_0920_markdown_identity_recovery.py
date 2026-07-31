#!/usr/bin/env python3
"""Validate the exact handoff-0920 Markdown identity recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HANDOFF_MD = ROOT / "research_control/handoffs/handoff-0920.md"
HANDOFF_YAML = ROOT / "research_control/handoffs/handoff-0920.yaml"
SOURCE_TASK = ROOT / "research_control/tasks/RT-20260730-013/00_TASK.yaml"
SOURCE_JOB = (
    ROOT
    / "research_control/tasks/RT-20260730-013/jobs/AJ-RT-20260730-013-001.yaml"
)
SOURCE_COMPLETION = (
    ROOT
    / "research_control/tasks/RT-20260730-013/jobs/completions/"
    "AJC-AJ-RT-20260730-013-001.yaml"
)
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260730-014/artifacts/"
    "handoff_0920_markdown_identity_recovery_receipt.json"
)

BEFORE_HEADING = "# Handoff 0920 — P9-T06 finite radiative case"
AFTER_HEADING = "# Handoff handoff-0920 — P9-T06 finite radiative case"
BEFORE_SHA256 = "1385b646fca4fd79a453811d4de22f97946c992e074b965db6641050bc603ca1"
AFTER_SHA256 = "4600c6cd5b15bec0628339ed83ed4779f8cccb60ee90ce22711c0629f5682b23"
HANDOFF_YAML_SHA256 = (
    "1dba29ed5bfa13291ce72449dba3bd6e30da65e493fd24b12a0711c97b52b4df"
)
SOURCE_TASK_SHA256 = (
    "504710727971bba08bfacc0ee987e82c0c378207b7c3aa2674d4bbd69dd422dd"
)
SOURCE_JOB_SHA256 = (
    "37c542a416eb31de349330778542065134cfc6e7faa9fb3814ce31c2769b74de"
)
SOURCE_COMPLETION_SHA256 = (
    "0ebe9ab415b60e01b8daf8fb235d18314c8ca52b4db2a60c86e99c1abb10ed70"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_git_diff_quiet(*paths: str) -> bool:
    result = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *paths],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def build_report() -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    after_bytes = HANDOFF_MD.read_bytes()
    after_text = after_bytes.decode("utf-8")
    lines = after_text.splitlines()
    after_heading = lines[2] if len(lines) > 2 else ""

    if after_heading != AFTER_HEADING:
        errors.append("handoff-0920 Markdown heading is not the exact repaired heading")
    if after_text.count("handoff-0920") < 1:
        errors.append("canonical literal handoff-0920 is absent")
    if after_text.count(AFTER_HEADING) != 1:
        errors.append("exact repaired heading does not occur once")

    reconstructed = after_text.replace(AFTER_HEADING, BEFORE_HEADING, 1).encode(
        "utf-8"
    )
    if sha256_bytes(reconstructed) != BEFORE_SHA256:
        errors.append("reconstructed pre-repair Markdown hash does not match")
    if sha256_bytes(after_bytes) != AFTER_SHA256:
        errors.append("repaired Markdown hash does not match")
    if len(after_bytes) - len(reconstructed) != 8:
        errors.append("repair is not the exact eight-byte insertion")

    protected_hashes = {
        "handoff_yaml_sha256": sha256_path(HANDOFF_YAML),
        "source_task_sha256": sha256_path(SOURCE_TASK),
        "source_job_sha256": sha256_path(SOURCE_JOB),
        "source_completion_sha256": sha256_path(SOURCE_COMPLETION),
    }
    expected_hashes = {
        "handoff_yaml_sha256": HANDOFF_YAML_SHA256,
        "source_task_sha256": SOURCE_TASK_SHA256,
        "source_job_sha256": SOURCE_JOB_SHA256,
        "source_completion_sha256": SOURCE_COMPLETION_SHA256,
    }
    for key, expected in expected_hashes.items():
        if protected_hashes[key] != expected:
            errors.append(f"protected hash mismatch: {key}")

    protected_git_paths = [
        "research_control/handoffs/handoff-0920.yaml",
        "research_control/tasks/RT-20260730-013",
    ]
    protected_git_clean = run_git_diff_quiet(*protected_git_paths)
    if not protected_git_clean:
        errors.append("protected predecessor paths differ from HEAD")

    resolver = subprocess.run(
        [
            str(ROOT / ".venv/bin/python"),
            "scripts/research_control/continue_research.py",
            "--summary",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    resolver_text = (resolver.stdout + resolver.stderr).strip()
    resolver_pass = (
        resolver.returncode == 0
        and "does not identify handoff-0920" not in resolver_text
        and "Boundary: director_decision_required" in resolver_text
    )
    if not resolver_pass:
        errors.append("live continuation boundary does not accept handoff-0920")

    report: dict[str, object] = {
        "schema_id": "handoff_0920_markdown_identity_recovery_receipt_v1",
        "status": "PASS" if not errors else "FAIL",
        "goal_id": "crg-20260720T161354Z-96bc2664ce31bfe0",
        "generation": 183,
        "task_id": "RT-20260730-014",
        "job_id": "AJ-RT-20260730-014-001",
        "work_item_id": "P9-T07",
        "strategy_id": "repair_handoff_0920_markdown_identity_and_checkpoint_v1",
        "route_sha256": (
            "92bbc9b51c6b523d8645a482aaae70efba66369c48c9134b81e1a3c63c376d39"
        ),
        "source_head": "8b2ebbae2de39669b4c95a9fa3485477430d6592",
        "handoff_markdown": {
            "path": "research_control/handoffs/handoff-0920.md",
            "before_heading": BEFORE_HEADING,
            "after_heading": after_heading,
            "before_sha256": BEFORE_SHA256,
            "after_sha256": sha256_bytes(after_bytes),
            "canonical_literal_present": "handoff-0920" in after_text,
            "exact_heading_occurrence_count": after_text.count(AFTER_HEADING),
            "insertion_byte_count": len(after_bytes) - len(reconstructed),
            "every_other_byte_unchanged": sha256_bytes(reconstructed)
            == BEFORE_SHA256,
            "reconstructed_before_hash_matches": sha256_bytes(reconstructed)
            == BEFORE_SHA256,
        },
        "protected_predecessor": {
            **protected_hashes,
            "git_paths_unchanged_from_head": protected_git_clean,
            "p9_t06_reexecuted": False,
            "p9_t07_executed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "benchmark_pass_count_changed": False,
            "physics_promotion_authorized": False,
        },
        "validation": {
            "live_continuation_boundary": {
                "status": "PASS" if resolver_pass else "FAIL",
                "exit_code": resolver.returncode,
                "expected_boundary": "director_decision_required",
            }
        },
        "errors": errors,
    }
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report, errors = build_report()
    if args.write_report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.check:
        if not REPORT.is_file():
            errors.append("tracked recovery receipt is missing")
        else:
            stored = json.loads(REPORT.read_text(encoding="utf-8"))
            if stored != report:
                errors.append("tracked recovery receipt differs from live validation")
    report["status"] = "PASS" if not errors else "FAIL"
    report["errors"] = errors
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif errors:
        print("\n".join(errors), file=sys.stderr)
    else:
        print("handoff-0920 Markdown identity recovery validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
