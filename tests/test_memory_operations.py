from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / ".codex/skills/project-memory-system/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from memory_operations import MemorySyncOperations, memory_sync  # noqa: E402


class MiniatureMemoryBackend:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.calls: list[str] = []

    def now(self) -> str:
        return "2026-07-15T00:00:00Z"

    def ensure_directories(self) -> None:
        self.calls.append("ensure_directories")
        (self.root / "registries").mkdir(parents=True, exist_ok=True)
        (self.root / "wiki/markdown").mkdir(parents=True, exist_ok=True)

    def discover_markdown_rows(self, _now: str) -> list[dict[str, str]]:
        self.calls.append("discover_markdown_rows")
        return [{"object_id": path.stem, "path": path.relative_to(self.root).as_posix()}
                for path in sorted((self.root / "sources").glob("*.md"))]

    def discover_tex_rows(self, _now: str) -> list[dict[str, str]]:
        self.calls.append("discover_tex_rows")
        return []

    def merge_authored_registry(
        self,
        name: str,
        _columns: list[str],
        rows: list[dict[str, str]],
        _refresh_existing: bool,
    ) -> list[dict[str, str]]:
        self.calls.append(f"merge:{name}")
        if name == "MARKDOWN_SOURCE_REGISTRY.csv":
            text = "\n".join(row["object_id"] for row in rows) + "\n"
            path = self.root / "registries" / name
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                path.write_text(text, encoding="utf-8")
        return rows

    def generate_pdf_rows(self, *_args, **_kwargs) -> list[dict[str, str]]:
        self.calls.append("generate_pdf_rows")
        return []

    def generate_html_rows(self, *_args) -> list[dict[str, str]]:
        self.calls.append("generate_html_rows")
        return []

    def generate_wiki(self, rows_by_registry, _now) -> list[dict[str, str]]:
        self.calls.append("generate_wiki")
        rows = rows_by_registry["MARKDOWN_SOURCE_REGISTRY.csv"]
        path = self.root / "wiki/markdown/generated.md"
        text = "\n".join(row["object_id"] for row in rows) + "\n"
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
        return [{"path": "wiki/markdown/generated.md"}]

    def generate_indexes(self, _rows_by_registry) -> None:
        self.calls.append("generate_indexes")

    def write_generated_registries(
        self,
        _repo_root,
        _rows_by_registry,
        _now,
        *,
        write_semantic_text: bool,
    ) -> dict[str, list[dict[str, str]]]:
        self.calls.append(f"local_retrieval:{write_semantic_text}")
        if write_semantic_text:
            path = self.root / ".local/content_semantics/source.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("source\n", encoding="utf-8")
        return {}

    def prune_stale_generated_files(
        self,
        _rows_by_registry,
        *,
        include_local_retrieval: bool,
    ) -> None:
        self.calls.append(f"prune:{include_local_retrieval}")
        stale = self.root / "wiki/markdown/stale.md"
        if stale.exists():
            stale.unlink()

    def generate_file_object_registry(self, *_args) -> list[dict[str, str]]:
        self.calls.append("generate_file_object_registry")
        return []

    def generate_folder_map(self, _rows_by_registry) -> None:
        self.calls.append("generate_folder_map")
        path = self.root / "FOLDER_MAP.md"
        if not path.exists():
            path.write_text("# Folders\n", encoding="utf-8")

    def operations(self) -> MemorySyncOperations:
        return MemorySyncOperations(
            now=self.now,
            ensure_directories=self.ensure_directories,
            discover_markdown_rows=self.discover_markdown_rows,
            discover_tex_rows=self.discover_tex_rows,
            merge_authored_registry=self.merge_authored_registry,
            generate_pdf_rows=self.generate_pdf_rows,
            generate_html_rows=self.generate_html_rows,
            generate_wiki=self.generate_wiki,
            generate_indexes=self.generate_indexes,
            write_generated_registries=self.write_generated_registries,
            prune_stale_generated_files=self.prune_stale_generated_files,
            generate_file_object_registry=self.generate_file_object_registry,
            generate_folder_map=self.generate_folder_map,
            markdown_columns=["object_id", "path"],
            tex_columns=["object_id", "path"],
        )


class MemoryOperationsTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> MiniatureMemoryBackend:
        (root / "sources").mkdir(parents=True)
        (root / "sources/source.md").write_text("# Source\n", encoding="utf-8")
        (root / "registries").mkdir()
        (root / "registries/MARKDOWN_SOURCE_REGISTRY.csv").write_text(
            "old\n", encoding="utf-8"
        )
        (root / "wiki/markdown").mkdir(parents=True)
        (root / "wiki/markdown/stale.md").write_text("stale\n", encoding="utf-8")
        return MiniatureMemoryBackend(root)

    def test_discovery_generation_pruning_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            backend = self.make_fixture(root)
            receipt = memory_sync(backend.operations(), repo_root=root)

        self.assertIn("registries/MARKDOWN_SOURCE_REGISTRY.csv", receipt.changed)
        self.assertIn("wiki/markdown/generated.md", receipt.created)
        self.assertIn("FOLDER_MAP.md", receipt.created)
        self.assertIn("wiki/markdown/stale.md", receipt.pruned)
        self.assertFalse(receipt.local_retrieval_enabled)
        self.assertNotIn("validate", " ".join(backend.calls))

    def test_second_synchronization_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            backend = self.make_fixture(root)
            memory_sync(backend.operations(), repo_root=root)
            receipt = memory_sync(backend.operations(), repo_root=root)

        self.assertFalse(receipt.mutated)
        self.assertEqual(receipt.changed, ())
        self.assertEqual(receipt.created, ())
        self.assertEqual(receipt.pruned, ())
        self.assertIn("wiki/markdown/generated.md", receipt.unchanged)

    def test_local_retrieval_generation_requires_explicit_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            backend = self.make_fixture(root)
            memory_sync(backend.operations(), repo_root=root)
            local_path = root / ".local/content_semantics/source.txt"
            self.assertFalse(local_path.exists())

            receipt = memory_sync(
                backend.operations(),
                repo_root=root,
                include_local_retrieval=True,
            )

        self.assertTrue(receipt.local_retrieval_enabled)
        self.assertIn(".local/content_semantics/source.txt", receipt.created)


if __name__ == "__main__":
    unittest.main()
