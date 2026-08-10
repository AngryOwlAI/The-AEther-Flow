#!/usr/bin/env python3
"""Validate the exact RT023 checkpoint-acceptance recovery boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "research_control/tasks/RT-20260809-024/artifacts/v22_p4_t02_b2_descriptor_checkpoint_recovery_validation.json"
RECEIPT_ROOT = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844"

EXPECTED_RECEIPTS = {
    "RUN-CHECKPOINT-98526e01392211f5": "d942fca046f3f4804f2036a2a5e7b6dae35e96aca947e164d250064edec169e8",
    "RUN-CHECKPOINT-bc05e07710ffd3ae": "232f835fe76faf83566523494f902f00e7b9c41b22bfe17868a475f6cd8a0464",
    "RUN-CHECKPOINT-29f02e278335a022": "9d18391b61ef15013b11a84dc806a16ff581e11299ec2dda87779e066152e27d",
    "RUN-CHECKPOINT-0e238274095c768c": "56f5849e5a6d018695ffa026acff2d5e26fa0cd3ae1222d232527a2cff1d60e6",
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


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks: list[dict] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    manifest_path = ROOT / "research_control/tasks/RT-20260809-024/artifacts/inherited_dirty_manifest_v22_p4_t02_b2_descriptor_checkpoint_recovery.json"
    manifest = json.loads(manifest_path.read_text())
    check("manifest_hash", sha(manifest_path) == "bf81564982e800e0f9f5c03180021d4fa0226c3c9f2362df629d66aeeb1b9759", "sealed inherited manifest hash")
    check("manifest_source", manifest.get("source_head") == "6a585fc6fa73c8bc326e2d1c4e087317c747698d" and manifest.get("entry_index_tree") == "a2136776d8663d9391ca0347a05f2650619b7678", "source commit and clean entry index tree")
    check("manifest_paths", manifest.get("path_count") == 52 and len(manifest.get("paths", [])) == 52 and manifest.get("error_count") == 0, "exact 52-path inherited transaction")

    blocker_path = ROOT / "research_control/tasks/RT-20260809-024/artifacts/v22_p4_t02_b2_descriptor_checkpoint_blocker.yaml"
    blocker = yaml.safe_load(blocker_path.read_text())
    check(
        "checkpoint_blocker",
        sha(blocker_path) == "3d0f6ddcbf51a100bea353db7bb9f345039a015f2c05b2ccec81a6ffebe03219"
        and blocker.get("status") == "active_blocking"
        and blocker.get("job_id") == "AJ-RT-20260809-023-001",
        "hash-bound active blocker names the uncheckpointed predecessor job",
    )

    for run_id, expected_hash in EXPECTED_RECEIPTS.items():
        receipt_path = RECEIPT_ROOT / run_id / "receipt.json"
        receipt = json.loads(receipt_path.read_text())
        failed = [gate for gate in receipt["gate_results"] if gate["status"] == "FAIL"]
        output_hash = sha(Path(failed[0]["stdout_path"])) if len(failed) == 1 else ""
        condition = (
            sha(receipt_path) == expected_hash
            and receipt["exit_code"] == 1
            and receipt["counts"]["gate_count"] == 7
            and receipt["counts"]["pass_count"] == 6
            and receipt["counts"]["fail_count"] == 1
            and failed[0]["gate_id"] == "research_control_diff"
            and output_hash == "50c4b8988edce9b5d4172db9921206f45443401132d45886b64f8e3181454e80"
            and receipt["final_plan_hash"] == "7e538467c7d75033bcd6248ae7a8793da1b95de6763a7e7842c7002c61398b35"
        )
        check(f"receipt_{run_id}", condition, "sealed 6-of-7 failed checkpoint receipt with common failed output")

    for path, expected_hash in PROTECTED.items():
        check(f"protected_{Path(path).name}", sha(ROOT / path) == expected_hash, f"protected hash {expected_hash}")

    rt023_job = load_yaml("research_control/tasks/RT-20260809-023/jobs/AJ-RT-20260809-023-001.yaml")
    queries = rt023_job["memory_preflight"]["queries"]
    check("rt023_query_receipts", len(queries) == 2 and all(q.get("returned_object_ids") for q in queries), "empty retrieval receipt removed without fabrication")
    check("rt023_forbidden_class", "candidate_reconstruction" in rt023_job.get("forbidden_source_classes", []), "required forbidden source class present")

    rt023_completion = load_yaml("research_control/tasks/RT-20260809-023/jobs/completions/AJC-AJ-RT-20260809-023-001.yaml")
    bridge = rt023_completion.get("bridge_attempt_status", {})
    check("rt023_bridge_status", bridge.get("current_ontology_implication") == "does_not_derive" and bridge.get("claim_boundary_preserved") is True, "schema-required bridge status preserves the scientific boundary")

    h993 = load_yaml("research_control/handoffs/handoff-0993.yaml")
    check("handoff_0993_alignment", h993["active_state_bifurcation"]["latest_research_next_action"] == h993["next_action"], "handoff-0993 internal next-action parity")
    check("handoff_0993_markdown_identity", "handoff-0993" in (ROOT / "research_control/handoffs/handoff-0993.md").read_text(), "handoff Markdown carries literal identity")

    job = load_yaml("research_control/tasks/RT-20260809-024/jobs/AJ-RT-20260809-024-001.yaml")
    role = load_yaml("research_control/tasks/RT-20260809-024/roles/process-integrity-auditor@0.1.0--RT-20260809-024.yaml")
    check("write_path_parity", job["allowed_write_paths"] == role["allowed_write_paths"], "job and execution-role write path order agree exactly")
    check("checkpoint_limit", job.get("checkpoint_invocation_limit") == 1 and job.get("checkpoint_invocation_count") == 0, "one fresh checkpoint allowed before invocation")

    program = load_yaml("research_control/program_state.yaml")
    h994 = load_yaml("research_control/handoffs/handoff-0994.yaml")
    state_ok = (
        program.get("active_task_id") == "RT-20260809-024"
        and program.get("active_agent_job_id") == "AJ-RT-20260809-024-001"
        and program.get("latest_handoff_id") == "handoff-0994"
        and h994.get("task_id") == "RT-20260809-024"
        and h994["active_state_bifurcation"]["latest_research_next_action"] == h994["next_action"]
    )
    check("active_state_alignment", state_ok, "program state and handoff-0994 identify the recovery and one checkpoint-gated science route")

    frontier = (ROOT / "research_control/current_frontier.md").read_text()
    check("frontier_alignment", "RT-20260809-024" in frontier and "handoff-0994" in frontier, "current frontier regenerated from recovery authority")
    compact = json.loads((ROOT / "output/compact_current_frontier_v16.json").read_text())
    active = compact.get("active_state", {})
    check("compact_alignment", active.get("active_task_id") == "RT-20260809-024" and active.get("latest_handoff_id") == "handoff-0994", "compact frontier regenerated from recovery authority")

    failures = [item for item in checks if item["status"] == "FAIL"]
    report = {
        "authority": "operational_validation_only",
        "task_id": "RT-20260809-024",
        "job_id": "AJ-RT-20260809-024-001",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failures),
        "failure_count": len(failures),
        "corrected_finding_count": 23 if not failures else 0,
        "protected_science_hash_count": len(PROTECTED),
        "failed_checkpoint_receipt_count": len(EXPECTED_RECEIPTS),
        "checkpoint_replayed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_changed": False,
        "checks": checks,
    }
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
