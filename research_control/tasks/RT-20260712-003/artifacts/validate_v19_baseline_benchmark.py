from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
RECEIPT = ROOT / "research_control/tasks/RT-20260712-003/artifacts/v19_baseline_benchmark.json"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate() -> dict[str, object]:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    errors: list[str] = []

    expected_scalars = {
        "schema_id": "v19_baseline_benchmark_v1",
        "task_id": "RT-20260712-003",
        "job_id": "AJ-RT-20260712-003-001",
        "plan_task_id": "P0-T03",
        "status": "PASS_WITH_BASELINE_CONDITIONS",
        "next_route": "P0-T04",
    }
    for key, expected in expected_scalars.items():
        if data.get(key) != expected:
            errors.append(f"{key}: expected {expected!r}, got {data.get(key)!r}")

    historical = data.get("historical_reference", {})
    for key, expected in {
        "full_suite_seconds": 507.215,
        "dependency_graph_module_seconds": 378.598,
        "research_control_module_seconds": 64.568,
        "memory_module_seconds": 23.880,
        "ci_validation_step_seconds": 1025,
    }.items():
        if historical.get(key) != expected:
            errors.append(f"historical_reference.{key}: expected {expected}")

    repository = data.get("repository_state", {})
    if repository.get("pre_measurement_working_fingerprint") != repository.get("post_restoration_working_fingerprint"):
        errors.append("primary working fingerprint was not restored")
    if not repository.get("primary_workspace_restored"):
        errors.append("primary workspace restoration is not asserted")
    if repository.get("real_git_index_changed"):
        errors.append("real Git index must remain unchanged")

    exact = data.get("exact_current_state_suite", {})
    if (exact.get("tests_run"), exact.get("tests_passed"), exact.get("tests_failed")) != (584, 582, 2):
        errors.append("exact current-state suite counts do not equal 584/582/2")
    if exact.get("status") != "FAIL_BASELINE" or not exact.get("restoration_method"):
        errors.append("exact current-state failure or restoration classification is incomplete")

    repaired = data.get("repaired_clean_clone_suite", {})
    if (repaired.get("status"), repaired.get("tests_run"), repaired.get("tests_passed"), repaired.get("tests_failed")) != ("PASS", 584, 584, 0):
        errors.append("repaired clean-clone suite did not record 584/584 PASS")
    if repaired.get("working_fingerprint_before") != repaired.get("working_fingerprint_after"):
        errors.append("repaired clean-clone fingerprint changed")
    for metric in ("duration_seconds", "subprocess_count", "output_bytes", "cache_hits", "cache_misses"):
        if metric not in repaired:
            errors.append(f"repaired clean-clone metric missing: {metric}")

    focused = data.get("focused_baseline_conditions", {})
    vault = focused.get("local_vault", {})
    if len(vault.get("durations_seconds", [])) != 3 or vault.get("median_duration_seconds") != 0.230888:
        errors.append("sub-second local-vault measurement is not represented by three runs and median")
    for gate in ("dependency_graph", "task_index", "local_vault"):
        if not str(focused.get(gate, {}).get("status", "")).startswith("FAIL"):
            errors.append(f"focused baseline condition missing failure classification: {gate}")

    missing_logs: list[str] = []
    mismatched_logs: list[str] = []
    manifests = list(data.get("raw_measurement_manifests", [])) + list(data.get("raw_log_manifest", []))
    for entry in manifests:
        relative = entry.get("path", "")
        expected = entry.get("sha256", "")
        path = ROOT / relative
        if not relative.startswith(".local/v19-baseline/"):
            errors.append(f"raw evidence path is not under .local/v19-baseline: {relative}")
            continue
        if not path.exists():
            missing_logs.append(relative)
        elif file_hash(path) != expected:
            mismatched_logs.append(relative)
    if missing_logs:
        errors.append(f"missing retained raw evidence: {missing_logs}")
    if mismatched_logs:
        errors.append(f"raw evidence hash mismatch: {mismatched_logs}")

    boundary = data.get("claim_boundary", {})
    if any(boundary.get(key) for key in ("scientific_claims_changed", "physics_promotion_authorized", "proof_authority", "distance_to_gr_changed", "benchmark_result_is_physics_evidence")):
        errors.append("no-physics-authority boundary is not preserved")
    if boundary.get("ordinary_research_handoff_preserved") != "handoff-0740":
        errors.append("handoff-0740 preservation is missing")

    return {
        "schema_id": "v19_baseline_benchmark_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "receipt_path": str(RECEIPT.relative_to(ROOT)),
        "receipt_sha256": file_hash(RECEIPT),
        "raw_measurement_manifest_count": len(data.get("raw_measurement_manifests", [])),
        "raw_log_count": len(data.get("raw_log_manifest", [])),
        "verified_raw_evidence_count": len(manifests) - len(missing_logs) - len(mismatched_logs),
        "errors": errors,
        "next_route": data.get("next_route"),
        "scientific_claims_changed": boundary.get("scientific_claims_changed"),
        "physics_promotion_authorized": boundary.get("physics_promotion_authorized"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = validate()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
