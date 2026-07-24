"""Stable typed API for the repository validation planner and executor.

The functions in this module are a programmatic adapter over the tracked
planner, manifest, adapter bindings, and executor.  They do not create
validation policy or confer scientific, source, ontology, benchmark, proof, or
Gate Chair authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from scripts.project_control.classify_project_changes import classify_paths
from scripts.validation.executor import (
    ExecutionOutcome,
    ExecutorError,
    execute_plan,
)
from scripts.validation.plan import (
    PlannerError,
    ValidationPlan,
    build_plan,
    load_manifest,
)
from scripts.validation.run import load_adapters

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_ADAPTER_BINDINGS = (
    REPO_ROOT / "research_control/design/validation_adapter_bindings_v1.json"
)
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".local/validation-receipts"


class ValidationApiError(ValueError):
    """Fail-closed programmatic API error with CLI-compatible exit semantics."""

    exit_code = 2
    status = "BLOCKED_CONFIGURATION"


def _tuple_of_nonblank_strings(values: Iterable[str], name: str) -> tuple[str, ...]:
    result = tuple(values)
    if any(not isinstance(value, str) or not value for value in result):
        raise ValidationApiError(f"{name} must contain nonblank strings")
    return result


@dataclass(frozen=True, slots=True)
class ValidationPlanRequest:
    """Inputs for deterministic plan construction."""

    profile: str
    paths: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ()
    role_obligations: tuple[str, ...] = ()
    manifest_path: Path = DEFAULT_MANIFEST

    def __post_init__(self) -> None:
        object.__setattr__(self, "paths", _tuple_of_nonblank_strings(self.paths, "paths"))
        object.__setattr__(
            self,
            "scopes",
            _tuple_of_nonblank_strings(self.scopes, "scopes"),
        )
        object.__setattr__(
            self,
            "role_obligations",
            _tuple_of_nonblank_strings(self.role_obligations, "role_obligations"),
        )
        object.__setattr__(self, "manifest_path", Path(self.manifest_path))


@dataclass(frozen=True, slots=True)
class ValidationExecutionRequest:
    """Bounded execution inputs for a plan returned by :func:`plan_validation`."""

    manifest_path: Path = DEFAULT_MANIFEST
    adapter_bindings_path: Path = DEFAULT_ADAPTER_BINDINGS
    receipt_root: Path = DEFAULT_RECEIPT_ROOT
    max_workers: int = 4
    run_id: str | None = None
    mutation_root: Path | None = None
    allowed_mutation_globs: tuple[str, ...] = ()
    max_stabilization_passes: int = 3

    def __post_init__(self) -> None:
        object.__setattr__(self, "manifest_path", Path(self.manifest_path))
        object.__setattr__(
            self,
            "adapter_bindings_path",
            Path(self.adapter_bindings_path),
        )
        object.__setattr__(self, "receipt_root", Path(self.receipt_root))
        if self.mutation_root is not None:
            object.__setattr__(self, "mutation_root", Path(self.mutation_root))
        object.__setattr__(
            self,
            "allowed_mutation_globs",
            _tuple_of_nonblank_strings(
                self.allowed_mutation_globs,
                "allowed_mutation_globs",
            ),
        )


def plan_validation(request: ValidationPlanRequest) -> ValidationPlan:
    """Build one deterministic validation plan without executing commands.

    Configuration and I/O failures raise :class:`ValidationApiError`, whose
    status is ``BLOCKED_CONFIGURATION`` and whose exit code is ``2``.
    """

    if not isinstance(request, ValidationPlanRequest):
        raise ValidationApiError("request must be a ValidationPlanRequest")
    try:
        classification = classify_paths(request.paths)
        return build_plan(
            load_manifest(request.manifest_path),
            classification,
            profile=request.profile,
            scopes=request.scopes,
            role_obligations=request.role_obligations,
        )
    except (OSError, RuntimeError, PlannerError) as error:
        raise ValidationApiError(str(error)) from error


def plan_exit_code(plan: ValidationPlan) -> int:
    """Return ``0`` for a ready plan and ``2`` for blocked configuration."""

    if not isinstance(plan, ValidationPlan):
        raise ValidationApiError("plan must be a ValidationPlan")
    return 0 if plan.status == "READY" else 2


def execute_validation(
    plan: ValidationPlan,
    request: ValidationExecutionRequest | None = None,
) -> ExecutionOutcome:
    """Execute one validated plan through the tracked adapter bindings.

    The returned outcome preserves executor exit codes: ``0`` for PASS/WARN,
    ``1`` for validation failure, and ``2`` for blocked configuration.  An API
    setup error raises :class:`ValidationApiError` with exit code ``2``.
    """

    if not isinstance(plan, ValidationPlan):
        raise ValidationApiError("plan must be a ValidationPlan")
    selected = request or ValidationExecutionRequest()
    if not isinstance(selected, ValidationExecutionRequest):
        raise ValidationApiError("request must be a ValidationExecutionRequest")
    try:
        manifest = load_manifest(selected.manifest_path)
        adapters = load_adapters(selected.adapter_bindings_path, manifest)
        return execute_plan(
            plan,
            manifest,
            adapters,
            receipt_root=selected.receipt_root,
            max_workers=selected.max_workers,
            run_id=selected.run_id,
            mutation_root=selected.mutation_root,
            allowed_mutation_globs=selected.allowed_mutation_globs,
            max_stabilization_passes=selected.max_stabilization_passes,
        )
    except (OSError, PlannerError, ExecutorError) as error:
        raise ValidationApiError(str(error)) from error


__all__ = [
    "DEFAULT_ADAPTER_BINDINGS",
    "DEFAULT_MANIFEST",
    "DEFAULT_RECEIPT_ROOT",
    "ValidationApiError",
    "ValidationExecutionRequest",
    "ValidationPlanRequest",
    "execute_validation",
    "plan_exit_code",
    "plan_validation",
]
