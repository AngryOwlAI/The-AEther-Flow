#!/usr/bin/env python3
"""Validate the immutable internal V21 terminal baseline release candidate."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
CREATED_AT = "2026-08-08T21:32:43Z"
BASELINE_COMMIT = "233e5dd7024fc068032d0afe86d85dc25e2246e9"
BASELINE_TREE = "a7d9c9448de8e204643b093878ba4d84bd58f020"
PROPOSED_TAG = "v21-scientific-baseline-233e5dd7"

MANIFEST_PATH = ARTIFACT_DIR / "v21_terminal_baseline_release_manifest_v1.json"
PARTITION_PATH = ARTIFACT_DIR / "v21_terminal_baseline_canonical_derivative_partition_v1.json"
REPRODUCTION_PATH = ARTIFACT_DIR / "v21_terminal_baseline_reproduction_receipt_v1.json"
FREEZE_POLICY_PATH = ARTIFACT_DIR / "v21_terminal_baseline_freeze_policy_v1.md"
RELEASE_NOTES_PATH = ARTIFACT_DIR / "v21_terminal_baseline_release_notes_v1.md"
PROPOSED_TAG_PATH = ARTIFACT_DIR / "v21_terminal_baseline_proposed_tag_v1.yaml"
ARCHIVE_PATH = ARTIFACT_DIR / "v21_terminal_scientific_baseline_release_candidate_v1.tar"
CATALOG_PATH = ARTIFACT_DIR / "v21_terminal_baseline_release_catalog_v1.json"
REPORT_PATH = ARTIFACT_DIR / "v22_p0_t02_baseline_release_validation_v1.json"
COMPACT_PATH = ARTIFACT_DIR / "v22_p0_t02_compact_receipt_v1.json"

CORE_PATHS = {
    "manifest": MANIFEST_PATH,
    "partition": PARTITION_PATH,
    "reproduction": REPRODUCTION_PATH,
    "freeze_policy": FREEZE_POLICY_PATH,
    "release_notes": RELEASE_NOTES_PATH,
    "proposed_tag": PROPOSED_TAG_PATH,
    "archive": ARCHIVE_PATH,
    "catalog": CATALOG_PATH,
}

REQUIRED_CATEGORIES = {
    "distance_to_gr",
    "gate_a",
    "selector_theorem_and_proof_archive",
    "p5_p6_negative_results_and_gate_b",
    "p7_postulate_ledger_and_gate_c",
    "p8_obstruction_and_gate_d",
    "p9_benchmarks_and_gate_e",
    "p13_validation_environment_and_provenance",
    "p15_reproducibility_packages",
    "p16_final_scorecards_and_work_ledger",
}

REQUIRED_PROFILE_IDS = {
    "selector_theorem_validator",
    "lean_selector_kernel_build",
    "selector_manuscript_tex_build",
    "source_dynamics_python_model",
    "p9_benchmark_audit_validator",
}

REQUIRED_NOTES_PHRASES = (
    "Gate B: `NOT_READY`",
    "Gate D: `NOT_READY`",
    "Gate E: `NOT_READY`",
    "six inconclusive, zero pass, zero independent replication",
    "GR is not source-derived",
    "Same-context AI critique is not external human review",
    "The tag has **not** been created",
)

REQUIRED_FREEZE_PHRASES = (
    "demonstrated security or reproducibility defect",
    "distinct superseding release record",
    "preservation of the original baseline",
    "separate human authority before any tag or public-release execution",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts


def git_text(*args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode("utf-8").strip()


def validate() -> tuple[dict[str, Any], dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for name, path in CORE_PATHS.items():
        check(f"exists::{name}", path.is_file(), str(path.relative_to(ROOT)))
    if not all(path.is_file() for path in CORE_PATHS.values()):
        failed = [item["check_id"] for item in checks if item["status"] == "FAIL"]
        report = {
            "schema_id": "v22_p0_t02_baseline_release_validation_v1",
            "status": "FAIL",
            "failed_check_ids": failed,
            "checks": checks,
        }
        return report, {
            "schema_id": "v22_p0_t02_compact_receipt_v1",
            "result_status": "FAIL_MISSING_REQUIRED_OUTPUT",
        }

    manifest = load_json(MANIFEST_PATH)
    partition = load_json(PARTITION_PATH)
    reproduction = load_json(REPRODUCTION_PATH)
    catalog = load_json(CATALOG_PATH)
    proposed_tag = yaml.safe_load(PROPOSED_TAG_PATH.read_text(encoding="utf-8"))
    if not isinstance(proposed_tag, dict):
        proposed_tag = {}
    release_notes = RELEASE_NOTES_PATH.read_text(encoding="utf-8")
    freeze_policy = FREEZE_POLICY_PATH.read_text(encoding="utf-8")

    check(
        "git::baseline_commit",
        git_text("rev-parse", f"{BASELINE_COMMIT}^{{commit}}") == BASELINE_COMMIT,
        BASELINE_COMMIT,
    )
    check(
        "git::baseline_tree",
        git_text("rev-parse", f"{BASELINE_COMMIT}^{{tree}}") == BASELINE_TREE,
        BASELINE_TREE,
    )

    baseline = manifest.get("baseline", {})
    check(
        "manifest::baseline_identity",
        baseline.get("commit") == BASELINE_COMMIT
        and baseline.get("tree") == BASELINE_TREE,
        f"commit={baseline.get('commit')} tree={baseline.get('tree')}",
    )
    expected_source_counts = {"tex": 448, "markdown": 649, "total": 1097}
    check(
        "manifest::canonical_source_counts",
        manifest.get("canonical_source_counts") == expected_source_counts
        and partition.get("canonical_source_counts") == expected_source_counts,
        str(manifest.get("canonical_source_counts")),
    )
    expected_derivative_counts = {
        "pdf": 16,
        "html": 19,
        "wiki": 1132,
        "declared_control_report": 2,
        "total": 1169,
    }
    check(
        "manifest::derivative_counts",
        manifest.get("derivative_counts") == expected_derivative_counts
        and partition.get("derivative_counts") == expected_derivative_counts,
        str(manifest.get("derivative_counts")),
    )

    sources = partition.get("canonical_sources", [])
    derivatives = partition.get("derivatives", [])
    source_ids = {
        item.get("object_id") for item in sources if isinstance(item, dict)
    }
    derivative_ids = {
        item.get("object_id") for item in derivatives if isinstance(item, dict)
    }
    resolvable_ids = source_ids | derivative_ids
    check(
        "partition::unique_source_ids",
        len(source_ids) == len(sources) == 1097,
        f"source_count={len(sources)} unique={len(source_ids)}",
    )
    check(
        "partition::unique_derivative_ids",
        len(derivative_ids) == len(derivatives) == 1169,
        f"derivative_count={len(derivatives)} unique={len(derivative_ids)}",
    )
    derivative_trace_ok = all(
        isinstance(item, dict)
        and bool(item.get("source_object_ids"))
        and all(source_id in resolvable_ids for source_id in item["source_object_ids"])
        for item in derivatives
    )
    check(
        "partition::derivative_traceability",
        derivative_trace_ok
        and partition.get("traceability", {}).get(
            "every_declared_generated_path_has_derivative_row"
        )
        is True,
        "all derivative source IDs resolve and declared generated paths close",
    )

    categories = manifest.get("curated_evidence_categories", {})
    check(
        "manifest::curated_categories",
        isinstance(categories, dict)
        and set(categories) == REQUIRED_CATEGORIES
        and all(categories[name] for name in REQUIRED_CATEGORIES),
        str({name: len(categories.get(name, [])) for name in sorted(REQUIRED_CATEGORIES)}),
    )
    required_category_paths = {
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex",
        "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml",
        "research_control/tasks/RT-20260729-001/artifacts/p7_t08_constitutive_postulate_ledger_v1.yaml",
        "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex",
        "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex",
        "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_science_scorecard.yaml",
        "research_control/tasks/RT-20260804-003/artifacts/v21_p16_t05_system_scorecard.yaml",
        "research_control/tasks/RT-20260804-004/artifacts/v21_p16_t06_final_work_item_status_ledger.json",
        "research_control/tasks/RT-20260724-003/artifacts/reproducible_environment_definition.json",
        "research_control/tasks/RT-20260724-003/artifacts/reproduction_receipt.json",
    }
    curated_paths = {
        item.get("path")
        for entries in categories.values()
        for item in entries
        if isinstance(item, dict)
    }
    check(
        "manifest::required_curated_artifacts",
        required_category_paths <= curated_paths,
        f"required={len(required_category_paths)} resolved={len(required_category_paths & curated_paths)}",
    )

    scientific = manifest.get("scientific_status", {})
    scientific_status_ok = (
        scientific.get("Gate_B") == "NOT_READY"
        and scientific.get("Gate_D") == "NOT_READY"
        and scientific.get("Gate_E") == "NOT_READY"
        and scientific.get("benchmark_case_count") == 6
        and scientific.get("benchmark_inconclusive_count") == 6
        and scientific.get("benchmark_pass_count") == 0
        and scientific.get("independent_replication_count") == 0
        and scientific.get("first_principles_gr_derivation_status")
        == "OPEN_NOT_COMPLETED"
        and scientific.get("gr_source_derived") is False
    )
    check(
        "manifest::negative_scientific_status",
        scientific_status_ok,
        json.dumps(scientific, sort_keys=True),
    )
    check(
        "manifest::authority_limits",
        all(value is False for value in manifest.get("authority_limits", {}).values()),
        json.dumps(manifest.get("authority_limits", {}), sort_keys=True),
    )

    normalized_notes = " ".join(release_notes.split())
    notes_missing = [
        phrase for phrase in REQUIRED_NOTES_PHRASES if phrase not in normalized_notes
    ]
    check(
        "release_notes::calibrated_status",
        not notes_missing,
        f"missing={notes_missing}",
    )
    normalized_freeze = " ".join(freeze_policy.split())
    freeze_missing = [
        phrase for phrase in REQUIRED_FREEZE_PHRASES if phrase not in normalized_freeze
    ]
    check(
        "freeze_policy::superseding_record_only",
        not freeze_missing,
        f"missing={freeze_missing}",
    )

    existing_tags = git_text("tag", "--list", PROPOSED_TAG).splitlines()
    check(
        "tag::proposed_not_created",
        not existing_tags
        and proposed_tag.get("tag_name") == PROPOSED_TAG
        and proposed_tag.get("target_commit") == BASELINE_COMMIT
        and proposed_tag.get("status") == "PROPOSED_NOT_CREATED"
        and proposed_tag.get("tag_creation_authorized") is False
        and proposed_tag.get("public_release_authorized") is False,
        f"existing_tags={existing_tags} status={proposed_tag.get('status')}",
    )

    profiles = reproduction.get("profiles", [])
    profiles_by_id = {
        item.get("profile_id"): item for item in profiles if isinstance(item, dict)
    }
    check(
        "reproduction::five_profiles_pass",
        reproduction.get("status") == "PASS"
        and reproduction.get("profile_count") == 5
        and reproduction.get("passed_profile_count") == 5
        and reproduction.get("failed_profile_count") == 0
        and set(profiles_by_id) == REQUIRED_PROFILE_IDS
        and all(item.get("status") == "PASS" for item in profiles_by_id.values()),
        f"status={reproduction.get('status')} profiles={sorted(profiles_by_id)}",
    )
    theorem = profiles_by_id.get("selector_theorem_validator", {})
    deltas = theorem.get("terminal_source_deltas", [])
    check(
        "reproduction::selector_qualifying_snapshot_disclosure",
        theorem.get("source_snapshot_class") == "p15_t03_qualifying_source_bundle"
        and len(deltas) == 2
        and all(item.get("hashes_differ") is True for item in deltas),
        f"snapshot={theorem.get('source_snapshot_class')} delta_count={len(deltas)}",
    )
    lean = profiles_by_id.get("lean_selector_kernel_build", {})
    check(
        "reproduction::lean_proof_object",
        lean.get("proof_object_reproduced") is True
        and lean.get("proof_object_sha256")
        == "3fff7e0bff2e331400ba52305a2f34e3deb93f2b85ac1e3850a1625ef6bd468a",
        str(lean.get("proof_object_sha256")),
    )
    tex = profiles_by_id.get("selector_manuscript_tex_build", {})
    check(
        "reproduction::tex_pdf",
        tex.get("pdf_created") is True and int(tex.get("page_count", 0)) > 0,
        f"pdf_created={tex.get('pdf_created')} pages={tex.get('page_count')}",
    )
    benchmark = profiles_by_id.get("p9_benchmark_audit_validator", {})
    check(
        "reproduction::benchmark_negative_result",
        benchmark.get("reported_status") == "PASS"
        and benchmark.get("benchmark_pass_count") == 0,
        f"reported={benchmark.get('reported_status')} passes={benchmark.get('benchmark_pass_count')}",
    )

    archive_data = ARCHIVE_PATH.read_bytes()
    archive_hash = sha256_bytes(archive_data)
    check(
        "archive::catalog_hash",
        archive_hash == catalog.get("archive", {}).get("sha256")
        and len(archive_data) == catalog.get("archive", {}).get("bytes"),
        f"sha256={archive_hash} bytes={len(archive_data)}",
    )
    with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:") as archive:
        members = archive.getmembers()
        names = [item.name for item in members]
        safe = all(item.isfile() and safe_member(item.name) for item in members)
        fixed_metadata = all(
            item.mtime == 0
            and item.uid == 0
            and item.gid == 0
            and item.mode == 0o644
            for item in members
        )
        member_data = {
            item.name: archive.extractfile(item).read()
            for item in members
            if archive.extractfile(item) is not None
        }
    check(
        "archive::safe_unique_fixed_metadata",
        safe and len(names) == len(set(names)) and fixed_metadata,
        f"member_count={len(names)} safe={safe} fixed_metadata={fixed_metadata}",
    )
    index = json.loads(member_data.get("ARCHIVE_INDEX.json", b"{}").decode("utf-8"))
    index_entries = index.get("entries", []) if isinstance(index, dict) else []
    index_hashes_ok = all(
        item.get("path") in member_data
        and sha256_bytes(member_data[item["path"]]) == item.get("sha256")
        and len(member_data[item["path"]]) == item.get("bytes")
        for item in index_entries
        if isinstance(item, dict)
    )
    check(
        "archive::index_closure",
        index_hashes_ok
        and len(index_entries) == len(member_data) - 1
        and index.get("indexed_member_count") == len(index_entries)
        and catalog.get("archive", {}).get("member_count") == len(member_data),
        f"indexed={len(index_entries)} members={len(member_data)}",
    )

    inventory = manifest.get("repository_archive_inventory", [])
    inventory_paths = [item.get("path") for item in inventory if isinstance(item, dict)]
    inventory_hashes_ok = all(
        f"repository/{item['path']}" in member_data
        and sha256_bytes(member_data[f"repository/{item['path']}"])
        == item.get("sha256")
        and len(member_data[f"repository/{item['path']}"]) == item.get("bytes")
        for item in inventory
        if isinstance(item, dict) and item.get("path")
    )
    check(
        "archive::repository_inventory_closure",
        inventory_hashes_ok and len(inventory_paths) == len(set(inventory_paths)) == 2417,
        f"inventory_count={len(inventory_paths)} unique={len(set(inventory_paths))}",
    )

    release_members = {
        "manifest": "release-control/RELEASE_MANIFEST.json",
        "partition": "release-control/CANONICAL_DERIVATIVE_PARTITION.json",
        "reproduction": "release-control/REPRODUCTION_RECEIPT.json",
        "freeze_policy": "release-control/FREEZE_POLICY.md",
        "release_notes": "release-control/RELEASE_NOTES.md",
        "proposed_tag": "release-control/PROPOSED_TAG.yaml",
    }
    component_closure_ok = True
    for key, archive_name in release_members.items():
        local_data = CORE_PATHS[key].read_bytes()
        component = catalog.get("components", {}).get(key, {})
        component_closure_ok = component_closure_ok and (
            archive_name in member_data
            and member_data[archive_name] == local_data
            and component.get("sha256") == sha256_bytes(local_data)
            and component.get("bytes") == len(local_data)
        )
    check(
        "archive::release_component_closure",
        component_closure_ok,
        f"component_count={len(release_members)}",
    )

    failed = [item["check_id"] for item in checks if item["status"] == "FAIL"]
    report = {
        "schema_id": "v22_p0_t02_baseline_release_validation_v1",
        "validator_id": "VAL-V22-P0-T02-V21-BASELINE-RELEASE-001",
        "task_id": "RT-20260808-002",
        "job_id": "AJ-RT-20260808-002-001",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "failed_check_ids": failed,
        "canonical_source_count": len(sources),
        "derivative_count": len(derivatives),
        "archive_member_count": len(member_data),
        "archive_sha256": archive_hash,
        "reproduction_profile_count": len(profiles_by_id),
        "reproduction_pass_count": sum(
            item.get("status") == "PASS" for item in profiles_by_id.values()
        ),
        "checks": checks,
        "authority_limits": {
            "validator_pass_is_operational_evidence_only": True,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "proof_authority": False,
            "external_review_completed": False,
            "independent_replication_completed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "tag_creation_authorized": False,
            "public_release_authorized": False,
            "publication_authorized": False,
            "push_authorized": False,
            "external_action_authorized": False,
            "completed_derivation_authorized": False,
        },
    }
    compact_sources = {
        str(path.relative_to(ROOT)): sha256_path(path)
        for path in CORE_PATHS.values()
    }
    compact = {
        "schema_id": "v22_p0_t02_compact_receipt_v1",
        "receipt_id": "RECEIPT-V22-P0-T02-V21-BASELINE-001",
        "task_id": "RT-20260808-002",
        "job_id": "AJ-RT-20260808-002-001",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "result_status": (
            "PASS_IMMUTABLE_INTERNAL_V21_BASELINE_RELEASE_CANDIDATE"
            if not failed
            else "FAIL_PRECISE_BASELINE_RELEASE_VALIDATION_BLOCKER"
        ),
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "canonical_source_count": len(sources),
        "derivative_count": len(derivatives),
        "archive_member_count": len(member_data),
        "archive_sha256": archive_hash,
        "reproduction_profile_count": len(profiles_by_id),
        "reproduction_pass_count": report["reproduction_pass_count"],
        "validation_check_count": len(checks),
        "validation_failed_check_count": len(failed),
        "source_hashes": compact_sources,
        "proposed_tag": PROPOSED_TAG,
        "tag_created": False,
        "public_release_created": False,
        "scientific_status_summary": "Gate B D and E NOT_READY; six inconclusive; zero pass; zero independent replication; first-principles GR OPEN_NOT_COMPLETED and not source-derived.",
        "authority_limits": report["authority_limits"],
    }
    return report, compact


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report, compact = validate()
    report_text = json_text(report)
    compact_text = json_text(compact)
    stale: list[str] = []
    if args.write_report:
        REPORT_PATH.write_text(report_text, encoding="utf-8")
        COMPACT_PATH.write_text(compact_text, encoding="utf-8")
    else:
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report_text:
            stale.append(str(REPORT_PATH.relative_to(ROOT)))
        if not COMPACT_PATH.is_file() or COMPACT_PATH.read_text(encoding="utf-8") != compact_text:
            stale.append(str(COMPACT_PATH.relative_to(ROOT)))

    summary = {
        "schema_id": report["schema_id"],
        "status": "PASS" if report["status"] == "PASS" and not stale else "FAIL",
        "check_count": report.get("check_count", 0),
        "failed_check_ids": report.get("failed_check_ids", []),
        "canonical_source_count": report.get("canonical_source_count", 0),
        "derivative_count": report.get("derivative_count", 0),
        "archive_member_count": report.get("archive_member_count", 0),
        "reproduction_pass_count": report.get("reproduction_pass_count", 0),
        "stale_outputs": stale,
        "tag_created": False,
        "public_release_created": False,
        "authority": "operational_release_control_only",
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
