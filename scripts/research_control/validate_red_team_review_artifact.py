"""Validate skeptical-review artifacts and their current internal label contract.

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
CURRENT_ROLE_PATH = ".agents/roles/physics/external-red-team-reviewer.v0.1.0.md"
CURRENT_TEMPLATE_PATH = "research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml"
CURRENT_DESIGN_PATH = "research_control/design/external_red_team_reviewer_role_design.md"
CURRENT_ROLE_ID = "external-red-team-reviewer"
CURRENT_ROLE_VERSION = "0.1.0"
CURRENT_REVIEWER_DISPLAY_NAME = "Internal Skeptical Reviewer"
CURRENT_REVIEWER_ROLE_KIND = "scientific_adversarial_internal_review"
CURRENT_LABEL_FIELDS: tuple[str, ...] = (
    "reviewer_display_name",
    "reviewer_role_kind",
)
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
REVIEW_CONTEXT_SCHEMA_ID = "v21_review_context_v1"
REVIEW_CONTEXT_CLASSIFICATIONS: tuple[str, ...] = (
    "same_context_role_review",
    "blind_same_model_review",
    "different_model_review",
    "human_expert_review",
    "independent_replication",
    "unknown",
)
REVIEWER_KINDS: tuple[str, ...] = ("human", "ai", "mixed", "unknown")
PRIOR_CONTEXT_ACCESS_VALUES: tuple[str, ...] = (
    "same_context",
    "blind_packet_only",
    "fresh_context",
    "partial",
    "unknown",
    "not_applicable",
)
INDEPENDENCE_DIMENSIONS: tuple[str, ...] = (
    "model_family",
    "prompt_context",
    "data_access",
    "institution",
    "human_authorship",
    "code_base",
    "method",
)
DIMENSION_RELATIONSHIPS: tuple[str, ...] = (
    "same",
    "different",
    "independent",
    "not_applicable",
    "unknown",
)
REVIEW_CLAIM_FIELDS: tuple[str, ...] = (
    "external_review_completed",
    "human_expert_review_completed",
    "independent_replication_completed",
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


def _validate_current_label_fields(
    data: dict[str, Any], issues: list[ValidationIssue]
) -> str:
    present = {field for field in CURRENT_LABEL_FIELDS if field in data}
    if not present:
        return "legacy_identifier_only"
    for field in CURRENT_LABEL_FIELDS:
        if field not in data:
            issues.append(
                ValidationIssue(
                    field,
                    "must be present when either current reviewer label field is present",
                )
            )
    expected = {
        "reviewer_display_name": CURRENT_REVIEWER_DISPLAY_NAME,
        "reviewer_role_kind": CURRENT_REVIEWER_ROLE_KIND,
    }
    for field, expected_value in expected.items():
        if field in data and data.get(field) != expected_value:
            issues.append(ValidationIssue(field, f"must be exactly {expected_value}"))
    return "current_internal" if len(present) == len(CURRENT_LABEL_FIELDS) else "invalid"


def validate_current_contract(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Fail closed when the live role, schema, design, or template drifts externally."""

    issues: list[ValidationIssue] = []
    role_path = repo_root / CURRENT_ROLE_PATH
    try:
        frontmatter, role_body = strict_yaml.load_frontmatter(role_path)
    except (OSError, strict_yaml.StrictYamlError) as exc:
        issues.append(ValidationIssue(CURRENT_ROLE_PATH, str(exc)))
        frontmatter, role_body = {}, ""

    expected_frontmatter = {
        "role_id": CURRENT_ROLE_ID,
        "version": CURRENT_ROLE_VERSION,
        "role_name": CURRENT_REVIEWER_DISPLAY_NAME,
        "role_kind": CURRENT_REVIEWER_ROLE_KIND,
    }
    for field, expected_value in expected_frontmatter.items():
        if frontmatter.get(field) != expected_value:
            issues.append(
                ValidationIssue(
                    f"{CURRENT_ROLE_PATH}:{field}",
                    f"must be exactly {expected_value}",
                )
            )
    for marker in (
        "stable role identifier",
        "legacy identifier",
        "same-context AI is internal review",
        "cannot claim that it performed external",
        "independent replication",
    ):
        if marker.lower() not in role_body.lower():
            issues.append(
                ValidationIssue(CURRENT_ROLE_PATH, f"missing internal-label marker: {marker}")
            )

    schema_path = repo_root / SCHEMA_PATH
    design_path = repo_root / CURRENT_DESIGN_PATH
    for path_text, markers in {
        SCHEMA_PATH: (
            "# Internal Skeptical Review Artifact Schema",
            'reviewer_display_name: "Internal Skeptical Reviewer"',
            'reviewer_role_kind: "scientific_adversarial_internal_review"',
            "internal skeptical-review classes",
            "not external",
        ),
        CURRENT_DESIGN_PATH: (
            "## Current V21 Label Contract",
            "same-context AI review is internal",
            "stable legacy identifier only",
        ),
    }.items():
        path = schema_path if path_text == SCHEMA_PATH else design_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(ValidationIssue(path_text, str(exc)))
            continue
        for marker in markers:
            if marker.lower() not in text.lower():
                issues.append(
                    ValidationIssue(path_text, f"missing internal-label marker: {marker}")
                )

    template_path = repo_root / CURRENT_TEMPLATE_PATH
    try:
        template = strict_yaml.load(template_path)
    except (OSError, strict_yaml.StrictYamlError) as exc:
        issues.append(ValidationIssue(CURRENT_TEMPLATE_PATH, str(exc)))
        template = {}
    for field, expected_value in {
        "reviewer_role_id": CURRENT_ROLE_ID,
        "reviewer_role_version": CURRENT_ROLE_VERSION,
        "reviewer_display_name": CURRENT_REVIEWER_DISPLAY_NAME,
        "reviewer_role_kind": CURRENT_REVIEWER_ROLE_KIND,
    }.items():
        if template.get(field) != expected_value:
            issues.append(
                ValidationIssue(
                    f"{CURRENT_TEMPLATE_PATH}:{field}",
                    f"must be exactly {expected_value}",
                )
            )

    if issues:
        raise RedTeamReviewValidationError(schema_path, issues)
    return {
        "status": "PASS",
        "role_id": CURRENT_ROLE_ID,
        "role_version": CURRENT_ROLE_VERSION,
        "reviewer_display_name": CURRENT_REVIEWER_DISPLAY_NAME,
        "reviewer_role_kind": CURRENT_REVIEWER_ROLE_KIND,
        "legacy_identifier_preserved": True,
        "external_provenance_inferred": False,
    }


