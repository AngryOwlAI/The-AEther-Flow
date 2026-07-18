#!/usr/bin/env python3
"""Materialize and validate the v20 P0-T02 backlog and dependency DAG."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v20.md"
BACKLOG = ROOT / "research_control/tasks/RT-20260718-011/artifacts/v20_recommendation_backlog.yaml"
SCHEMA = ROOT / "research_control/tasks/RT-20260718-011/artifacts/v20_recommendation_backlog_schema.md"
REPORT = ROOT / "research_control/tasks/RT-20260718-011/artifacts/v20_backlog_dependency_report.json"
ROLE_REGISTRY = ROOT / "registries/AGENT_ROLE_REGISTRY.csv"

EXPECTED_RECOMMENDATIONS = [f"V20-R{index:02d}" for index in range(1, 22)]
FINAL_COVERAGE_TASK = "P16-T03"
ROOT_TASK = "P0-T01"
TASK_HEADING = re.compile(r"^### (P\d+-T\d+):\s*(.+)$", re.MULTILINE)
PROTECTED_TERMINAL_PHASES = [
    "terminal_awaiting_human",
    "terminal_capability_blocked",
    "terminal_guard_exhausted",
    "terminal_no_progress",
    "terminal_validation_failed",
    "terminal_handoff_ambiguous",
    "terminal_handoff_timeout",
    "terminal_duplicate_detected",
    "terminal_corrupt_state",
    "terminal_failed",
    "terminal_cancelled",
]
REQUIRED_ITEM_FIELDS = {
    "plan_task_id",
    "phase_id",
    "title",
    "task_kind",
    "recommendation_ids",
    "expected_role_families",
    "depends_on",
    "conditional_task",
    "requires_human_gate",
    "state_changing_expected",
    "target_derivation_milestone",
    "milestone_burden",
    "relay_boundary",
    "source_boundaries",
    "write_boundaries",
    "required_artifacts",
    "implementation_actions",
    "validator_obligations",
    "completion_criteria",
    "completion_record_contract",
    "terminal_outcome_rules",
    "rollback_and_stop_rules",
    "human_intervention_boundary",
    "next_task_rules",
    "recommendation_coverage_role",
    "implementation_status",
    "scientific_claims_changed",
    "distance_to_gr_delta_changed",
    "physics_promotion_authorized",
    "proof_authority",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def subsection(section: str, heading: str) -> str:
    match = re.search(
        rf"^#### {re.escape(heading)}\s*$\n(.*?)(?=^#### |\Z)",
        section,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def strip_markup(text: str) -> str:
    return text.replace("`", "").strip()


def bullets(text: str) -> list[str]:
    return [strip_markup(match.group(1)) for match in re.finditer(r"^-\s+(.+)$", text, re.MULTILINE)]


def ordered_items(text: str) -> list[str]:
    return [strip_markup(match.group(1)) for match in re.finditer(r"^\d+\.\s+(.+)$", text, re.MULTILINE)]


def normalize_dependencies(values: list[Any]) -> list[str]:
    return [str(value) for value in values if value is not None and str(value).lower() != "none"]


def active_roles() -> set[str]:
    roles = set()
    with ROLE_REGISTRY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["status"] == "active":
                roles.add(f"{row['role_id']}@{row['version']}")
    return roles


def parse_plan() -> list[dict[str, Any]]:
    text = PLAN.read_text(encoding="utf-8")
    headings = list(TASK_HEADING.finditer(text))
    items: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.start():end]
        blocks = re.findall(r"```yaml\n(.*?)\n```", section, re.DOTALL)
        if len(blocks) < 3:
            raise ValueError(f"{heading.group(1)} has fewer than three YAML contracts")
        source = yaml.safe_load(blocks[0])
        launch = yaml.safe_load(blocks[1])
        completion = yaml.safe_load(blocks[2])
        task_id = source["plan_task_id"]
        if task_id != heading.group(1):
            raise ValueError(f"heading/task mismatch: {heading.group(1)} != {task_id}")

        source = dict(source)
        source["depends_on"] = normalize_dependencies(source.get("depends_on", []))
        source["milestone_burden"] = source.get(
            "milestone_burden",
            "No task-specific milestone burden is declared; preserve the named target milestone and all claim gates.",
        )
        goal_text = launch.get("goal", "")
        if not isinstance(goal_text, str) or not goal_text:
            raise ValueError(f"{task_id} has no exact relay goal text")

        preconditions = bullets(subsection(section, "Preconditions and dependency evidence"))
        stop_rules = bullets(subsection(section, "Stop, repair, rollback, and guard conditions"))
        human_terms = re.compile(r"human|external|protected|publication authority|gate chair", re.IGNORECASE)
        human_preconditions = [entry for entry in preconditions if human_terms.search(entry)]
        human_stops = [entry for entry in stop_rules if human_terms.search(entry)]

        coverage_role = "direct_implementation"
        if task_id in {"P0-T01", "P0-T02"}:
            coverage_role = "support"
        elif task_id == FINAL_COVERAGE_TASK:
            coverage_role = "final_coverage_audit"

        item = dict(source)
        item.update(
            {
                "title": heading.group(2).strip(),
                "relay_boundary": {
                    "controlling_launcher": source["controlling_launcher"],
                    "generation_worker": source["generation_worker"],
                    "research_authority_per_generation": source["research_authority_per_generation"],
                    "execution_profile": source["execution_profile"],
                    "goal_text": goal_text,
                    "goal_text_sha256": sha256_bytes(goal_text.encode("utf-8")),
                    "max_continue_passes": source["max_continue_passes"],
                    "max_elapsed_minutes": source["max_elapsed_minutes"],
                    "max_live_continuations": source["max_live_continuations"],
                    "max_outer_agentjobs_per_generation": source["max_outer_agentjobs_per_generation"],
                    "cross_task_relay_reuse": source["cross_task_relay_reuse"],
                },
                "source_boundaries": bullets(subsection(section, "Required source inspection")),
                "write_boundaries": bullets(subsection(section, "Planned write boundary")),
                "required_artifacts": bullets(subsection(section, "Required durable outputs")),
                "implementation_actions": ordered_items(subsection(section, "Implementation actions")),
                "validator_obligations": bullets(
                    subsection(section, "Required validation and canonical evidence")
                ),
                "completion_criteria": bullets(subsection(section, "Definition of done")),
                "completion_record_contract": completion,
                "terminal_outcome_rules": {
                    "success_phase": "terminal_complete",
                    "protected_or_failure_phases": PROTECTED_TERMINAL_PHASES,
                    "success_requires_all_completion_criteria": True,
                    "worker_prose_is_authority": False,
                },
                "rollback_and_stop_rules": stop_rules,
                "human_intervention_boundary": {
                    "requires_human_gate": source["requires_human_gate"],
                    "external_or_human_preconditions": human_preconditions,
                    "protected_stop_rules": human_stops,
                    "relay_may_supply_human_authority": False,
                },
                "next_task_rules": bullets(subsection(section, "Handoff rule")),
                "recommendation_coverage_role": coverage_role,
                "implementation_status": "completed" if task_id in {"P0-T01", "P0-T02"} else "pending",
                "scientific_claims_changed": False,
                "distance_to_gr_delta_changed": False,
                "physics_promotion_authorized": False,
                "proof_authority": False,
            }
        )
        items.append(item)
    return items


def topological_order(items: list[dict[str, Any]]) -> tuple[list[str], list[Any]]:
    ids = [item["plan_task_id"] for item in items]
    children: dict[str, list[str]] = defaultdict(list)
    indegree = {task_id: 0 for task_id in ids}
    errors: list[Any] = []
    for item in items:
        task_id = item["plan_task_id"]
        for dependency in item.get("depends_on", []):
            if dependency not in indegree:
                errors.append({task_id: f"dangling dependency {dependency}"})
                continue
            children[dependency].append(task_id)
            indegree[task_id] += 1
    queue = deque(task_id for task_id in ids if indegree[task_id] == 0)
    order: list[str] = []
    while queue:
        task_id = queue.popleft()
        order.append(task_id)
        for child in children[task_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(ids):
        errors.append("dependency graph contains a cycle")
    return order, errors


def reachable_from_root(items: list[dict[str, Any]]) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for item in items:
        for dependency in item.get("depends_on", []):
            children[dependency].append(item["plan_task_id"])
    reached: set[str] = set()
    queue = deque([ROOT_TASK])
    while queue:
        task_id = queue.popleft()
        if task_id in reached:
            continue
        reached.add(task_id)
        queue.extend(children[task_id])
    return reached


def coverage_matrix(items: list[dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    matrix = {
        recommendation: {"support": [], "direct_implementation": [], "final_coverage_audit": []}
        for recommendation in EXPECTED_RECOMMENDATIONS
    }
    for item in items:
        role = item["recommendation_coverage_role"]
        for recommendation in item["recommendation_ids"]:
            if recommendation in matrix:
                matrix[recommendation][role].append(item["plan_task_id"])
    return matrix


def build_backlog(items: list[dict[str, Any]]) -> dict[str, Any]:
    order, errors = topological_order(items)
    if errors:
        raise ValueError(json.dumps(errors, sort_keys=True))
    edges = [
        {"from": dependency, "to": item["plan_task_id"]}
        for item in items
        for dependency in item["depends_on"]
    ]
    return {
        "schema_id": "v20_recommendation_backlog_v1",
        "authority": "project_control",
        "status": "draft_control_backlog",
        "created_at": "2026-07-18T20:18:11Z",
        "source_plan": {
            "plan_id": "recommendations_implementation_plan_continue_task-v20",
            "plan_path": str(PLAN.relative_to(ROOT)),
            "object_id": "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V20",
            "source_hash": sha256(PLAN),
        },
        "scope": {
            "plan_task_id": "P0-T02",
            "execution_mode": "one_bounded_agentjob_per_plan_task",
            "dependency_model": "explicit_plan_dependency_dag_v1",
            "task_count": len(items),
            "phase_count": len({item["phase_id"] for item in items}),
            "max_live_continuations": 1,
            "max_outer_agentjobs_per_generation": 1,
            "cross_task_relay_reuse": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "ordinary_research_route_preserved": "EqSrc_family_closure_repair_or_stress",
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
        "terminal_outcome_vocabulary": {
            "success": "terminal_complete",
            "protected_or_failure": PROTECTED_TERMINAL_PHASES,
        },
        "recommendation_coverage_rules": {
            "expected_recommendation_ids": EXPECTED_RECOMMENDATIONS,
            "direct_implementation_role": "direct_implementation",
            "final_coverage_audit_task_id": FINAL_COVERAGE_TASK,
            "final_coverage_audit_role": "final_coverage_audit",
        },
        "recommendation_coverage_matrix": coverage_matrix(items),
        "dependency_graph": {
            "root_task_id": ROOT_TASK,
            "acyclic": True,
            "all_required_tasks_reachable": True,
            "node_count": len(items),
            "edge_count": len(edges),
            "edges": edges,
            "topological_order": order,
        },
        "items": items,
    }


def validate(backlog: dict[str, Any], plan_items: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[Any] = []
    items = backlog.get("items", [])
    ids = [item.get("plan_task_id") for item in items]
    plan_ids = [item["plan_task_id"] for item in plan_items]
    item_by_id = {item.get("plan_task_id"): item for item in items}
    plan_by_id = {item["plan_task_id"]: item for item in plan_items}
    roles = active_roles()

    duplicates = sorted(task_id for task_id, count in Counter(ids).items() if count > 1)
    if backlog.get("authority") != "project_control":
        errors.append("backlog authority must be project_control")
    if Counter(ids) != Counter(plan_ids):
        errors.append(
            {
                "task_parity": {
                    "missing": sorted(set(plan_ids) - set(ids)),
                    "extra": sorted(set(ids) - set(plan_ids)),
                    "duplicates": duplicates,
                }
            }
        )

    exact_fields = [
        "phase_id",
        "task_kind",
        "recommendation_ids",
        "expected_role_families",
        "depends_on",
        "conditional_task",
        "requires_human_gate",
        "state_changing_expected",
        "target_derivation_milestone",
        "milestone_burden",
    ]
    goal_hashes: list[str] = []
    unknown_recommendations: set[str] = set()
    for item in items:
        task_id = item.get("plan_task_id", "unknown")
        missing = sorted(REQUIRED_ITEM_FIELDS - set(item))
        if missing:
            errors.append({task_id: {"missing_fields": missing}})
        source = plan_by_id.get(task_id)
        if source:
            mismatches = [field for field in exact_fields if item.get(field) != source.get(field)]
            if mismatches:
                errors.append({task_id: {"plan_field_mismatches": mismatches}})

        relay = item.get("relay_boundary", {})
        goal_text = relay.get("goal_text", "")
        goal_hash = relay.get("goal_text_sha256", "")
        goal_hashes.append(goal_hash)
        if goal_hash != sha256_bytes(goal_text.encode("utf-8")):
            errors.append({task_id: "goal text hash mismatch"})
        if relay.get("max_continue_passes") != source.get("max_continue_passes"):
            errors.append({task_id: "pass guard differs from plan task block"})
        if relay.get("max_elapsed_minutes") != source.get("max_elapsed_minutes"):
            errors.append({task_id: "elapsed guard differs from plan task block"})
        if relay.get("max_live_continuations") != 1:
            errors.append({task_id: "max_live_continuations must equal 1"})
        if relay.get("max_outer_agentjobs_per_generation") != 1:
            errors.append({task_id: "max_outer_agentjobs_per_generation must equal 1"})
        if relay.get("cross_task_relay_reuse") is not False:
            errors.append({task_id: "cross-task relay reuse must be false"})
        if relay.get("controlling_launcher") != "continue-research-goal":
            errors.append({task_id: "unexpected controlling launcher"})
        if relay.get("generation_worker") != "continue-research-continue-goal":
            errors.append({task_id: "unexpected generation worker"})
        if relay.get("research_authority_per_generation") != "continue-research":
            errors.append({task_id: "unexpected per-generation research authority"})

        for role in item.get("expected_role_families", []):
            if role not in roles:
                errors.append({task_id: f"unregistered or inactive role {role}"})
        if not item.get("recommendation_ids"):
            errors.append({task_id: "recommendation_ids must be nonempty"})
        unknown_recommendations.update(set(item.get("recommendation_ids", [])) - set(EXPECTED_RECOMMENDATIONS))
        for field in (
            "source_boundaries",
            "write_boundaries",
            "required_artifacts",
            "implementation_actions",
            "validator_obligations",
            "completion_criteria",
            "rollback_and_stop_rules",
            "next_task_rules",
        ):
            if not item.get(field):
                errors.append({task_id: f"{field} must be nonempty"})
        human = item.get("human_intervention_boundary", {})
        if not human.get("external_or_human_preconditions"):
            errors.append({task_id: "human/external authority must be represented as a precondition"})
        if human.get("relay_may_supply_human_authority") is not False:
            errors.append({task_id: "relay must not supply human authority"})
        terminal = item.get("terminal_outcome_rules", {})
        if terminal.get("success_phase") != "terminal_complete":
            errors.append({task_id: "success phase must be terminal_complete"})
        if terminal.get("success_requires_all_completion_criteria") is not True:
            errors.append({task_id: "terminal completion must require all completion criteria"})
        if terminal.get("worker_prose_is_authority") is not False:
            errors.append({task_id: "worker prose must remain telemetry"})
        for boundary_field in (
            "scientific_claims_changed",
            "distance_to_gr_delta_changed",
            "physics_promotion_authorized",
            "proof_authority",
        ):
            if item.get(boundary_field) is not False:
                errors.append({task_id: f"{boundary_field} must be false"})

    if len(set(goal_hashes)) != len(goal_hashes):
        errors.append("each task must have one unique immutable goal boundary")
    if unknown_recommendations:
        errors.append({"unregistered_recommendation_ids": sorted(unknown_recommendations)})

    order, graph_errors = topological_order(items)
    errors.extend(graph_errors)
    reached = reachable_from_root(items)
    orphans = sorted(set(ids) - reached)
    if orphans:
        errors.append({"unreachable_required_tasks": orphans})

    matrix = coverage_matrix(items)
    for recommendation in EXPECTED_RECOMMENDATIONS:
        if not matrix[recommendation]["direct_implementation"]:
            errors.append({recommendation: "missing direct implementation-task coverage"})
        if matrix[recommendation]["final_coverage_audit"] != [FINAL_COVERAGE_TASK]:
            errors.append(
                {
                    recommendation: (
                        f"final-audit coverage must be {FINAL_COVERAGE_TASK}, got "
                        f"{matrix[recommendation]['final_coverage_audit']}"
                    )
                }
            )

    graph = backlog.get("dependency_graph", {})
    expected_edges = sum(len(item.get("depends_on", [])) for item in items)
    if graph.get("topological_order") != order:
        errors.append("stored topological order differs from computed order")
    if graph.get("node_count") != len(items) or graph.get("edge_count") != expected_edges:
        errors.append("stored dependency graph counts differ from items")

    return {
        "status": "PASS" if not errors else "FAIL",
        "gate_ids": [
            "v20_backlog_schema_parity",
            "v20_dependency_graph_integrity",
            "v20_recommendation_direct_and_final_coverage",
            "v20_relay_boundary_integrity",
            "v20_role_registry_integrity",
            "v20_human_authority_boundary",
            "v20_no_physics_authority_boundary",
        ],
        "plan_task_count": len(plan_ids),
        "backlog_item_count": len(items),
        "phase_count": len({item.get("phase_id") for item in items}),
        "dependency_edge_count": expected_edges,
        "dependencies_acyclic": not graph_errors,
        "all_required_tasks_reachable_from_p0_t01": not orphans,
        "duplicate_task_ids": duplicates,
        "unreachable_required_tasks": orphans,
        "recommendation_count": len(EXPECTED_RECOMMENDATIONS),
        "recommendation_coverage_matrix": matrix,
        "final_coverage_audit_task_id": FINAL_COVERAGE_TASK,
        "registered_role_families": sorted(
            {role for item in items for role in item.get("expected_role_families", [])}
        ),
        "unique_goal_boundary_count": len(set(goal_hashes)),
        "cross_task_relay_reuse_prohibited_for_all_tasks": all(
            item.get("relay_boundary", {}).get("cross_task_relay_reuse") is False for item in items
        ),
        "human_authority_is_precondition_only": all(
            item.get("human_intervention_boundary", {}).get("relay_may_supply_human_authority") is False
            and bool(item.get("human_intervention_boundary", {}).get("external_or_human_preconditions"))
            for item in items
        ),
        "next_route_after_p0_t02": item_by_id.get("P0-T02", {}).get("next_task_rules", []),
        "source_hashes": {
            "plan": sha256(PLAN),
            "backlog": sha256(BACKLOG),
            "schema": sha256(SCHEMA),
        },
        "no_physics_authority_boundary": {
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "ordinary_research_route_preserved": "EqSrc_family_closure_repair_or_stress",
        },
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="materialize the deterministic backlog")
    parser.add_argument("--json", action="store_true", help="retained for command-contract clarity")
    args = parser.parse_args()

    plan_items = parse_plan()
    if args.write:
        BACKLOG.write_text(
            yaml.safe_dump(build_backlog(plan_items), sort_keys=False, width=120, allow_unicode=True),
            encoding="utf-8",
        )
    if not BACKLOG.exists():
        raise SystemExit(f"missing backlog: {BACKLOG}")
    backlog = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    report = validate(backlog, plan_items)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
