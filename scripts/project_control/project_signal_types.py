#!/usr/bin/env python3
"""Read canonical project-improvement signal-type metadata."""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNAL_TYPE_REGISTRY_NAME = "PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
SIGNAL_TYPE_COLUMNS = (
    "signal_type",
    "default_recommended_skill",
    "default_recommended_role",
    "status",
    "notes",
)
ACTIVE_STATUSES = {"active"}


def registry_path(repo_root: Path = REPO_ROOT) -> Path:
    return repo_root / "registries" / SIGNAL_TYPE_REGISTRY_NAME


def read_signal_type_rows(repo_root: Path = REPO_ROOT) -> list[dict[str, str]]:
    path = registry_path(repo_root)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def active_signal_type_rows(repo_root: Path = REPO_ROOT) -> list[dict[str, str]]:
    return [
        row
        for row in read_signal_type_rows(repo_root)
        if row.get("status") in ACTIVE_STATUSES
    ]


def signal_type_names(repo_root: Path = REPO_ROOT) -> set[str]:
    return {
        row.get("signal_type", "")
        for row in active_signal_type_rows(repo_root)
        if row.get("signal_type")
    }


def signal_type_role_map(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    return {
        row.get("signal_type", ""): row.get("default_recommended_role", "")
        for row in active_signal_type_rows(repo_root)
        if row.get("signal_type") and row.get("default_recommended_role")
    }


def signal_type_skill_map(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    return {
        row.get("signal_type", ""): row.get("default_recommended_skill", "")
        for row in active_signal_type_rows(repo_root)
        if row.get("signal_type") and row.get("default_recommended_skill")
    }
