#!/usr/bin/env python3
"""Classify Git changes for project-system and documentation impact."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from project_signal_types import signal_type_names  # noqa: E402
from scripts.validation.models import (  # noqa: E402
    ValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (  # noqa: E402
    DEFAULT_RECEIPT_ROOT,
    add_reporting_arguments,
    emit_report,
    options_from_namespace,
)
from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402

IGNORED_PREFIXES = (".local/", ".venv/", "__pycache__/")
GENERATED_REGISTRY_NAMES = {
    "FILE_OBJECT_REGISTRY.csv",
    "WIKI_ARTIFACT_REGISTRY.csv",
    "OBSIDIAN_VAULT_REGISTRY.csv",
    "CONTENT_SEMANTIC_REGISTRY.csv",
    "OBJECT_RELATIONSHIP_REGISTRY.csv",
}
GENERATED_REGISTRY_PREFIXES = (
    "registries/FILE_OBJECT_REGISTRY.meta.json",
    "registries/WIKI_ARTIFACT_REGISTRY.meta.json",
    "registries/OBSIDIAN_VAULT_REGISTRY.meta.json",
    "registries/CONTENT_SEMANTIC_REGISTRY.meta.json",
    "registries/OBJECT_RELATIONSHIP_REGISTRY.meta.json",
)
SIGNAL_FIELDS = (
    "signal_id",
    "signal_type",
    "severity",
    "evidence",
    "evidence_path",
    "recommended_skill",
    "recommended_role",
    "notes",
)
DOCUMENTATION_ROLE = "documentation-curator"
CONTROL_ROLE = "project-control-maintainer"
VALIDATOR_ROLE = "validator-engineer"
MEMORY_ROLE = "memory-system-maintainer"
ROLE_PRIORITY = {
    DOCUMENTATION_ROLE: 10,
    CONTROL_ROLE: 60,
    VALIDATOR_ROLE: 70,
    MEMORY_ROLE: 80,
}
MIXED_MARKDOWN_PATHS = {
    "README.md",
    "AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
}
CONTROL_REGISTRY_PATHS = {
    "registries/AGENT_ROLE_REGISTRY.csv",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv",
    "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
}
DOCUMENTATION_REGISTRY_PATHS = {
    "registries/HTML_EXPLAINER_REGISTRY.csv",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
}
DEPENDENCY_GRAPH_REGISTRY_PATHS = {
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/RESEARCH_TASK_REGISTRY.csv",
    "registries/CLAIM_BOUNDARY_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
    "registries/ROLE_EXECUTION_REGISTRY.csv",
    "registries/TEX_SOURCE_REGISTRY.csv",
    "registries/MARKDOWN_SOURCE_REGISTRY.csv",
    "registries/FILE_OBJECT_REGISTRY.csv",
}
DEPENDENCY_GRAPH_IMPLEMENTATION_PATHS = {
    "scripts/research_control/dependency_graph_model.py",
    "scripts/research_control/render_dependency_graph.py",
}
DEPENDENCY_GRAPH_OUTPUT_PATHS = {
    "output/research_dependency_graph.json",
    "output/research_dependency_graph.dot",
    "wiki/indexes/research_dependency_graph.md",
}
AUTHORITY_MARKER_RE = re.compile(r"<!--\s*authority:\s*(explanatory|control)\s*-->")
HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
PATH_FAMILY_TAGS = (
    "control_state",
    "role_or_schema_contract",
    "validator_code",
    "memory_code",
    "registered_markdown",
    "registered_tex",
    "required_pdf",
    "publication_spec",
    "html",
    "mermaid",
    "dependency_graph_input",
    "task_index_input",
    "claim_graph_input",
    "traceability",
    "scientific_checker",
    "local_retrieval",
    "ci_orchestration",
    "unknown_governed_path",
)
SOURCE_REGISTRIES = (
    ("MARKDOWN_SOURCE_REGISTRY.csv", "markdown"),
    ("TEX_SOURCE_REGISTRY.csv", "tex"),
)


@dataclass
class Classification:
    changed_paths: set[str] = field(default_factory=set)
    ignored_paths: set[str] = field(default_factory=set)
    generated_only_paths: set[str] = field(default_factory=set)
    blocked_paths: set[str] = field(default_factory=set)
    reason_codes: set[str] = field(default_factory=set)
    required_documentation_surfaces: set[str] = field(default_factory=set)
    docs_impact_required: bool = False
    project_system_improvement_required: bool = False
    recommended_role: str = ""
    recommended_role_priority: int = 0
    path_family_tags: set[str] = field(default_factory=set)
    path_family_reasons: set[str] = field(default_factory=set)
    canonical_paths: set[str] = field(default_factory=set)
    generated_derivatives: set[str] = field(default_factory=set)
    affected_source_object_ids: set[str] = field(default_factory=set)
    path_family_details: list[dict[str, object]] = field(default_factory=list)
    recommended_validation_profile: str = ""

    def recommend(self, role: str) -> None:
        priority = ROLE_PRIORITY.get(role, 0)
        if priority > self.recommended_role_priority:
            self.recommended_role = role
            self.recommended_role_priority = priority

    def docs(self, *surfaces: str, role: str = DOCUMENTATION_ROLE) -> None:
        self.docs_impact_required = True
        self.required_documentation_surfaces.update(surface for surface in surfaces if surface)
        self.recommend(role)

    def improve(self, role: str = VALIDATOR_ROLE) -> None:
        self.project_system_improvement_required = True
        self.recommend(role)

    def as_dict(self) -> dict[str, object]:
        recommended_role = self.recommended_role
        if not recommended_role and self.docs_impact_required:
            recommended_role = DOCUMENTATION_ROLE
        elif not recommended_role and self.project_system_improvement_required:
            recommended_role = VALIDATOR_ROLE
        if self.docs_impact_required or self.project_system_improvement_required:
            documentation_impact_guidance = (
                "State-changing project-system work requires research_control/tasks/<task_id>/documentation_impact.yaml. "
                "Use docs_update_required: false only when no source documentation or registry documentation update is needed; "
                "the receipt must still list live changed_paths, exact classifier reason_codes, generated_derivatives, validators_run, and a no_update_rationale."
            )
        else:
            documentation_impact_guidance = (
                "No documentation-impact receipt is required for the current path set."
            )
        return {
            "docs_impact_required": self.docs_impact_required,
            "project_system_improvement_required": self.project_system_improvement_required,
            "reason_codes": sorted(self.reason_codes),
            "changed_paths": sorted(self.changed_paths),
            "ignored_paths": sorted(self.ignored_paths),
            "generated_only_paths": sorted(self.generated_only_paths),
            "blocked_paths": sorted(self.blocked_paths),
            "path_family_tags": sorted(self.path_family_tags),
            "path_family_reasons": sorted(self.path_family_reasons),
            "canonical_paths": sorted(self.canonical_paths),
            "generated_derivatives": sorted(self.generated_derivatives),
            "affected_source_object_ids": sorted(self.affected_source_object_ids),
            "path_family_details": sorted(
                self.path_family_details,
                key=lambda item: str(item.get("path", "")),
            ),
            "recommended_validation_profile": self.recommended_validation_profile,
            "recommended_skill": "improve-project-system"
            if self.docs_impact_required or self.project_system_improvement_required
            else "",
            "recommended_role": recommended_role,
            "required_documentation_surfaces": sorted(self.required_documentation_surfaces),
            "required_validators": [
                "bootstrap_memory_system",
                "validate_documentation_impact",
            ]
            if self.docs_impact_required or self.project_system_improvement_required
            else [],
            "documentation_impact_guidance": documentation_impact_guidance,
            "block_checkpoint_until_addressed": bool(
                self.docs_impact_required or self.blocked_paths
            ),
        }


def run_git(command: list[str]) -> list[str]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def run_git_text(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if result.returncode == 0 else ""


def changed_paths_from_name_status(command: list[str]) -> list[str]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or "git command failed")
    fields = result.stdout.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index].decode("ascii", errors="replace")
        index += 1
        path_count = 2 if status.startswith(("R", "C")) else 1
        if index + path_count > len(fields):
            raise RuntimeError("git name-status output was truncated")
        for raw_path in fields[index : index + path_count]:
            if raw_path:
                paths.append(raw_path.decode("utf-8", errors="surrogateescape"))
        index += path_count
    return paths


def changed_paths_from_git(
    *,
    staged: bool = False,
    base_ref: str = "HEAD",
    include_untracked: bool = True,
) -> list[str]:
    if staged:
        paths = changed_paths_from_name_status(
            ["git", "diff", "--cached", "--name-status", "-z", base_ref, "--"]
        )
    else:
        paths = changed_paths_from_name_status(
            ["git", "diff", "--name-status", "-z", base_ref, "--"]
        )
        paths.extend(
            changed_paths_from_name_status(
                ["git", "diff", "--cached", "--name-status", "-z", base_ref, "--"]
            )
        )
        if include_untracked:
            paths.extend(run_git(["git", "ls-files", "--others", "--exclude-standard"]))
    return sorted(set(paths))


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    return any(path == pattern or fnmatch.fnmatch(path, pattern) for pattern in patterns)


def is_ignored(path: str) -> bool:
    return path.startswith(IGNORED_PREFIXES) or "/__pycache__/" in path


def is_generated_registry(path: str) -> bool:
    if path.startswith(GENERATED_REGISTRY_PREFIXES):
        return True
    if not path.startswith("registries/"):
        return False
    name = path.removeprefix("registries/")
    return name in GENERATED_REGISTRY_NAMES


def is_generated_derivative(path: str) -> bool:
    return (
        path == "FOLDER_MAP.md"
        or path.startswith("wiki/")
        or path.startswith("html/")
        or path.startswith("ontology/pdfs/")
        or path.startswith("manuscripts/pdfs/")
    )


def split_registry_paths(value: object) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


@dataclass(frozen=True)
class RegisteredSource:
    object_id: str
    path: str
    source_format: str
    role: str
    generated_outputs: tuple[str, ...]
    contains_mermaid: bool = False
    pdf_required: bool = False
    pdf_path: str = ""


@dataclass
class RegistryIndex:
    sources_by_path: dict[str, list[RegisteredSource]] = field(default_factory=dict)
    sources_by_id: dict[str, RegisteredSource] = field(default_factory=dict)
    sources_by_derivative: dict[str, list[RegisteredSource]] = field(default_factory=dict)
    html_paths: set[str] = field(default_factory=set)

    def add_derivative(self, path: str, source: RegisteredSource) -> None:
        if not path:
            return
        rows = self.sources_by_derivative.setdefault(path, [])
        if source not in rows:
            rows.append(source)


def read_registry_rows(root: Path, name: str) -> list[dict[str, str]]:
    path = root / "registries" / name
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_registry_index(root: Path = REPO_ROOT) -> RegistryIndex:
    index = RegistryIndex()
    for registry_name, source_format in SOURCE_REGISTRIES:
        for row in read_registry_rows(root, registry_name):
            path = text_value(row.get("path"))
            object_id = text_value(row.get("object_id"))
            if not path or not object_id:
                continue
            source = RegisteredSource(
                object_id=object_id,
                path=path,
                source_format=source_format,
                role=text_value(row.get("role")),
                generated_outputs=tuple(split_registry_paths(row.get("generated_outputs"))),
                contains_mermaid=text_value(row.get("contains_mermaid")).lower() == "true",
                pdf_required=text_value(row.get("pdf_required")).lower() == "true",
                pdf_path=text_value(row.get("pdf_path")),
            )
            index.sources_by_path.setdefault(path, []).append(source)
            index.sources_by_id[object_id] = source
            for derivative in source.generated_outputs:
                index.add_derivative(derivative, source)
            if source.pdf_required and source.pdf_path:
                index.add_derivative(source.pdf_path, source)

    for row in read_registry_rows(root, "HTML_EXPLAINER_REGISTRY.csv"):
        html_path = text_value(row.get("path"))
        if html_path:
            index.html_paths.add(html_path)
        source_id = text_value(row.get("source_basis")) or text_value(row.get("generated_from"))
        source = index.sources_by_id.get(source_id)
        if not source:
            continue
        index.add_derivative(html_path, source)
        for derivative in split_registry_paths(row.get("generated_outputs")):
            index.add_derivative(derivative, source)
    return index


def is_control_state_path(path: str) -> bool:
    return (
        path == "research_control/program_state.yaml"
        or path.startswith("research_control/tasks/")
        or path.startswith("research_control/handoffs/")
        or path.startswith("research_control/project_improvement_handoffs/")
        or path in CONTROL_REGISTRY_PATHS
    )


def is_dependency_graph_input(path: str) -> bool:
    return (
        path == "research_control/program_state.yaml"
        or fnmatch.fnmatch(
            path,
            "research_control/tasks/*/jobs/completions/*.yaml",
        )
        or fnmatch.fnmatch(path, "research_control/handoffs/handoff-*.yaml")
        or path in DEPENDENCY_GRAPH_REGISTRY_PATHS
        or path in DEPENDENCY_GRAPH_IMPLEMENTATION_PATHS
        or path in DEPENDENCY_GRAPH_OUTPUT_PATHS
    )


def is_task_index_input(path: str) -> bool:
    return (
        path.startswith("research_control/tasks/")
        or path
        in {
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "registries/AGENT_JOB_REGISTRY.csv",
            "research_control/tasks/TASK_INDEX.csv",
            "research_control/tasks/TASK_INDEX.md",
        }
    )


def is_claim_graph_input(path: str) -> bool:
    return (
        path
        in {
            "registries/CLAIM_REGISTRY.csv",
            "registries/CLAIM_BOUNDARY_REGISTRY.csv",
            "registries/RELATIONSHIP_REGISTRY.csv",
            "output/claim_graph_v1.json",
            "output/claim_graph_v1.dot",
        }
        or Path(path).name in {"generate_claim_graph_v1.py", "validate_claim_graph_v1.py"}
    )


def classify_path_family(path: str, registry: RegistryIndex) -> dict[str, object]:
    tags: set[str] = set()
    reasons: set[str] = set()
    canonical_paths: set[str] = set()
    derivatives: set[str] = set()
    object_ids: set[str] = set()

    sources = list(registry.sources_by_path.get(path, []))
    for source in registry.sources_by_derivative.get(path, []):
        if source not in sources:
            sources.append(source)

    for source in sources:
        tag = "registered_markdown" if source.source_format == "markdown" else "registered_tex"
        tags.add(tag)
        reasons.add(f"registry:{source.source_format}:{source.object_id}")
        canonical_paths.add(source.path)
        object_ids.add(source.object_id)
        derivatives.update(source.generated_outputs)
        if source.contains_mermaid:
            tags.add("mermaid")
            reasons.add(f"registry:contains_mermaid:{source.object_id}")
        if source.role == "html_explainer_source_spec":
            tags.add("publication_spec")
            reasons.add(f"registry:publication_spec:{source.object_id}")
        if source.pdf_required:
            tags.add("required_pdf")
            reasons.add(f"registry:pdf_required:{source.object_id}")
            if source.pdf_path:
                derivatives.add(source.pdf_path)

    if is_ignored(path):
        tags.add("local_retrieval")
        reasons.add("path_rule:local_retrieval")
    elif not is_generated_derivative(path):
        canonical_paths.add(path)

    if path in registry.sources_by_derivative or is_generated_derivative(path):
        derivatives.add(path)
    if path in registry.html_paths or path.startswith("html/"):
        tags.add("html")
        reasons.add("path_rule:html")
    if path.startswith("markdown/html-explainer-specs/"):
        tags.add("publication_spec")
        reasons.add("path_rule:publication_spec")
    if is_control_state_path(path):
        tags.add("control_state")
        reasons.add("path_rule:control_state")
    if (
        path.startswith(".agents/roles/")
        or path.startswith(".agents/schemas/")
        or path_matches(path, [".codex/skills/*/SKILL.md"])
        or any(source.role in {"control_schema", "control_policy"} for source in sources)
    ):
        tags.add("role_or_schema_contract")
        reasons.add("path_rule:role_or_schema_contract")
    if (
        path.startswith("scripts/project_control/")
        or path.startswith("scripts/validation/")
        or (path.startswith("scripts/research_control/") and Path(path).name.startswith("validate"))
        or path.startswith("tests/")
    ):
        tags.add("validator_code")
        reasons.add("path_rule:validator_code")
    if (
        path.startswith(".codex/skills/project-memory-system/scripts/")
        or path.startswith("scripts/memory/")
        or Path(path).name in {"memory_operations.py", "memory_core.py", "local_retrieval.py"}
    ):
        tags.add("memory_code")
        reasons.add("path_rule:memory_code")
    if is_dependency_graph_input(path):
        tags.add("dependency_graph_input")
        reasons.add("path_rule:dependency_graph_input")
    if is_task_index_input(path):
        tags.add("task_index_input")
        reasons.add("path_rule:task_index_input")
    if is_claim_graph_input(path):
        tags.add("claim_graph_input")
        reasons.add("path_rule:claim_graph_input")
    if "traceability" in path or path == "registries/FORMALIZATION_TRACEABILITY_REGISTRY.csv":
        tags.add("traceability")
        reasons.add("path_rule:traceability")
    if (
        Path(path).name.endswith("_checker.py")
        or "scientific_payload" in Path(path).name
        or (
            path.startswith("scripts/research_control/support_formalization/")
            and "traceability" not in Path(path).name
        )
    ):
        tags.add("scientific_checker")
        reasons.add("path_rule:scientific_checker")
    if (
        path.startswith(".github/workflows/")
        or path == "Makefile"
        or path.startswith("scripts/validation/")
        or Path(path).name.startswith(("checkpoint_", "continue_", "run_full_"))
    ):
        tags.add("ci_orchestration")
        reasons.add("path_rule:ci_orchestration")

    return {
        "path": path,
        "tags": sorted(tags),
        "reasons": sorted(reasons),
        "canonical_paths": sorted(canonical_paths),
        "generated_derivatives": sorted(derivatives),
        "affected_source_object_ids": sorted(object_ids),
    }


def is_signal_emission_path(path: str) -> bool:
    return (
        fnmatch.fnmatch(path, "research_control/tasks/*/jobs/completions/*.yaml")
        or fnmatch.fnmatch(path, "research_control/handoffs/handoff-*.yaml")
    )


def text_value(value: object) -> str:
    return str(value or "").strip()


def changed_new_lines_from_diff(diff_text: str) -> set[int]:
    lines: set[int] = set()
    for raw_line in diff_text.splitlines():
        match = HUNK_RE.search(raw_line)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        if count > 0:
            lines.update(range(start, start + count))
    return lines


def changed_new_lines(path: str) -> set[int]:
    unstaged = run_git_text(["git", "diff", "--unified=0", "--", path])
    staged = run_git_text(["git", "diff", "--cached", "--unified=0", "--", path])
    return changed_new_lines_from_diff(unstaged) | changed_new_lines_from_diff(staged)


def authority_by_line(text: str) -> dict[int, str]:
    active = ""
    authorities: dict[int, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = AUTHORITY_MARKER_RE.search(line)
        if match:
            active = match.group(1)
        authorities[line_number] = active or "unmarked"
    return authorities


def markdown_authorities(path: str) -> set[str]:
    absolute = REPO_ROOT / path
    if not absolute.exists() or not absolute.is_file():
        return {"unmarked"}
    text = absolute.read_text(encoding="utf-8")
    line_authorities = authority_by_line(text)
    changed_lines = changed_new_lines(path)
    if changed_lines:
        return {
            line_authorities.get(line_number, "unmarked")
            for line_number in changed_lines
        }
    markers = set(AUTHORITY_MARKER_RE.findall(text))
    return markers or {"unmarked"}


def is_nonblank_signal(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    return any(text_value(value.get(field)) for field in SIGNAL_FIELDS)


def contains_project_signal(path: str) -> bool:
    if not is_signal_emission_path(path):
        return False
    absolute = REPO_ROOT / path
    if not absolute.exists() or not absolute.is_file():
        return False
    try:
        data = load_yaml(absolute)
    except StrictYamlError:
        return False
    signals = data.get("project_improvement_signals", [])
    if not isinstance(signals, list):
        return False
    known_types = signal_type_names(REPO_ROOT)
    for signal in signals:
        if not is_nonblank_signal(signal):
            continue
        signal_type = text_value(signal.get("signal_type")) if isinstance(signal, dict) else ""
        if not signal_type or signal_type in known_types:
            return True
    return False


def classify_canonical_path(path: str, result: Classification) -> None:
    if path.startswith(".agents/roles/"):
        result.reason_codes.add("role_contract_changed")
        result.docs("AGENTS.md", "README.md", "registries/AGENT_ROLE_REGISTRY.csv", role=CONTROL_ROLE)
        result.improve(CONTROL_ROLE)
    elif path.startswith(".agents/schemas/"):
        result.reason_codes.add("schema_contract_changed")
        result.docs("AGENTS.md", "README.md", role=CONTROL_ROLE)
        result.improve(CONTROL_ROLE)
    elif path_matches(path, [".codex/skills/*/SKILL.md"]):
        result.reason_codes.add("skill_contract_changed")
        result.docs("AGENTS.md", "README.md", role=CONTROL_ROLE)
        result.improve(CONTROL_ROLE)
    elif path.startswith(".codex/skills/project-memory-system/scripts/"):
        result.reason_codes.add("memory_tooling_changed")
        result.docs("README.md", ".codex/skills/project-memory-system/SKILL.md", role=MEMORY_ROLE)
        result.improve(MEMORY_ROLE)
    elif path.startswith("scripts/research_control/"):
        if "validate" in Path(path).name:
            result.reason_codes.add("validator_changed")
        elif "checkpoint" in Path(path).name:
            result.reason_codes.add("checkpoint_changed")
        elif "continue" in Path(path).name:
            result.reason_codes.add("continuation_script_changed")
        else:
            result.reason_codes.add("research_control_tooling_changed")
        result.docs(
            "README.md",
            "research_control/README.md",
            ".codex/skills/continue-research/SKILL.md",
            role=VALIDATOR_ROLE,
        )
        result.improve(VALIDATOR_ROLE)
    elif path.startswith("scripts/project_control/"):
        if "validate" in Path(path).name:
            result.reason_codes.add("validator_changed")
        else:
            result.reason_codes.add("project_control_tooling_changed")
        result.docs("README.md", ".codex/skills/improve-project-system/SKILL.md", role=VALIDATOR_ROLE)
        result.improve(VALIDATOR_ROLE)
    elif path.startswith("tests/"):
        result.reason_codes.add("test_changed")
        result.improve(VALIDATOR_ROLE)
    elif path.startswith("registries/") and path.endswith("REGISTRY.csv"):
        if path == "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv":
            result.reason_codes.add("project_improvement_signal_registry_changed")
            result.docs("README.md", ".codex/skills/improve-project-system/SKILL.md", role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
        elif path == "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv":
            result.reason_codes.add("project_improvement_signal_type_registry_changed")
            result.docs("README.md", ".codex/skills/improve-project-system/SKILL.md", role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
        elif path in DOCUMENTATION_REGISTRY_PATHS:
            result.reason_codes.add("documentation_registry_changed")
            result.docs("README.md", path)
        elif path in CONTROL_REGISTRY_PATHS:
            result.reason_codes.add("control_registry_changed")
            result.docs("README.md", "AGENTS.md", role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
        else:
            result.reason_codes.add("registry_changed")
            result.docs("README.md", "AGENTS.md", role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
    elif path in MIXED_MARKDOWN_PATHS:
        authorities = markdown_authorities(path)
        if "unmarked" in authorities:
            result.reason_codes.add("unmarked_mixed_markdown_changed")
            result.docs(path, role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
        elif "control" in authorities:
            result.reason_codes.add("control_markdown_changed")
            result.docs(path, role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
        else:
            result.reason_codes.add("documentation_surface_changed")
            result.docs(path)
    elif path.startswith("markdown/html-explainer-specs/"):
        result.reason_codes.add("html_source_spec_changed")
        result.docs("registries/HTML_EXPLAINER_REGISTRY.csv", "README.md")
    elif path.startswith("github-facing/") and path.endswith(".md"):
        result.reason_codes.add("github_facing_markdown_changed")
        result.docs(
            "registries/MARKDOWN_SOURCE_REGISTRY.csv",
        )
    elif path.startswith("markdown/"):
        result.reason_codes.add("markdown_source_changed")
        result.docs("registries/MARKDOWN_SOURCE_REGISTRY.csv")
    elif path.startswith("research_control/"):
        result.reason_codes.add("research_control_state_changed")
        if contains_project_signal(path):
            result.reason_codes.add("project_improvement_signal_recorded")
            result.docs("research_control/README.md", ".codex/skills/improve-project-system/SKILL.md", role=CONTROL_ROLE)
            result.improve(CONTROL_ROLE)
    elif path.startswith("ontology/tex/") or path.startswith("manuscripts/tex/"):
        result.reason_codes.add("physics_source_changed")
    elif path == "Makefile":
        result.reason_codes.add("validation_entrypoint_changed")
        result.docs("README.md", role=VALIDATOR_ROLE)
        result.improve(VALIDATOR_ROLE)


def classify_paths(paths: Iterable[str], *, registry_root: Path | None = None) -> dict[str, object]:
    result = Classification()
    canonical_changed = False
    generated_derivative_paths: set[str] = set()
    registry = load_registry_index(registry_root or REPO_ROOT)

    for path in sorted(set(paths)):
        if not path:
            continue
        family = classify_path_family(path, registry)
        result.path_family_details.append(family)
        result.path_family_tags.update(str(tag) for tag in family["tags"])
        result.path_family_reasons.update(str(reason) for reason in family["reasons"])
        result.canonical_paths.update(str(item) for item in family["canonical_paths"])
        result.generated_derivatives.update(str(item) for item in family["generated_derivatives"])
        result.affected_source_object_ids.update(
            str(item) for item in family["affected_source_object_ids"]
        )
        if not is_ignored(path) and not result.recommended_validation_profile:
            result.recommended_validation_profile = "affected"
        result.changed_paths.add(path)
        if is_ignored(path):
            result.ignored_paths.add(path)
            continue
        if is_generated_registry(path):
            result.generated_only_paths.add(path)
            result.reason_codes.add("generated_registry_changed")
            continue
        if is_generated_derivative(path):
            generated_derivative_paths.add(path)
            result.generated_only_paths.add(path)
            result.reason_codes.add("generated_derivative_changed")
            continue
        canonical_changed = True
        reason_codes_before = set(result.reason_codes)
        classify_canonical_path(path, result)
        if not family["tags"] and result.reason_codes == reason_codes_before:
            family["tags"] = ["unknown_governed_path"]
            family["reasons"] = ["fallback:unknown_governed_path"]
            result.path_family_tags.add("unknown_governed_path")
            result.path_family_reasons.add("fallback:unknown_governed_path")
            result.reason_codes.add("unknown_governed_path")
            result.improve(VALIDATOR_ROLE)
            result.recommended_validation_profile = "full"

    if generated_derivative_paths and not canonical_changed:
        result.reason_codes.add("direct_generated_derivative_edit")
        result.docs(
            "markdown/html-explainer-specs/",
            "registries/HTML_EXPLAINER_REGISTRY.csv",
            "registries/WIKI_ARTIFACT_REGISTRY.csv",
        )
        result.blocked_paths.update(generated_derivative_paths)

    return result.as_dict()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_reporting_arguments(parser)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the previous complete JSON payload.",
    )
    parser.add_argument("--staged", action="store_true", help="Classify staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base reference.")
    parser.add_argument("--no-untracked", action="store_true", help="Ignore untracked files.")
    parser.add_argument("--paths", nargs="*", help="Classify explicit paths instead of Git state.")
    args = parser.parse_args(argv)
    common_mode_selected = any(
        getattr(args, name)
        for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.json and common_mode_selected:
        parser.error("--json cannot be combined with a common reporting mode")
    return args


def _working_tree_digest(payload: dict[str, object]) -> str:
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    )
    results: dict[str, bytes] = {}
    for label, command in (
        ("head", ["git", "rev-parse", "HEAD"]),
        ("diff", ["git", "diff", "--no-ext-diff", "--binary", "HEAD", "--"]),
        ("untracked", ["git", "ls-files", "--others", "--exclude-standard", "-z"]),
    ):
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            return digest.hexdigest()
        results[label] = completed.stdout
        digest.update(label.encode("ascii") + b"\0" + completed.stdout)
    for raw_path in sorted(path for path in results["untracked"].split(b"\0") if path):
        path = REPO_ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        if path.is_file():
            digest.update(b"untracked-content\0" + raw_path + b"\0" + path.read_bytes())
    return digest.hexdigest()


def adapt_to_common_run(
    payload: dict[str, object],
    selected_paths: Iterable[str],
    *,
    error: str = "",
) -> ValidationRun:
    normalized_paths = sorted(set(selected_paths))
    identity_payload = {"payload": payload, "selected_paths": normalized_paths}
    digest = _working_tree_digest(identity_payload)
    findings = ()
    if error:
        finding_digest = hashlib.sha256(error.encode("utf-8")).hexdigest()[:12].upper()
        findings = (
            ValidationFinding(
                finding_id=f"CLASSIFY-CHANGES-ERROR-{finding_digest}",
                level="ERROR",
                code="change_classification_error",
                message=error,
            ),
        )
    status = "FAIL" if error else "PASS"
    exit_code = 1 if error else 0
    gate = ValidationGateResult(
        gate_id="classify_changes",
        status=status,
        severity="blocking",
        exit_code=exit_code,
        findings=findings,
    )
    return ValidationRun(
        run_id=f"CLASSIFY-CHANGES-{digest[:16].upper()}",
        tree_hash=f"working-sha256:{digest}",
        status=status,
        exit_code=exit_code,
        gate_results=(gate,),
        profile="shadow_planner",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths: list[str] = []
    error = ""
    try:
        paths = args.paths if args.paths is not None else changed_paths_from_git(
            staged=args.staged,
            base_ref=args.base_ref,
            include_untracked=not args.no_untracked,
        )
        payload = classify_paths(paths)
    except RuntimeError as exc:
        error = str(exc)
        payload = {"status": "error", "error": error}
    if args.json:
        print(json.dumps(payload, indent=2), file=sys.stderr if error else sys.stdout)
        return 1 if error else 0
    return emit_report(
        adapt_to_common_run(payload, paths, error=error),
        options=options_from_namespace(args),
        receipt_root=REPO_ROOT / DEFAULT_RECEIPT_ROOT,
        stream=sys.stderr if error else sys.stdout,
    )


if __name__ == "__main__":
    raise SystemExit(main())
