#!/usr/bin/env python3
"""Validate the exact-path blank-at-EOF policy for RT-20260722-023."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
ATTRIBUTE_VALUE = "-blank-at-eof"
PROTECTED = {
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_claim_map_v1.yaml":
        "e9283556dd03a08a37ddd55962884ad1cd57ec6c60f194d01bc37a13733eb679",
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_internal_review_packet_v1.md":
        "25087b0dcacc1c07faff48e2ecddc6e57b026a352faf27ccbb5015774203479b",
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_reproducibility_source_package_v1.yaml":
        "e4f4e0cd9c2beff5ad4e9de90d33734d4d4a0f1719e05c4ef24649bd791d3c79",
    "research_control/tasks/RT-20260722-021/artifacts/validate_exact_gr_interpretive_package.py":
        "ace6d4bd7b98da40af8632d1617d0c8f4126f0c272310d76cacf7affb7ef24cf",
}
CONTROL = (
    "research_control/tasks/RT-20260722-021/artifacts/"
    "exact_gr_interpretive_manuscript_v1.md"
)
PRESERVED = {
    "research_control/tasks/RT-20260722-022/jobs/completions/"
    "AJC-AJ-RT-20260722-022-001.yaml":
        "95ff0395615017e5829934356c729b62ab073e8e057f39c4f1bf73d6d1d4136a",
    "research_control/handoffs/handoff-0831.yaml":
        "7dee8cfd13fde6e0296cc05179407884adffc0ef58a9dbc40d62078366926eec",
    "research_control/handoffs/handoff-0831.md":
        "10cd285c7d9121fa9948e675a5f471db0a2cb789181eca8d5bb96d0a903b1ee6",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def check_attributes(paths: list[str]) -> dict[str, str]:
    result = run("git", "check-attr", "whitespace", "--", *paths)
    if result.returncode:
        raise RuntimeError(f"git check-attr failed: {result.stdout.strip()}")
    observed: dict[str, str] = {}
    for line in result.stdout.splitlines():
        path, attribute, value = line.rsplit(": ", 2)
        if attribute != "whitespace":
            raise RuntimeError(f"unexpected attribute output: {line}")
        observed[path] = value
    return observed


def isolated_diff_proof(attribute_text: str) -> dict[str, object]:
    all_paths = [*PROTECTED, CONTROL]
    with tempfile.TemporaryDirectory(prefix="rt-20260722-023-") as temp:
        repo = Path(temp)
        init = run("git", "init", "-q", cwd=repo)
        if init.returncode:
            raise RuntimeError(f"git init failed: {init.stdout.strip()}")
        (repo / ".gitattributes").write_text(attribute_text, encoding="utf-8")
        for relative in all_paths:
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("content\n", encoding="utf-8")
        run("git", "add", ".", cwd=repo)
        run("git", "-c", "user.name=Control", "-c", "user.email=control@example.invalid",
            "commit", "-qm", "baseline", cwd=repo)
        for relative in all_paths:
            (repo / relative).write_text("content\n\n", encoding="utf-8")

        intended = run("git", "diff", "--check", "--", *PROTECTED, cwd=repo)
        control = run("git", "diff", "--check", "--", CONTROL, cwd=repo)
        combined = run("git", "diff", "--check", cwd=repo)
        return {
            "intended_returncode": intended.returncode,
            "intended_output": intended.stdout,
            "control_returncode": control.returncode,
            "control_output": control.stdout,
            "combined_returncode": combined.returncode,
            "combined_output": combined.stdout,
        }


def validate() -> dict[str, object]:
    errors: list[str] = []
    attributes_path = ROOT / ".gitattributes"
    attribute_text = attributes_path.read_text(encoding="utf-8")
    lines = [
        line.strip()
        for line in attribute_text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    required_lines = [
        f"{path} whitespace={ATTRIBUTE_VALUE}" for path in PROTECTED
    ]
    for line in required_lines:
        if lines.count(line) != 1:
            errors.append(f"required literal rule must occur exactly once: {line}")
    whitespace_rules = [line for line in lines if " whitespace=" in line]
    if whitespace_rules != required_lines:
        errors.append("whitespace rules must be exactly the four ordered literal paths")
    if any(any(mark in line.split()[0] for mark in ("*", "?", "[")) for line in whitespace_rules):
        errors.append("wildcard syntax is forbidden in exact-path whitespace rules")

    protected_hashes = {path: sha256(ROOT / path) for path in PROTECTED}
    preserved_hashes = {path: sha256(ROOT / path) for path in PRESERVED}
    for path, expected in PROTECTED.items():
        if protected_hashes[path] != expected:
            errors.append(f"protected hash mismatch: {path}")
    for path, expected in PRESERVED.items():
        if preserved_hashes[path] != expected:
            errors.append(f"predecessor preservation mismatch: {path}")

    observed_attributes = check_attributes([*PROTECTED, CONTROL])
    for path in PROTECTED:
        if observed_attributes.get(path) != ATTRIBUTE_VALUE:
            errors.append(f"unexpected whitespace attribute for {path}")
    if observed_attributes.get(CONTROL) != "unspecified":
        errors.append(f"control path must remain unspecified: {CONTROL}")

    isolated = isolated_diff_proof(attribute_text)
    if isolated["intended_returncode"] != 0 or isolated["intended_output"]:
        errors.append("intended paths did not pass isolated git diff --check")
    if isolated["control_returncode"] == 0:
        errors.append("adjacent control path did not fail isolated git diff --check")
    if "blank line at EOF" not in str(isolated["control_output"]):
        errors.append("adjacent control did not report blank line at EOF")
    combined_output = str(isolated["combined_output"])
    if isolated["combined_returncode"] == 0 or CONTROL not in combined_output:
        errors.append("combined isolated proof did not retain the control failure")
    if any(path in combined_output for path in PROTECTED):
        errors.append("combined isolated proof reported an intended protected path")

    return {
        "schema_id": "exact_path_whitespace_policy_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260722-023",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "gitattributes_sha256": sha256(attributes_path),
        "required_rules": required_lines,
        "observed_attributes": observed_attributes,
        "protected_hashes": protected_hashes,
        "preserved_hashes": preserved_hashes,
        "isolated_diff_proof": isolated,
        "claim_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "p15_t03_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = validate()
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
