#!/usr/bin/env python3
"""Validate the exact-path blank-at-EOF policy for RT-20260724-006."""

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
    "research_control/tasks/RT-20260724-004/artifacts/"
    "child_phys_math_ontology_regime_gate_chair_review.yaml":
        "c86d80fea5916fd17aff2136506b4c7844b16fb5ee0d9591993b78cb70ec0d82",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "child_phys_phil_ontology_regime_gate_chair_review.yaml":
        "c39c5cd7ca47606bbc07c703c266aa2e79e152a349e9c9db4deef7bb0400c971",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "human_authorization_p4_t05_continuum_first_v1.yaml":
        "3421808c71a64279ef5ba62df5376ab4999d2c67978d4f7ceabbeb0ae9b2bde6",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "ontology_regime_gate_chair_decision_v1.tex":
        "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "parent_conflict_review_ontology_regime_gate_chair_review.yaml":
        "c3b86e3a3dee6c4f6a4f6f7fc3a93333151c40277e7b9d8a9ad6bc1ae0463d21",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "parent_fusion_notes_ontology_regime_gate_chair_review.md":
        "7fd0427102dd471b02b9b068492bac276369193a84c6f5c25d04698a8f8218c7",
}
CONTROL = (
    "research_control/tasks/RT-20260724-004/artifacts/"
    "child_phys_math_ontology_regime_gate_chair_review.md"
)
PREEXISTING_EXACT_RULES = [
    "research_control/tasks/RT-20260722-021/artifacts/"
    "exact_gr_claim_map_v1.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/"
    "exact_gr_internal_review_packet_v1.md whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/"
    "exact_gr_reproducibility_source_package_v1.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/"
    "validate_exact_gr_interpretive_package.py whitespace=-blank-at-eof",
]
PRESERVED = {
    "research_control/approvals/approval-20260724-001.yaml":
        "37038157b5deb23a3ae8249dcf5562ac8e9be37f6fa4ae8704c47b0eeb24a412",
    "research_control/tasks/RT-20260724-004/jobs/completions/"
    "AJC-AJ-RT-20260724-004-001.yaml":
        "d248a2abfe6a2571b7ebb6a930c720f64af7f3d39cdf0e497a5e194308a055bf",
    "research_control/handoffs/handoff-0854.yaml":
        "19be01044894e6611cf11d8f7ce91cbff04a93e0bd88f8a6d353eca7fbf4acda",
    "research_control/tasks/RT-20260724-005/jobs/completions/"
    "AJC-AJ-RT-20260724-005-001.yaml":
        "a8da857a9759d8bb0021b42585adca3ea8c41b6d5b3b394a3e74e5d9b0d9b7c0",
    "research_control/handoffs/handoff-0855.yaml":
        "828de27d9c7bcdf7e5a8ed1ae728297d0f912dc7cb0964aa6433f34a04ee5a40",
    "research_control/tasks/RT-20260724-005/artifacts/"
    "validation_blocker_checkpoint_hash_bound_p4_t05_blank_eof_v1.yaml":
        "e78a29f97da516d72ddd08c711509bd6e68bb63362ddb7a4457ad90754afd364",
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
    with tempfile.TemporaryDirectory(prefix="rt-20260724-006-") as temp:
        repo = Path(temp)
        init = run("git", "init", "-q", cwd=repo)
        if init.returncode:
            raise RuntimeError(f"git init failed: {init.stdout.strip()}")
        (repo / ".gitattributes").write_text(attribute_text, encoding="utf-8")
        for relative in all_paths:
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("content\n", encoding="utf-8")
        add = run("git", "add", ".", cwd=repo)
        if add.returncode:
            raise RuntimeError(f"git add failed: {add.stdout.strip()}")
        commit = run(
            "git",
            "-c",
            "user.name=Control",
            "-c",
            "user.email=control@example.invalid",
            "commit",
            "-qm",
            "baseline",
            cwd=repo,
        )
        if commit.returncode:
            raise RuntimeError(f"git commit failed: {commit.stdout.strip()}")
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
    expected_rules = [*PREEXISTING_EXACT_RULES, *required_lines]
    for line in expected_rules:
        if lines.count(line) != 1:
            errors.append(f"required literal rule must occur exactly once: {line}")
    whitespace_rules = [line for line in lines if " whitespace=" in line]
    if whitespace_rules != expected_rules:
        errors.append(
            "whitespace rules must be exactly the ten ordered literal paths"
        )
    if any(
        any(mark in line.split()[0] for mark in ("*", "?", "["))
        for line in whitespace_rules
    ):
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
        errors.append("unrelated control path did not fail isolated git diff --check")
    if "blank line at EOF" not in str(isolated["control_output"]):
        errors.append("unrelated control did not report blank line at EOF")
    combined_output = str(isolated["combined_output"])
    if isolated["combined_returncode"] == 0 or CONTROL not in combined_output:
        errors.append("combined isolated proof did not retain the control failure")
    if any(path in combined_output for path in PROTECTED):
        errors.append("combined isolated proof reported an intended protected path")

    return {
        "schema_id": "exact_path_whitespace_policy_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260724-006",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "gitattributes_sha256": sha256(attributes_path),
        "required_rules": required_lines,
        "preserved_preexisting_rules": PREEXISTING_EXACT_RULES,
        "observed_attributes": observed_attributes,
        "protected_hashes": protected_hashes,
        "preserved_hashes": preserved_hashes,
        "isolated_diff_proof": isolated,
        "claim_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "p4_t06_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = validate()
    if args.write_report:
        report_path = (
            ROOT
            / "research_control/tasks/RT-20260724-006/artifacts/"
            "exact_path_whitespace_policy_recovery_receipt.json"
        )
        report_path.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
