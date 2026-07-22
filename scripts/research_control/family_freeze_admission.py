#!/usr/bin/env python3
"""Prospective family-freeze and evidence-based reopening admission policy."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


SCHEMA_ID = "family_freeze_route_admission_v1"
POLICY_ID = "family_freeze_reopening_policy_v1"
ACTIVE_AFTER = "2026-07-22T17:25:51Z"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260722-013"
    / "artifacts"
    / "family_freeze_historical_seed.json"
)

CANDIDATE_CYCLE_ROUTE_KINDS = frozenset(
    {
        "candidate_construction",
        "candidate_audit",
        "candidate_stress",
        "candidate_repair",
    }
)
DISTINCT_BRANCH_ROUTE_KINDS = frozenset(
    {
        "theorem_investigation",
        "primitive_investigation",
        "variation_class_investigation",
        "source_acquisition",
        "precise_obstruction",
    }
)
ROUTE_KINDS = CANDIDATE_CYCLE_ROUTE_KINDS | DISTINCT_BRANCH_ROUTE_KINDS | {
    "rename_or_repackage",
}
REOPENING_CLASSES = frozenset(
    {"new_primitive", "new_theorem", "new_variation_class", "protected_decision"}
)
AUTHORITY_LIMITS = {
    "local_family_freeze_preserved": True,
    "global_no_go_claimed": False,
    "automatic_candidate_adoption": False,
    "theorem_truth_inferred": False,
    "ontology_modified": False,
    "physics_promotion_authorized": False,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _timestamp(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def policy_active(created_at: str) -> bool:
    created = _timestamp(created_at)
    activated = _timestamp(ACTIVE_AFTER)
    return bool(created and activated and created > activated)


def load_freeze_registry(path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def family_freeze_policy() -> dict[str, object]:
    """Return the Director-facing policy context without scientific authority."""

    registry = load_freeze_registry()
    return {
        "policy_id": POLICY_ID,
        "schema_id": SCHEMA_ID,
        "active_after": ACTIVE_AFTER,
        "enforcement": "hard_failure_for_repeated_candidate_cycles",
        "historical_jobs_without_block": "legacy_readable",
        "frozen_family_count": len(registry.get("freezes", [])),
        "match_fields": [
            "family_id",
            "family_identity_sha256",
            "assumption_sha256",
        ],
        "candidate_cycle_route_kinds": sorted(CANDIDATE_CYCLE_ROUTE_KINDS),
        "distinct_branch_route_kinds": sorted(DISTINCT_BRANCH_ROUTE_KINDS),
        "reopening_classes": sorted(REOPENING_CLASSES),
        "renamed_or_repackaged_route_admitted": False,
        "distinct_theorem_or_ontology_branch_blocked": False,
        "local_freeze_is_global_no_go": False,
        "theorem_truth_evaluated": False,
        "physics_promotion_authorized": False,
    }


def _nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def _match_reasons(block: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    family_id = str(block.get("family_id", "")).strip()
    family_hash = str(block.get("family_identity_sha256", "")).strip()
    assumption_hashes = {
        str(value).strip()
        for value in block.get("assumption_sha256es", [])
        if str(value).strip()
    }
    reasons: set[str] = set()
    for freeze in registry.get("freezes", []):
        if family_id and family_id == str(freeze.get("family_id", "")).strip():
            reasons.add("family_id")
        if family_hash and family_hash == str(freeze.get("family_identity_sha256", "")).strip():
            reasons.add("family_identity_sha256")
        frozen_assumptions = {
            str(value).strip()
            for value in freeze.get("assumption_sha256es", [])
            if str(value).strip()
        }
        if assumption_hashes & frozen_assumptions:
            reasons.add("assumption_sha256")
    return sorted(reasons)


def _default_evidence_verifier(path_text: str, expected_sha256: str) -> str:
    if not path_text or Path(path_text).is_absolute() or ".." in Path(path_text).parts:
        return "reopening evidence_path must be a repository-relative path"
    path = REPO_ROOT / path_text
    if not path.is_file():
        return f"reopening evidence_path does not exist: {path_text}"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected_sha256:
        return f"reopening evidence_sha256 does not match {path_text}"
    return ""


def _validate_reopening(
    reopening: dict[str, Any],
    *,
    family_id: str,
    job: dict[str, Any],
    evidence_verifier: Callable[[str, str], str],
) -> list[str]:
    errors: list[str] = []
    reopening_class = str(reopening.get("class", "")).strip()
    if reopening.get("requested") is not True:
        errors.append("repeated candidate-family route requires reopening.requested true")
    if reopening_class not in REOPENING_CLASSES:
        errors.append(
            "reopening.class must be one of " + ", ".join(sorted(REOPENING_CLASSES))
        )
    for field_name in ("evidence_id", "evidence_path", "evidence_sha256", "material_delta"):
        if not str(reopening.get(field_name, "")).strip():
            errors.append(f"reopening.{field_name} must be nonblank")
    evidence_sha = str(reopening.get("evidence_sha256", "")).strip()
    if evidence_sha and not SHA256_RE.fullmatch(evidence_sha):
        errors.append("reopening.evidence_sha256 must be a lowercase SHA-256 digest")
    if str(reopening.get("opens_exact_family_id", "")).strip() != family_id:
        errors.append("reopening.opens_exact_family_id must equal family_id")
    if reopening.get("automatic_adoption") is not False:
        errors.append("reopening.automatic_adoption must be false")
    if reopening.get("theorem_truth_inferred") is not False:
        errors.append("reopening.theorem_truth_inferred must be false")

    if reopening_class == "new_primitive":
        if not str(reopening.get("primitive_id", "")).strip():
            errors.append("new_primitive reopening requires primitive_id")
        if reopening.get("canonical_ontology_modified") is not False:
            errors.append("new_primitive reopening requires canonical_ontology_modified false")
        if reopening.get("materially_distinct") is not True:
            errors.append("new_primitive reopening requires materially_distinct true")
    elif reopening_class == "new_theorem":
        if not str(reopening.get("theorem_id", "")).strip():
            errors.append("new_theorem reopening requires theorem_id")
        if reopening.get("proposal_neutral") is not True:
            errors.append("new_theorem reopening requires proposal_neutral true")
    elif reopening_class == "new_variation_class":
        if not str(reopening.get("variation_class_id", "")).strip():
            errors.append("new_variation_class reopening requires variation_class_id")
        if not str(reopening.get("independent_physical_basis", "")).strip():
            errors.append(
                "new_variation_class reopening requires independent_physical_basis"
            )
        if reopening.get("materially_distinct") is not True:
            errors.append("new_variation_class reopening requires materially_distinct true")
    elif reopening_class == "protected_decision":
        if not str(reopening.get("human_gate_id", "")).strip():
            errors.append("protected_decision reopening requires human_gate_id")
        if reopening.get("protected_human_authority") is not True:
            errors.append(
                "protected_decision reopening requires protected_human_authority true"
            )
        if job.get("requires_human_gate") is not True:
            errors.append("protected_decision reopening requires AgentJob human gate")
    if reopening_class != "protected_decision" and reopening.get(
        "protected_human_authority"
    ) is not False:
        errors.append(
            "non-protected reopening requires protected_human_authority false"
        )

    evidence_path = str(reopening.get("evidence_path", "")).strip()
    if evidence_path and SHA256_RE.fullmatch(evidence_sha):
        evidence_error = evidence_verifier(evidence_path, evidence_sha)
        if evidence_error:
            errors.append(evidence_error)
    return errors


def evaluate_family_freeze_admission(
    job: dict[str, Any],
    *,
    expected_admission_path: str,
    created_at: str = "",
    registry: dict[str, Any] | None = None,
    evidence_verifier: Callable[[str, str], str] | None = None,
) -> dict[str, object]:
    """Evaluate route identity and evidence shape without evaluating scientific truth."""

    effective_created_at = str(created_at or job.get("created_at", "")).strip()
    active = policy_active(effective_created_at)
    if expected_admission_path != "physics":
        return {
            "status": "not_applicable",
            "required": False,
            "match_reasons": [],
            "errors": [],
            "theorem_truth_evaluated": False,
        }

    block = job.get("family_freeze_admission")
    if not isinstance(block, dict):
        if not active:
            return {
                "status": "legacy_readable",
                "required": False,
                "match_reasons": [],
                "errors": [],
                "theorem_truth_evaluated": False,
            }
        return {
            "status": "rejected",
            "required": True,
            "match_reasons": [],
            "errors": ["prospective physics AgentJob missing family_freeze_admission"],
            "theorem_truth_evaluated": False,
        }

    registry = registry or load_freeze_registry()
    evidence_verifier = evidence_verifier or _default_evidence_verifier
    errors: list[str] = []
    if str(block.get("schema_id", "")).strip() != SCHEMA_ID:
        errors.append(f"schema_id must be {SCHEMA_ID}")
    if str(block.get("policy_id", "")).strip() != POLICY_ID:
        errors.append(f"policy_id must be {POLICY_ID}")
    if not str(block.get("route_id", "")).strip():
        errors.append("route_id must be nonblank")

    family_id = str(block.get("family_id", "")).strip()
    family_hash = str(block.get("family_identity_sha256", "")).strip()
    assumption_hashes = block.get("assumption_sha256es")
    route_kind = str(block.get("route_kind", "")).strip()
    if not family_id:
        errors.append("family_id must be nonblank")
    if not SHA256_RE.fullmatch(family_hash):
        errors.append("family_identity_sha256 must be a lowercase SHA-256 digest")
    if not _nonempty_string_list(assumption_hashes):
        errors.append("assumption_sha256es must be a non-empty list")
    else:
        for assumption_hash in assumption_hashes:
            if not SHA256_RE.fullmatch(str(assumption_hash).strip()):
                errors.append(
                    "assumption_sha256es entries must be lowercase SHA-256 digests"
                )
                break
    if route_kind not in ROUTE_KINDS:
        errors.append("route_kind must be one of " + ", ".join(sorted(ROUTE_KINDS)))

    authority = block.get("authority_limits")
    if not isinstance(authority, dict):
        errors.append("authority_limits must be a mapping")
    else:
        for field_name, expected in AUTHORITY_LIMITS.items():
            if authority.get(field_name) is not expected:
                errors.append(f"authority_limits.{field_name} must be {str(expected).lower()}")

    match_reasons = _match_reasons(block, registry)
    declared_matches = block.get("detected_match_basis")
    declared_matches = (
        sorted(str(value).strip() for value in declared_matches if str(value).strip())
        if isinstance(declared_matches, list)
        else []
    )
    if declared_matches != match_reasons:
        errors.append(
            "detected_match_basis must equal independently computed match reasons"
        )

    reopening = block.get("reopening")
    reopening = reopening if isinstance(reopening, dict) else {}
    if not match_reasons:
        if reopening.get("requested") is not False:
            errors.append("unfrozen route requires reopening.requested false")
        status = "admitted_unfrozen"
    elif route_kind == "rename_or_repackage":
        errors.append("renamed or repackaged frozen-family route is barred")
        status = "rejected"
    elif route_kind in DISTINCT_BRANCH_ROUTE_KINDS:
        distinct = block.get("distinct_branch")
        if not isinstance(distinct, dict):
            errors.append("matched distinct branch requires distinct_branch mapping")
        else:
            if not str(distinct.get("branch_identity", "")).strip():
                errors.append("distinct_branch.branch_identity must be nonblank")
            if not str(distinct.get("material_difference_basis", "")).strip():
                errors.append("distinct_branch.material_difference_basis must be nonblank")
            if distinct.get("reconstructs_frozen_candidate") is not False:
                errors.append(
                    "distinct_branch.reconstructs_frozen_candidate must be false"
                )
            if not _nonempty_string_list(distinct.get("expected_artifact_paths")):
                errors.append(
                    "distinct_branch.expected_artifact_paths must be a non-empty list"
                )
        if reopening.get("requested") is not False:
            errors.append(
                "distinct investigation preserves the freeze and requires reopening.requested false"
            )
        status = "admitted_distinct_branch"
    else:
        if not reopening:
            errors.append("repeated candidate-family route requires reopening mapping")
        else:
            errors.extend(
                _validate_reopening(
                    reopening,
                    family_id=family_id,
                    job=job,
                    evidence_verifier=evidence_verifier,
                )
            )
        status = "admitted_reopened"

    if errors:
        status = "rejected"
    return {
        "status": status,
        "required": active,
        "route_kind": route_kind,
        "match_reasons": match_reasons,
        "reopening_class": str(reopening.get("class", "")).strip(),
        "errors": errors,
        "theorem_truth_evaluated": False,
        "global_no_go_inferred": False,
    }
