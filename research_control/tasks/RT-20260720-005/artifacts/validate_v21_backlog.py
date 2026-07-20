#!/usr/bin/env python3
"""Materialize and validate the v21 P0-T02 backlog and dependency DAG."""
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
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
BACKLOG = ROOT / "research_control/design/v21_recommendation_backlog.yaml"
SCHEMA = ROOT / "research_control/design/v21_recommendation_backlog_schema.md"
REPORT = ROOT / "research_control/tasks/RT-20260720-005/artifacts/v21_backlog_dependency_report.json"
ROLE_REGISTRY = ROOT / "registries/AGENT_ROLE_REGISTRY.csv"

CREATED_AT = "2026-07-20T18:41:34Z"
EXPECTED_RECOMMENDATIONS = [f"V21-R{index:02d}" for index in range(1, 73)]
FINAL_COVERAGE_TASK = "P16-T01"
FINAL_GOAL_TASK = "P16-T06"
ROOT_TASK = "P0-T01"
TASK_HEADING = re.compile(r"^### (P\d+-T\d+):\s*(.+)$", re.MULTILINE)
ALLOWED_WORKER_SKILLS = {
    "continue-research",
    "improve-project-system",
    "none_until_human_authorization",
}
PLAN_EXACT_FIELDS = {
    "plan_task_id",
    "phase_id",
    "work_kind",
    "task_class",
    "title",
    "recommendation_ids",
    "role_family",
    "controlling_launcher",
    "worker_skill",
    "route_label",
    "target_derivation_milestone",
    "milestone_burden",
    "expected_result_kind",
    "depends_on",
    "max_worker_invocations_per_generation",
    "max_outer_agentjobs_per_generation",
    "requires_human_gate",
    "dependency_independent_after_other_human_gates",
    "allow_scope_expansion",
    "physics_promotion_authorized_by_plan",
    "proof_authority_created_by_plan",
}
DERIVED_ITEM_FIELDS = {
    "exact_objective",
    "source_boundaries",
    "write_boundaries",
    "implementation_actions",
    "required_artifacts",
    "validator_obligations",
    "completion_criteria",
    "rollback_and_stop_rules",
    "next_task_rules",
    "human_intervention_boundary",
    "recommendation_coverage_role",
    "implementation_status",
    "scientific_claims_changed",
    "distance_to_gr_delta_changed",
    "physics_promotion_authorized",
    "proof_authority",
}
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def subsection(section: str, heading: str) -> str:
    match = re.search(
        rf"^#### {re.escape(heading)}\s*$\n(.*?)(?=^#{{1,4}} |\Z)",
        section,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def strip_markup(text: str) -> str:
    return text.replace("`", "").strip()


def normalized_prose(text: str) -> str:
    return re.sub(r"\s+", " ", strip_markup(text))


def bullets(text: str) -> list[str]:
    return [
        strip_markup(match.group(1))
        for match in re.finditer(r"^-\s+(.+)$", text, re.MULTILINE)
    ]


def ordered_items(text: str) -> list[str]:
    return [
        strip_markup(match.group(1))
        for match in re.finditer(r"^\d+\.\s+(.+)$", text, re.MULTILINE)
    ]


def role_registry_state() -> tuple[set[str], set[str]]:
    active_refs: set[str] = set()
    permitted_bare_ids: set[str] = set()
    with ROLE_REGISTRY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            status = row["status"]
            if status == "active":
                active_refs.add(f"{row['role_id']}@{row['version']}")
                permitted_bare_ids.add(row["role_id"])
            elif status == "status_defined":
                permitted_bare_ids.add(row["role_id"])
    return active_refs, permitted_bare_ids


def coverage_role(task_id: str) -> str:
    if task_id in {"P0-T01", "P0-T02"}:
        return "support"
    if task_id == FINAL_COVERAGE_TASK:
        return "final_coverage_audit"
    if task_id == FINAL_GOAL_TASK:
        return "final_goal_disposition"
    return "direct_implementation"


def parse_plan() -> list[dict[str, Any]]:
    text = PLAN.read_text(encoding="utf-8")
    headings = list(TASK_HEADING.finditer(text))
    items: list[dict[str, Any]] = []
    human_terms = re.compile(
        r"human|external|protected|publication authority|gate chair",
        re.IGNORECASE,
    )
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.start():end]
        blocks = re.findall(r"```yaml\n(.*?)\n```", section, re.DOTALL)
        if len(blocks) != 1:
            raise ValueError(f"{heading.group(1)} must have exactly one YAML task contract")
        source = yaml.safe_load(blocks[0])
        if set(source) != PLAN_EXACT_FIELDS:
            raise ValueError(
                f"{heading.group(1)} task contract fields differ: "
                f"missing={sorted(PLAN_EXACT_FIELDS - set(source))} "
                f"extra={sorted(set(source) - PLAN_EXACT_FIELDS)}"
            )
        task_id = source["plan_task_id"]
        if task_id != heading.group(1):
            raise ValueError(f"heading/task mismatch: {heading.group(1)} != {task_id}")
        if source["title"] != heading.group(2).strip():
            raise ValueError(f"{task_id} heading/title mismatch")

        source_sections = {
            "objective": subsection(section, "Objective"),
            "preconditions": subsection(section, "Preconditions and dependency evidence"),
            "sources": subsection(section, "Required source inspection"),
            "writes": subsection(section, "Planned write scope"),
            "actions": subsection(section, "Implementation actions"),
            "artifacts": subsection(section, "Required durable outputs"),
            "validators": subsection(section, "Required validation and evidence"),
            "done": subsection(section, "Definition of done"),
            "stops": subsection(section, "Stop, repair, and rollback conditions"),
            "handoff": subsection(section, "Handoff rule"),
        }
        if any(not value for value in source_sections.values()):
            missing = sorted(key for key, value in source_sections.items() if not value)
            raise ValueError(f"{task_id} missing authored subsections: {missing}")

        protected_conditions = [
            entry
            for entry in (
                bullets(source_sections["preconditions"])
                + bullets(source_sections["stops"])
                + bullets(source_sections["handoff"])
            )
            if human_terms.search(entry)
        ]
        item = dict(source)
        item.update(
            {
                "exact_objective": normalized_prose(source_sections["objective"]),
                "source_boundaries": bullets(source_sections["sources"]),
                "write_boundaries": bullets(source_sections["writes"]),
                "implementation_actions": ordered_items(source_sections["actions"]),
                "required_artifacts": bullets(source_sections["artifacts"]),
                "validator_obligations": bullets(source_sections["validators"]),
                "completion_criteria": bullets(source_sections["done"]),
                "rollback_and_stop_rules": bullets(source_sections["stops"]),
                "next_task_rules": bullets(source_sections["handoff"]),
                "human_intervention_boundary": {
                    "requires_human_gate": source["requires_human_gate"],
                    "protected_or_external_conditions": protected_conditions,
                    "relay_may_supply_human_authority": False,
                },
                "recommendation_coverage_role": coverage_role(task_id),
                "implementation_status": (
                    "completed" if task_id in {"P0-T01", "P0-T02"} else "pending"
                ),
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
        for dependency in item["depends_on"]:
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
        for dependency in item["depends_on"]:
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
    roles = (
        "support",
        "direct_implementation",
        "final_coverage_audit",
        "final_goal_disposition",
    )
    matrix = {
        recommendation: {role: [] for role in roles}
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
    human_gate_ids = [
        item["plan_task_id"] for item in items if item["requires_human_gate"]
    ]
    independent_ids = [
        item["plan_task_id"]
        for item in items
        if item["dependency_independent_after_other_human_gates"]
    ]
    return {
        "schema_id": "v21_recommendation_backlog_v1",
        "authority": "project_control",
        "status": "draft_control_backlog",
        "created_at": CREATED_AT,
        "source_plan": {
            "plan_id": "recommendations_implementation_plan_continue_task-v21",
            "plan_path": str(PLAN.relative_to(ROOT)),
            "object_id": "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21",
            "source_hash": sha256(PLAN),
        },
        "source_evidence": {
            "p0_t01_completion_path": (
                "research_control/tasks/RT-20260720-003/jobs/completions/"
                "AJC-AJ-RT-20260720-003-001.yaml"
            ),
            "p0_t01_completion_sha256": (
                "55683b6f6f13408f2200b765f2c9e193fb7cfce0ac6e5131fc6c6de44cdb674d"
            ),
            "plan_registration_report_path": (
                "research_control/tasks/RT-20260720-003/artifacts/"
                "v21_plan_registration_report.json"
            ),
            "plan_registration_report_sha256": (
                "eed1d2c0eea893f623d3dbee89071f10041ba1fc60b629f50a2f16132ea1abf0"
            ),
            "current_control_handoff": "handoff-0774",
            "preserved_scientific_handoff": "handoff-0772",
            "preserved_scientific_handoff_sha256": (
                "31374c85ee49e457a8b25eaf6d729a0d0e286f1dd53eac184a502044fdd8de0a"
            ),
        },
        "scope": {
            "mode": "multi_step",
            "plan_task_id": "P0-T02",
            "execution_mode": "one_bounded_worker_and_agentjob_per_generation",
            "dependency_model": "explicit_plan_dependency_dag_v1",
            "task_count": len(items),
            "phase_count": len({item["phase_id"] for item in items}),
            "max_live_continuations": 1,
            "max_worker_invocations_per_generation": 1,
            "max_outer_agentjobs_per_generation": 1,
            "allow_scope_expansion": False,
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "control_handoff_supersedes_scientific_handoff": False,
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
            "final_goal_disposition_task_id": FINAL_GOAL_TASK,
            "final_goal_disposition_role": "final_goal_disposition",
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
        "human_gate_summary": {
            "human_gated_work_item_ids": human_gate_ids,
            "dependency_independent_work_item_ids": independent_ids,
            "relay_may_supply_human_authority": False,
        },
        "items": items,
    }


def validate(backlog: dict[str, Any], plan_items: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[Any] = []
    items = backlog.get("items", [])
    ids = [item.get("plan_task_id") for item in items]
    plan_ids = [item["plan_task_id"] for item in plan_items]
    plan_by_id = {item["plan_task_id"]: item for item in plan_items}
    active_role_refs, permitted_bare_role_ids = role_registry_state()
    duplicates = sorted(task_id for task_id, count in Counter(ids).items() if count > 1)

    if backlog.get("schema_id") != "v21_recommendation_backlog_v1":
        errors.append("unexpected backlog schema_id")
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

    unknown_recommendations: set[str] = set()
    for item in items:
        task_id = item.get("plan_task_id", "unknown")
        missing = sorted((PLAN_EXACT_FIELDS | DERIVED_ITEM_FIELDS) - set(item))
        if missing:
            errors.append({task_id: {"missing_fields": missing}})
        source = plan_by_id.get(task_id)
        if source:
            mismatches = [
                field for field in PLAN_EXACT_FIELDS if item.get(field) != source.get(field)
            ]
            if mismatches:
                errors.append({task_id: {"plan_field_mismatches": mismatches}})

        if item.get("worker_skill") not in ALLOWED_WORKER_SKILLS:
            errors.append({task_id: "unsupported worker_skill"})
        role = item.get("role_family", "")
        if "@" in role:
            if role not in active_role_refs:
                errors.append({task_id: f"versioned role is not active: {role}"})
        elif role not in permitted_bare_role_ids:
            errors.append({task_id: f"bare role is not registered for use: {role}"})

        if not item.get("recommendation_ids"):
            errors.append({task_id: "recommendation_ids must be nonempty"})
        unknown_recommendations.update(
            set(item.get("recommendation_ids", [])) - set(EXPECTED_RECOMMENDATIONS)
        )
        for field in (
            "exact_objective",
            "source_boundaries",
            "write_boundaries",
            "implementation_actions",
            "required_artifacts",
            "validator_obligations",
            "completion_criteria",
            "rollback_and_stop_rules",
            "next_task_rules",
        ):
            if not item.get(field):
                errors.append({task_id: f"{field} must be nonempty"})

        human = item.get("human_intervention_boundary", {})
        if human.get("requires_human_gate") != item.get("requires_human_gate"):
            errors.append({task_id: "human-gate parity mismatch"})
        if item.get("requires_human_gate") and not human.get(
            "protected_or_external_conditions"
        ):
            errors.append({task_id: "human-gated task lacks a protected condition"})
        if human.get("relay_may_supply_human_authority") is not False:
            errors.append({task_id: "relay must not supply human authority"})

        for boundary_field in (
            "allow_scope_expansion",
            "physics_promotion_authorized_by_plan",
            "proof_authority_created_by_plan",
            "scientific_claims_changed",
            "distance_to_gr_delta_changed",
            "physics_promotion_authorized",
            "proof_authority",
        ):
            if item.get(boundary_field) is not False:
                errors.append({task_id: f"{boundary_field} must be false"})
        if item.get("max_worker_invocations_per_generation") != 1:
            errors.append({task_id: "worker invocation bound must equal 1"})
        if item.get("max_outer_agentjobs_per_generation") != 1:
            errors.append({task_id: "outer AgentJob bound must equal 1"})

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
                        f"final coverage audit must be {FINAL_COVERAGE_TASK}, got "
                        f"{matrix[recommendation]['final_coverage_audit']}"
                    )
                }
            )
        if matrix[recommendation]["final_goal_disposition"] != [FINAL_GOAL_TASK]:
            errors.append(
                {
                    recommendation: (
                        f"final goal disposition must be {FINAL_GOAL_TASK}, got "
                        f"{matrix[recommendation]['final_goal_disposition']}"
                    )
                }
            )

    graph = backlog.get("dependency_graph", {})
    expected_edges = sum(len(item.get("depends_on", [])) for item in items)
    if graph.get("topological_order") != order:
        errors.append("stored topological order differs from computed order")
    if graph.get("node_count") != len(items) or graph.get("edge_count") != expected_edges:
        errors.append("stored dependency graph counts differ from items")
    expected_human_ids = [
        item["plan_task_id"] for item in items if item.get("requires_human_gate")
    ]
    if backlog.get("human_gate_summary", {}).get("human_gated_work_item_ids") != expected_human_ids:
        errors.append("stored human-gate summary differs from items")

    return {
        "schema_version": "v21_backlog_dependency_report.v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260720-005",
        "plan_task_id": "P0-T02",
        "gate_ids": [
            "v21_backlog_schema_parity",
            "v21_dependency_graph_integrity",
            "v21_recommendation_direct_and_final_coverage",
            "v21_worker_route_integrity",
            "v21_role_registry_integrity",
            "v21_human_authority_boundary",
            "v21_no_physics_authority_boundary",
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
        "final_goal_disposition_task_id": FINAL_GOAL_TASK,
        "role_family_count": len({item.get("role_family") for item in items}),
        "worker_skill_counts": dict(
            sorted(Counter(item.get("worker_skill") for item in items).items())
        ),
        "human_gated_work_item_count": sum(
            bool(item.get("requires_human_gate")) for item in items
        ),
        "dependency_independent_work_item_count": sum(
            bool(item.get("dependency_independent_after_other_human_gates"))
            for item in items
        ),
        "next_route_after_p0_t02": next(
            item["next_task_rules"] for item in items if item["plan_task_id"] == "P0-T02"
        ),
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
            "preserved_scientific_handoff": "handoff-0772",
        },
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="materialize the backlog")
    parser.add_argument("--json", action="store_true", help="print the compact report")
    args = parser.parse_args()

    plan_items = parse_plan()
    if args.write:
        BACKLOG.write_text(
            yaml.safe_dump(
                build_backlog(plan_items),
                sort_keys=False,
                width=120,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )
    if not BACKLOG.exists():
        raise SystemExit(f"missing backlog: {BACKLOG}")
    backlog = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    report = validate(backlog, plan_items)
    REPORT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
