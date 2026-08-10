#!/usr/bin/env python3
"""Validate the sealed two-file RT024 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-025"
JOB_ID = "AJ-RT-20260809-025-001"
STRATEGY_ID = "repair_v22_p4_t02_b2_two_eof_blank_lines_and_checkpoint_v1"
ROUTE_SHA256 = "0b14d6c3d1d016ad9f363a153b91df09ff2f3f4b876a43002292f47cb38cd2b9"
BLOCKER_SHA256 = "4b30b0ab8ebc05e0e0cbf6e935e8667ac0dc2f50226305b1ab6a3707ce45b055"
MANIFEST_SHA256 = "7beabab32b3d5211f01c13802702aa814cca8b189d0a5f216f8c1331b84d77c8"
SOURCE_HEAD = "6a585fc6fa73c8bc326e2d1c4e087317c747698d"
SOURCE_TREE = "a2136776d8663d9391ca0347a05f2650619b7678"
BOUNDARY_RECEIPT_SHA256 = "4976519a51a31d25c6cc2f46e856981bf87fece10beada28b65733959aac4729"
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-025"
MANIFEST_PATH = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p4_t02_b2_two_eof_checkpoint_recovery.json"
BLOCKER_PATH = TASK_DIR / "artifacts/v22_p4_t02_b2_two_eof_checkpoint_blocker.yaml"
BOUNDARY_PATH = TASK_DIR / "artifacts/v22_p4_t02_b2_two_eof_repair_boundary_receipt.json"
VALIDATION_PATH = TASK_DIR / "artifacts/v22_p4_t02_b2_two_eof_checkpoint_recovery_validation.json"
CHECKPOINT_RECEIPT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-ccf454970bb530f6/receipt.json"
FAILED_OUTPUT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-ccf454970bb530f6/gates/0006-git_diff_check.stdout"
CHECKPOINT_RECEIPT_SHA256 = "8289376ceeaf208476bec7986ab10b19dd34cb1d2c1246998fd81d62e8c7b04d"
FAILED_OUTPUT_SHA256 = "83727704842057c1b4b4c70c934928106fe548d6ed824ef34cd3769b9280298a"

TARGETS = {
    "research_control/tasks/RT-20260809-023/documentation_impact.yaml": {
        "preimage_sha256": "dfdbff9193e6e00a70d79bef1470e5f887b31a112c94e712d2a54637c80b1133",
        "postimage_sha256": "163a7e33f15c66842292110bc925d369f35572d659eba334648a443508236601",
        "preimage_bytes": 12597,
        "postimage_bytes": 12596,
    },
    "research_control/tasks/RT-20260809-024/documentation_impact.yaml": {
        "preimage_sha256": "ee0b240ae362e8e7ad0a471851c48ee9426a8fc1a3529f0b90197b580d6c0432",
        "postimage_sha256": "37b6ce458346fc5f1d240f15955678cd07502127d048ab013b1536ecc1b86e9e",
        "preimage_bytes": 10505,
        "postimage_bytes": 10504,
    },
}

PROTECTED = {
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex": "6b35e208631b287cd4ec5c6e27bc73c8389c555cad1c8a3cde24021e35be4169",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_equipped_chain_descriptor_population_v1.yaml": "fde2dbbfb1622f6877067408db184d24d477d40acaee953d48585385c4ceeed9",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_atomic_obligation_construction_matrix_v1.yaml": "ce44c482a60ff04f1228ed68d4adbc510f3c4350c2278927ed38e611e5a19219",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_source_factorization_provenance_v1.yaml": "023084b678b9771796652520e1df0c876f2425f622e6431ff59fc2c95d905245",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_explicit_unit_cocycle_v1.yaml": "1e070af78bcb24d426f44123f3186dfbefb6244192cc77cf1983ec095681f07f",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_d7_separation_obstruction_v1.yaml": "95577e04db61fdc37d8597a367dfd0025fbdeb30f8c9ce9e1d86806cb6b52dc2",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_descriptor_construction_model.py": "c5e40b3453b2ecb1b40ce2ddf10caee0984fdc297ecf9a39bff5af6f50cb4660",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_descriptor_construction_validation.json": "c9eefc62a41f1aa08f0d834e6887296c9b6b6d98fd142e05cc70c09638b195ab",
    "research_control/tasks/RT-20260809-023/artifacts/v22_p4_t02_b2_descriptor_construction_compact_receipt.json": "f3ada7680813b437f9522aace462a8c6878ac800f1bcd1e07fef4a48d04608cf",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def load_yaml(relative: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def checkpoint_evidence() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    receipt_hash = sha256_path(CHECKPOINT_RECEIPT_PATH)
    output_hash = sha256_path(FAILED_OUTPUT_PATH)
    payload = json.loads(CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8"))
    failed = [gate for gate in payload.get("gate_results", []) if gate.get("status") == "FAIL"]
    counts = payload.get("counts", {})
    expected_counts = {"gate_count": 7, "pass_count": 2, "fail_count": 1, "skipped_count": 4}
    if receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("checkpoint receipt hash mismatch")
    if output_hash != FAILED_OUTPUT_SHA256:
        errors.append("failed gate output hash mismatch")
    if payload.get("exit_code") != 1 or len(failed) != 1:
        errors.append("checkpoint failure shape mismatch")
    elif failed[0].get("gate_id") != "git_diff_check" or failed[0].get("exit_code") != 2:
        errors.append("checkpoint sole failed gate mismatch")
    if payload.get("final_plan_hash") != "96ee83ebd1906eb554c78276bc3d87b62f67d83f129da9a3399002c75ece7994":
        errors.append("checkpoint final plan hash mismatch")
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            errors.append(f"checkpoint count mismatch: {key}")
    findings = [line for line in FAILED_OUTPUT_PATH.read_text(encoding="utf-8").splitlines() if line]
    if len(findings) != 2:
        errors.append("checkpoint finding count is not two")
    for relative in TARGETS:
        if sum(line.startswith(f"{relative}:") and line.endswith("new blank line at EOF.") for line in findings) != 1:
            errors.append(f"checkpoint output does not name exactly one EOF defect for {relative}")
    return errors, {
        "run_id": payload.get("run_id"),
        "receipt_sha256": receipt_hash,
        "failed_output_sha256": output_hash,
        "final_plan_hash": payload.get("final_plan_hash"),
        "counts": counts,
        "finding_count": len(findings),
        "failed_gate": failed[0] if len(failed) == 1 else {},
    }


def build_boundary_receipt() -> dict[str, Any]:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if sha256_path(MANIFEST_PATH) != MANIFEST_SHA256:
        errors.append("inherited manifest hash mismatch")
    rows = {row["path"]: row for row in manifest.get("paths", [])}
    if manifest.get("path_count") != 78 or len(rows) != 78 or manifest.get("error_count") != 0:
        errors.append("inherited manifest is not the sealed 78-path intake")
    if set(TARGETS) - set(rows):
        errors.append("one or more repair targets are absent from the manifest")

    target_checks: dict[str, Any] = {}
    non_target_mismatches: list[str] = []
    for relative, row in rows.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"manifest path missing: {relative}")
            continue
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if relative in TARGETS:
            expected = TARGETS[relative]
            parses = False
            try:
                parses = yaml.safe_load(data.decode("utf-8")) is not None
            except Exception:
                parses = False
            exact = (
                row.get("working_sha256") == expected["preimage_sha256"]
                and row.get("working_bytes") == expected["preimage_bytes"]
                and observed == expected["postimage_sha256"]
                and len(data) == expected["postimage_bytes"]
                and data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected["preimage_sha256"]
            )
            target_checks[relative] = {
                "preimage_sha256": expected["preimage_sha256"],
                "postimage_sha256": observed,
                "byte_delta": 1,
                "document_parses": parses,
                "ends_with_exactly_one_newline": data.endswith(b"\n") and not data.endswith(b"\n\n"),
                "exact_one_final_newline_removed": exact,
            }
            if not exact or not parses:
                errors.append(f"target is not the exact one-newline postimage: {relative}")
        elif observed != row.get("working_sha256"):
            non_target_mismatches.append(relative)
    if non_target_mismatches:
        errors.append(f"{len(non_target_mismatches)} inherited non-target paths changed before boundary sealing")

    evidence_errors, evidence = checkpoint_evidence()
    errors.extend(evidence_errors)
    protected_checks = {}
    for relative, expected in PROTECTED.items():
        observed = sha256_path(ROOT / relative)
        protected_checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": observed == expected}
        if observed != expected:
            errors.append(f"protected science hash mismatch: {relative}")

    head = git("rev-parse", "HEAD").stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD or tree != SOURCE_TREE:
        errors.append("source commit changed before boundary sealing")
    if not index_clean:
        errors.append("Git index is not clean at the repair boundary")

    return {
        "schema_id": "v22_p4_t02_b2_two_eof_repair_boundary_receipt_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "inherited_manifest": {"path": str(MANIFEST_PATH.relative_to(ROOT)), "sha256": MANIFEST_SHA256, "path_count": len(rows), "target_path_count": len(TARGETS), "non_target_path_count": len(rows) - len(TARGETS)},
        "repair_boundary": {
            "target_checks": target_checks,
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "protected_science": protected_checks,
            "checkpoint_evidence": evidence,
            "git_head": head,
            "git_tree": tree,
            "git_index_clean": index_clean,
        },
        "authority_limits": {
            "semantic_science_changed": False,
            "prior_job_replayed": False,
            "populated_instance_audit_executed": False,
            "p4_t03_executed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "publication_or_push_authorized": False,
            "external_action_authorized": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def changed_paths() -> list[str]:
    result = git("status", "--porcelain=v1", "-z", "--untracked-files=all")
    raw = result.stdout.encode("utf-8", "surrogateescape")
    fields = raw.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(fields) and fields[index]:
        record = fields[index]
        status = record[:2].decode("utf-8", "surrogateescape")
        relative = record[3:].decode("utf-8", "surrogateescape")
        index += 1
        if "R" in status or "C" in status:
            index += 1
        paths.append(relative)
    return sorted(paths)


def build_final_validation() -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    receipt = json.loads(BOUNDARY_PATH.read_text(encoding="utf-8")) if BOUNDARY_PATH.is_file() else {}
    check("boundary_receipt_hash", BOUNDARY_PATH.is_file() and sha256_path(BOUNDARY_PATH) == BOUNDARY_RECEIPT_SHA256, "sealed exact-repair boundary receipt hash")
    check("boundary_receipt_status", receipt.get("status") == "PASS" and receipt.get("error_count") == 0, "boundary receipt has no errors")
    repair = receipt.get("repair_boundary", {})
    check("boundary_non_target_preservation", repair.get("non_target_hash_mismatch_count") == 0, "all 76 inherited non-target paths matched at repair boundary")
    target_checks = repair.get("target_checks", {})
    check("boundary_exact_postimages", set(target_checks) == set(TARGETS) and all(item.get("exact_one_final_newline_removed") for item in target_checks.values()), "both exact one-byte postimages were observed")

    for relative in TARGETS:
        data = (ROOT / relative).read_bytes()
        parses = False
        try:
            parses = yaml.safe_load(data.decode("utf-8")) is not None
        except Exception:
            parses = False
        check(f"current_eof_{Path(relative).parent.name}", data.endswith(b"\n") and not data.endswith(b"\n\n") and parses, f"{relative} is valid YAML ending in exactly one newline")

    for relative, expected in PROTECTED.items():
        check(f"protected_{Path(relative).name}", sha256_path(ROOT / relative) == expected, f"protected science hash {expected}")

    evidence_errors, _ = checkpoint_evidence()
    check("checkpoint_evidence", not evidence_errors, "consumed RT024 checkpoint receipt and two findings remain hash-bound")
    check("manifest_and_blocker", sha256_path(MANIFEST_PATH) == MANIFEST_SHA256 and sha256_path(BLOCKER_PATH) == BLOCKER_SHA256, "manifest and blocker hashes match")

    job = load_yaml("research_control/tasks/RT-20260809-025/jobs/AJ-RT-20260809-025-001.yaml")
    role = load_yaml("research_control/tasks/RT-20260809-025/roles/process-integrity-auditor@0.1.0--RT-20260809-025.yaml")
    check("write_path_parity", job.get("allowed_write_paths") == role.get("allowed_write_paths"), "job and role allowlist order match")
    check("checkpoint_limit", job.get("checkpoint_invocation_limit") == 1 and job.get("checkpoint_invocation_count") == 0 and job.get("prior_failed_checkpoint_replayed") is False, "one fresh checkpoint and no replay")
    recovery = job.get("checkpoint_recovery", {})
    check("checkpoint_recovery_binding", recovery.get("prior_job_id") == "AJ-RT-20260809-024-001" and recovery.get("blocker_sha256") == BLOCKER_SHA256 and recovery.get("source_handoff_sha256") == "088d91eea391b14c83c55da4bd500daeeeaab95591c6af58de336d946f71398a", "exact atomic recovery binding")

    completion = load_yaml("research_control/tasks/RT-20260809-025/jobs/completions/AJC-AJ-RT-20260809-025-001.yaml")
    prior_completion = load_yaml("research_control/tasks/RT-20260809-024/jobs/completions/AJC-AJ-RT-20260809-024-001.yaml")
    check("pending_checkpoint_chain", prior_completion.get("checkpoint_commit", {}).get("status") == "PENDING" and completion.get("checkpoint_commit", {}).get("status") == "PENDING", "prior and recovery completion checkpoint states are pending")

    handoff = load_yaml("research_control/handoffs/handoff-0995.yaml")
    program = load_yaml("research_control/program_state.yaml")
    check("active_state_alignment", program.get("active_task_id") == TASK_ID and program.get("active_agent_job_id") == JOB_ID and program.get("latest_handoff_id") == "handoff-0995" and handoff.get("task_id") == TASK_ID and handoff.get("next_action") == handoff.get("active_state_bifurcation", {}).get("latest_research_next_action"), "program state and handoff-0995 agree")

    live_paths = changed_paths()
    classifier = subprocess.run([str(ROOT / ".venv/bin/python"), "scripts/project_control/classify_project_changes.py", "--json"], cwd=ROOT, text=True, capture_output=True, check=False)
    classifier_payload = json.loads(classifier.stdout) if classifier.returncode == 0 else {}
    check("classifier_path_identity", classifier.returncode == 0 and classifier_payload.get("changed_paths") == live_paths, "classifier covers the exact live transaction")
    for task_id in ("RT-20260809-023", "RT-20260809-024", "RT-20260809-025"):
        impact = load_yaml(f"research_control/tasks/{task_id}/documentation_impact.yaml")
        check(f"documentation_coverage_{task_id}", impact.get("changed_paths") == live_paths and impact.get("generated_derivatives") == classifier_payload.get("generated_only_paths") and impact.get("reason_codes") == classifier_payload.get("reason_codes"), f"{task_id} documentation receipt exactly covers live classifier output")

    eof_findings: list[str] = []
    for relative in live_paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" not in data and data.endswith(b"\n\n"):
            eof_findings.append(relative)
    check("no_candidate_blank_at_eof", not eof_findings, f"candidate blank-at-EOF findings: {eof_findings}")
    check("clean_index", git("diff", "--cached", "--quiet").returncode == 0, "Git index remains clean before checkpoint")

    failures = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "v22_p4_t02_b2_two_eof_checkpoint_recovery_validation_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "repaired_eof_count": 2 if not failures else 0,
        "protected_science_hash_count": len(PROTECTED),
        "inherited_path_count": 78,
        "prior_checkpoint_replayed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_changed": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-boundary", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build_boundary_receipt() if args.emit_boundary else build_final_validation()
    print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.emit_boundary else result["status"])
    return 1 if result.get("status") != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
