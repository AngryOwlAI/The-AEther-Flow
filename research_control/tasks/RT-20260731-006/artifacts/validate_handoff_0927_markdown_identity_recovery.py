#!/usr/bin/env python3
"""Validate the exact handoff-0927 Markdown identity recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HANDOFF_MD = ROOT / "research_control/handoffs/handoff-0927.md"
HANDOFF_YAML = ROOT / "research_control/handoffs/handoff-0927.yaml"
SOURCE_TASK = ROOT / "research_control/tasks/RT-20260731-005/00_TASK.yaml"
SOURCE_JOB = (
    ROOT
    / "research_control/tasks/RT-20260731-005/jobs/AJ-RT-20260731-005-001.yaml"
)
SOURCE_COMPLETION = (
    ROOT
    / "research_control/tasks/RT-20260731-005/jobs/completions/"
    "AJC-AJ-RT-20260731-005-001.yaml"
)
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260731-006/artifacts/"
    "handoff_0927_markdown_identity_recovery_receipt.json"
)

BEFORE_HEADING = "# Handoff 0927"
AFTER_HEADING = "# Handoff handoff-0927"
BEFORE_SHA256 = "d25d4f490040375e5d727712e7eee3ec1478e728742ab73bb87d55cd30c8a358"
AFTER_SHA256 = "2ae32cef59debe23a84fc344a06649c4776bc77977dd46960a51f6a0c99c7e13"
HANDOFF_YAML_SHA256 = (
    "6ba67c71d3e8920cacc02215d69da0d91f7b1f1dd45fa9b28a3de28af50236ed"
)
SOURCE_TASK_SHA256 = (
    "1485b9ffd48ada691ab6a0761618c68d83dd173ad36095fc7fb83b61477c2010"
)
SOURCE_JOB_SHA256 = (
    "2e983cbe9b17bf59e0b37327f9e7458d0fa1ea0482bc4c61f56e945811453d96"
)
SOURCE_COMPLETION_SHA256 = (
    "9592bcac19a7095feb603d61b2be689468b2c19e3aad7f22b34360e6bd6c8df0"
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
        errors.append("handoff-0927 Markdown heading is not the exact repaired heading")
    if after_text.count("handoff-0927") < 1:
        errors.append("canonical literal handoff-0927 is absent")
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
        "research_control/handoffs/handoff-0927.yaml",
        "research_control/tasks/RT-20260731-005",
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
        and "does not identify handoff-0927" not in resolver_text
        and "Boundary: director_decision_required" in resolver_text
    )
    if not resolver_pass:
        errors.append("live continuation boundary does not accept handoff-0927")

    report: dict[str, object] = {
        "schema_id": "handoff_0927_markdown_identity_recovery_receipt_v1",
        "status": "PASS" if not errors else "FAIL",
        "goal_id": "crg-20260720T161354Z-96bc2664ce31bfe0",
        "generation": 192,
        "task_id": "RT-20260731-006",
        "job_id": "AJ-RT-20260731-006-001",
        "work_item_id": "P14-T04",
        "strategy_id": "repair_handoff_0927_markdown_identity_and_checkpoint_v1",
        "route_sha256": (
            "a5151b8c5d6b1850086c691c894c58efcf93756c3f3e9c05288f9e41aa21cbd2"
        ),
        "source_head": "c34629620ef0d5513d2abf4f1c6c7ac3fb14da7a",
        "handoff_markdown": {
            "path": "research_control/handoffs/handoff-0927.md",
            "before_heading": BEFORE_HEADING,
            "after_heading": after_heading,
            "before_sha256": BEFORE_SHA256,
            "after_sha256": sha256_bytes(after_bytes),
            "canonical_literal_present": "handoff-0927" in after_text,
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
            "p14_t04_reexecuted": False,
            "p14_t06_executed": False,
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
        print("handoff-0927 Markdown identity recovery validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
