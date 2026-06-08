#!/usr/bin/env python3
"""Resolve the latest tracked research-control handoff."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from strict_yaml import StrictYamlError, load as load_yaml
except ImportError:  # pragma: no cover
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
HANDOFF_DIR = REPO_ROOT / "research_control" / "handoffs"
HANDOFF_RE = re.compile(r"handoff-(\d{4})\.yaml$")


def resolve_latest() -> dict[str, object]:
    candidates: list[tuple[int, Path]] = []
    for path in HANDOFF_DIR.glob("handoff-*.yaml"):
        match = HANDOFF_RE.fullmatch(path.name)
        if match:
            candidates.append((int(match.group(1)), path))
    if not candidates:
        raise FileNotFoundError("no tracked handoff YAML files found")
    number, yaml_path = sorted(candidates)[-1]
    markdown_path = yaml_path.with_suffix(".md")
    if not markdown_path.exists():
        raise FileNotFoundError(f"missing Markdown mirror for {yaml_path.name}")
    try:
        data = load_yaml(yaml_path)
    except StrictYamlError as exc:
        raise ValueError(f"{yaml_path.name}: {exc}") from exc
    return {
        "handoff_number": number,
        "handoff_id": data.get("handoff_id", yaml_path.stem),
        "yaml_path": yaml_path.relative_to(REPO_ROOT).as_posix(),
        "markdown_path": markdown_path.relative_to(REPO_ROOT).as_posix(),
        "task_id": data.get("task_id", ""),
        "job_id": data.get("job_id", ""),
        "next_action": data.get("next_action", ""),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = resolve_latest()
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Latest handoff: {result['yaml_path']}")
        print(f"Task: {result['task_id']}")
        print(f"Next action: {result['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
