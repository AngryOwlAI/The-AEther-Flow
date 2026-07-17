"""Raw input dependencies shared by support-traceability validators."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping


FileLoader = Callable[[Path], bytes]
HashProvider = Callable[[bytes], str]


def read_file_bytes(path: Path) -> bytes:
    """Read one raw file without interpreting its validation meaning."""

    return path.read_bytes()


def sha256_bytes(payload: bytes) -> str:
    """Return the content identity used by both traceability registries."""

    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class TraceabilityInputs:
    """Raw validator inputs; validation outcomes are deliberately not injectable."""

    repo_root: Path
    registry: Mapping[str, Any] | None = None
    file_loader: FileLoader = read_file_bytes
    hash_provider: HashProvider = sha256_bytes
    proof_normal_form_rows: Mapping[str, Mapping[str, str]] | None = None

    def path(self, rel_path: str) -> Path:
        return self.repo_root / rel_path

    def read_bytes(self, rel_path: str) -> bytes:
        return self.file_loader(self.path(rel_path))

    def read_text(self, rel_path: str) -> str:
        return self.read_bytes(rel_path).decode("utf-8")

    def sha256_file(self, rel_path: str) -> str:
        return self.hash_provider(self.read_bytes(rel_path))
