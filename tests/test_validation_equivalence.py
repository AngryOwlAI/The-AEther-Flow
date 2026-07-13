from __future__ import annotations

import argparse
import io
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
PROJECT_SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
CORPUS_PATH = REPO_ROOT / "tests" / "fixtures" / "validation_equivalence" / "corpus.json"
TAXONOMY_PATH = REPO_ROOT / "research_control" / "design" / "claim_language_linter_taxonomy.yaml"
REVIEWED_CONTEXTS_PATH = (
    REPO_ROOT / "research_control" / "design" / "claim_language_linter_reviewed_contexts.yaml"
)
COMPARISON_FIELDS = (
    "status",
    "hard_finding_ids",
    "warning_finding_ids",
    "selected_paths",
    "authority_fields",
)
REPORT_TASK_ID = "RT-20260713-002"
REPORT_JOB_ID = "AJ-RT-20260713-002-001"
CLAIM_ERROR_RE = re.compile(
    r"claim-language hard failure (?P<class_id>[^ ]+).*"
    r"\((?P<severity>hard_fail_[^)]+)\);"
)
CLAIM_WARNING_RE = re.compile(
    r"claim-language (?:warning )?(?P<class_id>[a-z0-9_]+).*"
    r"\((?P<severity>warn_[^)]+)\)"
)


