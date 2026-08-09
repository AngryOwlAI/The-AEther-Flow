#!/usr/bin/env python3
"""Seal and validate the bounded V22 P3-T02 staged-acceptance recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-013"
JOB_ID = "AJ-RT-20260809-013-001"
SOURCE_TASK_ID = "RT-20260809-012"
SOURCE_JOB_ID = "AJ-RT-20260809-012-001"
SOURCE_HEAD = "d18637379d0dbde560f1b910255f370fe0c1ce54"
SOURCE_TREE = "55d849173a1b60a78c52a6961e0abd4b8f6af8f5"
ENTRY_INDEX_TREE = "43ed0f91697cbe4d67acfffadfaa46211f65e2aa"
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-013"
MANIFEST_PATH = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p3_t02_staged_acceptance.json"
VALIDATION_PATH = TASK_DIR / "artifacts/v22_p3_t02_staged_acceptance_recovery_validation.json"
CHECKPOINT_RECEIPT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-1f74f450980b9360/receipt.json"
FAILED_OUTPUT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-1f74f450980b9360/gates/0004-research_control_diff.stdout"
CHECKPOINT_RECEIPT_SHA256 = "adfa18dff11b838f1976f30e24a2b07da12afde0e2691eb0e688ad5c0444850f"
FAILED_OUTPUT_SHA256 = "e78bf302cd06956704e4e0bc9afa0ff9092789cb853269c6e89f9097653c0c8e"
SOURCE_DOCUMENTATION_IMPACT_BLOB = "0e24fb2801817c9b2efa9d1f02e854938a62e6b0"
SOURCE_DOCUMENTATION_IMPACT_SHA256 = "b718fb075e4522d6d29b447130aff63e479a705e8bb054a63b457185c02a03e4"

RECOVERY_COVERAGE_PATHS = {
    "research_control/handoffs/handoff-0983.md",
    "research_control/handoffs/handoff-0983.yaml",
    "research_control/tasks/RT-20260809-013/00_TASK.yaml",
    "research_control/tasks/RT-20260809-013/DDR-20260809-013.md",
    "research_control/tasks/RT-20260809-013/artifacts/inherited_dirty_manifest_v22_p3_t02_staged_acceptance.json",
    "research_control/tasks/RT-20260809-013/artifacts/p3_t02_staged_acceptance_checkpoint_blocker.yaml",
    "research_control/tasks/RT-20260809-013/artifacts/v22_p3_t02_staged_acceptance_recovery_validation.json",
    "research_control/tasks/RT-20260809-013/artifacts/validate_v22_p3_t02_staged_acceptance_recovery.py",
    "research_control/tasks/RT-20260809-013/documentation_impact.yaml",
    "research_control/tasks/RT-20260809-013/jobs/AJ-RT-20260809-013-001.yaml",
    "research_control/tasks/RT-20260809-013/jobs/completions/AJC-AJ-RT-20260809-013-001.yaml",
    "research_control/tasks/RT-20260809-013/roles/process-integrity-auditor@0.1.0--RT-20260809-013.yaml",
}

REPAIR_TARGETS = {
    "research_control/tasks/RT-20260809-012/jobs/AJ-RT-20260809-012-001.yaml",
    "research_control/tasks/RT-20260809-012/jobs/completions/AJC-AJ-RT-20260809-012-001.yaml",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
}

PROTECTED_P3_T02 = {
    "research_control/handoffs/handoff-0982.md": "97265e14f91c0f794a4f8a9ca4cf050bee047b8cc6504bcb8896cccc4839dfa7",
    "research_control/handoffs/handoff-0982.yaml": "385886fa86770d3c671307847aaaeb2900db3df2a4aaf62c98708feb0515f8b6",
    "research_control/design/v22_recommendation_backlog.yaml": "37db3df782d53cbb3aca1ff359e54418fe28fa332d3ef57ee37e9f68f645a8fc",
    "research_control/tasks/RT-20260809-012/00_TASK.yaml": "f355e180582eb05009f259cedc084bb21f4d9bc6c13965ff887c7c46d25f2bc8",
    "research_control/tasks/RT-20260809-012/DDR-20260809-012.md": "3285bbce23fce833bdfd6c336d29e7a358e8d1b0b33b7d33f3aac131a3fc33b9",
    "research_control/tasks/RT-20260809-012/artifacts/child_phys_math_p3_t02_source_dynamics.yaml": "ae4523e3c320a8f214813662f3dc44db6530a0f80aca0f84cc24c26bef80366f",
    "research_control/tasks/RT-20260809-012/artifacts/child_phys_phil_p3_t02_source_purity.yaml": "c0e0a6cde16c05e8a9306bcbee7626c9cc7aa2a2779606b97121d4f9e9ea172b",
    "research_control/tasks/RT-20260809-012/artifacts/fixtures/v22_p3_t02_source_dynamics_cases.yaml": "835d6129390002a32ec570bba1694ec3a83675967cf3e9929f52661ed9cc5785",
    "research_control/tasks/RT-20260809-012/artifacts/parent_conflict_review_p3_t02_source_dynamics.yaml": "e9b9f45e24ffba4b912efe631cd99fef6707fc5b5c854abbcf0267716bf7565f",
    "research_control/tasks/RT-20260809-012/artifacts/parent_fusion_notes_p3_t02_source_dynamics.md": "131e7111c06012fb9356fd0bf19b4c0a4d2f6142643d0b520a020ea15bb5bbe9",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_coefficient_provenance_v1.yaml": "0fdf8307c8ca5ec3c96bf9c820b5a46ff3bfae611750f15de27925787bd3484a",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_compact_receipt.json": "39edbdde60ac9996a888f6553648f331cd3ccfaf046833ee9661800e4f310493",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_constraint_identity_ledger_v1.yaml": "5f64d17fa9b7a6fc5c647a8b3093cf7b110d93987e627aa0be9ff3272b70a1a9",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_latex_compile_receipt.json": "f7d615dac79725a0c138e99c99cd4e38199be3980993584db2a8ed64c3356514",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_source_dynamics_specification_v1.yaml": "941e16e8a535622fcbcf6a5ac1802cd4bb86a5950af49260a22d2c69d279f46e",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_source_dynamics_validation.json": "651bc8f00ecc7dbf651a2b7ea4dda8d3f067d6e04e965457da99149142e16893",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_source_dynamics_without_hidden_geometry_v1.tex": "f26c77a175e7a5783e859eacc5de24270e1089a253e73493114a1403bbd61037",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_transport_model.py": "cf3cb7b3dc706ed4d58ca1ce3230a13a63cd5a783fbb0fd50ba0995941d12bd1",
    "research_control/tasks/RT-20260809-012/artifacts/v22_p3_t02_units_debt_wellposedness_v1.yaml": "bc2fc4fc34db8893b68b569a615658b0bd26bd10989af7bcde689f3774cd7338",
    "research_control/tasks/RT-20260809-012/artifacts/validate_v22_p3_t02_source_dynamics.py": "d663819ba480a2fe783e319b5e77df74df46381402a3b4a15d895ddeaa1112ca",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)


def load_yaml(relative: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def capture_manifest() -> dict[str, Any]:
    errors: list[str] = []
    status = git("status", "--porcelain=v1", "-z").stdout
    rows: list[dict[str, Any]] = []
    for entry in status.split(b"\0"):
        if not entry:
            continue
        state = entry[:2].decode("utf-8")
        relative = entry[3:].decode("utf-8")
        if relative.startswith("research_control/tasks/RT-20260809-013"):
            continue
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"inherited path is not a file: {relative}")
            continue
        working = path.read_bytes()
        indexed = git("show", f":{relative}")
        rows.append(
            {
                "path": relative,
                "status": state,
                "working_sha256": sha256_bytes(working),
                "working_bytes": len(working),
                "index_sha256": sha256_bytes(indexed.stdout) if indexed.returncode == 0 else None,
                "index_bytes": len(indexed.stdout) if indexed.returncode == 0 else None,
            }
        )
    rows.sort(key=lambda item: item["path"])
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.decode().strip()
    index_tree = git("write-tree").stdout.decode().strip()
    if len(rows) != 65:
        errors.append(f"expected 65 inherited paths, observed {len(rows)}")
    if head != SOURCE_HEAD or tree != SOURCE_TREE or index_tree != ENTRY_INDEX_TREE:
        errors.append("source HEAD, tree, or restored entry-index tree mismatch")
    folder = next((row for row in rows if row["path"] == "FOLDER_MAP.md"), {})
    if folder.get("status") != "MM" or folder.get("working_sha256") == folder.get("index_sha256"):
        errors.append("FOLDER_MAP.md does not preserve the expected working-only checkpoint refresh")
    receipt_hash = sha256_path(CHECKPOINT_RECEIPT_PATH)
    output_hash = sha256_path(FAILED_OUTPUT_PATH)
    if receipt_hash != CHECKPOINT_RECEIPT_SHA256 or output_hash != FAILED_OUTPUT_SHA256:
        errors.append("failed checkpoint evidence hash mismatch")
    result = {
        "schema_id": "v22_p3_t02_staged_acceptance_inherited_manifest_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "source_head": head,
        "source_tree": tree,
        "entry_index_tree": index_tree,
        "path_count": len(rows),
        "repair_target_paths": sorted(REPAIR_TARGETS),
        "checkpoint_evidence": {
            "run_id": "RUN-CHECKPOINT-1f74f450980b9360",
            "receipt_sha256": receipt_hash,
            "failed_output_sha256": output_hash,
            "consumed": True,
            "replayed": False,
        },
        "paths": rows,
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }
    MANIFEST_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def checkpoint_evidence_errors() -> list[str]:
    errors: list[str] = []
    if sha256_path(CHECKPOINT_RECEIPT_PATH) != CHECKPOINT_RECEIPT_SHA256:
        errors.append("checkpoint receipt hash mismatch")
    if sha256_path(FAILED_OUTPUT_PATH) != FAILED_OUTPUT_SHA256:
        errors.append("failed research-control output hash mismatch")
    receipt = json.loads(CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8"))
    counts = receipt.get("counts", {})
    gates = receipt.get("gate_results", [])
    failed = [gate for gate in gates if gate.get("status") == "FAIL"]
    if receipt.get("status") != "FAIL" or receipt.get("exit_code") != 1:
        errors.append("checkpoint receipt is not the expected failed transaction")
    expected_counts = {"fail_count": 1, "gate_count": 7, "pass_count": 6, "skipped_count": 0}
    if any(counts.get(key) != value for key, value in expected_counts.items()):
        errors.append("checkpoint gate counts differ from the sealed failure")
    if len(failed) != 1 or failed[0].get("gate_id") != "research_control_diff":
        errors.append("research_control_diff is not the sole sealed checkpoint failure")
    failed_text = FAILED_OUTPUT_PATH.read_text(encoding="utf-8")
    try:
        payload = json.loads(failed_text)
    except json.JSONDecodeError:
        errors.append("failed gate output is not JSON")
    else:
        if len(payload.get("errors", [])) != 28:
            errors.append("failed gate output does not contain exactly 28 findings")
    return errors


def repaired_source_errors() -> list[str]:
    errors: list[str] = []
    job = load_yaml("research_control/tasks/RT-20260809-012/jobs/AJ-RT-20260809-012-001.yaml")
    completion = load_yaml("research_control/tasks/RT-20260809-012/jobs/completions/AJC-AJ-RT-20260809-012-001.yaml")
    queries = job.get("memory_preflight", {}).get("queries", [])
    completion_queries = completion.get("memory_preflight", {}).get("queries", [])
    if any(not item.get("returned_object_ids") for item in queries if isinstance(item, dict)):
        errors.append("P3-T02 job retains an empty memory query receipt")
    if any(not item.get("returned_object_ids") for item in completion_queries if isinstance(item, dict)):
        errors.append("P3-T02 completion retains an empty memory query receipt")
    children = {item.get("execution_unit_id"): item for item in job.get("role_decomposition", {}).get("children", [])}
    if children.get("child_phys_math", {}).get("perspective") != "physicist_mathematician":
        errors.append("P3-T02 job mathematical child perspective is not canonical")
    if children.get("child_phys_phil", {}).get("perspective") != "physicist_philosopher":
        errors.append("P3-T02 job philosophical child perspective is not canonical")
    forbidden = set(job.get("forbidden_source_classes", []))
    if "candidate_reconstruction" not in forbidden:
        errors.append("P3-T02 job lacks the candidate_reconstruction source-class block")
    output_children = {item.get("execution_unit_id"): item for item in completion.get("parent_child_synthesis", {}).get("child_outputs", [])}
    if output_children.get("child_phys_math", {}).get("perspective") != "physicist_mathematician":
        errors.append("P3-T02 completion mathematical child perspective is not canonical")
    if output_children.get("child_phys_phil", {}).get("perspective") != "physicist_philosopher":
        errors.append("P3-T02 completion philosophical child perspective is not canonical")
    payload_types = {item.get("payload_type") for item in completion.get("new_mathematical_payload", [])}
    if "construction" in payload_types:
        errors.append("P3-T02 completion retains unsupported construction payload type")
    if completion.get("bridge_attempt_status", {}).get("preserves_blocks") is not True:
        errors.append("P3-T02 completion does not preserve bridge blocks")
    if completion.get("candidate_constructor_result", {}).get("next_required_role") != "refuter":
        errors.append("P3-T02 next required role is not the admitted refuter")
    source_records = completion.get("source_extension_classification", {}).get("records", [])
    if not source_records:
        errors.append("P3-T02 completion lacks a source-extension classification record")
    source_documentation = git("cat-file", "blob", SOURCE_DOCUMENTATION_IMPACT_BLOB)
    if source_documentation.returncode != 0:
        errors.append("sealed P3-T02 documentation-impact baseline blob is unavailable")
    elif sha256_bytes(source_documentation.stdout) != SOURCE_DOCUMENTATION_IMPACT_SHA256:
        errors.append("sealed P3-T02 documentation-impact baseline hash mismatch")
    else:
        baseline_documentation = yaml.safe_load(source_documentation.stdout)
        live_documentation = load_yaml("research_control/tasks/RT-20260809-012/documentation_impact.yaml")
        baseline_paths = set(baseline_documentation.get("changed_paths", []))
        live_paths = set(live_documentation.get("changed_paths", []))
        if live_paths != baseline_paths | RECOVERY_COVERAGE_PATHS:
            errors.append("P3-T02 documentation-impact coverage differs from the sealed baseline plus exact recovery paths")
        baseline_metadata = {key: value for key, value in baseline_documentation.items() if key != "changed_paths"}
        live_metadata = {key: value for key, value in live_documentation.items() if key != "changed_paths"}
        if live_metadata != baseline_metadata:
            errors.append("P3-T02 documentation-impact metadata changed outside cumulative recovery coverage")
    return errors


def role_registry_errors() -> list[str]:
    errors: list[str] = []
    role = load_yaml("research_control/tasks/RT-20260809-012/roles/candidate-constructor@0.2.0--RT-20260809-012.yaml")
    with (ROOT / "registries/ROLE_EXECUTION_REGISTRY.csv").open(encoding="utf-8", newline="") as handle:
        row = next((item for item in csv.DictReader(handle) if item.get("execution_role_ref") == role.get("execution_role_ref")), None)
    if row is None:
        return ["P3-T02 role registry row is missing"]
    expected = {
        "authority_delta_summary": str(role.get("authority_delta_summary", "")),
        "justification": str(role.get("justification", "")),
        "added_constraints": ";".join(str(item) for item in role.get("added_constraints", [])),
    }
    for key, value in expected.items():
        if row.get(key) != value:
            errors.append(f"P3-T02 role registry parity mismatch: {key}")
    return errors


def protected_errors() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_P3_T02.items():
        observed = sha256_path(ROOT / relative)
        match = observed == expected
        checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": match}
        if not match:
            errors.append(f"protected P3-T02 path changed: {relative}")
    return errors, checks


def active_state_errors() -> list[str]:
    errors: list[str] = []
    state = load_yaml("research_control/program_state.yaml")
    handoff = load_yaml("research_control/handoffs/handoff-0983.yaml")
    bifurcation = handoff.get("active_state_bifurcation", {})
    if state.get("active_task_id") != TASK_ID or state.get("active_agent_job_id") != JOB_ID:
        errors.append("program state does not select the recovery task and job")
    if state.get("latest_handoff_id") != "handoff-0983":
        errors.append("program state does not select handoff-0983")
    if bifurcation.get("latest_research_next_action") != handoff.get("next_action"):
        errors.append("handoff-0983 research-next-action bifurcation is inconsistent")
    if bifurcation.get("latest_project_system_task_id") != "none":
        errors.append("handoff-0983 does not preserve the inactive project-system sidecar marker")
    completion = load_yaml("research_control/tasks/RT-20260809-013/jobs/completions/AJC-AJ-RT-20260809-013-001.yaml")
    if completion.get("checkpoint_invocation_count") != 0:
        errors.append("recovery completion does not preserve its one fresh pending checkpoint")
    prior = completion.get("prior_checkpoint", {})
    if prior.get("consumed") is not True or prior.get("replayed") is not False:
        errors.append("recovery completion does not preserve prior checkpoint non-replay")
    return errors


def validate_live() -> dict[str, Any]:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("validation_status") != "PASS" or manifest.get("path_count") != 65:
        errors.append("inherited manifest is not a sealed 65-path PASS")
    if manifest.get("source_head") != SOURCE_HEAD or manifest.get("entry_index_tree") != ENTRY_INDEX_TREE:
        errors.append("inherited manifest source identity mismatch")
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    if head != SOURCE_HEAD:
        errors.append("HEAD changed before the fresh recovery checkpoint")
    errors.extend(checkpoint_evidence_errors())
    errors.extend(repaired_source_errors())
    errors.extend(role_registry_errors())
    protected_failures, protected_checks = protected_errors()
    errors.extend(protected_failures)
    errors.extend(active_state_errors())
    result = {
        "schema_id": "v22_p3_t02_staged_acceptance_recovery_validation_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "source_task_id": SOURCE_TASK_ID,
        "source_job_id": SOURCE_JOB_ID,
        "source_head": head,
        "inherited_manifest_path": str(MANIFEST_PATH.relative_to(ROOT)),
        "inherited_manifest_sha256": sha256_path(MANIFEST_PATH),
        "prior_checkpoint": {
            "run_id": "RUN-CHECKPOINT-1f74f450980b9360",
            "consumed": True,
            "replayed": False,
            "sole_failure_gate": "research_control_diff",
            "finding_count": 28,
        },
        "protected_p3_t02_checks": protected_checks,
        "protected_p3_t02_failure_count": len(protected_failures),
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "checkpoint_invocation_limit": 1,
        "error_count": len(errors),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.capture:
        result = capture_manifest()
    else:
        result = validate_live()
        if args.write:
            VALIDATION_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not (args.capture or args.write):
        print(json.dumps(result, indent=2, sort_keys=True))
    status = result.get("validation_status", result.get("status"))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
