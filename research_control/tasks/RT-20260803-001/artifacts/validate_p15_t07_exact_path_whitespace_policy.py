#!/usr/bin/env python3
"""Validate RT-20260803-001's exact-path P15-T07 whitespace policy."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
ATTRIBUTE_VALUE = "-blank-at-eof"
REPORT = ROOT / "research_control/tasks/RT-20260803-001/artifacts/p15_t07_exact_path_whitespace_policy_receipt.json"
CHECKPOINT_RECEIPT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-18eab97204b5dadb/receipt.json"
FAILED_OUTPUT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-18eab97204b5dadb/gates/0006-git_diff_check.stdout"
PROTECTED = {
    "research_control/tasks/RT-20260802-010/artifacts/child_phys_math_p15_t07_external_action_decision.yaml": "6c6a3b75cec86d219f94899caea830bcf7c3df5a219f13eaa2b0d1369a45fbfc",
    "research_control/tasks/RT-20260802-010/artifacts/child_phys_phil_p15_t07_external_action_decision.yaml": "6db9e21254b0c3f2926a10784e02fd3fa1219cd8b509258923b95a0ed89795dd",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_claim_to_evidence_map_v1.yaml": "7e8f24bce39d5a8120dae43f7f8b8412468a0dcd1fca3aaa50f05ffe8c7c68b5",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_external_action_decision_v1.tex": "054db567ce5bbd15a4796f6e85dcf012cc563c51a36d58692c7dea1d7db6cf22",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_external_action_log_v1.yaml": "4971c55a8a70b68d2749af3fa5499b08bd17e7db165f50a2aaf23323acea02e5",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_internal_ai_advisory_review_v1.yaml": "d3d48c80125f7a9cc635c74c8c156a4fd5c9e9c344e25247341290ae39b4ead5",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_reproducibility_manifest_v1.yaml": "3d260aa8cc53ea2698f0f4723027514e57f0ab798895ee2a94468bca5c0dafa5",
    "research_control/tasks/RT-20260802-010/artifacts/p15_t07_submission_claim_venue_decisions_v1.yaml": "e97374f766a1c078d261632e98bd16673eb531ef1a11e2b3ba41321d1cfbf5b8",
    "research_control/tasks/RT-20260802-010/artifacts/parent_conflict_review_p15_t07_external_action_decision.yaml": "c0987d389100cbcb0f9c7dc53826046a320bec561a4c6652164308c1cc12cb7d",
    "research_control/tasks/RT-20260802-010/artifacts/parent_fusion_notes_p15_t07_external_action_decision.md": "90dbdf0a27755e1ea5f409a06f9c00d3af6c1156d207c42f8caaff80ae86a182",
    "research_control/tasks/RT-20260802-010/artifacts/validate_p15_t07_no_external_action.py": "e3e29c403042594c9bca25b06f36453cdc8301f89484f95c75de92900918007f",
}
CONTROL = "research_control/tasks/RT-20260802-010/artifacts/human_authorization_p15_t07_no_external_action_v1.yaml"
PREEXISTING_EXACT_RULES = [
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_claim_map_v1.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_internal_review_packet_v1.md whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/exact_gr_reproducibility_source_package_v1.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260722-021/artifacts/validate_exact_gr_interpretive_package.py whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/child_phys_math_ontology_regime_gate_chair_review.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/child_phys_phil_ontology_regime_gate_chair_review.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/human_authorization_p4_t05_continuum_first_v1.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/parent_conflict_review_ontology_regime_gate_chair_review.yaml whitespace=-blank-at-eof",
    "research_control/tasks/RT-20260724-004/artifacts/parent_fusion_notes_ontology_regime_gate_chair_review.md whitespace=-blank-at-eof",
]
PRESERVED = {
    "research_control/approvals/approval-20260802-001.yaml": "c0176cb6fb924616d9324bd622d7b68d5f4fcc30fb00c9b2a55601a10d7503e3",
    "research_control/tasks/RT-20260802-010/jobs/completions/AJC-AJ-RT-20260802-010-001.yaml": "1a0220b0d08fd74af0ba12eb76479e6eee7a571eeb5362418d3b5c38dd1728fb",
    "research_control/handoffs/handoff-0943.yaml": "1ce2e68c38b2939adf6a4a8392c26011fa857cb919cdb8db53c1e666e3a7bbfb",
}
LOCAL_EVIDENCE = {
    str(CHECKPOINT_RECEIPT.relative_to(ROOT)): "ac94d93be6c573bad0187179315b5938f33e2dbf018311d36817d559ae6b3725",
    str(FAILED_OUTPUT.relative_to(ROOT)): "18aac0f75f77eab2b937fc8811ededcdb06ac5b1c3fa78ef8645ae130fc2f62a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


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
    with tempfile.TemporaryDirectory(prefix="rt-20260803-001-") as temp:
        repo = Path(temp)
        init = run("git", "init", "-q", cwd=repo)
        if init.returncode:
            raise RuntimeError(init.stdout.strip())
        (repo / ".gitattributes").write_text(attribute_text, encoding="utf-8")
        for relative in [*PROTECTED, CONTROL]:
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("content\n", encoding="utf-8")
        add = run("git", "add", ".", cwd=repo)
        if add.returncode:
            raise RuntimeError(add.stdout.strip())
        commit = run("git", "-c", "user.name=Control", "-c", "user.email=control@example.invalid", "commit", "-qm", "baseline", cwd=repo)
        if commit.returncode:
            raise RuntimeError(commit.stdout.strip())
        for relative in [*PROTECTED, CONTROL]:
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
    lines = [line.strip() for line in attribute_text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    required_lines = [f"{path} whitespace={ATTRIBUTE_VALUE}" for path in PROTECTED]
    expected_rules = [*PREEXISTING_EXACT_RULES, *required_lines]
    whitespace_rules = [line for line in lines if " whitespace=" in line]
    for line in expected_rules:
        if lines.count(line) != 1:
            errors.append(f"required literal rule must occur exactly once: {line}")
    if whitespace_rules != expected_rules:
        errors.append("whitespace rules must be exactly the twenty-one ordered literal paths")
    if any(any(mark in line.split()[0] for mark in ("*", "?", "[")) for line in whitespace_rules):
        errors.append("wildcard syntax is forbidden in exact-path whitespace rules")

    protected_hashes = {path: sha256(ROOT / path) for path in PROTECTED}
    preserved_hashes = {path: sha256(ROOT / path) for path in PRESERVED}
    local_evidence_hashes = {path: sha256(ROOT / path) for path in LOCAL_EVIDENCE}
    for expected_set, observed_set, label in (
        (PROTECTED, protected_hashes, "protected"),
        (PRESERVED, preserved_hashes, "preserved"),
        (LOCAL_EVIDENCE, local_evidence_hashes, "local evidence"),
    ):
        for path, expected in expected_set.items():
            if observed_set[path] != expected:
                errors.append(f"{label} hash mismatch: {path}")

    failure_lines = [line for line in FAILED_OUTPUT.read_text(encoding="utf-8").splitlines() if line]
    if len(failure_lines) != 11:
        errors.append("failed checkpoint output must contain exactly eleven findings")
    for path in PROTECTED:
        matches = [line for line in failure_lines if line.startswith(f"{path}:") and line.endswith("new blank line at EOF.")]
        if len(matches) != 1:
            errors.append(f"failed checkpoint finding mismatch: {path}")

    observed_attributes = check_attributes([*PROTECTED, CONTROL])
    for path in PROTECTED:
        if observed_attributes.get(path) != ATTRIBUTE_VALUE:
            errors.append(f"unexpected whitespace attribute for {path}")
    if observed_attributes.get(CONTROL) != "unspecified":
        errors.append(f"control path must remain unspecified: {CONTROL}")

    isolated = isolated_diff_proof(attribute_text)
    if isolated["intended_returncode"] != 0 or isolated["intended_output"]:
        errors.append("intended paths did not pass isolated git diff --check")
    if isolated["control_returncode"] == 0 or "blank line at EOF" not in str(isolated["control_output"]):
        errors.append("unrelated control did not retain the blank-at-EOF failure")
    if isolated["combined_returncode"] == 0 or CONTROL not in str(isolated["combined_output"]):
        errors.append("combined isolated proof did not retain the control failure")
    if any(path in str(isolated["combined_output"]) for path in PROTECTED):
        errors.append("combined isolated proof reported an intended protected path")

    return {
        "schema_id": "p15_t07_exact_path_whitespace_policy_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260803-001",
        "source_task_id": "RT-20260802-010",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "gitattributes_sha256": sha256(attributes_path),
        "required_rules": required_lines,
        "preserved_preexisting_rules": PREEXISTING_EXACT_RULES,
        "observed_attributes": observed_attributes,
        "protected_hashes": protected_hashes,
        "preserved_hashes": preserved_hashes,
        "local_evidence_hashes": local_evidence_hashes,
        "failed_checkpoint_finding_count": len(failure_lines),
        "isolated_diff_proof": isolated,
        "claim_limits": {
            "protected_payload_changed": False,
            "p16_t01_executed": False,
            "external_action_performed": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
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
        REPORT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
