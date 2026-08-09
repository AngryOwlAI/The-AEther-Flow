#!/usr/bin/env python3
"""Validate the sealed eleven-file V22 P3-T04 EOF-only checkpoint recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260809-017"
JOB_ID = "AJ-RT-20260809-017-001"
STRATEGY_ID = "repair_v22_p3_t04_eleven_eof_blank_lines_and_checkpoint_v1"
ROUTE_SHA256 = "4e972aeaaaa66e135c4370d950dc74bef7776d54fd2da58c40188a8ee137fa7c"
BLOCKER_FINGERPRINT = "07df0f98c60ef7e24a1099086ef94cca6eee96fde018201705f6d33a081ec407"
MANIFEST_SHA256 = "093446a15f2c0557751d04094cd3c1a0116c0c91cbb4a380facd18b73675cc82"
SOURCE_HEAD = "918cc216b29b83b34eb122c341273dd490657525"
SOURCE_TREE = "618dee8bf2cde810c90719b2ab39de8c1bb5d453"
TASK_DIR = ROOT / "research_control/tasks/RT-20260809-017"
MANIFEST_PATH = TASK_DIR / "artifacts/inherited_dirty_manifest_v22_p3_t04_eleven_eof_checkpoint.txt"
REPORT_PATH = TASK_DIR / "artifacts/v22_p3_t04_eleven_eof_checkpoint_recovery_receipt.json"
VALIDATION_PATH = TASK_DIR / "artifacts/v22_p3_t04_eleven_eof_checkpoint_recovery_validation.json"
CHECKPOINT_RECEIPT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-1ac1a382ca29b5bc/receipt.json"
FAILED_OUTPUT_PATH = ROOT / ".local/validation-receipts/8afbc6d6c1cc892533a3e7f8e45a1e2fb8243d85d803a1dadc854fe5c9fbe844/RUN-CHECKPOINT-1ac1a382ca29b5bc/gates/0006-git_diff_check.stdout"
CHECKPOINT_RECEIPT_SHA256 = "ffd05dd0d023e1d319785cd397d273c65583c3979cbf0a6cf426052d09f112ac"
FAILED_OUTPUT_SHA256 = "137597e27a0e6b2680c9e4db3878b595a7ba45800e73964dcd443fc59513980a"

TARGETS = {
    "research_control/handoffs/handoff-0986.md": (
        "d081cd8b16a564a662326b73f51a581c85a7e6ee04073fe7e6a5fdf8c46dd8f8",
        "e278ef552370bd5cf73b8aabb7528b733c697d4c675c7780236034a2d5086f18",
        "markdown",
    ),
    "research_control/tasks/RT-20260809-016/00_TASK.yaml": (
        "a7502e46772aefc260a319f695de8b437499b8c945853d2b89c09a640d808de0",
        "f3f8ab01dea7a7c46f5024beb6ef29ceb0708cbe4cfdc88fc1addbd69477bf4e",
        "yaml",
    ),
    "research_control/tasks/RT-20260809-016/DDR-20260809-016.md": (
        "224f05af441bda402ccc3616589a4c6f0101c31540389446eb6b6ce77c42bccb",
        "d104c444ae92704dc1e9721f8a80a2f11af3f5e93b04569a7093b72a5974ebbe",
        "markdown",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/child_phys_math_p3_t04_linear_response.yaml": (
        "6923ba600cd04605df80c33b4f2311dbe6344aa950f382e7baa811155d1a85c8",
        "d4cbef1fa21fc8d9963442bf18987f0004847ba6f68b26246f3dd122225e346a",
        "yaml",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/child_phys_phil_p3_t04_smuggling_refutation.yaml": (
        "5e11e0a53f3de0e2cdcd4a7b08df09d22e9af6a044e6f0f64cba5b2e682fb43a",
        "bcb7874370001300ea3316f55b1ce55a720601eafc783c9b5e0496038dae05a0",
        "yaml",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/fixtures/v22_p3_t04_background_linear_response_cases.yaml": (
        "8b9167f561f7eb244d8cdb36d6898858c5709581cc3fa794fd586dcc5c50f715",
        "336f8172a5866000eefa975287fd32b2f9b19c65e27f754f9d80877759a0b6ce",
        "yaml",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/parent_conflict_review_p3_t04_linear_response.yaml": (
        "3c5c0d844496141b688f4fe654c79e279eda216085a32de2076b0940b05b2a5b",
        "150d35d19c8738fe4be4b23425b100a58fee11102f8dbe243a578f38ab351428",
        "yaml",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/parent_fusion_notes_p3_t04_linear_response.md": (
        "27f15ca1dd64f61d497ea80d50b1d9f2042f54b56805b71d1498db814adab8a9",
        "a2a033d8193242f17d78384f5da45b43b12f090fad70ace4f0a24fd9b4ee0584",
        "markdown",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_latex_compile_receipt.json": (
        "595fe5d4e384460f4cfa4f9695c5ec85c1da4b35075f5c1ac89e70ac35d75319",
        "8a04faccf3c5f07e442a644946b093f98c924c79b5ff6a0b1061747f62f2ea2a",
        "json",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/validate_v22_p3_t04_linear_response.py": (
        "60e772273fcf17a4fed36d2294a23dc6abc96a975f920210fd5f271973c1bedd",
        "1eba6df9868454361d743a475bd3a266c0ef42e37a8d6af1e3eb73de7117fd4d",
        "python",
    ),
    "research_control/tasks/RT-20260809-016/artifacts/validator_engineer_p3_t04_independent_evidence.yaml": (
        "9903dec31094b7c34815bdb2263f18fde0b45b398c1bdf932095b2ed94dfb632",
        "d8692e9723895bf3dec2bad20a6c92ee93a8eb373358e16726cb650c8189dce5",
        "yaml",
    ),
}

CUMULATIVE_DOCUMENTATION_PATH = "research_control/tasks/RT-20260809-016/documentation_impact.yaml"
REQUIRED_RECOVERY_DOCUMENTATION_PATHS = {
    "research_control/handoffs/handoff-0987.md",
    "research_control/handoffs/handoff-0987.yaml",
    "research_control/tasks/RT-20260809-017/00_TASK.yaml",
    "research_control/tasks/RT-20260809-017/DDR-20260809-017.md",
    "research_control/tasks/RT-20260809-017/artifacts/inherited_dirty_manifest_v22_p3_t04_eleven_eof_checkpoint.txt",
    "research_control/tasks/RT-20260809-017/artifacts/p3_t04_eleven_eof_checkpoint_blocker.yaml",
    "research_control/tasks/RT-20260809-017/artifacts/v22_p3_t04_eleven_eof_checkpoint_recovery_receipt.json",
    "research_control/tasks/RT-20260809-017/artifacts/v22_p3_t04_eleven_eof_checkpoint_recovery_validation.json",
    "research_control/tasks/RT-20260809-017/artifacts/validate_v22_p3_t04_eleven_eof_checkpoint_recovery.py",
    "research_control/tasks/RT-20260809-017/documentation_impact.yaml",
    "research_control/tasks/RT-20260809-017/jobs/AJ-RT-20260809-017-001.yaml",
    "research_control/tasks/RT-20260809-017/jobs/completions/AJC-AJ-RT-20260809-017-001.yaml",
    "research_control/tasks/RT-20260809-017/roles/process-integrity-auditor@0.1.0--RT-20260809-017.yaml",
}

PROTECTED_LIVE_PATHS = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/design/v22_recommendation_backlog.yaml": "1bb484a5ea9390d28556b2e248a239fd04a536d63e28610e85f2accf422cd499",
    "research_control/handoffs/handoff-0986.yaml": "7742960f304753054239958a6852980d6ebef608d34c3d67fa370fcf631d6d51",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_background_linear_response_preprincipal_v1.tex": "f2d4307aeaf746dc5df48c14d6ed8eb59d7c4bbfb8afd1e69c1c8b88aa72d6f6",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_background_linear_response_specification_v1.yaml": "3875e2f30c92513b664a11f68001128d5bc675366b92b848ee4850f73a53a464",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_countermodel_adequacy_ledger_v1.yaml": "dc540eb2bc2a230c906601e55984e5d9f9f647855d35259043b57c648f0198d3",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_linear_response_model.py": "3ca66f6b236124257a6ec46b3a6ee18f2e76d4f9df19d2ef2fcb445319f632b3",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_independent_linearization.py": "76abfa2eb37cb873cb294d0f9c9ba461fee704b577afa6cf942dbfe864b0382e",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_linear_response_validation.json": "caa4d1130cb23bf133480d8d997c978d34bed0e00a063d3c5367cd75ffbeb4dc",
    "research_control/tasks/RT-20260809-016/artifacts/v22_p3_t04_compact_receipt.json": "bad862eb7e894658f816e090e9e8881616a6e3500e79928ee30d127ffa5bb97a",
    "research_control/tasks/RT-20260809-016/jobs/AJ-RT-20260809-016-001.yaml": "ab88eaf8f2fdcdee94729dac2d8fb24ba28305c082e1783aa1d5f3664cc2d6bd",
    "research_control/tasks/RT-20260809-016/jobs/completions/AJC-AJ-RT-20260809-016-001.yaml": "000ea94591724880b8236c1dae85629124246e555d9f85009de749fb21bb6606",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)


def load_yaml(relative: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def load_manifest() -> tuple[list[str], dict[str, str]]:
    lines = [line for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines() if line]
    rows: dict[str, str] = {}
    for line in lines:
        relative, digest = line.rsplit("=", 1)
        rows[relative] = digest
    return lines, rows


def document_parses(data: bytes, kind: str, relative: str) -> bool:
    try:
        text = data.decode("utf-8")
        if kind == "yaml":
            return yaml.safe_load(text) is not None
        if kind == "json":
            return json.loads(text) is not None
        if kind == "python":
            compile(text, relative, "exec")
        return True
    except Exception:
        return False


def checkpoint_evidence_errors() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    receipt_hash = sha256_path(CHECKPOINT_RECEIPT_PATH)
    output_hash = sha256_path(FAILED_OUTPUT_PATH)
    if receipt_hash != CHECKPOINT_RECEIPT_SHA256:
        errors.append("checkpoint receipt hash mismatch")
    if output_hash != FAILED_OUTPUT_SHA256:
        errors.append("failed git-diff output hash mismatch")
    receipt = json.loads(CHECKPOINT_RECEIPT_PATH.read_text(encoding="utf-8"))
    failed_gate = next(
        (item for item in receipt.get("gate_results", []) if item.get("gate_id") == "git_diff_check"),
        {},
    )
    counts = receipt.get("counts", {})
    if receipt.get("status") != "FAIL" or receipt.get("exit_code") != 1:
        errors.append("checkpoint receipt does not record the expected failure")
    if failed_gate.get("status") != "FAIL" or failed_gate.get("exit_code") != 2:
        errors.append("git_diff_check gate does not record the expected return code")
    expected_counts = {"gate_count": 7, "pass_count": 2, "fail_count": 1, "skipped_count": 4}
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            errors.append(f"checkpoint count mismatch for {key}")
    output_lines = [line for line in FAILED_OUTPUT_PATH.read_text(encoding="utf-8").splitlines() if line]
    if len(output_lines) != len(TARGETS):
        errors.append(f"expected eleven git-diff findings, observed {len(output_lines)}")
    for relative in TARGETS:
        matches = [line for line in output_lines if line.startswith(f"{relative}:") and line.endswith("new blank line at EOF.")]
        if len(matches) != 1:
            errors.append(f"checkpoint output does not name exactly one EOF finding for {relative}")
    return errors, {
        "receipt_sha256": receipt_hash,
        "failed_output_sha256": output_hash,
        "failed_gate_status": failed_gate.get("status"),
        "failed_gate_exit_code": failed_gate.get("exit_code"),
        "finding_count": len(output_lines),
        "counts": counts,
    }


def build_boundary_receipt() -> dict[str, Any]:
    errors: list[str] = []
    manifest_lines, manifest = load_manifest()
    manifest_hash = sha256_path(MANIFEST_PATH)
    if manifest_hash != MANIFEST_SHA256:
        errors.append("inherited dirty manifest hash mismatch")
    if len(manifest_lines) != 65 or len(manifest) != 65:
        errors.append(f"expected 65 unique manifest paths, observed {len(manifest)}")
    if manifest_lines != sorted(manifest_lines):
        errors.append("inherited dirty manifest is not sorted")
    if set(TARGETS) - set(manifest):
        errors.append("one or more EOF targets are absent from the inherited manifest")

    target_checks: dict[str, Any] = {}
    non_target_mismatches: list[str] = []
    for relative, expected_before in manifest.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"manifest path missing: {relative}")
            continue
        data = path.read_bytes()
        observed = sha256_bytes(data)
        if relative in TARGETS:
            declared_before, expected_after, kind = TARGETS[relative]
            parses = document_parses(data, kind, relative)
            exact_one_newline_removed = (
                expected_before == declared_before
                and observed == expected_after
                and data.endswith(b"\n")
                and not data.endswith(b"\n\n")
                and sha256_bytes(data + b"\n") == expected_before
            )
            target_checks[relative] = {
                "before_sha256": expected_before,
                "after_sha256": observed,
                "byte_delta": 1,
                "document_kind": kind,
                "document_parses": parses,
                "ends_with_exactly_one_newline": data.endswith(b"\n") and not data.endswith(b"\n\n"),
                "exact_one_final_newline_removed": exact_one_newline_removed,
            }
            if not exact_one_newline_removed or not parses:
                errors.append(f"target is not the exact required one-newline deletion: {relative}")
        elif observed != expected_before:
            non_target_mismatches.append(relative)
    if non_target_mismatches:
        errors.append(f"{len(non_target_mismatches)} non-target inherited paths changed before sealing")

    evidence_errors, checkpoint_evidence = checkpoint_evidence_errors()
    errors.extend(evidence_errors)
    protected_checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256_path(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": match}
        if not match:
            errors.append(f"protected P3-T04 hash mismatch: {relative}")

    head = git("rev-parse", "HEAD").stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD:
        errors.append("source HEAD changed before recovery checkpoint")
    if tree != SOURCE_TREE:
        errors.append("source tree changed before recovery checkpoint")
    if not index_clean:
        errors.append("Git index is not clean at the repair boundary")

    return {
        "schema_id": "v22_p3_t04_eleven_eof_checkpoint_recovery_receipt_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "strategy_id": STRATEGY_ID,
        "immutable_route_sha256": ROUTE_SHA256,
        "route_blocker_fingerprint": BLOCKER_FINGERPRINT,
        "source_head": SOURCE_HEAD,
        "source_tree": SOURCE_TREE,
        "source_task_id": "RT-20260809-016",
        "source_job_id": "AJ-RT-20260809-016-001",
        "source_handoff_id": "handoff-0986",
        "inherited_manifest": {
            "path": str(MANIFEST_PATH.relative_to(ROOT)),
            "sha256": manifest_hash,
            "path_count": len(manifest),
            "target_path_count": len(TARGETS),
            "non_target_path_count": len(manifest) - len(TARGETS),
        },
        "repair_boundary": {
            "target_checks": target_checks,
            "non_target_hash_mismatch_count": len(non_target_mismatches),
            "non_target_hash_mismatches": non_target_mismatches,
            "protected_live_paths": protected_checks,
            "checkpoint_evidence": checkpoint_evidence,
            "git_head": head,
            "git_tree": tree,
            "git_index_clean": index_clean,
        },
        "plan_state": {
            "p3_t04_executed": True,
            "p3_t04_replayed": False,
            "p4_t01_selected": True,
            "p4_t01_executed": False,
            "p2_t02_external_review_completed": False,
        },
        "authority_limits": {
            "semantic_payload_changed": False,
            "p3_t04_replayed": False,
            "p4_t01_executed": False,
            "p2_t02_external_action_taken": False,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_push_authorized": False,
            "external_action_authorized": False,
        },
        "error_count": len(errors),
        "errors": errors,
        "validation_status": "PASS" if not errors else "FAIL",
    }


def control_record_errors() -> list[str]:
    errors: list[str] = []
    expected = {
        "research_control/tasks/RT-20260809-017/00_TASK.yaml": ("task_id", TASK_ID, "status", "completed"),
        "research_control/tasks/RT-20260809-017/jobs/AJ-RT-20260809-017-001.yaml": ("job_id", JOB_ID, "status", "completed"),
        "research_control/tasks/RT-20260809-017/jobs/completions/AJC-AJ-RT-20260809-017-001.yaml": ("job_id", JOB_ID, "status", "completed"),
        "research_control/handoffs/handoff-0987.yaml": ("handoff_id", "handoff-0987", "status", "ready_for_v22_p4_t01_after_fresh_checkpoint"),
    }
    for relative, (key1, value1, key2, value2) in expected.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"required recovery control record missing: {relative}")
            continue
        data = load_yaml(relative)
        if data.get(key1) != value1 or data.get(key2) != value2:
            errors.append(f"recovery control record state mismatch: {relative}")
    completion_path = ROOT / "research_control/tasks/RT-20260809-017/jobs/completions/AJC-AJ-RT-20260809-017-001.yaml"
    if completion_path.is_file():
        completion = load_yaml(str(completion_path.relative_to(ROOT)))
        checkpoint = completion.get("checkpoint_commit", {})
        if checkpoint.get("status") != "PENDING" or completion.get("checkpoint_invocation_count") != 0:
            errors.append("recovery completion does not preserve one fresh pending checkpoint")
        prior = completion.get("prior_checkpoint", {})
        if prior.get("consumed") is not True or prior.get("replayed") is not False:
            errors.append("recovery completion does not preserve consumed-checkpoint non-replay")
    state_path = ROOT / "research_control/program_state.yaml"
    if state_path.is_file():
        state = load_yaml("research_control/program_state.yaml")
        if state.get("active_task_id") != TASK_ID or state.get("active_agent_job_id") != JOB_ID or state.get("latest_handoff_id") != "handoff-0987":
            errors.append("program state does not point to the recovery transaction")
    return errors


def check_sealed_receipt() -> dict[str, Any]:
    errors: list[str] = []
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    if report.get("validation_status") != "PASS":
        errors.append("sealed repair-boundary receipt is not PASS")
    if report.get("immutable_route_sha256") != ROUTE_SHA256:
        errors.append("sealed receipt route hash mismatch")
    if report.get("route_blocker_fingerprint") != BLOCKER_FINGERPRINT:
        errors.append("sealed receipt blocker fingerprint mismatch")
    inherited = report.get("inherited_manifest", {})
    if inherited.get("sha256") != MANIFEST_SHA256 or inherited.get("path_count") != 65:
        errors.append("sealed receipt inherited-manifest binding mismatch")
    repair = report.get("repair_boundary", {})
    if repair.get("non_target_hash_mismatch_count") != 0:
        errors.append("sealed receipt records non-target repair-boundary drift")

    target_checks: dict[str, Any] = {}
    sealed_targets = repair.get("target_checks", {})
    for relative, (_, expected_after, kind) in TARGETS.items():
        data = (ROOT / relative).read_bytes()
        observed = sha256_bytes(data)
        sealed_after = sealed_targets.get(relative, {}).get("after_sha256")
        parses = document_parses(data, kind, relative)
        match = observed == expected_after and sealed_after == expected_after and data.endswith(b"\n") and not data.endswith(b"\n\n") and parses
        target_checks[relative] = {
            "expected_repair_boundary_sha256": expected_after,
            "sealed_after_sha256": sealed_after,
            "observed_sha256": observed,
            "document_parses": parses,
            "match": match,
        }
        if not match:
            errors.append(f"live recovered target mismatch: {relative}")

    protected_checks: dict[str, Any] = {}
    for relative, expected in PROTECTED_LIVE_PATHS.items():
        observed = sha256_path(ROOT / relative)
        match = observed == expected
        protected_checks[relative] = {"expected_sha256": expected, "observed_sha256": observed, "match": match}
        if not match:
            errors.append(f"live protected P3-T04 hash mismatch: {relative}")

    missing_documentation_paths: list[str] = []
    documentation_path = ROOT / CUMULATIVE_DOCUMENTATION_PATH
    if documentation_path.is_file():
        documentation = load_yaml(CUMULATIVE_DOCUMENTATION_PATH)
        changed_paths = set(documentation.get("changed_paths", []))
        missing_documentation_paths = sorted(REQUIRED_RECOVERY_DOCUMENTATION_PATHS - changed_paths)
        if missing_documentation_paths:
            errors.append("predecessor documentation impact lacks cumulative recovery coverage")
    else:
        errors.append("predecessor documentation impact is missing")

    head = git("rev-parse", "HEAD").stdout.strip()
    index_clean = git("diff", "--cached", "--quiet").returncode == 0
    if head != SOURCE_HEAD:
        errors.append("source HEAD changed before fresh recovery checkpoint")
    if not index_clean:
        errors.append("Git index is not clean before fresh recovery checkpoint")
    errors.extend(control_record_errors())

    return {
        "schema_id": "v22_p3_t04_eleven_eof_checkpoint_recovery_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "status": "PASS" if not errors else "FAIL",
        "sealed_receipt_sha256": sha256_path(REPORT_PATH),
        "inherited_manifest_sha256": sha256_path(MANIFEST_PATH),
        "target_check_count": len(target_checks),
        "target_checks": target_checks,
        "protected_check_count": len(protected_checks),
        "protected_checks": protected_checks,
        "cumulative_documentation_path": CUMULATIVE_DOCUMENTATION_PATH,
        "missing_recovery_documentation_paths": missing_documentation_paths,
        "source_head": head,
        "git_index_clean": index_clean,
        "prior_checkpoint": {
            "job_id": "AJ-RT-20260809-016-001",
            "run_id": "RUN-CHECKPOINT-1ac1a382ca29b5bc",
            "consumed": True,
            "replayed": False,
            "sole_failure_gate": "git_diff_check",
            "finding_count": 11,
        },
        "plan_state": report.get("plan_state", {}),
        "authority_limits": report.get("authority_limits", {}),
        "error_count": len(errors),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-boundary", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.write_boundary:
        result = build_boundary_receipt()
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        result = check_sealed_receipt()
        if args.write:
            VALIDATION_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not (args.write_boundary or args.write):
        print(json.dumps(result, indent=2, sort_keys=True))
    status = result.get("validation_status", result.get("status"))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
