#!/usr/bin/env python3
"""Audit registered documentation and derivative surface consistency."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = "registries"

REQUIRED_REGISTRIES = {
    "markdown": "MARKDOWN_SOURCE_REGISTRY.csv",
    "html": "HTML_EXPLAINER_REGISTRY.csv",
    "tex": "TEX_SOURCE_REGISTRY.csv",
    "pdf": "PDF_DERIVATIVE_REGISTRY.csv",
    "wiki": "WIKI_ARTIFACT_REGISTRY.csv",
    "file": "FILE_OBJECT_REGISTRY.csv",
    "semantic": "CONTENT_SEMANTIC_REGISTRY.csv",
    "vault": "OBSIDIAN_VAULT_REGISTRY.csv",
    "relationships": "OBJECT_RELATIONSHIP_REGISTRY.csv",
}

LOCAL_PREFIXES = (".local/",)
STALE_REFERENCE = "docs/github-facing"
ACTIVE_REFERENCE_ROOTS = (
    "README.md",
    "CONTEXT.md",
    "AGENTS.md",
    "research_control/AGENTS.md",
    ".codex/skills",
    ".agents/roles",
    "github-facing",
    "markdown",
)


@dataclass
class AuditReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    include_local: bool = True

    def error(self, message: str) -> None:
        self.errors.append(message)

    def ok(self) -> bool:
        return not self.errors

    def count(self, name: str, increment: int = 1) -> None:
        self.counts[name] = self.counts.get(name, 0) + increment

    def as_dict(self) -> dict[str, object]:
        return {
            "status": "PASS" if self.ok() else "FAIL",
            "errors": self.errors,
            "warnings": self.warnings,
            "counts": dict(sorted(self.counts.items())),
            "include_local": self.include_local,
        }


def normalized_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip() + "\n"


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[index + 1 :])
    return text


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def should_check_path(path_text: str, *, include_local: bool) -> bool:
    path_text = path_text.strip()
    if not path_text:
        return False
    if path_text.startswith(("http://", "https://")):
        return False
    if path_text.startswith(LOCAL_PREFIXES) and not include_local:
        return False
    return True


def looks_like_path(value: str) -> bool:
    if not value:
        return False
    return "/" in value or value.startswith(".") or bool(Path(value).suffix)


def check_path_exists(
    report: AuditReport,
    root: Path,
    path_text: str,
    *,
    context: str,
) -> None:
    if not should_check_path(path_text, include_local=report.include_local):
        return
    if not (root / path_text).exists():
        report.error(f"{context}: path does not exist: {path_text}")


def read_registry(
    report: AuditReport,
    root: Path,
    registry_name: str,
) -> list[dict[str, str]]:
    path = root / REGISTRY_DIR / registry_name
    if not path.exists():
        report.error(f"{registry_name}: required registry is missing")
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def row_by_object(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("object_id", "").strip(): row
        for row in rows
        if row.get("object_id", "").strip()
    }


def check_hash(
    report: AuditReport,
    root: Path,
    row: dict[str, str],
    *,
    path_field: str,
    hash_field: str,
    context: str,
) -> None:
    path_text = row.get(path_field, "").strip()
    expected_hash = row.get(hash_field, "").strip()
    if not path_text or not expected_hash:
        return
    if not should_check_path(path_text, include_local=report.include_local):
        return
    path = root / path_text
    if not path.exists() or not path.is_file():
        return
    actual_hash = sha256_file(path)
    if actual_hash != expected_hash:
        report.error(
            f"{context}: stale {hash_field} for {path_text}: "
            f"expected {expected_hash} actual {actual_hash}"
        )


def check_generated_outputs(
    report: AuditReport,
    root: Path,
    row: dict[str, str],
    *,
    context: str,
) -> None:
    for output_path in split_paths(row.get("generated_outputs", "")):
        check_path_exists(report, root, output_path, context=context)


def check_markdown_rows(
    report: AuditReport,
    root: Path,
    markdown_rows: list[dict[str, str]],
) -> None:
    for row in markdown_rows:
        object_id = row.get("object_id", "").strip() or "<missing-object-id>"
        context = f"MARKDOWN_SOURCE_REGISTRY.csv:{object_id}"
        path_text = row.get("path", "").strip()
        check_path_exists(report, root, path_text, context=context)
        check_hash(report, root, row, path_field="path", hash_field="source_hash", context=context)
        check_generated_outputs(report, root, row, context=context)
        report.count("checked_markdown_rows")


def check_html_rows(
    report: AuditReport,
    root: Path,
    html_rows: list[dict[str, str]],
    markdown_by_object: dict[str, dict[str, str]],
) -> None:
    for row in html_rows:
        object_id = row.get("object_id", "").strip() or "<missing-object-id>"
        context = f"HTML_EXPLAINER_REGISTRY.csv:{object_id}"
        path_text = row.get("path", "").strip()
        check_path_exists(report, root, path_text, context=context)
        check_hash(report, root, row, path_field="path", hash_field="source_hash", context=context)
        check_hash(report, root, row, path_field="path", hash_field="html_hash", context=context)
        check_generated_outputs(report, root, row, context=context)

        source_basis = row.get("source_basis", "").strip()
        if not source_basis:
            report.error(f"{context}: missing source_basis")
        elif source_basis not in markdown_by_object:
            report.error(f"{context}: source_basis is not registered: {source_basis}")
        else:
            source_row = markdown_by_object[source_basis]
            source_path = source_row.get("path", "").strip()
            check_path_exists(report, root, source_path, context=f"{context}:source_basis")
            expected_source_hash = row.get("source_basis_hash", "").strip()
            if source_path and expected_source_hash and (root / source_path).exists():
                actual_source_hash = sha256_file(root / source_path)
                if actual_source_hash != expected_source_hash:
                    report.error(
                        f"{context}: stale source_basis_hash for {source_path}: "
                        f"expected {expected_source_hash} actual {actual_source_hash}"
                    )

        generated_from = row.get("generated_from", "").strip()
        if generated_from and source_basis and generated_from != source_basis:
            report.error(
                f"{context}: generated_from {generated_from} does not match source_basis {source_basis}"
            )
        report.count("checked_html_rows")


def check_tex_rows(
    report: AuditReport,
    root: Path,
    tex_rows: list[dict[str, str]],
    pdf_by_object: dict[str, dict[str, str]],
) -> None:
    for row in tex_rows:
        object_id = row.get("object_id", "").strip() or "<missing-object-id>"
        context = f"TEX_SOURCE_REGISTRY.csv:{object_id}"
        path_text = row.get("path", "").strip()
        check_path_exists(report, root, path_text, context=context)
        check_hash(report, root, row, path_field="path", hash_field="source_hash", context=context)
        check_generated_outputs(report, root, row, context=context)

        if row.get("pdf_required", "").strip().lower() == "true":
            pdf_object_id = row.get("pdf_object_id", "").strip()
            pdf_path = row.get("pdf_path", "").strip()
            if pdf_object_id and pdf_object_id not in pdf_by_object:
                report.error(f"{context}: pdf_object_id is not registered: {pdf_object_id}")
            check_path_exists(report, root, pdf_path, context=context)
        report.count("checked_tex_rows")


def check_pdf_rows(
    report: AuditReport,
    root: Path,
    pdf_rows: list[dict[str, str]],
    tex_by_object: dict[str, dict[str, str]],
) -> None:
    for row in pdf_rows:
        object_id = row.get("object_id", "").strip() or "<missing-object-id>"
        context = f"PDF_DERIVATIVE_REGISTRY.csv:{object_id}"
        path_text = row.get("path", "").strip()
        check_path_exists(report, root, path_text, context=context)
        check_hash(report, root, row, path_field="path", hash_field="source_hash", context=context)
        check_hash(report, root, row, path_field="path", hash_field="pdf_hash", context=context)
        check_generated_outputs(report, root, row, context=context)

        source_tex_id = row.get("source_tex_object_id", "").strip()
        if not source_tex_id:
            report.error(f"{context}: missing source_tex_object_id")
        elif source_tex_id not in tex_by_object:
            report.error(f"{context}: source_tex_object_id is not registered: {source_tex_id}")
        else:
            tex_row = tex_by_object[source_tex_id]
            source_tex_path = row.get("source_tex_path", "").strip()
            if source_tex_path != tex_row.get("path", "").strip():
                report.error(f"{context}: source_tex_path does not match TEX registry row")
            source_tex_hash = row.get("source_tex_hash", "").strip()
            if source_tex_hash and source_tex_hash != tex_row.get("source_hash", "").strip():
                report.error(f"{context}: source_tex_hash does not match TEX registry row")
        report.count("checked_pdf_rows")


def check_path_registry(
    report: AuditReport,
    root: Path,
    rows: list[dict[str, str]],
    *,
    registry_name: str,
    fields: tuple[str, ...],
) -> None:
    for row in rows:
        object_id = row.get("object_id", "").strip() or "<missing-object-id>"
        context = f"{registry_name}:{object_id}"
        for field_name in fields:
            value = row.get(field_name, "").strip()
            if not value:
                continue
            if field_name == "generated_outputs":
                for path_text in split_paths(value):
                    check_path_exists(report, root, path_text, context=context)
            else:
                check_path_exists(report, root, value, context=context)
        report.count(f"checked_{registry_name.removesuffix('.csv').lower()}_rows")


def check_relationship_rows(
    report: AuditReport,
    root: Path,
    rows: list[dict[str, str]],
) -> None:
    for row in rows:
        object_id = row.get("object_id", "").strip() or row.get("edge_id", "").strip() or "<missing-object-id>"
        context = f"OBJECT_RELATIONSHIP_REGISTRY.csv:{object_id}"
        for field_name in ("source_path", "target_path"):
            value = row.get(field_name, "").strip()
            if value and looks_like_path(value):
                check_path_exists(report, root, value, context=context)
        report.count("checked_relationship_rows")


def check_github_facing_mirrors(report: AuditReport, root: Path) -> None:
    mirror_dir = root / "github-facing"
    if not mirror_dir.exists():
        report.warnings.append("github-facing directory is absent; mirror check skipped")
        return
    for mirror_path in sorted(mirror_dir.glob("*.md")):
        source_path = root / "markdown" / "html-explainer-specs" / mirror_path.name
        relative_mirror = mirror_path.relative_to(root).as_posix()
        relative_source = source_path.relative_to(root).as_posix()
        if not source_path.exists():
            report.error(f"{relative_mirror}: matching source spec is missing: {relative_source}")
            continue
        mirror_text = normalized_text(mirror_path.read_text(encoding="utf-8"))
        source_text = normalized_text(strip_frontmatter(source_path.read_text(encoding="utf-8")))
        if mirror_text != source_text:
            report.error(f"{relative_mirror}: mirror body differs from {relative_source}")
        report.count("checked_github_facing_mirrors")


def iter_active_reference_files(root: Path) -> Iterable[Path]:
    for relative in ACTIVE_REFERENCE_ROOTS:
        path = root / relative
        if not path.exists():
            continue
        if path.is_file():
            yield path
            continue
        for child in sorted(path.rglob("*")):
            if child.is_file() and child.suffix in {".md", ".py", ".yaml", ".yml", ".csv"}:
                yield child


def check_stale_references(report: AuditReport, root: Path, needle: str) -> None:
    for path in iter_active_reference_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        if needle in text:
            relative = path.relative_to(root).as_posix()
            report.error(f"{relative}: stale reference found: {needle}")


def audit_documentation_surfaces(
    root: Path = REPO_ROOT,
    *,
    include_local: bool = True,
    stale_reference: str = STALE_REFERENCE,
) -> AuditReport:
    root = root.resolve()
    report = AuditReport(include_local=include_local)
    registries = {
        key: read_registry(report, root, filename)
        for key, filename in REQUIRED_REGISTRIES.items()
    }

    markdown_rows = registries["markdown"]
    html_rows = registries["html"]
    tex_rows = registries["tex"]
    pdf_rows = registries["pdf"]

    markdown_by_object = row_by_object(markdown_rows)
    tex_by_object = row_by_object(tex_rows)
    pdf_by_object = row_by_object(pdf_rows)

    check_markdown_rows(report, root, markdown_rows)
    check_html_rows(report, root, html_rows, markdown_by_object)
    check_tex_rows(report, root, tex_rows, pdf_by_object)
    check_pdf_rows(report, root, pdf_rows, tex_by_object)
    check_path_registry(
        report,
        root,
        registries["wiki"],
        registry_name=REQUIRED_REGISTRIES["wiki"],
        fields=("path", "source_path"),
    )
    check_path_registry(
        report,
        root,
        registries["file"],
        registry_name=REQUIRED_REGISTRIES["file"],
        fields=("path",),
    )
    check_path_registry(
        report,
        root,
        registries["semantic"],
        registry_name=REQUIRED_REGISTRIES["semantic"],
        fields=("path", "extracted_text_path"),
    )
    check_path_registry(
        report,
        root,
        registries["vault"],
        registry_name=REQUIRED_REGISTRIES["vault"],
        fields=(
            "path",
            "vault_note_path",
            "vault_raw_path",
            "vault_attachment_path",
            "vault_index_path",
        ),
    )
    check_relationship_rows(report, root, registries["relationships"])
    check_github_facing_mirrors(report, root)
    check_stale_references(report, root, stale_reference)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root.")
    parser.add_argument(
        "--skip-local",
        action="store_true",
        help="Skip ignored .local retrieval/vault path existence checks.",
    )
    parser.add_argument(
        "--stale-reference",
        default=STALE_REFERENCE,
        help="Reference string that must be absent from active docs/specs.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = audit_documentation_surfaces(
        Path(args.root),
        include_local=not args.skip_local,
        stale_reference=args.stale_reference,
    )
    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
    elif report.ok():
        print("Documentation surface audit passed.")
        for name, count in sorted(report.counts.items()):
            print(f"- {name}: {count}")
        if not report.include_local:
            print("- local_path_checks: skipped")
    else:
        print("Documentation surface audit failed:")
        for error in report.errors:
            print(f"- {error}")
        for warning in report.warnings:
            print(f"- warning: {warning}")
    return 0 if report.ok() else 1


if __name__ == "__main__":
    raise SystemExit(main())
