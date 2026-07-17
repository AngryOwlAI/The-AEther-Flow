from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "render_dependency_graph",
        SCRIPT_DIR / "render_dependency_graph.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def freeze_value(value):
    if isinstance(value, dict):
        return MappingProxyType({key: freeze_value(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(freeze_value(item) for item in value)
    return value


def instrumentation_counts(instrumentation):
    return (
        instrumentation.source_loads,
        instrumentation.graph_builds,
        instrumentation.render_calls,
        tuple(sorted(instrumentation.renders_by_format.items())),
    )


class DependencyGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph_module = load_module()
        cls.shared_instrumentation = cls.graph_module.GraphInstrumentation()
        snapshot = cls.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in cls.graph_module.REGISTRY_SPECS
            ),
            instrumentation=cls.shared_instrumentation,
        )
        live_graph = cls.graph_module.build_graph(
            REPO_ROOT,
            snapshot=snapshot,
            instrumentation=cls.shared_instrumentation,
        )
        cls.shared_renders = MappingProxyType(
            {
                "json": cls.graph_module.render_json(live_graph, cls.shared_instrumentation),
                "markdown": cls.graph_module.render_markdown(live_graph, cls.shared_instrumentation),
                "dot": cls.graph_module.render_dot(live_graph, cls.shared_instrumentation),
            }
        )
        cls.shared_graph = freeze_value(live_graph)
        cls.shared_render_hashes = MappingProxyType(
            {
                name: hashlib.sha256(payload.encode("utf-8")).hexdigest()
                for name, payload in cls.shared_renders.items()
            }
        )
        cls.shared_counter_baseline = instrumentation_counts(cls.shared_instrumentation)
        cls.shared_freeze_summary = cls.graph_module.freeze_criteria_summary(
            {
                "repeated_burden": True,
                "freeze_evaluation_required": True,
                "active_freeze_label": "COUPLING-LAW-CANDIDATE-EVIDENCE-ACCEPTED",
                "candidate_freeze_label": "COUPLING-LAW-CANDIDATE-POST-EVIDENCE-CRITERIA-MISSING",
                "prior_attempts_considered": [
                    "RT-20260614-230",
                    "RT-20260614-231",
                ],
                "freeze_decision": "not_frozen",
                "next_allowed_route": "ontology_formalizer_positive_success_criteria",
            },
            "RT-20260614-235",
        )

    def tearDown(self) -> None:
        self.assertEqual(
            instrumentation_counts(self.shared_instrumentation),
            self.shared_counter_baseline,
            "a test triggered another shared source load, graph build, or render",
        )
        self.assertEqual(
            {
                name: hashlib.sha256(payload.encode("utf-8")).hexdigest()
                for name, payload in self.shared_renders.items()
            },
            self.shared_render_hashes,
            "a test mutated a shared rendered payload",
        )

    def assert_required_frontier_items(self, graph) -> None:
        labels = {node["label"] for node in graph["nodes"]}
        for required in (
            "Resp_lc",
            "M_src",
            "g_eff",
            "matter-coupling burden",
            "Einstein-equations burden",
            "benchmark-promotion burden",
            "finite toy metric response",
        ):
            self.assertIn(required, labels, f"required frontier node missing: {required}")
        for required_fragment in ("B_E", "BridgeCert", "SEI-MC", "SEI_src"):
            self.assertTrue(any(required_fragment in label for label in labels))

    def assert_authority_boundary(self, graph) -> None:
        boundary = graph["authority_boundary"]
        expected = {
            "navigational_support_only": True,
            "physics_claim_authority": False,
            "generated_graph_can_promote_claims": False,
        }
        for key, value in expected.items():
            self.assertIs(
                boundary[key],
                value,
                f"authority boundary mutated: {key} must remain {str(value).lower()}",
            )

    def assert_referential_integrity(self, graph) -> None:
        node_ids = {node["node_id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            for endpoint, kind in (("source_id", "source"), ("target_id", "target")):
                self.assertIn(
                    edge[endpoint],
                    node_ids,
                    f"edge {kind} missing: {edge[endpoint]}",
                )
            self.assertIn(edge["edge_class"], self.graph_module.EDGE_CLASSES)
            self.assertTrue(edge["source_path"])
            self.assertTrue(edge["source_field"])

    def test_shared_graph_includes_required_frontier_items(self) -> None:
        self.assert_required_frontier_items(self.shared_graph)

    def test_shared_graph_preserves_authority_boundary(self) -> None:
        self.assert_authority_boundary(self.shared_graph)

    def test_shared_graph_edges_reference_existing_nodes(self) -> None:
        self.assert_referential_integrity(self.shared_graph)

    def test_graph_rendering_is_deterministic_for_unchanged_state(self) -> None:
        for name, payload in self.shared_renders.items():
            self.assertEqual(
                hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                self.shared_render_hashes[name],
            )

    def test_shared_graph_formats_contain_required_content(self) -> None:
        json_graph = json.loads(self.shared_renders["json"])
        self.assertEqual(json_graph["schema_id"], "research_dependency_graph_v1")
        self.assertTrue(json_graph["authority_boundary"]["navigational_support_only"])
        self.assertIn("navigational support only", self.shared_renders["markdown"])
        self.assertIn("navigational_support_only", self.shared_renders["dot"])
        for payload in self.shared_renders.values():
            self.assertIn("Resp_lc", payload)

    def test_negative_fixtures_report_specific_failures_without_shared_mutation(self) -> None:
        mutable_graph = json.loads(self.shared_renders["json"])

        missing_node_graph = copy.deepcopy(mutable_graph)
        missing_node_graph["nodes"] = [
            node
            for node in missing_node_graph["nodes"]
            if node["label"] != "Resp_lc"
        ]
        with self.assertRaisesRegex(AssertionError, "required frontier node missing: Resp_lc"):
            self.assert_required_frontier_items(missing_node_graph)

        bad_edge_graph = copy.deepcopy(mutable_graph)
        bad_edge_graph["edges"][0]["target_id"] = "missing-target-fixture"
        with self.assertRaisesRegex(AssertionError, "edge target missing: missing-target-fixture"):
            self.assert_referential_integrity(bad_edge_graph)

        bad_authority_graph = copy.deepcopy(mutable_graph)
        bad_authority_graph["authority_boundary"]["navigational_support_only"] = False
        with self.assertRaisesRegex(
            AssertionError,
            re.escape("authority boundary mutated: navigational_support_only must remain true"),
        ):
            self.assert_authority_boundary(bad_authority_graph)

    def test_snapshot_is_immutable_and_loads_each_source_once(self) -> None:
        instrumentation = self.graph_module.GraphInstrumentation()
        snapshot = self.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in self.graph_module.REGISTRY_SPECS
            ),
            instrumentation=instrumentation,
        )

        self.assertEqual(instrumentation.source_loads, len(snapshot.sources))
        self.assertTrue(instrumentation.source_loads_by_path)
        self.assertEqual(set(instrumentation.source_loads_by_path.values()), {1})
        with self.assertRaises(TypeError):
            snapshot.sources["new"] = object()
        with self.assertRaises(TypeError):
            snapshot.source_hashes["new"] = "not-allowed"
        program_state = snapshot.sources["research_control/program_state.yaml"].payload
        with self.assertRaises(TypeError):
            program_state["active_task_id"] = "not-allowed"

    def test_snapshot_build_and_repeated_rendering_perform_no_file_reads(self) -> None:
        instrumentation = self.graph_module.GraphInstrumentation()
        snapshot = self.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in self.graph_module.REGISTRY_SPECS
            ),
            instrumentation=instrumentation,
        )
        loads_after_snapshot = instrumentation.source_loads

        with (
            mock.patch.object(Path, "read_bytes", side_effect=AssertionError("unexpected read_bytes")),
            mock.patch.object(Path, "read_text", side_effect=AssertionError("unexpected read_text")),
            mock.patch.object(Path, "open", side_effect=AssertionError("unexpected open")),
        ):
            graph = self.graph_module.build_graph(
                REPO_ROOT,
                snapshot=snapshot,
                instrumentation=instrumentation,
            )
            first = (
                self.graph_module.render_json(graph, instrumentation),
                self.graph_module.render_markdown(graph, instrumentation),
                self.graph_module.render_dot(graph, instrumentation),
            )
            second = (
                self.graph_module.render_json(graph, instrumentation),
                self.graph_module.render_markdown(graph, instrumentation),
                self.graph_module.render_dot(graph, instrumentation),
            )

        self.assertEqual(first, second)
        self.assertEqual(instrumentation.source_loads, loads_after_snapshot)
        self.assertEqual(instrumentation.graph_builds, 1)
        self.assertEqual(instrumentation.render_calls, 6)
        self.assertEqual(
            instrumentation.renders_by_format,
            {"json": 2, "markdown": 2, "dot": 2},
        )

    def test_implicit_and_explicit_snapshot_apis_are_byte_identical(self) -> None:
        implicit_graph = self.graph_module.build_graph(REPO_ROOT)
        snapshot_graph = json.loads(self.shared_renders["json"])

        self.assertEqual(implicit_graph, snapshot_graph)
        self.assertEqual(
            self.graph_module.render_json(implicit_graph),
            self.shared_renders["json"],
        )
        self.assertEqual(
            self.graph_module.render_markdown(implicit_graph),
            self.shared_renders["markdown"],
        )
        self.assertEqual(
            self.graph_module.render_dot(implicit_graph),
            self.shared_renders["dot"],
        )

    def test_freeze_summary_scopes_high_risk_accepted_label(self) -> None:
        self.assertIn(
            "scoped evidence/precondition status",
            self.shared_freeze_summary,
        )
        self.assertIn("not_frozen", self.shared_freeze_summary)
        self.assertNotIn("EVIDENCE-ACCEPTED", self.shared_freeze_summary)
        self.assertNotIn("True True", self.shared_freeze_summary)

    def test_cli_writes_all_declared_formats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            exit_code = self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertIn("navigational support only", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("navigational_support_only", dot_path.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["schema_id"], "research_dependency_graph_v1")

    def test_cli_check_passes_for_fresh_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            exit_code = self.graph_module.main(
                [
                    "--check",
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 0)

    def test_cli_check_fails_for_stale_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )
            markdown_path.write_text(
                markdown_path.read_text(encoding="utf-8") + "\nstale fixture\n",
                encoding="utf-8",
            )

            exit_code = self.graph_module.main(
                [
                    "--check",
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
