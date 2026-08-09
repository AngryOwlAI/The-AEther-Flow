#!/usr/bin/env python3
"""Validate the one-field V22 P2-T01 inherited taxonomy recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-006"
TARGET = ROOT / "research_control/tasks/RT-20260804-001/00_TASK.yaml"
COMPARABLE = ROOT / "research_control/tasks/RT-20260803-014/00_TASK.yaml"
POLICY = ROOT / "research_control/design/v21_task_taxonomy_policy.md"
TAXONOMY_TEST = ROOT / "tests/test_task_taxonomy.py"
MANIFEST = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p2_t01_checkpoint.txt"
VALIDATION = TASK_DIR / "artifacts/v22_p2_t01_taxonomy_checkpoint_recovery_validation.json"
RECEIPT = TASK_DIR / "artifacts/v22_p2_t01_taxonomy_checkpoint_recovery_receipt.json"

OLD_LINE = '  result_kind: "qualifying_bounded_audit_verdict"\n'
NEW_LINE = '  result_kind: "audit_verdict_or_precise_repair"\n'
EXPECTED_HEAD = "b1dd6195bb963ab02780e24c089d545cb8319cee"
EXPECTED_PREIMAGE = "9647114ee7d259d155d61aa7c476d17522927f3978bfea146345609059b720cf"
EXPECTED_MANIFEST = "58fca4eeecf5fc7d8eea4f4c46b64921154617c86a8149529819ddd7a535ec50"
EXPECTED_HASHES = {
    "research_control/design/v21_task_taxonomy_policy.md": "7460702270a26079f39f64ced2b5934e6a67a721983d913e4d3d114917ecca0b",
    "research_control/tasks/RT-20260803-014/00_TASK.yaml": "655801d0fba61821ebcc41f170792b25ff66900f2598bd9fba642dcc0b46cc72",
    "tests/test_task_taxonomy.py": "fb1fdcdf8a936b282cb00025868cfc9887709d03f372be9c547f465251832804",
    "research_control/design/v22_recommendation_backlog.yaml": "d7d33ad808cded6cb429d6bc4ead72c4e1593550f24eb4ff67d11f1f539f6d58",
    "research_control/handoffs/handoff-0975.yaml": "5d0a708da483f567d7329a9f0c4623192ab3095663062a8f47cb2f8726fa595d",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_local_source_information_capacity_theorem_v1.tex": "2ba813e4e961b9ea2709a31c6e06152b1cb4d50ebd90185c2ed93d7aeb132439",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_capacity_validation.json": "0f5400de250218eca95d5c78ff2b4a8e062bd41f08eee93f581156ae9c708d4f",
    "research_control/tasks/RT-20260809-005/artifacts/v22_p2_t01_compact_receipt.json": "330d1f1982b4cd6e1d3861c20cfdbbc858baaadff642ec586a45552902dd9663",
    "research_control/tasks/RT-20260809-005/jobs/completions/AJC-AJ-RT-20260809-005-001.yaml": "087086ab7b5840209601794e9b66d0c29d466bbc65e05b22490a786760ea0d5d",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )


def validate() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def record(check_id: str, passed: bool, detail: object) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    target_bytes = TARGET.read_bytes()
    target_text = target_bytes.decode("utf-8")
    record("replacement_occurs_exactly_once", target_text.count(NEW_LINE) == 1, target_text.count(NEW_LINE))
    record("invalid_value_absent", OLD_LINE not in target_text, OLD_LINE.strip())
    reconstructed = target_bytes.replace(NEW_LINE.encode(), OLD_LINE.encode(), 1)
    reconstructed_hash = sha256_bytes(reconstructed)
    record("whole_file_preimage_reconstruction", reconstructed_hash == EXPECTED_PREIMAGE, reconstructed_hash)

    target_doc = yaml.safe_load(target_text)
    comparable_doc = yaml.safe_load(COMPARABLE.read_text(encoding="utf-8"))
    expected_target = {
        "work_kind": "audit_or_review",
        "milestone": "benchmark_promotion",
        "result_kind": "audit_verdict_or_precise_repair",
        "authority": "project_control",
        "scope": "scientific",
    }
    target_taxonomy = target_doc.get("task_taxonomy", {})
    comparable_taxonomy = comparable_doc.get("task_taxonomy", {})
    record(
        "target_taxonomy_exact",
        all(target_taxonomy.get(key) == value for key, value in expected_target.items()),
        {key: target_taxonomy.get(key) for key in expected_target},
    )
    record(
        "like_for_like_audit_classification",
        all(comparable_taxonomy.get(key) == value for key, value in expected_target.items()),
        {key: comparable_taxonomy.get(key) for key in expected_target},
    )

    policy_text = POLICY.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- v21-task-taxonomy-contract:start -->\s*```json\s*(\{.*?\})\s*```",
        policy_text,
        flags=re.DOTALL,
    )
    policy_contract = json.loads(match.group(1)) if match else {}
    result_vocabulary = policy_contract.get("vocabularies", {}).get("result_kind", [])
    record("policy_contract_parsed", bool(policy_contract), policy_contract.get("schema_id"))
    record("replacement_is_policy_enumerated", "audit_verdict_or_precise_repair" in result_vocabulary, result_vocabulary)
    record("invalid_value_not_policy_enumerated", "qualifying_bounded_audit_verdict" not in result_vocabulary, result_vocabulary)

    observed_hashes: dict[str, str] = {}
    for relative_path, expected_hash in EXPECTED_HASHES.items():
        observed = sha256_path(ROOT / relative_path)
        observed_hashes[relative_path] = observed
        record(f"preserve_sha256::{relative_path}", observed == expected_hash, observed)

    manifest_hash = sha256_path(MANIFEST)
    manifest_lines = [line for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line]
    record("inherited_manifest_sha256", manifest_hash == EXPECTED_MANIFEST, manifest_hash)
    record("inherited_manifest_file_count", len(manifest_lines) == 62, len(manifest_lines))
    record("inherited_manifest_is_sorted", manifest_lines == sorted(manifest_lines), len(manifest_lines))

    head = git("rev-parse", "HEAD").stdout.strip()
    record("source_head_unchanged", head == EXPECTED_HEAD, head)
    cached = git("diff", "--cached", "--quiet")
    record("git_index_clean_precheckpoint", cached.returncode == 0, cached.returncode)

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "v22_p2_t01_taxonomy_checkpoint_recovery_validation_v1",
        "task_id": "RT-20260809-006",
        "job_id": "AJ-RT-20260809-006-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "checks": checks,
        "evidence": {
            "prior_checkpoint": {
                "job_id": "AJ-RT-20260809-005-001",
                "test_count": 1328,
                "failure_count": 1,
                "skipped_count": 1,
                "consumed": True,
                "replayed": False,
                "sole_failure": "tests.test_task_taxonomy.TaskTaxonomyTests.test_repository_report_records_zero_mutation_and_strengthening",
            },
            "target_preimage_sha256": reconstructed_hash,
            "target_postimage_sha256": sha256_bytes(target_bytes),
            "inherited_manifest_sha256": manifest_hash,
            "source_head": head,
            "preserved_hashes": observed_hashes,
        },
        "authority_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "p2_t01_replayed": False,
            "p2_t03_executed": False,
            "p2_t02_external_action_taken": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
        },
    }


def compact_receipt(result: dict[str, object]) -> dict[str, object]:
    evidence = result["evidence"]
    return {
        "schema_id": "v22_p2_t01_taxonomy_checkpoint_recovery_receipt_v1",
        "task_id": "RT-20260809-006",
        "job_id": "AJ-RT-20260809-006-001",
        "status": result["status"],
        "repair": {
            "path": "research_control/tasks/RT-20260804-001/00_TASK.yaml",
            "field": "task_taxonomy.result_kind",
            "old_value": "qualifying_bounded_audit_verdict",
            "new_value": "audit_verdict_or_precise_repair",
            "old_whole_file_sha256": EXPECTED_PREIMAGE,
            "new_whole_file_sha256": evidence["target_postimage_sha256"],
            "other_target_bytes_changed": False,
        },
        "prior_checkpoint": evidence["prior_checkpoint"],
        "inherited_manifest": {
            "path": "research_control/tasks/RT-20260809-006/artifacts/inherited_dirty_manifest_v22_p2_t01_checkpoint.txt",
            "sha256": evidence["inherited_manifest_sha256"],
            "file_count": 62,
        },
        "p2_t01_preserved_hashes": evidence["preserved_hashes"],
        "next_checkpoint": {
            "job_id": "AJ-RT-20260809-006-001",
            "invocation_limit": 1,
            "legacy_validation_allowed": False,
            "invoked": False,
        },
        "next_research_route": {
            "plan_task_id": "P2-T03",
            "selected": True,
            "executed": False,
        },
        "authority_note": "Project-system validation and checkpoint recovery do not change scientific claims, Distance-to-GR, ontology, metric, coupling, Einstein-equation, Gate, benchmark, proof, publication, push, external-action, or completed-derivation authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write:
        VALIDATION.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        RECEIPT.write_text(json.dumps(compact_receipt(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