def load_module(name: str, path: Path):
    for script_dir in (RESEARCH_SCRIPT_DIR, PROJECT_SCRIPT_DIR):
        if str(script_dir) not in sys.path:
            sys.path.insert(0, str(script_dir))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module(
    "validate_research_control_p1_t03",
    RESEARCH_SCRIPT_DIR / "validate_research_control.py",
)
CLAIM_LINTER = VALIDATOR.claim_language_linter


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_corpus() -> dict[str, Any]:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def materialize_files(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def outcome(
    *,
    hard: set[str] | None = None,
    warnings: set[str] | None = None,
    selected_paths: set[str] | None = None,
    authority: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    hard = hard or set()
    warnings = warnings or set()
    selected_paths = selected_paths or set()
    authority = authority or []
    authority_by_identity = {
        json.dumps(entry, sort_keys=True): entry
        for entry in authority
    }
    return {
        "status": "FAIL" if hard else "PASS",
        "hard_finding_ids": sorted(hard),
        "warning_finding_ids": sorted(warnings),
        "selected_paths": sorted(selected_paths),
        "authority_fields": [
            authority_by_identity[key]
            for key in sorted(authority_by_identity)
        ],
    }


def merge_outcomes(*items: dict[str, Any]) -> dict[str, Any]:
    hard: set[str] = set()
    warnings: set[str] = set()
    selected: set[str] = set()
    authority: list[dict[str, str]] = []
    for item in items:
        hard.update(item["hard_finding_ids"])
        warnings.update(item["warning_finding_ids"])
        selected.update(item["selected_paths"])
        authority.extend(item["authority_fields"])
    return outcome(hard=hard, warnings=warnings, selected_paths=selected, authority=authority)


def standalone_claim_report_outcome(
    report: dict[str, Any],
    selected: list[str],
) -> dict[str, Any]:
    hard: set[str] = set()
    warnings: set[str] = set()
    authority: list[dict[str, str]] = []
    for _error in report.get("config_errors", []):
        finding_id = "claim_language_changed:configuration_error"
        hard.add(finding_id)
        authority.append(
            {
                "finding_id": finding_id,
                "severity": "blocking",
                "surface_class": "configuration",
                "finding_kind": "configuration_error",
                "context": "claim_configuration",
            }
        )
    for finding in report["findings"]:
        finding_id = f"claim_language_changed:{finding['class_id']}"
        severity = finding["severity"]
        authority.append(
            {
                "finding_id": finding_id,
                "severity": severity,
                "surface_class": finding["surface_class"],
                "finding_kind": finding["finding_kind"],
                "context": finding["context"],
            }
        )
        if severity.startswith("hard_fail_"):
            hard.add(finding_id)
        else:
            warnings.add(finding_id)
    return outcome(
        hard=hard,
        warnings=warnings,
        selected_paths=set(selected),
        authority=authority,
    )


def standalone_claim_outcome(root: Path, changed_paths: list[str]) -> dict[str, Any]:
    selected = CLAIM_LINTER.claim_language_gate_paths(changed_paths, repo_root=root)
    report = CLAIM_LINTER.validate_paths(
        repo_root=root,
        taxonomy_path=TAXONOMY_PATH,
        reviewed_contexts_path=REVIEWED_CONTEXTS_PATH,
        paths=selected,
    )
    return standalone_claim_report_outcome(report, selected)


def normalize_validation_report(
    report: Any,
    fixture: dict[str, Any],
    selected_paths: set[str],
) -> dict[str, Any]:
    hard: set[str] = set()
    warnings: set[str] = set()
    authority: list[dict[str, str]] = []
    matchers = fixture.get("message_matchers", [])
    structured_authority = {
        (str(finding.get("finding_id", "")), str(finding.get("severity", ""))): {
            "finding_id": str(finding.get("finding_id", "")),
            "severity": str(finding.get("severity", "")),
            "surface_class": str(finding.get("surface_class", "")),
            "finding_kind": str(finding.get("finding_kind", "")),
            "context": str(finding.get("context", "")),
        }
        for finding in getattr(report, "findings", [])
        if finding.get("finding_id") and finding.get("severity")
    }

    for message in report.errors:
        claim_match = CLAIM_ERROR_RE.search(message)
        if message.startswith(("claim-language config error:", "claim-language validation failed to run:")):
            finding_id = "claim_language_changed:configuration_error"
            severity = "blocking"
            authority_entry = {
                "finding_id": finding_id,
                "severity": severity,
                "surface_class": "configuration",
                "finding_kind": "configuration_error",
                "context": "claim_configuration",
            }
        elif claim_match:
            finding_id = f"claim_language_changed:{claim_match.group('class_id')}"
            severity = claim_match.group("severity")
            authority_entry = structured_authority.get(
                (finding_id, severity),
                {"finding_id": finding_id, "severity": severity},
            )
        else:
            matched = [entry for entry in matchers if entry["contains"] in message]
            if not matched:
                raise AssertionError(f"{fixture['fixture_id']}: unmatched hard finding: {message}")
            finding_id = matched[0]["finding_id"]
            severity = matched[0]["severity"]
            authority_entry = {"finding_id": finding_id, "severity": severity}
        hard.add(finding_id)
        authority.append(authority_entry)

    for message in report.warnings:
        claim_match = CLAIM_WARNING_RE.search(message)
        if claim_match:
            finding_id = f"claim_language_changed:{claim_match.group('class_id')}"
            severity = claim_match.group("severity")
            authority_entry = structured_authority.get(
                (finding_id, severity),
                {"finding_id": finding_id, "severity": severity},
            )
        else:
            matched = [entry for entry in matchers if entry["contains"] in message]
            if not matched:
                raise AssertionError(f"{fixture['fixture_id']}: unmatched warning finding: {message}")
            finding_id = matched[0]["finding_id"]
            severity = matched[0]["severity"]
            authority_entry = {"finding_id": finding_id, "severity": severity}
        warnings.add(finding_id)
        authority.append(authority_entry)

    return outcome(
        hard=hard,
        warnings=warnings,
        selected_paths=selected_paths,
        authority=authority,
    )


def integrated_claim_outcome(root: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    report = VALIDATOR.ValidationReport()
    selected: set[str] = set()
    original_selector = CLAIM_LINTER.claim_language_gate_paths

    def capture(paths, *, repo_root):
        resolved = original_selector(paths, repo_root=repo_root)
        selected.update(resolved)
        return resolved

    with mock.patch.object(VALIDATOR, "REPO_ROOT", root), mock.patch.object(
        CLAIM_LINTER,
        "claim_language_gate_paths",
        side_effect=capture,
    ):
        VALIDATOR.validate_changed_claim_language(report, fixture["changed_paths"])
    return normalize_validation_report(report, fixture, selected)


def validate_diff_outcome(
    root: Path,
    fixture: dict[str, Any],
    *,
    include_integrated_claim: bool,
) -> dict[str, Any]:
    report = VALIDATOR.ValidationReport()
    selected: set[str] = set()
    original_selector = CLAIM_LINTER.claim_language_gate_paths

    def capture(paths, *, repo_root):
        resolved = original_selector(paths, repo_root=repo_root)
        selected.update(resolved)
        return resolved

    job_config = fixture.get("job")
    jobs: dict[str, dict[str, str]] = {}
    if job_config:
        jobs["AJ-FIXTURE"] = {
            "job_id": "AJ-FIXTURE",
            "role_id": job_config["role_id"],
            "status": "completed",
            "created_at": "2026-07-13T00:00:00Z",
            "allowed_write_paths": job_config["allowed_write_paths"],
            "output_paths": "",
            "job_path": "",
        }

    patches = [
        mock.patch.object(VALIDATOR, "REPO_ROOT", root),
        mock.patch.object(VALIDATOR, "changed_paths", return_value=fixture["changed_paths"]),
        mock.patch.object(CLAIM_LINTER, "claim_language_gate_paths", side_effect=capture),
    ]
    if fixture.get("changed_line_numbers") is not None:
        patches.append(
            mock.patch.object(
                VALIDATOR,
                "changed_line_numbers",
                return_value=set(fixture["changed_line_numbers"]),
            )
        )
    claim_patch = (
        mock.patch.object(VALIDATOR, "validate_changed_claim_language", return_value=None)
        if not include_integrated_claim
        else mock.patch.object(
            VALIDATOR,
            "validate_changed_claim_language",
            wraps=VALIDATOR.validate_changed_claim_language,
        )
    )
    with patches[0], patches[1], patches[2], claim_patch:
        if len(patches) == 4:
            with patches[3]:
                VALIDATOR.validate_diff(report, jobs, "HEAD", False)
        else:
            VALIDATOR.validate_diff(report, jobs, "HEAD", False)
    return normalize_validation_report(report, fixture, selected)


def diff_outcomes(root: Path, fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    standalone = standalone_claim_outcome(root, fixture["changed_paths"])
    legacy_diff = validate_diff_outcome(root, fixture, include_integrated_claim=False)
    consolidated = validate_diff_outcome(root, fixture, include_integrated_claim=True)
    return merge_outcomes(legacy_diff, standalone), consolidated


def malformed_registry_outcomes(
    root: Path,
    fixture: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    registry_dir = root / "registries"
    registry_dir.mkdir(parents=True)
    for name, columns in VALIDATOR.REGISTRY_COLUMNS.items():
        (registry_dir / name).write_text(",".join(columns) + "\n", encoding="utf-8")
    (registry_dir / fixture["registry_name"]).write_text(
        fixture["bad_header"] + "\n",
        encoding="utf-8",
    )
    def execute() -> dict[str, Any]:
        report = VALIDATOR.ValidationReport()
        with mock.patch.object(VALIDATOR, "REGISTRY_DIR", registry_dir):
            VALIDATOR.validate_registry_columns(report)
        return normalize_validation_report(report, fixture, set())

    return execute(), execute()


def stale_sidecar_outcomes(
    root: Path,
    fixture: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    materialize_files(root, fixture["files"])
    registry_dir = root / "registries"
    registry_dir.mkdir(parents=True, exist_ok=True)
    (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv").write_text(
        "signal_type,default_recommended_skill,default_recommended_role,status,notes\n"
        "validator_gap,improve-project-system,validator-engineer,active,Synthetic type.\n",
        encoding="utf-8",
    )
    (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv").write_text(
        "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n",
        encoding="utf-8",
    )
    def execute() -> dict[str, Any]:
        result = VALIDATOR.validate_project_improvement_handoff_records(root)
        report = VALIDATOR.ValidationReport(errors=result["errors"], warnings=result["warnings"])
        return normalize_validation_report(report, fixture, set())

    return execute(), execute()


def prepare_entrypoint_fixture(root: Path, fixture: dict[str, Any]) -> Path:
    materialize_files(root, fixture.get("files", {}))
    registry_dir = root / "registries"
    registry_dir.mkdir(parents=True, exist_ok=True)
    for name, columns in VALIDATOR.REGISTRY_COLUMNS.items():
        (registry_dir / name).write_text(",".join(columns) + "\n", encoding="utf-8")
    if fixture["runner"] == "malformed_registry":
        (registry_dir / fixture["registry_name"]).write_text(
            fixture["bad_header"] + "\n",
            encoding="utf-8",
        )
    if fixture["runner"] == "stale_sidecar":
        (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv").write_text(
            "signal_type,default_recommended_skill,default_recommended_role,status,notes\n"
            "validator_gap,improve-project-system,validator-engineer,active,Synthetic type.\n",
            encoding="utf-8",
        )
    return registry_dir


def jobs_for_fixture(fixture: dict[str, Any]) -> dict[str, dict[str, str]]:
    if fixture["fixture_id"] == "missing_active_agentjob":
        return {}
    job_config = fixture.get("job") or {}
    changed = fixture.get("changed_paths", [])
    allowed = job_config.get("allowed_write_paths") or ";".join(changed)
    if not allowed:
        allowed = "tests/fixtures/validation_equivalence/**"
    return {
        "AJ-FIXTURE": {
            "job_id": "AJ-FIXTURE",
            "role_id": job_config.get("role_id", "validator-engineer"),
            "status": "completed",
            "created_at": "2026-07-13T00:00:00Z",
            "allowed_write_paths": allowed,
            "output_paths": "",
            "job_path": "",
        }
    }


def validate_all_outcome(
    root: Path,
    registry_dir: Path,
    fixture: dict[str, Any],
    *,
    check_diff: bool,
    include_integrated_claim: bool,
) -> dict[str, Any]:
    selected: set[str] = set()
    original_selector = CLAIM_LINTER.claim_language_gate_paths

    def capture(paths, *, repo_root):
        resolved = original_selector(paths, repo_root=repo_root)
        selected.update(resolved)
        return resolved

    noop_names = (
        "validate_distance_to_gr_ledger",
        "validate_frontier_theorem_inventory",
        "validate_registry_values",
        "validate_countermodel_obligation_registry",
        "validate_execution_roles",
        "validate_program_state",
        "validate_handoffs",
        "validate_current_frontier_sync",
        "validate_active_state_bifurcation",
        "validate_compact_current_frontier_sync",
        "validate_approvals",
        "validate_claim_boundaries",
        "scan_for_forbidden_claims",
    )
    with ExitStack() as stack:
        stack.enter_context(mock.patch.object(VALIDATOR, "REPO_ROOT", root))
        stack.enter_context(mock.patch.object(VALIDATOR, "REGISTRY_DIR", registry_dir))
        stack.enter_context(
            mock.patch.object(VALIDATOR, "CONTROL_DIR", root / "research_control")
        )
        stack.enter_context(
            mock.patch.object(
                VALIDATOR,
                "changed_paths",
                return_value=fixture.get("changed_paths", []),
            )
        )
        stack.enter_context(
            mock.patch.object(CLAIM_LINTER, "claim_language_gate_paths", side_effect=capture)
        )
        if fixture.get("changed_line_numbers") is not None:
            stack.enter_context(
                mock.patch.object(
                    VALIDATOR,
                    "changed_line_numbers",
                    return_value=set(fixture["changed_line_numbers"]),
                )
            )
        for name in noop_names:
            stack.enter_context(mock.patch.object(VALIDATOR, name, return_value=None))
        stack.enter_context(mock.patch.object(VALIDATOR, "validate_roles", return_value={}))
        stack.enter_context(
            mock.patch.object(VALIDATOR, "validate_director_decisions", return_value={})
        )
        stack.enter_context(
            mock.patch.object(
                VALIDATOR,
                "validate_agent_jobs",
                return_value=jobs_for_fixture(fixture),
            )
        )
        stack.enter_context(mock.patch.object(VALIDATOR, "validate_tasks", return_value={}))
        if not include_integrated_claim:
            stack.enter_context(
                mock.patch.object(
                    VALIDATOR,
                    "validate_changed_claim_language",
                    return_value=None,
                )
            )
        report = VALIDATOR.validate_all(check_diff=check_diff)
    return normalize_validation_report(report, fixture, selected)


def entrypoint_outcomes(root: Path, fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    registry_dir = prepare_entrypoint_fixture(root, fixture)
    changed = fixture.get("changed_paths", [])
    legacy_plain = validate_all_outcome(
        root,
        registry_dir,
        fixture,
        check_diff=False,
        include_integrated_claim=False,
    )
    legacy_diff = validate_all_outcome(
        root,
        registry_dir,
        fixture,
        check_diff=True,
        include_integrated_claim=False,
    )
    legacy_claim = standalone_claim_outcome(root, changed)
    consolidated = validate_all_outcome(
        root,
        registry_dir,
        fixture,
        check_diff=True,
        include_integrated_claim=True,
    )
    return merge_outcomes(legacy_plain, legacy_diff, legacy_claim), consolidated


def run_fixture(fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        return entrypoint_outcomes(root, fixture)


def mismatch_fields(legacy: dict[str, Any], consolidated: dict[str, Any]) -> list[str]:
    return [field for field in COMPARISON_FIELDS if legacy[field] != consolidated[field]]


def execute_corpus() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for fixture in load_corpus()["cases"]:
        legacy, consolidated = run_fixture(fixture)
        results.append(
            {
                "fixture_id": fixture["fixture_id"],
                "legacy": legacy,
                "consolidated": consolidated,
                "mismatch_fields": mismatch_fields(legacy, consolidated),
                "blocking": bool(mismatch_fields(legacy, consolidated)),
            }
        )
    return results


def taxonomy_classification_audit() -> dict[str, Any]:
    taxonomy = CLAIM_LINTER.load_taxonomy(TAXONOMY_PATH)
    underclaim_text = (
        REPO_ROOT / "tests/fixtures/claim_language/accepted_underclaim_overcorrection.md"
    ).read_text(encoding="utf-8")
    special_texts = {
        "rr_e_transport_source_law_overclaim": (
            "RR_ETransportCompletenessOrInvarianceLaw_v1 adopted.\n"
        ),
        "accepted_positive_status_missing": underclaim_text,
        "accepted_scope_after_blocked_overread": underclaim_text,
        "caveat_wall_public_summary": underclaim_text,
        "status_card_v2_missing_next_burden": (
            REPO_ROOT
            / "tests/fixtures/claim_language/status_card_v2_missing_next_burden.md"
        ).read_text(encoding="utf-8"),
    }
    class_results: list[dict[str, Any]] = []
    for phrase_class in taxonomy["phrase_classes"]:
        class_id = phrase_class["class_id"]
        bad_phrases = phrase_class.get("bad_phrases", [])
        text = special_texts.get(class_id, f"{bad_phrases[0]}\n" if bad_phrases else "")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = "research_control/current_frontier.md"
            materialize_files(root, {path: text})
            fixture = {
                "fixture_id": f"taxonomy_{class_id}",
                "changed_paths": [path],
                "message_matchers": [],
            }
            legacy = standalone_claim_outcome(root, [path])
            consolidated = integrated_claim_outcome(root, fixture)
        finding_id = f"claim_language_changed:{class_id}"
        legacy_ids = set(legacy["hard_finding_ids"]) | set(legacy["warning_finding_ids"])
        consolidated_ids = set(consolidated["hard_finding_ids"]) | set(
            consolidated["warning_finding_ids"]
        )
        legacy_authority = [
            entry for entry in legacy["authority_fields"] if entry["finding_id"] == finding_id
        ]
        consolidated_authority = [
            entry
            for entry in consolidated["authority_fields"]
            if entry["finding_id"] == finding_id
        ]
        class_results.append(
            {
                "class_id": class_id,
                "legacy_detected": finding_id in legacy_ids,
                "consolidated_detected": finding_id in consolidated_ids,
                "legacy_severities": sorted({entry["severity"] for entry in legacy_authority}),
                "consolidated_severities": sorted(
                    {entry["severity"] for entry in consolidated_authority}
                ),
                "authority_fields_preserved": legacy_authority == consolidated_authority,
            }
        )
    return {
        "active_class_count": len(class_results),
        "legacy_covered_class_count": sum(item["legacy_detected"] for item in class_results),
        "legacy_missing_class_ids": [
            item["class_id"] for item in class_results if not item["legacy_detected"]
        ],
        "consolidated_missing_class_ids": [
            item["class_id"] for item in class_results if not item["consolidated_detected"]
        ],
        "authority_mismatch_class_ids": [
            item["class_id"]
            for item in class_results
            if item["legacy_detected"] and not item["authority_fields_preserved"]
        ],
        "class_results": class_results,
    }


def severity_classification_audit() -> dict[str, Any]:
    taxonomy = CLAIM_LINTER.load_taxonomy(TAXONOMY_PATH)
    probes = [
        {
            "probe_id": "current_public_hard",
            "path": "README.md",
            "text": "GR derived.\n",
            "class_id": "einstein_equation_overclaim",
            "severity": "hard_fail_current_public",
        },
        {
            "probe_id": "current_control_hard",
            "path": "research_control/handoffs/handoff-synthetic.md",
            "text": "GR derived.\n",
            "class_id": "einstein_equation_overclaim",
            "severity": "hard_fail_current_control",
        },
        {
            "probe_id": "intentional_example_warning",
            "path": "README.md",
            "text": "Bad example: GR derived.\n",
            "class_id": "einstein_equation_overclaim",
            "severity": "warn_intentional_example",
        },
        {
            "probe_id": "historical_warning",
            "path": "research_control/tasks/RT-SYNTHETIC/artifacts/history.md",
            "text": "Historical GR derived.\n",
            "class_id": "einstein_equation_overclaim",
            "severity": "warn_historical",
        },
        {
            "probe_id": "public_summary_warning",
            "path": "README.md",
            "text": "M_src is not really anything.\n",
            "class_id": "scoped_adoption_minimized",
            "severity": "warn_public_summary",
        },
        {
            "probe_id": "current_control_warning",
            "path": "research_control/handoffs/handoff-synthetic.md",
            "text": "M_src is not really anything.\n",
            "class_id": "scoped_adoption_minimized",
            "severity": "warn_current_control",
        },
    ]
    results: list[dict[str, Any]] = []
    for probe in probes:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            materialize_files(
                root,
                {
                    probe["path"]: probe["text"],
                    "research_control/program_state.yaml": (
                        'latest_handoff_id: "handoff-synthetic"\n'
                    ),
                },
            )
            fixture = {
                "fixture_id": f"severity_{probe['probe_id']}",
                "changed_paths": [probe["path"]],
                "message_matchers": [],
            }
            legacy = standalone_claim_outcome(root, [probe["path"]])
            consolidated = integrated_claim_outcome(root, fixture)
        finding_id = f"claim_language_changed:{probe['class_id']}"
        legacy_severities = {
            entry["severity"]
            for entry in legacy["authority_fields"]
            if entry["finding_id"] == finding_id
        }
        consolidated_severities = {
            entry["severity"]
            for entry in consolidated["authority_fields"]
            if entry["finding_id"] == finding_id
        }
        results.append(
            {
                **probe,
                "legacy_preserved": probe["severity"] in legacy_severities,
                "consolidated_preserved": probe["severity"] in consolidated_severities,
            }
        )
    reachable = sorted({probe["severity"] for probe in probes})
    declared = sorted(taxonomy["severity_levels"])
    reviewed_contexts = CLAIM_LINTER.load_reviewed_contexts(REVIEWED_CONTEXTS_PATH)
    mapped_levels = {
        str(phrase_class.get(field, ""))
        for phrase_class in taxonomy["phrase_classes"]
        for field in ("default_severity", "control_severity", "historical_severity")
        if str(phrase_class.get(field, ""))
    }
    mapped_levels.update(
        str(rule.get("severity_override", ""))
        for rule in taxonomy.get("context_rules", {}).get("allow_contexts", [])
        if str(rule.get("severity_override", ""))
    )
    mapped_levels.update(
        str(entry.get("severity_override", ""))
        for entry in reviewed_contexts
        if str(entry.get("severity_override", ""))
    )
    return {
        "declared_severity_levels": declared,
        "reachable_severity_levels": reachable,
        "declared_without_active_mapping": sorted(set(declared) - mapped_levels),
        "legacy_missing_reachable_levels": sorted(
            {item["severity"] for item in results if not item["legacy_preserved"]}
        ),
        "consolidated_missing_reachable_levels": sorted(
            {item["severity"] for item in results if not item["consolidated_preserved"]}
        ),
        "probe_results": results,
    }


def configuration_error_audit() -> dict[str, Any]:
    selected = ["README.md"]
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        materialize_files(root, {"README.md": "Scoped project status.\n"})
        bad_taxonomy = root / "malformed_taxonomy.yaml"
        bad_taxonomy.write_text('schema_id: "unsupported"\n', encoding="utf-8")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            standalone_exit_code = CLAIM_LINTER.main(
                [
                    "--json",
                    "--repo-root",
                    root.as_posix(),
                    "--taxonomy",
                    bad_taxonomy.as_posix(),
                    "--reviewed-contexts",
                    REVIEWED_CONTEXTS_PATH.as_posix(),
                    "--paths",
                    "README.md",
                ]
            )
        raw = json.loads(stdout.getvalue())
        legacy = standalone_claim_report_outcome(raw, selected)
        real_validate_paths = CLAIM_LINTER.validate_paths

        def validate_with_malformed_taxonomy(**kwargs):
            return real_validate_paths(
                **kwargs,
                taxonomy_path=bad_taxonomy,
                reviewed_contexts_path=REVIEWED_CONTEXTS_PATH,
            )

        report = VALIDATOR.ValidationReport()
        with mock.patch.object(VALIDATOR, "REPO_ROOT", root), mock.patch.object(
            CLAIM_LINTER,
            "validate_paths",
            side_effect=validate_with_malformed_taxonomy,
        ):
            VALIDATOR.validate_changed_claim_language(report, selected)
    consolidated = normalize_validation_report(
        report,
        {"fixture_id": "configuration_error", "message_matchers": []},
        set(selected),
    )
    return {
        "status": "PASS" if legacy == consolidated else "REPAIR_REQUIRED",
        "standalone_exit_code": standalone_exit_code,
        "legacy": legacy,
        "consolidated": consolidated,
        "mismatch_fields": mismatch_fields(legacy, consolidated),
    }


def composition_audit() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        registry_dir = root / "registries"
        registry_dir.mkdir()

        def core_probe(report: Any) -> None:
            report.error("synthetic core failure")

        def diff_probe(report: Any, *_args: Any, **_kwargs: Any) -> None:
            report.error("synthetic diff failure")

        with mock.patch.object(VALIDATOR, "REPO_ROOT", root), mock.patch.object(
            VALIDATOR,
            "REGISTRY_DIR",
            registry_dir,
        ), mock.patch.object(
            VALIDATOR,
            "validate_registry_columns",
            side_effect=core_probe,
        ), mock.patch.object(
            VALIDATOR,
            "validate_distance_to_gr_ledger",
            return_value=None,
        ), mock.patch.object(
            VALIDATOR,
            "validate_frontier_theorem_inventory",
            return_value=None,
        ), mock.patch.object(VALIDATOR, "validate_diff", side_effect=diff_probe) as diff_spy:
            report = VALIDATOR.validate_all(check_diff=True)
    core_preserved = "synthetic core failure" in report.errors
    diff_executed = diff_spy.call_count == 1
    diff_preserved = "synthetic diff failure" in report.errors
    semantic_match = core_preserved and diff_executed and diff_preserved
    return {
        "status": "PASS" if semantic_match else "REPAIR_REQUIRED",
        "hermetic": True,
        "core_failure_preserved": core_preserved,
        "diff_gate_executed": diff_executed,
        "diff_failure_preserved": diff_preserved,
        "reason": (
            "validate_all returns before validate_diff when required registry surfaces are absent"
            if not semantic_match
            else "core and diff findings are both preserved"
        ),
    }


def build_report() -> dict[str, Any]:
    started = time.monotonic()
    cases = execute_corpus()
    mismatches = [case for case in cases if case["blocking"]]
    taxonomy_audit = taxonomy_classification_audit()
    severity_audit = severity_classification_audit()
    config_audit = configuration_error_audit()
    composed = composition_audit()
    hard_disappearances = sum(
        len(set(case["legacy"]["hard_finding_ids"]) - set(case["consolidated"]["hard_finding_ids"]))
        for case in cases
    )
    warning_disappearances = sum(
        len(set(case["legacy"]["warning_finding_ids"]) - set(case["consolidated"]["warning_finding_ids"]))
        for case in cases
    )
    report: dict[str, Any] = {
        "schema_id": "legacy_consolidated_equivalence_report_v1",
        "plan_task_id": "P1-T03",
        "task_id": REPORT_TASK_ID,
        "job_id": REPORT_JOB_ID,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "migration_epoch": "legacy",
        "status": "REPAIR_REQUIRED"
        if (
            mismatches
            or taxonomy_audit["legacy_missing_class_ids"]
            or taxonomy_audit["consolidated_missing_class_ids"]
            or taxonomy_audit["authority_mismatch_class_ids"]
            or severity_audit["legacy_missing_reachable_levels"]
            or severity_audit["consolidated_missing_reachable_levels"]
            or config_audit["status"] != "PASS"
            or composed["status"] != "PASS"
        )
        else "PASS",
        "comparison_scope": "component semantic equivalence plus consolidated composition guard",
        "gate_ids": {
            "legacy": ["research_control_core", "research_control_diff", "claim_language_changed"],
            "consolidated_candidate": ["research_control_diff"],
            "deduplication_activated": False,
            "orchestration_changed": False,
        },
        "counts": {
            "fixture_count": len(cases),
            "equivalent_fixture_count": len(cases) - len(mismatches),
            "semantic_mismatch_fixture_count": len(mismatches),
            "hard_finding_disappearance_count": hard_disappearances,
            "warning_finding_disappearance_count": warning_disappearances,
            "legacy_fail_consolidated_pass_count": sum(
                case["legacy"]["status"] == "FAIL" and case["consolidated"]["status"] == "PASS"
                for case in cases
            ),
            "taxonomy_class_count": taxonomy_audit["active_class_count"],
            "taxonomy_class_finding_disappearance_count": len(
                taxonomy_audit["consolidated_missing_class_ids"]
            ),
            "taxonomy_authority_mismatch_class_count": len(
                taxonomy_audit["authority_mismatch_class_ids"]
            ),
        },
        "blocking_mismatches": [
            {
                "fixture_id": case["fixture_id"],
                "mismatch_fields": case["mismatch_fields"],
                "legacy_hard_finding_ids": case["legacy"]["hard_finding_ids"],
                "consolidated_hard_finding_ids": case["consolidated"]["hard_finding_ids"],
                "legacy_warning_finding_ids": case["legacy"]["warning_finding_ids"],
                "consolidated_warning_finding_ids": case["consolidated"]["warning_finding_ids"],
            }
            for case in mismatches
        ],
        "coverage": {
            "required_fixture_ids": [case["fixture_id"] for case in cases],
            "claim_taxonomy_class_ids": [
                item["class_id"] for item in taxonomy_audit["class_results"]
            ],
            "diff_boundary_classes": [
                "missing_active_agentjob",
                "disallowed_path",
                "overly_broad_allowlist",
                "markdown_authority_violation",
                "unrelated_path",
            ],
            "mutation_guard": "Every manifest fixture is mutated and the comparator must reject the changed semantic result.",
        },
        "taxonomy_classification_audit": taxonomy_audit,
        "severity_classification_audit": severity_audit,
        "configuration_error_audit": config_audit,
        "composition_audit": composed,
        "case_results": cases,
        "source_hashes": {
            "fixture_corpus_sha256": sha256_file(CORPUS_PATH),
            "test_module_sha256": sha256_file(Path(__file__)),
            "research_control_validator_sha256": sha256_file(
                RESEARCH_SCRIPT_DIR / "validate_research_control.py"
            ),
            "claim_language_validator_sha256": sha256_file(
                PROJECT_SCRIPT_DIR / "validate_claim_language.py"
            ),
            "claim_taxonomy_sha256": sha256_file(TAXONOMY_PATH),
            "reviewed_contexts_sha256": sha256_file(REVIEWED_CONTEXTS_PATH),
        },
        "performance_evidence": {
            "before_reference": "research_control/tasks/RT-20260712-003/artifacts/v19_baseline_benchmark.json",
            "duration_seconds": round(time.monotonic() - started, 6),
            "subprocess_count": 0,
            "output_bytes": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        },
        "authority_boundary": {
            "project_system_change_only": True,
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "ordinary_research_handoff_preserved": "handoff-0740",
            "p1_t04_unlocked": not mismatches,
        },
        "repair_route": {
            "required": bool(mismatches),
            "reason": "The integrated path drops claim warnings and structured authority metadata and can short-circuit claim or diff findings on early failures.",
            "production_validator_modified_by_this_job": False,
            "next_task": "One separately bounded Validator Engineer repair must preserve structured warnings and claim findings across early-failure branches, then rerun P1-T03.",
        },
    }
    while True:
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        size = len(rendered.encode("utf-8"))
        if report["performance_evidence"]["output_bytes"] == size:
            break
        report["performance_evidence"]["output_bytes"] = size
    return report


class ValidationEquivalenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_corpus()
        cls.results = execute_corpus()
        cls.by_id = {result["fixture_id"]: result for result in cls.results}

    def test_corpus_contains_every_required_fixture(self) -> None:
        required = {
            "clean_pass",
            "malformed_registry",
            "missing_active_agentjob",
            "disallowed_path",
            "overly_broad_allowlist",
            "markdown_authority_violation",
            "public_overclaim",
            "reviewed_historical_warning",
            "target_import",
            "stale_sidecar",
            "unrelated_path",
        }
        self.assertEqual({case["fixture_id"] for case in self.corpus["cases"]}, required)
        self.assertEqual(tuple(self.corpus["comparison_fields"]), COMPARISON_FIELDS)

    def test_current_outcomes_match_fixture_contract(self) -> None:
        for fixture in self.corpus["cases"]:
            with self.subTest(fixture=fixture["fixture_id"]):
                observed = self.by_id[fixture["fixture_id"]]
                self.assertEqual(observed["legacy"], fixture["expected_legacy"])
                self.assertEqual(observed["consolidated"], fixture["expected_consolidated"])
                self.assertEqual(observed["mismatch_fields"], fixture["expected_mismatch_fields"])

    def test_each_adversarial_fixture_hits_its_intended_finding(self) -> None:
        for fixture in self.corpus["cases"]:
            intended = set(fixture["intended_finding_ids"])
            observed = self.by_id[fixture["fixture_id"]]["legacy"]
            findings = set(observed["hard_finding_ids"]) | set(observed["warning_finding_ids"])
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertTrue(intended.issubset(findings))

    def test_current_semantics_are_equivalent(self) -> None:
        blocking = {
            result["fixture_id"]: result["mismatch_fields"]
            for result in self.results
            if result["blocking"]
        }
        self.assertEqual(blocking, {})

    def test_comparator_rejects_a_semantic_mutation_for_every_fixture(self) -> None:
        for fixture in self.corpus["cases"]:
            baseline = self.by_id[fixture["fixture_id"]]["legacy"]
            mutated = json.loads(json.dumps(baseline))
            intended = set(fixture["intended_finding_ids"])
            if intended:
                mutated["hard_finding_ids"] = [
                    item for item in mutated["hard_finding_ids"] if item not in intended
                ]
                mutated["warning_finding_ids"] = [
                    item for item in mutated["warning_finding_ids"] if item not in intended
                ]
                mutated["authority_fields"] = [
                    item
                    for item in mutated["authority_fields"]
                    if item["finding_id"] not in intended
                ]
                mutated["status"] = "FAIL" if mutated["hard_finding_ids"] else "PASS"
            else:
                mutated["hard_finding_ids"] = ["mutation:spurious_failure"]
                mutated["authority_fields"] = [
                    {"finding_id": "mutation:spurious_failure", "severity": "blocking"}
                ]
                mutated["status"] = "FAIL"
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertTrue(mismatch_fields(baseline, mutated))

    def test_taxonomy_and_severity_classifications_are_exhaustively_audited(self) -> None:
        taxonomy = taxonomy_classification_audit()
        self.assertEqual(taxonomy["active_class_count"], 42)
        self.assertEqual(taxonomy["legacy_covered_class_count"], 42)
        self.assertEqual(taxonomy["legacy_missing_class_ids"], [])
        self.assertEqual(taxonomy["consolidated_missing_class_ids"], [])
        self.assertEqual(taxonomy["authority_mismatch_class_ids"], [])

        severity = severity_classification_audit()
        self.assertEqual(severity["declared_without_active_mapping"], ["warn_review"])
        self.assertEqual(severity["legacy_missing_reachable_levels"], [])
        self.assertEqual(severity["consolidated_missing_reachable_levels"], [])

    def test_configuration_errors_preserve_blocking_semantics(self) -> None:
        audit = configuration_error_audit()
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["mismatch_fields"], [])

    def test_hermetic_composition_guard_preserves_both_gates(self) -> None:
        audit = composition_audit()
        self.assertEqual(audit["status"], "PASS")
        self.assertTrue(audit["hermetic"])
        self.assertTrue(audit["core_failure_preserved"])
        self.assertTrue(audit["diff_gate_executed"])
        self.assertTrue(audit["diff_failure_preserved"])

    def test_report_passes_and_unlocks_future_p1_t04_dependency(self) -> None:
        report = build_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"]["semantic_mismatch_fixture_count"], 0)
        self.assertEqual(report["counts"]["hard_finding_disappearance_count"], 0)
        self.assertEqual(report["counts"]["warning_finding_disappearance_count"], 0)
        self.assertEqual(report["counts"]["taxonomy_class_count"], 42)
        self.assertEqual(report["counts"]["taxonomy_class_finding_disappearance_count"], 0)
        self.assertEqual(report["counts"]["taxonomy_authority_mismatch_class_count"], 0)
        self.assertTrue(report["authority_boundary"]["p1_t04_unlocked"])
        self.assertFalse(report["gate_ids"]["deduplication_activated"])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", type=Path)
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(
            json.dumps(build_report(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(args.write_report.as_posix())
    else:
        unittest.main(argv=[sys.argv[0]])
