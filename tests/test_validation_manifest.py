from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
CATALOG_PATH = ROOT / "research_control/design/validation_gate_id_catalog_v1.md"
LEGACY_GRAPH_PATH = ROOT / "research_control/design/v19_legacy_validation_invocation_graph.json"
LEGACY_COVERAGE_FIXTURE_PATH = (
    ROOT / "tests/fixtures/validation_manifest/legacy_gate_coverage_v1.json"
)

TOP_LEVEL_FIELDS = {
    "schema_id",
    "schema_version",
    "manifest_id",
    "migration_epoch",
    "population_status",
    "execution_authority",
    "authority",
    "gates",
}
AUTHORITY_FIELDS = {
    "benchmark_authority",
    "gate_chair_authority",
    "ontology_authority",
    "operational_validation_only",
    "physics_claim_authority",
    "proof_authority",
    "source_authoritative",
}
GATE_FIELDS = {
    "gate_id",
    "description",
    "owner_role",
    "adapter",
    "command_compatibility",
    "input_globs",
    "output_globs",
    "global_invariant_justification",
    "scopes",
    "severity",
    "mutating",
    "cost_class",
    "prerequisites",
    "supersedes",
    "satisfies_obligations",
    "profiles",
    "path_tags",
    "selection",
    "timeout_seconds",
    "parallel_group",
    "cache_policy",
    "receipt_schema",
    "test_shard",
}
SCOPES = {"working", "staged", "commit", "repository", "local_retrieval"}
SEVERITIES = {"blocking", "advisory", "local_only"}
PROFILES = {"fast", "affected", "checkpoint", "full", "doctor"}
COST_CLASSES = {"fast", "medium", "slow"}
CACHE_POLICIES = {"ineligible", "exact_tree", "scheduled_bypass"}
MIGRATION_EPOCHS = {
    "legacy",
    "legacy_consolidated",
    "shadow_planner",
    "planner_authoritative",
    "legacy_retired",
}
CONDITION_KINDS = {
    "always",
    "profile_selected",
    "path_tag_any",
    "path_tag_all",
    "explicit_scope",
    "changed_registered_tex_pdf_required",
    "registered_mermaid_changed",
    "publication_surface_changed",
    "graph_inputs_changed",
    "task_index_inputs_changed",
    "traceability_inputs_changed",
    "scientific_checker_family",
}
ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[_:.-][a-z0-9]+)*$")
CATALOG_ROW_RE = re.compile(r"^\| `([^`]+)` \| `(LVG-\d{3})` \|")


class ManifestError(ValueError):
    pass


def canonical_manifest_bytes(manifest: dict[str, object]) -> bytes:
    return json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_manifest_sha256(manifest: dict[str, object]) -> str:
    return hashlib.sha256(canonical_manifest_bytes(manifest)).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError(f"duplicate object key: {key}")
        result[key] = value
    return result


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, object]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )


