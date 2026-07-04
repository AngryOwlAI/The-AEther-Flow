#!/usr/bin/env python3
"""Audit high-risk bare ``accepted`` wording for v15 P13-T01.

The audit is intentionally task-local: it reports and classifies findings but
does not remediate source wording or promote any scientific claim.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260703-026"
JOB_ID = "AJ-RT-20260703-026-001"
PLAN_TASK_ID = "P13-T01"

ACCEPTED_RE = re.compile(r"\baccepted\b", re.IGNORECASE)

HIGH_RISK_TERMS: dict[str, tuple[str, ...]] = {
    "M_src": (r"\bM_src\b",),
    "g_eff": (r"\bg_eff\b", r"\bgeff\b", r"\bMetricData\(E\)\b"),
    "Resp_lc": (r"\bResp_lc\b", r"\bresponse token\b", r"\bresponse-token\b"),
    "matter_coupling": (r"\bmatter_coupling\b", r"\bmatter coupling\b"),
    "PositiveMSProfile_v1": (r"\bPositiveMSProfile_v1\b",),
    "RR_ETransportCompletenessOrInvarianceLaw_v1": (
        r"\bRR_ETransportCompletenessOrInvarianceLaw_v1\b",
        r"\bRR_E\b",
    ),
    "SourceMatterSemanticsAdoptionReadinessLaw_v1": (
        r"\bSourceMatterSemanticsAdoptionReadinessLaw_v1\b",
    ),
    "MSStableMatterSemanticsBridge_v1": (
        r"\bMSStableMatterSemanticsBridge_v1\b",
        r"\bstable matter-semantics bridge\b",
        r"\bstable matter semantics bridge\b",
    ),
    "SourceCouplingLawCandidate": (
        r"\bSourceCouplingLawCandidate\b",
        r"\bcoupling-law-candidate\b",
        r"\bcoupling law candidate\b",
    ),
    "P2 theorem result": (
        r"\bNarrowMSCertEq_v1\b",
        r"\bNarrowMSCertEq\b",
        r"\bP2 theorem result\b",
        r"\bP2 theorem\b",
    ),
}

COMPILED_HIGH_RISK_TERMS = {
    key: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for key, patterns in HIGH_RISK_TERMS.items()
}

SCOPED_POSITIVE_MARKERS = (
    "accepted only as",
    "accepted only through",
    "accepted only under",
    "accepted only scoped",
    "accepted scoped",
    "accepted as scoped",
    "accepts only",
    "only as",
    "only as a scoped",
    "only as scoped",
    "only while",
    "accepted prerequisite evidence",
    "evidence as bounded input",
    "evidence as sufficient only",
    "evidence precondition only",
    "precondition data",
    "precondition evidence",
    "source-extension evidence",
    "source-extension metric-data",
    "source-extension selector evidence",
    "scoped source-extension",
    "accepted_as_scoped_evidence_precondition",
    "accepted only as scoped",
    "accepted scoped evidence/precondition only",
    "accepted only as certificate-indexed",
    "accepted only as certificate indexed",
    "accepted only as scoped positive",
    "accepted only as scoped source-extension",
    "accepted only as source-extension evidence-status",
    "accepted only as scoped source-extension evidence-status",
    "accepted only as scoped source-extension evidence/precondition",
    "scoped evidence/precondition",
    "scoped positive",
    "certificate-indexed scoped evidence/precondition",
    "certificate indexed scoped evidence/precondition",
    "source-extension evidence-status",
    "status-boundary evidence only",
)

INTENTIONAL_CONTEXT_MARKERS = (
    "bare accepted",
    "bare `accepted`",
    "blocked claim",
    "never bare accepted",
    "bad example",
    "forbidden phrase",
    "forbidden wording",
    "forbids overread",
    "accepted bridge evidence as",
    "accepted evidence as adoption",
    "accepted evidence as matter",
    "linter fixture",
    "negative example",
    "not adopted or accepted",
    "not be treated as accepted",
    "route requirement",
    "required bad example",
    "why it is wrong",
    "quotes forbidden",
)

INTENTIONAL_PATH_PATTERNS = (
    "research_control/design/claim_language_linter_taxonomy.yaml",
    "research_control/design/claim_language_linter_reviewed_contexts.yaml",
    "research_control/design/scoped_claim_language_examples.md",
    "tests/**",
)

RAW_ACCEPTED_FIELD_RE = re.compile(
    r'(^|,)"?accepted"?($|,)|'
    r'"(?:status|state|state_label|gate_chair_status|registry_status)"\s*:\s*"accepted"|'
    r"\b(?:status|state|gate_chair_status|registry_status):\s*\"?accepted\"?\b",
    re.IGNORECASE,
)

TEXT_SUFFIXES = {
    ".csv",
    ".dot",
    ".json",
    ".md",
    ".py",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}

INCLUDED_PATTERNS = (
    "README.md",
    "AGENTS.md",
    "github-facing/**",
    "implementations_plans/**",
    "markdown/**",
    "output/**",
    "registries/**",
    "research_control/**",
    "wiki/**",
    "FOLDER_MAP.md",
)

EXCLUDED_PATTERNS = (
    ".local/**",
    "research_control/tasks/RT-20260703-026/**",
)


@dataclass(frozen=True)
class Finding:
    finding_id: str
    path: str
    line: int
    classification: str
    high_risk_terms: list[str]
    matched_text: str
    rationale: str
    surface_class: str
    requires_followup: bool


def run_git_ls_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def should_scan(path: str) -> bool:
    if matches_any(path, EXCLUDED_PATTERNS):
        return False
    if Path(path).suffix not in TEXT_SUFFIXES and path not in {"README.md", "AGENTS.md", "FOLDER_MAP.md"}:
        return False
    return matches_any(path, INCLUDED_PATTERNS)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except UnicodeDecodeError:
            return None


def matched_high_risk_terms(text: str) -> list[str]:
    terms: list[str] = []
    for term, patterns in COMPILED_HIGH_RISK_TERMS.items():
        if any(pattern.search(text) for pattern in patterns):
            terms.append(term)
    return sorted(terms)


def surface_class(path: str) -> str:
    if path.startswith("wiki/") or path.startswith("output/") or path == "FOLDER_MAP.md":
        return "generated_derivative"
    if path.endswith(".meta.json") and path.startswith("registries/"):
        return "generated_derivative"
    if path.startswith("registries/"):
        return "registry"
    if path == "README.md" or path.startswith("github-facing/") or path.startswith("markdown/"):
        return "public_or_reader_facing"
    if path == "research_control/current_frontier.md":
        return "current_control"
    if path.startswith("research_control/design/"):
        return "current_control"
    if path.startswith("research_control/handoffs/"):
        return "historical_control"
    if path.startswith("research_control/tasks/"):
        return "historical_control"
    if path.startswith("implementations_plans/"):
        return "route_context"
    return "control_or_support"


def has_scoped_context(context: str) -> bool:
    lower = context.lower()
    return any(marker in lower for marker in SCOPED_POSITIVE_MARKERS)


def has_intentional_context(path: str, context: str) -> bool:
    if matches_any(path, INTENTIONAL_PATH_PATTERNS):
        return True
    lower = context.lower()
    return any(marker in lower for marker in INTENTIONAL_CONTEXT_MARKERS)


def has_raw_accepted_field(line_text: str) -> bool:
    return bool(RAW_ACCEPTED_FIELD_RE.search(line_text))


def classify(path: str, line_text: str, context: str, terms: list[str]) -> tuple[str, str, bool]:
    surface = surface_class(path)

    if surface == "registry" and has_raw_accepted_field(line_text):
        return (
            "registry field requiring alias layer",
            "The occurrence is in a raw registry status field and should be rendered through a scoped-positive alias layer before reader-facing use.",
            True,
        )

    if surface == "generated_derivative" and has_raw_accepted_field(line_text):
        return (
            "generated derivative requiring renderer fix",
            "The occurrence is in a generated raw status or summary field and should be eliminated by changing the source renderer or source alias layer, not by hand-editing the derivative.",
            True,
        )

    if has_scoped_context(context):
        return (
            "false positive",
            "The occurrence is immediately scoped by allowed scoped-positive wording.",
            False,
        )

    if has_intentional_context(path, context):
        return (
            "false positive",
            "The occurrence appears in a route requirement, negative example, or linter/control quotation rather than a project-status assertion.",
            False,
        )

    if surface == "generated_derivative":
        return (
            "generated derivative requiring renderer fix",
            "The occurrence is in a generated derivative surface and should be eliminated by changing the source renderer or source alias layer, not by hand-editing the derivative.",
            True,
        )

    if surface == "registry":
        return (
            "registry field requiring alias layer",
            "The occurrence is in a registry row or field and should be rendered through a scoped-positive alias layer before reader-facing use.",
            True,
        )

    if surface == "public_or_reader_facing" or surface == "current_control":
        return (
            "unsafe reader-facing wording",
            "The occurrence is on a current reader-facing or control-facing source surface and is not immediately scoped.",
            True,
        )

    if surface == "historical_control" or surface == "route_context":
        return (
            "safe legacy raw status",
            "The occurrence is retained in historical control or route-context material and is not presented as current status.",
            False,
        )

    return (
        "unsafe reader-facing wording",
        "The occurrence is on a tracked control/support surface and lacks immediate scoped-positive qualification.",
        True,
    )


def collect_findings(repo_root: Path) -> tuple[list[str], list[Finding]]:
    scanned_paths: list[str] = []
    findings: list[Finding] = []
    finding_index = 1

    for path in sorted(run_git_ls_files(repo_root)):
        if not should_scan(path):
            continue
        text = read_text(repo_root / path)
        if text is None:
            continue
        scanned_paths.append(path)
        lines = text.splitlines()
        for index, line in enumerate(lines, start=1):
            if not ACCEPTED_RE.search(line):
                continue
            context_lines = lines[max(0, index - 2) : min(len(lines), index + 1)]
            context = "\n".join(context_lines)
            terms = matched_high_risk_terms(context)
            if not terms:
                continue
            classification, rationale, requires_followup = classify(path, line, context, terms)
            findings.append(
                Finding(
                    finding_id=f"P13-T01-{finding_index:04d}",
                    path=path,
                    line=index,
                    classification=classification,
                    high_risk_terms=terms,
                    matched_text=line.strip(),
                    rationale=rationale,
                    surface_class=surface_class(path),
                    requires_followup=requires_followup,
                )
            )
            finding_index += 1

    return scanned_paths, findings


def make_report(scanned_paths: list[str], findings: list[Finding]) -> dict[str, object]:
    classification_counts = Counter(finding.classification for finding in findings)
    surface_counts = Counter(finding.surface_class for finding in findings)
    followup_count = sum(1 for finding in findings if finding.requires_followup)
    return {
        "schema_id": "high_risk_bare_accepted_wording_audit_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": PLAN_TASK_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "PASS",
        "no_physics_delta": True,
        "scan_scope": {
            "scanned_path_count": len(scanned_paths),
            "included_patterns": list(INCLUDED_PATTERNS),
            "excluded_patterns": list(EXCLUDED_PATTERNS),
            "high_risk_terms": {key: list(patterns) for key, patterns in HIGH_RISK_TERMS.items()},
        },
        "summary": {
            "finding_count": len(findings),
            "classification_counts": dict(sorted(classification_counts.items())),
            "surface_counts": dict(sorted(surface_counts.items())),
            "requires_followup_count": followup_count,
            "p13_t02_required": followup_count > 0,
            "next_recommended_route": (
                "P13-T02 high-risk status alias and renderer enforcement"
                if followup_count > 0
                else "P14-T01 public status source spec"
            ),
        },
        "findings": [asdict(finding) for finding in findings],
    }


def escape_cell(value: object) -> str:
    text = str(value).replace("\n", " ").strip()
    return text.replace("|", "\\|")


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]  # type: ignore[index]
    scan_scope = report["scan_scope"]  # type: ignore[index]
    findings = report["findings"]  # type: ignore[index]
    classification_counts: dict[str, int] = summary["classification_counts"]  # type: ignore[index]
    surface_counts: dict[str, int] = summary["surface_counts"]  # type: ignore[index]

    lines: list[str] = [
        "<!-- authority: control -->",
        "",
        "# High-Risk Bare Accepted Wording Audit v1",
        "",
        "## Scope",
        "",
        "This artifact implements v15 P13-T01. It audits tracked public-facing,",
        "control-facing, and generated source surfaces for bare `accepted` wording",
        "near high-risk rows. It is an audit and routing artifact only. It does",
        "not remediate wording, adopt a source law, promote matter coupling,",
        "derive Einstein equations, promote benchmark status, or complete a",
        "derivation.",
        "",
        "The audit excludes `research_control/tasks/RT-20260703-026/**` to avoid",
        "self-referential findings from this task's own report and control records.",
        "",
        "## Method",
        "",
        f"- Scanned tracked path count: `{scan_scope['scanned_path_count']}`.",
        "- Candidate rule: a line containing the token `accepted` with at least one",
        "  high-risk object in the one-line-before/current-line/one-line-after context.",
        "- Classification categories are exactly the P13-T01 categories.",
        "- Immediate scoped-positive language and explicit negative-example or route",
        "  quotation contexts are classified as `false positive`.",
        "",
        "## Summary",
        "",
        f"- Finding count: `{summary['finding_count']}`.",
        f"- Requires follow-up count: `{summary['requires_followup_count']}`.",
        f"- P13-T02 required: `{str(summary['p13_t02_required']).lower()}`.",
        f"- Next recommended route: `{summary['next_recommended_route']}`.",
        f"- No physics delta: `{str(report['no_physics_delta']).lower()}`.",
        "",
        "### Classification Counts",
        "",
        "| Classification | Count |",
        "| --- | ---: |",
    ]

    ordered_categories = (
        "safe legacy raw status",
        "unsafe reader-facing wording",
        "generated derivative requiring renderer fix",
        "registry field requiring alias layer",
        "false positive",
    )
    for category in ordered_categories:
        lines.append(f"| {escape_cell(category)} | {classification_counts.get(category, 0)} |")

    lines.extend(
        [
            "",
            "### Surface Counts",
            "",
            "| Surface class | Count |",
            "| --- | ---: |",
        ]
    )
    for surface, count in sorted(surface_counts.items()):
        lines.append(f"| {escape_cell(surface)} | {count} |")

    lines.extend(
        [
            "",
            "## Follow-Up Findings",
            "",
            "| ID | Classification | Path | Line | Terms | Matched text | Rationale |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    followup_rows = [finding for finding in findings if finding["requires_followup"]]
    if not followup_rows:
        lines.append("| none | none | none | 0 | none | none | none |")
    for finding in followup_rows:
        lines.append(
            "| {finding_id} | {classification} | `{path}` | {line} | {terms} | {matched} | {rationale} |".format(
                finding_id=escape_cell(finding["finding_id"]),
                classification=escape_cell(finding["classification"]),
                path=escape_cell(finding["path"]),
                line=finding["line"],
                terms=escape_cell(", ".join(finding["high_risk_terms"])),
                matched=escape_cell(finding["matched_text"]),
                rationale=escape_cell(finding["rationale"]),
            )
        )

    lines.extend(
        [
            "",
            "## Full Classification Table",
            "",
            "| ID | Classification | Surface | Path | Line | Terms | Matched text |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    if not findings:
        lines.append("| none | none | none | none | 0 | none | none |")
    for finding in findings:
        lines.append(
            "| {finding_id} | {classification} | {surface} | `{path}` | {line} | {terms} | {matched} |".format(
                finding_id=escape_cell(finding["finding_id"]),
                classification=escape_cell(finding["classification"]),
                surface=escape_cell(finding["surface_class"]),
                path=escape_cell(finding["path"]),
                line=finding["line"],
                terms=escape_cell(", ".join(finding["high_risk_terms"])),
                matched=escape_cell(finding["matched_text"]),
            )
        )

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "The audit is complete and has no physics delta. If `requires_followup_count`",
            "is nonzero, the logical next step is P13-T02 alias and renderer",
            "enforcement before any P13-T03 source remediation decision.",
            "",
            "## Source Materials",
            "",
            "The AEther-Flow Research Project. (2026, July 3). *Recommendations",
            "implementation plan continue task v15* [Internal implementation plan].",
            "",
            "The AEther-Flow Research Project. (2026, July 1). *Scoped positive claim",
            "vocabulary* [Internal control note].",
            "",
            "The AEther-Flow Research Project. (2026, July 2). *Three-tier claim",
            "convention* [Internal control policy].",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", required=True, help="Path for machine-readable JSON report.")
    parser.add_argument("--markdown-out", required=True, help="Path for required Markdown audit artifact.")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help="Repository root.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    scanned_paths, findings = collect_findings(repo_root)
    report = make_report(scanned_paths, findings)

    json_out = Path(args.json_out)
    markdown_out = Path(args.markdown_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown_out.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
