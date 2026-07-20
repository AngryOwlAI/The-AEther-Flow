#!/usr/bin/env python3
"""Build and validate the v21 P0-T05 independent prelaunch audit artifacts.

The checks in this file are control-contract checks.  They make the audit
reproducible, but their PASS result is not scientific evidence, proof
authority, or permission to cross a protected gate.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent

PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
BACKLOG = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
GOAL_SCHEMA = ROOT / ".codex/skills/continue-research-goal/references/goal-file-schema.md"
MANIFEST = ROOT / "research_control/tasks/RT-20260720-007/artifacts/v21_relay_launch_manifest.md"
SCOPE = ROOT / "research_control/tasks/RT-20260720-007/artifacts/v21_scope_contract_candidate.json"
COMPLETION_CONTRACT = ROOT / "research_control/tasks/RT-20260720-007/artifacts/v21_completion_contract.md"
CHECKLIST = ROOT / "research_control/tasks/RT-20260720-007/artifacts/v21_prelaunch_checklist.md"
LAUNCH_RECEIPT = ROOT / "research_control/tasks/RT-20260720-007/artifacts/v21_launch_manifest_receipt.json"
P0_T04_COMPLETION = ROOT / "research_control/tasks/RT-20260720-007/jobs/completions/AJC-AJ-RT-20260720-007-001.yaml"
SOURCE_HASH_MANIFEST = ROOT / "research_control/tasks/RT-20260720-006/artifacts/v21_source_hash_manifest.json"

REPORT = ARTIFACT_DIR / "v21_prelaunch_red_team_report.yaml"
COVERAGE = ARTIFACT_DIR / "v21_recommendation_coverage_audit.csv"
VERDICT = ARTIFACT_DIR / "v21_relay_readiness_verdict.yaml"
RECEIPT = ARTIFACT_DIR / "v21_prelaunch_audit_receipt.json"

EXPECTED_RECOMMENDATIONS = [f"V21-R{number:02d}" for number in range(1, 73)]
EXPECTED_HUMAN_GATES = {
    "P4-T05",
    "P7-T08",
    "P8-T07",
    "P9-T09",
    "P14-T04",
    "P15-T05",
    "P15-T07",
}
EXPECTED_FIXED_GUARDS = {
    "allow_scope_expansion": "false",
    "max_repeated_state_fingerprints": "1",
    "stop_on_human_gate": "true",
    "stop_on_no_progress": "true",
    "stop_on_repeated_state": "true",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class IndentDumper(yaml.SafeDumper):
    """Emit block sequences indented beneath their mapping keys."""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> Any:
        return super().increase_indent(flow, False)


def yaml_text(value: Any) -> str:
    return yaml.dump(
        value,
        Dumper=IndentDumper,
        sort_keys=False,
        allow_unicode=True,
        width=110,
        default_flow_style=False,
    )


def strict_yaml_text(data: dict[str, Any]) -> str:
    """Render the repository strict-YAML subset with quoted string scalars."""

    lines: list[str] = []

    def scalar(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        return json.dumps(str(value), ensure_ascii=False)

    def emit_map(mapping: dict[str, Any], indent: int) -> None:
        prefix = " " * indent
        for key, value in mapping.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                emit_map(value, indent + 2)
            elif isinstance(value, list):
                if not value:
                    lines.append(f"{prefix}{key}: []")
                    continue
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        first_key, first_value = next(iter(item.items()))
                        if isinstance(first_value, (dict, list)):
                            raise TypeError("strict YAML list maps require a scalar first field")
                        lines.append(f"{prefix}  - {first_key}: {scalar(first_value)}")
                        emit_map(dict(list(item.items())[1:]), indent + 4)
                    else:
                        lines.append(f"{prefix}  - {scalar(item)}")
            else:
                lines.append(f"{prefix}{key}: {scalar(value)}")

    emit_map(data, 0)
    return "\n".join(lines) + "\n"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def graph_audit(items: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    ids = [item["plan_task_id"] for item in items]
    id_set = set(ids)
    require(len(ids) == len(id_set), "work-item IDs are not unique", failures)

    edges = [(dependency, item["plan_task_id"]) for item in items for dependency in item["depends_on"]]
    require(all(source in id_set for source, _ in edges), "dependency references an unknown work item", failures)
    require(all(source != target for source, target in edges), "dependency graph contains a self-loop", failures)

    outgoing: dict[str, list[str]] = {item_id: [] for item_id in ids}
    indegree = {item_id: 0 for item_id in ids}
    for source, target in edges:
        outgoing[source].append(target)
        indegree[target] += 1
    queue = deque(sorted(item_id for item_id, count in indegree.items() if count == 0))
    topological_order: list[str] = []
    while queue:
        current = queue.popleft()
        topological_order.append(current)
        for target in sorted(outgoing[current]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    require(len(topological_order) == len(ids), "dependency graph contains a cycle", failures)

    reachable = {"P0-T01"}
    frontier = ["P0-T01"]
    while frontier:
        current = frontier.pop()
        for target in outgoing[current]:
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)
    require(reachable == id_set, "not every work item is reachable from P0-T01", failures)
    return {
        "node_count": len(ids),
        "edge_count": len(edges),
        "acyclic": len(topological_order) == len(ids),
        "all_nodes_reachable": reachable == id_set,
        "topological_order_count": len(topological_order),
    }


def build() -> tuple[dict[Path, str], dict[str, Any]]:
    failures: list[str] = []
    backlog = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    scope = json.loads(SCOPE.read_text(encoding="utf-8"))
    launch_receipt = json.loads(LAUNCH_RECEIPT.read_text(encoding="utf-8"))
    source_hash_manifest = json.loads(SOURCE_HASH_MANIFEST.read_text(encoding="utf-8"))
    items = backlog["items"]
    item_by_id = {item["plan_task_id"]: item for item in items}
    coverage_matrix = backlog["recommendation_coverage_matrix"]

    require(len(items) == 122, "expected 122 work items", failures)
    require(backlog["scope"]["task_count"] == 122, "backlog scope task count is not 122", failures)
    require(backlog["scope"]["allow_scope_expansion"] is False, "backlog permits scope expansion", failures)
    require(backlog["scope"]["max_worker_invocations_per_generation"] == 1, "backlog permits multiple worker invocations", failures)
    require(backlog["scope"]["max_outer_agentjobs_per_generation"] == 1, "backlog permits multiple outer AgentJobs", failures)

    graph = graph_audit(items, failures)
    require(graph["edge_count"] == 183, "expected 183 dependency edges", failures)
    recorded_edges = {(edge["from"], edge["to"]) for edge in backlog["dependency_graph"]["edges"]}
    derived_edges = {(dependency, item["plan_task_id"]) for item in items for dependency in item["depends_on"]}
    require(recorded_edges == derived_edges, "recorded dependency edges differ from work-item dependencies", failures)

    expected_recommendations = backlog["recommendation_coverage_rules"]["expected_recommendation_ids"]
    require(expected_recommendations == EXPECTED_RECOMMENDATIONS, "recommendation ID set is incomplete or reordered", failures)
    require(set(coverage_matrix) == set(EXPECTED_RECOMMENDATIONS), "coverage matrix does not contain exactly 72 recommendations", failures)

    coverage_rows: list[dict[str, str]] = []
    for recommendation_id in EXPECTED_RECOMMENDATIONS:
        row = coverage_matrix[recommendation_id]
        direct = row.get("direct_implementation", [])
        final_audit = row.get("final_coverage_audit", [])
        final_disposition = row.get("final_goal_disposition", [])
        unknown = set(direct + final_audit + final_disposition) - set(item_by_id)
        validated_direct = [
            task_id
            for task_id in direct
            if task_id in item_by_id and item_by_id[task_id].get("validator_obligations")
        ]
        require(bool(direct), f"{recommendation_id} has no direct implementation task", failures)
        require(not unknown, f"{recommendation_id} references unknown tasks: {sorted(unknown)}", failures)
        require(bool(validated_direct), f"{recommendation_id} has no direct task with a validation path", failures)
        require(final_audit == ["P16-T01"], f"{recommendation_id} lacks exact P16-T01 final audit", failures)
        require(final_disposition == ["P16-T06"], f"{recommendation_id} lacks exact P16-T06 disposition", failures)
        coverage_rows.append(
            {
                "recommendation_id": recommendation_id,
                "direct_task_count": str(len(direct)),
                "direct_tasks": ";".join(direct),
                "direct_tasks_with_validation": ";".join(validated_direct),
                "final_coverage_audit": ";".join(final_audit),
                "final_goal_disposition": ";".join(final_disposition),
                "audit_status": "PASS",
            }
        )

    worker_counts = Counter(item["worker_skill"] for item in items)
    require(worker_counts == Counter({"continue-research": 83, "improve-project-system": 33, "none_until_human_authorization": 6}), "worker-skill counts changed", failures)
    for item in items:
        task_id = item["plan_task_id"]
        worker = item["worker_skill"]
        task_class = item["task_class"]
        require(item["controlling_launcher"] == "continue-research-goal@v4", f"{task_id} has an ambiguous launcher", failures)
        require(item["max_worker_invocations_per_generation"] == 1, f"{task_id} permits multiple worker invocations", failures)
        require(item["max_outer_agentjobs_per_generation"] == 1, f"{task_id} permits multiple AgentJobs", failures)
        require(item["allow_scope_expansion"] is False, f"{task_id} permits scope expansion", failures)
        require(item["proof_authority_created_by_plan"] is False, f"{task_id} creates proof authority", failures)
        require(item["physics_promotion_authorized_by_plan"] is False, f"{task_id} authorizes physics promotion", failures)
        if task_class == "project_system":
            require(worker == "improve-project-system", f"{task_id} project-system work has the wrong worker", failures)
        else:
            require(worker != "improve-project-system", f"{task_id} science/control work is routed through project-system validation", failures)
        if worker == "none_until_human_authorization":
            require(item["requires_human_gate"] is True, f"{task_id} suppresses a worker without a human gate", failures)
            require(item["role_family"] == "gate-chair", f"{task_id} suppressed worker is not a Gate Chair task", failures)

    gate_ids = {item["plan_task_id"] for item in items if item["requires_human_gate"]}
    require(gate_ids == EXPECTED_HUMAN_GATES, "human-gate set changed", failures)
    require(set(backlog["human_gate_summary"]["human_gated_work_item_ids"]) == EXPECTED_HUMAN_GATES, "human-gate summary differs from items", failures)
    require(backlog["human_gate_summary"]["relay_may_supply_human_authority"] is False, "relay may supply human authority", failures)
    for task_id in sorted(gate_ids):
        boundary = item_by_id[task_id]["human_intervention_boundary"]
        conditions = " ".join(boundary["protected_or_external_conditions"])
        require(boundary["relay_may_supply_human_authority"] is False, f"{task_id} permits relay-supplied authority", failures)
        require("exact human authorization" in conditions, f"{task_id} lacks an exact human-authorization condition", failures)
        require("do not create a worker invocation" in conditions.lower(), f"{task_id} does not block preauthorization invocation", failures)

    scope_projection = [
        {"work_item_id": item["work_item_id"], "objective": item["objective"], "depends_on": item["depends_on"]}
        for item in scope["included_work_items"]
    ]
    backlog_projection = [
        {"work_item_id": item["plan_task_id"], "objective": item["exact_objective"], "depends_on": item["depends_on"]}
        for item in items
    ]
    require(scope_projection == backlog_projection, "relay scope work items differ from the materialized backlog", failures)
    require(scope["allow_scope_expansion"] is False, "relay scope permits expansion", failures)
    require(scope["dependency_source"]["sha256"] == sha256(PLAN), "relay dependency-source hash differs from the plan", failures)

    baseline_rows = {row["path"]: row["sha256"] for row in source_hash_manifest["records"]}
    require(baseline_rows.get("research_control/design/v21_recommendation_backlog.yaml") == sha256(BACKLOG), "backlog hash differs from the frozen P0-T03 source manifest", failures)
    require(launch_receipt["work_item_count"] == 122 and launch_receipt["dependency_edge_count"] == 183, "P0-T04 launch receipt has wrong scope counts", failures)
    require(all(result["status"] == "PASS" for result in launch_receipt["validator_results"]), "P0-T04 receipt contains a failed contract check", failures)
    for path_text, expected_hash in launch_receipt["artifact_sha256"].items():
        require(sha256(ROOT / path_text) == expected_hash, f"P0-T04 artifact hash changed: {path_text}", failures)

    goal_schema_text = GOAL_SCHEMA.read_text(encoding="utf-8")
    completion_contract_text = COMPLETION_CONTRACT.read_text(encoding="utf-8")
    checklist_text = CHECKLIST.read_text(encoding="utf-8")
    for guard, expected_value in EXPECTED_FIXED_GUARDS.items():
        require(f"{guard}: {expected_value}" in goal_schema_text, f"goal schema lacks fixed guard {guard}", failures)
    require("max_continue_passes` and `deadline_at` are JSON `null`" in checklist_text, "checklist does not preserve null scheduling horizons", failures)
    require("unresolved protected human gate" in completion_contract_text, "completion contract lacks human-gate terminal handling", failures)

    completed_p0 = {"P0-T01", "P0-T02", "P0-T03", "P0-T04", "P0-T05"}
    immediately_eligible = sorted(
        item["plan_task_id"]
        for item in items
        if item["plan_task_id"] not in completed_p0 and set(item["depends_on"]).issubset(completed_p0)
    )
    require(immediately_eligible == ["P1-T01", "P10-T01", "P13-T01", "P13-T03"], "post-P0-T05 eligibility set changed", failures)
    require(item_by_id["P1-T01"]["task_class"] == "science", "P1-T01 is no longer the first scientific task", failures)

    checks = {
        "recommendation_coverage": {
            "status": "PASS",
            "recommendation_count": len(EXPECTED_RECOMMENDATIONS),
            "missing_direct_task_count": 0,
            "missing_validation_path_count": 0,
            "missing_final_audit_count": 0,
            "missing_final_disposition_count": 0,
        },
        "dependency_graph": {"status": "PASS", **graph},
        "worker_skill_boundaries": {
            "status": "PASS",
            "route_counts": [f"{name}={count}" for name, count in sorted(worker_counts.items())],
        },
        "human_gates": {
            "status": "PASS",
            "gate_count": len(gate_ids),
            "gate_ids": sorted(gate_ids),
            "relay_may_supply_human_authority": False,
        },
        "relay_manifest_parity": {
            "status": "PASS",
            "scope_projection_sha256": canonical_sha256(scope_projection),
            "backlog_projection_sha256": canonical_sha256(backlog_projection),
            "frozen_backlog_sha256": sha256(BACKLOG),
            "manifest_sha256": sha256(MANIFEST),
            "scope_contract_sha256": sha256(SCOPE),
            "completion_contract_sha256": sha256(COMPLETION_CONTRACT),
        },
        "stop_guards": {
            "status": "PASS",
            "scheduling_horizon": "unlimited_by_null_only",
            "fixed_guards": EXPECTED_FIXED_GUARDS,
        },
        "authority_separation": {
            "status": "PASS",
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "validator_pass_is_scientific_evidence": False,
        },
    }

    findings = [
        {
            "finding_id": "P0-T05-OBS-001",
            "severity": "advisory",
            "status": "nonblocking",
            "finding": "The registered role name external-red-team-reviewer does not establish epistemic independence for this same-context review.",
            "exact_repair_route": "P11-T02 defines normalized reviewer-independence and model-diversity classifications; do not relabel this packet as independent replication.",
        },
        {
            "finding_id": "P0-T05-OBS-002",
            "severity": "advisory",
            "status": "nonblocking",
            "finding": "P0 recommendation coverage is traceability and prelaunch pressure, not evidence that downstream recommendation implementations are complete.",
            "exact_repair_route": "Preserve every downstream task disposition and require P16-T01 final coverage evidence before any all-recommendations-complete statement.",
        },
        {
            "finding_id": "P0-T05-OBS-003",
            "severity": "informational",
            "status": "nonblocking",
            "finding": "P0-T05 makes four tasks immediately dependency-ready; the existing scientific handoff selects P1-T01 while P10-T01, P13-T01, and P13-T03 remain eligible but unselected.",
            "exact_repair_route": "Dispatch only one immutable included work item per generation and preserve the other eligible tasks as pending.",
        },
        {
            "finding_id": "P0-T05-OBS-004",
            "severity": "informational",
            "status": "nonblocking",
            "finding": "The launch packet intentionally retains one explained historical program-state hash mismatch because tracked state evolved before the frozen baseline.",
            "exact_repair_route": "Recompute every mutable live source hash before any future launch; never edit an active scope contract to conceal drift.",
        },
    ]

    report = {
        "schema_id": "external_red_team_review_artifact_schema_v1",
        "schema_path": ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md",
        "review_id": "ERT-REVIEW-V21-P0-T05-001",
        "task_id": "RT-20260720-008",
        "agent_job_id": "AJ-RT-20260720-008-001",
        "role_execution_ref": "external-red-team-reviewer@0.1.0--RT-20260720-008",
        "reviewed_object_id": "v21-P0-T05-prelaunch-contract-set",
        "reviewed_source_paths": [
            "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
            "research_control/design/v21_recommendation_backlog.yaml",
            "research_control/tasks/RT-20260720-006/artifacts/v21_source_hash_manifest.json",
            "research_control/tasks/RT-20260720-007/artifacts/v21_relay_launch_manifest.md",
            "research_control/tasks/RT-20260720-007/artifacts/v21_scope_contract_candidate.json",
            "research_control/tasks/RT-20260720-007/artifacts/v21_completion_contract.md",
            "research_control/tasks/RT-20260720-007/artifacts/v21_prelaunch_checklist.md",
            "research_control/tasks/RT-20260720-007/artifacts/v21_launch_manifest_receipt.json",
            "research_control/tasks/RT-20260720-007/jobs/completions/AJC-AJ-RT-20260720-007-001.yaml",
            ".codex/skills/continue-research-goal/references/goal-file-schema.md",
            "research_control/handoffs/handoff-0777.yaml",
            "registries/DISTANCE_TO_GR_LEDGER.csv",
            "research_control/design/gr_derivation_burden_map.md",
            "research_control/design/frontier_theorem_inventory.md",
        ],
        "claim_under_review": "The tracked v21 scope is complete and authority-bounded enough for the existing active relay to advance after P0-T05, with P1-T01 remaining the first scientific task.",
        "workflow_success_disregarded_as_evidence": True,
        "validator_success_disregarded_as_evidence": True,
        "assumptions_read": [
            "P0-T04 has qualifying finalized canonical completion evidence and handoff-0777 selects exactly P0-T05.",
            "The active relay scope is immutable, allows no expansion, and permits one worker invocation plus at most one outer AgentJob per generation.",
            "Project-system validation cannot prove a science claim and science roles cannot silently execute project-system changes.",
            "A protected work item receives no worker invocation until its exact human authorization exists.",
        ],
        "definitions_read": [
            "v21 recommendation coverage roles",
            "explicit dependency DAG",
            "worker_skill and role_family route fields",
            "human_intervention_boundary",
            "continue-research-goal v4 fixed guards",
            "v21 completion contract",
        ],
        "proof_steps_checked": [
            "Each V21-R01 through V21-R72 row has a direct task, a direct-task validation path, P16-T01 final coverage audit, and P16-T06 final disposition.",
            "All 122 unique work items and 183 derived edges form an acyclic graph reachable from P0-T01.",
            "Every project-system task routes only through improve-project-system and no science/control task does so.",
            "All seven human gates deny relay-supplied authority and block invocation before exact human authorization.",
            "The scope candidate exactly matches the backlog work-item IDs, objectives, dependencies, and registered plan hash.",
            "Null scheduling horizons leave all fixed v4 human-gate, no-progress, repeated-state, validation, capability, and repository stops intact.",
        ],
        "circularity_findings": [
            "No blocking circular completion criterion was found: P0-T05 establishes prelaunch readiness only, while P16-T01 and P16-T06 remain separate final-evidence tasks.",
        ],
        "hidden_import_findings": [
            "No blocking target import was found in the control contract; all work-item promotion and proof-authority flags remain false.",
            "Workflow status, registry status, validator PASS, and relay continuation remain explicitly blocked as scientific evidence.",
        ],
        "notation_overload_findings": [
            "The word external in the role name must not be read as epistemic independence; P11-T02 owns that classification.",
        ],
        "unproven_equivalence_findings": [
            "Complete recommendation traceability is not equivalent to completed recommendation implementation.",
            "Manifest/backlog parity is not equivalent to scientific correctness, source-law adoption, EqSrc discharge, benchmark recovery, or completed GR derivation.",
        ],
        "minimal_countermodel_attempt": {
            "attempted": True,
            "result": "no_countermodel_found_under_scope",
            "summary": "Attempted failure paths for missing coverage, dependency cycle, cross-worker authority laundering, preauthorization human-gate invocation, scope expansion, and process-as-proof. The explicit contract blocks each tested path; four nonblocking observations remain.",
            "artifact_path": "research_control/tasks/RT-20260720-008/artifacts/v21_relay_readiness_verdict.yaml",
        },
        "external_mathematical_pressure_points": [
            "Treat this as a same-context skeptical control review, not independent replication.",
            "Keep P1-T01 as the selected first scientific packet while preserving other dependency-ready tasks as pending.",
            "Recompute mutable hashes before any future launch and stop on unexplained drift.",
            "Require P16-T01 and P16-T06 before claiming full recommendation completion.",
        ],
        "verdict": "no_blocking_defect_found_as_written",
        "recommended_next_route": "Run exactly one bounded P1-T01 fresh Smuggling Auditor ontology-law-research-packet against the unchanged graded-orbit root candidate.",
        "physics_promotion_authorized": False,
        "audit_checks": checks,
        "findings": findings,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "proof_authority": False,
    }

    verdict = {
        "schema_id": "v21_p0_t05_relay_readiness_verdict_v1",
        "task_id": "RT-20260720-008",
        "plan_task_id": "P0-T05",
        "verdict": "PASS",
        "relay_readiness": "ready_for_existing_active_relay_continuation",
        "blocking_finding_count": 0,
        "nonblocking_finding_count": len(findings),
        "checks": checks,
        "findings": findings,
        "immediately_eligible_after_p0_t05": immediately_eligible,
        "selected_next_work_item": "P1-T01",
        "selection_basis": "handoff-0777 preserves handoff-0772 as the first required scientific route; only one included work item may be dispatched per generation.",
        "unselected_eligible_work_items": ["P10-T01", "P13-T01", "P13-T03"],
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "forbidden_conclusions": [
            "recommendation traceability as completed implementation",
            "validator PASS or checkpoint as scientific proof",
            "manifest parity as source-law or ontology adoption",
            "P0-T05 as P1-T01 execution",
            "general EqSrc discharge or Distance-to-GR progress",
            "benchmark promotion, Gate Chair verdict, publication, or completed derivation",
        ],
    }

    coverage_buffer = io.StringIO(newline="")
    writer = csv.DictWriter(coverage_buffer, fieldnames=list(coverage_rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(coverage_rows)

    generated_without_receipt = {
        REPORT: strict_yaml_text(report),
        COVERAGE: coverage_buffer.getvalue(),
        VERDICT: yaml_text(verdict),
    }
    receipt = {
        "schema_id": "v21_p0_t05_prelaunch_audit_receipt_v1",
        "task_id": "RT-20260720-008",
        "plan_task_id": "P0-T05",
        "result_status": "PASS",
        "verdict": "no_blocking_defect_found_as_written",
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [
                PLAN,
                BACKLOG,
                GOAL_SCHEMA,
                MANIFEST,
                SCOPE,
                COMPLETION_CONTRACT,
                CHECKLIST,
                LAUNCH_RECEIPT,
                P0_T04_COMPLETION,
                SOURCE_HASH_MANIFEST,
            ]
        },
        "artifact_sha256": {
            str(path.relative_to(ROOT)): hashlib.sha256(text.encode("utf-8")).hexdigest()
            for path, text in generated_without_receipt.items()
        },
        "finding_counts": {"blocking": 0, "advisory": 2, "informational": 2},
        "recommendation_count": 72,
        "work_item_count": 122,
        "dependency_edge_count": 183,
        "human_gate_count": 7,
        "worker_skill_counts": dict(sorted(worker_counts.items())),
        "immediately_eligible_after_p0_t05": immediately_eligible,
        "selected_next_work_item": "P1-T01",
        "validator_results": [
            {"validator_id": name, "status": check["status"]}
            for name, check in checks.items()
        ],
        "claim_boundary_summary": "Control-only same-context skeptical review; no science source edit, promotion, proof authority, protected authority, publication, or P1-T01 execution.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    generated = {**generated_without_receipt, RECEIPT: json.dumps(receipt, indent=2, sort_keys=True) + "\n"}
    result = {
        "schema_id": "v21_p0_t05_prelaunch_audit_builder_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "artifact_count": len(generated),
        "recommendation_count": 72,
        "work_item_count": graph["node_count"],
        "dependency_edge_count": graph["edge_count"],
        "blocking_finding_count": 0,
        "nonblocking_finding_count": len(findings),
        "physics_promotion_authorized": False,
    }
    return generated, result


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    generated, result = build()
    if result["failures"]:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1
    if args.write:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        for path, text in generated.items():
            path.write_text(text, encoding="utf-8")
    else:
        stale = [str(path.relative_to(ROOT)) for path, text in generated.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
        if stale:
            result["status"] = "FAIL"
            result["failures"] = [f"stale generated artifact: {path}" for path in stale]
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
