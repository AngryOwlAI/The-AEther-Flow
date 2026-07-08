#!/usr/bin/env python3
"""Validate P9-T03 public documentation status-card v2 calibration."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]

PUBLIC_DOCS = [
    "README.md",
    "github-facing/project-overview-explainer.md",
    "github-facing/proof-state-dashboard-explainer.md",
    "github-facing/source-authority-explainer.md",
    "github-facing/aether-flow-physics-program-explainer.md",
    "github-facing/aether-flow-ontology-explainer.md",
    "github-facing/gr-derivation-roadmap-explainer.md",
    "github-facing/claim-gates-explainer.md",
    "github-facing/negative-results-and-obstructions-explainer.md",
]

SOURCE_SPECS = [
    "markdown/html-explainer-specs/project-overview-explainer.md",
    "markdown/html-explainer-specs/proof-state-dashboard-explainer.spec.md",
    "markdown/html-explainer-specs/source-authority-explainer.md",
    "markdown/html-explainer-specs/aether-flow-physics-program-explainer.md",
    "markdown/html-explainer-specs/aether-flow-ontology-explainer.md",
    "markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md",
    "markdown/html-explainer-specs/claim-gates-explainer.md",
    "markdown/html-explainer-specs/negative-results-and-obstructions-explainer.md",
]

PUBLICATION_BRIEFS = [
    "markdown/publication-briefs/project-overview.publication-brief.md",
    "markdown/publication-briefs/proof-state-dashboard.publication-brief.md",
    "markdown/publication-briefs/source-authority.publication-brief.md",
    "markdown/publication-briefs/aether-flow-physics-program.publication-brief.md",
    "markdown/publication-briefs/aether-flow-ontology.publication-brief.md",
    "markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md",
    "markdown/publication-briefs/claim-gates.publication-brief.md",
    "markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md",
]

REQUIRED_PUBLIC_TERMS = [
    "Positive status",
    "Exact scope",
    "Blocked overread",
    "Next burden",
]

REQUIRED_V2_SOURCE_TERMS = [
    "research_control/design/status_card_v2_schema.md",
    "research_control/design/accepted_status_calibration_v2.yaml",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    re.compile(r"\bGR has been derived\b", re.IGNORECASE),
    re.compile(r"\bhas already derived GR\b", re.IGNORECASE),
    re.compile(r"\bEinstein equations (?:are|were|have been) derived\b", re.IGNORECASE),
    re.compile(r"\bbenchmark (?:is|was|has been) promoted\b", re.IGNORECASE),
    re.compile(r"\bGate Chair verdict (?:is|was|has been) issued\b", re.IGNORECASE),
    re.compile(r"\bcompleted derivation (?:is|was|has been) established\b", re.IGNORECASE),
]

BLOCKED_CONTEXT_MARKERS = (
    "unsafe summary",
    "unsafe claim",
    "forbidden",
    "blocked overread",
    "avoid broad language",
    "it cannot support",
    "forbidden claim",
    "does not",
    "cannot",
    "no ",
    "not ",
    "without",
)


@dataclass
class Report:
    status: str = "PASS"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_public_docs: list[str] = field(default_factory=list)
    checked_source_specs: list[str] = field(default_factory=list)
    checked_publication_briefs: list[str] = field(default_factory=list)
    html_outputs_changed: bool = True
    html_content_regenerated: bool = False
    html_metadata_synchronized_paths: list[str] = field(default_factory=lambda: [
        "html/project-overview-explainer.html",
        "html/proof-state-dashboard-explainer.html",
        "html/source-authority-explainer.html",
        "html/aether-flow-physics-program-explainer.html",
        "html/aether-flow-ontology-explainer.html",
        "html/gr-derivation-roadmap-explainer.html",
        "html/claim-gates-explainer.html",
        "html/negative-results-and-obstructions-explainer.html",
    ])
    html_regeneration_rationale: str = (
        "P9-T03 calibrates public Markdown, source specs, and publication briefs. "
        "Tracked HTML prose and layout were not regenerated. The affected HTML "
        "source-basis hash metadata was synchronized because the established "
        "explainer validation pipeline requires generated derivatives to point "
        "at the current registered source-spec hash."
    )

    def error(self, message: str) -> None:
        self.errors.append(message)
        self.status = "FAIL"

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path_text: str, report: Report) -> str:
    path = REPO_ROOT / path_text
    if not path.exists():
        report.error(f"missing required path: {path_text}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def has_blocked_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in BLOCKED_CONTEXT_MARKERS)


def validate_public_doc(path_text: str, report: Report) -> None:
    text = read_text(path_text, report)
    if not text:
        return
    report.checked_public_docs.append(path_text)
    for term in REQUIRED_PUBLIC_TERMS:
        if term not in text:
            report.error(f"{path_text}: missing public status-card field {term!r}")
    if "completed derivation" not in text.lower():
        report.warn(f"{path_text}: no explicit completed-derivation blocked phrase")
    lines = text.splitlines()
    for line_no, line in enumerate(lines, start=1):
        context_window = "\n".join(lines[max(0, line_no - 8) : min(len(lines), line_no + 2)])
        for pattern in FORBIDDEN_POSITIVE_CLAIMS:
            if pattern.search(line) and not has_blocked_context(context_window):
                report.error(
                    f"{path_text}:{line_no}: possible public overclaim outside blocked context: {line.strip()}"
                )


def validate_v2_source_binding(path_text: str, report: Report, *, kind: str) -> None:
    text = read_text(path_text, report)
    if not text:
        return
    if kind == "source_spec":
        report.checked_source_specs.append(path_text)
    else:
        report.checked_publication_briefs.append(path_text)
    for term in REQUIRED_V2_SOURCE_TERMS:
        if term not in text:
            report.error(f"{path_text}: missing v2 source binding {term}")


def validate(repo_root: Path) -> Report:
    global REPO_ROOT
    REPO_ROOT = repo_root
    report = Report()
    for path_text in PUBLIC_DOCS:
        validate_public_doc(path_text, report)
    for path_text in SOURCE_SPECS:
        validate_v2_source_binding(path_text, report, kind="source_spec")
    for path_text in PUBLICATION_BRIEFS:
        validate_v2_source_binding(path_text, report, kind="publication_brief")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--report-path", default="research_control/tasks/RT-20260708-034/artifacts/p9_t03_public_docs_status_cards_report.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate(Path(args.repo_root).resolve())
    payload = asdict(report)
    if args.write_report:
        report_path = Path(args.repo_root) / args.report_path
        report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"P9-T03 public documentation status-card validation {report.status}")
        for error in report.errors:
            print(f"ERROR: {error}")
        for warning in report.warnings:
            print(f"WARNING: {warning}")
    return 0 if report.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
