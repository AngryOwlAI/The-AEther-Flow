#!/usr/bin/env python3
"""Validate the tracked research-control spine."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter
except ImportError:  # pragma: no cover - package import path for tests
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml, load_frontmatter


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
REGISTRY_DIR = REPO_ROOT / "registries"
CONTROL_DIR = REPO_ROOT / "research_control"
PROJECT_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
if str(PROJECT_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_CONTROL_SCRIPT_DIR))

from project_improvement_handoff_validation import (  # noqa: E402
    conditional_checkpoint_sidecar_paths,
    validate_project_improvement_handoffs as validate_project_improvement_handoff_records,
)
from scripts.research_control.physics_payload_admission import (  # noqa: E402
    evaluate_agent_job_admission,
)
from scripts.research_control.dual_budget_policy import (  # noqa: E402
    evaluate_dual_budget_allocation,
    evaluate_dual_budget_completion,
)
from scripts.research_control.ordinary_route_guard import (  # noqa: E402
    evaluate_agent_job_route_admission,
    evaluate_research_handoff_guard,
)
from scripts.validation.models import (  # noqa: E402
    ValidationFinding as CommonValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (  # noqa: E402
    DEFAULT_RECEIPT_ROOT,
    add_reporting_arguments,
    emit_report,
    options_from_namespace,
)

try:
    import validate_claim_language as claim_language_linter  # noqa: E402
except ImportError:  # pragma: no cover - reported as a validator error when needed
    claim_language_linter = None  # type: ignore[assignment]

try:
    import validate_compact_current_frontier_v16 as compact_frontier_validator  # noqa: E402
except ImportError:  # pragma: no cover - reported as a validator error when needed
    compact_frontier_validator = None  # type: ignore[assignment]

RESOLVER_SNAPSHOT_REQUIRED_FIELDS = (
    "status",
    "boundary",
    "reason",
    "resolver_is_advisory",
    "hard_checkpoint_gate",
    "checkpoint_gate_source",
    "selected_signal",
    "open_signals",
    "change_classification",
)

ROLE_COLUMNS = [
    "role_id",
    "version",
    "role_name",
    "role_kind",
    "role_contract_path",
    "authority_level",
    "status",
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
    "default_output_format",
    "default_validators",
    "created_at",
    "updated_at",
    "notes",
]

DECISION_COLUMNS = [
    "decision_id",
    "task_id",
    "decision_path",
    "director_version",
    "decision_type",
    "selected_role_id",
    "selected_role_version",
    "agent_job_id",
    "status",
    "supersedes_decision_id",
    "requires_human_gate",
    "created_at",
    "activated_at",
    "completed_at",
    "validation_status",
    "notes",
]

JOB_COLUMNS = [
    "job_id",
    "task_id",
    "decision_id",
    "role_id",
    "role_version",
    "job_path",
    "completion_path",
    "status",
    "allowed_write_paths",
    "output_paths",
    "validation_status",
    "created_at",
    "started_at",
    "completed_at",
    "requires_human_gate",
    "notes",
]

ROLE_EXECUTION_COLUMNS = [
    "execution_role_ref",
    "role_execution_kind",
    "task_id",
    "agent_job_id",
    "record_path",
    "base_role_id",
    "base_role_version",
    "provisional_role_name",
    "authority_delta_summary",
    "added_constraints",
    "removed_permissions",
    "expanded_permissions",
    "allowed_write_paths",
    "requires_human_gate",
    "expires_after",
    "justification",
    "non_reusable_until_registered",
    "validation_status",
    "created_at",
    "updated_at",
    "notes",
]

TASK_COLUMNS = [
    "task_id",
    "task_path",
    "task_type",
    "status",
    "current_decision_id",
    "current_job_id",
    "parent_task_id",
    "created_at",
    "updated_at",
    "closed_at",
    "closure_status",
    "requires_human_gate",
    "notes",
]

CLAIM_COLUMNS = [
    "claim_boundary_id",
    "scope",
    "applies_to_path",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "authority_source_path",
    "status",
    "created_at",
    "updated_at",
    "notes",
]

COUNTERMODEL_OBLIGATION_COLUMNS = [
    "obligation_id",
    "task_id",
    "artifact_path",
    "theorem_family",
    "countermodel_slot",
    "status",
    "result_artifact",
    "obstruction_id",
    "scope",
    "global_no_go_claimed",
    "created_at",
    "notes",
]

REGISTRY_COLUMNS = {
    "AGENT_ROLE_REGISTRY.csv": ROLE_COLUMNS,
    "ROLE_EXECUTION_REGISTRY.csv": ROLE_EXECUTION_COLUMNS,
    "DIRECTOR_DECISION_REGISTRY.csv": DECISION_COLUMNS,
    "AGENT_JOB_REGISTRY.csv": JOB_COLUMNS,
    "RESEARCH_TASK_REGISTRY.csv": TASK_COLUMNS,
    "CLAIM_BOUNDARY_REGISTRY.csv": CLAIM_COLUMNS,
    "COUNTERMODEL_OBLIGATION_REGISTRY.csv": COUNTERMODEL_OBLIGATION_COLUMNS,
}

BOOLEAN_FIELDS = {
    "may_execute_autonomously",
    "may_create_outputs",
    "may_modify_sources",
    "may_promote_claims",
    "requires_human_gate",
    "non_reusable_until_registered",
    "global_no_go_claimed",
}

SEMICOLON_FIELDS = {
    "default_validators",
    "allowed_write_paths",
    "output_paths",
    "allowed_claims",
    "forbidden_claims",
    "requires_gate_for",
    "added_constraints",
    "removed_permissions",
    "expanded_permissions",
}

ROLE_EXECUTION_KINDS = {
    "registered_role",
    "task_overlay",
    "one_job_provisional_role",
}

PROTECTED_AUTHORITY_MARKERS = (
    "claim promotion",
    "promote claims",
    "physics claim promotion",
    "canonical ontology",
    "ontology edit",
    "benchmark promotion",
    "benchmark status",
    "gate chair",
    "gate verdict",
    "permanent role registration",
    "role registration",
    "register as a permanent role",
    "register as permanent role",
)

GLOBALLY_BROAD_PATTERNS = {
    "*",
    "**",
    "**/*",
    ".agents/**",
    "html/**",
    "ontology/**",
    "research_control/**",
    "research_control/tasks/**",
    "wiki/**",
}

CURRENT_FRONTIER_REPAIR_ROUTE = (
    "run one bounded current-frontier synchronization repair packet under "
    "continue-research before proceeding"
)

IMMUTABLE_HISTORICAL_ORDINARY_ROUTE_GUARD_COMPATIBILITY = {
    "handoff-0861.yaml": {
        "sha256": "dcdbdb05d1fcf50e772321a9319f2f9dc5685e5138e14e61c3fd85241a379e2f",
        "evaluation_id": "ORE-HANDOFF-0861",
        "declared_count": 1,
        "errors": ("consecutive_project_system_task_count_mismatch",),
    },
}

PHYSICS_PAYLOAD_RATIO_POLICY_ID = "physics_payload_ratio_policy_v1"
PHYSICS_PAYLOAD_RATIO_THRESHOLD_DEFAULT = 3
PHYSICS_PAYLOAD_RATIO_REQUIRED_TASK_TYPES = {
    "theorem_candidate",
    "countermodel",
    "finite_witness",
    "obstruction_with_proof_sketch",
    "source_primitive_requirement",
    "candidate_construction",
}
PHYSICS_PAYLOAD_RATIO_EXCEPTIONS = {
    "claim_boundary_hard_failure",
    "failing_ci",
    "human_gate_required",
    "registry_corruption",
    "security_or_integrity_repair",
}
PHYSICS_PAYLOAD_RATIO_PROJECT_SYSTEM_TOKENS = {
    "checkpoint",
    "dashboard",
    "documentation",
    "handoff",
    "memory",
    "metrics",
    "project_system",
    "registry",
    "renderer",
    "route_history",
    "schema",
    "sidecar",
    "support",
    "tooling",
    "validation",
    "validator",
}
PHYSICS_PAYLOAD_RATIO_NO_DELTA_STATUS_TOKENS = {
    "no_physics_delta",
    "no physics delta",
    "support-only",
    "support_only",
    "validator_update_no_physics_delta",
}
PHYSICS_PAYLOAD_RATIO_DELTA_CLAIM_KEYS = (
    "physics_delta_claimed",
    "physics_delta_created",
    "physics_delta_allowed",
    "physics_promotion_authorized",
    "proof_authority",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
)

CURRENT_FRONTIER_ACTIVE_FIELD_MAP = {
    "Active task ID": "active_task_id",
    "Latest handoff ID": "latest_handoff_id",
    "Current status": "current_status",
    "Target derivation milestone": "target_derivation_milestone",
    "Current burden": "current_burden",
    "Next recommended action": "next_recommended_action",
}
CURRENT_FRONTIER_BIFURCATION_FIELD_MAP = {
    "Latest research task ID": "latest_research_task_id",
    "Latest research handoff ID": "latest_research_handoff_id",
    "Latest research next action": "latest_research_next_action",
    "Latest project-system task ID": "latest_project_system_task_id",
    "Latest project-system status": "latest_project_system_status",
    "Latest project-system sidecar task ID": "latest_project_system_sidecar_task_id",
    "Latest project-system sidecar status": "latest_project_system_sidecar_status",
    "Sidecar supersedes research handoff": "sidecar_supersedes_research_handoff",
    "Next research route source": "next_research_route_source",
}
ACTIVE_STATE_BIFURCATION_FIELDS = tuple(CURRENT_FRONTIER_BIFURCATION_FIELD_MAP.values())
PROTECTED_SIDECAR_CLAIM_FLAGS = {
    "physics_promotion_authorized",
    "canonical_ontology_edit_authorized",
    "source_law_adopted",
    "general_EqSrc_discharged",
    "RetainH_adopted",
    "GenH_adopted",
    "source_detector_readout_semantics_adopted",
    "coupling_law_adopted",
    "matter_coupling_derived",
    "matter_coupling_adopted",
    "stress_energy_semantics_imported",
    "stress_energy_tensor_constructed",
    "matter_action_imported",
    "einstein_equations_derived",
    "benchmark_promoted",
    "external_outreach_authorized",
    "proof_authority",
    "completed_derivation_claimed",
}
PROJECT_IMPROVEMENT_HANDOFF_DIR = CONTROL_DIR / "project_improvement_handoffs"
MIXED_MARKDOWN_PATHS = {
    "README.md",
    "AGENTS.md",
    "research_control/README.md",
    "research_control/AGENTS.md",
}
CONTROL_MARKDOWN_PATTERNS = (
    ".agents/roles/**/*.md",
    ".agents/schemas/*.md",
    ".agents/schemas/**/*.md",
    ".codex/skills/*/SKILL.md",
)
AUTHORITY_MARKER_RE = re.compile(r"<!--\s*authority:\s*(explanatory|control)\s*-->")
HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

FORBIDDEN_PHRASES = [
    "GR derived from ontology",
    "exact GR recovered from ontology",
    "GR_DERIVED_FROM_ANTHOLOGY",
]

SAFE_BOUNDARY_MARKERS = (
    "forbidden",
    "not established",
    "not authorized",
    "without gate",
    "compatibility-only",
    "claim boundary",
    "blocked claim",
    "open derivation",
)

LOOP_CONTROL_POLICY_ACTIVATED_AT = "2026-06-16T19:17:22Z"
PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT = "2026-06-17T04:08:16Z"
THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT = "2026-06-17T04:29:31Z"
GR_DERIVATION_ROADMAP_POLICY_ACTIVATED_AT = "2026-06-17T15:46:25Z"
MEMORY_PREFLIGHT_REQUIRED_AFTER = "2026-06-18T15:33:00Z"
VALIDATION_SCHEMA_SPLIT_ACTIVE_AFTER = "2026-07-01T23:20:00Z"

VALIDATION_LAYER_NAMES = (
    "pre_execution",
    "completion_internal",
    "post_write",
    "post_checkpoint",
    "renderer",
    "memory_bootstrap",
    "claim_language_linter",
)
VALIDATION_LAYER_STATUS_VALUES = {
    "PASS",
    "PASS_WITH_WARNINGS",
    "PENDING",
    "FAIL",
    "NOT_RUN",
    "NOT_APPLICABLE",
}
AUTHORIZATION_LAYER_BOOLEAN_FIELDS = (
    "protected_scoped_gate_review_authorized",
    "downstream_physics_promotion_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
)
AUTHORIZATION_LAYER_SCOPE_FIELD = "protected_scoped_gate_review_scope"
AUTHORIZATION_LAYER_SOURCE_FIELDS = {
    "protected_scoped_gate_review_authorized": "protected_scoped_gate_review_authority_source_path",
    "downstream_physics_promotion_authorized": "downstream_physics_promotion_authority_source_path",
    "benchmark_promotion_authorized": "benchmark_promotion_authority_source_path",
    "completed_derivation_authorized": "completed_derivation_authority_source_path",
}
MUTABLE_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS = {
    "MD-AETHER-FLOW-PHYSICS-PROGRAM-PUBLICATION-BRIEF",
    "MD-AGENTS",
    "MD-CLAIM-GATES-PUBLICATION-BRIEF",
    "MD-CONTRIBUTING",
    "MD-EXACT-GR-BENCHMARK-BOUNDARY-PUBLICATION-BRIEF",
    "MD-GITHUB-FACING-AETHER-FLOW-PHYSICS-PROGRAM-EXPLAINER",
    "MD-GITHUB-FACING-AETHER-FLOW-ONTOLOGY-EXPLAINER",
    "MD-GITHUB-FACING-CLAIM-GATES-EXPLAINER",
    "MD-GITHUB-FACING-EXACT-GR-BENCHMARK-BOUNDARY-EXPLAINER",
    "MD-GITHUB-FACING-GR-DERIVATION-ROADMAP-EXPLAINER",
    "MD-GITHUB-FACING-NEGATIVE-RESULTS-AND-OBSTRUCTIONS-EXPLAINER",
    "MD-GITHUB-FACING-PROJECT-OVERVIEW-EXPLAINER",
    "MD-GITHUB-FACING-PROOF-STATE-DASHBOARD-EXPLAINER",
    "MD-GITHUB-FACING-SOURCE-AUTHORITY-EXPLAINER",
    "MD-GR-DERIVATION-ROADMAP-PUBLICATION-BRIEF",
    "MD-HTML-SPEC-AETHER-FLOW-PHYSICS-PROGRAM-EXPLAINER",
    "MD-HTML-SPEC-AETHER-FLOW-ONTOLOGY-EXPLAINER",
    "MD-HTML-SPEC-CLAIM-GATES-EXPLAINER",
    "MD-HTML-SPEC-EXACT-GR-BENCHMARK-BOUNDARY-EXPLAINER",
    "MD-HTML-SPEC-GR-DERIVATION-ROADMAP-EXPLAINER",
    "MD-HTML-SPEC-NEGATIVE-RESULTS-AND-OBSTRUCTIONS-EXPLAINER",
    "MD-HTML-SPEC-PROJECT-OVERVIEW-EXPLAINER",
    "MD-HTML-SPEC-PROOF-STATE-DASHBOARD-EXPLAINER-SPEC",
    "MD-HTML-SPEC-SOURCE-AUTHORITY-EXPLAINER",
    "MD-NEGATIVE-RESULTS-AND-OBSTRUCTIONS-PUBLICATION-BRIEF",
    "MD-PROOF-STATE-DASHBOARD-PUBLICATION-BRIEF",
    "MD-PROJECT-OVERVIEW-PUBLICATION-BRIEF",
    "MD-README",
    "MD-README-TESTS",
    "MD-RESEARCH-CONTROL-CURRENT-FRONTIER",
    "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY",
    "MD-RESEARCH-CONTROL-DESIGN-GR-DERIVATION-BURDEN-MAP",
    "MD-RESEARCH-CONTROL-DESIGN-EPISTEMIC-CATEGORY-GLOSSARY",
    "MD-RESEARCH-CONTROL-DESIGN-CI-VALIDATION-SHARD-POLICY-V1",
    "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16",
    "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-PROFILE-POLICY-V1",
    "MD-RESEARCH-CONTROL-TASKS-RT-20260722-015-ORDINARY-ROUTE-GUARD-POLICY-V1",
    "MD-SCHEMA-AGENT-JOB-SCHEMA",
    "MD-SKILL-CONTINUE-RESEARCH",
    "MD-SKILL-CONTINUE-RESEARCH-CONTINUE-GOAL",
    "MD-SKILL-CONTINUE-RESEARCH-GOAL",
    "MD-SKILL-CONTINUE-RESEARCH-GOAL-SCHEMA",
    "MD-SKILL-IMPROVE-PROJECT-SYSTEM",
    "MD-SKILL-PROJECT-MEMORY-SYSTEM",
    "MD-SKILL-USER-MODIFIED-PROJECT",
    "TEX-ONTOLOGY-AETHER-FLOW-DYNAMICS",
    "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS",
    "TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY",
}
SELF_REFERENTIAL_GENERATED_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS = {
    "MD-RESEARCH-CONTROL-TASK-INDEX",
}

MEMORY_PREFLIGHT_SOURCE_REGISTRIES = {
    "MARKDOWN_SOURCE_REGISTRY.csv",
    "TEX_SOURCE_REGISTRY.csv",
    "PDF_DERIVATIVE_REGISTRY.csv",
    "HTML_EXPLAINER_REGISTRY.csv",
}

DISTANCE_TO_GR_LEDGER_COLUMNS = [
    "burden_id",
    "milestone",
    "required_object",
    "current_status",
    "blocking_burden",
    "accept_criteria",
    "failure_or_freeze_criteria",
    "last_evidence_path",
    "updated_at",
    "notes",
    "control_status",
    "mathematical_status",
    "physical_status",
    "promotion_status",
    "overread_guard",
]

DISTANCE_TO_GR_LEDGER_STATUS_VALUES = {
    "not started",
    "draft object exists",
    "constructive witness exists",
    "smuggling audit passed",
    "Refuter stress passed",
    "human-gated",
    "accepted",
    "frozen negative",
    "blocked by missing primitive",
}

DISTANCE_TO_GR_LEDGER_LAYER_COLUMNS = (
    "control_status",
    "mathematical_status",
    "physical_status",
    "promotion_status",
    "overread_guard",
)

DISTANCE_TO_GR_CONTROL_STATUS_VALUES = {
    "accepted_as_scoped_evidence",
    "accepted_as_scoped_evidence_precondition",
    "accepted_as_scoped_source_object",
    "accepted_as_source_extension_data",
    "audit_passed",
    "blocked",
    "construction_recorded",
    "constructive_witness_recorded",
    "draft_control_object_exists",
    "frozen_negative",
    "gate_review_completed",
    "human_gated",
    "not_started",
    "refuter_stress_passed",
}

DISTANCE_TO_GR_MATHEMATICAL_STATUS_VALUES = {
    "conditional_theorem_candidate",
    "constructive_witness",
    "countermodel",
    "definition_only",
    "definition_only_or_draft_object",
    "dynamics_action_or_variation_missing",
    "finite_local_witness",
    "general_equivalence_theorem_missing",
    "general_theorem_missing",
    "no_mathematical_object",
    "parameterized_finite_local_witness_precondition",
    "parameterized_witness_precondition",
    "primitive_missing",
    "protected_verdict_missing",
    "scoped_obstruction",
    "scoped_source_extension_geff_object",
    "scoped_source_extension_object",
    "scoped_source_only_adopted_object",
    "selector_data_source_extension",
    "source_only_adopted_object",
    "tag_removal_obstruction",
    "upstream_burdens_missing",
}

DISTANCE_TO_GR_PHYSICAL_STATUS_VALUES = {
    "benchmark_compatible_interpretive_boundary_only",
    "downstream_gr_blocked",
    "human_gate_required_before_physical_reading",
    "local_exact_branch_only",
    "local_toy_route_frozen_not_global_theory_rejection",
    "no_benchmark_closure",
    "no_canonical_ontology_adoption",
    "no_exact_gr_benchmark_promotion",
    "no_field_equation_derivation",
    "no_generator_law_adoption",
    "no_physical_interpretation_authorized",
    "no_retention_law_adoption",
    "not_benchmark_promotion",
    "not_detector_semantics_not_matter_coupling",
    "not_einstein_equations",
    "not_matter_coupling",
    "not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics",
    "not_stress_energy",
    "not_target_manifold_not_metric_not_gr_derivation",
    "not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations",
}

DISTANCE_TO_GR_PROMOTION_STATUS_VALUES = {
    "draft_control_only",
    "frozen_negative_no_promotion",
    "human_gate_required",
    "no_downstream_gr_promotion",
    "none",
    "scoped_source_evidence_only",
    "scoped_source_object_only",
}

DISTANCE_TO_GR_OVERREAD_GUARD_VALUES = {
    "no_benchmark_gate_chair_closure",
    "no_benchmark_promotion",
    "no_canonical_ontology_edit",
    "no_completed_derivation",
    "no_coupling_law_adoption",
    "no_detector_semantics",
    "no_einstein_equations",
    "no_future_source_extension_impossibility",
    "no_geff_scope_expansion",
    "no_global_theory_rejection",
    "no_matter_action",
    "no_matter_coupling_adoption",
    "no_matter_coupling_derivation",
    "no_metricdata_e_adoption",
    "no_source_law_adoption",
    "no_stress_energy_semantics",
    "no_stress_energy_tensor",
    "no_unscoped_geff_adoption",
}

COUNTERMODEL_OBLIGATION_POLICY_ACTIVE_AFTER = "2026-07-08T00:22:57Z"
COUNTERMODEL_OBLIGATION_THEOREM_MARKERS = (
    " theorem",
    "theorem_",
    "theorem-",
    "proof attempt",
    "theorem attempt",
    "conditional theorem",
    "source-side theorem",
)
COUNTERMODEL_OBLIGATION_FAMILIES = {
    "eqsrc",
    "matter_coupling",
    "detector_readout",
    "toy_model",
    "other",
}
COUNTERMODEL_OBLIGATION_STATUS_VALUES = {
    "filled",
    "pending",
    "waived_by_ddr",
    "not_applicable_by_ddr",
    "deferred_by_ddr",
}
COUNTERMODEL_REQUIRED_SLOTS_BY_FAMILY = {
    "eqsrc": {
        "missing_inverse_countermodel",
        "missing_composition_countermodel",
        "invariant_ledger_not_family_stable_countermodel",
        "target_import_needed_countermodel",
        "RetainH_needed_countermodel",
        "GenH_needed_countermodel",
    },
    "matter_coupling": {
        "source_matter_semantics_missing_countermodel",
        "coupling_law_gap_countermodel",
        "MetricData_or_g_eff_overread_countermodel",
        "stress_energy_import_countermodel",
        "matter_action_import_countermodel",
        "benchmark_dependency_countermodel",
    },
    "detector_readout": {
        "detector_semantics_import_countermodel",
        "readout_equivalence_nonconservation_countermodel",
        "rr_e_collapse_countermodel",
        "calibration_import_countermodel",
        "no_target_certificate_overread_countermodel",
    },
    "toy_model": {
        "missing_transport_countermodel",
        "missing_invariance_countermodel",
        "missing_factorization_countermodel",
        "finite_variation_fragility_countermodel",
        "empty_selector_countermodel",
        "support_tool_overread_countermodel",
    },
}
COUNTERMODEL_HARD_OVERREAD_PATTERNS = (
    re.compile(
        r"\b(?:local\s+)?countermodel\s+"
        r"(?:proves|establishes|means|is)\s+"
        r"(?:a\s+)?(?:program-wide|global)\s+no-go\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:local\s+)?countermodel\s+"
        r"(?:proves|establishes|means)\s+"
        r"(?:future\s+)?source-extension\s+impossible\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:local\s+)?countermodel\s+"
        r"(?:proves|establishes|means)\s+theory\s+rejected\b",
        re.IGNORECASE,
    ),
)

DISTANCE_TO_GR_FIELD_VALUE_SETS = {
    "control_status": DISTANCE_TO_GR_CONTROL_STATUS_VALUES,
    "mathematical_status": DISTANCE_TO_GR_MATHEMATICAL_STATUS_VALUES,
    "physical_status": DISTANCE_TO_GR_PHYSICAL_STATUS_VALUES,
    "promotion_status": DISTANCE_TO_GR_PROMOTION_STATUS_VALUES,
}

DISTANCE_TO_GR_ACCEPTED_CONTROL_STATUS_VALUES = {
    "accepted_as_scoped_evidence",
    "accepted_as_scoped_evidence_precondition",
    "accepted_as_scoped_source_object",
    "accepted_as_source_extension_data",
    "gate_review_completed",
}

DISTANCE_TO_GR_SCOPED_PROMOTION_STATUS_VALUES = {
    "scoped_source_evidence_only",
    "scoped_source_object_only",
}

DISTANCE_TO_GR_GENERATED_STATUS_AUTHORITY_PATHS = {
    "research_control/current_frontier.md",
}

DISTANCE_TO_GR_GENERATED_STATUS_AUTHORITY_PREFIXES = (
    ".local/",
    "output/",
    "wiki/",
)

DISTANCE_TO_GR_REQUIRED_GUARD_TOKENS = {
    "resp_lc": {
        "no_canonical_ontology_edit",
        "no_matter_coupling_derivation",
        "no_detector_semantics",
        "no_einstein_equations",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "m_src": {
        "no_metricdata_e_adoption",
        "no_geff_scope_expansion",
        "no_matter_coupling_derivation",
        "no_einstein_equations",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "g_eff": {
        "no_source_law_adoption",
        "no_metricdata_e_adoption",
        "no_unscoped_geff_adoption",
        "no_matter_coupling_derivation",
        "no_einstein_equations",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "matter_coupling": {
        "no_source_law_adoption",
        "no_metricdata_e_adoption",
        "no_geff_scope_expansion",
        "no_coupling_law_adoption",
        "no_matter_coupling_derivation",
        "no_matter_coupling_adoption",
        "no_stress_energy_semantics",
        "no_stress_energy_tensor",
        "no_matter_action",
        "no_detector_semantics",
        "no_einstein_equations",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "einstein_equations": {
        "no_einstein_equations",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "benchmark_promotion": {
        "no_benchmark_promotion",
        "no_benchmark_gate_chair_closure",
        "no_completed_derivation",
    },
    "gate_chair_status": {
        "no_benchmark_gate_chair_closure",
        "no_benchmark_promotion",
        "no_completed_derivation",
    },
    "finite_toy_metric_response": {
        "no_geff_scope_expansion",
        "no_global_theory_rejection",
        "no_future_source_extension_impossibility",
        "no_completed_derivation",
    },
}

FRONTIER_INVENTORY_OBJECT_ID = "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY"
FRONTIER_INVENTORY_PATH = "research_control/design/frontier_theorem_inventory.md"
FRONTIER_INVENTORY_REQUIRED_FIELDS = [
    "frontier_item_id",
    "frontier_item_class",
    "object_or_claim_name",
    "status_layer_summary",
    "source_artifact_path",
    "source_authority_type",
    "assumptions",
    "definitions_used",
    "statement_or_decision",
    "mathematical_conclusion",
    "physical_non_conclusions",
    "allowed_reuse",
    "blocked_reuse",
    "dependency_items",
    "missing_theorem_or_primitive",
    "candidate_next_task",
    "overread_guard",
    "external_review_notes",
]
FRONTIER_INVENTORY_ALLOWED_CLASSES = {
    "accepted_scoped_object",
    "definition",
    "frozen_negative_route",
    "gate_decision",
    "missing_theorem",
    "obstruction",
    "source_extension_evidence",
    "theorem",
    "witness",
}
FRONTIER_INVENTORY_ALLOWED_AUTHORITY_TYPES = {
    "claim_boundary_registry_row",
    "distance_to_gr_ledger_row",
    "gate_chair_artifact",
    "generated_summary_paired_with_source",
    "refuter_artifact",
    "registered_markdown_control",
    "registered_tex_artifact",
    "research_task_registry_row",
}
FRONTIER_INVENTORY_GENERATED_SOURCE_PATHS = {
    "research_control/current_frontier.md",
}
FRONTIER_INVENTORY_GENERATED_SOURCE_PREFIXES = (
    ".local/",
    "output/",
    "wiki/",
)
FRONTIER_INVENTORY_HIGH_RISK_GUARDS = {
    "matter": {"no_matter_coupling_derivation", "no_matter_coupling_adoption"},
    "coupling": {"no_matter_coupling_derivation", "no_matter_coupling_adoption"},
    "stress-energy": {"no_stress_energy_semantics", "no_stress_energy_tensor"},
    "stress_energy": {"no_stress_energy_semantics", "no_stress_energy_tensor"},
    "einstein": {"no_einstein_equations"},
    "benchmark": {"no_benchmark_promotion"},
    "g_eff": {"no_geff_scope_expansion", "no_unscoped_geff_adoption"},
    "metricdata": {"no_metricdata_e_adoption"},
}
FRONTIER_INVENTORY_FROZEN_GUARDS = {
    "no_global_theory_rejection",
    "no_future_source_extension_impossibility",
}

DISTANCE_TO_GR_EXPECTED_LAYER_VALUES = {
    "resp_lc": {
        "control_status": "accepted_as_source_extension_data",
        "mathematical_status": "selector_data_source_extension",
        "physical_status": "not_detector_semantics_not_matter_coupling",
        "promotion_status": "scoped_source_object_only",
    },
    "m_src": {
        "control_status": "gate_review_completed",
        "mathematical_status": "scoped_source_only_adopted_object",
        "physical_status": "not_target_manifold_not_metric_not_gr_derivation",
        "promotion_status": "scoped_source_object_only",
    },
    "g_eff": {
        "control_status": "gate_review_completed",
        "mathematical_status": "scoped_source_extension_geff_object",
        "physical_status": "not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations",
        "promotion_status": "scoped_source_object_only",
    },
    "matter_coupling": {
        "control_status": "accepted_as_scoped_evidence_precondition",
        "mathematical_status": "parameterized_finite_local_witness_precondition",
        "physical_status": "not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics",
        "promotion_status": "scoped_source_evidence_only",
    },
    "einstein_equations": {
        "control_status": "not_started",
        "mathematical_status": "dynamics_action_or_variation_missing",
        "physical_status": "no_field_equation_derivation",
        "promotion_status": "none",
    },
    "benchmark_promotion": {
        "control_status": "blocked",
        "mathematical_status": "upstream_burdens_missing",
        "physical_status": "no_exact_gr_benchmark_promotion",
        "promotion_status": "none",
    },
    "gate_chair_status": {
        "control_status": "human_gated",
        "mathematical_status": "protected_verdict_missing",
        "physical_status": "no_benchmark_closure",
        "promotion_status": "human_gate_required",
    },
    "finite_toy_metric_response": {
        "control_status": "frozen_negative",
        "mathematical_status": "tag_removal_obstruction",
        "physical_status": "local_toy_route_frozen_not_global_theory_rejection",
        "promotion_status": "frozen_negative_no_promotion",
    },
}

GR_DERIVATION_MILESTONES = (
    "source_ontology",
    "source_equivalence_eqsrc",
    "source_localization_obsloc_lc",
    "response_localization_resp_lc",
    "source_manifold_m_src",
    "effective_metric_g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
    "finite_toy_metric_response",
)

DISTANCE_TO_GR_LEDGER_REQUIRED_BURDENS = (
    "source_ontology_primitives",
    "source_equivalence_eqsrc",
    "retain_h",
    "gen_h",
    "obsloc_lc",
    "resp_lc",
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "finite_variation_robustness",
    "benchmark_promotion",
    "gate_chair_status",
    "finite_toy_metric_response",
)

PHYSICS_ROLE_IDS = {
    "ontology-formalizer",
    "candidate-constructor",
    "refuter",
    "smuggling-auditor",
    "theoretical-continuation-selector",
}

PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES = {
    "canonical_ontology_write",
    "benchmark_promotion",
    "candidate_reconstruction",
    "gate_chair_verdict",
    "completed_derivation_claim",
    "global_theory_rejection",
    "generated_derivative_authority",
}

PHYSICS_JOB_FORBIDDEN_WRITE_PREFIXES = (
    "ontology/",
    "manuscripts/",
    "html/",
)

PROTECTED_CANONICAL_INTEGRATION_SCHEMA_ID = (
    "protected_canonical_ontology_integration_admission_v1"
)
PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID = "P4-T06"
PROTECTED_CANONICAL_INTEGRATION_TASK_PATH = (
    "research_control/tasks/RT-20260724-010/00_TASK.yaml"
)
PROTECTED_CANONICAL_INTEGRATION_TASK_HISTORICAL_SHA256 = (
    "dea29e8ec6ba79a8c17cf0e2c0ae0be7a275db9845cae16f4f07eea508ada6ff"
)
PROTECTED_CANONICAL_INTEGRATION_TASK_METADATA_REPAIR_SHA256 = (
    "d105660a4fa96c961820f53a7904a5737c764de488a28e782a628cbdc67b46ed"
)
PROTECTED_CANONICAL_INTEGRATION_TASK_METADATA_REPAIR = {
    "title": "Integrate the selected ontology regime and retire hybrid language",
    "task_taxonomy": {
        "schema_id": "v21_task_taxonomy_v1",
        "work_kind": "integration_or_selection",
        "milestone": "source_ontology",
        "candidate_family": "unknown",
        "result_kind": "completed_or_precisely_blocked",
        "authority": "science_draft",
        "scope": "scientific",
    },
}
PROTECTED_CANONICAL_INTEGRATION_PATHS = frozenset(
    {
        "ontology/tex/aether_flow_foundations.tex",
        "ontology/tex/aether_flow_dynamics.tex",
        "ontology/tex/aether_flow_geometry.tex",
        "ontology/pdfs/aether_flow_foundations.pdf",
        "ontology/pdfs/aether_flow_dynamics.pdf",
        "ontology/pdfs/aether_flow_geometry.pdf",
    }
)

DISTANCE_TO_GR_REQUIRED_BURDENS = (
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "Finite variation robustness",
    "Concrete negative witnesses",
    "Observer normal/readout orbit",
    "Effective Lorentzian metric",
    "Universal matter coupling",
    "Einstein equations",
    "Benchmark promotion",
    "Gate Chair review",
    "Current line hard-fail",
)

ROADMAP_DISTANCE_TO_GR_REQUIRED_BURDENS = (
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "RetainH",
    "GenH",
    "ObsLoc_lc",
    "Resp_lc",
    "M_src",
    "g_eff",
    "matter coupling",
    "Einstein equations",
    "finite-variation robustness",
    "benchmark promotion",
    "Gate Chair status",
    "current route freeze or hard-fail status",
)

LOOP_RISK_DECISION_CATEGORIES = {
    "concrete_witness_path",
    "source_side_irrelevance_theorem_path",
    "bridge_facing_candidate_path",
    "repeated_unmet_burdens_no_new_payload",
    "scoped_obstruction",
}

BRIDGE_OR_FAIL_ROUTES = {
    "candidate_constructor_bridge_attempt",
    "ontology_formalizer_concrete_witness_construction",
    "refuter_scoped_no_go_or_obstruction",
    "gate_chair_closure_or_suspension_proposal",
    "human_gated_ontology_change_required",
    "theoretical_decision_role_selection",
}

LEGACY_BRIDGE_OR_FAIL_ROUTES = {
    "controlled_pause",
}

LOOP_RISK_SUCCESS_ROUTES = {
    "continue_concrete_witness_path",
    "continue_source_side_irrelevance_theorem_path",
    "continue_bridge_facing_candidate_path",
}

ONTOLOGY_FORMALIZER_PAYLOAD_TYPES = {
    "finite_concrete_source_object_witnesses",
    "concrete_certificate_step_families",
    "explicit_inverse_provenance_tokens",
    "source_side_irrelevance_proof",
    "bridge_map_candidate",
    "theorem_with_hypotheses_and_proof",
    "countermodel_or_obstruction",
}

GENERAL_PHYSICS_PAYLOAD_TYPES = ONTOLOGY_FORMALIZER_PAYLOAD_TYPES | {
    "definition",
    "lemma",
    "theorem",
    "finite_model",
    "countermodel",
    "explicit_witness",
    "obstruction",
    "dependency_map_update",
    "finite_toy_model_target",
    "source_extension_classification",
    "packet_selection",
}

ONTOLOGY_PAYLOAD_TEXT_MARKERS = (
    "finite concrete",
    "concrete witness",
    "certificate-step",
    "certificate step",
    "inverse-provenance",
    "inverse provenance",
    "source-side irrelevance",
    "bridge map",
    "bridge candidate",
    "theorem",
    "countermodel",
    "obstruction",
)

THEORETICAL_DECISION_PACKET_TYPES = {
    "source_side_selector_primitive",
    "source_side_irrelevance_theorem",
    "concrete_resp_lc_witness",
    "distinct_scoped_no_go_question",
    "bounded_theoretical_calculation",
    "finite_toy_metric_response_model",
    "ontology_law_research_packet",
    "source_extension_candidate",
    "source_extension_smuggling_audit",
    "source_extension_refuter_stress",
    "source_extension_human_gate",
    "human_gated_ontology_change_required",
}

ONTOLOGY_LAW_ROUTE_LABEL = "ontology-law-research-packet"
ONTOLOGY_LAW_SELECTOR_PACKET = "ontology_law_research_packet"
ONTOLOGY_LAW_TRIGGER_CLASSIFICATION = "derivation_critical_missing_source_law"
ONTOLOGY_LAW_STATUS_PAIR = "blocked_adoption_open_continuation"
ONTOLOGY_LAW_PAYLOAD_MODES = {
    "candidate_law_payload",
    "candidate_law_comparison",
    "candidate_law_refutation",
    "human_gate_precondition",
}
ONTOLOGY_LAW_STATUS_LABELS = {
    "draft/control",
    "proposal-only",
    "source-extension data",
    "canonical-ontology candidate",
    "adopted",
    "rejected",
    "human-gated",
}
ONTOLOGY_LAW_NON_TRIGGERS = {
    "ordinary_gap",
    "workflow_inconvenience",
}
ONTOLOGY_LAW_REQUIRED_FORBIDDEN_SOURCE_CLASSES = {
    "target_atlas",
    "target_metric",
    "benchmark_success",
    "generated_derivative",
    "registry_metadata_authority",
    "role_authority",
    "validation_authority",
}
ONTOLOGY_LAW_TARGET_IMPORT_MARKERS = {
    "target atlas",
    "target_atlas",
    "target metric",
    "target_metric",
    "benchmark success",
    "benchmark_success",
    "generated derivative",
    "generated_derivative",
    "registry metadata authority",
    "registry_metadata_authority",
    "role authority",
    "role_authority",
    "validation authority",
    "validation_authority",
}
ONTOLOGY_LAW_NO_GO_PRESENT_MARKERS = {
    "proved",
    "scoped_obstruction",
    "scoped obstruction",
    "no_go_theorem",
    "no-go theorem",
}

MATHEMATICAL_DECISIVENESS_CONTRACT_ACTIVE_AFTER = "2026-06-21T02:32:39Z"
MATHEMATICAL_DECISIVENESS_SCHEMA_PATH = ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"
MATHEMATICAL_DECISIVENESS_CONTRACT_PATH = (
    "research_control/design/mathematical_decisiveness_completion_contract.md"
)
MATHEMATICAL_DECISIVENESS_REQUIRED_FIELDS = (
    "physics_progress_status",
    "distance_to_gr_delta",
    "mathematical_payload_manifest",
    "forbidden_conclusion_summary",
)
PHYSICS_PROGRESS_STATUS_VALUES = {
    "burden_discharged",
    "candidate_constructed_pending_audit",
    "candidate_audited_pending_stress",
    "candidate_stress_passed_pending_gate",
    "precise_obstruction_found",
    "route_frozen",
    "human_gate_required",
    "selector_only_no_distance_delta",
    "documentation_or_control_only_no_physics_delta",
    "invalid_under_claim_boundary",
    "no_distance_delta",
}
DISTANCE_TO_GR_DELTA_EFFECT_ACTIVE_AFTER = "2026-07-03T11:24:00Z"
DISTANCE_TO_GR_DELTA_EFFECT_VALUES = {
    "no_distance_delta",
    "scoped_evidence_precondition",
    "scoped_source_only_object",
    "scoped_source_extension_object",
    "conditional_theorem_candidate",
    "obstruction_recorded",
    "frozen_negative",
    "milestone_discharge",
    "protected_gate_pending",
}
MATHEMATICAL_PAYLOAD_MANIFEST_TYPES = {
    "definition",
    "lemma",
    "theorem",
    "finite_model",
    "countermodel",
    "explicit_witness",
    "obstruction",
    "construction",
    "dependency_map_update",
    "packet_selection",
    "source_extension_classification",
}
MATHEMATICAL_PAYLOAD_MANIFEST_REQUIRED_FIELDS = (
    "payload_id",
    "payload_type",
    "object_name",
    "claim_status",
    "source_path",
    "burden_effect",
    "summary",
)
CANDIDATE_CONSTRUCTOR_RESULT_TYPES = {
    "constructed_candidate",
    "minimal_countermodel",
    "precise_obstruction",
    "invalid_under_claim_boundary",
}
CANDIDATE_CONSTRUCTOR_NEXT_REQUIRED_ROLES = {
    "smuggling_auditor",
    "smuggling-auditor",
    "refuter",
    "theoretical-continuation-selector",
    "theoretical_selector",
    "gate-chair",
    "gate_chair",
    "none",
}
CANDIDATE_CONSTRUCTOR_FOG_ONLY_PHRASES = (
    "more work required",
    "candidate remains open",
    "future work should explore",
    "insufficient time",
    "controlled pause",
    "selector should decide next",
    "generalization not attempted",
)
OBSTRUCTION_RECORD_SCOPES = {
    "local_finite_example",
    "exact_finite_local_branch",
    "current_ontology_only",
    "source_extension_candidate",
    "general_source_cover",
    "downstream_metric",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
}
OBSTRUCTION_CURRENT_ONTOLOGY_IMPLICATIONS = {
    "does_not_derive",
    "contradicts",
    "not_applicable",
}
OBSTRUCTION_SOURCE_EXTENSION_IMPLICATIONS = {
    "repair_allowed",
    "new_primitive_required",
    "target_import_detected",
    "not_applicable",
}
OBSTRUCTION_CONSEQUENCES = {
    "repair_candidate_allowed",
    "selector_required",
    "route_frozen",
    "human_gate_required",
    "downstream_block_preserved",
    "new_primitive_required",
    "target_import_detected",
}
MATHEMATICAL_DECISIVENESS_FREEZE_DECISIONS = {
    "not_frozen",
    "locally_frozen",
    "freeze_review_required",
    "human_gate_required",
}
MATHEMATICAL_DECISIVENESS_NEXT_ALLOWED_ROUTES = {
    "candidate_constructor",
    "smuggling_auditor",
    "refuter",
    "theoretical_selector",
    "gate_chair",
    "freeze_review",
    "none",
}
UNAUTHORIZED_DOWNSTREAM_GR_UNLOCKS = {
    "g_eff",
    "matter_coupling",
    "matter coupling",
    "einstein_equations",
    "einstein equations",
    "benchmark_promotion",
    "benchmark promotion",
}
CANDIDATE_CONSTRUCTOR_ROLE_IDS = {
    "candidate-constructor",
}

SOURCE_EXTENSION_WORKFLOW_CATEGORIES = {
    "source_extension_candidate",
    "source_extension_smuggling_audit",
    "source_extension_refuter_stress",
    "source_extension_human_gate",
    "source_extension_adopted_or_rejected",
}
SOURCE_EXTENSION_CLASSIFICATION_REQUIRED_AFTER = "2026-07-03T06:45:00Z"
SOURCE_EXTENSION_CLASSIFICATION_CHECKLIST_ID = "source_extension_classification_checklist_v1"
SOURCE_EXTENSION_CLASSIFICATION_VALUES = {
    "derived_from_current_ontology",
    "conservative_definitional_extension",
    "new_ontology_primitive_candidate",
    "forbidden_target_import",
    "status_boundary_evidence_only",
    "blocked_adoption_open_continuation",
}
SOURCE_EXTENSION_ONTOLOGY_RELATION_VALUES = {
    "derived",
    "conservative",
    "missing_primitive",
    "target_import",
    "evidence_only",
    "blocked_open",
}
SOURCE_EXTENSION_CLASSIFICATION_ROLE_IDS = PHYSICS_ROLE_IDS | {"gate-chair"}

FREEZE_DECISION_VALUES = {
    "not_frozen",
    "freeze_route",
    "human_gate_required",
}

THEORETICAL_DECISION_TEXT_MARKERS = (
    "theoretical-continuation-selector",
    "theoretical continuation selector",
    "source-side selector",
    "selector primitive",
    "source-side irrelevance",
    "irrelevance theorem",
    "concrete resp_lc",
    "concrete resp lc",
    "resp_lc witness",
    "scoped no-go",
    "new mathematical payload",
    "bounded theoretical calculation",
)

PARENT_CHILD_SYNTHESIS_MODE = "parent_child_parallel_synthesis"
PARENT_CHILD_SYNTHESIS_VERSION = "0.1.0"
PARENT_CHILD_PARENT_UNIT_ID = "parent"
PARENT_CHILD_PARENT_PERSPECTIVE = "physicist_mathematician_philosopher"
PARENT_CHILD_REQUIRED_CHILDREN = {
    "child_phys_math": "physicist_mathematician",
    "child_phys_phil": "physicist_philosopher",
}
PARENT_CHILD_CONFLICT_TYPES = {
    "mathematical",
    "physical",
    "ontological",
    "claim_boundary",
    "source_or_citation",
    "terminology",
    "next_route",
    "validator_or_schema",
}
PARENT_CHILD_CONFLICT_SEVERITIES = {"blocking", "nonblocking"}
PARENT_CHILD_CONFLICT_STATUSES = {
    "no_conflict",
    "resolved",
    "unresolved_nonblocking",
    "unresolved_blocking",
    "blocked",
}
PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS = {
    "allowed_generated_paths",
    "allowed_read_paths",
    "allowed_source_classes",
    "allowed_write_paths",
    "authority_delta_summary",
    "base_role_id",
    "base_role_version",
    "claim_boundary",
    "expanded_permissions",
    "forbidden_paths",
    "forbidden_source_classes",
    "provisional_role_contract",
    "requires_human_gate",
    "role_id",
    "role_version",
}


def loop_control_policy() -> dict[str, object]:
    return {
        "policy_id": "bridge_or_fail_loop_control_v1",
        "activated_at": LOOP_CONTROL_POLICY_ACTIVATED_AT,
        "theoretical_continuation_policy_activated_at": THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT,
        "distance_to_gr_required_burdens": list(DISTANCE_TO_GR_REQUIRED_BURDENS),
        "refuter_decision_categories": sorted(LOOP_RISK_DECISION_CATEGORIES),
        "bridge_or_fail_routes": sorted(BRIDGE_OR_FAIL_ROUTES),
        "legacy_bridge_or_fail_routes": sorted(LEGACY_BRIDGE_OR_FAIL_ROUTES),
        "ontology_formalizer_payload_types": sorted(ONTOLOGY_FORMALIZER_PAYLOAD_TYPES),
        "theoretical_decision_packet_types": sorted(THEORETICAL_DECISION_PACKET_TYPES),
    }


def theoretical_continuation_policy() -> dict[str, object]:
    return {
        "policy_id": "theoretical_continuation_pause_gate_v1",
        "activated_at": THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT,
        "pause_route": "human_gated_ontology_change_required",
        "decision_role_id": "theoretical-continuation-selector",
        "generic_controlled_pause_allowed_for_future_physics": False,
        "allowed_theoretical_packet_types": sorted(THEORETICAL_DECISION_PACKET_TYPES),
    }


def gr_derivation_roadmap_policy() -> dict[str, object]:
    return {
        "policy_id": "gr_derivation_roadmap_v1",
        "activated_at": GR_DERIVATION_ROADMAP_POLICY_ACTIVATED_AT,
        "roadmap_path": "research_control/design/gr_derivation_burden_map.md",
        "distance_to_gr_ledger_path": "registries/DISTANCE_TO_GR_LEDGER.csv",
        "required_job_fields": [
            "target_derivation_milestone",
            "milestone_burden",
        ],
        "allowed_milestones": list(GR_DERIVATION_MILESTONES),
        "distance_to_gr_required_burdens": list(ROADMAP_DISTANCE_TO_GR_REQUIRED_BURDENS),
        "mathematical_payload_types": sorted(GENERAL_PHYSICS_PAYLOAD_TYPES),
        "source_extension_categories": sorted(SOURCE_EXTENSION_WORKFLOW_CATEGORIES),
        "freeze_decisions": sorted(FREEZE_DECISION_VALUES),
    }


def parent_child_decomposition_policy() -> dict[str, object]:
    return {
        "policy_id": "parent_child_parallel_synthesis_v1",
        "mode": PARENT_CHILD_SYNTHESIS_MODE,
        "decomposition_version": PARENT_CHILD_SYNTHESIS_VERSION,
        "activated_at": PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT,
        "required_for_future_physics_agent_jobs": True,
        "execution_boundary": "one outer AgentJob with internal execution units",
        "parent": {
            "execution_unit_id": PARENT_CHILD_PARENT_UNIT_ID,
            "perspective": PARENT_CHILD_PARENT_PERSPECTIVE,
        },
        "children": [
            {"execution_unit_id": unit_id, "perspective": perspective}
            for unit_id, perspective in sorted(PARENT_CHILD_REQUIRED_CHILDREN.items())
        ],
        "conflict_types": sorted(PARENT_CHILD_CONFLICT_TYPES),
        "conflict_severities": sorted(PARENT_CHILD_CONFLICT_SEVERITIES),
        "forbidden_authority_expansion_keys": sorted(PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS),
    }


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self) -> bool:
        return not self.errors


def repo_path(relative_path: str) -> Path:
    return REPO_ROOT / relative_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_relative_path(path_text: str) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if path.is_absolute():
        return "absolute paths are not allowed"
    if any(part == ".." for part in path.parts):
        return "path traversal is not allowed"
    return None


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def int_value(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


def _clean_timestamp(value: Any) -> str:
    text = str(value or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", text):
        return text
    return ""


def timestamp_at_or_after(value: Any, threshold: str = LOOP_CONTROL_POLICY_ACTIVATED_AT) -> bool:
    text = _clean_timestamp(value)
    return bool(text and text >= threshold)


def job_policy_active(job_row: dict[str, str], completion: dict[str, Any] | None = None) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(timestamp_at_or_after(value) for value in timestamps)


def theoretical_continuation_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, THEORETICAL_CONTINUATION_POLICY_ACTIVATED_AT)
        for value in timestamps
    )


def gr_derivation_roadmap_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, GR_DERIVATION_ROADMAP_POLICY_ACTIVATED_AT)
        for value in timestamps
    )


def distance_to_gr_delta_effect_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return False
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, DISTANCE_TO_GR_DELTA_EFFECT_ACTIVE_AFTER)
        for value in timestamps
    )


def validation_schema_split_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
        if isinstance(completion.get("validation_layers"), dict) or isinstance(
            completion.get("authorization_layers"), dict
        ):
            return True
    return any(
        timestamp_at_or_after(value, VALIDATION_SCHEMA_SPLIT_ACTIVE_AFTER)
        for value in timestamps
    )


def _mathematical_decisiveness_active_after(
    job_contract: dict[str, Any],
    completion: dict[str, Any],
) -> str:
    for source in (job_contract, completion):
        active_after = str(source.get("mathematical_decisiveness_contract_active_after", "")).strip()
        if _clean_timestamp(active_after):
            return active_after
        block = source.get("mathematical_decisiveness_contract")
        if isinstance(block, dict):
            block_active_after = str(block.get("active_after", "")).strip()
            if _clean_timestamp(block_active_after):
                return block_active_after
    return MATHEMATICAL_DECISIVENESS_CONTRACT_ACTIVE_AFTER


def mathematical_decisiveness_warning_policy_active(
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
) -> bool:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return False
    requested_by_key = any(
        "mathematical_decisiveness_contract_active_after" in source
        or "mathematical_decisiveness_contract" in source
        or "mathematical_decisiveness_schema" in source
        for source in (job_contract, completion)
    )
    blob = text_blob(job_contract, completion)
    requested_by_value = any(
        marker.lower() in blob
        for marker in (
            "PHYSICS_COMPLETION_DECISIVENESS_SCHEMA",
            MATHEMATICAL_DECISIVENESS_SCHEMA_PATH,
            MATHEMATICAL_DECISIVENESS_CONTRACT_PATH,
        )
    )
    requested = requested_by_key or requested_by_value
    if not requested:
        return False
    active_after = _mathematical_decisiveness_active_after(job_contract, completion)
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
        completion.get("completed_at", ""),
    ]
    return any(timestamp_at_or_after(value, active_after) for value in timestamps)


def memory_preflight_required(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, MEMORY_PREFLIGHT_REQUIRED_AFTER)
        for value in timestamps
    )


def parent_child_required_for_job(job_row: dict[str, str]) -> bool:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return False
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    return any(
        timestamp_at_or_after(value, PARENT_CHILD_REQUIRED_FOR_PHYSICS_ACTIVATED_AT)
        for value in timestamps
    )


def _collect_text(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        text: list[str] = []
        for child in value.values():
            text.extend(_collect_text(child))
        return text
    if isinstance(value, list):
        text = []
        for child in value:
            text.extend(_collect_text(child))
        return text
    return []


def text_blob(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        parts.extend(_collect_text(value))
    return "\n".join(parts).lower()


def read_csv_rows(name: str) -> list[dict[str, str]]:
    path = REGISTRY_DIR / name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def existing_by_id(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def role_key(role_id: str, version: str) -> str:
    return f"{role_id}@{version}"


def role_row_key(row: dict[str, str]) -> str:
    return role_key(row.get("role_id", ""), row.get("version", ""))


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def validate_registry_columns(report: ValidationReport) -> None:
    for name, expected in REGISTRY_COLUMNS.items():
        path = REGISTRY_DIR / name
        if not path.exists():
            report.error(f"missing registry: registries/{name}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
        if header != expected:
            report.error(f"{name}: expected columns {expected}, found {header}")


def validate_distance_to_gr_ledger(report: ValidationReport) -> None:
    path = REGISTRY_DIR / "DISTANCE_TO_GR_LEDGER.csv"
    if not path.exists():
        report.error("missing registry: registries/DISTANCE_TO_GR_LEDGER.csv")
        return
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        if header != DISTANCE_TO_GR_LEDGER_COLUMNS:
            report.error(
                "DISTANCE_TO_GR_LEDGER.csv: expected columns "
                f"{DISTANCE_TO_GR_LEDGER_COLUMNS}, found {header}"
            )
            return
        rows = list(reader)
    by_burden: dict[str, dict[str, str]] = {}
    for row_number, row in enumerate(rows, start=2):
        burden_id = row.get("burden_id", "").strip()
        if not burden_id:
            report.error(f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: missing burden_id")
            continue
        if burden_id in by_burden:
            report.error(f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: duplicate burden_id {burden_id}")
        by_burden[burden_id] = row
        milestone = row.get("milestone", "").strip()
        if milestone not in GR_DERIVATION_MILESTONES:
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: unsupported milestone {milestone}"
            )
        status = row.get("current_status", "").strip()
        if status not in DISTANCE_TO_GR_LEDGER_STATUS_VALUES:
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: unsupported current_status {status}"
            )
        for field_name in [
            "required_object",
            "blocking_burden",
            "accept_criteria",
            "failure_or_freeze_criteria",
            "last_evidence_path",
            "updated_at",
        ]:
            if not row.get(field_name, "").strip():
                report.error(f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: missing {field_name}")
        for field_name in DISTANCE_TO_GR_LEDGER_LAYER_COLUMNS:
            if not row.get(field_name, "").strip():
                report.error(f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: missing {field_name}")
        for field_name, allowed_values in DISTANCE_TO_GR_FIELD_VALUE_SETS.items():
            value = row.get(field_name, "").strip()
            if value and value not in allowed_values:
                report.error(
                    f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: unsupported {field_name} {value}"
                )
        guard_value = row.get("overread_guard", "").strip()
        guard_tokens = [token.strip() for token in guard_value.split(";") if token.strip()]
        if guard_value and not guard_tokens:
            report.error(f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: empty overread_guard")
        for token in guard_tokens:
            if token not in DISTANCE_TO_GR_OVERREAD_GUARD_VALUES:
                report.error(
                    f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: unsupported overread_guard token {token}"
                )
        expected_layer_values = DISTANCE_TO_GR_EXPECTED_LAYER_VALUES.get(burden_id, {})
        for field_name, expected_value in expected_layer_values.items():
            field_value = row.get(field_name, "").strip()
            if field_value != expected_value:
                report.error(
                    f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: {burden_id} {field_name} "
                    f"must be {expected_value}, found {field_value}"
                )
        physical_status = row.get("physical_status", "").strip()
        promotion_status = row.get("promotion_status", "").strip()
        if promotion_status in DISTANCE_TO_GR_SCOPED_PROMOTION_STATUS_VALUES and not (
            physical_status.startswith(("not_", "no_")) or "blocked" in physical_status
        ):
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: scoped promotion_status "
                f"{promotion_status} requires physical_status with explicit not/no/blocked "
                f"wording, found {physical_status}"
            )
        required_guard_tokens = DISTANCE_TO_GR_REQUIRED_GUARD_TOKENS.get(burden_id, set())
        missing_guard_tokens = sorted(required_guard_tokens - set(guard_tokens))
        if missing_guard_tokens:
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: {burden_id} missing "
                f"overread_guard tokens {missing_guard_tokens}"
            )
        if status == "accepted" and promotion_status not in DISTANCE_TO_GR_SCOPED_PROMOTION_STATUS_VALUES:
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: accepted current_status must "
                "use scoped promotion_status"
            )
        control_status = row.get("control_status", "").strip()
        if status == "accepted" and control_status not in DISTANCE_TO_GR_ACCEPTED_CONTROL_STATUS_VALUES:
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: accepted current_status must "
                "use scoped or gate-reviewed control_status"
            )
        last_evidence_path = row.get("last_evidence_path", "").strip()
        if burden_id in DISTANCE_TO_GR_EXPECTED_LAYER_VALUES and (
            last_evidence_path in DISTANCE_TO_GR_GENERATED_STATUS_AUTHORITY_PATHS
            or last_evidence_path.startswith(DISTANCE_TO_GR_GENERATED_STATUS_AUTHORITY_PREFIXES)
        ):
            report.error(
                f"DISTANCE_TO_GR_LEDGER.csv:{row_number}: generated snapshot or "
                f"noncanonical retrieval path cannot serve as layered status authority "
                f"for {burden_id}: {last_evidence_path}"
            )
    missing = sorted(set(DISTANCE_TO_GR_LEDGER_REQUIRED_BURDENS) - set(by_burden))
    if missing:
        report.error(f"DISTANCE_TO_GR_LEDGER.csv: missing required burdens {missing}")


def _frontier_inventory_item_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^### Item \d+:\s*(.+?)\s*$", text, re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1).strip(), text[match.end() : end]))
    return sections


def _frontier_inventory_fields(section: str) -> dict[str, str]:
    fields: dict[str, list[str]] = {}
    current_field = ""
    for line in section.splitlines():
        match = re.match(r"^- `([^`]+)`:\s*(.*)$", line)
        if match:
            current_field = match.group(1).strip()
            fields[current_field] = [match.group(2).strip()]
            continue
        if current_field and (line.startswith("  ") or not line.strip()):
            fields[current_field].append(line.strip())
    return {key: "\n".join(value).strip() for key, value in fields.items()}


def _frontier_inventory_tokens(value: str) -> set[str]:
    return {
        token.strip().strip("`").lower()
        for token in re.split(r"[;\n,]+", value)
        if token.strip().strip("`")
    }


def _frontier_inventory_backtick_paths(value: str) -> list[str]:
    paths: list[str] = []
    for token in re.findall(r"`([^`]+)`", value):
        token = token.strip()
        if (
            "/" in token
            or token.endswith((".csv", ".md", ".tex", ".yaml", ".yml"))
            or token in {"AGENTS.md", "README.md"}
        ):
            paths.append(token)
    return paths


def _frontier_inventory_generated_path(path_text: str) -> bool:
    return path_text in FRONTIER_INVENTORY_GENERATED_SOURCE_PATHS or path_text.startswith(
        FRONTIER_INVENTORY_GENERATED_SOURCE_PREFIXES
    )


def validate_frontier_theorem_inventory(report: ValidationReport) -> None:
    inventory_path = repo_path(FRONTIER_INVENTORY_PATH)
    if not inventory_path.exists():
        report.error(f"{FRONTIER_INVENTORY_PATH}: missing frontier theorem inventory source")
        return

    registry_rows = read_csv_rows("MARKDOWN_SOURCE_REGISTRY.csv")
    inventory_row = next(
        (
            row
            for row in registry_rows
            if row.get("object_id", "") == FRONTIER_INVENTORY_OBJECT_ID
        ),
        None,
    )
    if not inventory_row:
        report.error(
            f"MARKDOWN_SOURCE_REGISTRY.csv: missing {FRONTIER_INVENTORY_OBJECT_ID}"
        )
    else:
        if inventory_row.get("path", "") != FRONTIER_INVENTORY_PATH:
            report.error(
                f"MARKDOWN_SOURCE_REGISTRY.csv: {FRONTIER_INVENTORY_OBJECT_ID} "
                f"path must be {FRONTIER_INVENTORY_PATH}"
            )
        actual_hash = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
        if inventory_row.get("source_hash", "") != actual_hash:
            report.error(
                f"MARKDOWN_SOURCE_REGISTRY.csv: {FRONTIER_INVENTORY_OBJECT_ID} "
                "source_hash does not match inventory source"
            )

    text = inventory_path.read_text(encoding="utf-8")
    sections = _frontier_inventory_item_sections(text)
    if not sections:
        report.error(f"{FRONTIER_INVENTORY_PATH}: no inventory items found")
        return

    seen_item_ids: set[str] = set()
    for heading, section in sections:
        fields = _frontier_inventory_fields(section)
        item_id = fields.get("frontier_item_id", "").strip().strip("`")
        item_ref = item_id or heading
        prefix = f"{FRONTIER_INVENTORY_PATH}: {item_ref}"

        if item_id in seen_item_ids:
            report.error(f"{prefix}: duplicate frontier_item_id")
        if item_id:
            seen_item_ids.add(item_id)

        for field_name in FRONTIER_INVENTORY_REQUIRED_FIELDS:
            value = fields.get(field_name, "")
            if not value or value == "``":
                report.error(f"{prefix}: missing {field_name}")

        class_tokens = _frontier_inventory_tokens(fields.get("frontier_item_class", ""))
        unsupported_classes = sorted(class_tokens - FRONTIER_INVENTORY_ALLOWED_CLASSES)
        if unsupported_classes:
            report.error(f"{prefix}: unsupported frontier_item_class values {unsupported_classes}")

        authority_tokens = _frontier_inventory_tokens(fields.get("source_authority_type", ""))
        unsupported_authority = sorted(
            authority_tokens - FRONTIER_INVENTORY_ALLOWED_AUTHORITY_TYPES
        )
        if unsupported_authority:
            report.error(f"{prefix}: unsupported source_authority_type values {unsupported_authority}")

        source_paths = _frontier_inventory_backtick_paths(
            fields.get("source_artifact_path", "")
        )
        if not source_paths:
            report.error(f"{prefix}: source_artifact_path must include a path")
        generated_paths = [path for path in source_paths if _frontier_inventory_generated_path(path)]
        canonical_paths = [
            path for path in source_paths if not _frontier_inventory_generated_path(path)
        ]
        for path_text in canonical_paths:
            reason = validate_relative_path(path_text)
            if reason:
                report.error(f"{prefix}: invalid source_artifact_path {path_text}: {reason}")
                continue
            if not repo_path(path_text).exists():
                report.error(f"{prefix}: source_artifact_path does not exist: {path_text}")
        if generated_paths and not canonical_paths:
            report.error(
                f"{prefix}: generated derivative source path requires paired canonical source path"
            )

        guard_tokens = _frontier_inventory_tokens(fields.get("overread_guard", ""))
        physical_non_conclusions = fields.get("physical_non_conclusions", "").lower()
        item_text = text_blob(heading, section)
        risk_trigger_text = text_blob(
            fields.get("frontier_item_id", ""),
            fields.get("frontier_item_class", ""),
            fields.get("object_or_claim_name", ""),
            fields.get("status_layer_summary", ""),
            fields.get("definitions_used", ""),
            fields.get("statement_or_decision", ""),
            fields.get("mathematical_conclusion", ""),
            fields.get("missing_theorem_or_primitive", ""),
        )
        if not physical_non_conclusions:
            report.error(f"{prefix}: physical_non_conclusions must be nonblank")
        for marker, required_guards in FRONTIER_INVENTORY_HIGH_RISK_GUARDS.items():
            if marker in risk_trigger_text:
                if guard_tokens.isdisjoint(required_guards):
                    report.error(
                        f"{prefix}: high-risk term {marker} requires one of "
                        f"overread_guard tokens {sorted(required_guards)}"
                    )
        if "frozen_negative_route" in class_tokens or "frozen negative" in item_text:
            missing_frozen_guards = sorted(FRONTIER_INVENTORY_FROZEN_GUARDS - guard_tokens)
            if missing_frozen_guards:
                report.error(
                    f"{prefix}: frozen negative item missing overread_guard tokens "
                    f"{missing_frozen_guards}"
                )


def validate_registry_values(report: ValidationReport, rows_by_registry: dict[str, list[dict[str, str]]]) -> None:
    seen: set[tuple[str, str]] = set()
    id_fields = {
        "AGENT_ROLE_REGISTRY.csv": "role_id",
        "ROLE_EXECUTION_REGISTRY.csv": "execution_role_ref",
        "DIRECTOR_DECISION_REGISTRY.csv": "decision_id",
        "AGENT_JOB_REGISTRY.csv": "job_id",
        "RESEARCH_TASK_REGISTRY.csv": "task_id",
        "CLAIM_BOUNDARY_REGISTRY.csv": "claim_boundary_id",
        "COUNTERMODEL_OBLIGATION_REGISTRY.csv": "obligation_id",
    }
    for registry_name, rows in rows_by_registry.items():
        id_field = id_fields[registry_name]
        local_ids: set[str] = set()
        for row_number, row in enumerate(rows, start=2):
            if registry_name == "AGENT_ROLE_REGISTRY.csv":
                missing = [
                    field_name
                    for field_name in ("role_id", "version")
                    if not row.get(field_name, "")
                ]
                for field_name in missing:
                    report.error(f"{registry_name}:{row_number}: missing {field_name}")
                row_id = role_row_key(row)
            else:
                row_id = row.get(id_field, "")
            if not row_id:
                report.error(f"{registry_name}:{row_number}: missing {id_field}")
            if row_id in local_ids:
                report.error(f"{registry_name}:{row_number}: duplicate {id_field} {row_id}")
            local_ids.add(row_id)
            seen.add((registry_name, row_id))
            for field_name in BOOLEAN_FIELDS & set(row):
                if row[field_name] not in {"true", "false"}:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must be lowercase true/false"
                    )
            for field_name in SEMICOLON_FIELDS & set(row):
                if "," in row[field_name]:
                    report.error(
                        f"{registry_name}:{row_number}: {field_name} must use semicolons, not commas"
                    )


def _countermodel_row_text(row: dict[str, str]) -> str:
    return " ".join(str(row.get(field_name, "")) for field_name in COUNTERMODEL_OBLIGATION_COLUMNS)


def _countermodel_path_check(report: ValidationReport, row_ref: str, field_name: str, value: str) -> None:
    if not value.strip():
        report.warn(f"{row_ref}: {field_name} is missing")
        return
    reason = validate_relative_path(value)
    if reason:
        report.error(f"{row_ref}: invalid {field_name}: {reason}")
        return
    if not repo_path(value).exists():
        report.warn(f"{row_ref}: {field_name} does not exist: {value}")


def validate_countermodel_obligation_registry(
    report: ValidationReport,
    rows: list[dict[str, str]],
) -> None:
    slots_by_family: dict[str, set[str]] = {}
    for row_number, row in enumerate(rows, start=2):
        row_ref = (
            "COUNTERMODEL_OBLIGATION_REGISTRY.csv:"
            f"{row_number}:{row.get('obligation_id', '<missing>')}"
        )
        family = row.get("theorem_family", "").strip()
        slot = row.get("countermodel_slot", "").strip()
        status = row.get("status", "").strip()
        scope = row.get("scope", "").strip()

        if family not in COUNTERMODEL_OBLIGATION_FAMILIES:
            report.error(f"{row_ref}: unsupported theorem_family {family}")
        elif family != "other":
            slots_by_family.setdefault(family, set()).add(slot)
        if status not in COUNTERMODEL_OBLIGATION_STATUS_VALUES:
            report.error(f"{row_ref}: unsupported status {status}")
        if not slot:
            report.warn(f"{row_ref}: missing_countermodel_slot countermodel_slot is blank")
        if not scope:
            report.warn(f"{row_ref}: countermodel_scope_missing scope is blank")

        _countermodel_path_check(report, row_ref, "artifact_path", row.get("artifact_path", ""))
        _countermodel_path_check(report, row_ref, "result_artifact", row.get("result_artifact", ""))

        if bool_value(row.get("global_no_go_claimed", "")):
            report.error(
                f"{row_ref}: countermodel_overread_as_global_no_go "
                "global_no_go_claimed must remain false without protected no-go authority"
            )

        row_text = _countermodel_row_text(row)
        for pattern in COUNTERMODEL_HARD_OVERREAD_PATTERNS:
            match = pattern.search(row_text)
            if match:
                report.error(
                    f"{row_ref}: countermodel_overread_as_global_no_go "
                    f"matched {match.group(0)!r}"
                )

        if status in {"waived_by_ddr", "not_applicable_by_ddr", "deferred_by_ddr"}:
            notes = row.get("notes", "")
            result_artifact = row.get("result_artifact", "")
            if "DDR-" not in notes and "DDR-" not in result_artifact:
                report.warn(
                    f"{row_ref}: waiver_without_director_decision "
                    "DDR reference is required for waiver/deferred status"
                )

    for family, required_slots in sorted(COUNTERMODEL_REQUIRED_SLOTS_BY_FAMILY.items()):
        observed = slots_by_family.get(family, set())
        if not observed:
            continue
        missing = sorted(required_slots - observed)
        if missing:
            report.warn(
                "COUNTERMODEL_OBLIGATION_REGISTRY.csv: "
                f"missing_countermodel_slot theorem_family {family} missing slots {missing}"
            )


def _countermodel_completion_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any],
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
        completion.get("completed_at", ""),
    ]
    return any(
        timestamp_at_or_after(value, COUNTERMODEL_OBLIGATION_POLICY_ACTIVE_AFTER)
        for value in timestamps
    )


def _looks_like_theorem_attempt(job_contract: dict[str, Any], completion: dict[str, Any]) -> bool:
    blob = text_blob(job_contract, completion)
    return any(marker in blob for marker in COUNTERMODEL_OBLIGATION_THEOREM_MARKERS)


def validate_countermodel_obligation_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    if not _countermodel_completion_policy_active(job_row, completion):
        return
    if not (job_row.get("role_id", "") in PHYSICS_ROLE_IDS or "countermodel_obligations" in completion):
        return

    receipt = completion.get("countermodel_obligations")
    if not isinstance(receipt, dict):
        if _looks_like_theorem_attempt(job_contract, completion):
            report.warn(
                f"{path_text}: theorem_without_countermodel_justification "
                "missing countermodel_obligations block"
            )
        return

    policy_id = str(receipt.get("policy_id", "")).strip()
    if policy_id != "minimal_countermodel_obligation_policy_v1":
        report.warn(
            f"{path_text}: countermodel_obligations.policy_id should be "
            "minimal_countermodel_obligation_policy_v1"
        )
    family = str(receipt.get("theorem_family", "")).strip()
    if family not in COUNTERMODEL_OBLIGATION_FAMILIES:
        report.warn(f"{path_text}: countermodel_obligations.theorem_family is unsupported: {family}")
    waiver_decision_id = str(receipt.get("waiver_decision_id", "")).strip()
    slots = receipt.get("slots")
    if not isinstance(slots, list) or not slots:
        report.warn(f"{path_text}: missing_countermodel_slot countermodel_obligations.slots is empty")
        return

    observed_slots: set[str] = set()
    for index, slot_record in enumerate(slots, start=1):
        if not isinstance(slot_record, dict):
            report.warn(f"{path_text}: countermodel_obligations.slots[{index}] should be a map")
            continue
        slot_name = str(slot_record.get("countermodel_slot", "")).strip()
        slot_status = str(slot_record.get("status", "")).strip()
        observed_slots.add(slot_name)
        if not slot_name:
            report.warn(
                f"{path_text}: missing_countermodel_slot "
                f"countermodel_obligations.slots[{index}].countermodel_slot is blank"
            )
        if slot_status not in COUNTERMODEL_OBLIGATION_STATUS_VALUES:
            report.warn(
                f"{path_text}: countermodel_obligations.slots[{index}].status "
                f"is unsupported: {slot_status}"
            )
        if not str(slot_record.get("scope", "")).strip():
            report.warn(
                f"{path_text}: countermodel_scope_missing "
                f"countermodel_obligations.slots[{index}].scope is blank"
            )
        if not str(slot_record.get("result_artifact", "")).strip():
            report.warn(
                f"{path_text}: countermodel_obligations.slots[{index}].result_artifact is blank"
            )
        if slot_status in {"waived_by_ddr", "not_applicable_by_ddr", "deferred_by_ddr"} and not waiver_decision_id:
            report.warn(
                f"{path_text}: waiver_without_director_decision "
                f"countermodel_obligations.slots[{index}] requires waiver_decision_id"
            )

    required = COUNTERMODEL_REQUIRED_SLOTS_BY_FAMILY.get(family, set())
    missing = sorted(required - observed_slots)
    if missing:
        report.warn(
            f"{path_text}: missing_countermodel_slot theorem_family {family} missing slots {missing}"
        )


def _frontmatter_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def validate_roles(report: ValidationReport, role_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    roles = {role_row_key(row): row for row in role_rows if row.get("role_id") and row.get("version")}
    active_by_role_id: dict[str, str] = {}
    for row in role_rows:
        if row.get("status") == "active":
            previous = active_by_role_id.get(row["role_id"])
            if previous:
                report.error(
                    f"{row['role_id']}: multiple active role versions {previous} and {row['version']}"
                )
            active_by_role_id[row["role_id"]] = row["version"]
        path_text = row["role_contract_path"]
        reason = validate_relative_path(path_text)
        if reason:
            report.error(f"{role_row_key(row)}: invalid role_contract_path: {reason}")
            continue
        path = repo_path(path_text)
        if not path.exists():
            report.error(f"{role_row_key(row)}: missing role contract {path_text}")
            continue
        try:
            frontmatter, _ = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{path_text}: {exc}")
            continue
        for field_name in [
            "role_id",
            "version",
            "role_kind",
            "authority_level",
            "status",
            "may_execute_autonomously",
            "may_create_outputs",
            "may_modify_sources",
            "may_promote_claims",
            "requires_human_gate",
            "default_output_format",
            "default_validators",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{path_text}: frontmatter {field_name} does not match AGENT_ROLE_REGISTRY.csv"
                )
    return roles


def validate_tasks(
    report: ValidationReport,
    task_rows: list[dict[str, str]],
    decision_rows: dict[str, dict[str, str]],
    job_rows: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    tasks = existing_by_id(task_rows, "task_id")
    for row in task_rows:
        reason = validate_relative_path(row["task_path"])
        if reason:
            report.error(f"{row['task_id']}: invalid task_path: {reason}")
            continue
        task_dir = repo_path(row["task_path"])
        task_yaml = task_dir / "00_TASK.yaml"
        if not task_yaml.exists():
            report.error(f"{row['task_id']}: missing 00_TASK.yaml")
            continue
        try:
            task_data = load_yaml(task_yaml)
        except StrictYamlError as exc:
            report.error(f"{task_yaml.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        if str(task_data.get("task_id", "")) != row["task_id"]:
            report.error(f"{row['task_id']}: 00_TASK.yaml task_id mismatch")
        if row["current_decision_id"] and row["current_decision_id"] not in decision_rows:
            report.error(f"{row['task_id']}: current_decision_id is not registered")
        if row["current_job_id"] and row["current_job_id"] not in job_rows:
            report.error(f"{row['task_id']}: current_job_id is not registered")
    return tasks


def validate_director_decisions(
    report: ValidationReport,
    decision_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    decisions = existing_by_id(decision_rows, "decision_id")
    for row in decision_rows:
        reason = validate_relative_path(row["decision_path"])
        if reason:
            report.error(f"{row['decision_id']}: invalid decision_path: {reason}")
            continue
        path = repo_path(row["decision_path"])
        if not path.exists():
            report.error(f"{row['decision_id']}: missing DDR {row['decision_path']}")
            continue
        try:
            frontmatter, body = load_frontmatter(path)
        except StrictYamlError as exc:
            report.error(f"{row['decision_path']}: {exc}")
            continue
        for field_name in [
            "decision_id",
            "task_id",
            "director_version",
            "decision_type",
            "selected_role_id",
            "selected_role_version",
            "agent_job_id",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(frontmatter.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['decision_path']}: frontmatter {field_name} does not match DIRECTOR_DECISION_REGISTRY.csv"
                )
        if row["decision_type"] != "provisional_role" and role_key(
            row["selected_role_id"], row["selected_role_version"]
        ) not in roles:
            report.error(f"{row['decision_id']}: selected role is not registered")
        if "## Role-Fit Matrix" not in body:
            report.error(f"{row['decision_path']}: missing ## Role-Fit Matrix")
    return decisions


def validate_agent_jobs(
    report: ValidationReport,
    job_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
    decisions: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    jobs = existing_by_id(job_rows, "job_id")
    for row in job_rows:
        reason = validate_relative_path(row["job_path"])
        if reason:
            report.error(f"{row['job_id']}: invalid job_path: {reason}")
            continue
        path = repo_path(row["job_path"])
        if not path.exists():
            report.error(f"{row['job_id']}: missing AgentJob {row['job_path']}")
            continue
        try:
            job = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{row['job_path']}: {exc}")
            continue
        for field_name in [
            "job_id",
            "task_id",
            "decision_id",
            "role_id",
            "role_version",
            "status",
            "requires_human_gate",
        ]:
            if _frontmatter_value(job.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['job_path']}: {field_name} does not match AGENT_JOB_REGISTRY.csv"
                )
        if row["decision_id"] not in decisions:
            report.error(f"{row['job_id']}: decision_id is not registered")
        if role_key(row["role_id"], row["role_version"]) not in roles:
            provisional = job.get("provisional_role_contract")
            if not isinstance(provisional, dict):
                report.error(f"{row['job_id']}: unregistered role lacks provisional_role_contract")
            elif str(provisional.get("role_id", "")) != row["role_id"]:
                report.error(f"{row['job_id']}: provisional role_id mismatch")
            elif str(provisional.get("expires_after_job_id", "")) != row["job_id"]:
                report.error(f"{row['job_id']}: provisional role must expire after this job")
        for field_name in ["allowed_write_paths", "allowed_generated_paths", "forbidden_paths"]:
            value = job.get(field_name, [])
            if not isinstance(value, list):
                report.error(f"{row['job_path']}: {field_name} must be a list")
                continue
            for item in value:
                if not isinstance(item, str):
                    report.error(f"{row['job_path']}: {field_name} entries must be strings")
                    continue
                reason = validate_relative_path(item.replace("**", "x").replace("*", "x"))
                if reason:
                    report.error(f"{row['job_path']}: invalid {field_name} entry {item}: {reason}")
        validate_memory_preflight(report, row, job, row["job_path"])
        task_record: dict[str, Any] = {}
        task_record_path = CONTROL_DIR / "tasks" / row["task_id"] / "00_TASK.yaml"
        if task_record_path.exists():
            try:
                loaded_task = load_yaml(task_record_path)
                if isinstance(loaded_task, dict):
                    task_record = loaded_task
            except StrictYamlError as exc:
                report.error(f"{row['job_path']}: cannot evaluate physics-payload admission: {exc}")
        admission = evaluate_agent_job_admission(
            job,
            task_record,
            created_at=row.get("created_at", ""),
            role_id=row.get("role_id", ""),
        )
        for error in admission["errors"]:
            report.error(f"{row['job_path']}: physics-payload admission: {error}")
        dual_budget = evaluate_dual_budget_allocation(
            job,
            created_at=row.get("created_at", ""),
        )
        for error in dual_budget["errors"]:
            report.error(f"{row['job_path']}: dual-budget allocation: {error}")
        ordinary_route = evaluate_agent_job_route_admission(
            job,
            created_at=row.get("created_at", ""),
            repo_root=REPO_ROOT,
        )
        for error in ordinary_route["errors"]:
            report.error(f"{row['job_path']}: ordinary-route admission: {error}")
        for warning in ordinary_route.get("warnings", []):
            report.warn(f"{row['job_path']}: ordinary-route admission: {warning}")
        validate_parent_child_decomposition(report, row, job)
        validate_future_physics_job_authority(report, row, job)
        if row["completion_path"]:
            completion_path = repo_path(row["completion_path"])
            if not completion_path.exists():
                report.error(f"{row['job_id']}: missing completion {row['completion_path']}")
            else:
                validate_completion(report, row, completion_path)
    return jobs


def validate_future_physics_job_authority(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
) -> None:
    if job_row.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return
    if not job_policy_active(job_row):
        return

    path_text = job_row.get("job_path", job_row.get("job_id", ""))
    if parent_child_required_for_job(job_row) and not isinstance(
        job_contract.get("role_decomposition"), dict
    ):
        report.error(
            f"{path_text}: future physics AgentJob must declare "
            f"role_decomposition.mode={PARENT_CHILD_SYNTHESIS_MODE}"
        )

    if gr_derivation_roadmap_policy_active(job_row):
        milestone = str(job_contract.get("target_derivation_milestone", "")).strip()
        burden = str(job_contract.get("milestone_burden", "")).strip()
        if milestone not in GR_DERIVATION_MILESTONES:
            report.error(
                f"{path_text}: future physics AgentJob must name target_derivation_milestone "
                f"from {list(GR_DERIVATION_MILESTONES)}"
            )
        if not burden:
            report.error(f"{path_text}: future physics AgentJob must declare milestone_burden")

    forbidden_classes = set(_listish_values(job_contract.get("forbidden_source_classes", [])))
    missing = sorted(PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES - forbidden_classes)
    if missing:
        report.error(
            f"{path_text}: future physics AgentJob missing forbidden_source_classes {missing}"
        )

    protected_canonical_paths_admitted = (
        validate_protected_canonical_integration_admission(
            report,
            job_row,
            job_contract,
        )
    )
    for item in _listish_values(job_contract.get("allowed_write_paths", [])):
        normalized = item.strip().lstrip("./")
        if any(normalized.startswith(prefix) for prefix in PHYSICS_JOB_FORBIDDEN_WRITE_PREFIXES):
            if (
                protected_canonical_paths_admitted
                and normalized in PROTECTED_CANONICAL_INTEGRATION_PATHS
            ):
                continue
            report.error(
                f"{path_text}: future physics AgentJob may not allow direct write path {item}"
            )


def _protected_canonical_bound_file(
    record: dict[str, Any],
    section_name: str,
    errors: list[str],
) -> Path | None:
    section = record.get(section_name)
    if not isinstance(section, dict):
        errors.append(f"{section_name}_must_be_a_map")
        return None
    path_text = str(section.get("path", "")).strip()
    expected_sha256 = str(section.get("sha256", "")).strip()
    if validate_relative_path(path_text) is not None:
        errors.append(f"{section_name}_path_invalid")
        return None
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        errors.append(f"{section_name}_sha256_invalid")
        return None
    path = repo_path(path_text)
    try:
        path.resolve().relative_to(REPO_ROOT.resolve())
    except (OSError, ValueError):
        errors.append(f"{section_name}_path_outside_repository")
        return None
    if not path.is_file() or path.is_symlink():
        errors.append(f"{section_name}_path_not_regular")
        return None
    if sha256_file(path) != expected_sha256:
        errors.append(f"{section_name}_hash_mismatch")
        return None
    return path


def _protected_canonical_bound_yaml(
    record: dict[str, Any],
    section_name: str,
    errors: list[str],
) -> dict[str, Any]:
    path = _protected_canonical_bound_file(record, section_name, errors)
    if path is None:
        return {}
    try:
        loaded = load_yaml(path)
    except StrictYamlError:
        errors.append(f"{section_name}_yaml_invalid")
        return {}
    if not isinstance(loaded, dict):
        errors.append(f"{section_name}_yaml_not_mapping")
        return {}
    return loaded


def _protected_canonical_bound_task(
    admitted: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    """Load the historical task or its one exact metadata-only compatibility repair."""

    path_text = str(admitted.get("task_path", "")).strip()
    expected_sha256 = str(admitted.get("task_sha256", "")).strip()
    if path_text != PROTECTED_CANONICAL_INTEGRATION_TASK_PATH:
        errors.append("bound_task_path_mismatch")
        return {}
    if expected_sha256 != PROTECTED_CANONICAL_INTEGRATION_TASK_HISTORICAL_SHA256:
        errors.append("bound_task_historical_hash_mismatch")
        return {}
    path = repo_path(path_text)
    if not path.is_file() or path.is_symlink():
        errors.append("bound_task_path_not_regular")
        return {}
    actual_sha256 = sha256_file(path)
    if actual_sha256 not in {
        expected_sha256,
        PROTECTED_CANONICAL_INTEGRATION_TASK_METADATA_REPAIR_SHA256,
    }:
        errors.append("bound_task_hash_mismatch")
        return {}
    try:
        loaded = load_yaml(path)
    except StrictYamlError:
        errors.append("bound_task_yaml_invalid")
        return {}
    if not isinstance(loaded, dict):
        errors.append("bound_task_yaml_not_mapping")
        return {}
    if actual_sha256 == PROTECTED_CANONICAL_INTEGRATION_TASK_METADATA_REPAIR_SHA256:
        for field_name, expected in (
            PROTECTED_CANONICAL_INTEGRATION_TASK_METADATA_REPAIR.items()
        ):
            if loaded.get(field_name) != expected:
                errors.append(f"bound_task_metadata_repair_{field_name}_mismatch")
    return loaded


def validate_protected_canonical_integration_admission(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
) -> bool:
    allowed_paths = {
        item.strip().lstrip("./")
        for item in _listish_values(job_contract.get("allowed_write_paths", []))
    }
    protected_paths = {
        path
        for path in allowed_paths
        if any(path.startswith(prefix) for prefix in PHYSICS_JOB_FORBIDDEN_WRITE_PREFIXES)
    }
    if not protected_paths:
        return False

    task_id = str(job_row.get("task_id", "")).strip()
    receipt_path = repo_path(
        f"research_control/tasks/{task_id}/artifacts/"
        "protected_canonical_ontology_integration_admission_v1.yaml"
    )
    if not receipt_path.is_file() or receipt_path.is_symlink():
        return False

    errors: list[str] = []
    try:
        receipt = load_yaml(receipt_path)
    except StrictYamlError:
        receipt = {}
        errors.append("receipt_yaml_invalid")
    if not isinstance(receipt, dict):
        receipt = {}
        errors.append("receipt_must_be_a_map")

    if receipt.get("schema_id") != PROTECTED_CANONICAL_INTEGRATION_SCHEMA_ID:
        errors.append("schema_id_invalid")
    if receipt.get("status") != "active":
        errors.append("status_not_active")
    if receipt.get("validation_status") != "PASS":
        errors.append("validation_status_not_pass")
    if protected_paths != PROTECTED_CANONICAL_INTEGRATION_PATHS:
        errors.append("protected_paths_not_exact")
    if set(_listish_values(receipt.get("exact_allowed_write_paths", []))) != (
        PROTECTED_CANONICAL_INTEGRATION_PATHS
    ):
        errors.append("receipt_paths_not_exact")

    admitted = receipt.get("admitted_job")
    if not isinstance(admitted, dict):
        admitted = {}
        errors.append("admitted_job_must_be_a_map")
    expected_identity = {
        "task_id": task_id,
        "job_id": str(job_row.get("job_id", "")).strip(),
        "plan_task_id": PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID,
        "role_id": str(job_row.get("role_id", "")).strip(),
    }
    for field_name, expected in expected_identity.items():
        if str(admitted.get(field_name, "")).strip() != expected:
            errors.append(f"admitted_job_{field_name}_mismatch")

    expected_job_path = str(job_row.get("job_path", "")).strip()
    if str(admitted.get("job_path", "")).strip() != expected_job_path:
        errors.append("admitted_job_path_mismatch")
    job_binding = {
        "path": admitted.get("job_path", ""),
        "sha256": admitted.get("job_sha256", ""),
    }
    bound_job = _protected_canonical_bound_yaml(
        {"bound_job": job_binding},
        "bound_job",
        errors,
    )
    if bound_job and bound_job != job_contract:
        errors.append("bound_job_content_mismatch")

    task_record = _protected_canonical_bound_task(admitted, errors)
    if task_record:
        for field_name, expected in (
            ("task_id", task_id),
            ("current_job_id", expected_identity["job_id"]),
            ("plan_task_id", PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID),
            ("approval_id", "approval-20260724-001"),
            (
                "human_authorization_id",
                "HUMAN-P4-T05-20260722-CONTINUUM-FIRST-01",
            ),
        ):
            if str(task_record.get(field_name, "")).strip() != expected:
                errors.append(f"bound_task_{field_name}_mismatch")

    completion_binding = {
        "path": admitted.get("completion_path", ""),
        "sha256": admitted.get("completion_sha256", ""),
    }
    completion = _protected_canonical_bound_yaml(
        {"bound_completion": completion_binding},
        "bound_completion",
        errors,
    )
    if completion:
        for field_name, expected in (
            ("job_id", expected_identity["job_id"]),
            ("task_id", task_id),
            ("completion_id", str(admitted.get("completion_id", "")).strip()),
        ):
            if str(completion.get(field_name, "")).strip() != expected:
                errors.append(f"bound_completion_{field_name}_mismatch")

    goal_route = receipt.get("immutable_goal_route")
    job_goal = job_contract.get("goal_receipt")
    if not isinstance(goal_route, dict) or not isinstance(job_goal, dict):
        errors.append("immutable_goal_route_missing")
    else:
        goal_expectations = {
            "goal_id": str(job_goal.get("goal_id", "")).strip(),
            "generation": job_goal.get("generation"),
            "plan_task_id": str(job_goal.get("route_work_item_id", "")).strip(),
            "worker_skill": str(job_goal.get("route_worker_skill", "")).strip(),
            "route_sha256": str(job_goal.get("route_sha256", "")).strip(),
        }
        for field_name, expected in goal_expectations.items():
            if goal_route.get(field_name) != expected:
                errors.append(f"immutable_goal_route_{field_name}_mismatch")
        if str(goal_route.get("generation", "")).strip() != "105":
            errors.append("immutable_goal_route_generation_not_105")
        if goal_route.get("plan_task_id") != PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID:
            errors.append("immutable_goal_route_plan_task_mismatch")
        if goal_route.get("worker_skill") != "continue-research":
            errors.append("immutable_goal_route_worker_mismatch")
        if str(job_contract.get("immutable_route_sha256", "")).strip() != str(
            goal_route.get("route_sha256", "")
        ).strip():
            errors.append("job_immutable_route_hash_mismatch")

    job_authority = job_contract.get("authorization_layers")
    if not isinstance(job_authority, dict):
        errors.append("job_authorization_layers_missing")
    else:
        if job_authority.get("canonical_ontology_edit_authorized") is not True:
            errors.append("canonical_ontology_edit_not_authorized")
        for field_name in (
            "downstream_physics_promotion_authorized",
            "benchmark_promotion_authorized",
            "completed_derivation_authorized",
            "source_law_adoption_authorized",
            "ontology_regime_selection_authorized",
            "physical_gauge_claim_authorized",
            "Gate_Chair_verdict_authorized",
            "global_no_go_claim_authorized",
        ):
            if job_authority.get(field_name) is not False:
                errors.append(f"job_authority_{field_name}_must_be_false")

    approval = _protected_canonical_bound_yaml(receipt, "approval", errors)
    if approval:
        for field_name, expected in (
            ("approval_id", "approval-20260724-001"),
            ("status", "consumed"),
            ("consumed_by", "AJ-RT-20260724-004-001"),
            ("expires_at", "AJ-RT-20260724-004-001"),
        ):
            if str(approval.get(field_name, "")).strip() != expected:
                errors.append(f"approval_{field_name}_mismatch")
        if approval.get("one_time_use") is not True:
            errors.append("approval_not_one_time_use")

    human_authorization = _protected_canonical_bound_yaml(
        receipt,
        "human_authorization",
        errors,
    )
    if human_authorization:
        if (
            human_authorization.get("human_authorization_id")
            != "HUMAN-P4-T05-20260722-CONTINUUM-FIRST-01"
        ):
            errors.append("human_authorization_id_mismatch")
        boundary = human_authorization.get("canonical_integration_boundary")
        if not isinstance(boundary, dict) or boundary.get("p4_t06_authorized") is not True:
            errors.append("human_authorization_p4_t06_not_authorized")
        if not _listish_values(human_authorization.get("non_authorizations", [])):
            errors.append("human_authorization_non_authorizations_missing")

    _protected_canonical_bound_file(receipt, "gate_decision", errors)
    route_authorization = _protected_canonical_bound_yaml(
        receipt,
        "route_authorization",
        errors,
    )
    if route_authorization:
        for field_name, expected in (
            ("status", "authorized_after_recovery_and_checkpoint"),
            ("approval_id", "approval-20260724-001"),
            (
                "human_authorization_id",
                "HUMAN-P4-T05-20260722-CONTINUUM-FIRST-01",
            ),
            ("selected_next_plan_task_id", PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID),
            ("selected_next_worker_skill", "continue-research"),
            ("validation_status", "PASS"),
        ):
            if str(route_authorization.get(field_name, "")).strip() != expected:
                errors.append(f"route_authorization_{field_name}_mismatch")
        if not _listish_values(route_authorization.get("forbidden_scope", [])):
            errors.append("route_authorization_forbidden_scope_missing")

    source_handoff = _protected_canonical_bound_yaml(receipt, "source_handoff", errors)
    if source_handoff:
        selected_route = source_handoff.get("selected_next_route")
        if (
            not isinstance(selected_route, dict)
            or selected_route.get("plan_task_id")
            != PROTECTED_CANONICAL_INTEGRATION_PLAN_TASK_ID
            or selected_route.get("worker_skill") != "continue-research"
        ):
            errors.append("source_handoff_route_mismatch")

    limits = receipt.get("authority_limits")
    if not isinstance(limits, dict):
        errors.append("authority_limits_missing")
    else:
        if limits.get("exact_scope_satisfied") is not True:
            errors.append("exact_scope_not_satisfied")
        for field_name in (
            "authority_expanded_beyond_scope",
            "approval_reused",
            "p4_t06_reexecuted",
            "physical_status_changed",
            "source_law_adopted",
            "distance_to_gr_changed",
            "benchmark_promotion_authorized",
            "physics_promotion_authorized",
            "proof_authority",
            "publication_authorized",
            "push_authorized",
            "completed_derivation_authorized",
        ):
            if limits.get(field_name) is not False:
                errors.append(f"authority_limit_{field_name}_must_be_false")

    if errors:
        path_text = job_row.get("job_path", job_row.get("job_id", ""))
        report.error(
            f"{path_text}: protected canonical integration admission invalid: "
            + ", ".join(sorted(set(errors)))
        )
        return False
    return True


def active_program_task_id() -> str:
    try:
        program_state = load_yaml(CONTROL_DIR / "program_state.yaml")
    except StrictYamlError:
        return ""
    if not isinstance(program_state, dict):
        return ""
    return str(program_state.get("active_task_id", "")).strip()


def memory_preflight_hash_must_be_current(job_row: dict[str, str], object_id: str) -> bool:
    if object_id in SELF_REFERENTIAL_GENERATED_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS:
        return False
    if object_id not in MUTABLE_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS:
        return True
    active_task = active_program_task_id()
    return bool(active_task and job_row.get("task_id", "") == active_task)


def validate_memory_preflight(
    report: ValidationReport,
    job_row: dict[str, str],
    record: dict[str, Any],
    owner_path: str,
) -> None:
    if not memory_preflight_required(job_row):
        return
    preflight = record.get("memory_preflight")
    if not isinstance(preflight, dict):
        report.error(f"{owner_path}: future AgentJob record missing memory_preflight")
        return

    status_command = str(preflight.get("status_command", "")).strip()
    if "query_memory.py status --json" not in status_command:
        report.error(f"{owner_path}: memory_preflight.status_command must run query_memory.py status --json")

    status_summary = preflight.get("status_summary")
    if not isinstance(status_summary, dict):
        report.error(f"{owner_path}: memory_preflight.status_summary must be a map")
    else:
        for field_name in ["vault_exists", "memory_index_exists", "source_object_count"]:
            if field_name not in status_summary:
                report.error(f"{owner_path}: memory_preflight.status_summary missing {field_name}")

    authority_note = str(preflight.get("authority_note", "")).strip().lower()
    required_terms = ["obsidian", ".local", "retrieval", "not authority"]
    missing_terms = [term for term in required_terms if term not in authority_note]
    if missing_terms:
        report.error(
            f"{owner_path}: memory_preflight.authority_note must preserve retrieval-only authority terms {missing_terms}"
        )

    queries = preflight.get("queries")
    if not isinstance(queries, list) or not queries:
        report.error(f"{owner_path}: memory_preflight.queries must contain at least one query receipt")
        queries = []

    returned_object_ids: set[str] = set()
    for index, query in enumerate(queries):
        if not isinstance(query, dict):
            report.error(f"{owner_path}: memory_preflight.queries[{index}] must be a map")
            continue
        command = str(query.get("command", "")).strip()
        query_type = str(query.get("query_type", "")).strip()
        if "query_memory.py" not in command:
            report.error(f"{owner_path}: memory_preflight.queries[{index}].command must run query_memory.py")
        if query_type not in {"lookup", "search"}:
            report.error(f"{owner_path}: memory_preflight.queries[{index}].query_type must be lookup or search")
        if not str(query.get("query_text", "")).strip():
            report.error(f"{owner_path}: memory_preflight.queries[{index}].query_text is required")
        object_ids = query.get("returned_object_ids")
        if not isinstance(object_ids, list) or not object_ids:
            report.error(
                f"{owner_path}: memory_preflight.queries[{index}].returned_object_ids must be nonempty"
            )
            continue
        for object_id in object_ids:
            object_text = str(object_id).strip()
            if object_text:
                returned_object_ids.add(object_text)

    inspections = preflight.get("canonical_inspections")
    if not isinstance(inspections, list) or not inspections:
        report.error(f"{owner_path}: memory_preflight.canonical_inspections must be nonempty")
        inspections = []

    inspected_ids: set[str] = set()
    for index, inspection in enumerate(inspections):
        if not isinstance(inspection, dict):
            report.error(f"{owner_path}: memory_preflight.canonical_inspections[{index}] must be a map")
            continue
        object_id = str(inspection.get("object_id", "")).strip()
        source_registry = str(inspection.get("source_registry", "")).strip()
        registry_path_text = str(inspection.get("registry_path", "")).strip()
        canonical_path_text = str(inspection.get("canonical_path", "")).strip()
        source_hash = str(inspection.get("source_hash", "")).strip()
        if object_id:
            inspected_ids.add(object_id)
        for field_name, value in [
            ("object_id", object_id),
            ("source_registry", source_registry),
            ("registry_path", registry_path_text),
            ("canonical_path", canonical_path_text),
            ("source_hash", source_hash),
        ]:
            if not value:
                report.error(
                    f"{owner_path}: memory_preflight.canonical_inspections[{index}].{field_name} is required"
                )

        if source_registry not in MEMORY_PREFLIGHT_SOURCE_REGISTRIES:
            report.error(
                f"{owner_path}: memory_preflight.canonical_inspections[{index}].source_registry is not an allowed source registry"
            )
            continue
        expected_registry_path = f"registries/{source_registry}"
        if registry_path_text != expected_registry_path:
            report.error(
                f"{owner_path}: memory_preflight.canonical_inspections[{index}].registry_path must be {expected_registry_path}"
            )
            continue
        reason = validate_relative_path(canonical_path_text)
        if reason:
            report.error(
                f"{owner_path}: invalid memory_preflight canonical_path {canonical_path_text}: {reason}"
            )
            continue
        registry_path = repo_path(registry_path_text)
        if not registry_path.exists():
            report.error(f"{owner_path}: memory_preflight registry path does not exist: {registry_path_text}")
            continue
        rows = read_csv_rows(source_registry)
        row = existing_by_id(rows, "object_id").get(object_id)
        if not row:
            report.error(
                f"{owner_path}: memory_preflight object {object_id} not found in {source_registry}"
            )
            continue
        if row.get("path", "") != canonical_path_text:
            report.error(
                f"{owner_path}: memory_preflight canonical_path does not match registry row for {object_id}"
            )
        require_current_hash = memory_preflight_hash_must_be_current(job_row, object_id)
        if require_current_hash and row.get("source_hash", "") != source_hash:
            report.error(
                f"{owner_path}: memory_preflight source_hash does not match registry row for {object_id}"
            )
        canonical_path = repo_path(canonical_path_text)
        if not canonical_path.exists():
            report.error(f"{owner_path}: memory_preflight canonical path does not exist: {canonical_path_text}")
            continue
        if require_current_hash and source_hash and sha256_file(canonical_path) != source_hash:
            report.error(
                f"{owner_path}: memory_preflight source_hash is stale for {canonical_path_text}"
            )

    missing_inspections = sorted(returned_object_ids - inspected_ids)
    if missing_inspections:
        generated_ids = [
            object_id
            for object_id in missing_inspections
            if object_id.startswith(("WIKI-", "VAULT-", "SEMANTIC-", "REL-"))
        ]
        if generated_ids:
            report.error(
                f"{owner_path}: memory_preflight returned generated retrieval IDs {generated_ids}; returned_object_ids must list inspected canonical source object IDs from source registries and generated retrieval IDs belong only in relationship or query evidence"
            )
        else:
            report.error(
                f"{owner_path}: memory_preflight returned canonical object IDs lack canonical inspection {missing_inspections}"
            )


def _listish_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        return split_semicolon(value)
    return []


def _has_substantive_value(value: Any) -> bool:
    return any(item.strip().lower() not in {"", "none"} for item in _listish_values(value))


def _substantive_list(value: Any) -> list[str]:
    return [
        item.strip()
        for item in _listish_values(value)
        if item.strip() and item.strip().lower() != "none"
    ]


def _validate_layer_evidence(
    report: ValidationReport,
    *,
    owner_path: str,
    layer_name: str,
    layer_record: dict[str, Any],
) -> None:
    evidence = layer_record.get("evidence")
    if not isinstance(evidence, list):
        report.error(f"{owner_path}: validation_layers.{layer_name}.evidence must be a list")
        return
    if not _substantive_list(evidence):
        report.error(
            f"{owner_path}: validation_layers.{layer_name}.evidence must explain the layer status"
        )


def validate_validation_layers(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    owner_path: str,
) -> None:
    if not validation_schema_split_policy_active(job_row, completion):
        return
    layers = completion.get("validation_layers")
    if not isinstance(layers, dict):
        report.error(f"{owner_path}: validation_layers map is required by validation-status schema split")
        return

    for layer_name in VALIDATION_LAYER_NAMES:
        layer_record = layers.get(layer_name)
        if not isinstance(layer_record, dict):
            report.error(f"{owner_path}: validation_layers.{layer_name} must be a map")
            continue
        status = str(layer_record.get("status", "")).strip()
        if not status:
            report.error(f"{owner_path}: validation_layers.{layer_name}.status is required")
        elif status not in VALIDATION_LAYER_STATUS_VALUES:
            report.error(
                f"{owner_path}: validation_layers.{layer_name}.status is not allowed: {status}"
            )
        _validate_layer_evidence(
            report,
            owner_path=owner_path,
            layer_name=layer_name,
            layer_record=layer_record,
        )

    for layer_name in sorted(set(layers) - set(VALIDATION_LAYER_NAMES)):
        report.warn(f"{owner_path}: validation_layers.{layer_name} is an extension layer")


def _authorization_source_path(record: dict[str, Any], field_name: str) -> str:
    source_field = AUTHORIZATION_LAYER_SOURCE_FIELDS.get(field_name, "")
    if not source_field:
        return ""
    return str(record.get(source_field, "")).strip()


def validate_authorization_layers(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    owner_path: str,
) -> None:
    if not validation_schema_split_policy_active(job_row, completion):
        return
    layers = completion.get("authorization_layers")
    if not isinstance(layers, dict):
        report.error(f"{owner_path}: authorization_layers map is required by validation-status schema split")
        return

    scope = str(layers.get(AUTHORIZATION_LAYER_SCOPE_FIELD, "")).strip()
    if not scope:
        report.error(f"{owner_path}: authorization_layers.{AUTHORIZATION_LAYER_SCOPE_FIELD} is required")

    for field_name in AUTHORIZATION_LAYER_BOOLEAN_FIELDS:
        if field_name not in layers:
            report.error(f"{owner_path}: authorization_layers.{field_name} is required")
            continue
        if not isinstance(layers.get(field_name), bool):
            report.error(f"{owner_path}: authorization_layers.{field_name} must be a boolean")
            continue
        if bool_value(layers.get(field_name)) and not _authorization_source_path(layers, field_name):
            report.error(
                f"{owner_path}: authorization_layers.{field_name} requires "
                f"{AUTHORIZATION_LAYER_SOURCE_FIELDS[field_name]}"
            )

    if bool_value(layers.get("protected_scoped_gate_review_authorized")) and scope.lower() in {
        "",
        "none",
        "not_applicable",
    }:
        report.error(
            f"{owner_path}: protected scoped gate authorization requires a non-empty scope"
        )

    progress = completion.get("physics_progress_status")
    if isinstance(progress, dict) and "physics_promotion_authorized" in progress:
        legacy_value = bool_value(progress.get("physics_promotion_authorized"))
        split_value = bool_value(layers.get("downstream_physics_promotion_authorized"))
        if legacy_value != split_value:
            report.error(
                f"{owner_path}: physics_progress_status.physics_promotion_authorized "
                "must match authorization_layers.downstream_physics_promotion_authorized"
            )


def _string_field(record: Any, field_name: str) -> str:
    if not isinstance(record, dict):
        return ""
    return str(record.get(field_name, "")).strip()


def _is_no_go_present(status: str) -> bool:
    lowered = status.strip().lower()
    if not lowered or lowered in {"not_proved", "not proved", "none", "false"}:
        return False
    return any(marker in lowered for marker in ONTOLOGY_LAW_NO_GO_PRESENT_MARKERS)


def _protected_authority_expansions(value: Any) -> list[str]:
    protected: list[str] = []
    for item in _listish_values(value):
        lowered = item.strip().lower()
        if lowered in {"", "none"}:
            continue
        if any(marker in lowered for marker in PROTECTED_AUTHORITY_MARKERS):
            protected.append(item)
    return protected


def _path_allowed_by_patterns(path_text: str, patterns: list[str]) -> bool:
    normalized = path_text.strip().lstrip("./")
    return any(_path_matches(normalized, pattern.strip().lstrip("./")) for pattern in patterns)


def _parent_child_authority_keys(value: Any, prefix: str = "role_decomposition") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}"
            if str(key) in PARENT_CHILD_FORBIDDEN_AUTHORITY_KEYS:
                found.append(child_prefix)
            found.extend(_parent_child_authority_keys(child, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_parent_child_authority_keys(child, f"{prefix}[{index}]"))
    return found


def _validate_decomposition_path(
    report: ValidationReport,
    *,
    path_text: str,
    owner_path: str,
    field_name: str,
    allowed_patterns: list[str],
) -> None:
    if not path_text:
        report.error(f"{owner_path}: role_decomposition.{field_name} is required")
        return
    reason = validate_relative_path(path_text)
    if reason:
        report.error(f"{owner_path}: invalid role_decomposition.{field_name}: {reason}")
        return
    if not _path_allowed_by_patterns(path_text, allowed_patterns):
        report.error(
            f"{owner_path}: role_decomposition.{field_name} is outside AgentJob allowlist: {path_text}"
        )


def _nonnegative_int(value: Any) -> int | None:
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, str) and value.strip().isdigit():
        parsed = int(value.strip())
        return parsed if parsed >= 0 else None
    return None


def _parent_child_job_paths(decomposition: dict[str, Any]) -> dict[str, str]:
    paths: dict[str, str] = {}
    children = decomposition.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                unit_id = str(child.get("execution_unit_id", "")).strip()
                output_path = str(child.get("output_path", "")).strip()
                if unit_id and output_path:
                    paths[f"children.{unit_id}.output_path"] = output_path
    conflict_policy = decomposition.get("conflict_policy", {})
    if isinstance(conflict_policy, dict):
        review_path = str(conflict_policy.get("review_path", "")).strip()
        if review_path:
            paths["conflict_policy.review_path"] = review_path
    fusion_policy = decomposition.get("fusion_policy", {})
    if isinstance(fusion_policy, dict):
        fusion_notes_path = str(fusion_policy.get("fusion_notes_path", "")).strip()
        if fusion_notes_path:
            paths["fusion_policy.fusion_notes_path"] = fusion_notes_path
        fused_output_path = str(fusion_policy.get("fused_output_path", "")).strip()
        if fused_output_path:
            paths["fusion_policy.fused_output_path"] = fused_output_path
    return paths


def validate_parent_child_decomposition(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
) -> None:
    decomposition = job_contract.get("role_decomposition")
    if decomposition in (None, "", []):
        return
    owner_path = job_row.get("job_path", job_row.get("job_id", "AgentJob"))
    if not isinstance(decomposition, dict):
        report.error(f"{owner_path}: role_decomposition must be a map")
        return

    if str(decomposition.get("mode", "")).strip() != PARENT_CHILD_SYNTHESIS_MODE:
        report.error(
            f"{owner_path}: role_decomposition.mode must be {PARENT_CHILD_SYNTHESIS_MODE}"
        )
    if str(decomposition.get("decomposition_version", "")).strip() != PARENT_CHILD_SYNTHESIS_VERSION:
        report.error(
            f"{owner_path}: role_decomposition.decomposition_version must be {PARENT_CHILD_SYNTHESIS_VERSION}"
        )

    authority_keys = _parent_child_authority_keys(decomposition)
    if authority_keys:
        report.error(
            f"{owner_path}: role_decomposition may not declare authority fields {sorted(authority_keys)}"
        )

    parent = decomposition.get("parent")
    if not isinstance(parent, dict):
        report.error(f"{owner_path}: role_decomposition.parent must be a map")
    else:
        if str(parent.get("execution_unit_id", "")).strip() != PARENT_CHILD_PARENT_UNIT_ID:
            report.error(
                f"{owner_path}: parent execution_unit_id must be {PARENT_CHILD_PARENT_UNIT_ID}"
            )
        if str(parent.get("perspective", "")).strip() != PARENT_CHILD_PARENT_PERSPECTIVE:
            report.error(
                f"{owner_path}: parent perspective must be {PARENT_CHILD_PARENT_PERSPECTIVE}"
            )

    children = decomposition.get("children")
    seen_children: dict[str, str] = {}
    if not isinstance(children, list) or len(children) != 2:
        report.error(f"{owner_path}: role_decomposition.children must contain exactly two children")
    else:
        for child in children:
            if not isinstance(child, dict):
                report.error(f"{owner_path}: role_decomposition.children entries must be maps")
                continue
            unit_id = str(child.get("execution_unit_id", "")).strip()
            perspective = str(child.get("perspective", "")).strip()
            expected_perspective = PARENT_CHILD_REQUIRED_CHILDREN.get(unit_id)
            if expected_perspective is None:
                report.error(f"{owner_path}: unsupported child execution_unit_id {unit_id}")
            elif perspective != expected_perspective:
                report.error(
                    f"{owner_path}: child {unit_id} perspective must be {expected_perspective}"
                )
            output_path = str(child.get("output_path", "")).strip()
            if not output_path:
                report.error(f"{owner_path}: child {unit_id} output_path is required")
            seen_children[unit_id] = perspective
        missing = sorted(set(PARENT_CHILD_REQUIRED_CHILDREN) - set(seen_children))
        if missing:
            report.error(f"{owner_path}: role_decomposition missing children {missing}")

    conflict_policy = decomposition.get("conflict_policy")
    if not isinstance(conflict_policy, dict):
        report.error(f"{owner_path}: role_decomposition.conflict_policy must be a map")
    else:
        if "review_path" not in conflict_policy:
            report.error(f"{owner_path}: conflict_policy.review_path is required")
        max_rounds = _nonnegative_int(conflict_policy.get("max_resolution_rounds"))
        if max_rounds is None:
            report.error(f"{owner_path}: conflict_policy.max_resolution_rounds must be a nonnegative integer")
        if conflict_policy.get("require_parallel_child_revision") is not True:
            report.error(f"{owner_path}: conflict_policy.require_parallel_child_revision must be true")
        if str(conflict_policy.get("unresolved_conflict_status", "")).strip() != "blocked":
            report.error(f"{owner_path}: conflict_policy.unresolved_conflict_status must be blocked")

    fusion_policy = decomposition.get("fusion_policy")
    fused_output_path = ""
    if not isinstance(fusion_policy, dict):
        report.error(f"{owner_path}: role_decomposition.fusion_policy must be a map")
    else:
        if "fusion_notes_path" not in fusion_policy:
            report.error(f"{owner_path}: fusion_policy.fusion_notes_path is required")
        fused_output_path = str(fusion_policy.get("fused_output_path", "")).strip()
        if not fused_output_path:
            report.error(f"{owner_path}: fusion_policy.fused_output_path is required")
        for field_name in [
            "preserve_shared_consensus",
            "preserve_unique_contributions",
            "preserve_unresolved_limitations",
            "final_output_replaces_old_single_role_artifact",
        ]:
            if fusion_policy.get(field_name) is not True:
                report.error(f"{owner_path}: fusion_policy.{field_name} must be true")

    allowed_patterns = _listish_values(job_contract.get("allowed_write_paths", []))
    if not allowed_patterns:
        report.error(f"{owner_path}: role_decomposition requires AgentJob allowed_write_paths")
    for field_name, path_text in _parent_child_job_paths(decomposition).items():
        _validate_decomposition_path(
            report,
            path_text=path_text,
            owner_path=owner_path,
            field_name=field_name,
            allowed_patterns=allowed_patterns,
        )

    expected_outputs = set(_listish_values(job_contract.get("expected_outputs", [])))
    registry_outputs = set(split_semicolon(job_row.get("output_paths", "")))
    if fused_output_path:
        if fused_output_path not in expected_outputs:
            report.error(
                f"{owner_path}: fusion_policy.fused_output_path must appear in expected_outputs"
            )
        if fused_output_path not in registry_outputs:
            report.error(
                f"{owner_path}: fusion_policy.fused_output_path must appear in AGENT_JOB_REGISTRY output_paths"
            )


def _completion_child_outputs_by_id(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        return {}
    by_unit: dict[str, dict[str, Any]] = {}
    for item in value:
        if isinstance(item, dict):
            unit_id = str(item.get("execution_unit_id", "")).strip()
            if unit_id:
                by_unit[unit_id] = item
    return by_unit


def _has_unresolved_blocking_conflict(conflict_review: dict[str, Any]) -> bool:
    status = str(conflict_review.get("status", "")).strip()
    if status in {"blocked", "unresolved_blocking"}:
        return True
    conflicts = conflict_review.get("unresolved_conflicts", [])
    if not isinstance(conflicts, list):
        return False
    for conflict in conflicts:
        if isinstance(conflict, str) and conflict.strip():
            return True
        if isinstance(conflict, dict) and str(conflict.get("severity", "")).strip() == "blocking":
            return True
    return False


def validate_parent_child_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    decomposition = job_contract.get("role_decomposition")
    if not isinstance(decomposition, dict):
        return
    path_text = path.relative_to(REPO_ROOT).as_posix()
    synthesis = completion.get("parent_child_synthesis")
    if not isinstance(synthesis, dict):
        report.error(f"{path_text}: parent-child AgentJob completion missing parent_child_synthesis")
        return
    if str(synthesis.get("mode", "")).strip() != PARENT_CHILD_SYNTHESIS_MODE:
        report.error(f"{path_text}: parent_child_synthesis.mode must be {PARENT_CHILD_SYNTHESIS_MODE}")
    if str(synthesis.get("decomposition_version", "")).strip() != PARENT_CHILD_SYNTHESIS_VERSION:
        report.error(
            f"{path_text}: parent_child_synthesis.decomposition_version must be {PARENT_CHILD_SYNTHESIS_VERSION}"
        )

    job_children = {
        str(child.get("execution_unit_id", "")).strip(): child
        for child in decomposition.get("children", [])
        if isinstance(child, dict)
    }
    completion_children = _completion_child_outputs_by_id(synthesis.get("child_outputs"))
    if set(completion_children) != set(PARENT_CHILD_REQUIRED_CHILDREN):
        report.error(
            f"{path_text}: parent_child_synthesis.child_outputs must name exactly {sorted(PARENT_CHILD_REQUIRED_CHILDREN)}"
        )
    for unit_id, expected_perspective in PARENT_CHILD_REQUIRED_CHILDREN.items():
        child = completion_children.get(unit_id)
        job_child = job_children.get(unit_id, {})
        if not child:
            continue
        if str(child.get("perspective", "")).strip() != expected_perspective:
            report.error(f"{path_text}: child output {unit_id} perspective must be {expected_perspective}")
        if str(child.get("output_path", "")).strip() != str(job_child.get("output_path", "")).strip():
            report.error(f"{path_text}: child output {unit_id} path must match AgentJob role_decomposition")
        if completion.get("validation_status") == "PASS" and str(child.get("status", "")).strip() != "completed":
            report.error(f"{path_text}: PASS parent-child completion requires child {unit_id} status completed")

    conflict_review = synthesis.get("conflict_review")
    if not isinstance(conflict_review, dict):
        report.error(f"{path_text}: parent_child_synthesis.conflict_review must be a map")
    else:
        status = str(conflict_review.get("status", "")).strip()
        if status not in PARENT_CHILD_CONFLICT_STATUSES:
            report.error(f"{path_text}: conflict_review.status is not allowed: {status}")
        job_review_path = str(
            decomposition.get("conflict_policy", {}).get("review_path", "")
            if isinstance(decomposition.get("conflict_policy"), dict)
            else ""
        ).strip()
        if str(conflict_review.get("review_path", "")).strip() != job_review_path:
            report.error(f"{path_text}: conflict_review.review_path must match AgentJob role_decomposition")
        rounds = _nonnegative_int(conflict_review.get("resolution_rounds"))
        max_rounds = _nonnegative_int(
            decomposition.get("conflict_policy", {}).get("max_resolution_rounds")
            if isinstance(decomposition.get("conflict_policy"), dict)
            else None
        )
        if rounds is None:
            report.error(f"{path_text}: conflict_review.resolution_rounds must be a nonnegative integer")
        elif max_rounds is not None and rounds > max_rounds:
            report.error(f"{path_text}: conflict_review.resolution_rounds exceeds AgentJob max_resolution_rounds")
        for conflict in conflict_review.get("unresolved_conflicts", []):
            if not isinstance(conflict, dict):
                continue
            conflict_type = str(conflict.get("type", "")).strip()
            severity = str(conflict.get("severity", "")).strip()
            if conflict_type and conflict_type not in PARENT_CHILD_CONFLICT_TYPES:
                report.error(f"{path_text}: unresolved conflict type is not allowed: {conflict_type}")
            if severity and severity not in PARENT_CHILD_CONFLICT_SEVERITIES:
                report.error(f"{path_text}: unresolved conflict severity is not allowed: {severity}")
        if completion.get("validation_status") == "PASS" and _has_unresolved_blocking_conflict(conflict_review):
            report.error(f"{path_text}: PASS parent-child completion may not contain unresolved blocking conflicts")

    fusion = synthesis.get("fusion")
    fusion_policy = decomposition.get("fusion_policy", {})
    fused_output_path = (
        str(fusion_policy.get("fused_output_path", "")).strip()
        if isinstance(fusion_policy, dict)
        else ""
    )
    if not isinstance(fusion, dict):
        report.error(f"{path_text}: parent_child_synthesis.fusion must be a map")
    else:
        if str(fusion.get("fused_output_path", "")).strip() != fused_output_path:
            report.error(f"{path_text}: fusion.fused_output_path must match AgentJob role_decomposition")
        completion_outputs = set(_listish_values(completion.get("output_paths", [])))
        if completion.get("validation_status") == "PASS" and fused_output_path not in completion_outputs:
            report.error(f"{path_text}: fused output path must appear in completion.output_paths")


def validate_execution_roles(
    report: ValidationReport,
    execution_rows: list[dict[str, str]],
    roles: dict[str, dict[str, str]],
    jobs: dict[str, dict[str, str]],
    tasks: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    executions = existing_by_id(execution_rows, "execution_role_ref")
    jobs_to_execution_refs: dict[str, list[str]] = {}
    for row in execution_rows:
        execution_ref = row["execution_role_ref"]
        kind = row["role_execution_kind"]
        if kind not in ROLE_EXECUTION_KINDS:
            report.error(f"{execution_ref}: invalid role_execution_kind {kind}")
        reason = validate_relative_path(row["record_path"])
        if reason:
            report.error(f"{execution_ref}: invalid record_path: {reason}")
            continue
        path = repo_path(row["record_path"])
        if not path.exists():
            report.error(f"{execution_ref}: missing execution-role record {row['record_path']}")
            continue
        try:
            record = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{row['record_path']}: {exc}")
            continue
        for field_name in [
            "execution_role_ref",
            "role_execution_kind",
            "task_id",
            "agent_job_id",
            "base_role_id",
            "base_role_version",
            "provisional_role_name",
            "authority_delta_summary",
            "requires_human_gate",
            "expires_after",
            "justification",
            "non_reusable_until_registered",
        ]:
            if _frontmatter_value(record.get(field_name, "")) != row[field_name]:
                report.error(
                    f"{row['record_path']}: {field_name} does not match ROLE_EXECUTION_REGISTRY.csv"
                )
        for field_name in [
            "allowed_write_paths",
            "added_constraints",
            "removed_permissions",
            "expanded_permissions",
        ]:
            if _frontmatter_value(record.get(field_name, [])) != row[field_name]:
                report.error(
                    f"{row['record_path']}: {field_name} does not match ROLE_EXECUTION_REGISTRY.csv"
                )
        if row["task_id"] not in tasks:
            report.error(f"{execution_ref}: task_id is not registered")
        job = jobs.get(row["agent_job_id"])
        if not job:
            report.error(f"{execution_ref}: agent_job_id is not registered")
        elif job["task_id"] != row["task_id"]:
            report.error(f"{execution_ref}: task_id does not match AgentJob task_id")
        jobs_to_execution_refs.setdefault(row["agent_job_id"], []).append(execution_ref)

        for item in _listish_values(record.get("allowed_write_paths", [])):
            reason = validate_relative_path(item.replace("**", "x").replace("*", "x"))
            if reason:
                report.error(f"{row['record_path']}: invalid allowed_write_paths entry {item}: {reason}")

        if kind in {"registered_role", "task_overlay"}:
            base_role = row["base_role_id"]
            base_role_ref = role_key(base_role, row["base_role_version"])
            if not base_role:
                report.error(f"{execution_ref}: {kind} requires base_role_id")
            elif base_role_ref not in roles:
                report.error(f"{execution_ref}: base_role_id is not registered")
        if kind == "registered_role":
            if _has_substantive_value(record.get("expanded_permissions", [])):
                report.error(f"{execution_ref}: registered_role may not expand permissions")
            if row["non_reusable_until_registered"] != "false":
                report.error(f"{execution_ref}: registered_role must be reusable")
        if kind == "task_overlay":
            if not _has_substantive_value(record.get("added_constraints", [])) and not _has_substantive_value(
                record.get("removed_permissions", [])
            ) and not _has_substantive_value(record.get("expanded_permissions", [])):
                report.error(f"{execution_ref}: task_overlay must declare an authority delta")
            protected = _protected_authority_expansions(record.get("expanded_permissions", []))
            if protected and row["requires_human_gate"] != "true":
                report.error(
                    f"{execution_ref}: protected expanded_permissions require a human gate"
                )
        if kind == "one_job_provisional_role":
            base_role = row["base_role_id"]
            base_version = row["base_role_version"]
            if bool(base_role) != bool(base_version):
                report.error(
                    f"{execution_ref}: provisional role base_role_id and base_role_version must be provided together"
                )
            elif base_role:
                base_role_ref = role_key(base_role, base_version)
                if base_role_ref not in roles:
                    report.error(f"{execution_ref}: provisional base_role_id is not registered")
            if not row["provisional_role_name"]:
                report.error(f"{execution_ref}: provisional role requires provisional_role_name")
            if not row["justification"]:
                report.error(f"{execution_ref}: provisional role requires justification")
            if row["non_reusable_until_registered"] != "true":
                report.error(f"{execution_ref}: provisional role must be non-reusable until registered")
            if row["expires_after"] != row["agent_job_id"]:
                report.error(f"{execution_ref}: provisional role must expire after its AgentJob")
            protected = _protected_authority_expansions(record.get("expanded_permissions", []))
            if protected and row["requires_human_gate"] != "true":
                report.error(
                    f"{execution_ref}: protected expanded_permissions require a human gate"
                )

    for job_id, job in jobs.items():
        execution_refs = jobs_to_execution_refs.get(job_id, [])
        if len(execution_refs) != 1:
            report.error(f"{job_id}: expected exactly one execution-role record, found {len(execution_refs)}")
            continue
        job_path_text = job.get("job_path", "")
        if not job_path_text:
            continue
        job_path = repo_path(job_path_text)
        if not job_path.exists():
            continue
        try:
            job_contract = load_yaml(job_path)
        except StrictYamlError:
            continue
        execution_role_ref = str(job_contract.get("execution_role_ref", ""))
        if execution_role_ref and execution_role_ref != execution_refs[0]:
            report.error(f"{job_path_text}: execution_role_ref does not match ROLE_EXECUTION_REGISTRY.csv")
        if not execution_role_ref and job["status"] in {"pending", "active"}:
            report.error(f"{job_path_text}: pending or active AgentJob must declare execution_role_ref")
    return executions


def validate_completion(report: ValidationReport, job_row: dict[str, str], path: Path) -> None:
    try:
        completion = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
        return
    expected_id = f"AJC-{job_row['job_id']}"
    if str(completion.get("completion_id", "")) != expected_id:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: completion_id must be {expected_id}")
    if str(completion.get("job_id", "")) != job_row["job_id"]:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: job_id mismatch")
    command_results = completion.get("command_results", [])
    if not isinstance(command_results, list) or not command_results:
        report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: missing command_results")
    validate_physics_payload_ratio_policy_record(
        report,
        completion,
        path.relative_to(REPO_ROOT).as_posix(),
    )
    validate_memory_preflight(report, job_row, completion, path.relative_to(REPO_ROOT).as_posix())
    validate_validation_layers(report, job_row, completion, path.relative_to(REPO_ROOT).as_posix())
    validate_authorization_layers(report, job_row, completion, path.relative_to(REPO_ROOT).as_posix())

    job_path_text = job_row.get("job_path", "")
    if not job_path_text:
        return
    try:
        job_contract = load_yaml(repo_path(job_path_text))
    except StrictYamlError as exc:
        report.error(f"{job_path_text}: {exc}")
        return
    dual_budget = evaluate_dual_budget_completion(
        job_contract,
        completion,
        created_at=job_row.get("created_at", ""),
    )
    for error in dual_budget["errors"]:
        report.error(
            f"{path.relative_to(REPO_ROOT).as_posix()}: dual-budget completion: {error}"
        )
    validate_parent_child_completion(report, job_row, job_contract, completion, path)
    validate_loop_control_completion(report, job_row, job_contract, completion, path)
    validate_mathematical_decisiveness_completion(
        report,
        job_row,
        job_contract,
        completion,
        path,
    )
    validate_countermodel_obligation_completion(
        report,
        job_row,
        job_contract,
        completion,
        path.relative_to(REPO_ROOT).as_posix(),
    )
    validate_ontology_law_research_packet(report, job_row, job_contract, completion, path)
    validate_source_extension_classification_receipt(
        report,
        job_row,
        job_contract,
        completion,
        path.relative_to(REPO_ROOT).as_posix(),
    )
    validate_completion_resolver_snapshots(report, completion, job_contract, path)


def extract_physics_payload_ratio_policy_record(container: dict[str, Any]) -> dict[str, Any] | None:
    record = container.get("physics_payload_ratio_policy_record")
    if isinstance(record, dict):
        return record
    if container.get("policy_id") == PHYSICS_PAYLOAD_RATIO_POLICY_ID:
        return container
    return None


def _payload_ratio_source_label(owner_path: str, index: int | None = None) -> str:
    if index is None:
        return owner_path
    return f"{owner_path}[{index}]"


def _payload_ratio_text(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("status", "")
    if value is None:
        return ""
    return str(value).strip()


def _payload_ratio_active_exception(record: dict[str, Any]) -> str:
    return _payload_ratio_text(record.get("active_exception")).lower()


def _payload_ratio_exception_has_evidence(record: dict[str, Any]) -> bool:
    evidence_fields = (
        "exception_source_path",
        "exception_evidence",
        "exception_evidence_path",
        "exception_receipt_path",
        "exception_receipt",
    )
    for field_name in evidence_fields:
        value = record.get(field_name)
        if isinstance(value, str) and value.strip():
            return True
        if isinstance(value, (dict, list)) and value:
            return True
    return False


def _payload_ratio_selected_task_type(record: dict[str, Any]) -> str:
    for field_name in (
        "selected_next_task_type",
        "selected_task_type",
        "next_task_type",
        "task_type",
    ):
        value = _payload_ratio_text(record.get(field_name))
        if value:
            return value
    return ""


def _payload_ratio_required_task_types(record: dict[str, Any]) -> set[str]:
    values = record.get("required_next_task_type_one_of")
    if not isinstance(values, list):
        return set(PHYSICS_PAYLOAD_RATIO_REQUIRED_TASK_TYPES)
    normalized = {str(value).strip() for value in values if str(value).strip()}
    return normalized or set(PHYSICS_PAYLOAD_RATIO_REQUIRED_TASK_TYPES)


def _payload_ratio_selected_is_physics_bearing(record: dict[str, Any]) -> bool:
    if bool_value(record.get("selected_packet_physics_bearing")) or bool_value(
        record.get("physics_bearing_task")
    ):
        return True
    selected_task_type = _payload_ratio_selected_task_type(record)
    return selected_task_type in _payload_ratio_required_task_types(record)


def _payload_ratio_selected_is_project_system(record: dict[str, Any]) -> bool:
    if bool_value(record.get("selected_packet_project_system")) or bool_value(
        record.get("project_system_task")
    ):
        return True
    selected_task_type = _payload_ratio_selected_task_type(record).lower()
    if selected_task_type in _payload_ratio_required_task_types(record):
        return False
    return any(token in selected_task_type for token in PHYSICS_PAYLOAD_RATIO_PROJECT_SYSTEM_TOKENS)


def _payload_ratio_claims_physics_delta(record: dict[str, Any]) -> bool:
    for field_name in PHYSICS_PAYLOAD_RATIO_DELTA_CLAIM_KEYS:
        if bool_value(record.get(field_name)):
            return True
    status_text = _payload_ratio_text(record.get("physics_progress_status")).lower()
    if not status_text:
        return False
    if any(token in status_text for token in PHYSICS_PAYLOAD_RATIO_NO_DELTA_STATUS_TOKENS):
        return False
    return "physics_delta" in status_text or "physics delta" in status_text


def physics_payload_ratio_policy_findings(
    record: dict[str, Any],
    source_label: str,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    policy_id = _payload_ratio_text(record.get("policy_id"))
    if policy_id and policy_id != PHYSICS_PAYLOAD_RATIO_POLICY_ID:
        findings.append(
            {
                "code": "policy_id_mismatch",
                "severity": "overclaim_hard_fail",
                "message": (
                    f"{source_label}: physics_payload_ratio_policy_record policy_id "
                    f"must be {PHYSICS_PAYLOAD_RATIO_POLICY_ID}"
                ),
            }
        )
        return findings

    threshold = int_value(
        record.get("after_project_system_tasks", record.get("threshold")),
        PHYSICS_PAYLOAD_RATIO_THRESHOLD_DEFAULT,
    )
    project_system_count = int_value(
        record.get(
            "consecutive_project_system_task_count",
            record.get("project_system_task_run_length"),
        )
    )
    threshold_met = bool_value(record.get("threshold_met")) or project_system_count >= threshold
    active_exception = _payload_ratio_active_exception(record)
    exception_known = active_exception in PHYSICS_PAYLOAD_RATIO_EXCEPTIONS
    selected_is_physics_bearing = _payload_ratio_selected_is_physics_bearing(record)
    selected_is_project_system = _payload_ratio_selected_is_project_system(record)

    if selected_is_project_system and _payload_ratio_claims_physics_delta(record):
        findings.append(
            {
                "code": "process_task_claims_physics_delta",
                "severity": "overclaim_hard_fail",
                "message": (
                    f"{source_label}: process task claims a physics delta under "
                    f"{PHYSICS_PAYLOAD_RATIO_POLICY_ID}"
                ),
            }
        )

    if active_exception and (not exception_known or not _payload_ratio_exception_has_evidence(record)):
        detail = "unsupported exception" if not exception_known else "missing exception evidence"
        findings.append(
            {
                "code": "exception_declared_without_evidence",
                "severity": "warn_current_control",
                "message": (
                    f"{source_label}: payload-ratio exception is declared with {detail}: "
                    f"{active_exception or '<blank>'}"
                ),
            }
        )
        return findings

    if active_exception and exception_known:
        return findings

    if threshold_met:
        findings.append(
            {
                "code": "project_system_run_exceeds_threshold",
                "severity": "warn_current_control",
                "message": (
                    f"{source_label}: consecutive project-system task count "
                    f"{project_system_count} meets advisory threshold {threshold}"
                ),
            }
        )
        if not selected_is_physics_bearing:
            selected_task_type = _payload_ratio_selected_task_type(record) or "<blank>"
            findings.append(
                {
                    "code": "physics_payload_missing_after_threshold",
                    "severity": "warn_current_control",
                    "message": (
                        f"{source_label}: selected next task type {selected_task_type} "
                        "is not physics-bearing under the payload-ratio policy"
                    ),
                }
            )

    return findings


def validate_physics_payload_ratio_policy_record(
    report: ValidationReport,
    container: dict[str, Any],
    owner_path: str,
) -> None:
    record = extract_physics_payload_ratio_policy_record(container)
    if record is None:
        return
    for finding in physics_payload_ratio_policy_findings(record, owner_path):
        message = f"{finding['code']}: {finding['message']}"
        if finding["severity"].startswith("overclaim_hard_fail"):
            report.error(message)
        else:
            report.warn(message)


def validate_physics_payload_ratio_policy_records(
    report: ValidationReport,
    records: list[dict[str, Any]],
    owner_path: str,
) -> None:
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            report.error(f"{_payload_ratio_source_label(owner_path, index)}: record must be a map")
            continue
        source_label = _payload_ratio_text(item.get("source")) or _payload_ratio_source_label(
            owner_path,
            index,
        )
        record = extract_physics_payload_ratio_policy_record(item) or item
        for finding in physics_payload_ratio_policy_findings(record, source_label):
            message = f"{finding['code']}: {finding['message']}"
            if finding["severity"].startswith("overclaim_hard_fail"):
                report.error(message)
            else:
                report.warn(message)


def evaluate_physics_payload_ratio_policy_records(
    records: list[dict[str, Any]],
    sample: str = "fixture",
) -> dict[str, Any]:
    report = ValidationReport()
    validate_physics_payload_ratio_policy_records(report, records, sample)
    warnings = [
        {"code": message.split(":", 1)[0], "message": message}
        for message in report.warnings
    ]
    hard_failures = [
        {"code": message.split(":", 1)[0], "message": message}
        for message in report.errors
    ]
    status = "HARD_FAIL" if hard_failures else "WARN" if warnings else "PASS"
    return {
        "schema_id": "physics_payload_ratio_policy_validator_pilot_v1",
        "policy_id": PHYSICS_PAYLOAD_RATIO_POLICY_ID,
        "status": status,
        "warning_count": len(warnings),
        "hard_failure_count": len(hard_failures),
        "warnings": warnings,
        "hard_failures": hard_failures,
        "authority_boundary": {
            "initial_enforcement": "advisory",
            "warnings_are_hard_gates": False,
            "hard_failures_are_overclaim_only": True,
            "physics_claim_authority_created": False,
            "proof_authority_created": False,
        },
    }


def load_physics_payload_ratio_policy_fixture(path: Path) -> tuple[str, str, list[dict[str, Any]]]:
    fixture = load_yaml(path)
    fixture_id = _payload_ratio_text(fixture.get("fixture_id")) or path.stem
    expected_status = _payload_ratio_text(fixture.get("expected_status")) or "PASS"
    records = fixture.get("records", [])
    if not isinstance(records, list):
        records = []
    return fixture_id, expected_status, records


def evaluate_physics_payload_ratio_policy_fixture(path: Path) -> dict[str, Any]:
    fixture_id, expected_status, records = load_physics_payload_ratio_policy_fixture(path)
    report = evaluate_physics_payload_ratio_policy_records(records, sample=fixture_id)
    report["fixture_id"] = fixture_id
    report["expected_status"] = expected_status
    report["matches_expected"] = report["status"] == expected_status
    return report


def validate_loop_control_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    role_id = job_row.get("role_id", "")
    if role_id not in PHYSICS_ROLE_IDS:
        return
    if not job_policy_active(job_row, completion):
        return

    path_text = path.relative_to(REPO_ROOT).as_posix()
    validate_distance_to_gr_status(
        report,
        completion,
        path_text,
        (
            ROADMAP_DISTANCE_TO_GR_REQUIRED_BURDENS
            if gr_derivation_roadmap_policy_active(job_row, completion)
            else DISTANCE_TO_GR_REQUIRED_BURDENS
        ),
    )
    validate_distance_to_gr_delta_effect(report, job_row, completion, path_text)
    if gr_derivation_roadmap_policy_active(job_row, completion):
        validate_general_physics_payload(report, completion, path_text)

    if role_id == "refuter" and "stress" in text_blob(job_contract, completion):
        validate_refuter_loop_decision(report, job_row, completion, path_text)
    if role_id == "ontology-formalizer":
        validate_ontology_formalizer_payload(report, completion, path_text)
    if role_id == "candidate-constructor" and any(
        marker in text_blob(job_contract, completion)
        for marker in ("bridge", "observer-readout", "observer readout", "([n]_u", "g_eff")
    ):
        validate_candidate_bridge_attempt(report, completion, path_text)
    if role_id == "theoretical-continuation-selector":
        validate_theoretical_continuation_decision(report, job_row, completion, path_text)


def validate_mathematical_decisiveness_completion(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    if not mathematical_decisiveness_warning_policy_active(job_row, job_contract, completion):
        return

    path_text = path.relative_to(REPO_ROOT).as_posix()
    prefix = f"{path_text}: mathematical decisiveness"

    for field_name in MATHEMATICAL_DECISIVENESS_REQUIRED_FIELDS:
        if field_name not in completion:
            report.error(f"{prefix}: missing {field_name}")

    progress = completion.get("physics_progress_status")
    status = ""
    promotion_authorized = False
    if isinstance(progress, dict):
        status = str(progress.get("status", "")).strip()
        promotion_authorized = bool_value(progress.get("physics_promotion_authorized"))
        if not status:
            report.error(f"{prefix}: physics_progress_status.status is required")
        elif status not in PHYSICS_PROGRESS_STATUS_VALUES:
            report.error(f"{prefix}: physics_progress_status.status is not allowed: {status}")
        if promotion_authorized and not str(progress.get("promotion_authority_path", "")).strip():
            report.error(f"{prefix}: physics_promotion_authorized requires promotion_authority_path")
    elif "physics_progress_status" in completion:
        report.error(f"{prefix}: physics_progress_status should be a map")

    delta = completion.get("distance_to_gr_delta")
    if isinstance(delta, dict):
        if bool_value(delta.get("changed")) and not (
            bool_value(delta.get("ledger_row_updated"))
            or str(delta.get("ledger_update_rationale", "")).strip()
            or str(delta.get("explanation", "")).strip()
        ):
            report.error(
                f"{prefix}: changed distance_to_gr_delta should include ledger update or rationale"
            )
        downstream_unlocked = delta.get("downstream_unlocked", [])
        if isinstance(downstream_unlocked, list):
            for item in downstream_unlocked:
                unlocked = str(item).strip().lower().replace("-", "_")
                if unlocked in UNAUTHORIZED_DOWNSTREAM_GR_UNLOCKS and not promotion_authorized:
                    report.error(
                        f"{prefix}: distance_to_gr_delta.downstream_unlocked may not unlock "
                        f"{item} without human-gated physics promotion authority"
                    )
    elif "distance_to_gr_delta" in completion:
        report.error(f"{prefix}: distance_to_gr_delta should be a map")

    manifest = completion.get("mathematical_payload_manifest")
    if isinstance(manifest, list):
        if not manifest:
            report.error(f"{prefix}: mathematical_payload_manifest should not be empty")
        for index, payload in enumerate(manifest, start=1):
            if not isinstance(payload, dict):
                report.error(
                    f"{prefix}: mathematical_payload_manifest[{index}] should be a map"
                )
                continue
            for field_name in MATHEMATICAL_PAYLOAD_MANIFEST_REQUIRED_FIELDS:
                if not str(payload.get(field_name, "")).strip():
                    report.error(
                        f"{prefix}: mathematical_payload_manifest[{index}]."
                        f"{field_name} is empty"
                    )
            payload_type = str(payload.get("payload_type", "")).strip()
            if payload_type and payload_type not in MATHEMATICAL_PAYLOAD_MANIFEST_TYPES:
                report.error(
                    f"{prefix}: mathematical_payload_manifest[{index}].payload_type "
                    f"is not allowed: {payload_type}"
                )
    elif "mathematical_payload_manifest" in completion:
        report.error(f"{prefix}: mathematical_payload_manifest should be a list")

    obstruction_required = status in {"precise_obstruction_found", "route_frozen"}
    obstruction = completion.get("obstruction_record")
    if obstruction_required and not isinstance(obstruction, dict):
        report.error(f"{prefix}: obstruction status requires obstruction_record")
    if isinstance(obstruction, dict) and (obstruction_required or bool_value(obstruction.get("present"))):
        if obstruction_required and not bool_value(obstruction.get("present")):
            report.error(f"{prefix}: obstruction_record.present must be true for obstruction status")
        for field_name in ("scope", "failed_object", "exact_failure", "consequence", "forbidden_overread"):
            if not str(obstruction.get(field_name, "")).strip():
                report.error(f"{prefix}: obstruction_record.{field_name} is required")
        scope = str(obstruction.get("scope", "")).strip()
        if scope and scope not in OBSTRUCTION_RECORD_SCOPES:
            report.error(f"{prefix}: obstruction_record.scope is not allowed: {scope}")
        current_implication = str(obstruction.get("current_ontology_implication", "")).strip()
        if current_implication and current_implication not in OBSTRUCTION_CURRENT_ONTOLOGY_IMPLICATIONS:
            report.error(
                f"{prefix}: obstruction_record.current_ontology_implication is not allowed: "
                f"{current_implication}"
            )
        source_implication = str(obstruction.get("source_extension_implication", "")).strip()
        if source_implication and source_implication not in OBSTRUCTION_SOURCE_EXTENSION_IMPLICATIONS:
            report.error(
                f"{prefix}: obstruction_record.source_extension_implication is not allowed: "
                f"{source_implication}"
            )
        consequence = str(obstruction.get("consequence", "")).strip()
        if consequence and consequence not in OBSTRUCTION_CONSEQUENCES:
            report.error(f"{prefix}: obstruction_record.consequence is not allowed: {consequence}")

    loop_risk = completion.get("loop_risk_decision")
    loop_category = ""
    if isinstance(loop_risk, dict):
        loop_category = str(loop_risk.get("category", "")).strip()
    freeze_required = obstruction_required or loop_category in {
        "scoped_obstruction",
        "repeated_unmet_burdens_no_new_payload",
    }
    route_cycle = completion.get("route_cycle_control")
    if freeze_required and not isinstance(route_cycle, dict):
        report.error(f"{prefix}: repeated-burden or obstruction completion requires route_cycle_control")
    if isinstance(route_cycle, dict) and (
        freeze_required or text_blob(route_cycle).strip()
    ):
        for field_name in (
            "cycle_family",
            "current_cycle_step",
            "cycle_risk",
            "orbit_avoidance_reason",
            "next_role_consequence",
        ):
            if not str(route_cycle.get(field_name, "")).strip():
                report.error(f"{prefix}: route_cycle_control.{field_name} is required")
        if not _substantive_list(route_cycle.get("prior_related_tasks", [])):
            report.error(f"{prefix}: route_cycle_control.prior_related_tasks must list prior tasks")

    freeze = completion.get("freeze_criteria_status")
    if freeze_required and not isinstance(freeze, dict):
        report.error(f"{prefix}: scoped obstruction or route freeze requires freeze_criteria_status")
    if isinstance(freeze, dict) and freeze_required:
        freeze_decision = str(freeze.get("freeze_decision", "")).strip()
        if not freeze_decision:
            report.error(f"{prefix}: freeze_criteria_status.freeze_decision is required")
        elif freeze_decision not in MATHEMATICAL_DECISIVENESS_FREEZE_DECISIONS:
            report.error(
                f"{prefix}: freeze_criteria_status.freeze_decision is not allowed: "
                f"{freeze_decision}"
            )
        if not (
            str(freeze.get("decision_reason", "")).strip()
            or str(freeze.get("rationale", "")).strip()
        ):
            report.error(f"{prefix}: freeze_criteria_status requires decision_reason or rationale")
        freeze_label = str(
            freeze.get("active_freeze_label")
            or freeze.get("candidate_freeze_label")
            or ""
        ).strip()
        if not freeze_label:
            report.error(f"{prefix}: freeze_criteria_status.active_freeze_label is required")
        if bool_value(freeze.get("repeated_burden")) and not _substantive_list(
            freeze.get("prior_attempts_considered", [])
        ):
            report.error(
                f"{prefix}: freeze_criteria_status.prior_attempts_considered must list prior tasks"
            )
        if bool_value(freeze.get("freeze_evaluation_required")):
            if not (
                _substantive_list(freeze.get("freeze_if", []))
                or _substantive_list(freeze.get("criteria_evaluated", []))
            ):
                report.error(f"{prefix}: freeze_criteria_status must list freeze_if criteria")
            if freeze_decision == "not_frozen" and not _substantive_list(
                freeze.get("do_not_freeze_if", [])
            ):
                report.error(
                    f"{prefix}: freeze_criteria_status.do_not_freeze_if is required "
                    "when not frozen"
                )
        next_allowed_route = str(freeze.get("next_allowed_route", "")).strip()
        if not next_allowed_route:
            report.error(f"{prefix}: freeze_criteria_status.next_allowed_route is required")
        elif next_allowed_route not in MATHEMATICAL_DECISIVENESS_NEXT_ALLOWED_ROUTES:
            report.error(
                f"{prefix}: freeze_criteria_status.next_allowed_route is not allowed: "
                f"{next_allowed_route}"
            )
        if next_allowed_route == "none" and freeze_decision not in {
            "locally_frozen",
            "freeze_review_required",
            "human_gate_required",
        }:
            report.error(
                f"{prefix}: freeze_criteria_status.next_allowed_route none requires "
                "local freeze, freeze review, or human gate"
            )
        if freeze_decision == "locally_frozen" and not (
            str(freeze.get("status_update_path", "")).strip()
            or str(freeze.get("ledger_or_registry_update_path", "")).strip()
            or str(freeze.get("no_status_update_rationale", "")).strip()
        ):
            report.error(
                f"{prefix}: locally_frozen requires status update path or "
                "no_status_update_rationale"
            )

    if job_row.get("role_id", "") in CANDIDATE_CONSTRUCTOR_ROLE_IDS:
        result = completion.get("candidate_constructor_result")
        if not isinstance(result, dict):
            report.error(f"{prefix}: Candidate Constructor completion requires candidate_constructor_result")
        else:
            result_type = str(result.get("result_type", "")).strip()
            if not result_type:
                report.error(f"{prefix}: candidate_constructor_result.result_type is required")
            elif result_type not in CANDIDATE_CONSTRUCTOR_RESULT_TYPES:
                report.error(
                    f"{prefix}: candidate_constructor_result.result_type is not allowed: "
                    f"{result_type}"
                )
            no_fog_explanation = str(result.get("no_fog_explanation", "")).strip()
            if not bool_value(result.get("no_fog_check")):
                report.error(f"{prefix}: candidate_constructor_result.no_fog_check must be true")
            if not no_fog_explanation:
                report.error(f"{prefix}: candidate_constructor_result.no_fog_explanation is empty")
            else:
                lowered_no_fog = no_fog_explanation.lower()
                for phrase in CANDIDATE_CONSTRUCTOR_FOG_ONLY_PHRASES:
                    if phrase in lowered_no_fog:
                        report.error(
                            f"{prefix}: candidate_constructor_result.no_fog_explanation "
                            f"contains fog-only phrase: {phrase}"
                        )
            next_required_role = str(result.get("next_required_role", "")).strip()
            if not next_required_role:
                report.error(f"{prefix}: candidate_constructor_result.next_required_role is required")
            elif next_required_role not in CANDIDATE_CONSTRUCTOR_NEXT_REQUIRED_ROLES:
                report.error(
                    f"{prefix}: candidate_constructor_result.next_required_role is not allowed: "
                    f"{next_required_role}"
                )
            if result_type == "constructed_candidate":
                if not str(result.get("constructed_candidate_path", "")).strip():
                    report.error(
                        f"{prefix}: candidate_constructor_result.constructed_candidate_path "
                        "is required for constructed_candidate"
                    )
                for list_field in ("formal_objects", "maps", "proof_obligations"):
                    if not _substantive_list(result.get(list_field, [])):
                        report.error(
                            f"{prefix}: candidate_constructor_result.{list_field} "
                            "must list concrete entries for constructed_candidate"
                        )
            if result_type == "minimal_countermodel":
                if not str(result.get("minimal_countermodel_path", "")).strip():
                    report.error(
                        f"{prefix}: candidate_constructor_result.minimal_countermodel_path "
                        "is required for minimal_countermodel"
                    )
                if not _substantive_list(result.get("failed_components", [])):
                    report.error(
                        f"{prefix}: candidate_constructor_result.failed_components "
                        "must list concrete entries for minimal_countermodel"
                    )
            if result_type == "precise_obstruction":
                if not str(result.get("obstruction_id", "")).strip():
                    report.error(
                        f"{prefix}: candidate_constructor_result.obstruction_id "
                        "is required for precise_obstruction"
                    )
                if not _substantive_list(result.get("failed_components", [])):
                    report.error(
                        f"{prefix}: candidate_constructor_result.failed_components "
                        "must list concrete entries for precise_obstruction"
                    )
                if not (isinstance(obstruction, dict) and bool_value(obstruction.get("present"))):
                    report.error(
                        f"{prefix}: candidate_constructor_result.precise_obstruction "
                        "requires present obstruction_record"
                    )
            if result_type == "invalid_under_claim_boundary":
                if not _substantive_list(result.get("failed_components", [])):
                    report.error(
                        f"{prefix}: candidate_constructor_result.failed_components "
                        "must list concrete entries for invalid_under_claim_boundary"
                    )
                if not str(result.get("claim_boundary_citation", "")).strip():
                    report.error(
                        f"{prefix}: candidate_constructor_result.claim_boundary_citation "
                        "is required for invalid_under_claim_boundary"
                    )
            if not bool_value(result.get("claim_boundary_preserved")):
                report.error(
                    f"{prefix}: candidate_constructor_result.claim_boundary_preserved must be true"
                )

    forbidden = completion.get("forbidden_conclusion_summary")
    if isinstance(forbidden, dict):
        if bool_value(forbidden.get("physics_promotion_authorized")) and not promotion_authorized:
            report.error(
                f"{prefix}: forbidden_conclusion_summary authorizes physics promotion "
                f"without physics_progress_status authority"
            )
        if not str(forbidden.get("summary", "")).strip():
            report.error(f"{prefix}: forbidden_conclusion_summary.summary is empty")
        forbidden_text = text_blob(
            forbidden.get("forbidden_conclusions", []),
            forbidden.get("summary", ""),
        ).lower()
        for marker in (
            "m_src adoption",
            "g_eff",
            "matter coupling",
            "einstein",
            "benchmark",
            "completed derivation",
            "global theory rejection",
        ):
            if marker not in forbidden_text:
                report.error(
                    f"{prefix}: forbidden_conclusion_summary must preserve {marker} block"
                )
    elif "forbidden_conclusion_summary" in completion:
        report.error(f"{prefix}: forbidden_conclusion_summary should be a map")


def ontology_law_receipt_required(
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
) -> bool:
    if isinstance(completion.get("ontology_law_research_packet"), dict):
        return True
    role_id = job_row.get("role_id", "")
    if role_id not in PHYSICS_ROLE_IDS:
        return False
    decision = completion.get("theoretical_decision_output", {})
    if isinstance(decision, dict):
        packet_type = str(decision.get("selected_next_packet_type", "")).strip()
        if packet_type == ONTOLOGY_LAW_SELECTOR_PACKET:
            return True
    blob = text_blob(job_contract, completion)
    return ONTOLOGY_LAW_ROUTE_LABEL in blob


def validate_ontology_law_research_packet(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path: Path,
) -> None:
    if not ontology_law_receipt_required(job_row, job_contract, completion):
        return

    path_text = path.relative_to(REPO_ROOT).as_posix()
    receipt = completion.get("ontology_law_research_packet")
    if not isinstance(receipt, dict):
        report.error(f"{path_text}: ontology-law route completion missing ontology_law_research_packet receipt")
        return

    route = _string_field(receipt, "route")
    trigger = _string_field(receipt, "trigger_classification")
    target_milestone = _string_field(receipt, "target_derivation_milestone")
    milestone_burden = _string_field(receipt, "milestone_burden")
    missing_law = _string_field(receipt, "missing_source_law")
    underdetermination = _string_field(receipt, "underdetermination_statement")
    no_go_status = _string_field(receipt, "no_go_theorem_status")
    payload_mode = _string_field(receipt, "packet_payload_mode")

    if route != ONTOLOGY_LAW_ROUTE_LABEL:
        report.error(f"{path_text}: ontology_law_research_packet.route must be {ONTOLOGY_LAW_ROUTE_LABEL}")
    if trigger != ONTOLOGY_LAW_TRIGGER_CLASSIFICATION:
        report.error(
            f"{path_text}: ontology_law_research_packet.trigger_classification must be "
            f"{ONTOLOGY_LAW_TRIGGER_CLASSIFICATION}"
        )
    if trigger in ONTOLOGY_LAW_NON_TRIGGERS:
        report.error(f"{path_text}: ordinary gaps and workflow inconvenience may not use ontology-law route")
    if not target_milestone:
        report.error(f"{path_text}: ontology_law_research_packet.target_derivation_milestone is required")
    elif target_milestone not in GR_DERIVATION_MILESTONES:
        report.error(
            f"{path_text}: ontology_law_research_packet.target_derivation_milestone is not registered: "
            f"{target_milestone}"
        )
    if not milestone_burden:
        report.error(f"{path_text}: ontology_law_research_packet.milestone_burden is required")
    if not missing_law:
        report.error(f"{path_text}: ontology_law_research_packet.missing_source_law is required")

    lowered_statement = underdetermination.lower()
    if "current ontology" not in lowered_statement or "does not derive" not in lowered_statement:
        report.error(
            f"{path_text}: ontology_law_research_packet.underdetermination_statement must state "
            "that current ontology does not derive the missing source law"
        )
    impossibility_markers = ["therefore", "impossible", "cannot exist", "no possible"]
    if any(marker in lowered_statement for marker in impossibility_markers) and not _is_no_go_present(no_go_status):
        report.error(
            f"{path_text}: ontology_law_research_packet.underdetermination_statement may not assert "
            "impossibility without a no-go theorem or scoped obstruction"
        )

    adoption_status = receipt.get("adoption_status")
    if not isinstance(adoption_status, dict):
        report.error(f"{path_text}: ontology_law_research_packet.adoption_status must be a map")
    else:
        current_adoption = _string_field(adoption_status, "current_adoption")
        continuation = _string_field(adoption_status, "continuation")
        status_pair = _string_field(adoption_status, "status_pair")
        if current_adoption != "blocked":
            report.error(f"{path_text}: ontology_law_research_packet.adoption_status.current_adoption must be blocked")
        if continuation != "open":
            report.error(f"{path_text}: ontology_law_research_packet.adoption_status.continuation must be open")
        if status_pair != ONTOLOGY_LAW_STATUS_PAIR:
            report.error(
                f"{path_text}: ontology_law_research_packet.adoption_status.status_pair must be "
                f"{ONTOLOGY_LAW_STATUS_PAIR}"
            )

    if payload_mode not in ONTOLOGY_LAW_PAYLOAD_MODES:
        report.error(
            f"{path_text}: ontology_law_research_packet.packet_payload_mode is not allowed: {payload_mode}"
        )
    else:
        validate_ontology_law_payload_mode(report, receipt, payload_mode, path_text)

    validate_ontology_law_status_label(report, receipt, path_text)
    validate_ontology_law_recovery_obligations(report, receipt, path_text)
    validate_ontology_law_no_target_scope(report, receipt, path_text)
    validate_ontology_law_human_gate(report, receipt, path_text)


def validate_ontology_law_payload_mode(
    report: ValidationReport,
    receipt: dict[str, Any],
    payload_mode: str,
    path_text: str,
) -> None:
    if payload_mode == "candidate_law_payload":
        payload = receipt.get("candidate_law_payload")
        if not isinstance(payload, dict):
            report.error(f"{path_text}: ontology_law_research_packet.candidate_law_payload must be a map")
            return
        if not _string_field(payload, "source_side_definition"):
            report.error(
                f"{path_text}: ontology_law_research_packet.candidate_law_payload.source_side_definition is required"
            )
        for field_name in ["formal_objects", "domains", "maps", "proof_obligations"]:
            if not _substantive_list(payload.get(field_name)):
                report.error(
                    f"{path_text}: ontology_law_research_packet.candidate_law_payload.{field_name} "
                    "must be nonempty"
                )
    elif payload_mode == "candidate_law_comparison":
        comparison = receipt.get("candidate_law_comparison")
        if not isinstance(comparison, dict):
            report.error(f"{path_text}: ontology_law_research_packet.candidate_law_comparison must be a map")
            return
        for field_name in ["candidates", "comparison_basis"]:
            if not _substantive_list(comparison.get(field_name)):
                report.error(
                    f"{path_text}: ontology_law_research_packet.candidate_law_comparison.{field_name} "
                    "must be nonempty"
                )
        if not _string_field(comparison, "selection_status"):
            report.error(
                f"{path_text}: ontology_law_research_packet.candidate_law_comparison.selection_status is required"
            )
    elif payload_mode == "candidate_law_refutation":
        refutation = receipt.get("candidate_law_refutation")
        if not isinstance(refutation, dict):
            report.error(f"{path_text}: ontology_law_research_packet.candidate_law_refutation must be a map")
            return
        for field_name in ["refuted_candidate", "refutation_basis"]:
            if not _string_field(refutation, field_name):
                report.error(
                    f"{path_text}: ontology_law_research_packet.candidate_law_refutation.{field_name} is required"
                )
        if not _substantive_list(refutation.get("surviving_obligations")):
            report.error(
                f"{path_text}: ontology_law_research_packet.candidate_law_refutation.surviving_obligations "
                "must be nonempty"
            )
    elif payload_mode == "human_gate_precondition":
        precondition = receipt.get("human_gate_precondition")
        if not isinstance(precondition, dict):
            report.error(f"{path_text}: ontology_law_research_packet.human_gate_precondition must be a map")
            return
        if not bool_value(precondition.get("blocks_payload_definition", False)):
            report.error(
                f"{path_text}: ontology_law_research_packet.human_gate_precondition.blocks_payload_definition "
                "must be true"
            )
        if not _string_field(precondition, "reason"):
            report.error(f"{path_text}: ontology_law_research_packet.human_gate_precondition.reason is required")


def validate_ontology_law_status_label(
    report: ValidationReport,
    receipt: dict[str, Any],
    path_text: str,
) -> None:
    payload = receipt.get("candidate_law_payload")
    if not isinstance(payload, dict):
        return
    status_label = _string_field(payload, "status_label")
    if status_label and status_label not in ONTOLOGY_LAW_STATUS_LABELS:
        report.error(
            f"{path_text}: ontology_law_research_packet.candidate_law_payload.status_label is not allowed: "
            f"{status_label}"
        )
    if status_label in {"canonical-ontology candidate", "adopted"}:
        gate = receipt.get("human_gate_request")
        gate_required = isinstance(gate, dict) and bool_value(gate.get("required_before_adoption", False))
        if not gate_required:
            report.error(
                f"{path_text}: ontology-law candidate or adopted labels must remain blocked pending human gate"
            )
    if status_label == "adopted":
        report.error(f"{path_text}: ontology_law_research_packet may not mark candidate law as adopted")


def validate_ontology_law_recovery_obligations(
    report: ValidationReport,
    receipt: dict[str, Any],
    path_text: str,
) -> None:
    obligations = receipt.get("exact_gr_recovery_obligations")
    if not isinstance(obligations, dict):
        report.error(f"{path_text}: ontology_law_research_packet.exact_gr_recovery_obligations must be a map")
        return
    if not _substantive_list(obligations.get("checklist")):
        report.error(
            f"{path_text}: ontology_law_research_packet.exact_gr_recovery_obligations.checklist "
            "must be nonempty"
        )
    if not _substantive_list(obligations.get("distance_to_gr_links")):
        report.error(
            f"{path_text}: ontology_law_research_packet.exact_gr_recovery_obligations.distance_to_gr_links "
            "must be nonempty"
        )


def validate_ontology_law_no_target_scope(
    report: ValidationReport,
    receipt: dict[str, Any],
    path_text: str,
) -> None:
    scope = receipt.get("no_target_import_audit_scope")
    if not isinstance(scope, dict):
        report.error(f"{path_text}: ontology_law_research_packet.no_target_import_audit_scope must be a map")
        return
    classes = set(_substantive_list(scope.get("forbidden_source_classes")))
    missing = sorted(ONTOLOGY_LAW_REQUIRED_FORBIDDEN_SOURCE_CLASSES - classes)
    if missing:
        report.error(
            f"{path_text}: ontology_law_research_packet.no_target_import_audit_scope missing "
            f"forbidden_source_classes {missing}"
        )

    payload = receipt.get("candidate_law_payload")
    if isinstance(payload, dict):
        definition = _string_field(payload, "source_side_definition").lower()
        if any(marker in definition for marker in ONTOLOGY_LAW_TARGET_IMPORT_MARKERS):
            report.error(
                f"{path_text}: ontology_law_research_packet.candidate_law_payload.source_side_definition "
                "must not define the source law from target-GR imports"
            )


def validate_ontology_law_human_gate(
    report: ValidationReport,
    receipt: dict[str, Any],
    path_text: str,
) -> None:
    gate = receipt.get("human_gate_request")
    if not isinstance(gate, dict):
        report.error(f"{path_text}: ontology_law_research_packet.human_gate_request must be a map")
        return
    if not bool_value(gate.get("required_before_adoption", False)):
        report.error(
            f"{path_text}: ontology_law_research_packet.human_gate_request.required_before_adoption must be true"
        )
    if not _string_field(gate, "requested_decision"):
        report.error(f"{path_text}: ontology_law_research_packet.human_gate_request.requested_decision is required")


def validate_distance_to_gr_status(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
    required_burdens: tuple[str, ...],
) -> None:
    matrix = completion.get("distance_to_gr_status")
    if not isinstance(matrix, list) or not matrix:
        report.error(f"{path_text}: future physics completion missing distance_to_gr_status matrix")
        return

    seen: dict[str, str] = {}
    for item in matrix:
        if not isinstance(item, dict):
            report.error(f"{path_text}: distance_to_gr_status entries must be maps")
            continue
        burden = str(item.get("burden", "")).strip()
        status = str(item.get("status", "")).strip()
        if not burden or not status:
            report.error(f"{path_text}: distance_to_gr_status entries require burden and status")
            continue
        seen[burden] = status
    missing = [burden for burden in required_burdens if burden not in seen]
    if missing:
        report.error(f"{path_text}: distance_to_gr_status missing burdens {missing}")


def _completion_physics_promotion_authorized(completion: dict[str, Any]) -> bool:
    if bool_value(completion.get("physics_promotion_authorized")):
        return True
    progress = completion.get("physics_progress_status")
    if isinstance(progress, dict) and bool_value(progress.get("physics_promotion_authorized")):
        return True
    layers = completion.get("authorization_layers")
    if isinstance(layers, dict) and bool_value(layers.get("downstream_physics_promotion_authorized")):
        return True
    return False


def validate_distance_to_gr_delta_effect(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    if not distance_to_gr_delta_effect_policy_active(job_row, completion):
        return

    delta = completion.get("distance_to_gr_delta")
    if not isinstance(delta, dict):
        report.error(f"{path_text}: future physics completion missing distance_to_gr_delta.effect")
        return

    effect = str(delta.get("effect", "")).strip()
    if not effect:
        report.error(f"{path_text}: future physics completion missing distance_to_gr_delta.effect")
    elif effect not in DISTANCE_TO_GR_DELTA_EFFECT_VALUES:
        report.error(f"{path_text}: distance_to_gr_delta.effect is not allowed: {effect}")

    downstream_unlocked = delta.get("downstream_unlocked", [])
    if not isinstance(downstream_unlocked, list):
        return
    promotion_authorized = _completion_physics_promotion_authorized(completion)
    for item in downstream_unlocked:
        unlocked = str(item).strip().lower().replace("-", "_")
        if unlocked in UNAUTHORIZED_DOWNSTREAM_GR_UNLOCKS and not promotion_authorized:
            report.error(
                f"{path_text}: distance_to_gr_delta.effect does not authorize "
                f"downstream_unlocked {item} without human-gated physics promotion authority"
            )


def validate_general_physics_payload(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    payloads = completion.get("new_mathematical_payload")
    if not isinstance(payloads, list) or not payloads:
        report.error(f"{path_text}: future physics completion missing new_mathematical_payload")
        return
    accepted = False
    for item in payloads:
        if not isinstance(item, dict):
            report.error(f"{path_text}: new_mathematical_payload entries must be maps")
            continue
        payload_type = str(item.get("payload_type", item.get("type", ""))).strip()
        summary = str(item.get("summary", "")).strip()
        if payload_type not in GENERAL_PHYSICS_PAYLOAD_TYPES:
            report.error(f"{path_text}: unsupported new_mathematical_payload type {payload_type}")
        elif summary:
            accepted = True
        else:
            report.error(f"{path_text}: new_mathematical_payload entries require summary")
    if not accepted:
        report.error(f"{path_text}: future physics completion has no accepted new mathematical payload")


def validate_refuter_loop_decision(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    decision = completion.get("loop_risk_decision")
    if not isinstance(decision, dict):
        report.error(f"{path_text}: Refuter stress completion missing loop_risk_decision")
        return
    category = str(decision.get("category", "")).strip()
    next_route = str(decision.get("next_route", "")).strip()
    rationale = str(decision.get("rationale", "")).strip()
    if category not in LOOP_RISK_DECISION_CATEGORIES:
        report.error(f"{path_text}: loop_risk_decision.category is not registered: {category}")
    future_pause_policy = theoretical_continuation_policy_active(job_row, completion)
    allowed_bridge_routes = set(BRIDGE_OR_FAIL_ROUTES)
    if not future_pause_policy:
        allowed_bridge_routes |= LEGACY_BRIDGE_OR_FAIL_ROUTES
    allowed_routes = allowed_bridge_routes | LOOP_RISK_SUCCESS_ROUTES
    if next_route not in allowed_routes:
        report.error(f"{path_text}: loop_risk_decision.next_route is not allowed: {next_route}")
    if not rationale:
        report.error(f"{path_text}: loop_risk_decision.rationale is required")
    if future_pause_policy and next_route in LEGACY_BRIDGE_OR_FAIL_ROUTES:
        report.error(
            f"{path_text}: future physics routing may not use generic controlled_pause; "
            "use theoretical_decision_role_selection or human_gated_ontology_change_required"
        )
    next_text = text_blob(completion.get("next_recommendation", ""), decision)
    if next_route == "human_gated_ontology_change_required":
        if "ontology" not in next_text or not any(marker in next_text for marker in ("human", "gate")):
            report.error(
                f"{path_text}: human_gated_ontology_change_required requires ontology and human-gate rationale"
            )
    if next_route == "theoretical_decision_role_selection" and not any(
        marker in next_text for marker in THEORETICAL_DECISION_TEXT_MARKERS
    ):
        report.error(
            f"{path_text}: theoretical_decision_role_selection requires a concrete theoretical payload marker"
        )

    if category == "repeated_unmet_burdens_no_new_payload":
        burdens = _listish_values(decision.get("repeated_burdens", []))
        if not burdens:
            report.error(f"{path_text}: repeated burden decisions must list repeated_burdens")
    if category == "scoped_obstruction" and not str(decision.get("obstruction_summary", "")).strip():
        report.error(f"{path_text}: scoped_obstruction decisions require obstruction_summary")
    if category in {"repeated_unmet_burdens_no_new_payload", "scoped_obstruction"}:
        if gr_derivation_roadmap_policy_active(job_row, completion):
            validate_freeze_criteria_status(report, completion, path_text)
        if next_route not in allowed_bridge_routes:
            report.error(
                f"{path_text}: {category} must route through bridge_or_fail escalation"
            )
        if (
            "ontology formalizer" in next_text
            and any(marker in next_text for marker in ("obligation packet", "generic repair", "repair packet"))
            and not any(marker in next_text for marker in ONTOLOGY_PAYLOAD_TEXT_MARKERS)
        ):
            report.error(
                f"{path_text}: bridge_or_fail escalation may not route to a generic Ontology Formalizer packet"
            )


def validate_freeze_criteria_status(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    freeze = completion.get("freeze_criteria_status")
    if not isinstance(freeze, dict):
        report.error(f"{path_text}: repeated-burden or scoped-obstruction completion missing freeze_criteria_status")
        return
    decision = str(freeze.get("freeze_decision", "")).strip()
    rationale = str(freeze.get("rationale", "")).strip()
    criteria = freeze.get("criteria_evaluated", [])
    label = str(freeze.get("candidate_freeze_label", "")).strip()
    if decision not in FREEZE_DECISION_VALUES:
        report.error(f"{path_text}: freeze_criteria_status.freeze_decision is not allowed: {decision}")
    if not isinstance(criteria, list) or not any(str(item).strip() for item in criteria):
        report.error(f"{path_text}: freeze_criteria_status.criteria_evaluated must list evaluated criteria")
    if not rationale:
        report.error(f"{path_text}: freeze_criteria_status.rationale is required")
    if decision == "freeze_route" and not label:
        report.error(f"{path_text}: freeze route decisions require candidate_freeze_label")


def validate_ontology_formalizer_payload(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    payloads = completion.get("new_mathematical_payload")
    if not isinstance(payloads, list) or not payloads:
        report.error(f"{path_text}: Ontology Formalizer completion missing new_mathematical_payload")
        return
    accepted = False
    for item in payloads:
        if not isinstance(item, dict):
            report.error(f"{path_text}: new_mathematical_payload entries must be maps")
            continue
        payload_type = str(item.get("payload_type", item.get("type", ""))).strip()
        summary = str(item.get("summary", "")).strip()
        if payload_type not in ONTOLOGY_FORMALIZER_PAYLOAD_TYPES:
            report.error(f"{path_text}: unsupported new_mathematical_payload type {payload_type}")
        elif summary:
            accepted = True
        else:
            report.error(f"{path_text}: new_mathematical_payload entries require summary")
    if not accepted:
        report.error(f"{path_text}: Ontology Formalizer completion has no accepted new mathematical payload")


def validate_candidate_bridge_attempt(
    report: ValidationReport,
    completion: dict[str, Any],
    path_text: str,
) -> None:
    bridge = completion.get("bridge_attempt_status")
    if not isinstance(bridge, dict):
        report.error(f"{path_text}: Candidate Constructor bridge completion missing bridge_attempt_status")
        return
    candidate_map = str(bridge.get("candidate_map", "")).strip()
    missing_primitive = str(bridge.get("missing_primitive", "")).strip()
    preserves_blocks = str(bridge.get("preserves_blocks", "")).strip()
    if not candidate_map and not missing_primitive:
        report.error(
            f"{path_text}: bridge_attempt_status requires candidate_map or missing_primitive"
        )
    if not preserves_blocks:
        report.error(f"{path_text}: bridge_attempt_status.preserves_blocks is required")


def validate_theoretical_continuation_decision(
    report: ValidationReport,
    job_row: dict[str, str],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    decision = completion.get("theoretical_decision_output")
    if not isinstance(decision, dict):
        report.error(f"{path_text}: theoretical-continuation-selector completion missing theoretical_decision_output")
        return
    packet_type = str(decision.get("selected_next_packet_type", "")).strip()
    basis = str(decision.get("decision_basis", "")).strip()
    method = str(decision.get("theoretical_method", "")).strip()
    preserves_blocks = str(decision.get("preserves_claim_blocks", "")).strip()
    requires_human_gate = bool_value(decision.get("requires_human_gate", False))
    human_gate_reason = str(decision.get("human_gate_reason", "")).strip()

    if packet_type not in THEORETICAL_DECISION_PACKET_TYPES:
        report.error(
            f"{path_text}: theoretical_decision_output.selected_next_packet_type is not allowed: {packet_type}"
        )
    if not basis:
        report.error(f"{path_text}: theoretical_decision_output.decision_basis is required")
    if not method:
        report.error(f"{path_text}: theoretical_decision_output.theoretical_method is required")
    if not preserves_blocks:
        report.error(f"{path_text}: theoretical_decision_output.preserves_claim_blocks is required")
    if packet_type == "human_gated_ontology_change_required":
        gate_text = text_blob(decision)
        if not requires_human_gate:
            report.error(
                f"{path_text}: human-gated ontology decision must set requires_human_gate true"
            )
        if "ontology" not in gate_text or not any(marker in gate_text for marker in ("human", "gate")):
            report.error(
                f"{path_text}: human-gated ontology decision requires ontology and human-gate rationale"
            )
        if not human_gate_reason:
            report.error(
                f"{path_text}: human-gated ontology decision requires human_gate_reason"
            )
    elif requires_human_gate:
        report.error(
            f"{path_text}: theoretical continuation decisions may require a human gate only for ontology-change authority"
        )
    if not gr_derivation_roadmap_policy_active(job_row, completion):
        return
    if packet_type == "distinct_scoped_no_go_question":
        if not str(decision.get("decision_consequence", "")).strip():
            report.error(
                f"{path_text}: distinct_scoped_no_go_question requires decision_consequence after roadmap activation"
            )
        if not str(decision.get("new_payload_novelty", "")).strip():
            report.error(
                f"{path_text}: distinct_scoped_no_go_question requires new_payload_novelty after roadmap activation"
            )
    if packet_type.startswith("source_extension_"):
        category = str(decision.get("source_extension_category", "")).strip()
        classification = str(decision.get("source_extension_import_classification", "")).strip()
        if category not in SOURCE_EXTENSION_WORKFLOW_CATEGORIES:
            report.error(
                f"{path_text}: source extension decisions require source_extension_category from "
                f"{sorted(SOURCE_EXTENSION_WORKFLOW_CATEGORIES)}"
            )
        if not classification:
            report.error(
                f"{path_text}: source extension decisions require source_extension_import_classification"
            )
    if packet_type == "finite_toy_metric_response_model":
        target = decision.get("finite_toy_model_target")
        if not isinstance(target, dict):
            report.error(f"{path_text}: finite toy model decisions require finite_toy_model_target")
        else:
            for field_name in [
                "source_set",
                "response_relation",
                "metric_response_analogue",
                "invariance_checks",
            ]:
                if not str(target.get(field_name, "")).strip():
                    report.error(
                        f"{path_text}: finite_toy_model_target.{field_name} is required"
                    )


def source_extension_classification_policy_active(
    job_row: dict[str, str],
    completion: dict[str, Any] | None = None,
) -> bool:
    timestamps = [
        job_row.get("created_at", ""),
        job_row.get("started_at", ""),
        job_row.get("completed_at", ""),
    ]
    if completion:
        timestamps.append(completion.get("completed_at", ""))
    return any(
        timestamp_at_or_after(value, SOURCE_EXTENSION_CLASSIFICATION_REQUIRED_AFTER)
        for value in timestamps
    )


def _source_extension_route_marker(value: Any) -> bool:
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    return text.startswith("source_extension_") or "source_extension" in text


def source_extension_classification_required(
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
) -> bool:
    if not source_extension_classification_policy_active(job_row, completion):
        return False
    if bool_value(job_contract.get("source_extension_classification_required")):
        return True
    if bool_value(completion.get("source_extension_classification_required")):
        return True
    if job_row.get("role_id", "") not in SOURCE_EXTENSION_CLASSIFICATION_ROLE_IDS:
        return False
    for field_name in ["route_label", "plan_task_id", "task_type"]:
        if _source_extension_route_marker(job_contract.get(field_name)):
            return True
    decision = completion.get("theoretical_decision_output")
    if isinstance(decision, dict):
        packet_type = str(decision.get("selected_next_packet_type", "")).strip()
        category = str(decision.get("source_extension_category", "")).strip()
        if packet_type.startswith("source_extension_") or category in SOURCE_EXTENSION_WORKFLOW_CATEGORIES:
            return True
    payloads = completion.get("new_mathematical_payload", [])
    if isinstance(payloads, list):
        for item in payloads:
            if isinstance(item, dict):
                payload_type = str(item.get("payload_type", item.get("type", ""))).strip()
                if payload_type == "source_extension_classification":
                    return True
    return False


def _source_extension_classification_records(receipt: Any) -> list[dict[str, Any]]:
    if isinstance(receipt, list):
        return [item for item in receipt if isinstance(item, dict)]
    if not isinstance(receipt, dict):
        return []
    if isinstance(receipt.get("records"), list):
        return [item for item in receipt["records"] if isinstance(item, dict)]
    if isinstance(receipt.get("classifications"), list):
        return [item for item in receipt["classifications"] if isinstance(item, dict)]
    if "classification" in receipt:
        return [receipt]
    return []


def validate_source_extension_classification_receipt(
    report: ValidationReport,
    job_row: dict[str, str],
    job_contract: dict[str, Any],
    completion: dict[str, Any],
    path_text: str,
) -> None:
    receipt = completion.get("source_extension_classification")
    required = source_extension_classification_required(job_row, job_contract, completion)
    if receipt is None:
        if required:
            report.error(f"{path_text}: source-extension completion missing source_extension_classification receipt")
        return
    if not source_extension_classification_policy_active(job_row, completion):
        return
    records = _source_extension_classification_records(receipt)
    if not records:
        report.error(f"{path_text}: source_extension_classification must contain at least one classification record")
        return
    if isinstance(receipt, dict):
        checklist_id = str(receipt.get("checklist_id", "")).strip()
        if checklist_id and checklist_id != SOURCE_EXTENSION_CLASSIFICATION_CHECKLIST_ID:
            report.error(
                f"{path_text}: source_extension_classification.checklist_id must be "
                f"{SOURCE_EXTENSION_CLASSIFICATION_CHECKLIST_ID}"
            )
    for index, record in enumerate(records, start=1):
        prefix = f"{path_text}: source_extension_classification[{index}]"
        classification = str(record.get("classification", "")).strip()
        if classification not in SOURCE_EXTENSION_CLASSIFICATION_VALUES:
            report.error(
                f"{prefix}.classification is not allowed: {classification}"
            )
        if not (
            str(record.get("claim_boundary_id", "")).strip()
            or str(record.get("claim_boundary_ref", "")).strip()
            or isinstance(record.get("claim_boundary"), dict)
        ):
            report.error(
                f"{prefix} requires claim_boundary, claim_boundary_id, or claim_boundary_ref"
            )
        blocked = _listish_values(record.get("blocked_overreads", record.get("forbidden_overreads", [])))
        if not blocked:
            report.error(f"{prefix} requires blocked_overreads or forbidden_overreads")
        relation = str(record.get("relation_to_current_ontology", "")).strip()
        if relation not in SOURCE_EXTENSION_ONTOLOGY_RELATION_VALUES:
            report.error(
                f"{prefix}.relation_to_current_ontology is not allowed: {relation}"
            )
        if "protected_authority_required" not in record:
            report.error(f"{prefix}.protected_authority_required is required")
        if "downstream_promotion_authorized" not in record:
            report.error(f"{prefix}.downstream_promotion_authorized is required")
        elif bool_value(record.get("downstream_promotion_authorized")):
            report.error(f"{prefix}.downstream_promotion_authorized must be false")
        if "physics_promotion_authorized" in record and bool_value(record.get("physics_promotion_authorized")):
            report.error(f"{prefix}.physics_promotion_authorized must be false")


def validate_completion_resolver_snapshots(
    report: ValidationReport,
    completion: dict[str, Any],
    job_contract: dict[str, Any],
    path: Path,
) -> None:
    if not bool_value(job_contract.get("resolves_signal_routing", False)):
        return
    path_text = path.relative_to(REPO_ROOT).as_posix()
    routing_delta_summary = completion.get("routing_delta_summary", "")
    if not isinstance(routing_delta_summary, str) or not routing_delta_summary.strip():
        report.error(f"{path_text}: routing-resolution completion missing routing_delta_summary")
    snapshots = completion.get("resolver_snapshots")
    if not isinstance(snapshots, dict):
        report.error(
            f"{path_text}: routing-resolution completion must declare resolver_snapshots.before and resolver_snapshots.after"
        )
        return
    for key in ["before", "after"]:
        value = snapshots.get(key, "")
        if not isinstance(value, str) or not value.strip():
            report.error(f"{path_text}: routing-resolution completion missing resolver_snapshots.{key}")
            continue
        reason = validate_relative_path(value)
        if reason:
            report.error(f"{path_text}: invalid resolver_snapshots.{key}: {reason}")
            continue
        snapshot_path = repo_path(value)
        if snapshot_path.suffix != ".json":
            report.error(f"{path_text}: resolver_snapshots.{key} must point to a .json file: {value}")
            continue
        if not snapshot_path.exists():
            report.error(f"{path_text}: resolver_snapshots.{key} path does not exist: {value}")
            continue
        validate_resolver_snapshot_json(report, path_text, key, snapshot_path)


def validate_resolver_snapshot_json(
    report: ValidationReport,
    completion_path_text: str,
    key: str,
    snapshot_path: Path,
) -> None:
    try:
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} is not valid JSON: {exc.msg}")
        return
    if not isinstance(data, dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must contain a JSON object")
        return

    for field_name in RESOLVER_SNAPSHOT_REQUIRED_FIELDS:
        if field_name not in data:
            report.error(
                f"{completion_path_text}: resolver_snapshots.{key} missing resolver field {field_name}"
            )
    for field_name in ["status", "boundary", "reason"]:
        if field_name in data and not isinstance(data[field_name], str):
            report.error(
                f"{completion_path_text}: resolver_snapshots.{key} field {field_name} must be a string"
            )
    if data.get("resolver_is_advisory") is not True:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must preserve resolver_is_advisory=true")
    if data.get("hard_checkpoint_gate") is not False:
        report.error(f"{completion_path_text}: resolver_snapshots.{key} must preserve hard_checkpoint_gate=false")
    if data.get("checkpoint_gate_source") != "validators":
        report.error(
            f"{completion_path_text}: resolver_snapshots.{key} must preserve checkpoint_gate_source=validators"
        )
    if "selected_signal" in data and not isinstance(data["selected_signal"], dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} selected_signal must be an object")
    if "open_signals" in data and not isinstance(data["open_signals"], list):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} open_signals must be a list")
    if "change_classification" in data and not isinstance(data["change_classification"], dict):
        report.error(f"{completion_path_text}: resolver_snapshots.{key} change_classification must be an object")


def validate_program_state(report: ValidationReport, tasks: dict[str, dict[str, str]]) -> None:
    path = CONTROL_DIR / "program_state.yaml"
    if not path.exists():
        report.error("missing research_control/program_state.yaml")
        return
    try:
        state = load_yaml(path)
    except StrictYamlError as exc:
        report.error(f"research_control/program_state.yaml: {exc}")
        return
    active_task_id = str(state.get("active_task_id", ""))
    if active_task_id and active_task_id not in tasks:
        report.error("program_state.yaml: active_task_id is not registered")
    if "gr_derived" in state:
        report.error("program_state.yaml: bootstrap must not define gr_derived")


def _normalize_frontier_cell(value: Any) -> str:
    text = str(value or "").strip()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _frontier_table_rows(text: str, heading: str) -> list[list[str]]:
    heading_line = f"## {heading}"
    lines = text.splitlines()
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == heading_line)
    except StopIteration:
        return []
    rows: list[list[str]] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            if rows and stripped:
                break
            continue
        cells = [_normalize_frontier_cell(cell) for cell in stripped.strip("|").split("|")]
        if not cells or all(set(cell) <= {"-"} for cell in cells if cell):
            continue
        rows.append(cells)
    return rows


def current_frontier_active_state(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for row in _frontier_table_rows(text, "Active Research State"):
        if len(row) < 2 or row[0] == "Field":
            continue
        key = CURRENT_FRONTIER_ACTIVE_FIELD_MAP.get(row[0])
        if key:
            fields[key] = row[1]
    return fields


def current_frontier_active_state_bifurcation(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for row in _frontier_table_rows(text, "Active-State Bifurcation"):
        if len(row) < 2 or row[0] == "Field":
            continue
        key = CURRENT_FRONTIER_BIFURCATION_FIELD_MAP.get(row[0])
        if key:
            fields[key] = row[1]
    return fields


def current_frontier_distance_rows(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    headers: list[str] = []
    for row in _frontier_table_rows(text, "Distance-To-GR Table"):
        if row and row[0] == "Burden ID":
            headers = row
            continue
        if not headers or len(row) < len(headers):
            continue
        record = dict(zip(headers, row))
        burden_id = record.get("Burden ID", "")
        if burden_id:
            rows[burden_id] = record
    return rows


def _current_frontier_drift_error(
    report: ValidationReport,
    field_name: str,
    authoritative_value: Any,
    snapshot_value: Any,
    authoritative_source: str,
) -> None:
    report.error(
        "research_control/current_frontier.md: active-state drift "
        f"field={field_name} "
        f"authoritative_value={_normalize_frontier_cell(authoritative_value)!r} "
        f"snapshot_value={_normalize_frontier_cell(snapshot_value)!r} "
        f"authoritative_source={authoritative_source} "
        f"suggested_repair_route={CURRENT_FRONTIER_REPAIR_ROUTE}"
    )


def _compare_current_frontier_field(
    report: ValidationReport,
    snapshot: dict[str, str],
    field_name: str,
    authoritative_value: Any,
    authoritative_source: str,
) -> None:
    snapshot_value = snapshot.get(field_name, "")
    authoritative_text = _normalize_frontier_cell(authoritative_value)
    snapshot_text = _normalize_frontier_cell(snapshot_value)
    if snapshot_text != authoritative_text:
        _current_frontier_drift_error(
            report,
            field_name,
            authoritative_text,
            snapshot_text,
            authoritative_source,
        )


def _frontier_contains_required_phrase(snapshot_value: str, authoritative_value: str) -> bool:
    snapshot_text = _normalize_frontier_cell(snapshot_value).rstrip(".")
    authoritative_text = _normalize_frontier_cell(authoritative_value).rstrip(".")
    return bool(authoritative_text and authoritative_text in snapshot_text)


def _normalize_bifurcation_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return _normalize_frontier_cell(value)


def _bifurcation_values_match(left: Any, right: Any) -> bool:
    left_text = _normalize_bifurcation_value(left)
    right_text = _normalize_bifurcation_value(right)
    if left_text.lower() in {"true", "false"} or right_text.lower() in {"true", "false"}:
        return left_text.lower() == right_text.lower()
    return left_text == right_text


def _truthy_flag(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "yes",
            "1",
            "authorized",
            "adopted",
            "claimed",
            "derived",
            "promoted",
        }
    return False


def _inactive_marker(value: Any) -> bool:
    return _normalize_bifurcation_value(value).lower() in {"", "none", "null", "false"}


SIDECAR_SUPERSESSION_DECISION_ID_FIELDS = (
    "active_state_supersession_decision_id",
    "sidecar_supersession_decision_id",
    "sidecar_supersession_authority_decision_id",
)
SIDECAR_SUPERSESSION_DECISION_PATH_FIELDS = (
    "active_state_supersession_authority_source_path",
    "sidecar_supersession_authority_source_path",
    "sidecar_supersession_decision_path",
)
SIDECAR_SUPERSESSION_SCOPE_FIELDS = (
    "active_state_supersession_scope",
    "sidecar_supersession_scope",
    "sidecar_supersession_authority_scope",
)


def _sidecar_supersession_authorization_ref(handoff: dict[str, Any]) -> tuple[str, str, str, bool]:
    bifurcation = handoff.get("active_state_bifurcation")
    bifurcation = bifurcation if isinstance(bifurcation, dict) else {}
    containers = (bifurcation, handoff)
    flag_present = False
    decision_id = ""
    decision_path = ""
    scope = ""
    for container in containers:
        explicit = container.get("explicit_sidecar_supersession_authorization")
        if isinstance(explicit, dict):
            flag_present = True
            decision_id = decision_id or str(explicit.get("decision_id", "")).strip()
            decision_path = decision_path or str(
                explicit.get("decision_path", explicit.get("authority_source_path", ""))
            ).strip()
            scope = scope or str(explicit.get("scope", "")).strip()
        elif _truthy_flag(explicit):
            flag_present = True
        for field_name in SIDECAR_SUPERSESSION_DECISION_ID_FIELDS:
            decision_id = decision_id or str(container.get(field_name, "")).strip()
        for field_name in SIDECAR_SUPERSESSION_DECISION_PATH_FIELDS:
            decision_path = decision_path or str(container.get(field_name, "")).strip()
        for field_name in SIDECAR_SUPERSESSION_SCOPE_FIELDS:
            scope = scope or str(container.get(field_name, "")).strip()
    return decision_id, decision_path, scope, flag_present


def _director_decision_authorizes_sidecar_supersession(
    decision_id: str,
    decision_path_text: str,
    scope: str,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not decision_id:
        errors.append("sidecar supersession requires an explicit Director decision id")
        return False, errors
    rows = read_csv_rows("DIRECTOR_DECISION_REGISTRY.csv")
    row = existing_by_id(rows, "decision_id").get(decision_id)
    if not row:
        errors.append(f"sidecar supersession Director decision {decision_id} is not registered")
        return False, errors
    row_path = str(row.get("decision_path", "")).strip()
    if decision_path_text and decision_path_text != row_path:
        errors.append(
            f"sidecar supersession decision path {decision_path_text} does not match "
            f"DIRECTOR_DECISION_REGISTRY.csv path {row_path}"
        )
        return False, errors
    decision_path_text = decision_path_text or row_path
    reason = validate_relative_path(decision_path_text)
    if reason:
        errors.append(f"invalid sidecar supersession decision path {decision_path_text}: {reason}")
        return False, errors
    decision_path = repo_path(decision_path_text)
    if not decision_path.exists():
        errors.append(f"sidecar supersession decision path does not exist: {decision_path_text}")
        return False, errors
    try:
        frontmatter, _ = load_frontmatter(decision_path)
    except StrictYamlError as exc:
        errors.append(f"sidecar supersession decision frontmatter is invalid: {exc}")
        return False, errors
    if _frontmatter_value(frontmatter.get("decision_id", "")) != decision_id:
        errors.append(f"sidecar supersession decision frontmatter decision_id does not match {decision_id}")
    authorized = any(
        _truthy_flag(frontmatter.get(field_name))
        for field_name in (
            "active_state_supersession_authorized",
            "sidecar_supersession_authorized",
        )
    )
    if not authorized:
        errors.append(
            f"{decision_path_text}: Director decision does not explicitly authorize "
            "active-state sidecar supersession"
        )
    decision_scope = str(
        frontmatter.get(
            "active_state_supersession_scope",
            frontmatter.get("sidecar_supersession_scope", ""),
        )
    ).strip()
    if not decision_scope:
        errors.append(f"{decision_path_text}: Director decision lacks sidecar supersession scope")
    if scope and decision_scope and scope != decision_scope:
        errors.append(
            f"sidecar supersession scope {scope!r} does not match Director decision scope {decision_scope!r}"
        )
    return not errors, errors


def _sidecar_supersession_authorized(handoff: dict[str, Any]) -> tuple[bool, list[str]]:
    decision_id, decision_path, scope, flag_present = _sidecar_supersession_authorization_ref(handoff)
    if not any([decision_id, decision_path, scope, flag_present]):
        return False, []
    if flag_present and not decision_id:
        return (
            False,
            [
                "flag-only sidecar supersession authorization is insufficient; "
                "provide a tracked Director decision id and authority source path"
            ],
        )
    return _director_decision_authorizes_sidecar_supersession(decision_id, decision_path, scope)


def _collect_protected_sidecar_flags(data: Any, prefix: str = "") -> list[str]:
    if isinstance(data, dict):
        found: list[str] = []
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in PROTECTED_SIDECAR_CLAIM_FLAGS and _truthy_flag(value):
                found.append(path)
            found.extend(_collect_protected_sidecar_flags(value, path))
        return found
    if isinstance(data, list):
        found = []
        for index, item in enumerate(data):
            path = f"{prefix}[{index}]" if prefix else f"[{index}]"
            found.extend(_collect_protected_sidecar_flags(item, path))
        return found
    return []


def _active_state_bifurcation_error(
    report: ValidationReport,
    field_name: str,
    authoritative_value: Any,
    snapshot_value: Any,
    authoritative_source: str,
    snapshot_source: str,
) -> None:
    report.error(
        f"{snapshot_source}: active_state_bifurcation drift "
        f"field={field_name} "
        f"authoritative_value={_normalize_bifurcation_value(authoritative_value)!r} "
        f"snapshot_value={_normalize_bifurcation_value(snapshot_value)!r} "
        f"authoritative_source={authoritative_source} "
        f"suggested_repair_route={CURRENT_FRONTIER_REPAIR_ROUTE}"
    )


def _compare_active_state_bifurcation_field(
    report: ValidationReport,
    snapshot: dict[str, Any],
    field_name: str,
    authoritative_value: Any,
    authoritative_source: str,
    snapshot_source: str,
) -> None:
    snapshot_value = snapshot.get(field_name, "")
    if not _bifurcation_values_match(authoritative_value, snapshot_value):
        _active_state_bifurcation_error(
            report,
            field_name,
            authoritative_value,
            snapshot_value,
            authoritative_source,
            snapshot_source,
        )


def _validate_sidecar_supersession_boundary(
    report: ValidationReport,
    bifurcation: dict[str, Any],
    handoff: dict[str, Any],
    source_path: str,
) -> None:
    sidecar_fields = (
        bifurcation.get("latest_project_system_sidecar_task_id"),
        bifurcation.get("latest_project_system_sidecar_status"),
    )
    sidecar_present = any(not _inactive_marker(value) for value in sidecar_fields)
    supersedes = _truthy_flag(bifurcation.get("sidecar_supersedes_research_handoff"))
    route_source = _normalize_bifurcation_value(
        bifurcation.get("next_research_route_source", "latest_research_handoff")
    )
    authorized, authorization_errors = _sidecar_supersession_authorized(handoff)
    if (supersedes or route_source != "latest_research_handoff") and not authorized:
        report.error(
            f"{source_path}: project-system sidecar may not supersede the latest "
            "ordinary research handoff without explicit tracked authorization"
        )
        for error in authorization_errors:
            report.error(f"{source_path}: {error}")
    if sidecar_present and not supersedes and route_source != "latest_research_handoff":
        report.error(
            f"{source_path}: project-system sidecar is present but next_research_route_source "
            "does not remain latest_research_handoff"
        )


def _validate_project_improvement_sidecar_claims(report: ValidationReport) -> None:
    sidecar_dir = CONTROL_DIR / "project_improvement_handoffs"
    if not sidecar_dir.exists():
        return
    for path in sorted(sidecar_dir.glob("improve-project-handoff_*.yaml")):
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        try:
            data = load_yaml(path)
        except StrictYamlError:
            continue
        flags = _collect_protected_sidecar_flags(data)
        if flags:
            report.error(
                f"{relative_path}: project-system sidecar contains protected "
                "physics-authority claim flags without ledger and Gate Chair authority: "
                + ";".join(sorted(flags))
            )


def validate_active_state_bifurcation(report: ValidationReport, tasks: dict[str, dict[str, str]]) -> None:
    """Validate sidecar/research authority separation in active-state surfaces."""

    frontier_path = CONTROL_DIR / "current_frontier.md"
    program_state_path = CONTROL_DIR / "program_state.yaml"
    if not frontier_path.exists() or not program_state_path.exists():
        return
    try:
        state = load_yaml(program_state_path)
    except StrictYamlError:
        return
    latest_handoff_id = str(state.get("latest_handoff_id", "")).strip()
    if not latest_handoff_id:
        return
    handoff_path = CONTROL_DIR / "handoffs" / f"{latest_handoff_id}.yaml"
    if not handoff_path.exists():
        return
    try:
        handoff = load_yaml(handoff_path)
    except StrictYamlError:
        return
    bifurcation = handoff.get("active_state_bifurcation")
    if not isinstance(bifurcation, dict):
        report.error(
            f"research_control/handoffs/{latest_handoff_id}.yaml: missing active_state_bifurcation "
            f"suggested_repair_route={CURRENT_FRONTIER_REPAIR_ROUTE}"
        )
        return

    frontier_text = frontier_path.read_text(encoding="utf-8")
    markdown_snapshot = current_frontier_active_state_bifurcation(frontier_text)
    if not markdown_snapshot:
        report.error(
            "research_control/current_frontier.md: missing Active-State Bifurcation section "
            f"suggested_repair_route={CURRENT_FRONTIER_REPAIR_ROUTE}"
        )
    handoff_source = f"research_control/handoffs/{latest_handoff_id}.yaml"
    for field_name in ACTIVE_STATE_BIFURCATION_FIELDS:
        _compare_active_state_bifurcation_field(
            report,
            markdown_snapshot,
            field_name,
            bifurcation.get(field_name, ""),
            handoff_source,
            "research_control/current_frontier.md",
        )

    if not _bifurcation_values_match(bifurcation.get("latest_research_handoff_id"), latest_handoff_id):
        _active_state_bifurcation_error(
            report,
            "latest_research_handoff_id",
            latest_handoff_id,
            bifurcation.get("latest_research_handoff_id"),
            "research_control/program_state.yaml",
            handoff_source,
        )
    handoff_task_id = str(handoff.get("task_id", "")).strip()
    if handoff_task_id and not _bifurcation_values_match(bifurcation.get("latest_research_task_id"), handoff_task_id):
        _active_state_bifurcation_error(
            report,
            "latest_research_task_id",
            handoff_task_id,
            bifurcation.get("latest_research_task_id"),
            handoff_source,
            handoff_source,
        )
    if handoff_task_id and handoff_task_id not in tasks:
        report.error(f"{handoff_source}: active_state_bifurcation latest_research_task_id is not registered")
    next_action = str(handoff.get("next_action", "")).strip()
    if next_action and not _bifurcation_values_match(bifurcation.get("latest_research_next_action"), next_action):
        _active_state_bifurcation_error(
            report,
            "latest_research_next_action",
            next_action,
            bifurcation.get("latest_research_next_action"),
            handoff_source,
            handoff_source,
        )

    _validate_sidecar_supersession_boundary(report, bifurcation, handoff, handoff_source)

    compact_path = REPO_ROOT / "output" / "compact_current_frontier_v16.json"
    if compact_path.exists():
        try:
            compact = json.loads(compact_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f"output/compact_current_frontier_v16.json: invalid JSON: {exc.msg}")
        else:
            compact_snapshot = compact.get("active_state_bifurcation")
            if not isinstance(compact_snapshot, dict):
                report.error("output/compact_current_frontier_v16.json: missing active_state_bifurcation object")
            else:
                for field_name in ACTIVE_STATE_BIFURCATION_FIELDS:
                    _compare_active_state_bifurcation_field(
                        report,
                        compact_snapshot,
                        field_name,
                        bifurcation.get(field_name, ""),
                        handoff_source,
                        "output/compact_current_frontier_v16.json",
                    )
                _validate_sidecar_supersession_boundary(
                    report,
                    compact_snapshot,
                    handoff,
                    "output/compact_current_frontier_v16.json",
                )

    _validate_project_improvement_sidecar_claims(report)


def validate_current_frontier_sync(report: ValidationReport, tasks: dict[str, dict[str, str]]) -> None:
    """Fail when current_frontier.md drifts from tracked active-state authority."""

    frontier_path = CONTROL_DIR / "current_frontier.md"
    program_state_path = CONTROL_DIR / "program_state.yaml"
    if not frontier_path.exists():
        report.error(
            "research_control/current_frontier.md: missing active-state snapshot "
            f"suggested_repair_route={CURRENT_FRONTIER_REPAIR_ROUTE}"
        )
        return
    if not program_state_path.exists():
        return
    try:
        state = load_yaml(program_state_path)
    except StrictYamlError:
        return
    frontier_text = frontier_path.read_text(encoding="utf-8")
    snapshot = current_frontier_active_state(frontier_text)
    distance_snapshot = current_frontier_distance_rows(frontier_text)

    active_task_id = str(state.get("active_task_id", "")).strip()
    latest_handoff_id = str(state.get("latest_handoff_id", "")).strip()
    current_status = str(state.get("current_status", "")).strip()
    next_recommended_action = str(state.get("next_recommended_action", "")).strip()

    _compare_current_frontier_field(
        report,
        snapshot,
        "active_task_id",
        active_task_id,
        "research_control/program_state.yaml",
    )
    _compare_current_frontier_field(
        report,
        snapshot,
        "latest_handoff_id",
        latest_handoff_id,
        "research_control/program_state.yaml",
    )
    _compare_current_frontier_field(
        report,
        snapshot,
        "current_status",
        current_status,
        "research_control/program_state.yaml",
    )

    active_task_path = CONTROL_DIR / "tasks" / active_task_id / "00_TASK.yaml"
    if active_task_id and active_task_id not in tasks:
        _current_frontier_drift_error(
            report,
            "active_task_folder",
            active_task_id,
            "missing registered active task",
            "registries/RESEARCH_TASK_REGISTRY.csv",
        )
    elif active_task_path.exists():
        try:
            active_task = load_yaml(active_task_path)
        except StrictYamlError:
            active_task = {}
        task_file_id = str(active_task.get("task_id", "")).strip()
        if task_file_id and task_file_id != active_task_id:
            _current_frontier_drift_error(
                report,
                "active_task_folder",
                active_task_id,
                task_file_id,
                f"research_control/tasks/{active_task_id}/00_TASK.yaml",
            )

    handoff_path = CONTROL_DIR / "handoffs" / f"{latest_handoff_id}.yaml"
    handoff: dict[str, Any] = {}
    if latest_handoff_id and not handoff_path.exists():
        _current_frontier_drift_error(
            report,
            "latest_handoff_id",
            latest_handoff_id,
            "missing handoff file",
            "research_control/program_state.yaml",
        )
    elif handoff_path.exists():
        try:
            handoff = load_yaml(handoff_path)
        except StrictYamlError:
            handoff = {}

    handoff_next_action = str(handoff.get("next_action", "")).strip()
    if handoff_next_action and next_recommended_action and handoff_next_action != next_recommended_action:
        _current_frontier_drift_error(
            report,
            "next_recommended_action",
            handoff_next_action,
            next_recommended_action,
            f"research_control/handoffs/{latest_handoff_id}.yaml",
        )
    next_authority = handoff_next_action or next_recommended_action
    if next_authority:
        snapshot_next = snapshot.get("next_recommended_action", "")
        if not _frontier_contains_required_phrase(snapshot_next, next_authority):
            _current_frontier_drift_error(
                report,
                "next_recommended_action",
                next_authority,
                snapshot_next,
                f"research_control/handoffs/{latest_handoff_id}.yaml"
                if handoff_next_action
                else "research_control/program_state.yaml",
            )

    distance = handoff.get("distance_to_gr") if isinstance(handoff, dict) else None
    distance = distance if isinstance(distance, dict) else {}
    milestone = str(distance.get("milestone", "")).strip()
    burden_id = str(distance.get("burden_id", "")).strip()

    milestone_snapshot = snapshot.get("target_derivation_milestone", "")
    if milestone and milestone != "none":
        if milestone not in milestone_snapshot:
            _current_frontier_drift_error(
                report,
                "target_derivation_milestone",
                milestone,
                milestone_snapshot,
                f"research_control/handoffs/{latest_handoff_id}.yaml",
            )
    elif milestone == "none" and "none" not in milestone_snapshot.lower():
        _current_frontier_drift_error(
            report,
            "target_derivation_milestone",
            "none",
            milestone_snapshot,
            f"research_control/handoffs/{latest_handoff_id}.yaml",
        )

    if not burden_id or burden_id == "none":
        return
    ledger_rows = existing_by_id(read_csv_rows("DISTANCE_TO_GR_LEDGER.csv"), "burden_id")
    ledger_row = ledger_rows.get(burden_id)
    snapshot_row = distance_snapshot.get(burden_id)
    if not ledger_row:
        _current_frontier_drift_error(
            report,
            f"distance_to_gr.current_status[{burden_id}]",
            burden_id,
            "missing ledger row",
            f"research_control/handoffs/{latest_handoff_id}.yaml",
        )
        return
    if not snapshot_row:
        _current_frontier_drift_error(
            report,
            f"distance_to_gr.current_status[{burden_id}]",
            ledger_row.get("current_status", ""),
            "missing Distance-To-GR row",
            "registries/DISTANCE_TO_GR_LEDGER.csv",
        )
        return
    ledger_status = _normalize_frontier_cell(ledger_row.get("current_status", ""))
    snapshot_status = _normalize_frontier_cell(
        snapshot_row.get("Legacy status", "") or snapshot_row.get("Current status", "")
    )
    if ledger_status != snapshot_status:
        _current_frontier_drift_error(
            report,
            f"distance_to_gr.current_status[{burden_id}]",
            ledger_status,
            snapshot_status,
            "registries/DISTANCE_TO_GR_LEDGER.csv",
        )


def validate_compact_current_frontier_sync(report: ValidationReport) -> None:
    """Fail when compact_current_frontier_v16 outputs drift from tracked state."""

    if compact_frontier_validator is None:
        report.error(
            "compact_current_frontier_v16: import failed for "
            "scripts/research_control/validate_compact_current_frontier_v16.py"
        )
        return
    result = compact_frontier_validator.build_report(REPO_ROOT)
    for error in result.get("errors", []):
        if isinstance(error, dict):
            error_id = error.get("id", "unknown_error")
            message = error.get("message", "")
        else:
            error_id = "unknown_error"
            message = str(error)
        report.error(
            "compact_current_frontier_v16: "
            f"{error_id}: {message} "
            "suggested_repair_route=compact_current_frontier_check_integration_v16"
        )


def handoff_number(path: Path) -> int | None:
    match = re.fullmatch(r"handoff-(\d{4})\.yaml", path.name)
    return int(match.group(1)) if match else None


def immutable_historical_ordinary_route_guard_is_compatible(
    yaml_path: Path,
    data: dict[str, Any],
    errors: list[str],
) -> bool:
    """Preserve one exact predecessor observation finalized after its timestamp."""

    compatibility = IMMUTABLE_HISTORICAL_ORDINARY_ROUTE_GUARD_COMPATIBILITY.get(
        yaml_path.name
    )
    if not compatibility:
        return False
    if sha256_file(yaml_path) != compatibility["sha256"]:
        return False
    if tuple(errors) != compatibility["errors"]:
        return False
    guard = data.get("ordinary_route_guard")
    if not isinstance(guard, dict):
        return False
    return (
        guard.get("evaluation_id") == compatibility["evaluation_id"]
        and str(guard.get("consecutive_project_system_tasks_before_selection", ""))
        == str(compatibility["declared_count"])
    )


def validate_handoffs(
    report: ValidationReport,
    tasks: dict[str, dict[str, str]],
    jobs: dict[str, dict[str, str]],
) -> None:
    handoff_dir = CONTROL_DIR / "handoffs"
    if not handoff_dir.exists():
        report.error("missing research_control/handoffs")
        return
    numbers: list[int] = []
    for yaml_path in sorted(handoff_dir.glob("handoff-*.yaml")):
        number = handoff_number(yaml_path)
        if number is None:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: invalid handoff filename")
            continue
        numbers.append(number)
        md_path = yaml_path.with_suffix(".md")
        if not md_path.exists():
            report.error(f"{yaml_path.name}: missing Markdown mirror")
        try:
            data = load_yaml(yaml_path)
        except StrictYamlError as exc:
            report.error(f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        for field_name in ["handoff_id", "created_at", "task_id", "job_id", "completion_path", "next_action"]:
            if not data.get(field_name):
                report.error(f"{yaml_path.name}: missing {field_name}")
        if str(data.get("task_id", "")) not in tasks:
            report.error(f"{yaml_path.name}: task_id is not registered")
        if str(data.get("job_id", "")) and str(data.get("job_id", "")) not in jobs:
            report.error(f"{yaml_path.name}: job_id is not registered")
        if ".local/" in yaml_path.read_text(encoding="utf-8"):
            report.error(f"{yaml_path.name}: tracked handoff YAML must not use .local/ as authority")
        validate_physics_payload_ratio_policy_record(
            report,
            data,
            yaml_path.relative_to(REPO_ROOT).as_posix(),
        )
        ordinary_route = evaluate_research_handoff_guard(data, REPO_ROOT)
        ordinary_route_errors = list(ordinary_route["errors"])
        if immutable_historical_ordinary_route_guard_is_compatible(
            yaml_path,
            data,
            ordinary_route_errors,
        ):
            report.warn(
                f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: ordinary-route guard: "
                "immutable historical count preserved because the predecessor lifecycle "
                "completed after the handoff timestamp"
            )
        else:
            for error in ordinary_route_errors:
                report.error(
                    f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: "
                    f"ordinary-route guard: {error}"
                )
        for warning in ordinary_route.get("warnings", []):
            report.warn(
                f"{yaml_path.relative_to(REPO_ROOT).as_posix()}: "
                f"ordinary-route guard: {warning}"
            )
        validate_loop_control_handoff(report, data, jobs, yaml_path)
    if numbers and numbers != list(range(min(numbers), max(numbers) + 1)):
        report.error("handoff IDs must be monotonic without gaps")


def validate_project_improvement_handoffs(report: ValidationReport) -> None:
    result = validate_project_improvement_handoff_records(REPO_ROOT)
    for error in result["errors"]:
        report.error(error)
    for warning in result["warnings"]:
        report.warn(warning)


def validate_loop_control_handoff(
    report: ValidationReport,
    data: dict[str, Any],
    jobs: dict[str, dict[str, str]],
    yaml_path: Path,
) -> None:
    if not timestamp_at_or_after(data.get("created_at", "")):
        return
    job_id = str(data.get("job_id", ""))
    job = jobs.get(job_id, {})
    if job.get("role_id", "") not in PHYSICS_ROLE_IDS:
        return

    path_text = yaml_path.relative_to(REPO_ROOT).as_posix()
    handoff_text = text_blob(data.get("summary", ""), data.get("next_action", ""))
    future_pause_policy = theoretical_continuation_policy_active(job, data)
    route = str(data.get("loop_risk_route", "")).strip()
    if future_pause_policy and route in LEGACY_BRIDGE_OR_FAIL_ROUTES:
        report.error(
            f"{path_text}: future physics handoff may not set loop_risk_route=controlled_pause; "
            "use theoretical_decision_role_selection or human_gated_ontology_change_required"
        )
    if (
        "ontology formalizer" in handoff_text
        and any(marker in handoff_text for marker in ("obligation packet", "generic repair", "repair packet"))
        and not any(marker in handoff_text for marker in ONTOLOGY_PAYLOAD_TEXT_MARKERS)
    ):
        report.error(
            f"{path_text}: future handoff may not route to a generic Ontology Formalizer packet"
        )

    if any(
        marker in handoff_text
        for marker in (
            "same burdens persist",
            "repeated unmet burdens",
            "no new mathematical payload",
            "scoped obstruction",
        )
    ):
        route_markers = (
            "candidate constructor",
            "concrete witness",
            "controlled pause",
            "gate chair",
            "human-gated ontology",
            "human gated ontology",
            "scoped no-go",
            "obstruction",
            "source-side selector",
            "source-side irrelevance",
            "theoretical decision",
            "theoretical-continuation-selector",
        )
        if future_pause_policy:
            route_markers = tuple(
                marker for marker in route_markers if marker != "controlled pause"
            )
        if not any(marker in handoff_text for marker in route_markers):
            report.error(
                f"{path_text}: repeated-burden or obstruction handoff must route through bridge_or_fail escalation"
            )


def validate_approvals(report: ValidationReport, decisions: dict[str, dict[str, str]]) -> None:
    approval_dir = CONTROL_DIR / "approvals"
    if not approval_dir.exists():
        report.error("missing research_control/approvals")
        return
    for path in approval_dir.glob("approval-*.yaml"):
        try:
            data = load_yaml(path)
        except StrictYamlError as exc:
            report.error(f"{path.relative_to(REPO_ROOT).as_posix()}: {exc}")
            continue
        decision_id = str(data.get("decision_id", ""))
        if decision_id and decision_id not in decisions:
            report.error(f"{path.name}: decision_id is not registered")


def _safe_claim_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in SAFE_BOUNDARY_MARKERS)


def validate_claim_boundaries(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    for row in claim_rows:
        if row["authority_source_path"]:
            reason = validate_relative_path(row["authority_source_path"])
            if reason:
                report.error(f"{row['claim_boundary_id']}: invalid authority_source_path: {reason}")
            elif not repo_path(row["authority_source_path"]).exists():
                report.error(f"{row['claim_boundary_id']}: missing authority_source_path")


def scan_for_forbidden_claims(report: ValidationReport, claim_rows: list[dict[str, str]]) -> None:
    scan_roots = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / ".agents",
        CONTROL_DIR,
        REPO_ROOT / ".codex" / "skills" / "continue-research",
    ]
    registry_path = REGISTRY_DIR / "CLAIM_BOUNDARY_REGISTRY.csv"
    for root in scan_roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                continue
            relative = path.relative_to(REPO_ROOT).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for phrase in FORBIDDEN_PHRASES:
                    if phrase in line and not _safe_claim_context(line):
                        report.error(f"{relative}:{line_number}: forbidden claim phrase outside boundary context: {phrase}")
    # The registry itself is allowed to contain forbidden phrases in forbidden_claims.
    if registry_path.exists():
        _ = claim_rows


def validate_changed_claim_language(report: ValidationReport, paths: Iterable[str]) -> None:
    if claim_language_linter is None:
        report.error("claim-language linter import failed: scripts/project_control/validate_claim_language.py")
        return

    selected_paths = claim_language_linter.claim_language_gate_paths(paths, repo_root=REPO_ROOT)
    if not selected_paths:
        return
    try:
        result = claim_language_linter.validate_paths(repo_root=REPO_ROOT, paths=selected_paths)
    except (FileNotFoundError, StrictYamlError, OSError, re.error) as exc:
        report.findings.append(
            {
                "gate_id": "claim_language_changed",
                "finding_id": "claim_language_changed:configuration_error",
                "severity": "blocking",
                "surface_class": "configuration",
                "finding_kind": "configuration_error",
                "context": "claim_configuration",
            }
        )
        report.error(f"claim-language validation failed to run: {exc}")
        return

    for error in result.get("config_errors", []):
        report.findings.append(
            {
                "gate_id": "claim_language_changed",
                "finding_id": "claim_language_changed:configuration_error",
                "severity": "blocking",
                "surface_class": "configuration",
                "finding_kind": "configuration_error",
                "context": "claim_configuration",
            }
        )
        report.error(f"claim-language config error: {error}")
    for finding in result.get("findings", []):
        severity = str(finding.get("severity", ""))
        class_id = str(finding.get("class_id", ""))
        report.findings.append(
            {
                **finding,
                "gate_id": "claim_language_changed",
                "finding_id": f"claim_language_changed:{class_id}",
            }
        )
        message = (
            f"{finding.get('path')}:{finding.get('line')}: claim-language "
            f"{'hard failure' if severity.startswith('hard_fail_') else 'warning'} "
            f"{class_id} {finding.get('matched_text')!r} ({severity}); "
            f"{finding.get('corrective_language')}"
        )
        if severity.startswith("hard_fail_"):
            report.error(message)
        else:
            report.warn(message)


def changed_paths(base_ref: str, staged_only: bool) -> list[str]:
    if staged_only:
        diff_cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", base_ref]
    else:
        diff_cmd = ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref]
    diff = subprocess.run(diff_cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if diff.returncode != 0:
        raise RuntimeError(diff.stderr)
    paths = [line.strip() for line in diff.stdout.splitlines() if line.strip()]
    if not staged_only:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if untracked.returncode != 0:
            raise RuntimeError(untracked.stderr)
        paths.extend(line.strip() for line in untracked.stdout.splitlines() if line.strip())
    return sorted(set(paths))


def changed_line_numbers_from_diff(diff_text: str) -> set[int]:
    lines: set[int] = set()
    for raw_line in diff_text.splitlines():
        match = HUNK_RE.search(raw_line)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        if count > 0:
            lines.update(range(start, start + count))
    return lines


def changed_line_numbers(path: str, base_ref: str, staged_only: bool) -> set[int]:
    if staged_only:
        command = ["git", "diff", "--cached", "--unified=0", base_ref, "--", path]
    else:
        command = ["git", "diff", "--unified=0", base_ref, "--", path]
    diff = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if diff.returncode != 0:
        return set()
    return changed_line_numbers_from_diff(diff.stdout)


def markdown_authority_by_line(text: str) -> dict[int, str]:
    active = ""
    authorities: dict[int, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        marker = AUTHORITY_MARKER_RE.search(line)
        if marker:
            active = marker.group(1)
        authorities[line_number] = active or "unmarked"
    return authorities


def markdown_authorities_for_changed_lines(
    path_text: str,
    base_ref: str,
    staged_only: bool,
) -> set[str]:
    path = repo_path(path_text)
    if not path.exists() or not path.is_file():
        return {"unmarked"}
    text = path.read_text(encoding="utf-8")
    authorities_by_line = markdown_authority_by_line(text)
    lines = changed_line_numbers(path_text, base_ref, staged_only)
    if lines:
        return {authorities_by_line.get(line_number, "unmarked") for line_number in lines}
    markers = set(AUTHORITY_MARKER_RE.findall(text))
    return markers or {"unmarked"}


def _pattern_is_too_broad(pattern: str) -> bool:
    return (
        pattern in GLOBALLY_BROAD_PATTERNS
        or pattern.startswith("*/")
        or pattern.startswith("**/")
    )


def _path_matches(path: str, pattern: str) -> bool:
    if _pattern_is_too_broad(pattern):
        return False
    return path == pattern or fnmatch.fnmatch(path, pattern)


def is_control_markdown_path(path: str) -> bool:
    return any(_path_matches(path, pattern) for pattern in CONTROL_MARKDOWN_PATTERNS)


def role_execution_row_for_job(job_id: str) -> dict[str, str]:
    try:
        rows = read_csv_rows("ROLE_EXECUTION_REGISTRY.csv")
    except FileNotFoundError:
        return {}
    for row in rows:
        if row.get("agent_job_id") == job_id:
            return row
    return {}


def allows_explanatory_markdown_overlay(job: dict[str, str]) -> bool:
    row = role_execution_row_for_job(job.get("job_id", ""))
    if row.get("role_execution_kind") != "task_overlay":
        return False
    tokens = split_semicolon(row.get("expanded_permissions", ""))
    tokens.extend(split_semicolon(row.get("added_constraints", "")))
    return any("explanatory_markdown" in token for token in tokens)


def validate_markdown_authority_boundaries(
    report: ValidationReport,
    job: dict[str, str],
    paths: Iterable[str],
    base_ref: str,
    staged_only: bool,
) -> None:
    role_id = job.get("role_id", "")
    explanatory_overlay = allows_explanatory_markdown_overlay(job)
    for changed in paths:
        if is_control_markdown_path(changed):
            if role_id == "documentation-curator":
                report.error(f"{changed}: documentation-curator cannot edit control markdown")
            continue
        if changed not in MIXED_MARKDOWN_PATHS:
            continue
        authorities = markdown_authorities_for_changed_lines(changed, base_ref, staged_only)
        if "unmarked" in authorities:
            report.error(f"{changed}: mixed markdown change is outside an authority marker")
        if role_id == "documentation-curator" and "control" in authorities:
            report.error(f"{changed}: documentation-curator cannot edit control-marked section")
        if (
            role_id == "project-control-maintainer"
            and "explanatory" in authorities
            and not explanatory_overlay
        ):
            report.error(
                f"{changed}: project-control-maintainer cannot edit explanatory section without task_overlay explanatory_markdown permission"
            )


def validate_diff(
    report: ValidationReport,
    job_rows: dict[str, dict[str, str]],
    base_ref: str,
    staged_only: bool,
) -> None:
    active_jobs = [row for row in job_rows.values() if row["status"] in {"active", "completed"}]
    job = sorted(active_jobs, key=lambda row: row["created_at"])[-1] if active_jobs else None
    if job is None:
        report.error("--check-diff requires an active or completed AgentJob")
    try:
        paths = changed_paths(base_ref, staged_only)
    except RuntimeError as exc:
        report.error(str(exc))
        return
    if job is not None:
        allowed = split_semicolon(job["allowed_write_paths"])
        output_paths = split_semicolon(job["output_paths"])
        allowed.extend(output_paths)
        job_path_text = job.get("job_path", "")
        job_path = repo_path(job_path_text) if job_path_text else None
        if job_path and job_path.exists():
            try:
                job_contract = load_yaml(job_path)
            except StrictYamlError as exc:
                report.error(f"{job_path_text}: {exc}")
                job_contract = {}
            generated_paths = job_contract.get("allowed_generated_paths", [])
            if isinstance(generated_paths, list):
                allowed.extend(str(path) for path in generated_paths if str(path))
        allowed.extend(conditional_checkpoint_sidecar_paths(REPO_ROOT, paths, allowed))
        for pattern in allowed:
            if _pattern_is_too_broad(pattern):
                report.error(f"{job['job_id']}: overly broad allowlist pattern {pattern}")
        for changed in paths:
            if changed.startswith(".local/"):
                continue
            if not any(_path_matches(changed, pattern) for pattern in allowed):
                report.error(f"{changed}: changed path is not allowed by {job['job_id']}")
        validate_markdown_authority_boundaries(report, job, paths, base_ref, staged_only)
    validate_changed_claim_language(report, paths)


def validate_all(
    *,
    check_diff: bool = False,
    base_ref: str = "HEAD",
    staged_only: bool = False,
) -> ValidationReport:
    report = ValidationReport()
    validate_registry_columns(report)
    validate_distance_to_gr_ledger(report)
    validate_frontier_theorem_inventory(report)
    rows_by_registry = {
        name: read_csv_rows(name)
        for name in REGISTRY_COLUMNS
        if (REGISTRY_DIR / name).exists()
    }
    if len(rows_by_registry) != len(REGISTRY_COLUMNS):
        if check_diff:
            partial_jobs = {
                row["job_id"]: row
                for row in rows_by_registry.get("AGENT_JOB_REGISTRY.csv", [])
                if row.get("job_id")
                and row.get("status")
                and row.get("created_at")
                and row.get("allowed_write_paths") is not None
                and row.get("output_paths") is not None
            }
            validate_diff(report, partial_jobs, base_ref, staged_only)
        return report
    validate_registry_values(report, rows_by_registry)
    validate_countermodel_obligation_registry(
        report,
        rows_by_registry["COUNTERMODEL_OBLIGATION_REGISTRY.csv"],
    )
    roles = validate_roles(report, rows_by_registry["AGENT_ROLE_REGISTRY.csv"])
    decisions = validate_director_decisions(
        report, rows_by_registry["DIRECTOR_DECISION_REGISTRY.csv"], roles
    )
    jobs = validate_agent_jobs(
        report, rows_by_registry["AGENT_JOB_REGISTRY.csv"], roles, decisions
    )
    tasks = validate_tasks(
        report,
        rows_by_registry["RESEARCH_TASK_REGISTRY.csv"],
        decisions,
        jobs,
    )
    validate_execution_roles(
        report,
        rows_by_registry["ROLE_EXECUTION_REGISTRY.csv"],
        roles,
        jobs,
        tasks,
    )
    validate_program_state(report, tasks)
    validate_handoffs(report, tasks, jobs)
    validate_current_frontier_sync(report, tasks)
    validate_active_state_bifurcation(report, tasks)
    validate_compact_current_frontier_sync(report)
    validate_project_improvement_handoffs(report)
    validate_approvals(report, decisions)
    validate_claim_boundaries(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    scan_for_forbidden_claims(report, rows_by_registry["CLAIM_BOUNDARY_REGISTRY.csv"])
    if check_diff:
        validate_diff(report, jobs, base_ref, staged_only)
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_reporting_arguments(parser)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results.")
    parser.add_argument(
        "--legacy-human",
        action="store_true",
        help="Emit the previous unbounded human-readable output.",
    )
    parser.add_argument("--check-diff", action="store_true", help="Check current git diff against the latest active/completed AgentJob.")
    parser.add_argument("--staged-only", action="store_true", help="Check staged changes only.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base ref for --check-diff.")
    args = parser.parse_args(argv)
    common_mode_selected = any(
        getattr(args, name)
        for name in ("summary", "json_summary", "full_json", "receipt", "quiet")
    )
    if args.json and (args.legacy_human or common_mode_selected):
        parser.error("--json cannot be combined with another reporting mode")
    if args.legacy_human and common_mode_selected:
        parser.error("--legacy-human cannot be combined with a common reporting mode")
    return args


def _legacy_payload(report: ValidationReport) -> dict[str, object]:
    return {
        "errors": report.errors,
        "warnings": report.warnings,
        "findings": report.findings,
    }


def _finding_id(gate_id: str, level: str, message: str, occurrence: int) -> str:
    prefix = gate_id.replace("_", "-").upper()
    digest = hashlib.sha256(
        json.dumps(
            {"level": level, "message": message, "occurrence": occurrence},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:12].upper()
    return f"{prefix}-{level}-{digest}"


def _working_tree_digest(payload: dict[str, object]) -> str:
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    )
    results: dict[str, bytes] = {}
    for label, command in (
        ("head", ["git", "rev-parse", "HEAD"]),
        ("diff", ["git", "diff", "--no-ext-diff", "--binary", "HEAD", "--"]),
        ("untracked", ["git", "ls-files", "--others", "--exclude-standard", "-z"]),
    ):
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            return digest.hexdigest()
        results[label] = completed.stdout
        digest.update(label.encode("ascii") + b"\0" + completed.stdout)
    for raw_path in sorted(path for path in results["untracked"].split(b"\0") if path):
        path = REPO_ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        if path.is_file():
            digest.update(b"untracked-content\0" + raw_path + b"\0" + path.read_bytes())
    return digest.hexdigest()


def adapt_to_common_run(report: ValidationReport, args: argparse.Namespace) -> ValidationRun:
    gate_id = "research_control_diff" if args.check_diff else "research_control_core"
    occurrence_counts: dict[tuple[str, str], int] = {}
    findings: list[CommonValidationFinding] = []
    for level, code, messages in (
        ("ERROR", "research_control_error", report.errors),
        ("WARN", "research_control_warning", report.warnings),
    ):
        for message in messages:
            key = (level, message)
            occurrence_counts[key] = occurrence_counts.get(key, 0) + 1
            findings.append(
                CommonValidationFinding(
                    finding_id=_finding_id(
                        gate_id,
                        level,
                        message,
                        occurrence_counts[key],
                    ),
                    level=level,
                    code=code,
                    message=message,
                )
            )
    payload = {
        "legacy": _legacy_payload(report),
        "check_diff": args.check_diff,
        "staged_only": args.staged_only,
        "base_ref": args.base_ref,
    }
    digest = _working_tree_digest(payload)
    status = "PASS" if report.ok() else "FAIL"
    exit_code = 0 if report.ok() else 1
    gate = ValidationGateResult(
        gate_id=gate_id,
        status=status,
        severity="blocking",
        exit_code=exit_code,
        findings=tuple(findings),
    )
    prefix = gate_id.replace("_", "-").upper()
    return ValidationRun(
        run_id=f"{prefix}-{digest[:16].upper()}",
        tree_hash=f"working-sha256:{digest}",
        status=status,
        exit_code=exit_code,
        gate_results=(gate,),
        profile="shadow_planner",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = validate_all(
        check_diff=args.check_diff,
        base_ref=args.base_ref,
        staged_only=args.staged_only,
    )
    if args.json:
        print(json.dumps(_legacy_payload(report), indent=2))
        return 0 if report.ok() else 1
    if args.legacy_human:
        if report.errors:
            print("Research-control validation failed:")
            for error in report.errors:
                print(f"- {error}")
        else:
            print("Research-control validation passed.")
        for warning in report.warnings:
            print(f"Warning: {warning}")
        return 0 if report.ok() else 1
    return emit_report(
        adapt_to_common_run(report, args),
        options=options_from_namespace(args),
        receipt_root=REPO_ROOT / DEFAULT_RECEIPT_ROOT,
        stream=sys.stdout,
    )


if __name__ == "__main__":
    raise SystemExit(main())