def require_exact_keys(value: object, expected: set[str], context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ManifestError(f"{context} must be an object")
    keys = set(value)
    if keys != expected:
        raise ManifestError(
            f"{context} fields differ: missing={sorted(expected - keys)} "
            f"unknown={sorted(keys - expected)}"
        )
    return value


def require_nonblank(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{context} must be a nonblank string")
    return value


def require_unique_strings(
    value: object,
    context: str,
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ManifestError(f"{context} must be a string array")
    if nonempty and not value:
        raise ManifestError(f"{context} must not be empty")
    if len(value) != len(set(value)):
        raise ManifestError(f"{context} must not contain duplicates")
    return value


def validate_glob(value: str, context: str) -> None:
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise ManifestError(f"{context} is not a normalized repository-relative glob")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ManifestError(f"{context} contains an invalid path segment")


def validate_manifest(manifest: object) -> None:
    document = require_exact_keys(manifest, TOP_LEVEL_FIELDS, "manifest")
    if document["schema_id"] != "validation_gate_manifest_v1":
        raise ManifestError("unsupported manifest schema_id")
    if document["schema_version"] != 1 or isinstance(document["schema_version"], bool):
        raise ManifestError("unsupported manifest schema_version")
    if document["manifest_id"] != "validation-gate-manifest-v1":
        raise ManifestError("unsupported manifest_id")
    if document["migration_epoch"] not in MIGRATION_EPOCHS:
        raise ManifestError("unsupported migration_epoch")
    if document["population_status"] not in {"schema_seed_pending_p5_t02", "populated"}:
        raise ManifestError("unsupported population_status")
    if document["execution_authority"] not in {"legacy", "manifest_planner"}:
        raise ManifestError("unsupported execution_authority")

    authority = require_exact_keys(document["authority"], AUTHORITY_FIELDS, "authority")
    expected_authority = {field: False for field in AUTHORITY_FIELDS}
    expected_authority["operational_validation_only"] = True
    if authority != expected_authority:
        raise ManifestError("authority must preserve the schema-v1 non-promotion boundary")

    gates = document["gates"]
    if not isinstance(gates, list):
        raise ManifestError("gates must be an array")
    if document["population_status"] == "schema_seed_pending_p5_t02":
        if gates or document["execution_authority"] != "legacy":
            raise ManifestError("the P5-T01 seed must be empty and legacy-authoritative")
        return
    if not gates:
        raise ManifestError("a populated manifest must contain at least one gate")

    gate_ids: list[str] = []
    for index, raw_gate in enumerate(gates):
        context = f"gates[{index}]"
        gate = require_exact_keys(raw_gate, GATE_FIELDS, context)
        gate_id = require_nonblank(gate["gate_id"], f"{context}.gate_id")
        if not ID_RE.fullmatch(gate_id):
            raise ManifestError(f"{context}.gate_id is not a stable lowercase ID")
        gate_ids.append(gate_id)
        for field in ("description", "owner_role", "adapter", "parallel_group", "test_shard"):
            require_nonblank(gate[field], f"{context}.{field}")

        command_compatibility = require_unique_strings(
            gate["command_compatibility"], f"{context}.command_compatibility", nonempty=True
        )
        for command_index, command in enumerate(command_compatibility):
            require_nonblank(command, f"{context}.command_compatibility[{command_index}]")

        broad_glob = False
        for field in ("input_globs", "output_globs"):
            globs = require_unique_strings(gate[field], f"{context}.{field}")
            for glob_index, glob in enumerate(globs):
                validate_glob(glob, f"{context}.{field}[{glob_index}]")
                broad_glob = broad_glob or glob == "**" or glob.startswith("**/")
        justification = gate["global_invariant_justification"]
        if justification is not None and not isinstance(justification, str):
            raise ManifestError(f"{context}.global_invariant_justification must be string or null")
        if broad_glob and (not isinstance(justification, str) or not justification.strip()):
            raise ManifestError(f"{context} uses a global glob without audited justification")

        scopes = require_unique_strings(gate["scopes"], f"{context}.scopes", nonempty=True)
        if not set(scopes) <= SCOPES:
            raise ManifestError(f"{context}.scopes contains an unsupported scope")
        if gate["severity"] not in SEVERITIES:
            raise ManifestError(f"{context}.severity is unsupported")
        if not isinstance(gate["mutating"], bool):
            raise ManifestError(f"{context}.mutating must be boolean")
        if gate["cost_class"] not in COST_CLASSES:
            raise ManifestError(f"{context}.cost_class is unsupported")

        require_unique_strings(gate["prerequisites"], f"{context}.prerequisites")
        require_unique_strings(
            gate["satisfies_obligations"],
            f"{context}.satisfies_obligations",
            nonempty=True,
        )
        profiles = require_unique_strings(gate["profiles"], f"{context}.profiles", nonempty=True)
        if not set(profiles) <= PROFILES:
            raise ManifestError(f"{context}.profiles contains an unsupported profile")
        require_unique_strings(gate["path_tags"], f"{context}.path_tags")

        selection = require_exact_keys(gate["selection"], {"operator", "conditions"}, f"{context}.selection")
        if selection["operator"] not in {"all", "any"}:
            raise ManifestError(f"{context}.selection.operator is unsupported")
        conditions = selection["conditions"]
        if not isinstance(conditions, list) or not conditions:
            raise ManifestError(f"{context}.selection.conditions must be nonempty")
        condition_ids: list[str] = []
        for condition_index, raw_condition in enumerate(conditions):
            condition_context = f"{context}.selection.conditions[{condition_index}]"
            condition = require_exact_keys(
                raw_condition,
                {"condition_id", "kind", "values"},
                condition_context,
            )
            condition_id = require_nonblank(condition["condition_id"], f"{condition_context}.condition_id")
            if not ID_RE.fullmatch(condition_id):
                raise ManifestError(f"{condition_context}.condition_id is invalid")
            condition_ids.append(condition_id)
            if condition["kind"] not in CONDITION_KINDS:
                raise ManifestError(f"{condition_context}.kind is unsupported")
            values = require_unique_strings(condition["values"], f"{condition_context}.values")
            if condition["kind"] == "always" and values:
                raise ManifestError(f"{condition_context}.values must be empty for always")
            if condition["kind"] != "always" and not values:
                raise ManifestError(f"{condition_context}.values must be nonempty")
        if len(condition_ids) != len(set(condition_ids)):
            raise ManifestError(f"{context}.selection condition IDs must be unique")

        if (
            not isinstance(gate["timeout_seconds"], int)
            or isinstance(gate["timeout_seconds"], bool)
            or not 1 <= gate["timeout_seconds"] <= 86400
        ):
            raise ManifestError(f"{context}.timeout_seconds is invalid")
        if gate["cache_policy"] not in CACHE_POLICIES:
            raise ManifestError(f"{context}.cache_policy is unsupported")
        if gate["receipt_schema"] != "validation_gate_result_v1":
            raise ManifestError(f"{context}.receipt_schema is unsupported")
        if not isinstance(gate["supersedes"], list):
            raise ManifestError(f"{context}.supersedes must be an array")

    if len(gate_ids) != len(set(gate_ids)):
        raise ManifestError("gate IDs must be unique")
    known_ids = set(gate_ids)

    prerequisites: dict[str, list[str]] = {}
    for index, raw_gate in enumerate(gates):
        gate = raw_gate
        gate_id = gate["gate_id"]
        prerequisites[gate_id] = gate["prerequisites"]
        unknown = set(gate["prerequisites"]) - known_ids
        if unknown:
            raise ManifestError(f"{gate_id} has unknown prerequisites: {sorted(unknown)}")
        superseded_ids: list[str] = []
        for supersedes_index, raw_supersedence in enumerate(gate["supersedes"]):
            supersedence = require_exact_keys(
                raw_supersedence,
                {"gate_id", "predicate_id", "status"},
                f"gates[{index}].supersedes[{supersedes_index}]",
            )
            target = require_nonblank(supersedence["gate_id"], "supersedence.gate_id")
            predicate = require_nonblank(supersedence["predicate_id"], "supersedence.predicate_id")
            if target not in known_ids or target == gate_id:
                raise ManifestError(f"{gate_id} has invalid supersedence target {target}")
            if not ID_RE.fullmatch(predicate):
                raise ManifestError(f"{gate_id} has invalid supersedence predicate")
            if supersedence["status"] not in {"policy_only_inactive", "active"}:
                raise ManifestError(f"{gate_id} has invalid supersedence status")
            superseded_ids.append(target)
        if len(superseded_ids) != len(set(superseded_ids)):
            raise ManifestError(f"{gate_id} has duplicate supersedence targets")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(gate_id: str) -> None:
        if gate_id in visiting:
            raise ManifestError("prerequisite graph contains a cycle")
        if gate_id in visited:
            return
        visiting.add(gate_id)
        for prerequisite in prerequisites[gate_id]:
            visit(prerequisite)
        visiting.remove(gate_id)
        visited.add(gate_id)

    for gate_id in gate_ids:
        visit(gate_id)


def gate_fixture(gate_id: str = "manifest_contract_test") -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "description": "Validate one manifest contract fixture.",
        "owner_role": "project-control-maintainer@0.2.0",
        "adapter": "compatibility:test_validation_manifest",
        "command_compatibility": ["python -m unittest tests/test_validation_manifest.py"],
        "input_globs": ["research_control/design/validation_gate_manifest_v1.yaml"],
        "output_globs": [],
        "global_invariant_justification": None,
        "scopes": ["repository"],
        "severity": "blocking",
        "mutating": False,
        "cost_class": "fast",
        "prerequisites": [],
        "supersedes": [],
        "satisfies_obligations": ["validation_manifest_schema_tests"],
        "profiles": ["full"],
        "path_tags": ["schema_contract"],
        "selection": {
            "operator": "all",
            "conditions": [{"condition_id": "always", "kind": "always", "values": []}],
        },
        "timeout_seconds": 600,
        "parallel_group": "schema_contracts",
        "cache_policy": "ineligible",
        "receipt_schema": "validation_gate_result_v1",
        "test_shard": "tests/test_validation_manifest.py",
    }


def populated_manifest(*gates: dict[str, object]) -> dict[str, object]:
    manifest = load_manifest()
    manifest["population_status"] = "populated"
    manifest["gates"] = list(gates)
    return manifest


class ManifestContractTests(unittest.TestCase):
    def test_canonical_manifest_is_populated_and_legacy_authoritative(self) -> None:
        manifest = load_manifest()
        validate_manifest(manifest)
        self.assertEqual(len(manifest["gates"]), 37)
        self.assertEqual(manifest["population_status"], "populated")
        self.assertEqual(manifest["execution_authority"], "legacy")
        self.assertTrue(all(gate["cache_policy"] == "ineligible" for gate in manifest["gates"]))
        self.assertTrue(
            all(
                item["status"] == "policy_only_inactive"
                for gate in manifest["gates"]
                for item in gate["supersedes"]
            )
        )

    def test_canonical_serialization_and_hash_are_key_order_independent(self) -> None:
        manifest = populated_manifest(gate_fixture())
        reordered = dict(reversed(list(manifest.items())))
        self.assertEqual(canonical_manifest_bytes(manifest), canonical_manifest_bytes(reordered))
        self.assertEqual(canonical_manifest_sha256(manifest), canonical_manifest_sha256(reordered))
        self.assertRegex(canonical_manifest_sha256(manifest), r"^[0-9a-f]{64}$")

    def test_loader_rejects_duplicate_object_keys(self) -> None:
        with self.assertRaisesRegex(ManifestError, "duplicate object key"):
            json.loads(
                '{"schema_id":"first","schema_id":"second"}',
                object_pairs_hook=reject_duplicate_keys,
            )

    def test_profile_membership_is_independent_from_severity(self) -> None:
        gate = gate_fixture()
        gate["severity"] = "advisory"
        gate["profiles"] = ["checkpoint", "full"]
        validate_manifest(populated_manifest(gate))


class ManifestMalformedFixtureTests(unittest.TestCase):
    def assert_invalid(self, manifest: dict[str, object], phrase: str) -> None:
        with self.assertRaisesRegex(ManifestError, phrase):
            validate_manifest(manifest)

    def test_rejects_duplicate_ids_and_unknown_fields(self) -> None:
        gate = gate_fixture()
        self.assert_invalid(populated_manifest(gate, deepcopy(gate)), "unique")
        unknown = populated_manifest(gate_fixture())
        unknown["unexpected"] = True
        self.assert_invalid(unknown, "unknown")

    def test_rejects_unknown_prerequisite_and_prerequisite_cycle(self) -> None:
        unknown = gate_fixture("gate_a")
        unknown["prerequisites"] = ["missing_gate"]
        self.assert_invalid(populated_manifest(unknown), "unknown prerequisites")

        gate_a = gate_fixture("gate_a")
        gate_b = gate_fixture("gate_b")
        gate_a["prerequisites"] = ["gate_b"]
        gate_b["prerequisites"] = ["gate_a"]
        self.assert_invalid(populated_manifest(gate_a, gate_b), "cycle")

    def test_rejects_invalid_supersedence(self) -> None:
        gate_a = gate_fixture("gate_a")
        gate_b = gate_fixture("gate_b")
        gate_a["supersedes"] = [
            {
                "gate_id": "missing_gate",
                "predicate_id": "same_scope",
                "status": "policy_only_inactive",
            }
        ]
        self.assert_invalid(populated_manifest(gate_a, gate_b), "invalid supersedence target")

        self_target = gate_fixture("gate_a")
        self_target["supersedes"] = [
            {"gate_id": "gate_a", "predicate_id": "same_scope", "status": "active"}
        ]
        self.assert_invalid(populated_manifest(self_target), "invalid supersedence target")

    def test_rejects_unsupported_scope_missing_test_shard_and_broad_glob(self) -> None:
        unsupported_scope = gate_fixture()
        unsupported_scope["scopes"] = ["unstated"]
        self.assert_invalid(populated_manifest(unsupported_scope), "unsupported scope")

        missing_test = gate_fixture()
        missing_test["test_shard"] = ""
        self.assert_invalid(populated_manifest(missing_test), "nonblank")

        broad_glob = gate_fixture()
        broad_glob["input_globs"] = ["**"]
        self.assert_invalid(populated_manifest(broad_glob), "audited justification")
        broad_glob["global_invariant_justification"] = "Audited repository-wide invariant."
        validate_manifest(populated_manifest(broad_glob))


class LegacyRepresentabilityTests(unittest.TestCase):
    def test_canonical_manifest_exactly_covers_the_legacy_inventory(self) -> None:
        manifest = load_manifest()
        validate_manifest(manifest)
        coverage = json.loads(LEGACY_COVERAGE_FIXTURE_PATH.read_text(encoding="utf-8"))
        graph_bytes = LEGACY_GRAPH_PATH.read_bytes()
        graph = json.loads(graph_bytes)

        self.assertEqual(coverage["source_graph_sha256"], hashlib.sha256(graph_bytes).hexdigest())
        self.assertEqual(coverage["catalog_count"], 37)
        self.assertEqual(coverage["execution_authority"], "legacy")
        self.assertEqual(len(coverage["entries"]), 37)

        graph_by_id = {gate["gate_id"]: gate for gate in graph["gate_catalog"]}
        manifest_by_id = {gate["gate_id"]: gate for gate in manifest["gates"]}
        expected_ids = {entry["canonical_gate_id"] for entry in coverage["entries"]}
        self.assertEqual(set(manifest_by_id), expected_ids)

        for entry in coverage["entries"]:
            legacy_gate = graph_by_id[entry["legacy_gate_id"]]
            gate = manifest_by_id[entry["canonical_gate_id"]]
            self.assertEqual(entry["legacy_name"], legacy_gate["name"])
            self.assertEqual(entry["authority"], legacy_gate["authority"])
            self.assertEqual(entry["mutating"], legacy_gate["mutating"])
            self.assertEqual(entry["implementation"], legacy_gate["implementation"])
            self.assertEqual(gate["adapter"], f"legacy:{entry['legacy_gate_id'].lower()}")
            self.assertIn(entry["implementation"], gate["command_compatibility"])
            expected_severity = (
                "local_only"
                if entry["authority"] == "local_only"
                else "advisory"
                if entry["authority"] in {"advisory", "diagnostic", "routing"}
                else "blocking"
            )
            self.assertEqual(gate["severity"], expected_severity)
            self.assertEqual(gate["mutating"], entry["mutating"])
            self.assertEqual(gate["cache_policy"], "ineligible")
            self.assertEqual(
                gate["test_shard"],
                "tests/fixtures/validation_manifest/legacy_gate_coverage_v1.json",
            )

    def test_all_37_legacy_nodes_are_representable(self) -> None:
        catalog_map = {}
        for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines():
            match = CATALOG_ROW_RE.match(line)
            if match:
                canonical_id, legacy_id = match.groups()
                catalog_map[legacy_id] = canonical_id
        graph = json.loads(LEGACY_GRAPH_PATH.read_text(encoding="utf-8"))
        legacy_gates = graph["gate_catalog"]

        self.assertEqual(len(catalog_map), 37)
        self.assertEqual(len(legacy_gates), 37)
        self.assertEqual(set(catalog_map), {gate["gate_id"] for gate in legacy_gates})

        represented = []
        for legacy_gate in legacy_gates:
            gate = gate_fixture(catalog_map[legacy_gate["gate_id"]])
            gate["description"] = f"Legacy representability fixture for {legacy_gate['name']}."
            gate["adapter"] = f"compatibility:{legacy_gate['gate_id'].lower()}"
            gate["command_compatibility"] = [legacy_gate["implementation"]]
            authority = legacy_gate["authority"]
            gate["severity"] = (
                "local_only"
                if authority == "local_only"
                else "advisory"
                if authority in {"advisory", "diagnostic", "routing"}
                else "blocking"
            )
            gate["mutating"] = legacy_gate["mutating"]
            gate["satisfies_obligations"] = [catalog_map[legacy_gate["gate_id"]]]
            gate["path_tags"] = ["legacy_inventory"]
            gate["test_shard"] = "full_profile_acceptance"
            represented.append(gate)

        manifest = populated_manifest(*represented)
        validate_manifest(manifest)
        self.assertEqual(len(manifest["gates"]), 37)


if __name__ == "__main__":
    unittest.main()
