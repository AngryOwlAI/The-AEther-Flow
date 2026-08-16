#!/usr/bin/env python3
"""Validate the exact handoff-1041 Markdown identity recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HANDOFF_MD = ROOT / "research_control/handoffs/handoff-1041.md"
HANDOFF_YAML = ROOT / "research_control/handoffs/handoff-1041.yaml"
SOURCE_TASK = ROOT / "research_control/tasks/RT-20260815-007/00_TASK.yaml"
SOURCE_JOB = ROOT / "research_control/tasks/RT-20260815-007/jobs/AJ-RT-20260815-007-001.yaml"
SOURCE_COMPLETION = ROOT / (
    "research_control/tasks/RT-20260815-007/jobs/completions/"
    "AJC-AJ-RT-20260815-007-001.yaml"
)
SOURCE_FUSION = ROOT / (
    "research_control/tasks/RT-20260815-007/artifacts/"
    "parent_fusion_notes_p4_t02_b2_canonical_source_open_event_fibration_typing_descent.md"
)
REPORT = ROOT / (
    "research_control/tasks/RT-20260815-008/artifacts/"
    "handoff_1041_markdown_identity_recovery_receipt.json"
)

BEFORE_HEADING = "# Handoff 1041"
AFTER_HEADING = "# handoff-1041"
BEFORE_SHA256 = "3edf4f4bcf80a765e70c1f62148c0535200c1fc2d49e70117b586b20ac316cf4"
AFTER_SHA256 = "a2e2fead3a1858b8d76a694dd2224d1992eef90b8b28803ccff728d96668c5ac"
EXPECTED_OFFSETS = [2, 9]
EXPECTED_LENGTH = 1861
PROTECTED_HASHES = {
    "handoff_yaml_sha256": "3ecf4ec8e17ba6e0b3ef590b78305a668a4cfc7ba21ca59dd03d8fcb3414c1ac",
    "source_task_sha256": "86071ed9137bda90dc6bd798cba542dd69eda90811707584fe7a2f3cfc09559f",
    "source_job_sha256": "85e8147a7f36a0cb3ccf75466cff35ed33fe2280ce461ce3b807053c793262cc",
    "source_completion_sha256": "b8d51235c26430b9db31be24357d73c8a40288be1b5018bb2d02c7938622c4e6",
    "source_fusion_sha256": "9e45c407be92b8d4b66303b5ed8cd4043453f09b303227ac35de74f1feb62604",
}


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
    after_heading = lines[0] if lines else ""

    if not after_heading.startswith(AFTER_HEADING + " "):
        errors.append("handoff-1041 Markdown heading is not the exact repaired heading")
    if after_text.count("handoff-1041") < 1:
        errors.append("canonical literal handoff-1041 is absent")
    if after_text.count(AFTER_HEADING) != 1:
        errors.append("exact repaired heading does not occur once")

    reconstructed = after_text.replace(AFTER_HEADING, BEFORE_HEADING, 1).encode("utf-8")
    observed_offsets = [
        index
        for index, (before, after) in enumerate(zip(reconstructed, after_bytes))
        if before != after
    ]
    if sha256_bytes(reconstructed) != BEFORE_SHA256:
        errors.append("reconstructed pre-repair Markdown hash does not match")
    if sha256_bytes(after_bytes) != AFTER_SHA256:
        errors.append("repaired Markdown hash does not match")
    if len(after_bytes) != EXPECTED_LENGTH or len(reconstructed) != EXPECTED_LENGTH:
        errors.append("repair changed the Markdown byte length")
    if observed_offsets != EXPECTED_OFFSETS:
        errors.append("repair is not the exact two-byte replacement")

    protected_paths = {
        "handoff_yaml_sha256": HANDOFF_YAML,
        "source_task_sha256": SOURCE_TASK,
        "source_job_sha256": SOURCE_JOB,
        "source_completion_sha256": SOURCE_COMPLETION,
        "source_fusion_sha256": SOURCE_FUSION,
    }
    observed_protected = {key: sha256_path(path) for key, path in protected_paths.items()}
    for key, expected in PROTECTED_HASHES.items():
        if observed_protected[key] != expected:
            errors.append(f"protected hash mismatch: {key}")

    protected_git_clean = run_git_diff_quiet(
        "research_control/handoffs/handoff-1041.yaml",
        "research_control/tasks/RT-20260815-007",
    )
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
        and "does not identify handoff-1041" not in resolver_text
        and "Status: blocked" not in resolver_text
    )
    if not resolver_pass:
        errors.append("live continuation boundary does not accept the repaired identity")

    report: dict[str, object] = {
        "schema_id": "handoff_1041_markdown_identity_recovery_receipt_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260815-008",
        "job_id": "AJ-RT-20260815-008-001",
        "work_item_id": "P4-T02",
        "strategy_id": "repair_handoff_1041_markdown_identity_and_checkpoint_v1",
        "route_sha256": "7b72346bbc220a76c68126423a22ba3cce8dc751156dee615491f42f44ace34a",
        "source_head": "20ae0306caed33b7f98bd62873606a8d7d8a2df9",
        "source_tree": "0899a684a622c10b461e54cda6d27cfefe394cc2",
        "handoff_markdown": {
            "path": "research_control/handoffs/handoff-1041.md",
            "before_heading": BEFORE_HEADING,
            "after_heading": after_heading,
            "before_sha256": BEFORE_SHA256,
            "after_sha256": sha256_bytes(after_bytes),
            "canonical_literal_present": "handoff-1041" in after_text,
            "exact_heading_occurrence_count": after_text.count(AFTER_HEADING),
            "replacement_count": len(observed_offsets),
            "replacement_offsets_zero_based": observed_offsets,
            "length_unchanged": len(after_bytes) == len(reconstructed) == EXPECTED_LENGTH,
            "every_other_byte_unchanged": sha256_bytes(reconstructed) == BEFORE_SHA256,
            "reconstructed_before_hash_matches": sha256_bytes(reconstructed) == BEFORE_SHA256,
        },
        "protected_predecessor": {
            **observed_protected,
            "git_paths_unchanged_from_head": protected_git_clean,
            "predecessor_science_reexecuted": False,
            "theoretical_selector_executed": False,
            "scientific_claims_changed": False,
            "physical_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        },
        "validation": {
            "live_continuation_boundary": {
                "status": "PASS" if resolver_pass else "FAIL",
                "exit_code": resolver.returncode,
                "expected_boundary": "nonblocked",
            }
        },
        "authority_limits": {
            "handoff_yaml_changed": False,
            "scientific_status_changed": False,
            "ontology_or_source_law_adopted": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authorized": False,
            "push_authorized": False,
            "external_action_authorized": False,
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
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
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
        print("handoff-1041 Markdown identity recovery validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
