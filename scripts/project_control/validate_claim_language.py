#!/usr/bin/env python3
"""Validate claim-language surfaces against the P3 claim-language taxonomy."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


DEFAULT_TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
DEFAULT_REVIEWED_CONTEXTS_PATH = (
    REPO_ROOT / "research_control/design/claim_language_linter_reviewed_contexts.yaml"
)

CURRENT_PUBLIC_PATTERNS = (
    "README.md",
    "github-facing/*.md",
    "github-facing/**/*.md",
    "research_control/current_frontier.md",
    "research_control/design/*.md",
    "implementations_plans/*.md",
    "markdown/publication-briefs/*.md",
    "markdown/html-explainer-specs/*.md",
)
WARNING_SURFACE_PATTERNS = (
    "research_control/tasks/**/*.md",
    "research_control/tasks/**/*.tex",
    "research_control/handoffs/*.md",
    "research_control/handoffs/*.yaml",
    "registries/*.csv",
)
INTENTIONAL_EXAMPLE_PATTERNS = (
    "research_control/design/scoped_claim_language_examples.md",
    "research_control/design/claim_language_linter_taxonomy.yaml",
    "research_control/design/claim_language_linter_reviewed_contexts.yaml",
    "tests/test_validate_claim_language.py",
    "tests/fixtures/claim_language/**",
)
DEFAULT_SCAN_PATTERNS = CURRENT_PUBLIC_PATTERNS + WARNING_SURFACE_PATTERNS

SCOPED_POSITIVE_MARKERS = (
    "accepted_as_scoped_evidence_precondition",
    "accepted only as scoped",
    "accepted scoped evidence/precondition only",
    "accepted only as certificate-indexed",
    "accepted only as scoped positive",
    "accepted only as scoped source-extension",
    "adopted only as scoped",
    "scoped source-extension evidence/precondition",
    "scoped evidence/precondition only",
)

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+(?:\([A-Za-z0-9_]+\))?")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    class_id: str
    matched_text: str
    severity: str
    surface_class: str
    corrective_language: str
    context: str

    @property
    def hard_fail(self) -> bool:
        return self.severity.startswith("hard_fail_")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value or "")


def matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def rel_path(path: str | Path, repo_root: Path) -> str:
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return candidate.relative_to(repo_root).as_posix()
        except ValueError:
            return candidate.as_posix()
    return candidate.as_posix()


def load_taxonomy(path: Path = DEFAULT_TAXONOMY_PATH) -> dict[str, Any]:
    data = load_yaml(path)
    if data.get("schema_id") != "claim_language_linter_taxonomy_v1":
        raise StrictYamlError(f"{path}: unsupported claim-language taxonomy schema")
    return data


def load_reviewed_contexts(path: Path = DEFAULT_REVIEWED_CONTEXTS_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = load_yaml(path)
    if data.get("schema_id") != "claim_language_linter_reviewed_contexts_v1":
        raise StrictYamlError(f"{path}: unsupported reviewed-context schema")
    entries = _as_list(data.get("entries"))
    for entry in entries:
        required = (
            "entry_id",
            "path",
            "class_ids",
            "surface_class_override",
            "severity_override",
            "reviewed_by_task_id",
            "reviewed_by_role",
            "scope_rationale",
        )
        missing = [field for field in required if not _text(entry.get(field)).strip()]
        if missing:
            raise StrictYamlError(
                f"{path}: reviewed context {entry.get('entry_id', '<missing>')} "
                f"missing {', '.join(missing)}"
            )
        if not _as_list(entry.get("class_ids")):
            raise StrictYamlError(f"{path}: {entry.get('entry_id')} class_ids must be non-empty")
    return entries


def latest_handoff_rel(repo_root: Path) -> set[str]:
    program_state = repo_root / "research_control/program_state.yaml"
    if not program_state.exists():
        return set()
    try:
        data = load_yaml(program_state)
    except StrictYamlError:
        return set()
    handoff_id = _text(data.get("latest_handoff_id"))
    if not handoff_id:
        return set()
    return {
        f"research_control/handoffs/{handoff_id}.yaml",
        f"research_control/handoffs/{handoff_id}.md",
    }


def classify_surface(path: str, active_handoffs: set[str] | None = None) -> str:
    active_handoffs = active_handoffs or set()
    if path in active_handoffs:
        return "current_control_surfaces"
    if any(matches(path, pattern) for pattern in INTENTIONAL_EXAMPLE_PATTERNS):
        return "intentional_bad_example_surfaces"
    if any(matches(path, pattern) for pattern in WARNING_SURFACE_PATTERNS):
        return "historical_artifacts"
    if any(matches(path, pattern) for pattern in CURRENT_PUBLIC_PATTERNS):
        return "current_public_surfaces"
    return "current_control_surfaces"


def severity_for_surface(phrase_class: dict[str, Any], surface_class: str) -> str:
    if surface_class == "current_control_surfaces":
        return _text(phrase_class.get("control_severity")) or "hard_fail_current_control"
    if surface_class == "historical_artifacts":
        return _text(phrase_class.get("historical_severity")) or "warn_historical"
    if surface_class == "intentional_bad_example_surfaces":
        return "warn_intentional_example"
    return _text(phrase_class.get("default_severity")) or "hard_fail_current_public"


def reviewed_context_override(
    path: str,
    class_id: str,
    reviewed_contexts: Iterable[dict[str, Any]],
) -> tuple[str, str, str] | None:
    for entry in reviewed_contexts:
        entry_path = _text(entry.get("path"))
        class_ids = [_text(item) for item in _as_list(entry.get("class_ids"))]
        if matches(path, entry_path) and ("*" in class_ids or class_id in class_ids):
            return (
                _text(entry.get("surface_class_override")),
                _text(entry.get("severity_override")),
                _text(entry.get("entry_id")),
            )
    return None


def line_context_override(
    line_text: str,
    taxonomy: dict[str, Any],
) -> tuple[str, str] | None:
    lower = line_text.lower()
    for rule in _as_list(taxonomy.get("context_rules", {}).get("allow_contexts")):
        markers = [_text(marker).lower() for marker in _as_list(rule.get("required_marker_any"))]
        if markers and any(marker in lower for marker in markers):
            return _text(rule.get("severity_override")), _text(rule.get("context_id"))
    return None


def has_scoped_positive_context(line_text: str, class_id: str) -> bool:
    if class_id != "bare_high_risk_accepted":
        return False
    lower = line_text.lower()
    return any(marker in lower for marker in SCOPED_POSITIVE_MARKERS)


def token_strings(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def window_contains_phrase(window_tokens: list[str], phrase: str) -> bool:
    phrase_tokens = token_strings(phrase)
    if not phrase_tokens:
        return False
    width = len(phrase_tokens)
    return any(window_tokens[index : index + width] == phrase_tokens for index in range(len(window_tokens)))


def near_term_matches(
    line_text: str,
    phrase_class: dict[str, Any],
) -> Iterable[tuple[int, int, str]]:
    status_terms = {term.lower() for term in _as_list(phrase_class.get("status_terms"))}
    near_terms = [_text(term) for term in _as_list(phrase_class.get("near_terms"))]
    window = 8
    patterns = _as_list(phrase_class.get("forbidden_patterns"))
    for pattern in patterns:
        if str(pattern.get("window_tokens", "")).isdigit():
            window = int(str(pattern["window_tokens"]))
            break

    tokens = list(TOKEN_RE.finditer(line_text))
    lowered = [token.group(0).lower() for token in tokens]
    for index, token in enumerate(tokens):
        if token.group(0).lower() not in status_terms:
            continue
        left = max(0, index - window)
        right = min(len(tokens), index + window + 1)
        window_tokens = lowered[left:right]
        for near_term in near_terms:
            if window_contains_phrase(window_tokens, near_term):
                start = tokens[left].start()
                end = tokens[right - 1].end()
                yield start, end, line_text[start:end].strip()
                break


def regex_matches(
    line_text: str,
    phrase_class: dict[str, Any],
) -> Iterable[tuple[int, int, str]]:
    for pattern_record in _as_list(phrase_class.get("forbidden_patterns")):
        pattern = _text(pattern_record.get("pattern"))
        if not pattern:
            continue
        for match in re.finditer(pattern, line_text, flags=re.IGNORECASE):
            yield match.start(), match.end(), match.group(0)


def class_matches(
    line_text: str,
    phrase_class: dict[str, Any],
) -> Iterable[tuple[int, int, str]]:
    detection_kind = _text(phrase_class.get("detection_kind"))
    if detection_kind == "near_term":
        yield from near_term_matches(line_text, phrase_class)
    else:
        yield from regex_matches(line_text, phrase_class)


def has_denial_context(line_text: str, match_start: int) -> bool:
    lower = line_text.lower()
    stripped = lower.strip()
    if stripped.startswith("- [ ]"):
        return True
    before = lower[max(0, match_start - 260) : match_start]
    return bool(
        re.search(
            r"(?:\bno\b|\bnot\b|\bmust not\b|\bdoes not\b|\bdo not\b|"
            r"\bwithout\b|\bblocked\b|\bforbidden\b)[^|.;:]{0,260}$",
            before,
        )
    )


def finding_for_match(
    *,
    path: str,
    line_number: int,
    line_text: str,
    match_start: int,
    phrase_class: dict[str, Any],
    matched_text: str,
    taxonomy: dict[str, Any],
    active_handoffs: set[str],
    reviewed_contexts: Iterable[dict[str, Any]],
) -> Finding | None:
    class_id = _text(phrase_class.get("class_id"))
    if has_scoped_positive_context(line_text, class_id):
        return None
    if has_denial_context(line_text, match_start):
        return None

    surface_class = classify_surface(path, active_handoffs)
    severity = severity_for_surface(phrase_class, surface_class)
    context = "surface_policy"

    line_override = line_context_override(line_text, taxonomy)
    if line_override:
        severity, context = line_override
        if severity == "warn_intentional_example":
            surface_class = "intentional_bad_example_surfaces"

    reviewed_override = reviewed_context_override(path, class_id, reviewed_contexts)
    if reviewed_override:
        surface_class, severity, context = reviewed_override

    return Finding(
        path=path,
        line=line_number,
        class_id=class_id,
        matched_text=matched_text,
        severity=severity,
        surface_class=surface_class,
        corrective_language=_text(phrase_class.get("corrective_language")),
        context=context,
    )


def scan_text_map(
    texts: dict[str, str],
    *,
    taxonomy: dict[str, Any],
    reviewed_contexts: Iterable[dict[str, Any]] | None = None,
    active_handoffs: set[str] | None = None,
) -> list[Finding]:
    reviewed_contexts = list(reviewed_contexts or [])
    active_handoffs = active_handoffs or set()
    phrase_classes = _as_list(taxonomy.get("phrase_classes"))
    findings: list[Finding] = []
    seen: set[tuple[str, int, str, str, str]] = set()

    for path, text in sorted(texts.items()):
        for line_number, line_text in enumerate(text.splitlines(), start=1):
            for phrase_class in phrase_classes:
                class_id = _text(phrase_class.get("class_id"))
                for start, end, matched_text in class_matches(line_text, phrase_class):
                    finding = finding_for_match(
                        path=path,
                        line_number=line_number,
                        line_text=line_text,
                        match_start=start,
                        phrase_class=phrase_class,
                        matched_text=matched_text,
                        taxonomy=taxonomy,
                        active_handoffs=active_handoffs,
                        reviewed_contexts=reviewed_contexts,
                    )
                    if finding is None:
                        continue
                    key = (path, line_number, class_id, matched_text.lower(), f"{start}:{end}")
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(finding)
    return findings


def expand_default_paths(repo_root: Path) -> list[str]:
    paths: set[str] = set()
    for pattern in DEFAULT_SCAN_PATTERNS:
        for candidate in repo_root.glob(pattern):
            if candidate.is_file():
                paths.add(candidate.relative_to(repo_root).as_posix())
    return sorted(paths)


def git_changed_paths(
    repo_root: Path,
    *,
    base_ref: str = "HEAD",
    staged_only: bool = False,
) -> list[str]:
    if staged_only:
        diff_command = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", base_ref]
    else:
        diff_command = ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref]
    diff = subprocess.run(
        diff_command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if diff.returncode != 0:
        raise OSError(diff.stderr.strip() or "git diff failed")
    paths = {line.strip() for line in diff.stdout.splitlines() if line.strip()}
    if not staged_only:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if untracked.returncode != 0:
            raise OSError(untracked.stderr.strip() or "git ls-files failed")
        paths.update(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return sorted(paths)


def claim_language_gate_paths(paths: Iterable[str], *, repo_root: Path = REPO_ROOT) -> list[str]:
    active_handoffs = latest_handoff_rel(repo_root)
    selected: set[str] = set()
    for raw_path in paths:
        path = rel_path(raw_path, repo_root)
        if path in active_handoffs or any(matches(path, pattern) for pattern in DEFAULT_SCAN_PATTERNS):
            if (repo_root / path).is_file():
                selected.add(path)
    return sorted(selected)


def read_paths(paths: Iterable[str], repo_root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path_text in paths:
        path = repo_root / path_text
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(path_text)
        try:
            texts[path_text] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            texts[path_text] = path.read_text(encoding="utf-8", errors="replace")
    return texts


def report_dict(
    findings: list[Finding],
    *,
    scanned_paths: list[str],
    config_errors: list[str] | None = None,
) -> dict[str, Any]:
    config_errors = config_errors or []
    hard_failures = [finding for finding in findings if finding.hard_fail]
    warnings = [finding for finding in findings if not finding.hard_fail]
    status = "FAIL" if config_errors or hard_failures else "PASS"
    return {
        "status": status,
        "hard_fail_count": len(hard_failures),
        "warning_count": len(warnings),
        "finding_count": len(findings),
        "scanned_path_count": len(scanned_paths),
        "scanned_paths": scanned_paths,
        "config_errors": config_errors,
        "findings": [asdict(finding) for finding in findings],
    }


def validate_paths(
    *,
    repo_root: Path = REPO_ROOT,
    taxonomy_path: Path = DEFAULT_TAXONOMY_PATH,
    reviewed_contexts_path: Path = DEFAULT_REVIEWED_CONTEXTS_PATH,
    paths: list[str] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    taxonomy = load_taxonomy(taxonomy_path)
    reviewed_contexts = load_reviewed_contexts(reviewed_contexts_path)
    selected_paths = (
        [rel_path(path, repo_root) for path in paths]
        if paths is not None
        else expand_default_paths(repo_root)
    )
    texts = read_paths(selected_paths, repo_root)
    findings = scan_text_map(
        texts,
        taxonomy=taxonomy,
        reviewed_contexts=reviewed_contexts,
        active_handoffs=latest_handoff_rel(repo_root),
    )
    return report_dict(findings, scanned_paths=selected_paths)


def validate_changed_paths(
    *,
    repo_root: Path = REPO_ROOT,
    taxonomy_path: Path = DEFAULT_TAXONOMY_PATH,
    reviewed_contexts_path: Path = DEFAULT_REVIEWED_CONTEXTS_PATH,
    base_ref: str = "HEAD",
    staged_only: bool = False,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    selected_paths = claim_language_gate_paths(
        git_changed_paths(repo_root, base_ref=base_ref, staged_only=staged_only),
        repo_root=repo_root,
    )
    return validate_paths(
        repo_root=repo_root,
        taxonomy_path=taxonomy_path,
        reviewed_contexts_path=reviewed_contexts_path,
        paths=selected_paths,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help="Repository root.")
    parser.add_argument("--taxonomy", default=DEFAULT_TAXONOMY_PATH.as_posix(), help="Taxonomy YAML path.")
    parser.add_argument(
        "--reviewed-contexts",
        default=DEFAULT_REVIEWED_CONTEXTS_PATH.as_posix(),
        help="Reviewed context allowlist YAML path.",
    )
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Scan changed claim-language gate paths from git diff plus untracked files.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Scan staged claim-language gate paths from git diff --cached.",
    )
    parser.add_argument("--base-ref", default="HEAD", help="Git base ref for --changed or --staged.")
    parser.add_argument("--paths", nargs="*", help="Explicit paths to scan instead of default surfaces.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.paths and (args.changed or args.staged):
        print("--paths cannot be combined with --changed or --staged", file=sys.stderr)
        return 2
    try:
        if args.changed or args.staged:
            report = validate_changed_paths(
                repo_root=Path(args.repo_root),
                taxonomy_path=Path(args.taxonomy),
                reviewed_contexts_path=Path(args.reviewed_contexts),
                base_ref=args.base_ref,
                staged_only=args.staged,
            )
        else:
            report = validate_paths(
                repo_root=Path(args.repo_root),
                taxonomy_path=Path(args.taxonomy),
                reviewed_contexts_path=Path(args.reviewed_contexts),
                paths=args.paths,
            )
    except (FileNotFoundError, StrictYamlError, OSError, re.error) as exc:
        report = report_dict([], scanned_paths=args.paths or [], config_errors=[str(exc)])

    if args.json:
        print(json.dumps(report, indent=2))
    elif report["status"] == "PASS":
        print(
            "Claim-language validation passed "
            f"({report['warning_count']} warning(s), {report['scanned_path_count']} path(s))."
        )
        for finding in report["findings"][:25]:
            print(
                f"- WARN {finding['path']}:{finding['line']} "
                f"{finding['class_id']} {finding['matched_text']!r}"
            )
    else:
        print("Claim-language validation failed:")
        for error in report["config_errors"]:
            print(f"- CONFIG {error}")
        for finding in report["findings"]:
            prefix = "FAIL" if finding["severity"].startswith("hard_fail_") else "WARN"
            print(
                f"- {prefix} {finding['path']}:{finding['line']} "
                f"{finding['class_id']} {finding['matched_text']!r} "
                f"({finding['severity']})"
            )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
