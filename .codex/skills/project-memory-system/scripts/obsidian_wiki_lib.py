#!/usr/bin/env python3
"""Shared helpers for the local Obsidian memory wiki."""

from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import re
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


COMMON_COLUMNS = [
    "object_id",
    "path",
    "format",
    "role",
    "authority_status",
    "audience",
    "source_hash",
    "related_source",
    "generated_from",
    "generated_outputs",
    "owner_skill",
    "validation_status",
    "last_validated_at",
    "notes",
]

SOURCE_REGISTRY_NAMES = [
    "MARKDOWN_SOURCE_REGISTRY.csv",
    "TEX_SOURCE_REGISTRY.csv",
    "PDF_DERIVATIVE_REGISTRY.csv",
    "HTML_EXPLAINER_REGISTRY.csv",
]

OBSIDIAN_VAULT_COLUMNS = COMMON_COLUMNS + [
    "source_object_id",
    "source_registry",
    "vault_root",
    "vault_note_path",
    "vault_raw_path",
    "vault_attachment_path",
    "vault_index_path",
    "sync_status",
    "synced_at",
]

CONTENT_SEMANTIC_COLUMNS = COMMON_COLUMNS + [
    "source_object_id",
    "source_registry",
    "extractor",
    "extraction_status",
    "content_hash",
    "extracted_text_path",
    "content_chars",
    "page_count",
    "headings",
    "links",
    "labels",
    "refs",
    "citations",
    "equation_count",
    "html_title",
    "generated_at",
]

OBJECT_RELATIONSHIP_COLUMNS = COMMON_COLUMNS + [
    "edge_id",
    "source_object_id",
    "target_object_id",
    "relationship_type",
    "source_registry",
    "source_field",
    "source_path",
    "target_path",
    "evidence",
    "generated_at",
]

GENERATED_REGISTRY_COLUMNS = {
    "OBSIDIAN_VAULT_REGISTRY.csv": OBSIDIAN_VAULT_COLUMNS,
    "CONTENT_SEMANTIC_REGISTRY.csv": CONTENT_SEMANTIC_COLUMNS,
    "OBJECT_RELATIONSHIP_REGISTRY.csv": OBJECT_RELATIONSHIP_COLUMNS,
}

VAULT_ROOT_RELATIVE = Path(".local/obsidian/aether-flow-wiki")
CONTENT_ROOT_RELATIVE = Path(".local/content_semantics")
MEMORY_INDEX_RELATIVE = Path(".local/memory_index/memory.sqlite")
TEMPLATE_ROOT_RELATIVE = Path(".codex/skills/project-memory-system/obsidian-vault-template")

VAULT_DIRECTORIES = [
    ".obsidian",
    "00_control",
    "01_raw/markdown",
    "01_raw/tex",
    "01_raw/pdf",
    "01_raw/html",
    "02_sources/markdown",
    "02_sources/tex",
    "02_sources/pdf",
    "02_sources/html",
    "03_indexes",
    "04_relationships",
    "05_queries",
    "07_logs",
    "08_templates",
    "09_schema",
]

MANUAL_NOTES_START = "<!-- MANUAL LOCAL NOTES START -->"
MANUAL_NOTES_END = "<!-- MANUAL LOCAL NOTES END -->"
DEFAULT_MANUAL_NOTES = "<!-- Add local, non-authoritative Obsidian-only notes here if needed. -->"


@dataclass
class SemanticExtract:
    """Content extracted from one registered object."""

    text: str
    status: str
    extractor: str
    page_count: int = 0
    headings: list[str] | None = None
    links: list[str] | None = None
    labels: list[str] | None = None
    refs: list[str] | None = None
    citations: list[str] | None = None
    equation_count: int = 0
    html_title: str = ""
    error: str = ""

    @property
    def content_hash(self) -> str:
        return sha256_text(self.text) if self.text else ""