def _validate_review_context(
    data: dict[str, Any], issues: list[ValidationIssue]
) -> dict[str, Any]:
    context = data.get("review_context")
    if context is None:
        return {
            "review_context_present": False,
            "review_context_classification": "legacy_unclassified",
        }
    if not isinstance(context, dict):
        issues.append(ValidationIssue("review_context", "must be a map"))
        return {
            "review_context_present": True,
            "review_context_classification": "unknown",
        }

    required_context_fields = {
        "schema_id",
        "classification",
        "reviewer_kind",
        "blind_packet_received",
        "prior_context_access",
        "review_executed",
        "replication_executed",
        "dimensions",
        "evidence_paths",
        "limitations",
        "claims",
    }
    for field in sorted(required_context_fields - set(context)):
        issues.append(ValidationIssue(f"review_context.{field}", "missing required field"))
    for field in sorted(set(context) - required_context_fields):
        issues.append(ValidationIssue(f"review_context.{field}", "unexpected field"))

    if context.get("schema_id") != REVIEW_CONTEXT_SCHEMA_ID:
        issues.append(
            ValidationIssue(
                "review_context.schema_id",
                f"must be exactly {REVIEW_CONTEXT_SCHEMA_ID}",
            )
        )

    classification = context.get("classification")
    if classification not in REVIEW_CONTEXT_CLASSIFICATIONS:
        issues.append(
            ValidationIssue(
                "review_context.classification",
                f"must be one of {', '.join(REVIEW_CONTEXT_CLASSIFICATIONS)}",
            )
        )
        classification = "unknown"

    reviewer_kind = context.get("reviewer_kind")
    if reviewer_kind not in REVIEWER_KINDS:
        issues.append(
            ValidationIssue(
                "review_context.reviewer_kind",
                f"must be one of {', '.join(REVIEWER_KINDS)}",
            )
        )

    prior_context_access = context.get("prior_context_access")
    if prior_context_access not in PRIOR_CONTEXT_ACCESS_VALUES:
        issues.append(
            ValidationIssue(
                "review_context.prior_context_access",
                f"must be one of {', '.join(PRIOR_CONTEXT_ACCESS_VALUES)}",
            )
        )

    for field in ("blind_packet_received", "review_executed", "replication_executed"):
        if not isinstance(context.get(field), bool):
            issues.append(ValidationIssue(f"review_context.{field}", "must be boolean"))

    dimensions = context.get("dimensions")
    relationships: dict[str, str] = {}
    if not isinstance(dimensions, dict):
        issues.append(ValidationIssue("review_context.dimensions", "must be a map"))
    else:
        for dimension in sorted(set(INDEPENDENCE_DIMENSIONS) - set(dimensions)):
            issues.append(
                ValidationIssue(
                    f"review_context.dimensions.{dimension}", "missing required dimension"
                )
            )
        for dimension in sorted(set(dimensions) - set(INDEPENDENCE_DIMENSIONS)):
            issues.append(
                ValidationIssue(
                    f"review_context.dimensions.{dimension}", "unexpected dimension"
                )
            )
        for dimension in INDEPENDENCE_DIMENSIONS:
            entry = dimensions.get(dimension)
            if not isinstance(entry, dict):
                if dimension in dimensions:
                    issues.append(
                        ValidationIssue(
                            f"review_context.dimensions.{dimension}", "must be a map"
                        )
                    )
                continue
            if set(entry) != {"relationship", "evidence"}:
                issues.append(
                    ValidationIssue(
                        f"review_context.dimensions.{dimension}",
                        "must contain exactly relationship and evidence",
                    )
                )
            relationship = entry.get("relationship")
            if relationship not in DIMENSION_RELATIONSHIPS:
                issues.append(
                    ValidationIssue(
                        f"review_context.dimensions.{dimension}.relationship",
                        f"must be one of {', '.join(DIMENSION_RELATIONSHIPS)}",
                    )
                )
            else:
                relationships[dimension] = relationship
            if not _is_nonempty_string(entry.get("evidence")):
                issues.append(
                    ValidationIssue(
                        f"review_context.dimensions.{dimension}.evidence",
                        "must be a nonempty string",
                    )
                )

    evidence_paths = context.get("evidence_paths")
    if not isinstance(evidence_paths, list):
        issues.append(ValidationIssue("review_context.evidence_paths", "must be a list"))
        evidence_paths = []
    else:
        for item in evidence_paths:
            if not isinstance(item, str):
                issues.append(
                    ValidationIssue(
                        "review_context.evidence_paths", "all entries must be strings"
                    )
                )
                continue
            reason = _validate_relative_source_path(item)
            if reason:
                issues.append(ValidationIssue("review_context.evidence_paths", reason))

    limitations = context.get("limitations")
    if not isinstance(limitations, list) or any(
        not _is_nonempty_string(item) for item in limitations
    ):
        issues.append(
            ValidationIssue(
                "review_context.limitations", "must be a list of nonempty strings"
            )
        )

    claims = context.get("claims")
    claim_values: dict[str, bool] = {}
    if not isinstance(claims, dict):
        issues.append(ValidationIssue("review_context.claims", "must be a map"))
    else:
        if set(claims) != set(REVIEW_CLAIM_FIELDS):
            issues.append(
                ValidationIssue(
                    "review_context.claims",
                    "must contain exactly external_review_completed, "
                    "human_expert_review_completed, and "
                    "independent_replication_completed",
                )
            )
        for field in REVIEW_CLAIM_FIELDS:
            value = claims.get(field)
            if not isinstance(value, bool):
                issues.append(
                    ValidationIssue(f"review_context.claims.{field}", "must be boolean")
                )
            else:
                claim_values[field] = value

    review_executed = context.get("review_executed") is True
    replication_executed = context.get("replication_executed") is True
    blind_packet_received = context.get("blind_packet_received") is True

    if classification == "same_context_role_review":
        if not review_executed or relationships.get("prompt_context") != "same":
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "same_context_role_review requires an executed review and same prompt context",
                )
            )
    elif classification == "blind_same_model_review":
        if (
            not review_executed
            or not blind_packet_received
            or relationships.get("model_family") != "same"
            or prior_context_access != "blind_packet_only"
        ):
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "blind_same_model_review requires review execution, a blind packet, "
                    "same model family, and blind_packet_only context",
                )
            )
    elif classification == "different_model_review":
        if not review_executed or relationships.get("model_family") not in {
            "different",
            "independent",
        }:
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "different_model_review requires review execution and different model-family evidence",
                )
            )
    elif classification == "human_expert_review":
        if (
            reviewer_kind != "human"
            or not review_executed
            or relationships.get("human_authorship") not in {"different", "independent"}
            or not evidence_paths
        ):
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "human_expert_review requires human provenance, executed review, "
                    "authorship separation, and evidence paths",
                )
            )
    elif classification == "independent_replication":
        independent_dimensions = ("data_access", "code_base", "method")
        if (
            reviewer_kind == "unknown"
            or not replication_executed
            or any(relationships.get(item) != "independent" for item in independent_dimensions)
            or not evidence_paths
        ):
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "independent_replication requires executed replication, known provenance, "
                    "independent data access, code base, and method, plus evidence paths",
                )
            )
    elif classification == "unknown":
        if relationships and "unknown" not in relationships.values():
            issues.append(
                ValidationIssue(
                    "review_context.classification",
                    "unknown requires at least one explicitly unknown dimension",
                )
            )

    external_claim = claim_values.get("external_review_completed", False)
    human_claim = claim_values.get("human_expert_review_completed", False)
    replication_claim = claim_values.get("independent_replication_completed", False)

    if external_claim and (
        reviewer_kind != "human"
        or classification not in {"human_expert_review", "independent_replication"}
        or relationships.get("human_authorship") not in {"different", "independent"}
        or not evidence_paths
    ):
        issues.append(
            ValidationIssue(
                "review_context.claims.external_review_completed",
                "positive external-review wording requires evidenced human review provenance",
            )
        )
    if human_claim and (
        reviewer_kind != "human"
        or classification not in {"human_expert_review", "independent_replication"}
        or not review_executed
    ):
        issues.append(
            ValidationIssue(
                "review_context.claims.human_expert_review_completed",
                "human-expert completion requires an evidenced executed human review",
            )
        )
    if replication_claim and (
        classification != "independent_replication" or not replication_executed
    ):
        issues.append(
            ValidationIssue(
                "review_context.claims.independent_replication_completed",
                "positive independent-replication wording requires the evidenced independent_replication class",
            )
        )
    if classification in {
        "same_context_role_review",
        "blind_same_model_review",
        "different_model_review",
        "unknown",
    } and any(claim_values.values()):
        issues.append(
            ValidationIssue(
                "review_context.claims",
                "internal or unknown review classes cannot claim external human review or independent replication",
            )
        )
    if classification == "human_expert_review" and replication_claim:
        issues.append(
            ValidationIssue(
                "review_context.claims.independent_replication_completed",
                "human expert review is not independent replication",
            )
        )

    return {
        "review_context_present": True,
        "review_context_classification": classification,
    }


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

    reviewer_label_contract = _validate_current_label_fields(data, issues)
    review_context_summary = _validate_review_context(data, issues)

    if issues:
        raise RedTeamReviewValidationError(path, issues)

    return {
        "artifact_path": path.as_posix(),
        "reviewed_object_id": data["reviewed_object_id"],
        "reviewed_source_path_count": len(data["reviewed_source_paths"]),
        "verdict": data["verdict"],
        "recommended_next_route": data["recommended_next_route"],
        "physics_promotion_authorized": False,
        "reviewer_label_contract": reviewer_label_contract,
        **review_context_summary,
    }


def validate_review_file(path: Path) -> dict[str, Any]:
    data = strict_yaml.load(path)
    return validate_review_data(data, path)


def validate_files(paths: list[Path], *, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    current_contract = validate_current_contract(repo_root)
    checked = [validate_review_file(path) for path in paths]
    context_counts: dict[str, int] = {}
    for item in checked:
        classification = item["review_context_classification"]
        context_counts[classification] = context_counts.get(classification, 0) + 1
    return {
        "schema_id": SCHEMA_ID,
        "schema_path": SCHEMA_PATH,
        "status": "PASS",
        "checked_artifact_count": len(checked),
        "checked_artifacts": checked,
        "current_contract": current_contract,
        "review_context_classification_counts": dict(sorted(context_counts.items())),
        "physics_promotion_authorized": False,
        "authority_boundary": (
            "shape_validation_only_no_proof_authority_no_gate_chair_authority"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate strict-YAML skeptical-review artifacts and current internal labels."
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
