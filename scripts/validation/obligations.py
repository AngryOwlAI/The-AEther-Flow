#!/usr/bin/env python3
"""Compile role and skill declarations into operational validation obligations.

The compiler is pure: it reads declared control sources and returns deterministic
requirements.  It does not execute gates, change role authority, activate
supersedence, or confer scientific, ontology, proof, benchmark, or Gate Chair
authority.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = REPO_ROOT / "research_control/design/validation_obligation_catalog_v1.yaml"
DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_ROLE_REGISTRY = REPO_ROOT / "registries/AGENT_ROLE_REGISTRY.csv"
SCOPES = {"working", "staged", "repository", "commit", "local_retrieval"}
SOURCE_TYPES = {"registered_role", "skill", "task_overlay", "profile", "changed_paths"}
PASS_STATUSES = {"PASS", "CACHE_HIT"}
SAME_SCOPE_PREDICATES = {
    "rc_diff_satisfies_core_same_scope_v1",
    "rc_diff_satisfies_claim_language_same_scope_v1",
}
ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[_:.-][a-z0-9]+)*$")
BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")


class ObligationError(ValueError):
    """Fail-closed declaration or catalog error."""


def _duplicate_key(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ObligationError(f"duplicate catalog key: {key}")
        result[key] = value
    return result


def _load_json_document(path: Path, label: str) -> dict[str, object]:
    def reject_constant(value: str) -> None:
        raise ObligationError(f"{label} contains non-finite number: {value}")

    try:
        value = json.loads(
            Path(path).read_text(encoding="utf-8"),
            object_pairs_hook=_duplicate_key,
            parse_constant=reject_constant,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise ObligationError(f"{label} load failed: {error}") from error
    if not isinstance(value, dict):
        raise ObligationError(f"{label} must be an object")
    return value


def load_catalog(path: Path = DEFAULT_CATALOG) -> dict[str, object]:
    return _load_json_document(path, "obligation catalog")


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, object]:
    return _load_json_document(path, "gate manifest")


def _exact_fields(value: object, fields: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ObligationError(f"{label} must be an object")
    keys = set(value)
    if keys != fields:
        raise ObligationError(
            f"{label} fields differ: missing={sorted(fields - keys)} "
            f"unknown={sorted(keys - fields)}"
        )
    return value


def _string_list(value: object, label: str, *, nonempty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ObligationError(f"{label} must be an array of nonblank strings")
    if nonempty and not value:
        raise ObligationError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise ObligationError(f"{label} contains duplicates")
    return tuple(value)


def _catalog_parts(
    catalog: Mapping[str, object], manifest: Mapping[str, object]
) -> tuple[dict[str, dict[str, object]], dict[str, tuple[str, ...]]]:
    top = _exact_fields(
        catalog,
        {
            "schema_id",
            "schema_version",
            "catalog_id",
            "migration_epoch",
            "execution_authority",
            "authority",
            "evidence_identity_fields",
            "obligation_specs",
            "declaration_aliases",
            "skill_sources",
        },
        "catalog",
    )
    if top["schema_id"] != "validation_obligation_catalog_v1":
        raise ObligationError("unsupported obligation catalog schema_id")
    if top["schema_version"] != 1 or isinstance(top["schema_version"], bool):
        raise ObligationError("unsupported obligation catalog schema_version")
    if top["catalog_id"] != "validation-obligation-catalog-v1":
        raise ObligationError("unsupported obligation catalog_id")
    authority_pair = (top["migration_epoch"], top["execution_authority"])
    if authority_pair not in {
        ("shadow_planner", "legacy"),
        ("planner_authoritative", "manifest_planner"),
    }:
        raise ObligationError("catalog has an unsupported migration authority pair")
    if authority_pair != (
        manifest.get("migration_epoch"),
        manifest.get("execution_authority"),
    ):
        raise ObligationError("catalog and manifest migration authority differ")
    authority = _exact_fields(
        top["authority"],
        {
            "operational_validation_only",
            "source_authoritative",
            "physics_claim_authority",
            "ontology_authority",
            "proof_authority",
            "benchmark_authority",
            "gate_chair_authority",
        },
        "catalog.authority",
    )
    expected_authority = {key: False for key in authority}
    expected_authority["operational_validation_only"] = True
    if authority != expected_authority:
        raise ObligationError("catalog authority changes the non-promotion boundary")
    identity_fields = _string_list(top["evidence_identity_fields"], "evidence fields")
    if identity_fields != (
        "tree_hash",
        "scope",
        "path_set_hash",
        "configuration_hash",
        "generation_state",
    ):
        raise ObligationError("evidence identity fields differ from the v1 contract")

    raw_gates = manifest.get("gates")
    if not isinstance(raw_gates, list) or not raw_gates:
        raise ObligationError("gate manifest must contain gates")
    manifest_gates: dict[str, dict[str, object]] = {}
    for raw_gate in raw_gates:
        if not isinstance(raw_gate, dict) or not isinstance(raw_gate.get("gate_id"), str):
            raise ObligationError("gate manifest contains a malformed gate")
        gate_id = str(raw_gate["gate_id"])
        if gate_id in manifest_gates:
            raise ObligationError(f"duplicate manifest gate: {gate_id}")
        manifest_gates[gate_id] = raw_gate

    raw_specs = top["obligation_specs"]
    if not isinstance(raw_specs, list) or not raw_specs:
        raise ObligationError("obligation_specs must be a nonempty array")
    specs: dict[str, dict[str, object]] = {}
    for index, raw_spec in enumerate(raw_specs):
        spec = _exact_fields(
            raw_spec,
            {"obligation_id", "description", "default_scope", "satisfying_gates"},
            f"obligation_specs[{index}]",
        )
        obligation_id = spec["obligation_id"]
        if not isinstance(obligation_id, str) or not ID_RE.fullmatch(obligation_id):
            raise ObligationError(f"obligation_specs[{index}] has invalid obligation_id")
        if obligation_id in specs:
            raise ObligationError(f"duplicate obligation_id: {obligation_id}")
        if not isinstance(spec["description"], str) or not spec["description"].strip():
            raise ObligationError(f"{obligation_id} has blank description")
        if spec["default_scope"] not in SCOPES:
            raise ObligationError(f"{obligation_id} has unsupported default_scope")
        mappings = spec["satisfying_gates"]
        if not isinstance(mappings, list) or not mappings:
            raise ObligationError(f"{obligation_id} has no satisfying gates")
        seen_mappings: set[tuple[str, tuple[str, ...], str | None]] = set()
        for mapping_index, raw_mapping in enumerate(mappings):
            mapping = _exact_fields(
                raw_mapping,
                {"gate_id", "allowed_scopes", "predicate_id"},
                f"{obligation_id}.satisfying_gates[{mapping_index}]",
            )
            gate_id = mapping["gate_id"]
            if not isinstance(gate_id, str) or gate_id not in manifest_gates:
                raise ObligationError(f"{obligation_id} references unknown gate {gate_id}")
            scopes = _string_list(mapping["allowed_scopes"], f"{obligation_id} scopes")
            if not set(scopes) <= SCOPES:
                raise ObligationError(f"{obligation_id} has unsupported satisfying scope")
            manifest_scopes = set(manifest_gates[gate_id].get("scopes", []))
            if not set(scopes) <= manifest_scopes:
                raise ObligationError(f"{gate_id} cannot satisfy declared scopes {scopes}")
            predicate = mapping["predicate_id"]
            if predicate is not None and predicate not in SAME_SCOPE_PREDICATES:
                raise ObligationError(f"{obligation_id} has unsupported predicate {predicate}")
            if predicate is None and obligation_id not in set(
                manifest_gates[gate_id].get("satisfies_obligations", [])
            ):
                raise ObligationError(
                    f"{gate_id} does not directly satisfy {obligation_id}"
                )
            key = (gate_id, tuple(scopes), predicate)
            if key in seen_mappings:
                raise ObligationError(f"{obligation_id} repeats a satisfying gate mapping")
            seen_mappings.add(key)
        if not any(spec["default_scope"] in item[1] for item in seen_mappings):
            raise ObligationError(f"{obligation_id} default scope has no satisfying gate")
        specs[obligation_id] = spec

    aliases: dict[str, tuple[str, ...]] = {}
    raw_aliases = top["declaration_aliases"]
    if not isinstance(raw_aliases, list):
        raise ObligationError("declaration_aliases must be an array")
    for index, raw_alias in enumerate(raw_aliases):
        alias = _exact_fields(
            raw_alias, {"label", "obligation_ids"}, f"declaration_aliases[{index}]"
        )
        label = alias["label"]
        if not isinstance(label, str) or not label.strip() or label in aliases:
            raise ObligationError(f"invalid or duplicate declaration alias: {label}")
        ids = _string_list(alias["obligation_ids"], f"alias {label}")
        unknown = set(ids) - set(specs)
        if unknown:
            raise ObligationError(f"alias {label} references unknown obligations {sorted(unknown)}")
        aliases[label] = ids

    raw_skills = top["skill_sources"]
    if not isinstance(raw_skills, list) or not raw_skills:
        raise ObligationError("skill_sources must be a nonempty array")
    skill_ids: set[str] = set()
    for index, raw_skill in enumerate(raw_skills):
        skill = _exact_fields(
            raw_skill, {"source_id", "path", "declarations"}, f"skill_sources[{index}]"
        )
        source_id = skill["source_id"]
        path = skill["path"]
        if not isinstance(source_id, str) or not source_id.strip() or source_id in skill_ids:
            raise ObligationError(f"invalid or duplicate skill source_id: {source_id}")
        if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
            raise ObligationError(f"skill {source_id} has invalid path")
        declarations = _string_list(skill["declarations"], f"skill {source_id}")
        if set(declarations) - set(specs):
            raise ObligationError(f"skill {source_id} declares an unknown obligation")
        skill_ids.add(source_id)
    return specs, aliases


@dataclass(frozen=True, slots=True)
class EvidenceContext:
    tree_hash: str
    path_set_hash: str
    configuration_hash: str
    generation_state: str

    def __post_init__(self) -> None:
        for field in ("tree_hash", "path_set_hash", "configuration_hash", "generation_state"):
            if not isinstance(getattr(self, field), str) or not getattr(self, field).strip():
                raise ObligationError(f"evidence context {field} must be nonblank")


@dataclass(frozen=True, slots=True)
class Declaration:
    source_type: str
    source_id: str
    label: str
    scope: str | None = None

    def __post_init__(self) -> None:
        if self.source_type not in SOURCE_TYPES:
            raise ObligationError(f"unsupported declaration source_type: {self.source_type}")
        if not self.source_id or not self.label:
            raise ObligationError("declaration source_id and label must be nonblank")
        if self.scope is not None and self.scope not in SCOPES:
            raise ObligationError(f"unsupported declaration scope: {self.scope}")


@dataclass(frozen=True, slots=True)
class ObligationRequirement:
    obligation_id: str
    scope: str
    evidence_context: EvidenceContext
    satisfying_gates: tuple[dict[str, object], ...]
    required_by: tuple[str, ...]

    @property
    def evidence_identity(self) -> dict[str, str]:
        return {
            "tree_hash": self.evidence_context.tree_hash,
            "scope": self.scope,
            "path_set_hash": self.evidence_context.path_set_hash,
            "configuration_hash": self.evidence_context.configuration_hash,
            "generation_state": self.evidence_context.generation_state,
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "obligation_id": self.obligation_id,
            "evidence_identity": self.evidence_identity,
            "satisfying_gates": list(self.satisfying_gates),
            "required_by": list(self.required_by),
        }


def active_role_declarations(role_registry: Path = DEFAULT_ROLE_REGISTRY) -> tuple[Declaration, ...]:
    try:
        with Path(role_registry).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        raise ObligationError(f"role registry load failed: {error}") from error
    declarations: list[Declaration] = []
    active_ids: set[str] = set()
    for row in rows:
        if row.get("status") != "active":
            continue
        source_id = f"{row.get('role_id', '')}@{row.get('version', '')}"
        if source_id in active_ids:
            raise ObligationError(f"duplicate active role: {source_id}")
        active_ids.add(source_id)
        labels = [label for label in row.get("default_validators", "").split(";") if label]
        if not labels:
            raise ObligationError(f"active role {source_id} has no validator declaration")
        declarations.extend(
            Declaration("registered_role", source_id, label) for label in labels
        )
    if not declarations:
        raise ObligationError("role registry has no active validator declarations")
    return tuple(declarations)


def skill_declarations(
    catalog: Mapping[str, object], repo_root: Path = REPO_ROOT
) -> tuple[Declaration, ...]:
    raw_sources = catalog.get("skill_sources")
    if not isinstance(raw_sources, list):
        raise ObligationError("catalog skill_sources must be an array")
    declarations: list[Declaration] = []
    for raw_source in raw_sources:
        if not isinstance(raw_source, dict):
            raise ObligationError("catalog skill source must be an object")
        source_id = raw_source.get("source_id")
        path = raw_source.get("path")
        labels = raw_source.get("declarations")
        if not isinstance(source_id, str) or not isinstance(path, str) or not isinstance(labels, list):
            raise ObligationError("catalog skill source is malformed")
        try:
            text = (Path(repo_root) / path).read_text(encoding="utf-8")
        except OSError as error:
            raise ObligationError(f"skill source load failed for {source_id}: {error}") from error
        tokens = set(BACKTICK_TOKEN_RE.findall(text))
        for label in labels:
            if not isinstance(label, str) or label not in tokens:
                raise ObligationError(f"skill {source_id} does not declare `{label}`")
            declarations.append(Declaration("skill", source_id, label))
    return tuple(declarations)


def compile_declarations(
    catalog: Mapping[str, object],
    manifest: Mapping[str, object],
    declarations: Iterable[Declaration],
    evidence_context: EvidenceContext,
) -> tuple[ObligationRequirement, ...]:
    """Resolve the union of declarations; no source may weaken another source."""

    specs, aliases = _catalog_parts(catalog, manifest)
    grouped: dict[tuple[str, str], set[str]] = {}
    for declaration in declarations:
        if not isinstance(declaration, Declaration):
            raise ObligationError("declarations must contain Declaration values")
        if declaration.label in aliases:
            obligation_ids = aliases[declaration.label]
        elif declaration.label in specs:
            obligation_ids = (declaration.label,)
        else:
            raise ObligationError(
                f"unmapped declaration {declaration.label!r} from {declaration.source_id}"
            )
        for obligation_id in obligation_ids:
            spec = specs[obligation_id]
            scope = declaration.scope or str(spec["default_scope"])
            mappings = tuple(
                {
                    "gate_id": str(mapping["gate_id"]),
                    "allowed_scopes": sorted(mapping["allowed_scopes"]),
                    "predicate_id": mapping["predicate_id"],
                }
                for mapping in spec["satisfying_gates"]
                if scope in mapping["allowed_scopes"]
            )
            if not mappings:
                raise ObligationError(
                    f"{obligation_id} has no satisfying gate for scope {scope}"
                )
            grouped.setdefault((obligation_id, scope), set()).add(
                f"{declaration.source_type}:{declaration.source_id}:{declaration.label}"
            )
    requirements: list[ObligationRequirement] = []
    for obligation_id, scope in sorted(grouped):
        spec = specs[obligation_id]
        mappings = tuple(
            {
                "gate_id": str(mapping["gate_id"]),
                "allowed_scopes": sorted(mapping["allowed_scopes"]),
                "predicate_id": mapping["predicate_id"],
            }
            for mapping in spec["satisfying_gates"]
            if scope in mapping["allowed_scopes"]
        )
        requirements.append(
            ObligationRequirement(
                obligation_id,
                scope,
                evidence_context,
                mappings,
                tuple(sorted(grouped[(obligation_id, scope)])),
            )
        )
    return tuple(requirements)


def _receipt_matches(
    requirement: ObligationRequirement, receipt: Mapping[str, object]
) -> bool:
    if receipt.get("status") not in PASS_STATUSES:
        return False
    if any(receipt.get(field) != value for field, value in requirement.evidence_identity.items()):
        return False
    predicates = receipt.get("satisfied_predicates", [])
    if not isinstance(predicates, list) or any(not isinstance(item, str) for item in predicates):
        raise ObligationError("receipt satisfied_predicates must be a string array")
    for mapping in requirement.satisfying_gates:
        if receipt.get("gate_id") != mapping["gate_id"]:
            continue
        predicate = mapping["predicate_id"]
        if predicate is None or predicate in predicates:
            return True
    return False


def annotate_satisfaction(
    requirements: Sequence[ObligationRequirement],
    receipts: Iterable[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    """Return receipts annotated with same-identity obligations they satisfy."""

    results: list[dict[str, object]] = []
    for receipt in receipts:
        if not isinstance(receipt, Mapping):
            raise ObligationError("receipts must be mappings")
        satisfied = [
            {
                "obligation_id": requirement.obligation_id,
                "required_by": list(requirement.required_by),
            }
            for requirement in requirements
            if _receipt_matches(requirement, receipt)
        ]
        annotated = dict(receipt)
        annotated["satisfied_obligations"] = sorted(
            satisfied, key=lambda item: str(item["obligation_id"])
        )
        results.append(annotated)
    return tuple(results)


def _source_fingerprint(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted((Path(path) for path in paths), key=lambda item: str(item)):
        digest.update(str(path.relative_to(REPO_ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def audit_repository(
    catalog_path: Path = DEFAULT_CATALOG,
    manifest_path: Path = DEFAULT_MANIFEST,
    role_registry: Path = DEFAULT_ROLE_REGISTRY,
    repo_root: Path = REPO_ROOT,
) -> dict[str, object]:
    catalog = load_catalog(catalog_path)
    manifest = load_manifest(manifest_path)
    role_decls = active_role_declarations(role_registry)
    skill_decls = skill_declarations(catalog, repo_root)
    skill_paths = [repo_root / str(item["path"]) for item in catalog["skill_sources"]]
    fingerprint = _source_fingerprint(
        [catalog_path, manifest_path, role_registry, *skill_paths]
    )
    context = EvidenceContext(
        tree_hash=f"source-sha256:{fingerprint}",
        path_set_hash=f"source-sha256:{fingerprint}",
        configuration_hash=f"source-sha256:{fingerprint}",
        generation_state="precheckpoint",
    )
    requirements = compile_declarations(
        catalog, manifest, (*role_decls, *skill_decls), context
    )
    active_roles = sorted({declaration.source_id for declaration in role_decls})
    skills = sorted({declaration.source_id for declaration in skill_decls})
    return {
        "schema_id": "validation_obligation_resolution_audit_v1",
        "status": "PASS",
        "catalog_id": catalog["catalog_id"],
        "migration_epoch": catalog["migration_epoch"],
        "execution_authority": catalog["execution_authority"],
        "source_fingerprint": fingerprint,
        "active_role_count": len(active_roles),
        "active_roles": active_roles,
        "skill_count": len(skills),
        "skills": skills,
        "role_declaration_count": len(role_decls),
        "skill_declaration_count": len(skill_decls),
        "resolved_declaration_count": sum(
            len(requirement.required_by) for requirement in requirements
        ),
        "compiled_requirement_count": len(requirements),
        "unmapped_declaration_count": 0,
        "requirements": [requirement.to_dict() for requirement in requirements],
        "authority": {
            "operational_validation_only": True,
            "legacy_execution_authoritative": True,
            "role_authority_changed": False,
            "scientific_claims_changed": False,
            "physics_claim_authority": False,
            "ontology_authority": False,
            "proof_authority": False,
            "benchmark_authority": False,
            "gate_chair_authority": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    audit = subcommands.add_parser("audit", help="audit active role and skill declarations")
    audit.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    audit.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    audit.add_argument("--role-registry", type=Path, default=DEFAULT_ROLE_REGISTRY)
    audit.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = audit_repository(args.catalog, args.manifest, args.role_registry)
    except (OSError, ObligationError) as error:
        print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":") if args.json else None,
            indent=None if args.json else 2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
