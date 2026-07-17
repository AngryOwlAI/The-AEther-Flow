from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "dependency_graph" / "synthetic_repo"
LIVE_TEST_PATH = REPO_ROOT / "tests" / "test_render_dependency_graph.py"


def load_graph_module():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "render_dependency_graph_synthetic_fixture",
        SCRIPT_DIR / "render_dependency_graph.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SyntheticDependencyGraphDeterminismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph_module = load_graph_module()
        cls.registry_paths = tuple(
            f"registries/{name}" for name in cls.graph_module.REGISTRY_SPECS
        )
        cls.snapshot = cls.graph_module.load_graph_input_snapshot(
            FIXTURE_ROOT,
            registry_paths=cls.registry_paths,
        )
        cls.graph = cls.graph_module.build_graph(
            FIXTURE_ROOT,
            snapshot=cls.snapshot,
        )
        cls.renders = cls.render_bundle(cls.graph)

    @classmethod
    def render_bundle(cls, graph):
        return {
            "json": cls.graph_module.render_json(graph),
            "markdown": cls.graph_module.render_markdown(graph),
            "dot": cls.graph_module.render_dot(graph),
        }

    @staticmethod
    def hashes(payloads):
        return {
            name: hashlib.sha256(payload.encode("utf-8")).hexdigest()
            for name, payload in payloads.items()
        }

    def test_repeated_builds_have_identical_graph_and_render_hashes(self) -> None:
        second_snapshot = self.graph_module.load_graph_input_snapshot(
            FIXTURE_ROOT,
            registry_paths=self.registry_paths,
        )
        second_graph = self.graph_module.build_graph(
            FIXTURE_ROOT,
            snapshot=second_snapshot,
        )
        second_renders = self.render_bundle(second_graph)

        self.assertEqual(second_graph, self.graph)
        self.assertEqual(second_renders, self.renders)
        self.assertEqual(self.hashes(second_renders), self.hashes(self.renders))

    def test_reversed_row_and_file_enumeration_is_byte_identical(self) -> None:
        real_glob = Path.glob

        def reversed_glob(path, pattern):
            paths = list(real_glob(path, pattern))
            if pattern == "handoff-*.yaml":
                paths.reverse()
            return iter(paths)

        with mock.patch.object(Path, "glob", new=reversed_glob):
            reordered_snapshot = self.graph_module.load_graph_input_snapshot(
                FIXTURE_ROOT,
                registry_paths=self.registry_paths,
            )

        self.assertEqual(reordered_snapshot.handoff_paths, self.snapshot.handoff_paths)
        original_csv_rows = self.graph_module.GraphInputSnapshot.csv_rows

        def reversed_csv_rows(snapshot, path_text):
            return list(reversed(original_csv_rows(snapshot, path_text)))

        with mock.patch.object(
            self.graph_module.GraphInputSnapshot,
            "csv_rows",
            new=reversed_csv_rows,
        ):
            reordered_graph = self.graph_module.build_graph(
                FIXTURE_ROOT,
                snapshot=reordered_snapshot,
            )
        reordered_renders = self.render_bundle(reordered_graph)

        self.assertEqual(reordered_graph, self.graph)
        self.assertEqual(reordered_renders, self.renders)
        self.assertEqual(self.hashes(reordered_renders), self.hashes(self.renders))

    def test_fixture_covers_emitted_classes_and_every_serialized_field(self) -> None:
        node_classes = {node["node_class"] for node in self.graph["nodes"]}
        edge_classes = {edge["edge_class"] for edge in self.graph["edges"]}

        self.assertEqual(node_classes, self.graph_module.NODE_CLASSES)
        # "rejects" is reserved schema vocabulary; no tracked-source extractor
        # currently emits it, so determinism covers every emitted edge class.
        self.assertEqual(edge_classes, self.graph_module.EDGE_CLASSES - {"rejects"})
        self.assertIn("rejects", self.graph_module.EDGE_CLASSES)

        self.assertEqual(
            set(self.graph),
            {
                "schema_id",
                "generated_at",
                "authority_notice",
                "authority_boundary",
                "source_fingerprint",
                "sources",
                "nodes",
                "edges",
                "warnings",
                "route_continuity",
            },
        )
        self.assertEqual(
            set(self.graph["authority_boundary"]),
            {
                "navigational_support_only",
                "physics_claim_authority",
                "proof_authority",
                "source_authority_required",
                "generated_graph_can_promote_claims",
            },
        )
        for source in self.graph["sources"]:
            self.assertEqual(
                set(source),
                {"path", "source_kind", "source_hash", "registry_object_id"},
            )
            self.assertRegex(source["source_hash"], r"^[0-9a-f]{64}$")
        for node in self.graph["nodes"]:
            self.assertEqual(
                set(node),
                {
                    "node_id",
                    "node_class",
                    "label",
                    "state_label",
                    "source_path",
                    "source_registry",
                    "source_field",
                    "authority_status",
                    "summary",
                    "metadata",
                },
            )
        for edge in self.graph["edges"]:
            self.assertEqual(
                set(edge),
                {
                    "edge_id",
                    "source_id",
                    "target_id",
                    "edge_class",
                    "source_path",
                    "source_field",
                    "summary",
                    "metadata",
                },
            )
        route = self.graph["route_continuity"]
        self.assertEqual(
            set(route),
            {
                "program_state_path",
                "active_task_id",
                "latest_handoff",
                "authority_note",
            },
        )
        self.assertEqual(
            set(route["latest_handoff"]),
            {"handoff_id", "path", "task_id", "job_id", "next_action"},
        )
        self.assertRegex(self.graph["source_fingerprint"], r"^[0-9a-f]{64}$")
        self.assertEqual(route["active_task_id"], "RT-SYNTH-CHILD")
        self.assertEqual(route["latest_handoff"]["handoff_id"], "handoff-0002")
        self.assertTrue(
            any(node["metadata"].get("source_refs") for node in self.graph["nodes"]),
            "duplicate source references must be normalized and retained",
        )

    def test_malformed_edge_is_rejected_with_specific_endpoint(self) -> None:
        builder = self.graph_module.GraphBuilder(self.snapshot)
        builder.add_node(
            "task:fixture-valid",
            "task",
            "fixture-valid",
            "support_only",
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "RESEARCH_TASK_REGISTRY.csv",
            "task_id",
            "project_control",
            "Synthetic valid endpoint.",
        )
        builder.add_edge(
            "task:fixture-valid",
            "task:fixture-missing",
            "depends_on",
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "parent_task_id",
            "Synthetic malformed target.",
        )

        with self.assertRaisesRegex(
            self.graph_module.GraphError,
            "missing target node task:fixture-missing",
        ):
            builder.validate()

    def test_missing_source_is_explicit_and_changes_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_root = Path(tmpdir) / "synthetic_repo"
            shutil.copytree(FIXTURE_ROOT, missing_root)
            missing_registry = "registries/MARKDOWN_SOURCE_REGISTRY.csv"
            (missing_root / missing_registry).unlink()
            snapshot = self.graph_module.load_graph_input_snapshot(
                missing_root,
                registry_paths=self.registry_paths,
            )
            missing_graph = self.graph_module.build_graph(
                missing_root,
                snapshot=snapshot,
            )

        self.assertEqual(snapshot.parse_error(missing_registry), "source missing")
        source = next(
            item for item in missing_graph["sources"] if item["path"] == missing_registry
        )
        self.assertEqual(source["source_hash"], "")
        self.assertNotEqual(missing_graph["source_fingerprint"], self.graph["source_fingerprint"])
        self.assertNotIn(
            "artifact:MD-SYNTH-CONTROL",
            {node["node_id"] for node in missing_graph["nodes"]},
        )

    def test_live_full_corpus_acceptance_remains_separate(self) -> None:
        live_test = LIVE_TEST_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "test_implicit_and_explicit_snapshot_apis_are_byte_identical",
            live_test,
        )
        self.assertIn("test_cli_write_fresh_and_stale_lifecycle", live_test)
        self.assertIsNone(
            re.search(r"FIXTURE_ROOT|synthetic_repo", live_test),
            "the live acceptance module must not be replaced by the synthetic fixture",
        )


if __name__ == "__main__":
    unittest.main()
