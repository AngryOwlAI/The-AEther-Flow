"""Validate external red-team review artifacts.

The validator is project-control tooling for P7 red-team review outputs. A
passing artifact is review/routing evidence only; it is not proof authority and
never authorizes physics promotion.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml


SCHEMA_ID = "external_red_team_review_artifact_schema_v1"
SCHEMA_PATH = ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md"
REQUIRED_FIELDS: tuple[str, ...] = (
    "reviewed_object_id",
    "reviewed_source_paths",
    "claim_under_review",
    "assumptions_read",
    "definitions_read",
    "proof_steps_checked",
    "circularity_findings",
    "hidden_import_findings",
    "notation_overload_findings",
    "unproven_equivalence_findings",
    "minimal_countermodel_attempt",
    "external_mathematical_pressure_points",
    "verdict",
    "recommended_next_route",
    "physics_promotion_authorized",
)
LIST_FIELDS: tuple[str, ...] = (
    "reviewed_source_paths",
    "assumptions_read",
    "definitions_read",
    "proof_steps_checked",
    "circularity_findings",
    "hidden_import_findings",
    "notation_overload_findings",
    "unproven_equivalence_findings",
    "external_mathematical_pressure_points",
)
NONEMPTY_LIST_FIELDS: tuple[str, ...] = (
    "reviewed_source_paths",
    "assumptions_read",
    "definitions_read",
    "proof_steps_checked",
)
VERDICT_VALUES: tuple[str, ...] = (
    "no_blocking_defect_found_as_written",
    "repair_required",
    "hidden_target_import_detected",
    "circularity_detected",
    "unproven_equivalence_blocks_claim",
    "not_enough_assumptions",
    "minimal_countermodel_found",
    "freeze_recommended",
    "external_expert_review_required",
)
COUNTERMODEL_RESULTS: tuple[str, ...] = (
    "not_attempted",
    "no_countermodel_found_under_scope",
    "countermodel_found",
    "not_enough_assumptions",
)
FORBIDDEN_SOURCE_PREFIXES: tuple[str, ...] = (
    ".local/",
    "wiki/markdown/",
    "wiki/tex/",
    "wiki/indexes/",
)


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"field": self.field, "message": self.message}


class RedTeamReviewValidationError(ValueError):
    """Raised when a red-team review artifact violates the schema."""

    def __init__(self, path: Path, issues: list[ValidationIssue]) -> None:
        self.path = path
        self.issues = issues
        joined = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        super().__init__(f"{path}: {joined}")


def _repo_root() -> Path:
    return REPO_ROOT


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_relative_source_path(path_text: str) -> str | None:
    if not path_text:
        return "path is empty"
    path = Path(path_text)
    if path.is_absolute():
        return "path must be repo-relative"
    if any(part == ".." for part in path.parts):
        return "path must not escape the repository"
    if any(path_text.startswith(prefix) for prefix in FORBIDDEN_SOURCE_PREFIXES):
        return "reviewed source path must be canonical, not generated or local"
    return None


def _append_type_issue(issues: list[ValidationIssue], data: dict[str, Any], field: str) -> None:
    if field not in data:
        issues.append(ValidationIssue(field, "missing required field"))


def validate_review_data(data: dict[str, Any], path: Path) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    for field in REQUIRED_FIELDS:
        _append_type_issue(issues, data, field)

    for field in ("reviewed_object_id", "claim_under_review", "recommended_next_route"):
        if field in data and not _is_nonempty_string(data[field]):
            issues.append(ValidationIssue(field, "must be a nonempty string"))

    for field in LIST_FIELDS:
        if field not in data:
            continue
        value = data[field]
        if not isinstance(value, list):
            issues.append(ValidationIssue(field, "must be a list"))
            continue
        if field in NONEMPTY_LIST_FIELDS and not value:
            issues.append(ValidationIssue(field, "must be nonempty"))
        if any(not isinstance(item, str) for item in value):
            issues.append(ValidationIssue(field, "all list items must be strings"))

    if isinstance(data.get("reviewed_source_paths"), list):
        for item in data["reviewed_source_paths"]:
            if isinstance(item, str):
                reason = _validate_relative_source_path(item)
                if reason:
                    issues.append(ValidationIssue("reviewed_source_paths", reason))

    verdict = data.get("verdict")
    if verdict is not None and verdict not in VERDICT_VALUES:
        issues.append(
            ValidationIssue("verdict", f"must be one of {', '.join(VERDICT_VALUES)}")
        )

    if data.get("physics_promotion_authorized") is not False:
        issues.append(
            ValidationIssue("physics_promotion_authorized", "must be exactly false")
        )

    countermodel = data.get("minimal_countermodel_attempt")
    if countermodel is not None:
        if not isinstance(countermodel, dict):
            issues.append(ValidationIssue("minimal_countermodel_attempt", "must be a map"))
        else:
            if not isinstance(countermodel.get("attempted"), bool):
                issues.append(
                    ValidationIssue("minimal_countermodel_attempt.attempted", "must be boolean")
                )
            result = countermodel.get("result")
            if result not in COUNTERMODEL_RESULTS:
                issues.append(
                    ValidationIssue(
                        "minimal_countermodel_attempt.result",
                        f"must be one of {', '.join(COUNTERMODEL_RESULTS)}",
                    )
                )
            if not _is_nonempty_string(countermodel.get("summary")):
                issues.append(
                    ValidationIssue("minimal_countermodel_attempt.summary", "must be nonempty")
                )
            artifact_path = countermodel.get("artifact_path", "")
            if artifact_path and isinstance(artifact_path, str):
                reason = _validate_relative_source_path(artifact_path)
                if reason:
                    issues.append(
                        ValidationIssue("minimal_countermodel_attempt.artifact_path", reason)
                    )
            elif artifact_path and not isinstance(artifact_path, str):
                issues.append(
                    ValidationIssue(
                        "minimal_countermodel_attempt.artifact_path", "must be a string"
                    )
                )

    if issues:
        raise RedTeamReviewValidationError(path, issues)

    return {
        "artifact_path": path.as_posix(),
        "reviewed_object_id": data["reviewed_object_id"],
        "reviewed_source_path_count": len(data["reviewed_source_paths"]),
        "verdict": data["verdict"],
        "recommended_next_route": data["recommended_next_route"],
        "physics_promotion_authorized": False,
    }


def validate_review_file(path: Path) -> dict[str, Any]:
    data = strict_yaml.load(path)
    return validate_review_data(data, path)


def validate_files(paths: list[Path]) -> dict[str, Any]:
    checked = [validate_review_file(path) for path in paths]
    return {
        "schema_id": SCHEMA_ID,
        "schema_path": SCHEMA_PATH,
        "status": "PASS",
        "checked_artifact_count": len(checked),
        "checked_artifacts": checked,
        "physics_promotion_authorized": False,
        "authority_boundary": (
            "shape_validation_only_no_proof_authority_no_gate_chair_authority"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate strict-YAML external red-team review artifacts."
    )
    parser.add_argument("artifacts", nargs="+", help="Review artifact YAML path(s).")
    parser.add_argument("--json", action="store_true", help="Emit JSON receipt.")
    args = parser.parse_args(argv)
    paths = [Path(item) for item in args.artifacts]
    try:
        receipt = validate_files(paths)
    except (strict_yaml.StrictYamlError, RedTeamReviewValidationError) as exc:
        failure = {
            "schema_id": SCHEMA_ID,
            "status": "FAIL",
            "error": str(exc),
            "physics_promotion_authorized": False,
        }
        if args.json:
            print(json.dumps(failure, indent=2, sort_keys=True))
        else:
            print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print("Red-team review artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
