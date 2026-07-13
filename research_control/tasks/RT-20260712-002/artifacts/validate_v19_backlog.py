#!/usr/bin/env python3
"""Materialize and validate the v19 P0-T02 recommendation backlog."""
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
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v19.md"
BACKLOG = ROOT / "research_control/design/v19_validation_overhead_backlog.yaml"
ROLE_REGISTRY = ROOT / "registries/AGENT_ROLE_REGISTRY.csv"
REPORT = ROOT / "research_control/tasks/RT-20260712-002/artifacts/v19_backlog_validation_report.json"
EXPECTED_RECOMMENDATIONS = [f"V19-R{index:02d}" for index in range(1, 49)]
FINAL_COVERAGE_TASK = "P12-T06"
TASK_HEADING = re.compile(r"^### (P\d+-T\d+):\s*(.+)$", re.MULTILINE)
REQUIRED_ITEM_FIELDS = {
    "plan_task_id",
    "phase_id",
    "task_type",
    "title",
    "recommendation_ids",
    "depends_on",
    "role_family",
    "controlling_skill",
    "migration_epoch",
    "expected_source_changes",
    "expected_generated_changes",
    "required_gates",
    "validation_obligations",
    "performance_evidence",
    "rollback_triggers",
    "next_route_on_success",
    "recommendation_coverage_role",
}
GENERATED_PREFIXES = (
    "output/",
    "wiki/",
    "research_control/current_frontier.md",
    "research_control/tasks/TASK_INDEX.",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_markup(text: str) -> str:
    return text.replace("`", "").strip()


def subsection(section: str, heading: str) -> str:
    match = re.search(
        rf"^#### {re.escape(heading)}\s*$\n(.*?)(?=^#### |\Z)",
        section,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def bullets(text: str) -> list[str]:
    return [strip_markup(match.group(1)) for match in re.finditer(r"^-\s+(.+)$", text, re.MULTILINE)]


def planned_paths(section: str) -> list[str]:
    result = []
    for entry in bullets(subsection(section, "Planned write scope")):
        if entry.startswith("Standard task-local") or entry.startswith("Any path outside"):
            continue
        result.append(entry)
    return result


def required_gates(epoch: str, task_id: str) -> list[str]:
    gates = ["task_local_focused_validation", "git_diff_check"]
    if epoch == "legacy":
        gates.insert(0, "legacy_acceptance_path")
    elif epoch == "legacy_consolidated":
        gates.insert(0, "legacy_consolidated_acceptance_path")
    elif epoch == "shadow_planner":
        gates[0:0] = ["legacy_authoritative_acceptance", "planner_shadow_comparison"]
    elif epoch in {"planner_authoritative", "legacy_retired"}:
        gates.insert(0, "planner_checkpoint_profile")
    else:
        gates.insert(0, "unknown_epoch_fail_closed")
    if task_id == "P12-T07":
        gates.append("research_handoff_program_state_consistency")
    return gates


def parse_next_route(section: str, task_id: str) -> str:
    handoff = subsection(section, "Handoff rule")
    select = re.search(r"On PASS, select `([^`]+)`", handoff)
    if select:
        return select.group(1)
    if task_id == "P12-T07" and "ordinary scientific next action" in handoff:
        return "ordinary_scientific_next_action_or_bounded_v19_repair"
    raise ValueError(f"cannot parse PASS route for {task_id}")


def parse_plan() -> list[dict[str, Any]]:
    text = PLAN.read_text(encoding="utf-8")
    headings = list(TASK_HEADING.finditer(text))
    items = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.start():end]
        yaml_match = re.search(r"```yaml\n(.*?)\n```", section, re.DOTALL)
        if not yaml_match:
            raise ValueError(f"missing YAML task block for {heading.group(1)}")
        source = yaml.safe_load(yaml_match.group(1))
        paths = planned_paths(section)
        generated = [path for path in paths if path.startswith(GENERATED_PREFIXES)]
        sources = [path for path in paths if path not in generated]
        generated.append("policy_required_registry_memory_wiki_derivatives")
        validation = bullets(subsection(section, "Required validation and evidence"))
        performance_terms = re.compile(
            r"benchmark|duration|subprocess|output|cache|timing|performance|measurement|runtime|wall time",
            re.IGNORECASE,
        )
        performance_specific = [entry for entry in validation if performance_terms.search(entry)]
        task_id = source["plan_task_id"]
        coverage_role = "support"
        if task_id == FINAL_COVERAGE_TASK:
            coverage_role = "final_coverage_audit"
        elif task_id not in {"P0-T01", "P0-T02", "P12-T07"}:
            coverage_role = "direct_implementation"
        item = dict(source)
        item.update(
            {
                "expected_source_changes": sources,
                "expected_generated_changes": generated,
                "required_gates": required_gates(source["migration_epoch"], task_id),
                "validation_obligations": validation,
                "performance_evidence": {
                    "before_reference": "reviews/verification_validation_testing_overhead_audit_2026-07-12.md",
                    "required_metrics": [
                        "duration_seconds",
                        "subprocess_count",
                        "output_bytes",
                        "cache_hits",
                        "cache_misses",
                    ],
                    "task_specific_requirements": performance_specific,
                },
                "rollback_triggers": bullets(subsection(section, "Stop, repair, and rollback conditions")),
                "next_route_on_success": parse_next_route(section, task_id),
                "next_route_on_repair": f"bounded_repair_preserving_{task_id}_coverage",
                "next_route_on_blocked": "preserve_evidence_and_report_narrow_blocker",
                "recommendation_coverage_role": coverage_role,
                "implementation_status": "completed" if task_id in {"P0-T01", "P0-T02"} else "pending",
            }
        )
        items.append(item)
    return items


def active_roles() -> set[str]:
    roles = set()
    with ROLE_REGISTRY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["status"] == "active":
                roles.add(f"{row['role_id']}@{row['version']}")
    return roles


def topological_order(items: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    ids = [item["plan_task_id"] for item in items]
    children: dict[str, list[str]] = defaultdict(list)
    indegree = {task_id: 0 for task_id in ids}
    errors = []
    for item in items:
        task_id = item["plan_task_id"]
        for dependency in item.get("depends_on", []):
            if dependency not in indegree:
                errors.append(f"{task_id} has dangling dependency {dependency}")
                continue
            children[dependency].append(task_id)
            indegree[task_id] += 1
    queue = deque(task_id for task_id in ids if indegree[task_id] == 0)
    order = []
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


def build_backlog(items: list[dict[str, Any]]) -> dict[str, Any]:
    order, graph_errors = topological_order(items)
    if graph_errors:
        raise ValueError("; ".join(graph_errors))
    edges = [
        {"from": dependency, "to": item["plan_task_id"]}
        for item in items
        for dependency in item["depends_on"]
    ]
    return {
        "schema_id": "v19_validation_overhead_backlog_v1",
        "authority": "project_control",
        "status": "draft_control_backlog",
        "created_at": "2026-07-12T21:03:24Z",
        "source_plan": {
            "plan_id": "recommendations_implementation_plan_continue_task-v19",
            "plan_path": str(PLAN.relative_to(ROOT)),
            "object_id": "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V19",
            "source_hash": sha256(PLAN),
        },
        "scope": {
            "execution_mode": "one_bounded_agentjob_per_plan_task",
            "dependency_model": "explicit_plan_dependencies_v1",
            "task_count": len(items),
            "phase_count": len({item["phase_id"] for item in items}),
            "physics_delta_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "ordinary_research_route_preserved": "EqSrc_family_closure_repair_or_stress",
        },
        "recommendation_coverage_rules": {
            "expected_recommendation_ids": EXPECTED_RECOMMENDATIONS,
            "direct_implementation_role": "direct_implementation",
            "final_coverage_audit_task_id": FINAL_COVERAGE_TASK,
            "final_coverage_audit_role": "final_coverage_audit",
        },
        "dependency_graph": {
            "root_task_id": "P0-T01",
            "acyclic": True,
            "all_tasks_reachable": True,
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
    roles = active_roles()

    if backlog.get("authority") != "project_control":
        errors.append("backlog authority must be project_control")
    if Counter(ids) != Counter(plan_ids):
        errors.append(
            {
                "task_parity": {
                    "missing": sorted(set(plan_ids) - set(ids)),
                    "extra": sorted(set(ids) - set(plan_ids)),
                    "duplicates": sorted(task_id for task_id, count in Counter(ids).items() if count > 1),
                }
            }
        )
    plan_by_id = {item["plan_task_id"]: item for item in plan_items}
    exact_fields = [
        "phase_id",
        "task_type",
        "title",
        "recommendation_ids",
        "depends_on",
        "role_family",
        "controlling_skill",
        "migration_epoch",
    ]
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
        if not item.get("recommendation_ids"):
            errors.append({task_id: "recommendation_ids must be nonempty"})
        if item.get("role_family") not in roles:
            errors.append({task_id: f"unregistered or inactive role {item.get('role_family')}"})
        if not item.get("expected_source_changes"):
            errors.append({task_id: "expected_source_changes must be nonempty"})
        if not item.get("expected_generated_changes"):
            errors.append({task_id: "expected_generated_changes must be nonempty"})
        if not item.get("required_gates") or not item.get("validation_obligations"):
            errors.append({task_id: "validator obligations must be nonempty"})
        if not item.get("performance_evidence", {}).get("required_metrics"):
            errors.append({task_id: "performance evidence metrics must be nonempty"})
        if not item.get("rollback_triggers"):
            errors.append({task_id: "rollback criteria must be nonempty"})
        if not item.get("next_route_on_success"):
            errors.append({task_id: "next route must be nonempty"})
        if item.get("scientific_claims_changed") is not False:
            errors.append({task_id: "scientific_claims_changed must be false"})
        if item.get("physics_delta_authorized") is not False:
            errors.append({task_id: "physics_delta_authorized must be false"})
        if item.get("physics_promotion_authorized") is not False:
            errors.append({task_id: "physics_promotion_authorized must be false"})
        if item.get("proof_authority") is not False:
            errors.append({task_id: "proof_authority must be false"})

    order, graph_errors = topological_order(items)
    errors.extend(graph_errors)
    root_reachable = set()
    children: dict[str, list[str]] = defaultdict(list)
    for item in items:
        for dependency in item.get("depends_on", []):
            children[dependency].append(item["plan_task_id"])
    queue = deque(["P0-T01"] if "P0-T01" in item_by_id else [])
    while queue:
        task_id = queue.popleft()
        if task_id in root_reachable:
            continue
        root_reachable.add(task_id)
        queue.extend(children[task_id])
    orphans = sorted(set(ids) - root_reachable)
    if orphans:
        errors.append({"orphan_tasks": orphans})

    direct_by_recommendation: dict[str, list[str]] = defaultdict(list)
    final_by_recommendation: dict[str, list[str]] = defaultdict(list)
    for item in items:
        target = direct_by_recommendation
        if item.get("recommendation_coverage_role") == "final_coverage_audit":
            target = final_by_recommendation
        for recommendation in item.get("recommendation_ids", []):
            if item.get("recommendation_coverage_role") in {"direct_implementation", "final_coverage_audit"}:
                target[recommendation].append(item["plan_task_id"])
    for recommendation in EXPECTED_RECOMMENDATIONS:
        if not direct_by_recommendation[recommendation]:
            errors.append({recommendation: "missing direct implementation coverage"})
        if final_by_recommendation[recommendation] != [FINAL_COVERAGE_TASK]:
            errors.append(
                {recommendation: f"final coverage must be {FINAL_COVERAGE_TASK}, got {final_by_recommendation[recommendation]}"}
            )

    graph = backlog.get("dependency_graph", {})
    expected_edges = sum(len(item.get("depends_on", [])) for item in items)
    if graph.get("topological_order") != order:
        errors.append("stored topological order does not match computed order")
    if graph.get("node_count") != len(items) or graph.get("edge_count") != expected_edges:
        errors.append("stored dependency graph counts do not match backlog items")

    return {
        "status": "PASS" if not errors else "FAIL",
        "gate_ids": [
            "v19_backlog_schema_parity",
            "v19_dependency_graph_integrity",
            "v19_recommendation_coverage",
            "v19_role_registry_integrity",
            "v19_no_physics_authority_boundary",
        ],
        "plan_task_count": len(plan_ids),
        "backlog_item_count": len(items),
        "phase_count": len({item.get("phase_id") for item in items}),
        "dependency_edge_count": expected_edges,
        "dependencies_acyclic": not graph_errors,
        "all_tasks_reachable_from_p0_t01": not orphans,
        "orphan_tasks": orphans,
        "recommendation_count": len(EXPECTED_RECOMMENDATIONS),
        "recommendation_direct_coverage": dict(direct_by_recommendation),
        "recommendation_final_audit_coverage": dict(final_by_recommendation),
        "registered_role_families": sorted({item.get("role_family") for item in items}),
        "next_route_after_p0_t02": item_by_id.get("P0-T02", {}).get("next_route_on_success"),
        "source_hashes": {
            "plan": sha256(PLAN),
            "backlog": sha256(BACKLOG),
        },
        "no_physics_authority_boundary": {
            "scientific_claims_changed": False,
            "physics_delta_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "ordinary_research_route_preserved": "EqSrc_family_closure_repair_or_stress",
        },
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="materialize the deterministic backlog before validation")
    args = parser.parse_args()
    plan_items = parse_plan()
    if args.write:
        BACKLOG.parent.mkdir(parents=True, exist_ok=True)
        BACKLOG.write_text(
            yaml.safe_dump(build_backlog(plan_items), sort_keys=False, width=1000, allow_unicode=True),
            encoding="utf-8",
        )
    if not BACKLOG.exists():
        raise SystemExit(f"missing backlog: {BACKLOG}")
    backlog = yaml.safe_load(BACKLOG.read_text(encoding="utf-8"))
    report = validate(backlog, plan_items)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
