#!/usr/bin/env python3
"""Classify Git changes for project-system and documentation impact."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from project_signal_types import signal_type_names  # noqa: E402
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
AUTHORITY_MARKER_RE = re.compile(r"<!--\s*authority:\s*(explanatory|control)\s*-->")
HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


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
        return {
            "docs_impact_required": self.docs_impact_required,
            "project_system_improvement_required": self.project_system_improvement_required,
            "reason_codes": sorted(self.reason_codes),
            "changed_paths": sorted(self.changed_paths),
            "ignored_paths": sorted(self.ignored_paths),
            "generated_only_paths": sorted(self.generated_only_paths),
            "blocked_paths": sorted(self.blocked_paths),
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


def changed_paths_from_git(
    *,
    staged: bool = False,
    base_ref: str = "HEAD",
    include_untracked: bool = True,
) -> list[str]:
    if staged:
        paths = run_git(["git", "diff", "--cached", "--name-only", base_ref])
    else:
        paths = run_git(["git", "diff", "--name-only", base_ref])
        paths.extend(run_git(["git", "diff", "--cached", "--name-only", base_ref]))
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


def classify_paths(paths: Iterable[str]) -> dict[str, object]:
    result = Classification()
    canonical_changed = False
    generated_derivative_paths: set[str] = set()

    for path in sorted(set(paths)):
        if not path:
            continue
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
        classify_canonical_path(path, result)

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
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--staged", action="store_true", help="Classify staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base reference.")
    parser.add_argument("--no-untracked", action="store_true", help="Ignore untracked files.")
    parser.add_argument("--paths", nargs="*", help="Classify explicit paths instead of Git state.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        paths = args.paths if args.paths is not None else changed_paths_from_git(
            staged=args.staged,
            base_ref=args.base_ref,
            include_untracked=not args.no_untracked,
        )
        print(json.dumps(classify_paths(paths), indent=2))
    except RuntimeError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
