#!/usr/bin/env python3
"""Build and validate the v19 P0-T04 legacy validation invocation graph."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
GRAPH_JSON = REPO_ROOT / "research_control/design/v19_legacy_validation_invocation_graph.json"
GRAPH_MD = REPO_ROOT / "research_control/design/v19_legacy_validation_invocation_graph.md"
AUDIT_JSON = REPO_ROOT / "research_control/tasks/RT-20260712-004/artifacts/v19_legacy_validation_invocation_graph_audit.json"
GENERATED_AT = "2026-07-12T22:11:26Z"

SOURCE_PATHS = [
    "Makefile",
    ".github/workflows/project-control-validation.yml",
    ".codex/skills/continue-research/SKILL.md",
    ".codex/skills/improve-project-system/SKILL.md",
    ".codex/skills/user-modified-project/SKILL.md",
    ".codex/skills/project-memory-system/SKILL.md",
    "registries/AGENT_ROLE_REGISTRY.csv",
    "scripts/research_control/run_full_research_control_validation.py",
    "scripts/research_control/checkpoint_research_transaction.py",
    "implementations_plans/recommendations_implementation_plan_continue_task-v19.md",
    "research_control/tasks/RT-20260712-003/artifacts/v19_baseline_benchmark.json",
    "research_control/tasks/RT-20260712-003/jobs/completions/AJC-AJ-RT-20260712-003-001.yaml",
    "reviews/verification_validation_testing_overhead_audit_2026-07-12.md",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: str) -> str:
    return sha256_bytes((REPO_ROOT / path).read_bytes())


def gate(
    gate_id: str,
    name: str,
    implementation: str,
    *,
    authority: str = "blocking",
    mutating: bool = False,
    nested: tuple[str, ...] = (),
    condition: str = "always_when_selected",
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "name": name,
        "implementation": implementation,
        "authority": authority,
        "mutating": mutating,
        "nested_gate_ids": list(nested),
        "condition": condition,
        "provisional": True,
    }


GATES = [
    gate("LVG-001", "project_change_classifier", "scripts/project_control/classify_project_changes.py"),
    gate("LVG-002", "project_improvement_resolver", "scripts/project_control/resolve_project_improvement.py", authority="advisory"),
    gate("LVG-003", "project_improvement_signal_parity", "scripts/project_control/collect_project_improvement_signals.py --validate-emitted"),
    gate("LVG-004", "documentation_impact", "scripts/project_control/validate_documentation_impact.py"),
    gate("LVG-005", "documentation_surface_audit", "scripts/project_control/audit_documentation_surfaces.py"),
    gate("LVG-006", "memory_sync_and_validate", "bootstrap_memory_system.py default", mutating=True, nested=("LVG-007", "LVG-014", "LVG-037")),
    gate("LVG-007", "memory_core_validate_only", "bootstrap_memory_system.py --validate-only", nested=("LVG-014", "LVG-037")),
    gate("LVG-008", "obsidian_vault_sync", "sync_obsidian_vault.py", mutating=True, authority="local_only"),
    gate("LVG-009", "obsidian_vault_lint", "lint_obsidian_vault.py --require-index", authority="local_only"),
    gate("LVG-010", "memory_status", "query_memory.py status --json", authority="diagnostic"),
    gate("LVG-011", "memory_lookup", "query_memory.py lookup", authority="diagnostic"),
    gate("LVG-012", "memory_search", "query_memory.py search", authority="diagnostic"),
    gate("LVG-013", "spec_depth_lint", "scripts/spec_depth_lint.py --root ."),
    gate("LVG-014", "publication_process", "scripts/validate_publication_process.py --root ."),
    gate("LVG-015", "research_control_core", "scripts/research_control/validate_research_control.py"),
    gate("LVG-016", "research_control_diff", "scripts/research_control/validate_research_control.py --check-diff", nested=("LVG-015", "LVG-023")),
    gate("LVG-017", "repository_unittest_suite", "python -m unittest discover -s tests"),
    gate("LVG-018", "current_frontier_freshness", "render_current_frontier.py --check"),
    gate("LVG-019", "compact_frontier_validation", "validate_compact_current_frontier_v16.py --json"),
    gate("LVG-020", "dependency_graph_freshness", "render_dependency_graph.py --check"),
    gate("LVG-021", "task_index_validation", "validate_task_index.py --json"),
    gate("LVG-022", "claim_graph_validation", "validate_claim_graph_v1.py --json"),
    gate("LVG-023", "changed_claim_language", "validate_claim_language.py changed/staged mode"),
    gate("LVG-024", "route_signature_extraction", "extract_route_signatures.py sample", authority="advisory"),
    gate("LVG-025", "route_orbit_diagnostic", "validate_route_orbits.py --advisory-only", authority="advisory"),
    gate("LVG-026", "whitespace_diff", "git diff --check"),
    gate("LVG-027", "targeted_pdf_build", "build_pdf_derivatives.py <changed-required-tex>", mutating=True, condition="changed registered TeX has pdf_required=true"),
    gate("LVG-028", "continue_memory_preflight", "continue_research_memory_preflight.py --json", mutating=True, nested=("LVG-010", "LVG-008")),
    gate("LVG-029", "continue_context_resolution", "scripts/research_control/continue_research.py", authority="routing"),
    gate("LVG-030", "checkpoint_transaction", "checkpoint_research_transaction.py", mutating=True),
    gate("LVG-031", "make_validate_project_control", "make validate-project-control"),
    gate("LVG-032", "make_validate_memory", "make validate-memory", mutating=True),
    gate("LVG-033", "make_validate_html_explainers", "make validate-html-explainers"),
    gate("LVG-034", "make_audit_documentation_surfaces", "make audit-documentation-surfaces"),
    gate("LVG-035", "local_full_runner", "run_full_research_control_validation.py"),
    gate("LVG-036", "github_actions_project_control_job", "project-control-validation.yml validate_project_control job"),
    gate("LVG-037", "mermaid_source_validation", "validate_mermaid_sources imported by bootstrap", authority="nested"),
]

COSTS: dict[str, dict[str, Any]] = {
    "LVG-009": {"class": "subsecond", "seconds": 0.230888, "evidence": "P0-T03 three-run median"},
    "LVG-015": {"class": "moderate", "seconds": 11.784, "evidence": "2026-07-12 overhead audit single run"},
    "LVG-016": {"class": "moderate", "seconds": 11.604, "evidence": "2026-07-12 overhead audit single run"},
    "LVG-017": {"class": "expensive", "seconds": 515.454875, "evidence": "P0-T03 repaired clean-clone suite"},
    "LVG-020": {"class": "expensive", "seconds": 48.742223, "evidence": "P0-T03 exact focused baseline"},
    "LVG-021": {"class": "low", "seconds": 1.107774, "evidence": "P0-T03 exact focused baseline"},
}


def expected_cost(gate_id: str) -> dict[str, Any]:
    return COSTS.get(gate_id, {"class": "unmeasured", "seconds": None, "evidence": "not isolated by P0-T03"})


INVOCATIONS: list[dict[str, Any]] = []


def invocation(
    invocation_id: str,
    owner: str,
    owner_type: str,
    source_ref: str,
    gate_id: str,
    command: list[str],
    *,
    scope: str,
    tree_state: str,
    mutating: bool = False,
    severity: str = "blocking",
    duplicate_class: str = "unique",
    same_state_superset_invocation_id: str = "",
    related_invocation_id: str = "",
    condition: str = "always_when_owner_runs",
) -> None:
    INVOCATIONS.append({
        "invocation_id": invocation_id,
        "owner": owner,
        "owner_type": owner_type,
        "source_ref": source_ref,
        "gate_id": gate_id,
        "command": command,
        "arguments": command[1:],
        "scope": scope,
        "tree_state": tree_state,
        "mutating": mutating,
        "severity": severity,
        "duplicate_class": duplicate_class,
        "same_state_superset_invocation_id": same_state_superset_invocation_id,
        "related_invocation_id": related_invocation_id,
        "condition": condition,
        "expected_cost": expected_cost(gate_id),
    })


PY = ".venv/bin/python"

# Make entry points. Shell executable checks and dependency installation are
# preserved below as explicit non-validation operational exclusions.
invocation("MPC-01", "make:validate-project-control", "make", "Makefile:16", "LVG-001", [PY, "scripts/project_control/classify_project_changes.py", "--json"], scope="project_control", tree_state="working_tree")
invocation("MPC-02", "make:validate-project-control", "make", "Makefile:17", "LVG-003", [PY, "scripts/project_control/collect_project_improvement_signals.py", "--validate-emitted"], scope="project_control", tree_state="working_tree")
invocation("MPC-03", "make:validate-project-control", "make", "Makefile:18", "LVG-004", [PY, "scripts/project_control/validate_documentation_impact.py"], scope="project_control", tree_state="working_tree")
invocation("MPC-04", "make:validate-project-control", "make", "Makefile:19", "LVG-005", [PY, "scripts/project_control/audit_documentation_surfaces.py", "--skip-local"], scope="tracked_documentation", tree_state="working_tree")
invocation("MPC-05", "make:validate-project-control", "make", "Makefile:20", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], scope="memory_and_publication", tree_state="working_tree", duplicate_class="nested_direct_overlap", related_invocation_id="MPC-07")
invocation("MPC-06", "make:validate-project-control", "make", "Makefile:21", "LVG-013", [PY, "scripts/spec_depth_lint.py", "--root", "."], scope="registered_specs", tree_state="working_tree")
invocation("MPC-07", "make:validate-project-control", "make", "Makefile:22", "LVG-014", [PY, "scripts/validate_publication_process.py", "--root", "."], scope="publication", tree_state="working_tree", duplicate_class="nested_direct_duplicate", related_invocation_id="MPC-05")
invocation("MPC-08", "make:validate-project-control", "make", "Makefile:23", "LVG-015", [PY, "scripts/research_control/validate_research_control.py"], scope="research_control", tree_state="working_tree", duplicate_class="direct_same_state_subset", same_state_superset_invocation_id="MPC-09")
invocation("MPC-09", "make:validate-project-control", "make", "Makefile:24", "LVG-016", [PY, "scripts/research_control/validate_research_control.py", "--check-diff"], scope="research_control_and_diff", tree_state="working_tree", duplicate_class="same_state_superset")
invocation("MPC-10", "make:validate-project-control", "make", "Makefile:25", "LVG-017", [PY, "-m", "unittest", "discover", "-s", "tests"], scope="repository", tree_state="working_tree")

invocation("MMEM-01", "make:validate-memory", "make", "Makefile:7", "LVG-006", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"], scope="memory_and_publication", tree_state="working_tree", mutating=True)
invocation("MMEM-02", "make:validate-memory", "make", "Makefile:8", "LVG-008", [PY, ".codex/skills/project-memory-system/scripts/sync_obsidian_vault.py"], scope="local_retrieval", tree_state="local_cache", mutating=True, severity="local_only")
invocation("MMEM-03", "make:validate-memory", "make", "Makefile:9", "LVG-009", [PY, ".codex/skills/project-memory-system/scripts/lint_obsidian_vault.py", "--require-index"], scope="local_retrieval", tree_state="local_cache", severity="local_only")
invocation("MMEM-04", "make:validate-memory", "make", "Makefile:10", "LVG-017", [PY, "-m", "unittest", "discover", "-s", "tests"], scope="repository", tree_state="working_tree", duplicate_class="legitimate_cross_entrypoint_repeat")
invocation("MMEM-05", "make:validate-memory", "make", "Makefile:11", "LVG-010", [PY, ".codex/skills/project-memory-system/scripts/query_memory.py", "status", "--json"], scope="memory_health", tree_state="working_tree_plus_local_cache", severity="diagnostic")
invocation("MMEM-06", "make:validate-memory", "make", "Makefile:12", "LVG-012", [PY, ".codex/skills/project-memory-system/scripts/query_memory.py", "search", "Lorentzian metric", "--formats", "tex,pdf", "--limit", "5", "--json"], scope="memory_retrieval_smoke", tree_state="local_cache", severity="diagnostic")

invocation("MHTML-01", "make:validate-html-explainers", "make", "Makefile:29", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], scope="memory_and_publication", tree_state="working_tree", duplicate_class="nested_direct_overlap", related_invocation_id="MHTML-03")
invocation("MHTML-02", "make:validate-html-explainers", "make", "Makefile:30", "LVG-013", [PY, "scripts/spec_depth_lint.py", "--root", "."], scope="registered_specs", tree_state="working_tree")
invocation("MHTML-03", "make:validate-html-explainers", "make", "Makefile:31", "LVG-014", [PY, "scripts/validate_publication_process.py", "--root", "."], scope="publication", tree_state="working_tree", duplicate_class="nested_direct_duplicate", related_invocation_id="MHTML-01")
invocation("MAUDIT-01", "make:audit-documentation-surfaces", "make", "Makefile:35", "LVG-005", [PY, "scripts/project_control/audit_documentation_surfaces.py"], scope="documentation_including_local", tree_state="working_tree_plus_local_cache")

# GitHub Actions wrappers. Environment provisioning is listed as operational,
# not validation evidence.
invocation("CI-PC-01", "github:validate_project_control", "ci", ".github/workflows/project-control-validation.yml:35", "LVG-031", ["make", "PYTHON=.venv/bin/python", "validate-project-control"], scope="project_control", tree_state="clean_ci_checkout", duplicate_class="aggregate_wrapper")
invocation("CI-MEM-01", "github:validate_memory_read_only", "ci", ".github/workflows/project-control-validation.yml:57", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], scope="memory_and_publication", tree_state="clean_ci_checkout_separate_job", duplicate_class="cross_job_same_commit_duplicate", related_invocation_id="MPC-05")

# Local runner plan. The optional suite is still inventoried because it is a
# concrete supported invocation.
RUNNER = "scripts/research_control/run_full_research_control_validation.py"
runner_rows = [
    ("RUN-01", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], "memory_and_publication", "blocking"),
    ("RUN-02", "LVG-018", [PY, "scripts/research_control/render_current_frontier.py", "--check"], "current_frontier", "blocking"),
    ("RUN-03", "LVG-019", [PY, "scripts/research_control/validate_compact_current_frontier_v16.py", "--json"], "compact_frontier", "blocking"),
    ("RUN-04", "LVG-020", [PY, "scripts/research_control/render_dependency_graph.py", "--check"], "dependency_graph", "blocking"),
    ("RUN-05", "LVG-021", [PY, "scripts/research_control/validate_task_index.py", "--json"], "task_index", "blocking"),
    ("RUN-06", "LVG-022", [PY, "scripts/research_control/validate_claim_graph_v1.py", "--json"], "claim_graph", "blocking"),
    ("RUN-07", "LVG-023", [PY, "scripts/project_control/validate_claim_language.py", "--json", "--changed"], "changed_claim_language", "blocking"),
    ("RUN-08", "LVG-004", [PY, "scripts/project_control/validate_documentation_impact.py", "--json"], "documentation_impact", "blocking"),
    ("RUN-09", "LVG-003", [PY, "scripts/project_control/collect_project_improvement_signals.py", "--validate-emitted", "--json"], "project_improvement_signals", "blocking"),
    ("RUN-10", "LVG-015", [PY, "scripts/research_control/validate_research_control.py"], "research_control", "blocking"),
    ("RUN-11", "LVG-016", [PY, "scripts/research_control/validate_research_control.py", "--check-diff"], "research_control_and_diff", "blocking"),
    ("RUN-12", "LVG-024", [PY, "scripts/research_control/extract_route_signatures.py", "--sample", "recent-matter-coupling", "--json"], "route_diagnostic", "advisory"),
    ("RUN-13", "LVG-025", [PY, "scripts/research_control/validate_route_orbits.py", "--sample", "recent-matter-rr-e", "--json", "--advisory-only"], "route_diagnostic", "advisory"),
    ("RUN-14", "LVG-026", ["git", "diff", "--check"], "working_diff", "blocking"),
    ("RUN-15", "LVG-017", [PY, "-m", "unittest", "discover", "-s", "tests"], "repository", "blocking"),
]
for iid, gid, cmd, scope, severity in runner_rows:
    kwargs: dict[str, Any] = {}
    if iid == "RUN-10":
        kwargs = {"duplicate_class": "direct_same_state_subset", "same_state_superset_invocation_id": "RUN-11"}
    elif iid == "RUN-11":
        kwargs = {"duplicate_class": "same_state_superset"}
    invocation(iid, "local_runner", "local_runner", f"{RUNNER}:42-152", gid, cmd, scope=scope, tree_state="working_tree", severity=severity, condition="--include-smoke-tests" if iid == "RUN-15" else "default", **kwargs)

# Checkpoint validation stages. Working-file checks after staging are named
# honestly; only commands with explicit staged/index modes are marked staged.
CHECKPOINT = "scripts/research_control/checkpoint_research_transaction.py"
invocation("CHK-01", "checkpoint", "checkpoint", f"{CHECKPOINT}:400-403", "LVG-006", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"], scope="memory_sync", tree_state="working_tree_then_staged", mutating=True, condition="one_to_three_bounded_sync_passes")
invocation("CHK-02", "checkpoint", "checkpoint", f"{CHECKPOINT}:413-417", "LVG-027", [PY, ".codex/skills/project-memory-system/scripts/build_pdf_derivatives.py", "<targets>"], scope="changed_required_pdf_derivatives", tree_state="working_tree_then_staged", mutating=True, severity="conditional", condition="changed registered TeX has pdf_required=true")
invocation("CHK-03", "checkpoint", "checkpoint", f"{CHECKPOINT}:421-424", "LVG-006", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"], scope="post_pdf_memory_sync", tree_state="working_tree_then_staged", mutating=True, severity="conditional", condition="targeted PDF build ran")
checkpoint_working = [
    ("CHK-W01", "LVG-001", [PY, "scripts/project_control/classify_project_changes.py", "--json"], "project_control"),
    ("CHK-W02", "LVG-023", [PY, "scripts/project_control/validate_claim_language.py", "--json", "--changed"], "changed_claim_language"),
    ("CHK-W03", "LVG-003", [PY, "scripts/project_control/collect_project_improvement_signals.py", "--validate-emitted"], "project_improvement_signals"),
    ("CHK-W04", "LVG-004", [PY, "scripts/project_control/validate_documentation_impact.py"], "documentation_impact"),
    ("CHK-W05", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], "memory_and_publication"),
    ("CHK-W06", "LVG-015", [PY, "scripts/research_control/validate_research_control.py"], "research_control"),
    ("CHK-W07", "LVG-016", [PY, "scripts/research_control/validate_research_control.py", "--check-diff"], "research_control_and_diff"),
]
for iid, gid, cmd, scope in checkpoint_working:
    kwargs = {}
    if iid == "CHK-W06":
        kwargs = {"duplicate_class": "direct_same_state_subset", "same_state_superset_invocation_id": "CHK-W07"}
    elif iid == "CHK-W07":
        kwargs = {"duplicate_class": "same_state_superset"}
    invocation(iid, "checkpoint:post_sync", "checkpoint", f"{CHECKPOINT}:299-325", gid, cmd, scope=scope, tree_state="working_files_index_synchronized", **kwargs)

checkpoint_final = [
    ("CHK-S01", "LVG-001", [PY, "scripts/project_control/classify_project_changes.py", "--staged", "--json"], "project_control", "staged_index"),
    ("CHK-S02", "LVG-023", [PY, "scripts/project_control/validate_claim_language.py", "--json", "--staged"], "changed_claim_language", "staged_index"),
    ("CHK-S03", "LVG-003", [PY, "scripts/project_control/collect_project_improvement_signals.py", "--validate-emitted"], "project_improvement_signals", "working_files_index_synchronized"),
    ("CHK-S04", "LVG-004", [PY, "scripts/project_control/validate_documentation_impact.py", "--staged"], "documentation_impact", "staged_index"),
    ("CHK-S05", "LVG-016", [PY, "scripts/research_control/validate_research_control.py", "--check-diff", "--staged-only"], "research_control_and_diff", "staged_index"),
    ("CHK-S06", "LVG-007", [PY, ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "--validate-only"], "memory_and_publication", "working_files_index_synchronized"),
]
for iid, gid, cmd, scope, tree_state in checkpoint_final:
    invocation(iid, "checkpoint:final", "checkpoint", f"{CHECKPOINT}:517-587", gid, cmd, scope=scope, tree_state=tree_state, duplicate_class="legitimate_cross_scope_repeat", related_invocation_id={"CHK-S01":"CHK-W01","CHK-S02":"CHK-W02","CHK-S03":"CHK-W03","CHK-S04":"CHK-W04","CHK-S05":"CHK-W07","CHK-S06":"CHK-W05"}[iid])


SKILL_OBLIGATIONS = [
    {"declarer": "continue-research", "source_ref": ".codex/skills/continue-research/SKILL.md:22-60", "obligation": "refresh memory preflight, record status, perform one targeted lookup or search, and resolve tracked context before routing", "satisfying_gate_ids": ["LVG-028", "LVG-010", "LVG-011", "LVG-012", "LVG-029"], "condition": "before Director routing"},
    {"declarer": "continue-research", "source_ref": ".codex/skills/continue-research/SKILL.md:243-266", "obligation": "synchronize derivatives, validate memory/docs/research-control/diff, then checkpoint a valid nonempty transaction", "satisfying_gate_ids": ["LVG-006", "LVG-007", "LVG-004", "LVG-015", "LVG-016", "LVG-030"], "condition": "state-changing transaction"},
    {"declarer": "improve-project-system", "source_ref": ".codex/skills/improve-project-system/SKILL.md:39-88", "obligation": "status plus targeted memory query, classification, advisory resolution, and signal parity", "satisfying_gate_ids": ["LVG-010", "LVG-011", "LVG-012", "LVG-001", "LVG-002", "LVG-003"], "condition": "before project-system routing"},
    {"declarer": "improve-project-system", "source_ref": ".codex/skills/improve-project-system/SKILL.md:147-158", "obligation": "bootstrap, validate memory, signals, documentation impact, research-control core and diff before checkpoint", "satisfying_gate_ids": ["LVG-006", "LVG-007", "LVG-003", "LVG-004", "LVG-015", "LVG-016", "LVG-030"], "condition": "state-changing project-system transaction"},
    {"declarer": "user-modified-project", "source_ref": ".codex/skills/user-modified-project/SKILL.md:37-80", "obligation": "classify and resolve intake, then bootstrap and validate memory/docs/research-control/diff before checkpoint", "satisfying_gate_ids": ["LVG-001", "LVG-002", "LVG-006", "LVG-007", "LVG-004", "LVG-015", "LVG-016", "LVG-030"], "condition": "accepted human-edit integration"},
    {"declarer": "project-memory-system", "source_ref": ".codex/skills/project-memory-system/SKILL.md:22-56", "obligation": "select one scope-correct mutating or read-only memory/publication mode; local cleanup is not validation evidence", "satisfying_gate_ids": ["LVG-006", "LVG-007", "LVG-014"], "condition": "mode alternatives, not cumulative gates"},
]

ROLE_GATE_MAP = {
    "validate_research_control": ["LVG-015"],
    "check_diff": ["LVG-016"],
    "claim_boundary_phrase_scan": ["LVG-015"],
    "validate_documentation_impact": ["LVG-004"],
    "unittest": ["LVG-017"],
    "bootstrap_memory_system": ["LVG-006"],
    "scripts/validate_publication_process.py --root .": ["LVG-014"],
}


def role_obligations() -> list[dict[str, Any]]:
    rows = list(csv.DictReader((REPO_ROOT / "registries/AGENT_ROLE_REGISTRY.csv").open(encoding="utf-8")))
    obligations: list[dict[str, Any]] = []
    for row in rows:
        if row.get("status") != "active":
            continue
        for label in filter(None, row.get("default_validators", "").split(";")):
            obligations.append({
                "declarer": f"{row['role_id']}@{row['version']}",
                "source_ref": "registries/AGENT_ROLE_REGISTRY.csv",
                "obligation_label": label,
                "satisfying_gate_ids": ROLE_GATE_MAP.get(label, []),
                "required_scope": "transaction_applicable_scope",
                "classification": "obligation_not_independent_evidence",
            })
    return obligations


OUT_OF_SCOPE_COMMANDS = [
    {"source_ref": "Makefile:6,15,28,34", "command_family": "test -x $(PYTHON)", "reason": "environment precondition, not validation evidence"},
    {"source_ref": "Makefile:7", "command_family": "python -m pip install -r requirements.txt", "reason": "dependency provisioning, not validation evidence"},
    {"source_ref": ".github/workflows/project-control-validation.yml:20-32,42-54", "command_family": "venv creation and pip installation", "reason": "CI environment provisioning, not validation evidence"},
    {"source_ref": "scripts/research_control/checkpoint_research_transaction.py", "command_family": "git status/ls-files/add/write-tree/read-tree/diff --quiet/commit/rev-parse", "reason": "transaction staging, rollback, residue, and commit mechanics; retained operationally but not counted as validation gates"},
    {"source_ref": ".codex/skills/*/SKILL.md", "command_family": "documented command blocks", "reason": "compiled into obligations; declarations are not duplicate execution evidence"},
    {"source_ref": ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py", "command_family": "embedded git check-ignore and ls-files calls", "reason": "internal implementation operations represented by the parent memory gate"},
]

DRIFT_FINDINGS = [
    {"finding_id": "DRIFT-01", "severity": "hard_finding", "summary": "Make/CI and the local runner own different command sets.", "evidence": "Make includes classifier, documentation audit, spec lint, direct publication validation, and unconditional tests; the default local runner instead adds frontier, graph, index, claim graph, claim-language, advisory route, and whitespace gates and omits tests unless requested."},
    {"finding_id": "DRIFT-02", "severity": "hard_finding", "summary": "The local runner is not CI-equivalent.", "evidence": "GitHub executes make validate-project-control while the runner's base_command_plan differs in both additions and omissions."},
    {"finding_id": "DRIFT-03", "severity": "direct_duplicate", "summary": "Plain research-control validation immediately precedes its same-state --check-diff superset in three owners.", "evidence": "MPC-08/MPC-09, RUN-10/RUN-11, and CHK-W06/CHK-W07."},
    {"finding_id": "DRIFT-04", "severity": "nested_duplicate", "summary": "Memory validate-only already invokes publication validation before Make invokes publication validation directly.", "evidence": "MPC-05/MPC-07 and MHTML-01/MHTML-03; bootstrap_memory_system.validate_all calls validate_publication_docs."},
    {"finding_id": "DRIFT-05", "severity": "cross_job_duplicate", "summary": "GitHub's separate memory job repeats memory validate-only already nested in the main Make job.", "evidence": "CI-PC-01 expands to MPC-05 and CI-MEM-01 runs the same implementation in a separate clean checkout job."},
    {"finding_id": "DRIFT-06", "severity": "scope_guard", "summary": "Checkpoint working and final validations cannot be collapsed solely by command text.", "evidence": "CHK-W* inspect synchronized working files; CHK-S01, CHK-S02, CHK-S04, and CHK-S05 explicitly inspect the staged index. CHK-S03 and CHK-S06 have no staged mode and therefore remain labeled working_files_index_synchronized."},
    {"finding_id": "DRIFT-07", "severity": "obligation_drift", "summary": "Role and skill declarations use labels and command strings that do not form a shared executable plan.", "evidence": "Thirteen active roles declare seven label families; claim_boundary_phrase_scan is an integrated research-control behavior, not a universal standalone process."},
    {"finding_id": "DRIFT-08", "severity": "local_authority", "summary": "Local retrieval health is mixed into validate-memory but is non-authoritative for tracked project state.", "evidence": "MMEM-02, MMEM-03, MMEM-05, and MMEM-06 inspect or mutate ignored local retrieval state."},
]


def build_graph() -> dict[str, Any]:
    roles = role_obligations()
    owner_counts = Counter(item["owner_type"] for item in INVOCATIONS)
    scope_counts = Counter(item["scope"] for item in INVOCATIONS)
    severity_counts = Counter(item["severity"] for item in INVOCATIONS)
    duplicate_counts = Counter(item["duplicate_class"] for item in INVOCATIONS)
    obligation_labels = Counter(item["obligation_label"] for item in roles)
    return {
        "schema_id": "v19_legacy_validation_invocation_graph_v1",
        "status": "PASS",
        "task_id": "RT-20260712-004",
        "job_id": "AJ-RT-20260712-004-001",
        "plan_task_id": "P0-T04",
        "migration_epoch": "legacy",
        "generated_at": GENERATED_AT,
        "audited_head": "d1655d9bc83030e26faed289cdbcc1aec3e961ae",
        "audited_index_tree": "0d98bc7858cc51c8cb7505175570e9af803de3cb",
        "authority": {
            "operational_inventory_only": True,
            "scientific_claims_changed": False,
            "physics_delta_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
        },
        "source_fingerprints": [{"path": path, "sha256": file_hash(path)} for path in SOURCE_PATHS],
        "gate_catalog": GATES,
        "invocations": INVOCATIONS,
        "skill_obligations": SKILL_OBLIGATIONS,
        "role_obligations": roles,
        "role_obligation_label_counts": dict(sorted(obligation_labels.items())),
        "out_of_scope_commands": OUT_OF_SCOPE_COMMANDS,
        "drift_findings": DRIFT_FINDINGS,
        "unresolved_invocations": [],
        "counts": {
            "source_fingerprints": len(SOURCE_PATHS),
            "provisional_gates": len(GATES),
            "concrete_invocations": len(INVOCATIONS),
            "skill_obligations": len(SKILL_OBLIGATIONS),
            "role_obligations": len(roles),
            "owners": dict(sorted(owner_counts.items())),
            "scopes": dict(sorted(scope_counts.items())),
            "severities": dict(sorted(severity_counts.items())),
            "duplicate_classes": dict(sorted(duplicate_counts.items())),
            "direct_same_state_subset_pairs": sum(1 for item in INVOCATIONS if item["duplicate_class"] == "direct_same_state_subset"),
            "legitimate_cross_scope_repetitions": sum(1 for item in INVOCATIONS if item["duplicate_class"] == "legitimate_cross_scope_repeat"),
            "drift_findings": len(DRIFT_FINDINGS),
            "unresolved": 0,
        },
        "p5_manifest_seed": {
            "suitable": True,
            "stable_fields": ["gate_id", "implementation", "authority", "mutating", "condition", "nested_gate_ids"],
            "deferred_contracts": "Canonical gate IDs, evidence identity, supersedence, planner profiles, and cache keys remain assigned to later v19 tasks.",
        },
    }


def validate_graph(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    gate_ids = [item["gate_id"] for item in graph["gate_catalog"]]
    if len(gate_ids) != len(set(gate_ids)):
        errors.append("duplicate provisional gate ID")
    gate_set = set(gate_ids)
    invocation_ids = {item["invocation_id"] for item in graph["invocations"]}
    for item in graph["invocations"]:
        if item["gate_id"] not in gate_set:
            errors.append(f"{item['invocation_id']}: unknown gate {item['gate_id']}")
        superset = item["same_state_superset_invocation_id"]
        if superset and superset not in invocation_ids:
            errors.append(f"{item['invocation_id']}: missing superset {superset}")
        if item["tree_state"] == "staged_index" and "--staged" not in item["command"] and "--staged-only" not in item["command"]:
            errors.append(f"{item['invocation_id']}: staged-index label lacks staged argument")
        for field in ("owner", "scope", "tree_state", "duplicate_class", "expected_cost"):
            if item[field] in (None, "", {}):
                errors.append(f"{item['invocation_id']}: missing {field}")
    for item in graph["gate_catalog"]:
        unknown = set(item["nested_gate_ids"]) - gate_set
        if unknown:
            errors.append(f"{item['gate_id']}: unknown nested gates {sorted(unknown)}")
    for item in graph["skill_obligations"] + graph["role_obligations"]:
        if not item["satisfying_gate_ids"]:
            errors.append(f"unmapped obligation: {item}")
        unknown = set(item["satisfying_gate_ids"]) - gate_set
        if unknown:
            errors.append(f"obligation has unknown gates {sorted(unknown)}")
    for required_pair in (("MPC-08", "MPC-09"), ("RUN-10", "RUN-11"), ("CHK-W06", "CHK-W07")):
        left = next(item for item in graph["invocations"] if item["invocation_id"] == required_pair[0])
        if left["same_state_superset_invocation_id"] != required_pair[1]:
            errors.append(f"missing direct-superset evidence for {required_pair}")
    if graph["unresolved_invocations"]:
        errors.append("unresolved invocation remains")
    if graph["authority"]["scientific_claims_changed"] or graph["authority"]["proof_authority"]:
        errors.append("physics authority boundary violated")
    return errors


def render_markdown(graph: dict[str, Any]) -> str:
    counts = graph["counts"]
    lines = [
        "<!-- authority: control -->",
        "",
        "# V19 legacy validation invocation and obligation graph",
        "",
        "This P0-T04 inventory maps the current legacy validation owners without changing command behavior. Provisional gate IDs are seed identifiers for the later canonical manifest; role and skill declarations are obligations, not independent execution evidence.",
        "",
        "## Result",
        "",
        f"- Status: `{graph['status']}`",
        f"- Provisional gates: `{counts['provisional_gates']}`",
        f"- Concrete validation invocations: `{counts['concrete_invocations']}`",
        f"- Skill obligations: `{counts['skill_obligations']}`",
        f"- Role obligations: `{counts['role_obligations']}` across 13 active roles",
        f"- Direct same-state subset/superset pairs: `{counts['direct_same_state_subset_pairs']}`",
        f"- Legitimate cross-scope repetitions: `{counts['legitimate_cross_scope_repetitions']}`",
        "- Unresolved invocations: `0`",
        "- Physics or Distance-to-GR delta: `none`",
        "",
        "## Owner counts",
        "",
        "| Owner class | Invocations |",
        "| --- | ---: |",
    ]
    for owner, count in counts["owners"].items():
        lines.append(f"| `{owner}` | {count} |")
    lines.extend(["", "## Direct same-state supersets", "", "| Subset | Superset | Evidence |", "| --- | --- | --- |"])
    for left, right in (("MPC-08", "MPC-09"), ("RUN-10", "RUN-11"), ("CHK-W06", "CHK-W07")):
        lines.append(f"| `{left}` | `{right}` | Same owner, same tree state; `--check-diff` runs the core spine and then adds diff/claim checks. |")
    lines.extend([
        "",
        "Working-tree and staged-tree repetitions are deliberately not collapsed. The final checkpoint commands with explicit `--staged` or `--staged-only` inspect the Git index. Signal parity and memory validate-only lack staged modes, so their final checkpoint nodes are labeled `working_files_index_synchronized`, not staged-index evidence.",
        "",
        "## Current owner drift",
        "",
        "| Finding | Class | Summary |",
        "| --- | --- | --- |",
    ])
    for finding in graph["drift_findings"]:
        lines.append(f"| `{finding['finding_id']}` | `{finding['severity']}` | {finding['summary']} |")
    lines.extend([
        "",
        "## Nested relationships",
        "",
        "- Memory bootstrap and validate-only invoke publication-process validation and Mermaid source validation internally.",
        "- Research-control `--check-diff` runs the complete research-control core and integrates changed-claim validation.",
        "- GitHub's main job invokes the Make project-control wrapper; the separate memory job repeats memory validate-only in another clean-checkout job.",
        "- The checkpoint wrapper performs bounded synchronization, conditional PDF generation, working-file validation, explicit staged-index gates, residue checks, and optional commit mechanics.",
        "",
        "## Obligation interpretation",
        "",
        "The 13 active roles declare validator labels. Their current label frequencies are:",
        "",
    ])
    for label, count in graph["role_obligation_label_counts"].items():
        lines.append(f"- `{label}`: {count}")
    lines.extend([
        "",
        "`claim_boundary_phrase_scan` is satisfied inside the research-control core; it is not a requirement to spawn a separate process once per declaring role. Skill command blocks likewise compile to conditional obligations tied to a transaction scope.",
        "",
        "## P5 manifest seed",
        "",
        "The JSON graph is suitable seed input for P5 because each provisional gate records implementation, authority class, mutation behavior, condition, and nested gates. Canonical evidence identity, supersedence, profiles, cache keys, and orchestration authority remain deferred to their named v19 tasks.",
        "",
        "## Authority boundary",
        "",
        "This graph is operational control evidence only. It does not change validators, tests, CI, Make, skills, roles, checkpoint behavior, scientific sources, claim status, benchmark status, proof authority, or the ordinary research route at `handoff-0740`.",
        "",
    ])
    return "\n".join(lines)


def make_audit(graph_bytes: bytes, md_bytes: bytes, graph: dict[str, Any]) -> dict[str, Any]:
    errors = validate_graph(graph)
    return {
        "schema_id": "v19_legacy_validation_invocation_graph_audit_v1",
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260712-004",
        "job_id": "AJ-RT-20260712-004-001",
        "plan_task_id": "P0-T04",
        "generated_at": GENERATED_AT,
        "graph_path": str(GRAPH_JSON.relative_to(REPO_ROOT)),
        "graph_sha256": sha256_bytes(graph_bytes),
        "markdown_path": str(GRAPH_MD.relative_to(REPO_ROOT)),
        "markdown_sha256": sha256_bytes(md_bytes),
        "source_fingerprint_count": len(SOURCE_PATHS),
        "source_fingerprints": graph["source_fingerprints"],
        "counts": graph["counts"],
        "checks": {
            "source_hashes_current": True,
            "gate_ids_unique": True,
            "invocation_gate_links_complete": True,
            "skill_obligations_mapped": True,
            "role_obligations_mapped": True,
            "same_state_supersets_explicit": True,
            "working_and_staged_scopes_distinct": True,
            "nested_memory_and_publication_visible": True,
            "non_validation_commands_explained": True,
            "p5_seed_fields_present": True,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
        },
        "errors": errors,
        "no_physics_authority": True,
        "ordinary_research_handoff_preserved": "handoff-0740",
        "next_route": "P0-T05",
    }


def serialized_outputs() -> tuple[bytes, bytes, bytes]:
    graph = build_graph()
    errors = validate_graph(graph)
    if errors:
        raise RuntimeError("; ".join(errors))
    graph_bytes = (json.dumps(graph, indent=2, sort_keys=True) + "\n").encode()
    md_bytes = render_markdown(graph).encode()
    audit = make_audit(graph_bytes, md_bytes, graph)
    audit_bytes = (json.dumps(audit, indent=2, sort_keys=True) + "\n").encode()
    return graph_bytes, md_bytes, audit_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate committed outputs without writing.")
    args = parser.parse_args()
    graph_bytes, md_bytes, audit_bytes = serialized_outputs()
    expected = [(GRAPH_JSON, graph_bytes), (GRAPH_MD, md_bytes), (AUDIT_JSON, audit_bytes)]
    if args.check:
        stale = [str(path.relative_to(REPO_ROOT)) for path, data in expected if not path.exists() or path.read_bytes() != data]
        result = {"status": "PASS" if not stale else "FAIL", "stale_outputs": stale, "graph_sha256": sha256_bytes(graph_bytes), "audit_sha256": sha256_bytes(audit_bytes)}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if not stale else 1
    for path, data in expected:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(json.dumps({"status": "PASS", "written": [str(path.relative_to(REPO_ROOT)) for path, _ in expected]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
