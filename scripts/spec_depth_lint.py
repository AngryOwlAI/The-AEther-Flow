#!/usr/bin/env python3
"""Depth lint for Æther-Flow HTML explainer specs and generated pages.

This is intentionally advisory. It catches a specific failure mode observed in
the current explainer pages: generated content blocks that contain renderer
instructions such as "Explain ..." rather than finished human documentation.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from dataclasses import dataclass

PLACEHOLDER_START = re.compile(
    r"^\s*(Explain|Show|Point readers to|List|Provide|Preserve)\b"
    r"|^\s*State\s+(that|the|whether|why|how)\b",
    re.IGNORECASE,
)
INSTRUCTION_START = re.compile(
    r"^\s*(Explain|Show|Point readers to|List|Provide|Preserve)\b"
    r"|^\s*State\s+(that|the|whether|why|how)\b",
    re.IGNORECASE,
)
FRONTMATTER_RE = re.compile(r"\A---\n(?P<frontmatter>.*?)\n---\n", re.DOTALL)
TEACHING_REQUIRED_BLOCKS = {
    "plain_language_model",
    "glossary",
    "guided_walkthrough",
    "common_questions",
    "examples_and_non_examples",
    "misconception_repairs",
    "check_your_understanding",
}

@dataclass
class Block:
    block_id: str
    text: str
    source: str

class ContentBlockParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str | None] = []
        self.blocks: list[Block] = []
        self.current_id: str | None = None
        self.current_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        block_id = attrs_dict.get("data-content-block")
        self.stack.append(block_id)
        if block_id:
            if self.current_id:
                self._flush()
            self.current_id = block_id
            self.current_parts = []

    def handle_endtag(self, tag):
        if self.stack:
            block_id = self.stack.pop()
            if block_id and self.current_id == block_id:
                self._flush()

    def handle_data(self, data):
        if self.current_id:
            self.current_parts.append(data)

    def _flush(self):
        text = re.sub(r"\s+", " ", " ".join(self.current_parts)).strip()
        self.blocks.append(Block(self.current_id or "", text, "html"))
        self.current_id = None
        self.current_parts = []

def lint_html(path: Path) -> list[str]:
    parser = ContentBlockParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    warnings: list[str] = []
    for block in parser.blocks:
        if block.block_id == "subject_summary":
            continue
        words = re.findall(r"\w+", block.text)
        # Ignore large atlas navigation link groups.
        if block.block_id == "atlas_navigation":
            continue
        if PLACEHOLDER_START.search(block.text):
            warnings.append(
                f"{path}:{block.block_id}: content appears to be an instruction, not documentation: {block.text[:120]!r}"
            )
        elif len(words) < 80:
            warnings.append(
                f"{path}:{block.block_id}: shallow content block ({len(words)} words); target at least 120-250 words or a structured matrix"
            )
    return warnings

def lint_spec(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    warnings: list[str] = []
    teaching_enabled = spec_teaching_enabled(text)
    match = re.search(r"(?ms)^## Required Content Blocks\s*(.*?)(?:^## |\Z)", text)
    if not match:
        return warnings
    for line_no, line in enumerate(match.group(1).splitlines(), start=text[:match.start(1)].count("\n") + 1):
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        _prefix, _sep, description = stripped.partition(":")
        if INSTRUCTION_START.search(description.strip()) and len(stripped.split()) < 35:
            warnings.append(
                f"{path}:{line_no}: required content block is too directive; include renderable documentation detail: {stripped}"
            )
        if teaching_enabled and _prefix.strip() != "- subject_summary":
            description_text = description.strip().lower()
            if "plain-language" not in description_text:
                warnings.append(
                    f"{path}:{line_no}: teaching-enabled content block should name its plain-language opening: {stripped}"
                )
            if "`" not in description:
                warnings.append(
                    f"{path}:{line_no}: teaching-enabled content block should name source paths: {stripped}"
                )
    if teaching_enabled:
        missing_blocks = sorted(
            block for block in TEACHING_REQUIRED_BLOCKS if f'"{block}"' not in text and f"- {block}" not in text
        )
        if missing_blocks:
            warnings.append(
                f"{path}: teaching-enabled spec missing teaching block(s): {', '.join(missing_blocks)}"
            )
    return warnings

def spec_teaching_enabled(text: str) -> bool:
    match = FRONTMATTER_RE.search(text)
    if not match:
        return False
    frontmatter = match.group("frontmatter")
    return bool(re.search(r"(?ms)^teaching_loop:\s*\n(?:  .+\n)*?  enabled:\s*true\s*$", frontmatter))

def lint_github_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    warnings: list[str] = []
    if "## Common questions" not in text:
        warnings.append(f"{path}: teaching-enabled GitHub-facing Markdown lacks a Common questions section")
    if "## Common misunderstandings" not in text:
        warnings.append(f"{path}: teaching-enabled GitHub-facing Markdown lacks misconception repair")
    return warnings

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    warnings: list[str] = []
    for html in sorted((args.root / "html").glob("*-explainer.html")):
        warnings.extend(lint_html(html))
    for spec in sorted((args.root / "markdown" / "html-explainer-specs").glob("*-explainer.md")):
        warnings.extend(lint_spec(spec))
        spec_text = spec.read_text(encoding="utf-8", errors="replace")
        if spec_teaching_enabled(spec_text):
            github_page = args.root / "github-facing" / spec.name
            if github_page.exists():
                warnings.extend(lint_github_markdown(github_page))

    if warnings:
        print("\n".join(warnings))
        print(f"\nDepth lint found {len(warnings)} warning(s).")
        return 2

    print("Depth lint PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
