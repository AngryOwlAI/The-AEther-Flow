#!/usr/bin/env python3
"""Validate the bounded P2-T05 Lean formal-proof packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260720-018"
ARTIFACTS = TASK / "artifacts"
PROOF = ARTIFACTS / "proof"
SOURCE = PROOF / "SelectorKernel.lean"
RECEIPT = ARTIFACTS / "eqsrc_selector_formal_proof_compact_receipt.json"
REPORT = ARTIFACTS / "eqsrc_selector_formal_proof_validation.json"
LEAN = (
    ROOT
    / ".local/rt-20260720-018-lean/toolchain/lean-4.30.0-darwin_aarch64/bin/lean"
)
BUILD_SCRIPT = PROOF / "build_proof.sh"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, evidence: object) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "evidence": evidence,
            }
        )

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    source_text = SOURCE.read_text(encoding="utf-8")

    check(
        "source_sha256",
        sha256(SOURCE) == receipt["build"]["source_sha256"],
        sha256(SOURCE),
    )
    check(
        "p2_t03_source_sha256",
        sha256(
            ROOT
            / "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex"
        )
        == receipt["source_dependencies"]
        ["research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex"],
        receipt["source_dependencies"],
    )
    check(
        "p2_t04_fixture_sha256",
        sha256(
            ROOT
            / "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_fixtures.json"
        )
        == receipt["source_dependencies"]
        ["research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_fixtures.json"],
        receipt["source_dependencies"],
    )

    banned_patterns = {
        "sorry": r"\bsorry\b",
        "admit": r"\badmit\b",
        "axiom_declaration": r"(?m)^\s*axiom\s+",
        "unsafe_declaration": r"(?m)^\s*unsafe\s+",
    }
    for label, pattern in banned_patterns.items():
        matches = re.findall(pattern, source_text)
        check(f"no_{label}", not matches, matches)

    theorem_names = [
        "empty_fixed_iff_no_invariant_selector",
        "fixed_choice_unique_of_transitive",
        "no_invariant_selector_of_transitive_distinct",
        "multiple_fixed_gives_multiple_selectors",
        "historical_sign_swap_no_invariant_selector",
        "trivial_action_has_multiple_selectors",
    ]
    for theorem_name in theorem_names:
        check(
            f"theorem_present:{theorem_name}",
            f"theorem {theorem_name}" in source_text,
            theorem_name,
        )
        check(
            f"axiom_query_present:{theorem_name}",
            f"#print axioms {theorem_name}" in source_text,
            theorem_name,
        )

    check(
        "historical_fixture_identity",
        "FX-RESP-XEMPTY-SIGN-SWAP" in source_text,
        "FX-RESP-XEMPTY-SIGN-SWAP",
    )
    check("lean_binary_present", LEAN.is_file(), str(LEAN))

    if LEAN.is_file():
        version = subprocess.run(
            [str(LEAN), "--version"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        check("lean_version", "version 4.30.0" in version, version)
        local_parent = ROOT / ".local/rt-20260720-018-lean"
        with tempfile.TemporaryDirectory(prefix="validate.", dir=local_parent) as tmp:
            output_dir = Path(tmp)
            subprocess.run(
                ["sh", str(BUILD_SCRIPT), str(LEAN), str(output_dir)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            proof_hash = sha256(output_dir / "SelectorKernel.olean")
            build_log = (output_dir / "lean-build.log").read_text(encoding="utf-8")
            axiom_lines = [
                line for line in build_log.splitlines() if "does not depend on any axioms" in line
            ]
            check(
                "proof_object_sha256",
                proof_hash == receipt["build"]["proof_object_sha256"],
                proof_hash,
            )
            check("axiom_report_count", len(axiom_lines) == 6, axiom_lines)
            check(
                "no_reported_axiom_dependencies",
                "depends on axioms:" not in build_log,
                build_log.splitlines(),
            )

    failures = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "eqsrc-selector-formal-proof-validation.v1",
        "task_id": "RT-20260720-018",
        "job_id": "AJ-RT-20260720-018-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "claim_boundary": {
            "machine_checked_under_declared_definitions": not failures,
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "general_eqsrc_discharged": False,
        },
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
