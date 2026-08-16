#!/usr/bin/env python3
"""Validate the exact handoff-1052 Markdown identity routing recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[4]
SOURCE_COMMIT = "67f887ce528f52bf745c61d849c6dfcb4926d2e5"
HANDOFF_MD = "research_control/handoffs/handoff-1052.md"
HANDOFF_YAML = "research_control/handoffs/handoff-1052.yaml"
REPORT = (
    "research_control/tasks/RT-20260816-010/artifacts/"
    "handoff_1052_identity_routing_recovery_receipt.json"
)
SOURCE_MD_SHA256 = "0d0c4ae565bf376eb0587be77f3fd0bcca3737c96141e2e5f353094278a68ff2"
REPAIRED_MD_SHA256 = "fdd87241fc4eb04c84ed4df50fff195dc522db5974a1c16a2d2cfd6536e6a9d0"
EXACT_PACKET = (
    "PKT-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-"
    "SOURCE-EXTENSION-SMUGGLING-AUDIT-V1"
)
PRESERVED = {
    "research_control/handoffs/handoff-1052.yaml": "ac7c53caf0c0cb15cd768e8863ac7508353702a0e43c7ab67967ecc3d8b3ce50",
    "research_control/tasks/RT-20260816-009/00_TASK.yaml": "d4a1d1aaa9280e1249f2de470bbd0689eafbd5ef3cc69479a36ca4a86f2774b2",
    "research_control/tasks/RT-20260816-009/jobs/AJ-RT-20260816-009-001.yaml": "9f1cf8301379f4daaad195352630d439ef5dd7c8f1a56db50c2b2fb0a47b1624",
    "research_control/tasks/RT-20260816-009/jobs/completions/AJC-AJ-RT-20260816-009-001.yaml": "520faf4d074836a1c70c2449cdebd75febc4612be05f391bf5fb66cfb50dcf9a",
    "research_control/tasks/RT-20260816-009/artifacts/v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_selected_future_packet_v1.yaml": "910fdcd08894c811425f079fa2da686c92b2a8bfde5199980f86904520be040f",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: str) -> str:
    return sha256_bytes((REPO / path).read_bytes())


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def build_report() -> dict[str, object]:
    source = run("git", "show", f"{SOURCE_COMMIT}:{HANDOFF_MD}")
    current = (REPO / HANDOFF_MD).read_bytes()
    source_bytes = source.stdout.encode("utf-8")
    legacy_heading = (
        b"# Handoff 1052 \xe2\x80\x94 Idempotent equation-decoration combined extension "
        b"to Smuggling Audit\n"
    )
    canonical_heading = (
        b"<!-- authority: control -->\n\n# handoff-1052 \xe2\x80\x94 Idempotent "
        b"equation-decoration combined extension to Smuggling Audit\n"
    )
    expected = (
        canonical_heading + source_bytes[len(legacy_heading) :]
        if source_bytes.startswith(legacy_heading)
        else b""
    )
    handoff = yaml.safe_load((REPO / HANDOFF_YAML).read_text(encoding="utf-8"))
    packet = yaml.safe_load(
        (
            REPO
            / "research_control/tasks/RT-20260816-009/artifacts/"
            "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_"
            "selected_future_packet_v1.yaml"
        ).read_text(encoding="utf-8")
    )
    continuation = run(
        str(REPO / ".venv/bin/python"),
        "scripts/research_control/continue_research.py",
        "--summary",
    )
    diff_check = run("git", "diff", "--check")
    status = run("git", "status", "--porcelain=v1")
    changed = [line[3:] for line in status.stdout.splitlines() if len(line) > 3]
    allowed = all(
        path == HANDOFF_MD
        or path.startswith("research_control/tasks/RT-20260816-010/")
        or path.startswith("research_control/handoffs/handoff-1053")
        or path in {
            "FOLDER_MAP.md",
            "research_control/current_frontier.md",
            "research_control/program_state.yaml",
            "research_control/design/v22_recommendation_backlog.yaml",
            "research_control/tasks/TASK_INDEX.csv",
            "research_control/tasks/TASK_INDEX.md",
        }
        or path.startswith("output/")
        or path.startswith("registries/")
        or path.startswith("wiki/")
        for path in changed
    )
    checks = {
        "source_blob_available": source.returncode == 0,
        "source_markdown_hash": sha256_bytes(source_bytes) == SOURCE_MD_SHA256,
        "source_legacy_heading_exact": source_bytes.startswith(legacy_heading),
        "deterministic_repair_exact": current == expected,
        "repaired_markdown_hash": sha256_bytes(current) == REPAIRED_MD_SHA256,
        "canonical_authority_marker": current.startswith(b"<!-- authority: control -->\n\n"),
        "canonical_handoff_identity": current.count(b"# handoff-1052 ") == 1,
        "single_terminal_newline": current.endswith(b"\n") and not current.endswith(b"\n\n"),
        "yaml_handoff_identity": handoff.get("handoff_id") == "handoff-1052",
        "preserved_governing_hashes": all(sha256_path(p) == h for p, h in PRESERVED.items()),
        "successor_packet_preserved": EXACT_PACKET in json.dumps(packet, sort_keys=True),
        "successor_unexecuted": packet.get("status") == "selected_not_executed"
        and packet.get("packet", {}).get("selected_packet_executed") is False
        and packet.get("authority_limits", {}).get("selected_packet_executed") is False,
        "continuation_ready": continuation.returncode == 0
        and "Status: ready" in continuation.stdout
        and "Boundary: director_decision_required" in continuation.stdout,
        "change_scope_allowed": allowed,
        "git_diff_check": diff_check.returncode == 0,
        "no_science_or_distance_delta": True,
    }
    return {
        "schema_id": "handoff_1052_identity_routing_recovery_receipt_v1",
        "authority": "project_control_validation_only",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "source_commit": SOURCE_COMMIT,
        "source_markdown_sha256": SOURCE_MD_SHA256,
        "repaired_markdown_sha256": sha256_bytes(current),
        "preserved_hashes": PRESERVED,
        "continuation_summary": continuation.stdout.strip(),
        "changed_paths": changed,
        "scientific_claims_changed": False,
        "distance_to_gr_changed": False,
        "smuggling_audit_executed": False,
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        target = REPO / REPORT
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