class VisibleHTMLTextParser(HTMLParser):
    """Extract visible text and simple structure from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.current_tag = ""
        self.title_chunks: list[str] = []
        self.headings: list[str] = []
        self.links: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.current_tag = tag
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if tag == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        self.current_tag = ""

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        self.text_chunks.append(text)
        if self.current_tag == "title":
            self.title_chunks.append(text)
        if self.current_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append(text)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "object"


def json_cell(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    ensure_directory(path.parent)
    path.write_text(text, encoding="utf-8")
    return True


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [{key: value or "" for key, value in row.items()} for row in reader]


def csv_text(fieldnames: list[str], rows: list[dict[str, str]]) -> str:
    handle = io.StringIO()
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fieldnames})
    return handle.getvalue()


def write_csv_if_changed(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> bool:
    return write_text_if_changed(path, csv_text(fieldnames, rows))


def registry_path(repo_root: Path, name: str) -> Path:
    return repo_root / "registries" / name


def vault_root(repo_root: Path, vault: str | Path | None = None) -> Path:
    if vault:
        candidate = Path(vault).expanduser()
        return candidate if candidate.is_absolute() else (repo_root / candidate)
    return repo_root / VAULT_ROOT_RELATIVE


def content_root(repo_root: Path) -> Path:
    return repo_root / CONTENT_ROOT_RELATIVE


def memory_index_path(repo_root: Path, index_path: str | Path | None = None) -> Path:
    if index_path:
        candidate = Path(index_path).expanduser()
        return candidate if candidate.is_absolute() else (repo_root / candidate)
    return repo_root / MEMORY_INDEX_RELATIVE


def rel_to_repo(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def load_rows_by_registry(repo_root: Path) -> dict[str, list[dict[str, str]]]:
    names = [
        *SOURCE_REGISTRY_NAMES,
        "WIKI_ARTIFACT_REGISTRY.csv",
        "OBSIDIAN_VAULT_REGISTRY.csv",
        "CONTENT_SEMANTIC_REGISTRY.csv",
        "OBJECT_RELATIONSHIP_REGISTRY.csv",
    ]
    return {name: read_csv_rows(registry_path(repo_root, name)) for name in names}


def source_rows_with_registry(
    rows_by_registry: dict[str, list[dict[str, str]]]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for registry_name in SOURCE_REGISTRY_NAMES:
        for row in rows_by_registry.get(registry_name, []):
            annotated = dict(row)
            annotated["_source_registry"] = registry_name
            rows.append(annotated)
    return rows


def existing_by_id(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("object_id", ""): row for row in rows if row.get("object_id")}


def source_format(row: dict[str, str]) -> str:
    value = row.get("format", "")
    return value if value in {"markdown", "tex", "pdf", "html"} else "markdown"


def object_slug(object_id: str) -> str:
    return slugify(object_id)


def vault_note_relative_path(source_row: dict[str, str]) -> str:
    lane = source_format(source_row)
    return f"02_sources/{lane}/{object_slug(source_row['object_id'])}.md"


def vault_raw_relative_path(source_row: dict[str, str]) -> str:
    lane = source_format(source_row)
    source_path = Path(source_row.get("path", "source.txt"))
    suffix = source_path.suffix or ".txt"
    return f"01_raw/{lane}/{object_slug(source_row['object_id'])}{suffix}"


def vault_index_relative_path(source_row: dict[str, str]) -> str:
    lane = source_format(source_row)
    return f"03_indexes/by-format-{lane}.md"


def extracted_text_relative_path(source_row: dict[str, str]) -> str:
    lane = source_format(source_row)
    return f".local/content_semantics/{lane}/{object_slug(source_row['object_id'])}.txt"


def repo_relative_vault_path(repo_root: Path, vault: Path, relative: str) -> str:
    return rel_to_repo(repo_root, vault / relative)


def stable_time(
    existing_row: dict[str, str],
    new_row: dict[str, str],
    watched_fields: Iterable[str],
    field_name: str,
    now: str,
) -> str:
    if existing_row and all(existing_row.get(field, "") == new_row.get(field, "") for field in watched_fields):
        return existing_row.get(field_name, "") or now
    return now


def extract_markdown(path: Path) -> SemanticExtract:
    text = read_text(path)
    headings = [
        match.group(1).strip()
        for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text)
    ]
    links = [match.group(2).strip() for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text)]
    tags = [match.group(1) for match in re.finditer(r"(?<!\w)#([A-Za-z0-9_-]+)", text)]
    equation_count = text.count("$$") // 2 + len(re.findall(r"\$[^$\n]+\$", text))
    return SemanticExtract(
        text=text,
        status="PASS",
        extractor="markdown",
        headings=headings,
        links=links + [f"tag:{tag}" for tag in tags],
        equation_count=equation_count,
    )


def extract_tex(path: Path) -> SemanticExtract:
    text = read_text(path)
    headings = [
        match.group(2).strip()
        for match in re.finditer(r"\\(part|chapter|section|subsection|subsubsection)\*?\{([^{}]+)\}", text)
    ]
    labels = re.findall(r"\\label\{([^{}]+)\}", text)
    refs = re.findall(r"\\(?:eqref|ref|autoref|cref|Cref)\{([^{}]+)\}", text)
    citations = re.findall(r"\\(?:cite|citep|citet)\{([^{}]+)\}", text)
    equation_count = len(re.findall(r"\\begin\{(?:equation|align|gather|multline)\*?\}", text))
    equation_count += text.count("$$") // 2
    normalized = re.sub(r"%.*", "", text)
    normalized = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r"\1", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return SemanticExtract(
        text=f"{text}\n\n--- normalized prose proxy ---\n{normalized}\n",
        status="PASS",
        extractor="tex",
        headings=headings,
        labels=labels,
        refs=refs,
        citations=citations,
        equation_count=equation_count,
    )


def extract_pdf(path: Path) -> SemanticExtract:
    try:
        import fitz  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        return SemanticExtract(
            text="",
            status="DEPENDENCY_MISSING",
            extractor="pymupdf",
            error="PyMuPDF is not installed",
        )
    try:
        document = fitz.open(path)
    except Exception as exc:  # pragma: no cover - depends on external PDF state.
        return SemanticExtract(text="", status="FAIL", extractor="pymupdf", error=str(exc))

    pages: list[str] = []
    try:
        for index, page in enumerate(document, start=1):
            page_text = page.get_text("text").strip()
            pages.append(f"--- page {index} ---\n{page_text}")
        page_count = document.page_count
    finally:
        document.close()
    text = "\n\n".join(pages).strip() + "\n"
    return SemanticExtract(
        text=text,
        status="PASS" if text.strip() else "EMPTY",
        extractor="pymupdf",
        page_count=page_count,
    )


def extract_html(path: Path) -> SemanticExtract:
    parser = VisibleHTMLTextParser()
    raw = read_text(path)
    parser.feed(raw)
    text = html.unescape("\n".join(parser.text_chunks)).strip() + "\n"
    return SemanticExtract(
        text=text,
        status="PASS" if text.strip() else "EMPTY",
        extractor="html",
        headings=parser.headings,
        links=parser.links,
        html_title=" ".join(parser.title_chunks).strip(),
    )


def extract_content(repo_root: Path, source_row: dict[str, str]) -> SemanticExtract:
    path_text = source_row.get("path", "")
    path = repo_root / path_text
    if not path.exists():
        return SemanticExtract(text="", status="MISSING", extractor=source_format(source_row))
    lane = source_format(source_row)
    if lane == "markdown":
        return extract_markdown(path)
    if lane == "tex":
        return extract_tex(path)
    if lane == "pdf":
        return extract_pdf(path)
    if lane == "html":
        return extract_html(path)
    return SemanticExtract(text="", status="UNSUPPORTED", extractor=lane)


def generate_content_semantic_rows(
    repo_root: Path,
    rows_by_registry: dict[str, list[dict[str, str]]],
    now: str,
    write_text: bool,
) -> list[dict[str, str]]:
    existing = existing_by_id(read_csv_rows(registry_path(repo_root, "CONTENT_SEMANTIC_REGISTRY.csv")))
    output: list[dict[str, str]] = []
    for source_row in source_rows_with_registry(rows_by_registry):
        object_id = f"SEMANTIC-{source_row['object_id']}"
        extract = extract_content(repo_root, source_row)
        extracted_path = extracted_text_relative_path(source_row)
        if write_text and extract.status in {"PASS", "EMPTY"}:
            write_text_if_changed(repo_root / extracted_path, extract.text)
        row = {
            "object_id": object_id,
            "path": extracted_path,
            "format": "content_semantics",
            "role": "content_semantic_extract",
            "authority_status": "generated_noncanonical",
            "audience": "agents",
            "source_hash": extract.content_hash,
            "related_source": source_row["object_id"],
            "generated_from": source_row["object_id"],
            "generated_outputs": "",
            "owner_skill": "obsidian-wiki",
            "validation_status": "PASS" if extract.status in {"PASS", "EMPTY"} else "FAIL",
            "last_validated_at": now,
            "notes": extract.error or "Generated deterministic content semantics for local agent retrieval.",
            "source_object_id": source_row["object_id"],
            "source_registry": source_row["_source_registry"],
            "extractor": extract.extractor,
            "extraction_status": extract.status,
            "content_hash": extract.content_hash,
            "extracted_text_path": extracted_path,
            "content_chars": str(len(extract.text)),
            "page_count": str(extract.page_count),
            "headings": json_cell(extract.headings or []),
            "links": json_cell(extract.links or []),
            "labels": json_cell(extract.labels or []),
            "refs": json_cell(extract.refs or []),
            "citations": json_cell(extract.citations or []),
            "equation_count": str(extract.equation_count),
            "html_title": extract.html_title,
            "generated_at": now,
        }
        prior = existing.get(object_id, {})
        stable = stable_time(
            prior,
            row,
            ["content_hash", "extraction_status", "extracted_text_path"],
            "generated_at",
            now,
        )
        row["generated_at"] = stable
        row["last_validated_at"] = stable_time(
            prior,
            row,
            ["content_hash", "extraction_status", "extracted_text_path"],
            "last_validated_at",
            now,
        )
        output.append(row)
    output.sort(key=lambda row: row["object_id"])
    return output


def generate_obsidian_vault_rows(
    repo_root: Path,
    rows_by_registry: dict[str, list[dict[str, str]]],
    now: str,
    vault: Path | None = None,
) -> list[dict[str, str]]:
    existing = existing_by_id(read_csv_rows(registry_path(repo_root, "OBSIDIAN_VAULT_REGISTRY.csv")))
    vault_path = vault or vault_root(repo_root)
    output: list[dict[str, str]] = []
    for source_row in source_rows_with_registry(rows_by_registry):
        source_id = source_row["object_id"]
        object_id = f"VAULT-{source_id}"
        note_relative = vault_note_relative_path(source_row)
        raw_relative = vault_raw_relative_path(source_row)
        index_relative = vault_index_relative_path(source_row)
        attachment_relative = raw_relative if source_format(source_row) == "pdf" else ""
        row = {
            "object_id": object_id,
            "path": repo_relative_vault_path(repo_root, vault_path, note_relative),
            "format": "obsidian_note",
            "role": "generated_memory_note",
            "authority_status": "generated_noncanonical",
            "audience": "humans_and_agents",
            "source_hash": source_row.get("source_hash", ""),
            "related_source": source_id,
            "generated_from": source_id,
            "generated_outputs": "",
            "owner_skill": "obsidian-wiki",
            "validation_status": "PASS",
            "last_validated_at": now,
            "notes": "Generated local Obsidian memory note; not canonical authority.",
            "source_object_id": source_id,
            "source_registry": source_row["_source_registry"],
            "vault_root": rel_to_repo(repo_root, vault_path),
            "vault_note_path": repo_relative_vault_path(repo_root, vault_path, note_relative),
            "vault_raw_path": repo_relative_vault_path(repo_root, vault_path, raw_relative),
            "vault_attachment_path": (
                repo_relative_vault_path(repo_root, vault_path, attachment_relative)
                if attachment_relative
                else ""
            ),
            "vault_index_path": repo_relative_vault_path(repo_root, vault_path, index_relative),
            "sync_status": "local_generated",
            "synced_at": now,
        }
        prior = existing.get(object_id, {})
        row["synced_at"] = stable_time(
            prior,
            row,
            ["source_hash", "vault_note_path", "vault_raw_path"],
            "synced_at",
            now,
        )
        row["last_validated_at"] = stable_time(
            prior,
            row,
            ["source_hash", "vault_note_path", "vault_raw_path"],
            "last_validated_at",
            now,
        )
        output.append(row)
    output.sort(key=lambda row: row["object_id"])
    return output


def edge_object_id(
    source_id: str,
    target_id: str,
    relationship_type: str,
    evidence: str,
) -> str:
    payload = f"{source_id}|{target_id}|{relationship_type}|{evidence}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12].upper()
    return f"REL-{digest}-{slugify(relationship_type).upper()}"


def add_edge(
    rows: list[dict[str, str]],
    existing: dict[str, dict[str, str]],
    now: str,
    source_id: str,
    target_id: str,
    relationship_type: str,
    source_registry: str,
    source_field: str,
    source_path: str,
    target_path: str,
    evidence: str,
) -> None:
    object_id = edge_object_id(source_id, target_id, relationship_type, evidence)
    if any(row.get("object_id") == object_id for row in rows):
        return
    row = {
        "object_id": object_id,
        "path": "",
        "format": "relationship",
        "role": "object_relationship_edge",
        "authority_status": "generated_noncanonical",
        "audience": "agents",
        "source_hash": sha256_text(f"{source_id}|{target_id}|{relationship_type}|{evidence}"),
        "related_source": source_id,
        "generated_from": source_id,
        "generated_outputs": "",
        "owner_skill": "obsidian-wiki",
        "validation_status": "PASS",
        "last_validated_at": now,
        "notes": "Generated relationship edge for local agent graph traversal.",
        "edge_id": object_id,
        "source_object_id": source_id,
        "target_object_id": target_id,
        "relationship_type": relationship_type,
        "source_registry": source_registry,
        "source_field": source_field,
        "source_path": source_path,
        "target_path": target_path,
        "evidence": evidence,
        "generated_at": now,
    }
    prior = existing.get(object_id, {})
    row["generated_at"] = stable_time(prior, row, ["source_hash"], "generated_at", now)
    row["last_validated_at"] = stable_time(prior, row, ["source_hash"], "last_validated_at", now)
    rows.append(row)


def generate_relationship_rows(
    repo_root: Path,
    rows_by_registry: dict[str, list[dict[str, str]]],
    obsidian_rows: list[dict[str, str]],
    semantic_rows: list[dict[str, str]],
    now: str,
) -> list[dict[str, str]]:
    existing = existing_by_id(read_csv_rows(registry_path(repo_root, "OBJECT_RELATIONSHIP_REGISTRY.csv")))
    rows: list[dict[str, str]] = []
    sources = source_rows_with_registry(rows_by_registry)
    wiki_rows = rows_by_registry.get("WIKI_ARTIFACT_REGISTRY.csv", [])
    all_rows = sources + wiki_rows + obsidian_rows + semantic_rows
    id_lookup = existing_by_id(all_rows)
    path_lookup = {row.get("path", ""): row.get("object_id", "") for row in all_rows if row.get("path")}

    for source_row in sources:
        source_id = source_row["object_id"]
        source_registry = source_row["_source_registry"]
        source_path = source_row.get("path", "")
        for field_name, relationship_type in [
            ("related_source", "related_source"),
            ("generated_from", "generated_from"),
        ]:
            target_id = source_row.get(field_name, "")
            if target_id and target_id in id_lookup and target_id != source_id:
                add_edge(
                    rows,
                    existing,
                    now,
                    source_id,
                    target_id,
                    relationship_type,
                    source_registry,
                    field_name,
                    source_path,
                    id_lookup[target_id].get("path", ""),
                    target_id,
                )
        for output in [part.strip() for part in source_row.get("generated_outputs", "").split(";") if part.strip()]:
            target_id = output if output in id_lookup else path_lookup.get(output, "")
            add_edge(
                rows,
                existing,
                now,
                source_id,
                target_id,
                "generated_output",
                source_registry,
                "generated_outputs",
                source_path,
                id_lookup.get(target_id, {}).get("path", output),
                output,
            )
        for generated_rows, relationship_type in [
            (wiki_rows, "has_wiki_note"),
            (obsidian_rows, "has_vault_note"),
            (semantic_rows, "has_content_semantics"),
        ]:
            generated_row = next(
                (row for row in generated_rows if row.get("source_object_id") == source_id),
                None,
            )
            if generated_row:
                add_edge(
                    rows,
                    existing,
                    now,
                    source_id,
                    generated_row["object_id"],
                    relationship_type,
                    source_registry,
                    "generated",
                    source_path,
                    generated_row.get("path", ""),
                    generated_row["object_id"],
                )

    for semantic_row in semantic_rows:
        source_id = semantic_row.get("source_object_id", "")
        source_path = semantic_row.get("path", "")
        source_registry = semantic_row.get("source_registry", "")
        for field_name, relationship_type in [
            ("links", "content_link"),
            ("labels", "tex_label"),
            ("refs", "tex_ref"),
            ("citations", "tex_citation"),
        ]:
            try:
                values = json.loads(semantic_row.get(field_name, "[]"))
            except json.JSONDecodeError:
                values = []
            for value in values[:200]:
                add_edge(
                    rows,
                    existing,
                    now,
                    source_id,
                    "",
                    relationship_type,
                    source_registry,
                    field_name,
                    source_path,
                    "",
                    str(value),
                )

    rows.sort(key=lambda row: row["object_id"])
    return rows


def write_meta(repo_root: Path, name: str, inputs: list[Path], now: str) -> None:
    input_hashes = {
        rel_to_repo(repo_root, path): sha256_file(path)
        for path in inputs
        if path.exists() and path.is_file()
    }
    meta_path = repo_root / "registries" / f"{Path(name).stem}.meta.json"
    existing: dict[str, object] = {}
    if meta_path.exists():
        try:
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    generated_at = existing.get("generated_at", "")
    if existing.get("input_hashes") != input_hashes:
        generated_at = now
    if not generated_at:
        generated_at = now
    payload = {
        "registry": f"registries/{name}",
        "generator_command": ".venv/bin/python .codex/skills/project-memory-system/scripts/extract_content_semantics.py",
        "generated_at": generated_at,
        "input_hashes": input_hashes,
    }
    write_text_if_changed(meta_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_generated_registries(
    repo_root: Path,
    rows_by_registry: dict[str, list[dict[str, str]]] | None = None,
    now: str | None = None,
    write_semantic_text: bool = True,
    vault: Path | None = None,
) -> dict[str, list[dict[str, str]]]:
    now = now or utc_now()
    rows_by_registry = rows_by_registry or load_rows_by_registry(repo_root)
    obsidian_rows = generate_obsidian_vault_rows(repo_root, rows_by_registry, now, vault=vault)
    semantic_rows = generate_content_semantic_rows(
        repo_root, rows_by_registry, now, write_text=write_semantic_text
    )
    relationships = generate_relationship_rows(
        repo_root, rows_by_registry, obsidian_rows, semantic_rows, now
    )
    generated = {
        "OBSIDIAN_VAULT_REGISTRY.csv": obsidian_rows,
        "CONTENT_SEMANTIC_REGISTRY.csv": semantic_rows,
        "OBJECT_RELATIONSHIP_REGISTRY.csv": relationships,
    }
    ensure_directory(repo_root / "registries")
    for name, rows in generated.items():
        write_csv_if_changed(registry_path(repo_root, name), GENERATED_REGISTRY_COLUMNS[name], rows)
        input_paths = [registry_path(repo_root, source) for source in SOURCE_REGISTRY_NAMES]
        input_paths.append(registry_path(repo_root, "WIKI_ARTIFACT_REGISTRY.csv"))
        write_meta(repo_root, name, input_paths, now)
    return generated


def ensure_vault(repo_root: Path, vault: Path) -> None:
    for relative in VAULT_DIRECTORIES:
        ensure_directory(vault / relative)
    template_root = repo_root / TEMPLATE_ROOT_RELATIVE
    if template_root.exists():
        copy_template_tree(template_root, vault, overwrite=False)
    write_default_obsidian_config(vault)


def copy_template_tree(template_root: Path, vault: Path, overwrite: bool) -> None:
    for source in sorted(template_root.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(template_root)
        destination = vault / relative
        ensure_directory(destination.parent)
        if destination.exists() and not overwrite:
            continue
        shutil.copy2(source, destination)


def write_default_obsidian_config(vault: Path) -> None:
    app_json = "{}\n"
    core_plugins = {
        "backlink": True,
        "bookmarks": True,
        "canvas": True,
        "command-palette": True,
        "file-explorer": True,
        "global-search": True,
        "graph": True,
        "outline": True,
        "outgoing-link": True,
        "page-preview": True,
        "properties": True,
        "tag-pane": True,
        "templates": True,
    }
    write_text_if_changed(vault / ".obsidian" / "app.json", app_json)
    write_text_if_changed(
        vault / ".obsidian" / "core-plugins.json",
        json.dumps(core_plugins, indent=2, sort_keys=True) + "\n",
    )


def yaml_scalar(value: str) -> str:
    value = str(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def frontmatter(values: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in values.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_scalar(str(item))}")
        else:
            lines.append(f"{key}: {yaml_scalar(str(value))}")
    lines.append("---")
    return "\n".join(lines)


def vault_rel_from_repo_path(vault: Path, repo_relative_path: str) -> str:
    path = Path(repo_relative_path)
    try:
        return path.resolve().relative_to(vault.resolve()).as_posix()
    except ValueError:
        marker = ".local/obsidian/aether-flow-wiki/"
        text = path.as_posix()
        return text.split(marker, 1)[1] if marker in text else text


def note_target(vault: Path, repo_relative_path: str) -> str:
    relative = vault_rel_from_repo_path(vault, repo_relative_path)
    return relative[:-3] if relative.endswith(".md") else relative


def wiki_link(vault: Path, repo_relative_path: str, label: str) -> str:
    return f"[[{note_target(vault, repo_relative_path)}|{label}]]"


def source_note_text(
    vault: Path,
    source_row: dict[str, str],
    source_registry: str,
    obsidian_row: dict[str, str],
    semantic_row: dict[str, str] | None,
    relationships: list[dict[str, str]],
    object_to_vault: dict[str, dict[str, str]],
    manual_notes: str | None = None,
) -> str:
    related_ids = sorted(
        {
            row.get("target_object_id", "")
            for row in relationships
            if row.get("source_object_id") == source_row["object_id"]
        }
        | {
            row.get("source_object_id", "")
            for row in relationships
            if row.get("target_object_id") == source_row["object_id"]
        }
    )
    related_ids = [value for value in related_ids if value and value != source_row["object_id"]]
    semantic = semantic_row or {}
    fm = frontmatter(
        {
            "object_id": source_row["object_id"],
            "format": source_row.get("format", ""),
            "source_path": source_row.get("path", ""),
            "source_hash": source_row.get("source_hash", ""),
            "authority_status": source_row.get("authority_status", ""),
            "role": source_row.get("role", ""),
            "owner_skill": source_row.get("owner_skill", ""),
            "source_registry": source_registry,
            "vault_note_path": obsidian_row.get("vault_note_path", ""),
            "vault_raw_path": obsidian_row.get("vault_raw_path", ""),
            "content_hash": semantic.get("content_hash", ""),
            "extraction_status": semantic.get("extraction_status", ""),
            "related_object_ids": related_ids,
        }
    )
    relationship_lines: list[str] = []
    for row in relationships:
        if row.get("source_object_id") != source_row["object_id"]:
            continue
        target = row.get("target_object_id", "")
        target_note = object_to_vault.get(target, {})
        target_text = (
            wiki_link(vault, target_note.get("vault_note_path", ""), target)
            if target_note
            else (target or row.get("evidence", ""))
        )
        relationship_lines.append(
            f"- `{row.get('relationship_type', '')}` -> {target_text} ({row.get('evidence', '')})"
        )
    if not relationship_lines:
        relationship_lines.append("- None registered.")
    return "\n".join(
        [
            fm,
            "",
            f"# {source_row['object_id']}",
            "",
            "> Generated local Obsidian memory note. Not canonical authority. Verify source files and CSV registries before making project or scientific claims.",
            "",
            "## Source",
            "",
            f"- Source path: `{source_row.get('path', '')}`",
            f"- Source registry: `{source_registry}`",
            f"- Format: `{source_row.get('format', '')}`",
            f"- Authority status: `{source_row.get('authority_status', '')}`",
            f"- Raw mirror: `{vault_rel_from_repo_path(vault, obsidian_row.get('vault_raw_path', ''))}`",
            "",
            "## Content Semantics",
            "",
            f"- Extraction status: `{semantic.get('extraction_status', '')}`",
            f"- Extractor: `{semantic.get('extractor', '')}`",
            f"- Content hash: `{semantic.get('content_hash', '')}`",
            f"- Extracted text path: `{semantic.get('extracted_text_path', '')}`",
            f"- Character count: `{semantic.get('content_chars', '')}`",
            "",
            "## Relationships",
            "",
            *relationship_lines,
            "",
            manual_notes or default_manual_notes_block(),
            "",
        ]
    )


def default_manual_notes_block() -> str:
    return "\n".join([MANUAL_NOTES_START, DEFAULT_MANUAL_NOTES, MANUAL_NOTES_END])


def preserved_manual_notes(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(
        rf"{re.escape(MANUAL_NOTES_START)}\n(?P<body>.*?){re.escape(MANUAL_NOTES_END)}",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None
    body = match.group("body").rstrip("\n")
    return "\n".join([MANUAL_NOTES_START, body, MANUAL_NOTES_END])


def write_vault(
    repo_root: Path,
    vault: Path,
    rows_by_registry: dict[str, list[dict[str, str]]] | None = None,
) -> None:
    ensure_vault(repo_root, vault)
    rows_by_registry = rows_by_registry or load_rows_by_registry(repo_root)
    obsidian_rows = existing_by_id(rows_by_registry.get("OBSIDIAN_VAULT_REGISTRY.csv", []))
    semantic_by_source = {
        row.get("source_object_id", ""): row
        for row in rows_by_registry.get("CONTENT_SEMANTIC_REGISTRY.csv", [])
    }
    relationships = rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", [])
    object_to_vault = {
        row.get("source_object_id", ""): row
        for row in rows_by_registry.get("OBSIDIAN_VAULT_REGISTRY.csv", [])
    }

    manifest_entries: list[dict[str, str]] = []
    for source_row in source_rows_with_registry(rows_by_registry):
        obsidian_id = f"VAULT-{source_row['object_id']}"
        obsidian_row = obsidian_rows[obsidian_id]
        source_path = repo_root / source_row.get("path", "")
        raw_path = repo_root / obsidian_row["vault_raw_path"]
        note_path = repo_root / obsidian_row["vault_note_path"]
        if source_path.exists():
            ensure_directory(raw_path.parent)
            if not raw_path.exists() or sha256_file(raw_path) != sha256_file(source_path):
                shutil.copy2(source_path, raw_path)
        note_text = source_note_text(
            vault,
            source_row,
            source_row["_source_registry"],
            obsidian_row,
            semantic_by_source.get(source_row["object_id"]),
            relationships,
            object_to_vault,
            preserved_manual_notes(note_path),
        )
        write_text_if_changed(note_path, note_text)
        manifest_entries.append(
            {
                "object_id": source_row["object_id"],
                "source_path": source_row.get("path", ""),
                "vault_note_path": obsidian_row["vault_note_path"],
                "vault_raw_path": obsidian_row["vault_raw_path"],
            }
        )

    write_vault_indexes(repo_root, vault, rows_by_registry)
    write_text_if_changed(
        vault / "07_logs" / "sync_manifest.json",
        json.dumps({"entries": manifest_entries, "generated_at": utc_now()}, indent=2, sort_keys=True)
        + "\n",
    )


def write_vault_indexes(
    repo_root: Path,
    vault: Path,
    rows_by_registry: dict[str, list[dict[str, str]]],
) -> None:
    source_rows = source_rows_with_registry(rows_by_registry)
    obsidian_by_source = {
        row.get("source_object_id", ""): row
        for row in rows_by_registry.get("OBSIDIAN_VAULT_REGISTRY.csv", [])
    }
    for field_name, title, output_name in [
        ("format", "Index By Format", "by-format.md"),
        ("authority_status", "Index By Authority Status", "by-authority-status.md"),
        ("owner_skill", "Index By Owner Skill", "by-owner-skill.md"),
    ]:
        groups: dict[str, list[dict[str, str]]] = {}
        for row in source_rows:
            groups.setdefault(row.get(field_name, ""), []).append(row)
        lines = [f"# {title}", "", "Generated Obsidian index. Not canonical authority.", ""]
        for group in sorted(groups):
            lines.extend([f"## {group or 'blank'}", ""])
            for row in sorted(groups[group], key=lambda item: item["object_id"]):
                vault_row = obsidian_by_source.get(row["object_id"], {})
                link = wiki_link(vault, vault_row.get("vault_note_path", ""), row["object_id"])
                lines.append(f"- {link} `{row.get('path', '')}`")
            lines.append("")
        write_text_if_changed(vault / "03_indexes" / output_name, "\n".join(lines))

        if field_name == "format":
            for group, rows in groups.items():
                group_lines = [
                    f"# Index By Format: {group or 'blank'}",
                    "",
                    "Generated Obsidian index. Not canonical authority.",
                    "",
                ]
                for row in sorted(rows, key=lambda item: item["object_id"]):
                    vault_row = obsidian_by_source.get(row["object_id"], {})
                    link = wiki_link(vault, vault_row.get("vault_note_path", ""), row["object_id"])
                    group_lines.append(f"- {link} `{row.get('path', '')}`")
                group_lines.append("")
                write_text_if_changed(
                    vault / "03_indexes" / f"by-format-{slugify(group or 'blank')}.md",
                    "\n".join(group_lines),
                )

    relationship_lines = [
        "# Relationship Graph",
        "",
        "Generated relationship overview. Not canonical authority.",
        "",
    ]
    for row in rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", []):
        relationship_lines.append(
            f"- `{row.get('relationship_type', '')}` `{row.get('source_object_id', '')}` -> `{row.get('target_object_id', '')}` `{row.get('evidence', '')}`"
        )
    write_text_if_changed(vault / "04_relationships" / "relationship-graph.md", "\n".join(relationship_lines) + "\n")

    write_text_if_changed(
        vault / "00_control" / "README.md",
        "\n".join(
            [
                "# AEther Flow Local Memory Vault",
                "",
                "Generated local Obsidian retrieval layer. CSV registries and canonical source files remain authoritative.",
                "",
                "Use `query_memory.py lookup`, `query_memory.py search`, `query_memory.py related`, and `query_memory.py status` for local AI-agent access.",
                "",
            ]
        ),
    )
    write_text_if_changed(
        vault / "05_queries" / "query-examples.md",
        "\n".join(
            [
                "# Query Examples",
                "",
                "```zsh",
                ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json",
                ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY --json",
                ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py search \"Lorentzian metric\" --formats tex,pdf --limit 10 --json",
                "```",
                "",
            ]
        ),
    )
    write_text_if_changed(
        vault / "09_schema" / "source-note-schema.md",
        "\n".join(
            [
                "# Source Note Schema",
                "",
                "Required frontmatter: `object_id`, `format`, `source_path`, `source_hash`, `authority_status`, `role`, `owner_skill`, `source_registry`, `vault_note_path`, `vault_raw_path`, `content_hash`, `extraction_status`, and `related_object_ids`.",
                "",
            ]
        ),
    )


def lint_vault(repo_root: Path, vault: Path, require_index: bool = False) -> list[str]:
    issues: list[str] = []
    rows_by_registry = load_rows_by_registry(repo_root)
    if not vault.exists():
        return [f"Vault does not exist: {vault}"]
    source_rows = source_rows_with_registry(rows_by_registry)
    obsidian_by_source = {
        row.get("source_object_id", ""): row
        for row in rows_by_registry.get("OBSIDIAN_VAULT_REGISTRY.csv", [])
    }
    semantic_by_source = {
        row.get("source_object_id", ""): row
        for row in rows_by_registry.get("CONTENT_SEMANTIC_REGISTRY.csv", [])
    }
    for row in source_rows:
        source_id = row["object_id"]
        vault_row = obsidian_by_source.get(source_id)
        if not vault_row:
            issues.append(f"Missing vault registry row for {source_id}")
            continue
        note_path = repo_root / vault_row.get("vault_note_path", "")
        raw_path = repo_root / vault_row.get("vault_raw_path", "")
        source_path = repo_root / row.get("path", "")
        if not note_path.exists():
            issues.append(f"Missing vault note for {source_id}: {note_path}")
        elif f"object_id: \"{source_id}\"" not in note_path.read_text(encoding="utf-8", errors="replace"):
            issues.append(f"Vault note frontmatter missing object_id for {source_id}")
        if source_path.exists():
            if not raw_path.exists():
                issues.append(f"Missing raw vault mirror for {source_id}")
            elif sha256_file(raw_path) != sha256_file(source_path):
                issues.append(f"Stale raw vault mirror for {source_id}")
        index_path = repo_root / vault_row.get("vault_index_path", "")
        if not index_path.exists():
            issues.append(f"Missing declared vault index for {source_id}: {index_path}")
        semantic_row = semantic_by_source.get(source_id)
        if not semantic_row:
            issues.append(f"Missing semantic registry row for {source_id}")
        else:
            text_path = repo_root / semantic_row.get("extracted_text_path", "")
            if semantic_row.get("extraction_status") in {"PASS", "EMPTY"}:
                if not text_path.exists():
                    issues.append(f"Missing extracted semantic text for {source_id}")
                elif sha256_file(text_path) != semantic_row.get("content_hash", ""):
                    issues.append(f"Stale extracted semantic text for {source_id}")
    if require_index and not memory_index_path(repo_root).exists():
        issues.append("Memory SQLite index is missing")
    return issues


def registry_rows_for_index(repo_root: Path) -> list[tuple[str, dict[str, str]]]:
    rows_by_registry = load_rows_by_registry(repo_root)
    output: list[tuple[str, dict[str, str]]] = []
    for name, rows in rows_by_registry.items():
        for row in rows:
            output.append((name, row))
    return output


def build_memory_index(repo_root: Path, index_path: Path | None = None) -> Path:
    target = index_path or memory_index_path(repo_root)
    ensure_directory(target.parent)
    rows_by_registry = load_rows_by_registry(repo_root)
    registry_rows = registry_rows_for_index(repo_root)
    semantic_rows = rows_by_registry.get("CONTENT_SEMANTIC_REGISTRY.csv", [])
    relationships = rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", [])
    if target.exists():
        target.unlink()
    connection = sqlite3.connect(target)
    try:
        connection.execute(
            "CREATE TABLE objects (object_id TEXT PRIMARY KEY, registry_name TEXT, path TEXT, format TEXT, role TEXT, authority_status TEXT, row_json TEXT)"
        )
        connection.execute(
            "CREATE TABLE relationships (edge_id TEXT PRIMARY KEY, source_object_id TEXT, target_object_id TEXT, relationship_type TEXT, evidence TEXT, row_json TEXT)"
        )
        connection.execute(
            "CREATE TABLE content (object_id TEXT PRIMARY KEY, source_object_id TEXT, text_path TEXT, content_hash TEXT, extraction_status TEXT, text TEXT)"
        )
        connection.execute(
            "CREATE VIRTUAL TABLE docs_fts USING fts5(object_id UNINDEXED, title, body, format UNINDEXED, source_path UNINDEXED)"
        )
        for registry_name, row in registry_rows:
            object_id = row.get("object_id", "")
            if not object_id:
                continue
            connection.execute(
                "INSERT OR REPLACE INTO objects VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    object_id,
                    registry_name,
                    row.get("path", ""),
                    row.get("format", ""),
                    row.get("role", ""),
                    row.get("authority_status", ""),
                    json.dumps(row, sort_keys=True),
                ),
            )
            registry_body = json.dumps(row, sort_keys=True)
            connection.execute(
                "INSERT INTO docs_fts (object_id, title, body, format, source_path) VALUES (?, ?, ?, ?, ?)",
                (object_id, object_id, registry_body, row.get("format", ""), row.get("path", "")),
            )
        for row in semantic_rows:
            text_path = repo_root / row.get("extracted_text_path", "")
            text = text_path.read_text(encoding="utf-8", errors="replace") if text_path.exists() else ""
            connection.execute(
                "INSERT OR REPLACE INTO content VALUES (?, ?, ?, ?, ?, ?)",
                (
                    row.get("object_id", ""),
                    row.get("source_object_id", ""),
                    row.get("extracted_text_path", ""),
                    row.get("content_hash", ""),
                    row.get("extraction_status", ""),
                    text,
                ),
            )
            if text:
                connection.execute(
                    "INSERT INTO docs_fts (object_id, title, body, format, source_path) VALUES (?, ?, ?, ?, ?)",
                    (
                        row.get("source_object_id", ""),
                        row.get("source_object_id", ""),
                        text,
                        row.get("extractor", ""),
                        row.get("path", ""),
                    ),
                )
        for row in relationships:
            edge_id = row.get("edge_id", "") or row.get("object_id", "")
            connection.execute(
                "INSERT OR REPLACE INTO relationships VALUES (?, ?, ?, ?, ?, ?)",
                (
                    edge_id,
                    row.get("source_object_id", ""),
                    row.get("target_object_id", ""),
                    row.get("relationship_type", ""),
                    row.get("evidence", ""),
                    json.dumps(row, sort_keys=True),
                ),
            )
        connection.commit()
    finally:
        connection.close()
    return target


def lookup_object(repo_root: Path, identifier: str) -> dict[str, object]:
    rows_by_registry = load_rows_by_registry(repo_root)
    matches: list[tuple[str, dict[str, str]]] = []
    for registry_name, rows in rows_by_registry.items():
        for row in rows:
            candidates = {
                row.get("object_id", ""),
                row.get("path", ""),
            }
            if registry_name in {
                "WIKI_ARTIFACT_REGISTRY.csv",
                "OBSIDIAN_VAULT_REGISTRY.csv",
                "CONTENT_SEMANTIC_REGISTRY.csv",
            }:
                candidates.update(
                    {
                        row.get("source_object_id", ""),
                        row.get("source_path", ""),
                        row.get("vault_note_path", ""),
                        row.get("vault_raw_path", ""),
                    }
                )
            if registry_name == "OBJECT_RELATIONSHIP_REGISTRY.csv":
                candidates.add(row.get("edge_id", ""))
            if identifier in candidates:
                matches.append((registry_name, row))
    primary = matches[0] if matches else ("", {})
    object_id = primary[1].get("object_id", identifier)
    source_id = primary[1].get("source_object_id", object_id)
    relationships = [
        row
        for row in rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", [])
        if row.get("source_object_id") in {object_id, source_id}
        or row.get("target_object_id") in {object_id, source_id}
    ]
    return {
        "query": identifier,
        "match_count": len(matches),
        "primary_registry": primary[0],
        "primary_row": primary[1],
        "matches": [{"registry": name, "row": row} for name, row in matches],
        "relationships": relationships,
    }


def related_objects(repo_root: Path, object_id: str, depth: int) -> dict[str, object]:
    rows_by_registry = load_rows_by_registry(repo_root)
    edges = rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", [])
    seen = {object_id}
    frontier = {object_id}
    traversed: list[dict[str, str]] = []
    for _ in range(max(depth, 1)):
        next_frontier: set[str] = set()
        for edge in edges:
            source = edge.get("source_object_id", "")
            target = edge.get("target_object_id", "")
            if source in frontier or target in frontier:
                traversed.append(edge)
                for candidate in [source, target]:
                    if candidate and candidate not in seen:
                        seen.add(candidate)
                        next_frontier.add(candidate)
        frontier = next_frontier
        if not frontier:
            break
    return {"object_id": object_id, "depth": depth, "related_object_ids": sorted(seen), "edges": traversed}


def search_index(
    repo_root: Path,
    query: str,
    formats: set[str] | None,
    limit: int,
    index_path: Path | None = None,
) -> dict[str, object]:
    target = index_path or memory_index_path(repo_root)
    if not target.exists():
        return {"query": query, "error": f"memory index does not exist: {target}", "results": []}
    connection = sqlite3.connect(target)
    connection.row_factory = sqlite3.Row
    try:
        sql = (
            "SELECT object_id, title, snippet(docs_fts, 2, '[', ']', '...', 16) AS snippet, "
            "format, source_path, bm25(docs_fts) AS rank FROM docs_fts WHERE docs_fts MATCH ?"
        )
        params: list[object] = [query]
        if formats:
            placeholders = ",".join("?" for _ in formats)
            sql += f" AND format IN ({placeholders})"
            params.extend(sorted(formats))
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)
        rows = [dict(row) for row in connection.execute(sql, params)]
    finally:
        connection.close()
    return {"query": query, "results": rows}


def status(repo_root: Path, vault: Path | None = None, index_path: Path | None = None) -> dict[str, object]:
    vault_path = vault or vault_root(repo_root)
    index = index_path or memory_index_path(repo_root)
    rows_by_registry = load_rows_by_registry(repo_root)
    return {
        "vault_path": rel_to_repo(repo_root, vault_path) if vault_path.exists() else vault_path.as_posix(),
        "vault_exists": vault_path.exists(),
        "memory_index_path": rel_to_repo(repo_root, index) if index.exists() else index.as_posix(),
        "memory_index_exists": index.exists(),
        "source_object_count": len(source_rows_with_registry(rows_by_registry)),
        "vault_row_count": len(rows_by_registry.get("OBSIDIAN_VAULT_REGISTRY.csv", [])),
        "semantic_row_count": len(rows_by_registry.get("CONTENT_SEMANTIC_REGISTRY.csv", [])),
        "relationship_row_count": len(rows_by_registry.get("OBJECT_RELATIONSHIP_REGISTRY.csv", [])),
        "lint_issues": lint_vault(repo_root, vault_path) if vault_path.exists() else [],
    }
