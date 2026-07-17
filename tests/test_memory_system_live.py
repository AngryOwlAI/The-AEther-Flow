from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / ".codex"
    / "skills"
    / "project-memory-system"
    / "scripts"
    / "bootstrap_memory_system.py"
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_snapshot() -> dict[str, str]:
    paths = [REPO_ROOT / "FOLDER_MAP.md"]
    paths.extend((REPO_ROOT / "registries").glob("*.csv"))
    paths.extend((REPO_ROOT / "registries").glob("*.json"))
    paths.extend((REPO_ROOT / "wiki").rglob("*.md"))
    return {
        path.relative_to(REPO_ROOT).as_posix(): file_hash(path)
        for path in sorted(paths)
        if path.exists()
    }


class MemorySystemLiveAcceptanceTests(unittest.TestCase):
    def test_validate_only_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--validate-only"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bootstrap_is_idempotent_for_generated_outputs(self) -> None:
        before = generated_snapshot()
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = generated_snapshot()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
