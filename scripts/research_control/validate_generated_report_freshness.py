#!/usr/bin/env python3
"""Validate provenance and freshness for every live generated report.

This is a project-control validator. A PASS means that the four registered
live views match their exact tracked inputs and remain within their permitted
commit lag. It does not make a generated view authoritative and does not
promote any scientific claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generated_report_provenance as report_provenance  # noqa: E402
import render_compact_current_frontier_v16 as compact_frontier  # noqa: E402
import render_current_frontier as current_frontier  # noqa: E402
import render_dependency_graph as dependency_graph  # noqa: E402
import render_task_index as task_index  # noqa: E402


SCHEMA_ID = "generated_report_freshness_validation_v1"


def _artifact_check(repo_root: Path, rel_path: str, expected: str) -> dict[str, Any]:
    path = repo_root / rel_path
    expected_hash = report_provenance.sha256_bytes(expected.encode("utf-8"))
    if not path.is_file():
        return {
            "path": rel_path,
            "status": "missing",
            "fresh": False,
            "expected_sha256": expected_hash,
            "actual_sha256": "",
        }
    actual = path.read_text(encoding="utf-8")
    return {
        "path": rel_path,
        "status": "fresh" if actual == expected else "stale",
        "fresh": actual == expected,
        "expected_sha256": expected_hash,
        "actual_sha256": report_provenance.sha256_bytes(actual.encode("utf-8")),
    }


def _evaluate(
    *,
    repo_root: Path,
    report_class: str,
    observed: dict[str, Any] | None,
    expected: dict[str, Any],
    outputs: dict[str, tuple[str, str]],
    strict: bool,
) -> dict[str, Any]:
    validation = report_provenance.validate_metadata(
        repo_root=repo_root,
        observed=observed or {},
        expected=expected,
        strict=strict,
    )
    artifacts = {
        name: _artifact_check(repo_root, rel_path, output_text)
        for name, (rel_path, output_text) in outputs.items()
    }
    fresh = all(item["fresh"] for item in artifacts.values())
    status = "PASS" if fresh and validation["status"] == "PASS" else "FAIL"
    return {
        "report_class": report_class,
        "status": status,
        "output_count": len(outputs),
        "artifacts": artifacts,
        "report_provenance": expected,
        "provenance_validation": validation,
        "generated_view_is_authority": False,
        "physics_promotion_authorized": False,
    }


def _current_frontier(repo_root: Path, strict: bool) -> dict[str, Any]:
    observed = report_provenance.metadata_from_markdown_file(
        repo_root, current_frontier.DEFAULT_FRONTIER_PATH
    )
    source_commit = report_provenance.source_commit_from_metadata(
        observed, report_provenance.git_head(repo_root)
    )
    payload, markdown = current_frontier.render_payload(
        repo_root,
        source_commit=source_commit,
        strict_provenance=strict,
    )
    return _evaluate(
        repo_root=repo_root,
        report_class="current_frontier",
        observed=observed,
        expected=payload["report_provenance"],
        outputs={"markdown": (current_frontier.DEFAULT_FRONTIER_PATH, markdown)},
        strict=strict,
    )


def _compact_frontier(repo_root: Path, strict: bool) -> dict[str, Any]:
    observed = report_provenance.metadata_from_json_file(
        repo_root, compact_frontier.DEFAULT_JSON_PATH
    )
    source_commit = report_provenance.source_commit_from_metadata(
        observed, report_provenance.git_head(repo_root)
    )
    snapshot = compact_frontier.build_snapshot(
        repo_root,
        source_commit=source_commit,
        strict_provenance=strict,
    )
    yaml_text, json_text, markdown = compact_frontier.rendered_texts(snapshot)
    return _evaluate(
        repo_root=repo_root,
        report_class="compact_current_frontier",
        observed=observed,
        expected=snapshot["report_provenance"],
        outputs={
            "yaml": (compact_frontier.DEFAULT_YAML_PATH, yaml_text),
            "json": (compact_frontier.DEFAULT_JSON_PATH, json_text),
            "markdown": (compact_frontier.DEFAULT_MARKDOWN_PATH, markdown),
        },
        strict=strict,
    )


def _task_index(repo_root: Path, strict: bool) -> dict[str, Any]:
    observed = report_provenance.metadata_from_markdown_file(
        repo_root, task_index.DEFAULT_MARKDOWN_PATH
    )
    source_commit = report_provenance.source_commit_from_metadata(
        observed, report_provenance.git_head(repo_root)
    )
    index = task_index.build_index(
        repo_root,
        source_commit=source_commit,
        strict_provenance=strict,
    )
    csv_text, markdown, wiki_markdown = task_index.rendered_texts(index)
    return _evaluate(
        repo_root=repo_root,
        report_class="research_task_index",
        observed=observed,
        expected=index["report_provenance"],
        outputs={
            "csv": (task_index.DEFAULT_CSV_PATH, csv_text),
            "markdown": (task_index.DEFAULT_MARKDOWN_PATH, markdown),
            "wiki_markdown": (task_index.DEFAULT_WIKI_MARKDOWN_PATH, wiki_markdown),
        },
        strict=strict,
    )


def _dependency_graph(repo_root: Path, strict: bool) -> dict[str, Any]:
    observed = report_provenance.metadata_from_json_file(
        repo_root, dependency_graph.DEFAULT_JSON_PATH
    )
    source_commit = report_provenance.source_commit_from_metadata(
        observed, report_provenance.git_head(repo_root)
    )
    snapshot = dependency_graph.load_graph_input_snapshot(
        repo_root,
        registry_paths=(f"registries/{name}" for name in dependency_graph.REGISTRY_SPECS),
    )
    graph = dependency_graph.build_graph(
        repo_root,
        snapshot=snapshot,
        source_commit=source_commit,
        strict_provenance=strict,
    )
    return _evaluate(
        repo_root=repo_root,
        report_class="research_dependency_graph",
        observed=observed,
        expected=dependency_graph.graph_report_provenance(graph),
        outputs={
            "json": (dependency_graph.DEFAULT_JSON_PATH, dependency_graph.render_json(graph)),
            "markdown": (
                dependency_graph.DEFAULT_MARKDOWN_PATH,
                dependency_graph.render_markdown(graph),
            ),
            "dot": (dependency_graph.DEFAULT_DOT_PATH, dependency_graph.render_dot(graph)),
        },
        strict=strict,
    )


def validate_live_reports(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    strict = repo_root == REPO_ROOT.resolve()
    evaluators: tuple[tuple[str, Callable[[Path, bool], dict[str, Any]]], ...] = (
        ("current_frontier", _current_frontier),
        ("compact_current_frontier", _compact_frontier),
        ("research_task_index", _task_index),
        ("research_dependency_graph", _dependency_graph),
    )
    reports: list[dict[str, Any]] = []
    for report_class, evaluator in evaluators:
        try:
            reports.append(evaluator(repo_root, strict))
        except (
            current_frontier.FrontierRenderError,
            compact_frontier.CompactFrontierError,
            task_index.TaskIndexError,
            dependency_graph.GraphError,
            report_provenance.GeneratedReportProvenanceError,
            OSError,
            ValueError,
        ) as exc:
            reports.append(
                {
                    "report_class": report_class,
                    "status": "FAIL",
                    "error": str(exc),
                    "generated_view_is_authority": False,
                    "physics_promotion_authorized": False,
                }
            )
    failures = [report["report_class"] for report in reports if report["status"] != "PASS"]
    return {
        "schema_id": SCHEMA_ID,
        "status": "PASS" if not failures else "FAIL",
        "policy_id": str(report_provenance.POLICY["policy_id"]),
        "report_count": len(reports),
        "failure_count": len(failures),
        "failed_report_classes": failures,
        "reports": reports,
        "operational_receipt_only": True,
        "generated_views_are_authority": False,
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit the full JSON receipt.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = validate_live_reports(Path(args.repo_root))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif report["status"] == "PASS":
        print(f"PASS live_generated_reports={report['report_count']}")
    else:
        failed = ",".join(report["failed_report_classes"])
        print(f"FAIL live_generated_reports={report['report_count']} failed={failed}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
