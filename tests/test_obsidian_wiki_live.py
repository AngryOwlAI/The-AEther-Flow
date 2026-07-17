from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / ".codex" / "skills" / "project-memory-system" / "scripts"
LIB_PATH = SCRIPT_DIR / "obsidian_wiki_lib.py"
FIXED_TIME = "2099-01-01T00:00:00Z"


def load_obsidian_wiki():
    spec = importlib.util.spec_from_file_location("obsidian_wiki_lib_live", LIB_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ObsidianWikiLiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obsidian = load_obsidian_wiki()

    def test_full_source_object_generation_and_search(self) -> None:
        rows_by_registry = self.obsidian.load_rows_by_registry(REPO_ROOT)
        source_rows = self.obsidian.source_rows_with_registry(rows_by_registry)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "full_source_mirror"
            registry_dir = root / "registries"
            registry_dir.mkdir(parents=True)
            for name in [
                *self.obsidian.SOURCE_REGISTRY_NAMES,
                "WIKI_ARTIFACT_REGISTRY.csv",
                "OBSIDIAN_VAULT_REGISTRY.csv",
                "CONTENT_SEMANTIC_REGISTRY.csv",
                "OBJECT_RELATIONSHIP_REGISTRY.csv",
            ]:
                shutil.copy2(REPO_ROOT / "registries" / name, registry_dir / name)

            for row in source_rows:
                source = REPO_ROOT / row["path"]
                self.assertTrue(source.is_file(), row["path"])
                destination = root / row["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    destination.symlink_to(source)

            generated = self.obsidian.write_generated_registries(
                root,
                rows_by_registry,
                FIXED_TIME,
                write_semantic_text=True,
            )
            index_path = root / ".local" / "memory_index" / "live.sqlite"
            self.obsidian.build_memory_index(root, index_path)
            payload = self.obsidian.search_index(
                root,
                "Lorentzian",
                None,
                10,
                index_path,
            )

        self.assertGreater(len(source_rows), 100)
        self.assertEqual(
            len(generated["OBSIDIAN_VAULT_REGISTRY.csv"]),
            len(source_rows),
        )
        self.assertEqual(
            len(generated["CONTENT_SEMANTIC_REGISTRY.csv"]),
            len(source_rows),
        )
        self.assertTrue(payload["results"])


if __name__ == "__main__":
    unittest.main()
