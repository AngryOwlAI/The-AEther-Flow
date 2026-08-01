#!/usr/bin/env python3
"""Command-line entry point for shared validation planning and execution."""

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
    load_manifest,
    render_explanation,
)
from scripts.validation.profiles import ProfileError, resolve_profile  # noqa: E402
from scripts.validation.executor import ExecutorError, execute_plan  # noqa: E402
from scripts.validation.run import (  # noqa: E402
    DEFAULT_BINDINGS,
    DEFAULT_RECEIPT_ROOT,
    load_adapters,
)


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"


def add_planning_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the deterministic inputs shared by plan and run."""

    parser.add_argument("--profile", required=True, choices=sorted(PROFILES))
    parser.add_argument("--scope", action="append", default=[], choices=sorted(SCOPES))
    parser.add_argument("--role-obligation", action="append", default=[])
    parser.add_argument("--paths", nargs="*", help="use explicit repository-relative paths")
    parser.add_argument("--staged", action="store_true", help="derive staged paths only")
    parser.add_argument("--base-ref", default="HEAD")
    parser.add_argument("--no-untracked", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    plan = subcommands.add_parser("plan", help="build a deterministic validation plan")
    add_planning_arguments(plan)
    output = plan.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="emit deterministic JSON")
    output.add_argument("--explain", action="store_true", help="explain gate selection")

    run = subcommands.add_parser(
        "run", help="build and execute the selected profile through tracked adapters"
    )
    add_planning_arguments(run)
    run.add_argument("--adapter-bindings", type=Path, default=DEFAULT_BINDINGS)
    run.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPT_ROOT)
    run.add_argument("--max-workers", type=int, default=4)
    run.add_argument("--run-id")
    run.add_argument("--max-stabilization-passes", type=int, default=3)
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
        manifest = load_manifest(args.manifest)
        plan = resolve_profile(
            manifest,
            classification,
            requested_profile=args.profile,
            scopes=args.scope,
            role_obligations=args.role_obligation,
        ).plan
        if args.command == "run":
            accumulated_paths = set(str(path) for path in paths)
            known_tags = set(str(tag) for tag in classification["path_family_tags"])

            def replan_if_new_tags(new_paths: tuple[str, ...]):
                accumulated_paths.update(new_paths)
                updated_classification = classify_paths(sorted(accumulated_paths))
                updated_tags = set(
                    str(tag)
                    for tag in updated_classification["path_family_tags"]
                )
                if not updated_tags - known_tags:
                    return None
                known_tags.update(updated_tags)
                return resolve_profile(
                    manifest,
                    updated_classification,
                    requested_profile=args.profile,
                    scopes=args.scope,
                    role_obligations=args.role_obligation,
                ).plan

            gates = {
                str(gate["gate_id"]): gate
                for gate in manifest.get("gates", [])
                if isinstance(gate, dict) and gate.get("gate_id")
            }
            allowed_mutation_globs = tuple(
                sorted(
                    {
                        str(pattern)
                        for gate_id in plan.ordered_gate_ids
                        if gates[gate_id].get("mutating") is True
                        for pattern in gates[gate_id].get("output_globs", [])
                    }
                )
            )
            outcome = execute_plan(
                plan,
                manifest,
                load_adapters(args.adapter_bindings, manifest),
                receipt_root=args.receipt_root,
                max_workers=args.max_workers,
                run_id=args.run_id,
                mutation_root=REPO_ROOT if allowed_mutation_globs else None,
                allowed_mutation_globs=allowed_mutation_globs,
                max_stabilization_passes=args.max_stabilization_passes,
                replan_if_new_tags=replan_if_new_tags,
            )
    except (OSError, RuntimeError, PlannerError, ProfileError, ExecutorError) as error:
        print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
        return 2
    if args.command == "run":
        counts = outcome.receipt["counts"]
        receipt = (
            str(outcome.receipt_path)
            if outcome.receipt_path is not None
            else "unavailable"
        )
        print(
            f"{outcome.status} profile={plan.effective_profile} "
            f"gates={counts['gate_count']} pass={counts['pass_count']} "
            f"warn={counts['warn_count']} fail={counts['fail_count']} "
            f"blocked={counts['blocked_count']} receipt={receipt}"
        )
        if outcome.error:
            print(outcome.error, file=sys.stderr)
        return outcome.exit_code
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
