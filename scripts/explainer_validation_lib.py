#!/usr/bin/env python3
"""Shared helpers for Documentation Curator atlas validators."""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
STRICT_YAML_DIR = REPO_ROOT / "scripts" / "research_control"
if str(STRICT_YAML_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_YAML_DIR))

from strict_yaml import StrictYamlError, load_frontmatter  # noqa: E402


READER_BLOCKS = [
    "what_this_does",
    "why_aether_needs_it",
    "system_map",
    "how_it_works",
    "objects_and_authority",
    "example",
    "non_example",
    "common_confusions",
    "what_this_does_not_authorize",
    "source_map",
    "next_reading_path",
]

READER_BLOCK_HEADINGS = {
    "what_this_does": "What This Does",
    "why_aether_needs_it": "Why AEther Needs It",
    "system_map": "System Map",
    "workflow_map": "System Map",
    "how_it_works": "How It Works",
    "objects_and_authority": "Objects And Authority",
    "example": "Example",
    "non_example": "Non-Example",
    "common_confusions": "Common Confusions",
    "what_this_does_not_authorize": "What This Does Not Authorize",
    "source_map": "Source Map",
    "next_reading_path": "Next Reading Path",
}

MERMAID_ID_RE = re.compile(r"<!--\s*mermaid-diagram-id:\s*([^>]+?)\s*-->")
HTML_DATA_ATTR_RE = r'\b{attr}\s*=\s*["\']([^"\']+)["\']'
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCED_CODE_RE = re.compile(r"(?ms)^```.*?^```\s*")
CODE_SPAN_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def count(self, key: str, amount: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + amount

    @property
    def ok(self) -> bool:
        return not self.errors

    def print(self, pass_message: str) -> None:
        if self.ok:
            print(pass_message)
        else:
            for error in self.errors:
                print(f"ERROR: {error}")
        for warning in self.warnings:
            print(f"WARNING: {warning}")
        for key, value in sorted(self.counts.items()):
            print(f"- {key}: {value}")


def repo_path(root: Path, path_text: str) -> Path:
    return root / path_text


def read_csv(root: Path, relative_path: str) -> list[dict[str, str]]:
    path = root / relative_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_spec(path: Path) -> tuple[dict[str, object], str]:
    try:
        return load_frontmatter(path)
    except StrictYamlError as exc:
        raise ValueError(str(exc)) from exc


def list_value(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def bool_value(value: object) -> bool:
    return value is True or str(value).strip().lower() == "true"


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def topic_rows(root: Path) -> list[dict[str, str]]:
    return read_csv(root, "registries/EXPLAINER_TOPIC_REGISTRY.csv")


def spec_frontmatter_for(root: Path, path_text: str) -> tuple[dict[str, object], str]:
    return load_spec(root / path_text)


def declared_visual_ids(frontmatter: dict[str, object], body: str) -> set[str]:
    ids: set[str] = set(MERMAID_ID_RE.findall(body))
    primary_visuals = frontmatter.get("primary_visuals", [])
    if isinstance(primary_visuals, list):
        for item in primary_visuals:
            if isinstance(item, dict) and str(item.get("id", "")).strip():
                ids.add(str(item["id"]).strip())
            elif isinstance(item, str):
                ids.add(item.strip())
    mermaid = frontmatter.get("mermaid_diagrams", {})
    if isinstance(mermaid, dict):
        ids.update(list_value(mermaid.get("ids", [])))
    return {item for item in ids if item}


def declared_reader_blocks(frontmatter: dict[str, object]) -> set[str]:
    values = set(list_value(frontmatter.get("reader_blocks", [])))
    values.update(list_value(frontmatter.get("required_content_blocks", [])))
    return values


def markdown_headings(text: str) -> set[str]:
    return {match.group(2).strip() for match in HEADING_RE.finditer(text)}


def markdown_code_spans(text: str) -> set[str]:
    text_without_fences = FENCED_CODE_RE.sub("", text)
    return {match.group(1).strip() for match in CODE_SPAN_RE.finditer(text_without_fences)}


def markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def html_data_values(attr: str, html_text: str) -> set[str]:
    pattern = re.compile(HTML_DATA_ATTR_RE.format(attr=re.escape(attr)), re.IGNORECASE)
    return {match.group(1).strip() for match in pattern.finditer(html_text)}


def html_has_diagram_id(html_text: str, diagram_id: str) -> bool:
    return (
        f'data-mermaid-diagram-id="{diagram_id}"' in html_text
        or f"data-diagram-id=\"{diagram_id}\"" in html_text
        or f"id=\"{diagram_id}\"" in html_text
    )


def html_has_block(html_text: str, block_id: str) -> bool:
    return f'data-content-block="{block_id}"' in html_text


def reader_heading_for(block_id: str) -> str:
    return READER_BLOCK_HEADINGS.get(block_id, block_id.replace("_", " ").title())


def iter_required_topics(rows: Iterable[dict[str, str]]) -> Iterable[dict[str, str]]:
    for row in rows:
        if row.get("required", "").strip().lower() == "true":
            yield row
