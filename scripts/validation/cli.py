#!/usr/bin/env python3
"""Command-line entry point for pure v19 validation planning."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.project_control.classify_project_changes import (  # noqa: E402
    changed_paths_from_git,
    classify_paths,
)
from scripts.validation.plan import (  # noqa: E402
    PROFILES,
    SCOPES,
    PlannerError,
    build_plan,
    load_manifest,
    render_explanation,
)


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    plan = subcommands.add_parser("plan", help="build a deterministic validation plan")
    plan.add_argument("--profile", required=True, choices=sorted(PROFILES))
    plan.add_argument("--scope", action="append", default=[], choices=sorted(SCOPES))
    plan.add_argument("--role-obligation", action="append", default=[])
    plan.add_argument("--paths", nargs="*", help="use explicit repository-relative paths")
    plan.add_argument("--staged", action="store_true", help="derive staged paths only")
    plan.add_argument("--base-ref", default="HEAD")
    plan.add_argument("--no-untracked", action="store_true")
    plan.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    output = plan.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="emit deterministic JSON")
    output.add_argument("--explain", action="store_true", help="explain gate selection")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        paths = args.paths
        if paths is None:
            paths = changed_paths_from_git(
                staged=args.staged,
                base_ref=args.base_ref,
                include_untracked=not args.no_untracked,
            )
        classification = classify_paths(paths)
        plan = build_plan(
            load_manifest(args.manifest),
            classification,
            profile=args.profile,
            scopes=args.scope,
            role_obligations=args.role_obligation,
        )
    except (OSError, RuntimeError, PlannerError) as error:
        print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
        return 2
    if args.explain:
        sys.stdout.write(render_explanation(plan))
    else:
        print(
            json.dumps(
                plan.to_dict(),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":") if args.json else None,
                indent=None if args.json else 2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
