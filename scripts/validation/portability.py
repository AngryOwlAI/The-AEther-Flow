#!/usr/bin/env python3
"""Prospective repository-relative path portability checks.

The policy is the shared implementation of the P10-T07 pilot rules.  It is
prospective only: it reports path spellings supplied by a caller and never
renames, truncates, deletes, or migrates repository content.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import Iterable

MAX_RELATIVE_PATH_CHARS = 180
MAX_RELATIVE_PATH_UTF8_BYTES = 220
MAX_COMPONENT_CHARS = 96
MAX_COMPONENT_UTF8_BYTES = 120
MAX_FILENAME_CHARS = 96
MAX_FILENAME_UTF8_BYTES = 120
POLICY = {
    "schema_id": "artifact_path_policy_v1",
    "max_relative_path_chars": MAX_RELATIVE_PATH_CHARS,
    "max_relative_path_utf8_bytes": MAX_RELATIVE_PATH_UTF8_BYTES,
    "max_component_chars": MAX_COMPONENT_CHARS,
    "max_component_utf8_bytes": MAX_COMPONENT_UTF8_BYTES,
    "max_filename_chars": MAX_FILENAME_CHARS,
    "max_filename_utf8_bytes": MAX_FILENAME_UTF8_BYTES,
    "normalization": "NFC",
    "separator": "/",
}
WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
WINDOWS_FORBIDDEN = set('<>:"\\|?*')


@dataclass(frozen=True, slots=True, order=True)
class PathFinding:
    """One deterministic portability finding."""

    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass(frozen=True, slots=True)
class CasefoldCollision:
    """Distinct spellings that collide after NFC normalization and casefolding."""

    paths: tuple[str, ...]
    code: str = "casefold_collision"

    def to_dict(self) -> dict[str, object]:
        return {"code": self.code, "paths": list(self.paths)}


def _finding(code: str, path: str, message: str) -> PathFinding:
    return PathFinding(code=code, path=path, message=message)


def lint_relative_path(path_text: object) -> tuple[PathFinding, ...]:
    """Return deterministic findings for one repository-relative path."""

    if not isinstance(path_text, str) or not path_text:
        return (
            _finding("empty_path", str(path_text), "path must be a nonempty string"),
        )

    findings: list[PathFinding] = []
    if path_text.startswith("/") or re.match(r"^[A-Za-z]:", path_text):
        findings.append(
            _finding("absolute_path", path_text, "path must be repository-relative")
        )
    if "\\" in path_text:
        findings.append(
            _finding("backslash_separator", path_text, "use POSIX forward slashes")
        )
    if unicodedata.normalize("NFC", path_text) != path_text:
        findings.append(_finding("non_nfc", path_text, "path must be Unicode NFC"))
    if len(path_text) > MAX_RELATIVE_PATH_CHARS:
        findings.append(
            _finding(
                "relative_path_chars",
                path_text,
                "repository-relative path is too long",
            )
        )
    if len(path_text.encode("utf-8")) > MAX_RELATIVE_PATH_UTF8_BYTES:
        findings.append(
            _finding(
                "relative_path_bytes",
                path_text,
                "repository-relative UTF-8 path is too long",
            )
        )

    components = path_text.split("/")
    for component in components:
        if component in {"", ".", ".."}:
            findings.append(
                _finding(
                    "unsafe_segment",
                    path_text,
                    f"unsafe path segment: {component!r}",
                )
            )
            continue
        if len(component) > MAX_COMPONENT_CHARS:
            findings.append(
                _finding(
                    "component_chars",
                    path_text,
                    f"component is too long: {component[:24]}",
                )
            )
        if len(component.encode("utf-8")) > MAX_COMPONENT_UTF8_BYTES:
            findings.append(
                _finding(
                    "component_bytes",
                    path_text,
                    f"component UTF-8 encoding is too long: {component[:24]}",
                )
            )
        if component.endswith((" ", ".")):
            findings.append(
                _finding(
                    "trailing_space_or_period",
                    path_text,
                    f"component has unsafe trailing character: {component!r}",
                )
            )
        if any(ord(character) < 32 or ord(character) == 127 for character in component):
            findings.append(
                _finding(
                    "control_character",
                    path_text,
                    "component contains a control character",
                )
            )
        forbidden = sorted(
            {character for character in component if character in WINDOWS_FORBIDDEN}
        )
        if forbidden:
            findings.append(
                _finding(
                    "windows_forbidden_character",
                    path_text,
                    f"component contains forbidden characters: {''.join(forbidden)}",
                )
            )
        stem = component.split(".", 1)[0].casefold()
        if stem in WINDOWS_RESERVED:
            findings.append(
                _finding(
                    "windows_reserved_name",
                    path_text,
                    f"reserved Windows device name: {component}",
                )
            )

    filename = components[-1] if components else ""
    if len(filename) > MAX_FILENAME_CHARS:
        findings.append(_finding("filename_chars", path_text, "filename is too long"))
    if len(filename.encode("utf-8")) > MAX_FILENAME_UTF8_BYTES:
        findings.append(
            _finding(
                "filename_bytes",
                path_text,
                "filename UTF-8 encoding is too long",
            )
        )
    return tuple(sorted(findings))


def casefold_collisions(paths: Iterable[str]) -> tuple[CasefoldCollision, ...]:
    """Return collisions after NFC normalization and Unicode casefolding."""

    buckets: dict[str, list[str]] = {}
    for path_text in paths:
        key = unicodedata.normalize("NFC", path_text).casefold()
        buckets.setdefault(key, []).append(path_text)
    return tuple(
        CasefoldCollision(tuple(sorted(values)))
        for _, values in sorted(buckets.items())
        if len(set(values)) > 1
    )


def evaluate_paths(paths: Iterable[str]) -> dict[str, object]:
    """Evaluate a bounded path set and return a deterministic compact receipt."""

    selected_paths = tuple(sorted(set(paths)))
    findings = tuple(
        finding
        for path_text in selected_paths
        for finding in lint_relative_path(path_text)
    )
    collisions = casefold_collisions(selected_paths)
    status = "FAIL" if findings or collisions else "PASS"
    return {
        "schema_id": "path_portability_receipt_v1",
        "status": status,
        "exit_code": 1 if status == "FAIL" else 0,
        "path_count": len(selected_paths),
        "finding_count": len(findings),
        "collision_count": len(collisions),
        "paths": list(selected_paths),
        "findings": [finding.to_dict() for finding in findings],
        "collisions": [collision.to_dict() for collision in collisions],
        "policy": dict(POLICY),
        "authority": {
            "prospective_only": True,
            "historical_paths_changed": False,
            "source_authoritative": False,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="repository-relative path to evaluate; repeat for collision checks",
    )
    parser.add_argument("--json", action="store_true", help="emit compact JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    receipt = evaluate_paths(args.path)
    if args.json:
        print(
            json.dumps(
                receipt,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    else:
        print(
            f"{receipt['status']} paths={receipt['path_count']} "
            f"findings={receipt['finding_count']} "
            f"collisions={receipt['collision_count']}"
        )
    return 1 if receipt["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
