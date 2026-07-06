#!/usr/bin/env python3
"""Validate the v17 P3-T05 public documentation calibration packet."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260705-058/artifacts/"
    / "p3_t05_public_documentation_calibration_report.json"
)

EXPLICIT_PUBLIC_PATHS = [
    "README.md",
    "github-facing/project-overview-explainer.md",
    "github-facing/aether-flow-physics-program-explainer.md",
    "github-facing/exact-gr-benchmark-boundary-explainer.md",
    "github-facing/gr-derivation-roadmap-explainer.md",
    "github-facing/claim-gates-explainer.md",
    "github-facing/negative-results-and-obstructions-explainer.md",
]

CALIBRATED_REQUIRED_MARKERS = {
    "README.md": [
        "positive status as a scoped source-only object",
        "positive status as a scoped source-extension object",
        "positive status as scoped evidence/preconditions only",
    ],
    "github-facing/project-overview-explainer.md": [
        "positive status as a scoped source-only object",
        "positive status as a scoped source-extension object",
        "positive status as scoped evidence/preconditions only",
    ],
    "github-facing/aether-flow-physics-program-explainer.md": [
        "Positive status: scoped source-only object",
        "Positive status: scoped source-extension object",
        "Positive status: scoped evidence/preconditions only",
    ],
    "github-facing/exact-gr-benchmark-boundary-explainer.md": [
        "positive status as a scoped source-only object",
        "positive status as a scoped source-extension object",
        "positive status as scoped evidence/preconditions only",
    ],
    "github-facing/gr-derivation-roadmap-explainer.md": [
        "Positive status: scoped source-only object",
        "Positive status: scoped source-extension object",
        "Positive status: scoped evidence/preconditions only",
    ],
    "github-facing/claim-gates-explainer.md": [
        "positive status as a scoped source-only object",
        "positive status as a scoped source-extension object",
        "positive status as scoped evidence/preconditions only",
    ],
}

SOURCE_CONTRACT_PATHS = [
    "markdown/html-explainer-specs/project-overview-explainer.md",
    "markdown/html-explainer-specs/aether-flow-physics-program-explainer.md",
    "markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md",
    "markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md",
    "markdown/html-explainer-specs/claim-gates-explainer.md",
    "markdown/publication-briefs/project-overview.publication-brief.md",
    "markdown/publication-briefs/aether-flow-physics-program.publication-brief.md",
    "markdown/publication-briefs/exact-gr-benchmark-boundary.publication-brief.md",
    "markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md",
    "markdown/publication-briefs/claim-gates.publication-brief.md",
]

ALLOWED_HTML_SYNC_PATHS = {
    "html/project-overview-explainer.html": (
        "markdown/html-explainer-specs/project-overview-explainer.md",
        "positive status as a scoped source-only object",
    ),
    "html/aether-flow-physics-program-explainer.html": (
        "markdown/html-explainer-specs/aether-flow-physics-program-explainer.md",
        "Positive status: scoped source-only object",
    ),
    "html/exact-gr-benchmark-boundary-explainer.html": (
        "markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md",
        "positive scoped status",
    ),
    "html/gr-derivation-roadmap-explainer.html": (
        "markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md",
        "positive scoped source-only object status",
    ),
    "html/claim-gates-explainer.html": (
        "markdown/html-explainer-specs/claim-gates-explainer.md",
        "positive status as a scoped source-only object",
    ),
}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def candidate_paths() -> list[str]:
    paths = list(EXPLICIT_PUBLIC_PATHS)
    paths.extend(sorted(glob.glob(str(REPO_ROOT / "markdown/html-explainer-specs/*.md"))))
    paths.extend(sorted(glob.glob(str(REPO_ROOT / "markdown/publication-briefs/*.md"))))
    return sorted(
        {
            str(Path(path).relative_to(REPO_ROOT) if Path(path).is_absolute() else Path(path))
            for path in paths
        }
    )


def changed_paths() -> list[str]:
    diff = run(["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"])
    if diff.returncode != 0:
        raise RuntimeError(diff.stderr.strip() or "git diff failed")
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"])
    if untracked.returncode != 0:
        raise RuntimeError(untracked.stderr.strip() or "git ls-files failed")
    paths = {line.strip() for line in diff.stdout.splitlines() if line.strip()}
    paths.update(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return sorted(paths)


def text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def normalized(value: str) -> str:
    return " ".join(value.split())


def sha256(path: str) -> str:
    return hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()


def validate_claim_language(paths: list[str]) -> dict[str, Any]:
    result = run(
        [
            sys.executable,
            "scripts/project_control/validate_claim_language.py",
            "--paths",
            *paths,
            "--json",
        ]
    )
    if result.returncode != 0:
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            report = {"status": "FAIL", "stdout": result.stdout, "stderr": result.stderr}
        return report
    return json.loads(result.stdout)


def validate() -> dict[str, Any]:
    errors: list[str] = []
    public_paths = candidate_paths()
    claim_report = validate_claim_language(public_paths)
    if claim_report.get("status") != "PASS":
        errors.append("focused claim-language scan did not pass")
    if claim_report.get("hard_fail_count") != 0:
        errors.append("focused claim-language scan has hard failures")
    if claim_report.get("underclaim_calibration_warning_count") != 0:
        errors.append("focused claim-language scan still has underclaim warnings")

    for path, markers in CALIBRATED_REQUIRED_MARKERS.items():
        body = normalized(text(path))
        missing = [marker for marker in markers if normalized(marker) not in body]
        if missing:
            errors.append(f"{path}: missing calibrated marker(s): {missing}")

    for path in SOURCE_CONTRACT_PATHS:
        body = text(path)
        if "positive-first" not in body and "positive scoped status" not in body:
            errors.append(f"{path}: missing positive-first source-contract marker")

    changed = changed_paths()
    html_changed = [path for path in changed if path.startswith("html/")]
    unexpected_html = [path for path in html_changed if path not in ALLOWED_HTML_SYNC_PATHS]
    if unexpected_html:
        errors.append(f"tracked HTML changed outside bounded derivative sync: {unexpected_html}")
    for html_path in html_changed:
        source_path, marker = ALLOWED_HTML_SYNC_PATHS[html_path]
        body = text(html_path)
        expected_hash = sha256(source_path)
        if expected_hash not in body:
            errors.append(f"{html_path}: missing source-basis hash {expected_hash}")
        if normalized(marker) not in normalized(body):
            errors.append(f"{html_path}: missing calibrated HTML marker {marker!r}")

    science_mutations = [
        path
        for path in changed
        if path.startswith("science/")
        or path.startswith("papers/")
        or path.startswith("ontology/")
        or path.startswith("tex/")
    ]
    if science_mutations:
        errors.append(f"science or ontology authority paths changed unexpectedly: {science_mutations}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "focused_claim_language": {
            "status": claim_report.get("status"),
            "hard_fail_count": claim_report.get("hard_fail_count"),
            "warning_count": claim_report.get("warning_count"),
            "finding_count": claim_report.get("finding_count"),
            "overclaim_hard_fail_count": claim_report.get("overclaim_hard_fail_count"),
            "underclaim_calibration_warning_count": claim_report.get(
                "underclaim_calibration_warning_count"
            ),
            "scanned_path_count": claim_report.get("scanned_path_count"),
        },
        "calibrated_public_paths": sorted(CALIBRATED_REQUIRED_MARKERS),
        "source_contract_paths": SOURCE_CONTRACT_PATHS,
        "candidate_public_path_count": len(public_paths),
        "changed_path_count": len(changed),
        "changed_paths": changed,
        "html_changed": html_changed,
        "allowed_html_sync_paths": sorted(ALLOWED_HTML_SYNC_PATHS),
        "science_mutations": science_mutations,
        "claim_boundary": {
            "scientific_claims_changed": False,
            "source_law_adopted": False,
            "detector_semantics_adopted": False,
            "coupling_law_adopted": False,
            "matter_coupling_derived": False,
            "matter_coupling_adopted": False,
            "stress_energy_semantics_imported": False,
            "matter_action_imported": False,
            "einstein_equations_derived": False,
            "benchmark_promoted": False,
            "gate_chair_verdict_issued": False,
            "completed_derivation_claimed": False,
            "direct_html_only_edit": False,
            "tracked_html_derivative_synchronized": bool(html_changed),
            "tracked_html_hand_edited": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
