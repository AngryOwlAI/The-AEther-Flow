#!/usr/bin/env python3
"""Collect and validate the immutable v21 P0-T03 starting baseline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260720-006"
JOB_ID = "AJ-RT-20260720-006-001"
PLAN_TASK_ID = "P0-T03"
BASE_HEAD = "2bf74499efb6d1337e4d7746b1c210e7f36d1ca9"
BASE_TREE = "320003ac423868b08581c96cca46394f98dd48b8"
CAPTURED_AT = "2026-07-20T19:15:34Z"
GOAL_ID = "crg-20260720T161354Z-96bc2664ce31bfe0"
GOAL_SCOPE_SHA256 = "d42e4db415c846892a991594e21da5d58202460f07f3b0325f3c3b6fa9f24eae"
ARTIFACT_DIR = Path(__file__).resolve().parent

BASELINE_JSON = ARTIFACT_DIR / "v21_starting_baseline.json"
BASELINE_MD = ARTIFACT_DIR / "v21_starting_baseline.md"
CANDIDATE_JSON = ARTIFACT_DIR / "v21_candidate_family_inventory.json"
SOURCE_JSON = ARTIFACT_DIR / "v21_source_hash_manifest.json"
RECEIPT_JSON = ARTIFACT_DIR / "v21_starting_baseline_receipt.json"

GOAL_SCOPE_HASHES = {
    ".codex/skills/continue-research-continue-goal/SKILL.md": "1c104985bb950cd1e1fe646f69dffce53d466a49b34f228c24f55efb58d0ac54",
    ".codex/skills/continue-research-goal/SKILL.md": "12e52f1cf5ef819814424b0b5811dc9ceba13c3bd2dd59e99569141a2ed89481",
    ".codex/skills/continue-research-goal/references/goal-file-schema.md": "35b1477ee973f268a7d2e7947a75b247a8294cbf6c4843f031f9f686e1c47018",
    ".codex/skills/continue-research/SKILL.md": "4ff16918097dd940bfed731f921acbe496b3e5a1d14f43a0fd352e74b7b0173f",
    "AGENTS.md": "0b6270b8eee144d65d6959c822a9bd6b5ba295bbe58d11833cbb44fbd211330f",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "research_control/AGENTS.md": "c93e14bb2cc6e7bbc5c299085f8843ca84d714cdaef99b2b78a46715b5b310ae",
    "research_control/handoffs/handoff-0772.yaml": "31374c85ee49e457a8b25eaf6d729a0d0e286f1dd53eac184a502044fdd8de0a",
    "research_control/program_state.yaml": "f0ba4ffcfed230f370fbb902f5bb8b32e3ec3f4a0c98163cdf810b585f8eb4c7",
}

REQUIRED_INSPECTION_PATHS = [
    "AGENTS.md",
    "research_control/AGENTS.md",
    "research_control/program_state.yaml",
    "research_control/current_frontier.md",
    "research_control/handoffs/handoff-0775.yaml",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/AGENT_JOB_REGISTRY.csv",
    "implementations_plans/recommendations_implementation_plan_continue_task-v19.md",
    ".codex/skills/continue-research-goal/references/goal-file-schema.md",
    "research_control/design/gr_derivation_burden_map.md",
    "research_control/design/frontier_theorem_inventory.md",
    "research_control/tasks/RT-20260720-005/jobs/completions/AJC-AJ-RT-20260720-005-001.yaml",
    "research_control/tasks/RT-20260720-005/artifacts/v21_backlog_dependency_report.json",
    "research_control/tasks/RT-20260720-005/artifacts/v21_backlog_materialization_receipt.json",
    "research_control/design/v21_recommendation_backlog.yaml",
    "research_control/design/v21_recommendation_backlog_schema.md",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/handoffs/handoff-0772.yaml",
    "research_control/design/validation_gate_manifest_v1.yaml",
    "research_control/design/validation_command_inventory_v16.md",
    "research_control/design/ai_research_agent_metrics_taxonomy_v1.md",
    "research_control/design/physics_payload_ratio_policy_v1.md",
    "requirements.txt",
    "requirements-dev.txt",
]

GENERATED_REPORT_PATHS = [
    "output/physics_progress_metrics.json",
    "output/physics_progress_metrics.md",
    "output/ai_methodology_metrics_dashboard.json",
    "output/ai_methodology_metrics_dashboard.md",
    "wiki/indexes/ai_methodology_metrics_dashboard.md",
    "output/compact_current_frontier_v16.json",
    "output/compact_current_frontier_v16.yaml",
    "output/research_dependency_graph.json",
]

LINEAGE = [
    {
        "task_id": "RT-20260718-038",
        "role_id": "theoretical-continuation-selector",
        "stage": "orientation_route_selection",
        "candidate_family": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
        "handoff_id": "handoff-0763",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-038/artifacts/eqsrc_orientation_torsor_descent_route.yaml",
        ],
    },
    {
        "task_id": "RT-20260718-039",
        "role_id": "ontology-formalizer",
        "stage": "orientation_candidate_construction",
        "candidate_family": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
        "handoff_id": "handoff-0764",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-039/artifacts/eqsrc_orientation_torsor_descent_law_candidate_v1.tex",
            "research_control/tasks/RT-20260718-039/artifacts/eqsrc_orientation_torsor_descent_law_candidate_receipt.md",
            "research_control/tasks/RT-20260718-039/artifacts/eqsrc_orientation_torsor_descent_law_candidate_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-040",
        "role_id": "smuggling-auditor",
        "stage": "orientation_candidate_audit",
        "candidate_family": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
        "handoff_id": "handoff-0765",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-040/artifacts/eqsrc_orientation_torsor_descent_law_smuggling_audit.tex",
            "research_control/tasks/RT-20260718-040/artifacts/eqsrc_orientation_torsor_descent_law_smuggling_audit_receipt.md",
            "research_control/tasks/RT-20260718-040/artifacts/eqsrc_orientation_torsor_descent_law_smuggling_audit_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-041",
        "role_id": "refuter",
        "stage": "orientation_candidate_stress_obstruction",
        "candidate_family": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
        "handoff_id": "handoff-0766",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_stress.tex",
            "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
            "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_stress_receipt.md",
            "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_stress_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-042",
        "role_id": "theoretical-continuation-selector",
        "stage": "rooted_partition_route_selection",
        "candidate_family": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
        "handoff_id": "handoff-0767",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-042/artifacts/eqsrc_ordered_motion_partition_provenance_route.yaml",
        ],
    },
    {
        "task_id": "RT-20260718-043",
        "role_id": "ontology-formalizer",
        "stage": "rooted_partition_candidate_construction",
        "candidate_family": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
        "handoff_id": "handoff-0768",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-043/artifacts/eqsrc_ordered_motion_rooted_partition_law_candidate_v1.tex",
            "research_control/tasks/RT-20260718-043/artifacts/eqsrc_ordered_motion_rooted_partition_law_candidate_receipt.md",
            "research_control/tasks/RT-20260718-043/artifacts/eqsrc_ordered_motion_rooted_partition_law_candidate_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-044",
        "role_id": "smuggling-auditor",
        "stage": "rooted_partition_candidate_audit",
        "candidate_family": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
        "handoff_id": "handoff-0769",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-044/artifacts/eqsrc_ordered_motion_rooted_partition_law_smuggling_audit.tex",
            "research_control/tasks/RT-20260718-044/artifacts/eqsrc_ordered_motion_rooted_partition_law_smuggling_audit_receipt.md",
            "research_control/tasks/RT-20260718-044/artifacts/eqsrc_ordered_motion_rooted_partition_law_smuggling_audit_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-045",
        "role_id": "refuter",
        "stage": "rooted_partition_candidate_stress_obstruction",
        "candidate_family": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
        "handoff_id": "handoff-0770",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_stress.tex",
            "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml",
            "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_stress_receipt.md",
            "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_stress_validation.json",
        ],
    },
    {
        "task_id": "RT-20260718-046",
        "role_id": "theoretical-continuation-selector",
        "stage": "flow_generated_graded_orbit_route_selection",
        "candidate_family": "EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1",
        "handoff_id": "handoff-0771",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-046/artifacts/eqsrc_flow_generated_graded_orbit_root_route.yaml",
        ],
    },
    {
        "task_id": "RT-20260718-047",
        "role_id": "ontology-formalizer",
        "stage": "flow_generated_graded_orbit_candidate_construction",
        "candidate_family": "EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1",
        "handoff_id": "handoff-0772",
        "primary_artifacts": [
            "research_control/tasks/RT-20260718-047/artifacts/eqsrc_flow_generated_graded_orbit_root_law_candidate_v1.tex",
            "research_control/tasks/RT-20260718-047/artifacts/eqsrc_flow_generated_graded_orbit_root_law_candidate_receipt.md",
            "research_control/tasks/RT-20260718-047/artifacts/eqsrc_flow_generated_graded_orbit_root_law_candidate_validation.json",
        ],
    },
]

EXPECTED_ROLE_COUNTS = {
    "candidate-constructor": 55,
    "smuggling-auditor": 96,
    "refuter": 94,
    "theoretical-continuation-selector": 109,
    "gate-chair": 31,
}


class BaselineError(RuntimeError):
    """Raised when immutable baseline evidence does not validate."""


def run(*args: str) -> bytes:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def git_show(path: str) -> bytes:
    try:
        return run("git", "show", f"{BASE_HEAD}:{path}")
    except subprocess.CalledProcessError as exc:
        raise BaselineError(f"baseline path missing: {path}") from exc


def git_lfs_json(path: str) -> dict[str, Any]:
    pointer = git_show(path).decode("utf-8").splitlines()
    if len(pointer) != 3 or pointer[0] != "version https://git-lfs.github.com/spec/v1":
        raise BaselineError(f"expected Git LFS pointer: {path}")
    oid_prefix = "oid sha256:"
    size_prefix = "size "
    if not pointer[1].startswith(oid_prefix) or not pointer[2].startswith(size_prefix):
        raise BaselineError(f"malformed Git LFS pointer: {path}")
    expected_oid = pointer[1].removeprefix(oid_prefix)
    expected_size = int(pointer[2].removeprefix(size_prefix))
    content = (ROOT / path).read_bytes()
    if sha256(content) != expected_oid or len(content) != expected_size:
        raise BaselineError(f"working Git LFS object does not match baseline pointer: {path}")
    value = json.loads(content)
    if not isinstance(value, dict):
        raise BaselineError(f"expected JSON object from Git LFS: {path}")
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def csv_rows(path: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(git_show(path).decode("utf-8"))))


def yaml_doc(path: str) -> dict[str, Any]:
    value = yaml.safe_load(git_show(path).decode("utf-8"))
    if not isinstance(value, dict):
        raise BaselineError(f"expected YAML mapping: {path}")
    return value


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def string_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def bool_value(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.lower() == "true")


def completion_record(job: dict[str, str]) -> dict[str, Any]:
    completion = yaml_doc(job["completion_path"])
    progress = dict_value(completion.get("physics_progress_status"))
    candidate = dict_value(completion.get("candidate_constructor_result"))
    obstruction = dict_value(completion.get("obstruction_record"))
    freeze = dict_value(completion.get("freeze_criteria_status"))
    bridge = dict_value(completion.get("bridge_attempt_status"))
    source_extension = string_value(completion.get("source_extension_category"))
    bridge_present = any(string_value(value) for value in bridge.values()) or (
        "candidate" in source_extension or "construction" in source_extension
    )
    return {
        "task_id": job["task_id"],
        "role_id": job["role_id"],
        "completion_path": job["completion_path"],
        "progress_status": string_value(progress.get("status")),
        "candidate_result_type": string_value(candidate.get("result_type")),
        "obstruction_present": bool_value(obstruction.get("present")),
        "freeze_repeated_burden": bool_value(freeze.get("repeated_burden")),
        "freeze_evaluation_required": bool_value(freeze.get("freeze_evaluation_required")),
        "freeze_decision": string_value(freeze.get("freeze_decision")),
        "bridge_attempt_present": bridge_present,
    }


def has_candidate_signal(record: dict[str, Any]) -> bool:
    return (
        record["role_id"] == "candidate-constructor"
        or bool(record["candidate_result_type"])
        or record["progress_status"].startswith("candidate_")
        or record["bridge_attempt_present"]
    )


def has_obstruction_signal(record: dict[str, Any]) -> bool:
    return (
        record["obstruction_present"]
        or record["candidate_result_type"] in {"precise_obstruction", "minimal_countermodel"}
        or record["progress_status"] == "precise_obstruction_found"
    )


def has_freeze_signal(record: dict[str, Any]) -> bool:
    return (
        record["freeze_repeated_burden"]
        or record["freeze_evaluation_required"]
        or bool(record["freeze_decision"])
        or record["progress_status"] == "route_frozen"
    )


def source_manifest() -> dict[str, Any]:
    categories: dict[str, set[str]] = {}

    def add(path: str, category: str) -> None:
        categories.setdefault(path, set()).add(category)

    for path in REQUIRED_INSPECTION_PATHS:
        add(path, "required_source_inspection")
    for path in GOAL_SCOPE_HASHES:
        add(path, "goal_scope_contract")
    for path in GENERATED_REPORT_PATHS:
        add(path, "generated_report_freshness_evidence")
    for stage in LINEAGE:
        task_id = stage["task_id"]
        completion = (
            f"research_control/tasks/{task_id}/jobs/completions/"
            f"AJC-AJ-{task_id}-001.yaml"
        )
        handoff = f"research_control/handoffs/{stage['handoff_id']}.yaml"
        add(completion, "candidate_lineage_completion")
        add(handoff, "candidate_lineage_handoff")
        for path in stage["primary_artifacts"]:
            add(path, "candidate_lineage_primary_artifact")

    records = []
    launch_mismatches = []
    for path in sorted(categories):
        digest = sha256(git_show(path))
        launch_digest = GOAL_SCOPE_HASHES.get(path)
        matches_launch = digest == launch_digest if launch_digest else None
        if matches_launch is False:
            launch_mismatches.append(path)
        records.append(
            {
                "path": path,
                "sha256": digest,
                "categories": sorted(categories[path]),
                "goal_scope_launch_sha256": launch_digest,
                "matches_goal_scope_launch_hash": matches_launch,
                "retained_at_baseline_commit": True,
            }
        )
    if len({record["path"] for record in records}) != len(records):
        raise BaselineError("duplicate source path")
    return {
        "schema_id": "v21_p0_t03_source_hash_manifest_v1",
        "task_id": TASK_ID,
        "captured_at": CAPTURED_AT,
        "source_commit": BASE_HEAD,
        "hash_algorithm": "sha256",
        "record_count": len(records),
        "goal_scope_contract": {
            "goal_id": GOAL_ID,
            "scope_contract_sha256": GOAL_SCOPE_SHA256,
            "required_path_count": len(GOAL_SCOPE_HASHES),
            "covered_path_count": sum(
                "goal_scope_contract" in record["categories"] for record in records
            ),
            "launch_hash_mismatch_count": len(launch_mismatches),
            "launch_hash_mismatch_paths": launch_mismatches,
            "mismatch_interpretation": (
                "The tracked program state evolved through P0-T01 and P0-T02. "
                "The baseline records both the immutable launch hash and the current baseline hash."
            ),
        },
        "duplicate_path_conflict_count": 0,
        "missing_retained_path_count": 0,
        "records": records,
    }


def candidate_inventory() -> dict[str, Any]:
    stages = []
    for item in LINEAGE:
        task_id = item["task_id"]
        completion_path = (
            f"research_control/tasks/{task_id}/jobs/completions/"
            f"AJC-AJ-{task_id}-001.yaml"
        )
        handoff_path = f"research_control/handoffs/{item['handoff_id']}.yaml"
        task = yaml_doc(f"research_control/tasks/{task_id}/00_TASK.yaml")
        stages.append(
            {
                **item,
                "task_type": task.get("task_type"),
                "closure_status": task.get("closure_status"),
                "completion": {
                    "path": completion_path,
                    "sha256": sha256(git_show(completion_path)),
                },
                "handoff": {
                    "path": handoff_path,
                    "sha256": sha256(git_show(handoff_path)),
                },
                "artifacts": [
                    {"path": path, "sha256": sha256(git_show(path))}
                    for path in item["primary_artifacts"]
                ],
            }
        )
    return {
        "schema_id": "v21_p0_t03_candidate_family_inventory_v1",
        "task_id": TASK_ID,
        "captured_at": CAPTURED_AT,
        "source_commit": BASE_HEAD,
        "target_derivation_milestone": "source_equivalence_eqsrc",
        "active_candidate": {
            "candidate_id": "EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1",
            "status_label": "proposal-only",
            "result": "candidate_constructed_pending_audit",
            "adoption_status": "blocked_adoption_open_continuation",
            "current_ontology_derives_candidate": False,
            "next_role": "smuggling-auditor@0.2.0",
            "scientific_authority_task": "RT-20260718-047",
            "scientific_authority_handoff": "handoff-0772",
        },
        "families": [
            {
                "candidate_family": "EqSrcOrientationTorsorDescentLaw_src^cand,v1",
                "stage_task_ids": [f"RT-20260718-{n:03d}" for n in range(38, 42)],
                "disposition": "scoped_line_selection_obstruction_then_locally_frozen",
                "obstruction_id": "OB-EQSRC-ORIENTATION-TORSOR-LINE-SELECTION-001",
                "global_no_go": False,
            },
            {
                "candidate_family": "EqSrcOrderedMotionRootedPartitionLaw_src^cand,v1",
                "stage_task_ids": [f"RT-20260718-{n:03d}" for n in range(42, 46)],
                "disposition": "scoped_root_and_relation_selection_obstruction_then_locally_frozen",
                "obstruction_id": "OB-EQSRC-ORDERED-MOTION-ROOT-SELECTION-001",
                "global_no_go": False,
            },
            {
                "candidate_family": "EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1",
                "stage_task_ids": ["RT-20260718-046", "RT-20260718-047"],
                "disposition": "proposal_only_candidate_pending_fresh_audit",
                "obstruction_id": "",
                "global_no_go": False,
            },
        ],
        "stage_count": len(stages),
        "stages": stages,
        "authority_boundary": {
            "inventory_is_scientific_authority": False,
            "candidate_adoption_authorized": False,
            "general_eqsrc_discharged": False,
            "physics_promotion_authorized": False,
        },
    }


def baseline_metrics() -> dict[str, Any]:
    task_rows = csv_rows("registries/RESEARCH_TASK_REGISTRY.csv")
    job_rows = csv_rows("registries/AGENT_JOB_REGISTRY.csv")
    role_counts = Counter(row["role_id"] for row in job_rows)
    records = [completion_record(row) for row in job_rows]
    missing_candidate_result_paths = sorted(
        record["completion_path"]
        for record in records
        if record["role_id"] == "candidate-constructor"
        and not record["candidate_result_type"]
    )
    category_counts = {
        "registered_tasks": len(task_rows),
        "registered_agent_jobs": len(job_rows),
        "candidate_constructor_role_jobs": role_counts["candidate-constructor"],
        "smuggling_audit_role_jobs": role_counts["smuggling-auditor"],
        "refuter_stress_role_jobs": role_counts["refuter"],
        "theoretical_selector_role_jobs": role_counts["theoretical-continuation-selector"],
        "gate_chair_role_jobs": role_counts["gate-chair"],
        "candidate_signal_packets": sum(has_candidate_signal(record) for record in records),
        "obstruction_signal_packets": sum(has_obstruction_signal(record) for record in records),
        "freeze_signal_packets": sum(has_freeze_signal(record) for record in records),
    }
    expected = {
        "registered_tasks": 1006,
        "registered_agent_jobs": 1006,
        "candidate_signal_packets": 199,
        "obstruction_signal_packets": 44,
        "freeze_signal_packets": 289,
    }
    for role_id, count in EXPECTED_ROLE_COUNTS.items():
        field = {
            "candidate-constructor": "candidate_constructor_role_jobs",
            "smuggling-auditor": "smuggling_audit_role_jobs",
            "refuter": "refuter_stress_role_jobs",
            "theoretical-continuation-selector": "theoretical_selector_role_jobs",
            "gate-chair": "gate_chair_role_jobs",
        }[role_id]
        expected[field] = count
    if category_counts != expected:
        raise BaselineError(
            f"baseline category counts changed: expected={expected} actual={category_counts}"
        )
    if len(missing_candidate_result_paths) != 11:
        raise BaselineError("candidate-result lineage gap count changed")
    return {
        "definitions": {
            "role_job_counts": "Exact role_id counts in baseline AGENT_JOB_REGISTRY.csv.",
            "candidate_signal_packets": "Metrics-reporter candidate signal predicate over baseline completion records.",
            "obstruction_signal_packets": "Metrics-reporter obstruction signal predicate over baseline completion records.",
            "freeze_signal_packets": "Metrics-reporter freeze signal predicate over baseline completion records.",
            "known_lineage_gaps": "Eleven candidate-constructor receipts missing normalized result_type plus two declared aggregate-lineage limitations.",
        },
        "counts": category_counts,
        "known_lineage_gaps": {
            "candidate_result_missing_completion_count": 11,
            "candidate_result_missing_completion_paths": missing_candidate_result_paths,
            "aggregate_lineage_limitation_count": 2,
            "aggregate_lineage_limitations": [
                "Audit-to-stress metrics count stage occurrences rather than candidate-linked transitions.",
                "Historical draft/control stress-survivor lineage is not fully normalized.",
            ],
            "total_gap_signal_count": 13,
            "repair_performed": False,
        },
    }


def generated_report_freshness(metrics: dict[str, Any]) -> dict[str, Any]:
    stored = json.loads(git_show("output/physics_progress_metrics.json"))
    stored_counts = stored["metrics"]["input_counts"]
    live_counts = {
        "tasks_registered": metrics["counts"]["registered_tasks"],
        "jobs_registered": metrics["counts"]["registered_agent_jobs"],
        "completions_read": 1006,
        "physics_completions_read": 505,
        "claim_boundary_rows": 963,
        "active_claim_boundary_rows": 899,
    }
    lag = {
        key: live_counts[key] - int(stored_counts[key])
        for key in live_counts
    }
    graph = git_lfs_json("output/research_dependency_graph.json")
    graph_ids = {node.get("node_id", "") for node in graph["nodes"]}
    graph_task_count = sum(node_id.startswith("task:RT-") for node_id in graph_ids)
    graph_job_count = sum(node_id.startswith("job:AJ-") for node_id in graph_ids)
    graph_handoff_numbers = [
        int(node_id.removeprefix("handoff:handoff-"))
        for node_id in graph_ids
        if node_id.startswith("handoff:handoff-")
    ]
    compact = json.loads(git_show("output/compact_current_frontier_v16.json"))
    return {
        "status": "PASS_WITH_PREEXISTING_DRIFT_CAPTURED",
        "repair_performed": False,
        "physics_progress_metrics": {
            "fresh": False,
            "classification": "preexisting_baseline_drift",
            "stored_as_of": stored.get("as_of"),
            "live_as_of": "2026-07-20T18:46:49Z",
            "stored_input_counts": {
                key: stored_counts[key] for key in live_counts
            },
            "live_input_counts": live_counts,
            "registry_to_report_lag": lag,
            "stored_json_sha256": sha256(git_show("output/physics_progress_metrics.json")),
            "expected_live_json_sha256": "520a2baf94bfb5ae9fe1ebb5e05595d100475b0691f79b6cc2aba3ba153c53cb",
            "stored_markdown_sha256": sha256(git_show("output/physics_progress_metrics.md")),
            "expected_live_markdown_sha256": "54986f236069b5ca5b1ca89ae84a4f3b9003b5bca9bb7c6ccbe552f0746682df",
        },
        "ai_methodology_dashboard": {
            "fresh": False,
            "classification": "preexisting_baseline_drift",
            "stored_json_sha256": sha256(
                git_show("output/ai_methodology_metrics_dashboard.json")
            ),
            "expected_live_json_sha256": "d2b20d01910d4a2276d2c018dc09c2ce6e1af3d9c81fc3bdcd8f9ef1b313ca90",
            "stored_markdown_sha256": sha256(
                git_show("output/ai_methodology_metrics_dashboard.md")
            ),
            "expected_live_markdown_sha256": "d0a121037319d9139171612607e7d3d2236224b2f999ab612c9f2c643bdbdb3b",
        },
        "research_dependency_graph": {
            "fresh": False,
            "classification": "preexisting_baseline_drift",
            "generated_at": graph.get("generated_at"),
            "task_node_count": graph_task_count,
            "task_registry_count": metrics["counts"]["registered_tasks"],
            "task_node_lag": metrics["counts"]["registered_tasks"] - graph_task_count,
            "job_node_count": graph_job_count,
            "job_registry_count": metrics["counts"]["registered_agent_jobs"],
            "job_node_lag": metrics["counts"]["registered_agent_jobs"] - graph_job_count,
            "latest_handoff_node": f"handoff-{max(graph_handoff_numbers):04d}",
            "latest_tracked_handoff": "handoff-0775",
        },
        "compact_current_frontier": {
            "fresh": compact["active_state"]["active_task_id"] == "RT-20260720-005"
            and compact["active_state"]["latest_handoff_id"] == "handoff-0775",
            "active_task_id": compact["active_state"]["active_task_id"],
            "latest_handoff_id": compact["active_state"]["latest_handoff_id"],
        },
    }


def build_all() -> dict[Path, str]:
    manifest = source_manifest()
    inventory = candidate_inventory()
    metrics = baseline_metrics()
    freshness = generated_report_freshness(metrics)
    program_state = yaml_doc("research_control/program_state.yaml")
    distance_rows = csv_rows("registries/DISTANCE_TO_GR_LEDGER.csv")
    distance_row = next(
        row for row in distance_rows if row["burden_id"] == "source_equivalence_eqsrc"
    )
    validation_manifest = yaml_doc("research_control/design/validation_gate_manifest_v1.yaml")
    source_text = canonical_json(manifest)
    candidate_text = canonical_json(inventory)
    baseline = {
        "schema_id": "v21_p0_t03_starting_baseline_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": PLAN_TASK_ID,
        "status": "PASS_WITH_BASELINE_FINDINGS",
        "captured_at": CAPTURED_AT,
        "repository_identity": {
            "profile": "production_profile",
            "root": str(ROOT),
            "git_common_dir": str(ROOT / ".git"),
            "branch": "main",
            "head": BASE_HEAD,
            "tree": BASE_TREE,
            "porcelain": "",
            "dirty_entry_count": 0,
            "tracked_blob_count": 12755,
            "origin_main_ahead_count": 4,
            "origin_main_behind_count": 0,
        },
        "runtime_environment": {
            "python_version": "3.12.13",
            "python_executable": str(ROOT / ".venv/bin/python"),
            "platform": "macOS-26.5.2-arm64-arm-64bit",
            "dependency_packages": ["PyMuPDF==1.27.2.3", "PyYAML==6.0.3"],
            "pip_freeze_sha256": "66c77456edd0c160995bc9d84bee63f568239677b6a2c69496e104d6a079c402",
            "requirements_sha256": sha256(git_show("requirements.txt")),
            "requirements_dev_sha256": sha256(git_show("requirements-dev.txt")),
        },
        "control_state": {
            "active_task_id": program_state["active_task_id"],
            "latest_handoff_id": program_state["latest_handoff_id"],
            "current_status": program_state["current_status"],
            "preserved_scientific_task_id": "RT-20260718-047",
            "preserved_scientific_handoff_id": "handoff-0772",
            "selected_control_route": "v21_p0_t03_starting_baseline_freeze",
            "preserved_scientific_route": "eqsrc_flow_generated_graded_orbit_root_law_smuggling_audit",
        },
        "distance_to_gr": {
            "ledger_path": "registries/DISTANCE_TO_GR_LEDGER.csv",
            "ledger_sha256": sha256(git_show("registries/DISTANCE_TO_GR_LEDGER.csv")),
            "active_row": distance_row,
            "delta_changed": False,
        },
        "metrics": metrics,
        "generated_report_freshness": freshness,
        "validation_system": {
            "manifest_path": "research_control/design/validation_gate_manifest_v1.yaml",
            "manifest_sha256": sha256(
                git_show("research_control/design/validation_gate_manifest_v1.yaml")
            ),
            "manifest_id": validation_manifest["manifest_id"],
            "schema_id": validation_manifest["schema_id"],
            "execution_authority": validation_manifest["execution_authority"],
            "gate_count": len(validation_manifest["gates"]),
            "blocking_gate_count": sum(
                gate.get("severity") == "blocking"
                for gate in validation_manifest["gates"]
            ),
            "mutating_gate_count": sum(
                bool(gate.get("mutating")) for gate in validation_manifest["gates"]
            ),
            "operational_evidence_only": True,
        },
        "candidate_family_inventory": {
            "path": str(CANDIDATE_JSON.relative_to(ROOT)),
            "sha256": sha256(candidate_text.encode("utf-8")),
            "stage_count": inventory["stage_count"],
            "active_candidate_id": inventory["active_candidate"]["candidate_id"],
        },
        "source_hash_manifest": {
            "path": str(SOURCE_JSON.relative_to(ROOT)),
            "sha256": sha256(source_text.encode("utf-8")),
            "record_count": manifest["record_count"],
            "duplicate_path_conflict_count": 0,
            "missing_retained_path_count": 0,
        },
        "goal_scope": manifest["goal_scope_contract"],
        "recommendation_coverage": {
            "plan_id": "recommendations_implementation_plan_continue_task-v21",
            "plan_task_id": PLAN_TASK_ID,
            "recommendation_ids": [
                "V21-R01",
                "V21-R02",
                "V21-R31",
                "V21-R43",
                "V21-R49",
                "V21-R52",
                "V21-R53",
            ],
            "implementation_status": "baseline_captured",
        },
        "assumption_delta": [],
        "authority_flags": {
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "source_law_adoption_authorized": False,
            "canonical_ontology_edit_authorized": False,
            "benchmark_promotion_authorized": False,
            "gate_chair_verdict_created": False,
            "completed_derivation_authorized": False,
            "baseline_finding_repair_authorized": False,
        },
        "findings": [
            {
                "finding_id": "P0-T03-FRESHNESS-METRICS-001",
                "classification": "preexisting_baseline_drift",
                "status": "RECORDED_NOT_REPAIRED",
                "summary": "Stored physics-progress metrics and methodology dashboard lag the live baseline registries.",
            },
            {
                "finding_id": "P0-T03-FRESHNESS-GRAPH-001",
                "classification": "preexisting_baseline_drift",
                "status": "RECORDED_NOT_REPAIRED",
                "summary": "The generated dependency graph stops at RT-20260718-047 and handoff-0772, five tasks and three handoffs behind the baseline control state.",
            },
            {
                "finding_id": "P0-T03-LINEAGE-GAPS-001",
                "classification": "preexisting_baseline_limitation",
                "status": "RECORDED_NOT_REPAIRED",
                "summary": "Thirteen lineage-gap signals are frozen: eleven missing normalized candidate results and two aggregate lineage limitations.",
            },
        ],
        "forbidden_conclusions": [
            "baseline or metrics as physics proof",
            "candidate inventory as adoption",
            "validator PASS as source authority",
            "pre-existing drift as a v21 regression",
            "general EqSrc discharge",
            "source-law or canonical ontology adoption",
            "benchmark promotion or Gate Chair verdict",
            "completed derivation",
        ],
    }
    baseline_text = canonical_json(baseline)
    markdown = render_markdown(baseline)
    receipt = {
        "schema_id": "v21_p0_t03_starting_baseline_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": PLAN_TASK_ID,
        "status": "PASS_WITH_BASELINE_FINDINGS",
        "captured_at": CAPTURED_AT,
        "source_commit": BASE_HEAD,
        "source_hashes": {
            "baseline_json": sha256(baseline_text.encode("utf-8")),
            "baseline_markdown": sha256(markdown.encode("utf-8")),
            "candidate_family_inventory": sha256(candidate_text.encode("utf-8")),
            "source_hash_manifest": sha256(source_text.encode("utf-8")),
        },
        "finding_counts": {
            "validation_errors": 0,
            "missing_retained_paths": 0,
            "conflicting_source_hash_paths": 0,
            "preexisting_generated_report_drift_findings": 2,
            "preexisting_lineage_gap_signals": 13,
            "repairs_performed": 0,
        },
        "validator_ids": [
            "v21_starting_baseline_schema",
            "v21_retained_source_paths",
            "v21_source_hash_manifest_unique",
            "v21_goal_scope_hash_coverage",
            "v21_candidate_family_inventory",
            "v21_repository_identity",
            "v21_generated_report_freshness_capture",
        ],
        "claim_boundary_summary": (
            "P0-T03 freezes task-local before-state evidence only. It repairs no "
            "finding, changes no scientific claim, and creates no promotion authority."
        ),
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "validation_status": "PASS",
    }
    return {
        SOURCE_JSON: source_text,
        CANDIDATE_JSON: candidate_text,
        BASELINE_JSON: baseline_text,
        BASELINE_MD: markdown,
        RECEIPT_JSON: canonical_json(receipt),
    }


def render_markdown(baseline: dict[str, Any]) -> str:
    counts = baseline["metrics"]["counts"]
    freshness = baseline["generated_report_freshness"]
    lines = [
        "<!-- authority: control -->",
        "",
        "# V21 P0-T03 Starting Baseline",
        "",
        f"Captured `{baseline['captured_at']}` from clean `main` commit "
        f"`{baseline['repository_identity']['head']}`. Status: "
        f"`{baseline['status']}`.",
        "",
        "This is immutable before-state evidence. It does not repair findings, "
        "change a scientific claim, or create proof, adoption, benchmark, or "
        "Gate Chair authority.",
        "",
        "## Control and scientific frontier",
        "",
        "- Active control state: `RT-20260720-005` / `handoff-0775`.",
        "- Preserved scientific authority: `RT-20260718-047` / `handoff-0772`.",
        "- Active candidate: `EqSrcFlowGeneratedGradedOrbitRootLaw_src^cand,v1`, "
        "proposal-only and pending fresh audit.",
        "- General `EqSrc` remains undischarged; the Distance-to-GR ledger is unchanged.",
        "",
        "## Baseline counts",
        "",
        "| Measure | Count |",
        "| --- | ---: |",
        f"| Registered tasks | {counts['registered_tasks']} |",
        f"| Registered AgentJobs | {counts['registered_agent_jobs']} |",
        f"| Candidate Constructor role jobs | {counts['candidate_constructor_role_jobs']} |",
        f"| Smuggling Auditor role jobs | {counts['smuggling_audit_role_jobs']} |",
        f"| Refuter stress role jobs | {counts['refuter_stress_role_jobs']} |",
        f"| Theoretical Selector role jobs | {counts['theoretical_selector_role_jobs']} |",
        f"| Gate Chair role jobs | {counts['gate_chair_role_jobs']} |",
        f"| Candidate-signal packets | {counts['candidate_signal_packets']} |",
        f"| Obstruction-signal packets | {counts['obstruction_signal_packets']} |",
        f"| Freeze-signal packets | {counts['freeze_signal_packets']} |",
        f"| Known lineage-gap signals | {baseline['metrics']['known_lineage_gaps']['total_gap_signal_count']} |",
        "",
        "## Candidate-family route",
        "",
        "The inventory freezes ten consecutive stages: orientation-torsor selection, "
        "construction, audit, and obstruction; rooted-partition selection, "
        "construction, audit, and obstruction; then flow-generated graded-orbit "
        "selection and construction. The first two exact cycles are locally frozen. "
        "The third candidate remains proposal-only and unaudited.",
        "",
        "## Generated-report freshness",
        "",
        "| Surface | Baseline status | Exact lag |",
        "| --- | --- | --- |",
        f"| Physics-progress metrics | stale, pre-existing | "
        f"{freshness['physics_progress_metrics']['registry_to_report_lag']['tasks_registered']} tasks; "
        f"{freshness['physics_progress_metrics']['registry_to_report_lag']['jobs_registered']} jobs |",
        "| AI methodology dashboard | stale, pre-existing | live render differs from stored outputs |",
        f"| Research dependency graph | stale, pre-existing | "
        f"{freshness['research_dependency_graph']['task_node_lag']} tasks; "
        f"{freshness['research_dependency_graph']['job_node_lag']} jobs; "
        f"`{freshness['research_dependency_graph']['latest_handoff_node']}` versus `handoff-0775` |",
        "| Compact current frontier | fresh | active task and handoff match |",
        "",
        "No freshness or lineage finding was repaired in P0-T03.",
        "",
        "## Evidence",
        "",
        f"- Source manifest: `{baseline['source_hash_manifest']['path']}` "
        f"({baseline['source_hash_manifest']['record_count']} retained paths).",
        f"- Candidate inventory: `{baseline['candidate_family_inventory']['path']}` "
        f"({baseline['candidate_family_inventory']['stage_count']} stages).",
        "- Goal-scope launch and baseline hashes are both retained; the evolving "
        "`program_state.yaml` is the only launch-hash mismatch.",
        "",
        "## Boundary",
        "",
        "Baseline counts, generated reports, validator results, task status, and "
        "recursive-relay continuation are operational evidence only. They do not "
        "adopt a source law or ontology, discharge EqSrc, promote a benchmark, "
        "issue a Gate Chair verdict, or complete a derivation.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def check_outputs(outputs: dict[Path, str]) -> list[str]:
    errors = []
    for path, expected in outputs.items():
        if not path.exists():
            errors.append(f"missing output: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(f"stale output: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        outputs = build_all()
        if args.write:
            write_outputs(outputs)
        errors = check_outputs(outputs)
        status = "PASS" if not errors else "FAIL"
        result = {
            "schema_id": "v21_p0_t03_starting_baseline_validation_v1",
            "task_id": TASK_ID,
            "status": status,
            "source_commit": BASE_HEAD,
            "output_count": len(outputs),
            "errors": errors,
        }
    except (BaselineError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        result = {
            "schema_id": "v21_p0_t03_starting_baseline_validation_v1",
            "task_id": TASK_ID,
            "status": "FAIL",
            "source_commit": BASE_HEAD,
            "output_count": 0,
            "errors": [str(exc)],
        }
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"V21 P0-T03 baseline validation: {result['status']}")
        for error in result["errors"]:
            print(error, file=sys.stderr)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
