#!/usr/bin/env python3
"""Register and validate the compact V22 P0-T03 plan and backlog."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260808-003"
PLAN_TASK_ID = "P0-T03"
CREATED_AT = "2026-08-08T22:37:10Z"
PLAN_ID = "recommendations_implementation_plan_continue_task-v22"
PLAN_OBJECT_ID = "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V22"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v22.md"
PLAN_SHA256 = "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65"
EXTERNAL_DRAFT = Path(
    "/Users/alex.omegapy/.codex/visualizations/2026/08/08/"
    "019fe2f1-1efd-74f0-9ad6-c0a8d7880d9e/"
    "recommendations_implementation_plan_continue_task-v22.md"
)
PREDECESSOR = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
PREDECESSOR_SHA256 = "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087"
REVIEW = Path(
    "/Users/alex.omegapy/.codex/attachments/64bf115e-0b54-4458-8db0-bb95b4a620ac/pasted-text-1.txt"
)
REVIEW_SHA256 = "1a0d36e14770c4591717cc4f317691f5efcb8ea6f5b300cb8fe63ba001d1eadd"
REGISTRY = ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
GITIGNORE = ROOT / ".gitignore"
SCHEMA = ROOT / "research_control/design/v22_recommendation_backlog_schema.md"
BACKLOG = ROOT / "research_control/design/v22_recommendation_backlog.yaml"
TASK_DIR = ROOT / f"research_control/tasks/{TASK_ID}"
ARTIFACTS = TASK_DIR / "artifacts"
DEPENDENCY_REPORT = ARTIFACTS / "v22_backlog_dependency_graph.json"
COVERAGE_SEED = ARTIFACTS / "v22_recommendation_coverage_seed.json"
SOURCE_HASH_RECEIPT = ARTIFACTS / "v22_plan_source_hash_receipt.json"
REGISTRATION_REPORT = ARTIFACTS / "v22_plan_registration_report.json"
VALIDATION_RECEIPT = ARTIFACTS / "v22_p0_t03_plan_registration_validation.json"
COMPACT_RECEIPT = ARTIFACTS / "v22_p0_t03_compact_receipt.json"
HANDOFF = ROOT / "research_control/handoffs/handoff-0968.yaml"
P0_T02_COMPLETION = ROOT / (
    "research_control/tasks/RT-20260808-002/jobs/completions/"
    "AJC-AJ-RT-20260808-002-001.yaml"
)
BASELINE_MANIFEST = ROOT / (
    "research_control/tasks/RT-20260808-002/artifacts/"
    "v21_terminal_baseline_release_manifest_v1.json"
)
REPRODUCTION_RECEIPT = ROOT / (
    "research_control/tasks/RT-20260808-002/artifacts/"
    "v21_terminal_baseline_reproduction_receipt_v1.json"
)
FREEZE_POLICY = ROOT / (
    "research_control/tasks/RT-20260808-002/artifacts/"
    "v21_terminal_baseline_freeze_policy_v1.md"
)

EXPECTED_RECOMMENDATIONS = [f"V22-R{number:02d}" for number in range(1, 20)]
EXPECTED_SEQUENCE_STEPS = [f"S{number}" for number in range(1, 13)]
EXPECTED_DIRECTIVES = [f"V22-X{number:02d}" for number in range(1, 11)]
EXPECTED_PHASES = [f"P{number}" for number in range(0, 11)]
EXPECTED_EDGE_COUNT = 61
EXPECTED_BASELINE_HASHES = {
    "handoff": "3c9b19e1845bb445365123155cd2dbb7b9a247e84e363c2dc88532f33a4aa149",
    "p0_t02_completion": "392c54ac9659e243c10b748b7a98073aabf6ac179d2b0b0912046b5f024cf0e3",
    "baseline_manifest": "cd4b3fa94e6b1fe3cd5eb576953d3e918b683e3628c0fe63887d9135281d4043",
    "reproduction_receipt": "3b924fe0eef7634c1043c24f6ef8ad9e6fb8b2f9d90a7c216d62f8ab71447007",
    "freeze_policy": "311a0e7553a4f8b75dde012ed751c7a3da515379b8b3b5a02c11638e927d60bf",
}
AUTHORITY_FLAGS = (
    "physics_promotion_authorized_by_plan",
    "canonical_ontology_edit_authorized_by_plan",
    "source_law_adoption_authorized_by_plan",
    "metric_adoption_authorized_by_plan",
    "matter_coupling_adoption_authorized_by_plan",
    "einstein_equation_adoption_authorized_by_plan",
    "benchmark_promotion_authorized_by_plan",
    "gate_chair_verdict_authorized_by_plan",
    "external_reviewer_contact_authorized_by_plan",
    "publication_or_public_release_authorized_by_plan",
    "repository_mutation_authorized_by_plan",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def require(condition: bool, finding_id: str, message: str, errors: list[dict[str, str]]) -> None:
    if not condition:
        errors.append({"finding_id": finding_id, "message": message})


def extract_fenced_yaml(text: str) -> dict[str, Any]:
    match = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not match:
        raise ValueError("missing top-level YAML metadata")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("top-level YAML metadata is not a mapping")
    return value


def extract_manifest(text: str) -> dict[str, Any]:
    marker = text.split("<!-- BEGIN V22_MACHINE_MANIFEST -->", 1)
    if len(marker) != 2:
        raise ValueError("missing V22 manifest start marker")
    body = marker[1].split("<!-- END V22_MACHINE_MANIFEST -->", 1)[0]
    match = re.search(r"```json\n(.*?)\n```", body, re.DOTALL)
    if not match:
        raise ValueError("missing fenced V22 manifest JSON")
    value = json.loads(match.group(1))
    if not isinstance(value, dict):
        raise ValueError("V22 manifest is not a mapping")
    return value


def extract_labeled(section: str, label: str, next_labels: list[str]) -> str:
    start = re.search(rf"\*\*{re.escape(label)}\.\*\*\s*", section)
    if not start:
        return ""
    tail = section[start.end():]
    positions = []
    for next_label in next_labels:
        match = re.search(rf"\n\n\*\*{re.escape(next_label)}\.\*\*", tail)
        if match:
            positions.append(match.start())
    end = min(positions) if positions else len(tail)
    return normalized(tail[:end])


def parse_work_packages(text: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    phase_matches = list(re.finditer(r"^## (P\d+)\.\s+(.+)$", text, re.MULTILINE))
    phases = {match.group(1): match.group(2).strip() for match in phase_matches}
    matches = list(re.finditer(r"^### (P\d+-T\d+) — (.+)$", text, re.MULTILINE))
    items: list[dict[str, Any]] = []
    labels = ["Objective", "Actions", "Outputs", "Acceptance", "Verification", "Stop conditions"]
    section_end = text.find("\n## 8. Execution waves")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else section_end
        section = text[match.start():end]
        preamble = section.split("\n\n**Objective.**", 1)[0]
        track = re.search(r"\*\*Track:\*\*\s*(.*?)\.\s+\*\*Covers:\*\*", preamble, re.DOTALL)
        covers = re.search(r"\*\*Covers:\*\*\s*(.*?)\.\s+\*\*Owner:\*\*", preamble, re.DOTALL)
        owner = re.search(r"\*\*Owner:\*\*\s*(.*?)\.\s+\*\*Depends\s+on:\*\*", preamble, re.DOTALL)
        depends = re.search(r"\*\*Depends\s+on:\*\*\s*(.*)$", preamble, re.DOTALL)
        fields = {
            label.lower().replace(" ", "_"): extract_labeled(section, label, labels[labels.index(label) + 1:])
            for label in labels
        }
        items.append(
            {
                "plan_task_id": match.group(1),
                "phase_id": match.group(1).split("-", 1)[0],
                "title": match.group(2).strip(),
                "track": normalized(track.group(1)) if track else "",
                "owner": normalized(owner.group(1)) if owner else "",
                "declared_coverage_ids": coverage_ids(covers.group(1) if covers else ""),
                "declared_dependency_text": normalized(depends.group(1)) if depends else "",
                **fields,
            }
        )
    return items, phases


def invert_mapping(mapping: dict[str, list[str]]) -> dict[str, list[str]]:
    inverted: dict[str, list[str]] = defaultdict(list)
    for source_id, package_ids in mapping.items():
        for package_id in package_ids:
            inverted[package_id].append(source_id)
    return {key: value for key, value in inverted.items()}


def coverage_ids(text: str) -> list[str]:
    """Expand compact authored coverage ranges while preserving source order."""
    values = re.findall(r"(?:V22-R\d{2}|V22-X\d{2}|S\d{1,2})", text)
    for match in re.finditer(r"V22-R(\d{2})\s+through\s+V22-R(\d{2})", text):
        values.extend(
            f"V22-R{number:02d}"
            for number in range(int(match.group(1)), int(match.group(2)) + 1)
        )
    for match in re.finditer(r"S(\d{1,2})\s+through\s+S(\d{1,2})", text):
        values.extend(
            f"S{number}"
            for number in range(int(match.group(1)), int(match.group(2)) + 1)
        )
    return list(dict.fromkeys(values))


def graph_state(work_packages: dict[str, list[str]]) -> dict[str, Any]:
    ids = list(work_packages)
    indegree = {package_id: 0 for package_id in ids}
    children: dict[str, list[str]] = defaultdict(list)
    edges: list[dict[str, str]] = []
    dangling: list[dict[str, str]] = []
    for package_id, dependencies in work_packages.items():
        for dependency in dependencies:
            edges.append({"from": dependency, "to": package_id})
            if dependency not in indegree:
                dangling.append({"from": dependency, "to": package_id})
                continue
            children[dependency].append(package_id)
            indegree[package_id] += 1
    queue = deque(package_id for package_id in ids if indegree[package_id] == 0)
    order: list[str] = []
    while queue:
        package_id = queue.popleft()
        order.append(package_id)
        for child in children[package_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    reachable: set[str] = set()
    pending = ["P0-T01"]
    while pending:
        package_id = pending.pop()
        if package_id in reachable or package_id not in work_packages:
            continue
        reachable.add(package_id)
        pending.extend(children[package_id])
    return {
        "root": "P0-T01",
        "node_count": len(ids),
        "edge_count": len(edges),
        "edges": edges,
        "topological_order": order,
        "dependencies_acyclic": len(order) == len(ids),
        "dangling_dependencies": dangling,
        "reachable_from_root": [package_id for package_id in ids if package_id in reachable],
        "unreachable_from_root": [package_id for package_id in ids if package_id not in reachable],
    }


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def write_or_compare(path: Path, payload: bytes, write: bool, errors: list[dict[str, str]]) -> None:
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        return
    if not path.is_file():
        errors.append({"finding_id": "V22-REG-OUTPUT-MISSING", "message": f"missing output: {path.relative_to(ROOT)}"})
    elif path.read_bytes() != payload:
        errors.append({"finding_id": "V22-REG-OUTPUT-DRIFT", "message": f"output drift: {path.relative_to(ROOT)}"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors: list[dict[str, str]] = []

    for name, path in {
        "plan": PLAN,
        "external_draft": EXTERNAL_DRAFT,
        "predecessor": PREDECESSOR,
        "review": REVIEW,
        "registry": REGISTRY,
        "gitignore": GITIGNORE,
        "schema": SCHEMA,
        "handoff": HANDOFF,
        "p0_t02_completion": P0_T02_COMPLETION,
        "baseline_manifest": BASELINE_MANIFEST,
        "reproduction_receipt": REPRODUCTION_RECEIPT,
        "freeze_policy": FREEZE_POLICY,
    }.items():
        require(path.is_file(), "V22-REG-001", f"missing required {name}: {path}", errors)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    text = PLAN.read_text(encoding="utf-8")
    metadata = extract_fenced_yaml(text)
    manifest = extract_manifest(text)
    parsed_items, phases = parse_work_packages(text)
    work_packages = manifest.get("work_packages", {})
    recommendations = manifest.get("review_recommendations", {})
    sequence_steps = manifest.get("sequence_steps", {})
    directives = manifest.get("cross_cutting_directives", {})
    conditional_rules = manifest.get("conditional_rules", {})
    package_ids = list(work_packages)
    parsed_ids = [item["plan_task_id"] for item in parsed_items]
    graph = graph_state(work_packages)

    require(sha256(PLAN) == PLAN_SHA256, "V22-REG-002", "registered plan hash differs from reviewed draft", errors)
    require(sha256(EXTERNAL_DRAFT) == PLAN_SHA256, "V22-REG-002A", "external draft hash mismatch", errors)
    require(EXTERNAL_DRAFT.read_bytes() == PLAN.read_bytes(), "V22-REG-002B", "registered plan is not byte-identical to external draft", errors)
    require(sha256(PREDECESSOR) == PREDECESSOR_SHA256, "V22-REG-003", "V21 predecessor hash mismatch", errors)
    require(sha256(REVIEW) == REVIEW_SHA256, "V22-REG-004", "review-source hash mismatch", errors)
    require(len(REVIEW.read_text(encoding="utf-8").splitlines()) == 1683, "V22-REG-005", "review line count mismatch", errors)
    require(metadata.get("plan_id") == PLAN_ID, "V22-REG-006", "plan ID mismatch", errors)
    require(metadata.get("plan_version") == "v22", "V22-REG-007", "plan version mismatch", errors)
    require(metadata.get("recommended_repo_path") == str(PLAN.relative_to(ROOT)), "V22-REG-008", "recommended path mismatch", errors)
    require(metadata.get("review_basis_sha256") == REVIEW_SHA256, "V22-REG-009", "declared review hash mismatch", errors)
    require(metadata.get("review_recommendation_count") == 19, "V22-REG-010", "declared recommendation count mismatch", errors)
    require(metadata.get("review_sequence_step_count") == 12, "V22-REG-011", "declared sequence count mismatch", errors)
    require(metadata.get("review_cross_cutting_directive_count") == 10, "V22-REG-012", "declared directive count mismatch", errors)
    require(metadata.get("phase_count") == 11, "V22-REG-013", "declared phase count mismatch", errors)
    require(metadata.get("work_package_count") == 40, "V22-REG-014", "declared package count mismatch", errors)
    for flag in AUTHORITY_FLAGS:
        require(metadata.get(flag) is False, "V22-REG-015", f"protected authority flag is not false: {flag}", errors)

    require(list(phases) == EXPECTED_PHASES, "V22-REG-016", "phase headings are not exactly P0 through P10", errors)
    require(len(parsed_ids) == 40 and len(set(parsed_ids)) == 40, "V22-REG-017", "work-package headings are not 40 unique IDs", errors)
    require(parsed_ids == package_ids, "V22-REG-018", "heading and manifest package order differ", errors)
    require(sorted(recommendations) == EXPECTED_RECOMMENDATIONS, "V22-REG-019", "recommendation IDs are incomplete", errors)
    require(sorted(sequence_steps, key=lambda value: int(value[1:])) == EXPECTED_SEQUENCE_STEPS, "V22-REG-020", "sequence IDs are incomplete", errors)
    require(sorted(directives) == EXPECTED_DIRECTIVES, "V22-REG-021", "directive IDs are incomplete", errors)
    require(graph["edge_count"] == EXPECTED_EDGE_COUNT, "V22-REG-022", "dependency edge count is not 61", errors)
    require(not graph["dangling_dependencies"], "V22-REG-023", "dependency graph has dangling endpoints", errors)
    require(graph["dependencies_acyclic"], "V22-REG-024", "dependency graph has a cycle", errors)
    require(not graph["unreachable_from_root"], "V22-REG-025", "dependency graph has unreachable packages", errors)
    require(conditional_rules.get("P5", "").startswith("Every P5 package requires"), "V22-REG-026", "Gate B lock missing", errors)
    require("positive P5-T03 Gate D" in conditional_rules.get("P6-T02", ""), "V22-REG-027", "Gate D lock missing", errors)
    require("At most one active source-extension family" in conditional_rules.get("source_candidate_concurrency", ""), "V22-REG-028", "candidate concurrency lock missing", errors)

    mapped_ids = set()
    for mapping in (recommendations, sequence_steps, directives):
        for source_id, mapped in mapping.items():
            for package_id in mapped:
                require(package_id in work_packages, "V22-REG-029", f"{source_id} maps missing package {package_id}", errors)
                mapped_ids.add(package_id)
    orphans = [package_id for package_id in package_ids if package_id not in mapped_ids]
    require(not orphans, "V22-REG-030", f"coverage orphans: {orphans}", errors)

    rec_by_package = invert_mapping(recommendations)
    seq_by_package = invert_mapping(sequence_steps)
    directive_by_package = invert_mapping(directives)
    all_coverage_ids = set(
        EXPECTED_RECOMMENDATIONS + EXPECTED_SEQUENCE_STEPS + EXPECTED_DIRECTIVES
    )
    for item in parsed_items:
        require(all(item[key] for key in ("track", "owner", "objective", "actions", "outputs", "acceptance", "verification", "stop_conditions")), "V22-REG-031", f"incomplete authored package section: {item['plan_task_id']}", errors)
        for declared in item["declared_coverage_ids"]:
            require(
                declared in all_coverage_ids,
                "V22-REG-032",
                f"unknown declared coverage ID {item['plan_task_id']} -> {declared}",
                errors,
            )

    with REGISTRY.open(newline="", encoding="utf-8") as stream:
        registry_rows = [row for row in csv.DictReader(stream) if row["object_id"] == PLAN_OBJECT_ID]
    require(len(registry_rows) == 1, "V22-REG-033", "expected exactly one V22 source registry row", errors)
    if len(registry_rows) == 1:
        row = registry_rows[0]
        require(row["path"] == str(PLAN.relative_to(ROOT)), "V22-REG-034", "V22 registry path mismatch", errors)
        require(row["source_hash"] == PLAN_SHA256, "V22-REG-035", "V22 registry hash mismatch", errors)
        require(row["related_source"] == "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21", "V22-REG-036", "V22 predecessor relation mismatch", errors)
        require(row["authority_status"] == "project_control", "V22-REG-037", "V22 registry authority mismatch", errors)
        require("v21_terminal_baseline_release_manifest_v1.json" in row["notes"], "V22-REG-038", "V22 registry baseline link missing", errors)
        require("not scientific authority" in row["notes"], "V22-REG-039", "V22 registry non-authority note missing", errors)
    require("!implementations_plans/recommendations_implementation_plan_continue_task-v22.md" in GITIGNORE.read_text(encoding="utf-8").splitlines(), "V22-REG-040", "V22 Git ignore exception missing", errors)

    baseline_paths = {
        "handoff": HANDOFF,
        "p0_t02_completion": P0_T02_COMPLETION,
        "baseline_manifest": BASELINE_MANIFEST,
        "reproduction_receipt": REPRODUCTION_RECEIPT,
        "freeze_policy": FREEZE_POLICY,
    }
    for name, path in baseline_paths.items():
        require(sha256(path) == EXPECTED_BASELINE_HASHES[name], "V22-REG-041", f"baseline evidence hash mismatch: {name}", errors)

    declared_by_package = {
        item["plan_task_id"]: item["declared_coverage_ids"] for item in parsed_items
    }
    package_coverage: dict[str, dict[str, list[str]]] = {}
    for package_id in package_ids:
        declared = declared_by_package[package_id]
        package_coverage[package_id] = {
            "recommendation_ids": list(
                dict.fromkeys(
                    rec_by_package.get(package_id, [])
                    + [value for value in declared if value.startswith("V22-R")]
                )
            ),
            "sequence_step_ids": list(
                dict.fromkeys(
                    seq_by_package.get(package_id, [])
                    + [value for value in declared if re.fullmatch(r"S\d+", value)]
                )
            ),
            "cross_cutting_directive_ids": list(
                dict.fromkeys(
                    directive_by_package.get(package_id, [])
                    + [value for value in declared if value.startswith("V22-X")]
                )
            ),
            "machine_manifest_recommendation_ids": rec_by_package.get(package_id, []),
            "machine_manifest_sequence_step_ids": seq_by_package.get(package_id, []),
            "machine_manifest_cross_cutting_directive_ids": directive_by_package.get(package_id, []),
            "authored_section_coverage_ids": declared,
        }
    coverage_seed = {
        "schema_id": "v22_recommendation_coverage_seed_v1",
        "authority": "project_control",
        "status": "validated_traceability_seed",
        "created_at": CREATED_AT,
        "plan_id": PLAN_ID,
        "plan_sha256": PLAN_SHA256,
        "review_recommendations": recommendations,
        "sequence_steps": sequence_steps,
        "cross_cutting_directives": directives,
        "package_coverage": package_coverage,
        "counts": {
            "recommendations": len(recommendations),
            "sequence_steps": len(sequence_steps),
            "cross_cutting_directives": len(directives),
            "work_packages": len(package_ids),
            "orphans": len(orphans),
        },
        "authority_limits": {
            "coverage_is_implementation_evidence": False,
            "scientific_status_changed": False,
            "physics_promotion_authorized": False,
        },
    }
    dependency_report = {
        "schema_id": "v22_backlog_dependency_graph_v1",
        "authority": "project_control",
        "created_at": CREATED_AT,
        "plan_id": PLAN_ID,
        "plan_sha256": PLAN_SHA256,
        **graph,
        "conditional_rules": conditional_rules,
        "orphan_packages": orphans,
        "next_dependency_ready_after_p0_t03": ["P1-T01"],
        "automatic_execution_authorized": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
    }
    backlog_items = []
    for item in parsed_items:
        package_id = item["plan_task_id"]
        if package_id in {"P0-T01", "P0-T02"}:
            implementation_status = "completed"
        elif package_id == "P0-T03":
            implementation_status = "completed_checkpoint_pending"
        elif package_id.startswith("P5-") or package_id in {"P6-T02", "P6-T03"}:
            implementation_status = "conditionally_locked"
        else:
            implementation_status = "pending"
        backlog_items.append(
            {
                "plan_task_id": package_id,
                "phase_id": item["phase_id"],
                "title": item["title"],
                "track": item["track"],
                "owner": item["owner"],
                "declared_coverage_ids": item["declared_coverage_ids"],
                "recommendation_ids": package_coverage[package_id]["recommendation_ids"],
                "sequence_step_ids": package_coverage[package_id]["sequence_step_ids"],
                "cross_cutting_directive_ids": package_coverage[package_id]["cross_cutting_directive_ids"],
                "depends_on": work_packages[package_id],
                "objective": item["objective"],
                "actions": item["actions"],
                "outputs": item["outputs"],
                "acceptance": item["acceptance"],
                "verification": item["verification"],
                "stop_conditions": item["stop_conditions"],
                "implementation_status": implementation_status,
                "requires_separate_agentjob": True,
                "max_outer_agentjobs_per_invocation": 1,
                "automatic_execution_authorized": False,
                "scientific_claims_changed": False,
                "distance_to_gr_delta_changed": False,
                "physics_promotion_authorized": False,
                "proof_authority": False,
            }
        )
    backlog = {
        "schema_id": "v22_recommendation_backlog_v1",
        "authority": "project_control",
        "status": "draft_control_backlog",
        "created_at": CREATED_AT,
        "source_plan": {
            "plan_id": PLAN_ID,
            "plan_path": str(PLAN.relative_to(ROOT)),
            "object_id": PLAN_OBJECT_ID,
            "source_hash": PLAN_SHA256,
            "git_blob_sha1": git_blob_sha1(PLAN),
            "predecessor_object_id": "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21",
            "predecessor_hash": PREDECESSOR_SHA256,
            "review_basis_sha256": REVIEW_SHA256,
        },
        "source_evidence": {
            name: {"path": str(path.relative_to(ROOT)), "sha256": EXPECTED_BASELINE_HASHES[name]}
            for name, path in baseline_paths.items()
        },
        "scope": {
            "plan_task_id": PLAN_TASK_ID,
            "phase_count": len(phases),
            "work_package_count": len(package_ids),
            "dependency_edge_count": graph["edge_count"],
            "execution_model": "one_bounded_agentjob_per_continue_research_invocation",
            "automatic_program_launch": False,
        },
        "coverage_rules": {
            "expected_recommendation_ids": EXPECTED_RECOMMENDATIONS,
            "expected_sequence_step_ids": EXPECTED_SEQUENCE_STEPS,
            "expected_cross_cutting_directive_ids": EXPECTED_DIRECTIVES,
            "every_package_requires_traceability": True,
        },
        "coverage_summary": coverage_seed["counts"],
        "conditional_rules": conditional_rules,
        "dependency_graph": graph,
        "items": backlog_items,
        "authority_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "source_law_adoption_authorized": False,
            "metric_adoption_authorized": False,
            "matter_coupling_adoption_authorized": False,
            "einstein_equation_adoption_authorized": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "gate_chair_verdict_authorized": False,
            "external_action_authorized": False,
        },
    }
    source_receipt = {
        "schema_id": "v22_plan_source_hash_receipt_v1",
        "status": "PASS_EXACT_REVIEW_AND_PLAN_SOURCE_IDENTITY" if not errors else "FAIL",
        "task_id": TASK_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "sources": {
            "review": {"path": str(REVIEW), "line_count": 1683, "sha256": REVIEW_SHA256},
            "registered_plan": {"path": str(PLAN.relative_to(ROOT)), "sha256": PLAN_SHA256, "git_blob_sha1": git_blob_sha1(PLAN)},
            "predecessor_plan": {"path": str(PREDECESSOR.relative_to(ROOT)), "sha256": PREDECESSOR_SHA256},
            **{
                name: {"path": str(path.relative_to(ROOT)), "sha256": EXPECTED_BASELINE_HASHES[name]}
                for name, path in baseline_paths.items()
            },
        },
        "copy_identity": {
            "external_draft_path": str(EXTERNAL_DRAFT),
            "registered_path": str(PLAN.relative_to(ROOT)),
            "byte_identical": EXTERNAL_DRAFT.read_bytes() == PLAN.read_bytes(),
            "sha256": PLAN_SHA256,
        },
        "authority_note": "Exact source identity and registration are project-control evidence only and are not scientific proof or promotion authority.",
    }
    registration_report = {
        "schema_id": "v22_plan_registration_report_v1",
        "status": "PASS_REGISTERED_DRAFT_CONTROL" if not errors else "FAIL",
        "task_id": TASK_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "plan_id": PLAN_ID,
        "plan_object_id": PLAN_OBJECT_ID,
        "plan_path": str(PLAN.relative_to(ROOT)),
        "plan_sha256": PLAN_SHA256,
        "registry_path": str(REGISTRY.relative_to(ROOT)),
        "registry_row_count": len(registry_rows),
        "predecessor_object_id": "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21",
        "terminal_baseline_manifest_path": str(BASELINE_MANIFEST.relative_to(ROOT)),
        "terminal_baseline_manifest_sha256": EXPECTED_BASELINE_HASHES["baseline_manifest"],
        "counts": {
            "recommendations": len(recommendations),
            "sequence_steps": len(sequence_steps),
            "cross_cutting_directives": len(directives),
            "phases": len(phases),
            "work_packages": len(package_ids),
            "dependency_edges": graph["edge_count"],
            "cycles": 0 if graph["dependencies_acyclic"] else 1,
            "orphans": len(orphans),
        },
        "registration_launches_program": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
    }

    primary_payloads = {
        BACKLOG: yaml_bytes(backlog),
        DEPENDENCY_REPORT: json_bytes(dependency_report),
        COVERAGE_SEED: json_bytes(coverage_seed),
        SOURCE_HASH_RECEIPT: json_bytes(source_receipt),
        REGISTRATION_REPORT: json_bytes(registration_report),
    }
    output_hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(payload).hexdigest()
        for path, payload in primary_payloads.items()
    }
    validation = {
        "schema_id": "v22_p0_t03_plan_registration_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": TASK_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "finding_count": len(errors),
        "findings": errors,
        "checks": {
            "review_hash_and_line_count": sha256(REVIEW) == REVIEW_SHA256,
            "plan_copy_identity": sha256(PLAN) == PLAN_SHA256 and EXTERNAL_DRAFT.read_bytes() == PLAN.read_bytes(),
            "predecessor_identity": sha256(PREDECESSOR) == PREDECESSOR_SHA256,
            "terminal_baseline_dependency": all(sha256(path) == EXPECTED_BASELINE_HASHES[name] for name, path in baseline_paths.items()),
            "source_registry_single_row": len(registry_rows) == 1,
            "recommendation_coverage_19_of_19": len(recommendations) == 19,
            "sequence_coverage_12_of_12": len(sequence_steps) == 12,
            "directive_coverage_10_of_10": len(directives) == 10,
            "phase_count_11": len(phases) == 11,
            "work_package_count_40": len(package_ids) == 40,
            "dependency_edge_count_61": graph["edge_count"] == 61,
            "dependency_graph_acyclic": graph["dependencies_acyclic"],
            "dependency_graph_reachable": not graph["unreachable_from_root"],
            "coverage_orphans_zero": not orphans,
            "conditional_gate_locks_present": not any(error["finding_id"] in {"V22-REG-026", "V22-REG-027", "V22-REG-028"} for error in errors),
            "protected_authority_flags_false": all(metadata.get(flag) is False for flag in AUTHORITY_FLAGS),
        },
        "output_hashes": output_hashes,
        "authority_note": "PASS establishes deterministic project-control registration and traceability only.",
    }
    validation_payload = json_bytes(validation)
    compact = {
        "schema_id": "v22_p0_t03_compact_receipt_v1",
        "receipt_id": "RECEIPT-V22-P0-T03-REGISTRATION-001",
        "status": "PASS_REGISTERED_COMPACT_V22_BACKLOG" if not errors else "FAIL",
        "task_id": TASK_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "plan_sha256": PLAN_SHA256,
        "review_sha256": REVIEW_SHA256,
        "registered_object_id": PLAN_OBJECT_ID,
        "recommendation_count": 19,
        "sequence_step_count": 12,
        "cross_cutting_directive_count": 10,
        "phase_count": 11,
        "work_package_count": 40,
        "dependency_edge_count": graph["edge_count"],
        "dependency_cycle_count": 0 if graph["dependencies_acyclic"] else 1,
        "orphan_count": len(orphans),
        "next_dependency_ready_plan_task_id": "P1-T01",
        "next_task_executed": False,
        "source_hashes": {
            **output_hashes,
            str(VALIDATION_RECEIPT.relative_to(ROOT)): hashlib.sha256(validation_payload).hexdigest(),
            str(SCHEMA.relative_to(ROOT)): sha256(SCHEMA),
        },
        "authority_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "gate_or_benchmark_status_changed": False,
            "program_launch_authorized": False,
            "tag_or_public_release_created": False,
            "publication_or_external_action_authorized": False,
        },
    }
    payloads = {
        **primary_payloads,
        VALIDATION_RECEIPT: validation_payload,
        COMPACT_RECEIPT: json_bytes(compact),
    }
    for path, payload in payloads.items():
        write_or_compare(path, payload, args.write, errors)

    status = "PASS" if not errors else "FAIL"
    result = {
        "status": status,
        "task_id": TASK_ID,
        "plan_task_id": PLAN_TASK_ID,
        "finding_count": len(errors),
        "findings": errors,
        "counts": registration_report["counts"],
        "written": args.write,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
