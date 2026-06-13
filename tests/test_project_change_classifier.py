from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
RESEARCH_CONTROL_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str, script_dir: Path = SCRIPT_DIR):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProjectChangeClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.classifier = load_module("classify_project_changes", "classify_project_changes.py")
        cls.doc_impact = load_module("validate_documentation_impact", "validate_documentation_impact.py")
        cls.resolver = load_module("resolve_project_improvement", "resolve_project_improvement.py")
        cls.signals = load_module("collect_project_improvement_signals", "collect_project_improvement_signals.py")
        cls.research_validator = load_module(
            "validate_research_control",
            "validate_research_control.py",
            RESEARCH_CONTROL_SCRIPT_DIR,
        )

    def write_signal_type_registry(self, root: Path, *signal_types: str) -> None:
        registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
        registry.parent.mkdir(parents=True, exist_ok=True)
        rows = [
            "signal_type,default_recommended_skill,default_recommended_role,status,notes",
        ]
        for signal_type in signal_types:
            rows.append(
                f"{signal_type},improve-project-system,validator-engineer,active,Synthetic test signal type."
            )
        registry.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def write_job_registry(self, root: Path, *job_ids: str) -> None:
        registry = root / "registries/AGENT_JOB_REGISTRY.csv"
        registry.parent.mkdir(parents=True, exist_ok=True)
        rows = ["job_id,job_path,completion_path"]
        for job_id in job_ids:
            rows.append(
                f"{job_id},research_control/tasks/RT-TEST/jobs/{job_id}.yaml,research_control/tasks/RT-TEST/jobs/completions/AJC-{job_id}.yaml"
            )
        registry.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def write_empty_signal_registry(self, root: Path) -> None:
        registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(
            "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n",
            encoding="utf-8",
        )

    def write_role_execution_registry(self, root: Path, count: int) -> None:
        registry = root / "registries/ROLE_EXECUTION_REGISTRY.csv"
        registry.parent.mkdir(parents=True, exist_ok=True)
        rows = [
            "execution_role_ref,role_execution_kind,task_id,agent_job_id,record_path,base_role_id,base_role_version,provisional_role_name,authority_delta_summary,added_constraints,removed_permissions,expanded_permissions,allowed_write_paths,requires_human_gate,expires_after,justification,non_reusable_until_registered,validation_status,created_at,updated_at,notes"
        ]
        for index in range(1, count + 1):
            rows.append(
                f"pilot-audit-{index},one_job_provisional_role,RT-ROLE-{index},AJ-ROLE-{index},research_control/tasks/RT-ROLE-{index}/roles/pilot-audit.yaml,refuter,0.1.0,Recurring Pilot Audit,One-job pilot role.,Synthetic constraint.,,,research_control/tasks/RT-ROLE-{index}/**,false,AJ-ROLE-{index},Synthetic recurrence fixture.,true,PASS,2026-06-10T00:0{index}:00Z,2026-06-10T00:0{index}:00Z,Synthetic role execution."
            )
        registry.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def write_job_contract(
        self,
        root: Path,
        *,
        job_id: str,
        objective: str,
        resolves_signal_routing: bool = False,
    ) -> str:
        path = root / f"research_control/tasks/RT-TEST/jobs/{job_id}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        routing_lines = ["resolves_signal_routing: true"] if resolves_signal_routing else []
        path.write_text(
            "\n".join(
                [
                    f'job_id: "{job_id}"',
                    'task_id: "RT-TEST"',
                    'decision_id: "DDR-TEST"',
                    'role_id: "validator-engineer"',
                    'role_version: "0.1.0"',
                    f'objective: "{objective}"',
                    *routing_lines,
                    'status: "completed"',
                    "requires_human_gate: false",
                    "allowed_read_paths:",
                    '  - "README.md"',
                    "allowed_write_paths:",
                    '  - "tests/test_project_change_classifier.py"',
                    "allowed_generated_paths:",
                    '  - ""',
                    "forbidden_paths:",
                    '  - "ontology/tex/**"',
                    "allowed_source_classes:",
                    '  - "test"',
                    "forbidden_source_classes:",
                    '  - "canonical_ontology"',
                    "approved_commands:",
                    '  - ".venv/bin/python -m unittest tests.test_project_change_classifier"',
                    "required_validators:",
                    '  - "unittest"',
                    "expected_outputs:",
                    '  - "tests/test_project_change_classifier.py"',
                    'claim_boundary: "CB-TEST"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return path.relative_to(root).as_posix()

    def write_completion(
        self,
        root: Path,
        *,
        job_id: str = "AJ-RESOLVE",
        validation_status: str = "PASS",
        resolved_signal_ids: list[str] | None = None,
        coherent_resolution_summary: str = "",
        resolver_snapshots: dict[str, str] | None = None,
        routing_delta_summary: str | None = None,
    ) -> str:
        path = root / f"research_control/tasks/RT-TEST/jobs/completions/AJC-{job_id}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        resolution_lines: list[str] = []
        if resolved_signal_ids is not None:
            resolution_lines.append("resolved_project_improvement_signals:")
            for signal_id in resolved_signal_ids:
                resolution_lines.append(f'  - signal_id: "{signal_id}"')
            resolution_lines.append(
                f'coherent_resolution_summary: "{coherent_resolution_summary}"'
            )
        snapshot_lines: list[str] = []
        if resolver_snapshots is not None:
            snapshot_lines.append("resolver_snapshots:")
            snapshot_lines.append(f'  before: "{resolver_snapshots.get("before", "")}"')
            snapshot_lines.append(f'  after: "{resolver_snapshots.get("after", "")}"')
        if routing_delta_summary is not None:
            snapshot_lines.append(f'routing_delta_summary: "{routing_delta_summary}"')
        path.write_text(
            "\n".join(
                [
                    f'completion_id: "AJC-{job_id}"',
                    f'job_id: "{job_id}"',
                    'task_id: "RT-TEST"',
                    'completed_at: "2026-06-10T00:00:00Z"',
                    'status: "completed"',
                    "output_paths:",
                    '  - "tests/test_project_change_classifier.py"',
                    "extra_read_paths:",
                    '  - "README.md"',
                    "command_results:",
                    '  - ".venv/bin/python -m unittest tests.test_project_change_classifier | exit_code=0 | status=pass"',
                    f'validation_status: "{validation_status}"',
                    'verdict: "synthetic_completion"',
                    *resolution_lines,
                    *snapshot_lines,
                    'next_recommendation: ""',
                    "project_improvement_signals:",
                    '  - signal_id: ""',
                    '    signal_type: ""',
                    '    severity: ""',
                    '    evidence: ""',
                    '    evidence_path: ""',
                    '    recommended_skill: ""',
                    '    recommended_role: ""',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return path.relative_to(root).as_posix()

    def write_resolver_snapshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "status": "ready",
                    "boundary": "project_improvement_signal_ready",
                    "reason": "Synthetic resolver state.",
                    "resolver_is_advisory": True,
                    "hard_checkpoint_gate": False,
                    "checkpoint_gate_source": "validators",
                    "selected_signal": {},
                    "open_signals": [],
                    "change_classification": {},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_role_skill_and_validator_changes_require_documentation_impact(self) -> None:
        result = self.classifier.classify_paths(
            [
                ".agents/roles/research_ops/documentation-curator.v0.1.0.md",
                ".codex/skills/continue-research/SKILL.md",
                "scripts/project_control/validate_documentation_impact.py",
            ]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertTrue(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "validator-engineer")
        self.assertIn("role_contract_changed", result["reason_codes"])
        self.assertIn("skill_contract_changed", result["reason_codes"])
        self.assertIn("validator_changed", result["reason_codes"])

    def test_skill_contract_change_routes_to_project_control_maintainer(self) -> None:
        result = self.classifier.classify_paths(
            [".codex/skills/continue-research/SKILL.md"]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertTrue(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "project-control-maintainer")
        self.assertIn("skill_contract_changed", result["reason_codes"])

    def test_explanatory_mixed_markdown_routes_to_documentation_curator(self) -> None:
        original_root = self.classifier.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text(
                "<!-- authority: explanatory -->\n# Example\n",
                encoding="utf-8",
            )
            self.classifier.REPO_ROOT = root
            try:
                result = self.classifier.classify_paths(["README.md"])
            finally:
                self.classifier.REPO_ROOT = original_root
        self.assertTrue(result["docs_impact_required"])
        self.assertFalse(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "documentation-curator")
        self.assertIn("documentation_surface_changed", result["reason_codes"])

    def test_control_mixed_markdown_routes_to_project_control_maintainer(self) -> None:
        original_root = self.classifier.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "AGENTS.md").write_text(
                "<!-- authority: control -->\n# Example\n",
                encoding="utf-8",
            )
            self.classifier.REPO_ROOT = root
            try:
                result = self.classifier.classify_paths(["AGENTS.md"])
            finally:
                self.classifier.REPO_ROOT = original_root
        self.assertTrue(result["docs_impact_required"])
        self.assertTrue(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "project-control-maintainer")
        self.assertIn("control_markdown_changed", result["reason_codes"])

    def test_physics_tex_change_does_not_trigger_curator_by_default(self) -> None:
        result = self.classifier.classify_paths(
            ["ontology/tex/aether_flow_foundations.tex"]
        )
        self.assertFalse(result["docs_impact_required"])
        self.assertFalse(result["project_system_improvement_required"])
        self.assertIn("physics_source_changed", result["reason_codes"])

    def test_generated_only_change_blocks_until_source_boundary_is_explained(self) -> None:
        result = self.classifier.classify_paths(["wiki/markdown/example.md"])
        self.assertTrue(result["docs_impact_required"])
        self.assertIn("wiki/markdown/example.md", result["blocked_paths"])
        self.assertIn("direct_generated_derivative_edit", result["reason_codes"])

    def test_generated_change_with_canonical_source_is_not_direct_edit_block(self) -> None:
        result = self.classifier.classify_paths(
            ["README.md", "wiki/markdown/md-readme.md"]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertEqual(result["blocked_paths"], [])
        self.assertIn("generated_derivative_changed", result["reason_codes"])

    def test_documentation_impact_validator_accepts_current_record(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "FOLDER_MAP.md",
                "scripts/project_control/classify_project_changes.py",
                "scripts/project_control/resolve_project_improvement.py",
                "scripts/project_control/validate_documentation_impact.py",
                "research_control/tasks/RT-20260610-002/jobs/AJ-RT-20260610-002-001.yaml",
                "research_control/tasks/RT-20260610-002/documentation_impact.yaml",
                "tests/test_project_change_classifier.py",
            ]
        )
        self.assertEqual(report.errors, [])

    def test_documentation_impact_record_must_cover_live_source_changes(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "scripts/project_control/synthetic_validator.py",
                "research_control/tasks/RT-20260610-002/documentation_impact.yaml",
            ]
        )
        self.assertTrue(any("changed_paths missing live source change" in error for error in report.errors))

    def test_documentation_impact_record_must_cover_classifier_reasons(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "markdown/synthetic.md",
                "research_control/tasks/RT-20260610-002/documentation_impact.yaml",
            ]
        )
        self.assertTrue(any("reason_codes missing classifier reason" in error for error in report.errors))

    def test_documentation_impact_record_must_cover_generated_changes(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "html/synthetic.html",
                "research_control/tasks/RT-20260610-002/documentation_impact.yaml",
            ]
        )
        self.assertTrue(any("generated_derivatives missing live generated change" in error for error in report.errors))

    def test_source_backed_html_routes_to_documentation_curator(self) -> None:
        result = self.classifier.classify_paths(
            [
                "markdown/html-explainer-specs/synthetic.md",
                "html/synthetic.html",
            ]
        )
        self.assertTrue(result["docs_impact_required"])
        self.assertFalse(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "documentation-curator")
        self.assertEqual(result["blocked_paths"], [])
        self.assertIn("html_source_spec_changed", result["reason_codes"])
        self.assertIn("generated_derivative_changed", result["reason_codes"])

    def test_github_facing_markdown_routes_to_documentation_curator(self) -> None:
        result = self.classifier.classify_paths(["docs/github-facing/start-here.md"])
        self.assertTrue(result["docs_impact_required"])
        self.assertFalse(result["project_system_improvement_required"])
        self.assertEqual(result["recommended_role"], "documentation-curator")
        self.assertIn("github_facing_markdown_changed", result["reason_codes"])
        self.assertIn(
            "registries/MARKDOWN_SOURCE_REGISTRY.csv",
            result["required_documentation_surfaces"],
        )

    def test_github_facing_markdown_counts_as_source_documentation_update(self) -> None:
        report = self.doc_impact.validate_paths(["docs/github-facing/start-here.md"])
        self.assertEqual(report.errors, [])

    def test_direct_html_edit_remains_blocked(self) -> None:
        result = self.classifier.classify_paths(["html/synthetic.html"])
        self.assertTrue(result["docs_impact_required"])
        self.assertIn("html/synthetic.html", result["blocked_paths"])
        self.assertIn("direct_generated_derivative_edit", result["reason_codes"])

    def test_project_system_impact_record_must_list_required_validators(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "scripts/project_control/validate_documentation_impact.py",
                "research_control/tasks/RT-20260610-001/jobs/AJ-RT-20260610-001-001.yaml",
                "research_control/tasks/RT-20260610-001/documentation_impact.yaml",
            ]
        )
        self.assertTrue(any("validators_run missing" in error for error in report.errors))

    def test_project_system_agent_job_requires_impact_record_even_with_doc_update(self) -> None:
        report = self.doc_impact.validate_paths(
            [
                "README.md",
                "scripts/project_control/validate_documentation_impact.py",
                "research_control/tasks/RT-20260610-002/jobs/AJ-RT-20260610-002-001.yaml",
            ]
        )
        self.assertTrue(
            any(
                "state-changing project-system AgentJob requires documentation_impact.yaml"
                in error
                for error in report.errors
            )
        )

    def test_plain_documentation_update_does_not_require_impact_record(self) -> None:
        report = self.doc_impact.validate_paths(["README.md"])
        self.assertEqual(report.errors, [])

    def test_documentation_impact_validator_requires_update_or_record(self) -> None:
        report = self.doc_impact.validate_paths(
            ["scripts/project_control/validate_documentation_impact.py"]
        )
        self.assertTrue(any("documentation impact is required" in error for error in report.errors))

    def test_classifier_detects_project_signals_structurally(self) -> None:
        original_root = self.classifier.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            completion = root / "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
            completion.parent.mkdir(parents=True)
            completion.write_text(
                "\n".join(
                    [
                        'job_id: "AJ-TEST"',
                        'task_id: "RT-TEST"',
                        "project_improvement_signals:",
                        '  - signal_type: "validator_gap"',
                        '    severity: "high"',
                        '    evidence: "Synthetic structural signal."',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            registry.parent.mkdir(parents=True)
            registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes\n"
                "PIS-TEST,2026-06-10T00:00:00Z,RT-TEST,AJ-TEST,validator-engineer,validator_gap,high,open,research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml,improve-project-system,validator-engineer,Synthetic structural signal.\n",
                encoding="utf-8",
            )
            self.write_signal_type_registry(root, "validator_gap")
            self.classifier.REPO_ROOT = root
            try:
                path = "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
                self.assertTrue(self.classifier.contains_project_signal(path))
                result = self.classifier.classify_paths([path])
            finally:
                self.classifier.REPO_ROOT = original_root
        self.assertTrue(result["docs_impact_required"])
        self.assertTrue(result["project_system_improvement_required"])
        self.assertIn("project_improvement_signal_recorded", result["reason_codes"])

    def test_classifier_ignores_signal_terms_outside_signal_structure(self) -> None:
        original_root = self.classifier.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            completion = root / "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
            completion.parent.mkdir(parents=True)
            completion.write_text(
                "\n".join(
                    [
                        'job_id: "AJ-TEST"',
                        'task_id: "RT-TEST"',
                        'verdict: "validator_gap mentioned in prose only"',
                        "project_improvement_signals:",
                        '  - signal_id: ""',
                        '    signal_type: ""',
                        '    severity: ""',
                        '    evidence: ""',
                        '    evidence_path: ""',
                        '    recommended_skill: ""',
                        '    recommended_role: ""',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            self.classifier.REPO_ROOT = root
            try:
                path = "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
                self.assertFalse(self.classifier.contains_project_signal(path))
                result = self.classifier.classify_paths([path])
            finally:
                self.classifier.REPO_ROOT = original_root
        self.assertIn("research_control_state_changed", result["reason_codes"])
        self.assertNotIn("project_improvement_signal_recorded", result["reason_codes"])

    def test_resolver_recommends_project_control_maintainer_for_skill_contract(self) -> None:
        result = self.resolver.resolve_project_improvement(
            [".codex/skills/continue-research/SKILL.md"]
        )
        self.assertEqual(result["boundary"], "project_system_agent_job_required")
        self.assertEqual(result["recommended_role"], "project-control-maintainer")
        self.assertTrue(result["resolver_is_advisory"])
        self.assertFalse(result["hard_checkpoint_gate"])
        self.assertEqual(result["checkpoint_gate_source"], "validators")

    def test_low_signal_does_not_preempt_current_documentation_impact(self) -> None:
        original = self.resolver.collect_signals
        self.resolver.collect_signals = lambda: {
            "open_signals": [
                {
                    "signal_id": "PIS-LOW",
                    "signal_type": "workflow_friction",
                    "severity": "low",
                    "recommended_role": "project-system-director",
                    "created_at": "2026-06-10T00:00:00Z",
                }
            ]
        }
        try:
            result = self.resolver.resolve_project_improvement(
                [".codex/skills/continue-research/SKILL.md"]
            )
        finally:
            self.resolver.collect_signals = original
        self.assertEqual(result["boundary"], "project_system_agent_job_required")
        self.assertEqual(result["recommended_role"], "project-control-maintainer")
        self.assertEqual(result["selected_signal"], {})

    def test_high_signal_preempts_current_documentation_impact(self) -> None:
        original = self.resolver.collect_signals
        self.resolver.collect_signals = lambda: {
            "open_signals": [
                {
                    "signal_id": "PIS-HIGH",
                    "signal_type": "validator_gap",
                    "severity": "high",
                    "recommended_role": "validator-engineer",
                    "created_at": "2026-06-10T00:00:00Z",
                }
            ]
        }
        try:
            result = self.resolver.resolve_project_improvement(
                [".codex/skills/continue-research/SKILL.md"]
            )
        finally:
            self.resolver.collect_signals = original
        self.assertEqual(result["boundary"], "project_improvement_signal_ready")
        self.assertEqual(result["recommended_role"], "validator-engineer")
        self.assertEqual(result["selected_signal"]["signal_id"], "PIS-HIGH")

    def test_resolver_uses_signal_type_registry_default_role(self) -> None:
        original_collect = self.resolver.collect_signals
        original_role_map = self.resolver.signal_type_role_map
        self.resolver.collect_signals = lambda: {
            "open_signals": [
                {
                    "signal_id": "PIS-TYPE-ROLE",
                    "signal_type": "validator_gap",
                    "severity": "high",
                    "recommended_role": "",
                    "created_at": "2026-06-10T00:00:00Z",
                }
            ]
        }
        self.resolver.signal_type_role_map = lambda: {"validator_gap": "validator-engineer"}
        try:
            result = self.resolver.resolve_project_improvement([])
        finally:
            self.resolver.collect_signals = original_collect
            self.resolver.signal_type_role_map = original_role_map
        self.assertEqual(result["boundary"], "project_improvement_signal_ready")
        self.assertEqual(result["recommended_role"], "validator-engineer")

    def test_two_matching_provisional_roles_do_not_emit_promotion_signal(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "role_authority_mismatch")
            self.write_empty_signal_registry(root)
            self.write_role_execution_registry(root, 2)
            self.signals.REPO_ROOT = root
            try:
                result = self.signals.collect_signals(signal_type="role_authority_mismatch")
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(result["open_signal_count"], 0)

    def test_three_matching_provisional_roles_emit_promotion_signal(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "role_authority_mismatch")
            self.write_empty_signal_registry(root)
            self.write_role_execution_registry(root, 3)
            self.signals.REPO_ROOT = root
            try:
                result = self.signals.collect_signals(signal_type="role_authority_mismatch")
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(result["open_signal_count"], 1)
        self.assertEqual(result["open_signals"][0]["recommended_role"], "project-system-director")
        self.assertIn("provisional_role_recurrence_key=", result["open_signals"][0]["notes"])

    def test_human_authorized_registration_can_close_recurrence_signal(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "role_authority_mismatch")
            self.write_role_execution_registry(root, 3)
            key = "name=recurring pilot audit|base=refuter|version=0.1.0"
            signal_id = self.signals._signal_id_for_recurrence(key)
            token = self.signals._recurrence_token(key)
            self.write_job_registry(root, "AJ-REGISTER")
            completion_path = self.write_completion(root, job_id="AJ-REGISTER")
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"{signal_id},2026-06-10T00:03:00Z,RT-ROLE-3,,Recurring Pilot Audit,role_authority_mismatch,medium,resolved,,improve-project-system,project-system-director,{token}; human-authorized registration completed.,AJ-REGISTER,{completion_path},2026-06-10T00:04:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                result = self.signals.collect_signals(status="open", signal_type="role_authority_mismatch")
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(result["open_signal_count"], 0)
        self.assertEqual(report["errors"], [])

    def test_emitted_project_improvement_signals_are_registered(self) -> None:
        report = self.signals.validate_signal_registration()
        self.assertEqual(report["errors"], [])

    def test_signal_registry_rejects_unregistered_signal_type(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                "PIS-UNKNOWN,2026-06-10T00:00:00Z,RT-TEST,,,unknown_type,high,open,,improve-project-system,validator-engineer,Synthetic unknown signal type.,,,\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "signal_type is not registered in PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
                in error
                for error in report["errors"]
            )
        )

    def test_resolved_signal_requires_resolution_evidence(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                "PIS-RESOLVED,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal without receipt.,,,\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "resolved signal missing resolution evidence fields"
                in error
                for error in report["errors"]
            )
        )

    def test_resolved_signal_requires_pass_completion_evidence(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            completion_path = self.write_completion(
                root,
                job_id="AJ-RESOLVE",
                validation_status="FAIL",
            )
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-RESOLVED,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal with failing receipt.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "completion validation_status must be PASS"
                in error
                for error in report["errors"]
            )
        )

    def test_resolved_signal_accepts_pass_completion_evidence(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            completion_path = self.write_completion(root, job_id="AJ-RESOLVE")
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-RESOLVED,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal with PASS receipt.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(report["errors"], [])

    def test_rejected_signal_accepts_director_decision_evidence(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-REJECT")
            decision = root / "research_control/tasks/RT-TEST/DDR-TEST.md"
            decision.parent.mkdir(parents=True, exist_ok=True)
            decision.write_text(
                "\n".join(
                    [
                        "---",
                        'decision_id: "DDR-TEST"',
                        'task_id: "RT-TEST"',
                        'status: "completed"',
                        "---",
                        "",
                        "# Director Decision Record DDR-TEST",
                        "",
                        "PIS-REJECTED is rejected because the synthetic signal is invalid.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                "PIS-REJECTED,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,low,rejected,,improve-project-system,validator-engineer,Synthetic rejected signal.,AJ-REJECT,research_control/tasks/RT-TEST/DDR-TEST.md,2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(report["errors"], [])

    def test_shared_signal_resolution_requires_job_objective_to_name_each_signal(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            self.write_job_contract(
                root,
                job_id="AJ-RESOLVE",
                objective="Resolve PIS-A with one bounded fix.",
            )
            completion_path = self.write_completion(
                root,
                job_id="AJ-RESOLVE",
                resolved_signal_ids=["PIS-A", "PIS-B"],
                coherent_resolution_summary="One validator fix resolves both synthetic signals.",
            )
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-A,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal A.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n"
                f"PIS-B,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,medium,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal B.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "AgentJob objective missing resolved signal_id PIS-B"
                in error
                for error in report["errors"]
            )
        )

    def test_shared_signal_resolution_requires_coherent_completion_record(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            self.write_job_contract(
                root,
                job_id="AJ-RESOLVE",
                objective="Resolve PIS-A and PIS-B with one bounded fix.",
            )
            completion_path = self.write_completion(root, job_id="AJ-RESOLVE")
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-A,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal A.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n"
                f"PIS-B,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,medium,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal B.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "completion resolving multiple signals must list resolved_project_improvement_signals"
                in error
                for error in report["errors"]
            )
        )
        self.assertTrue(
            any(
                "completion resolving multiple signals must include coherent_resolution_summary"
                in error
                for error in report["errors"]
            )
        )

    def test_shared_signal_resolution_requires_canonical_completion_path(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            self.write_job_contract(
                root,
                job_id="AJ-RESOLVE",
                objective="Resolve PIS-A and PIS-B with one bounded fix.",
            )
            canonical_completion_path = self.write_completion(
                root,
                job_id="AJ-RESOLVE",
                resolved_signal_ids=["PIS-A", "PIS-B"],
                coherent_resolution_summary="One validator fix resolves both synthetic signals.",
            )
            alternate = root / "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-RESOLVE-ALT.yaml"
            alternate.write_text(
                "\n".join(
                    [
                        'completion_id: "AJC-AJ-RESOLVE-ALT"',
                        'job_id: "AJ-RESOLVE"',
                        'task_id: "RT-TEST"',
                        'completed_at: "2026-06-10T00:00:00Z"',
                        'status: "completed"',
                        "output_paths:",
                        '  - "tests/test_project_change_classifier.py"',
                        "extra_read_paths:",
                        '  - "README.md"',
                        "command_results:",
                        '  - ".venv/bin/python -m unittest tests.test_project_change_classifier | exit_code=0 | status=pass"',
                        'validation_status: "PASS"',
                        'verdict: "alternate_synthetic_completion"',
                        "resolved_project_improvement_signals:",
                        '  - signal_id: "PIS-A"',
                        '  - signal_id: "PIS-B"',
                        'coherent_resolution_summary: "One validator fix resolves both synthetic signals."',
                        'next_recommendation: ""',
                        "project_improvement_signals:",
                        '  - signal_id: ""',
                        '    signal_type: ""',
                        '    severity: ""',
                        '    evidence: ""',
                        '    evidence_path: ""',
                        '    recommended_skill: ""',
                        '    recommended_role: ""',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            alternate_completion_path = alternate.relative_to(root).as_posix()
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-A,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal A.,AJ-RESOLVE,{canonical_completion_path},2026-06-10T00:00:00Z\n"
                f"PIS-B,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,medium,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal B.,AJ-RESOLVE,{alternate_completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "shared signal closure row PIS-B resolution_evidence_path must match AGENT_JOB_REGISTRY.csv completion_path"
                in error
                for error in report["errors"]
            )
        )

    def test_shared_signal_resolution_accepts_explicit_coherent_fix(self) -> None:
        original_root = self.signals.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_signal_type_registry(root, "validator_gap")
            self.write_job_registry(root, "AJ-RESOLVE")
            self.write_job_contract(
                root,
                job_id="AJ-RESOLVE",
                objective="Resolve PIS-A and PIS-B with one bounded fix.",
            )
            completion_path = self.write_completion(
                root,
                job_id="AJ-RESOLVE",
                resolved_signal_ids=["PIS-A", "PIS-B"],
                coherent_resolution_summary="One validator fix resolves both synthetic signals.",
            )
            signal_registry = root / "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
            signal_registry.write_text(
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,signal_type,severity,status,evidence_path,recommended_skill,recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at\n"
                f"PIS-A,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,high,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal A.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n"
                f"PIS-B,2026-06-10T00:00:00Z,RT-TEST,,,validator_gap,medium,resolved,,improve-project-system,validator-engineer,Synthetic resolved signal B.,AJ-RESOLVE,{completion_path},2026-06-10T00:00:00Z\n",
                encoding="utf-8",
            )
            self.signals.REPO_ROOT = root
            try:
                report = self.signals.validate_signal_registration()
            finally:
                self.signals.REPO_ROOT = original_root
        self.assertEqual(report["errors"], [])

    def test_routing_resolution_completion_requires_resolver_snapshots(self) -> None:
        original_root = self.research_validator.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            job_path = self.write_job_contract(
                root,
                job_id="AJ-ROUTE",
                objective="Resolve project-improvement signal routing.",
                resolves_signal_routing=True,
            )
            completion_path = self.write_completion(root, job_id="AJ-ROUTE")
            report = self.research_validator.ValidationReport()
            self.research_validator.REPO_ROOT = root
            try:
                self.research_validator.validate_completion(
                    report,
                    {"job_id": "AJ-ROUTE", "job_path": job_path},
                    root / completion_path,
                )
            finally:
                self.research_validator.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "routing-resolution completion must declare resolver_snapshots.before and resolver_snapshots.after"
                in error
                for error in report.errors
            )
        )

    def test_routing_resolution_completion_accepts_before_after_snapshots(self) -> None:
        original_root = self.research_validator.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            job_path = self.write_job_contract(
                root,
                job_id="AJ-ROUTE",
                objective="Resolve project-improvement signal routing.",
                resolves_signal_routing=True,
            )
            before = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-before.json"
            after = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-after.json"
            self.write_resolver_snapshot(before)
            self.write_resolver_snapshot(after)
            completion_path = self.write_completion(
                root,
                job_id="AJ-ROUTE",
                resolver_snapshots={
                    "before": before.relative_to(root).as_posix(),
                    "after": after.relative_to(root).as_posix(),
                },
                routing_delta_summary="Synthetic before after routing delta.",
            )
            report = self.research_validator.ValidationReport()
            self.research_validator.REPO_ROOT = root
            try:
                self.research_validator.validate_completion(
                    report,
                    {"job_id": "AJ-ROUTE", "job_path": job_path},
                    root / completion_path,
                )
            finally:
                self.research_validator.REPO_ROOT = original_root
        self.assertEqual(report.errors, [])

    def test_routing_resolution_completion_rejects_empty_snapshot_json(self) -> None:
        original_root = self.research_validator.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            job_path = self.write_job_contract(
                root,
                job_id="AJ-ROUTE",
                objective="Resolve project-improvement signal routing.",
                resolves_signal_routing=True,
            )
            before = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-before.json"
            after = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-after.json"
            before.parent.mkdir(parents=True, exist_ok=True)
            before.write_text("{}\n", encoding="utf-8")
            self.write_resolver_snapshot(after)
            completion_path = self.write_completion(
                root,
                job_id="AJ-ROUTE",
                resolver_snapshots={
                    "before": before.relative_to(root).as_posix(),
                    "after": after.relative_to(root).as_posix(),
                },
                routing_delta_summary="Synthetic before after routing delta.",
            )
            report = self.research_validator.ValidationReport()
            self.research_validator.REPO_ROOT = root
            try:
                self.research_validator.validate_completion(
                    report,
                    {"job_id": "AJ-ROUTE", "job_path": job_path},
                    root / completion_path,
                )
            finally:
                self.research_validator.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "resolver_snapshots.before missing resolver field status" in error
                for error in report.errors
            )
        )

    def test_routing_resolution_completion_requires_delta_summary(self) -> None:
        original_root = self.research_validator.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            job_path = self.write_job_contract(
                root,
                job_id="AJ-ROUTE",
                objective="Resolve project-improvement signal routing.",
                resolves_signal_routing=True,
            )
            before = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-before.json"
            after = root / "research_control/tasks/RT-TEST/resolver_snapshots/AJ-ROUTE-after.json"
            self.write_resolver_snapshot(before)
            self.write_resolver_snapshot(after)
            completion_path = self.write_completion(
                root,
                job_id="AJ-ROUTE",
                resolver_snapshots={
                    "before": before.relative_to(root).as_posix(),
                    "after": after.relative_to(root).as_posix(),
                },
            )
            report = self.research_validator.ValidationReport()
            self.research_validator.REPO_ROOT = root
            try:
                self.research_validator.validate_completion(
                    report,
                    {"job_id": "AJ-ROUTE", "job_path": job_path},
                    root / completion_path,
                )
            finally:
                self.research_validator.REPO_ROOT = original_root
        self.assertTrue(
            any(
                "routing-resolution completion missing routing_delta_summary" in error
                for error in report.errors
            )
        )

    def test_signal_match_rejects_unregistered_emission(self) -> None:
        emitted = {
            "source_path": "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml",
            "index": 1,
            "source_task_id": "RT-TEST",
            "source_job_id": "AJ-TEST",
            "source_role_id": "validator-engineer",
            "signal": {
                "signal_type": "validator_gap",
                "severity": "high",
                "evidence": "Synthetic unregistered signal.",
                "recommended_skill": "improve-project-system",
                "recommended_role": "validator-engineer",
            },
        }
        self.assertFalse(
            any(self.signals.signal_matches(row, emitted) for row in self.signals.read_signals())
        )

    def test_signal_id_match_still_requires_source_match(self) -> None:
        emitted = {
            "source_path": "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml",
            "index": 1,
            "source_task_id": "RT-TEST",
            "source_job_id": "AJ-TEST",
            "source_role_id": "validator-engineer",
            "signal": {
                "signal_id": "PIS-TEST",
                "signal_type": "validator_gap",
                "severity": "high",
            },
        }
        row = {
            "signal_id": "PIS-TEST",
            "source_task_id": "RT-OTHER",
            "source_job_id": "AJ-OTHER",
            "source_role_id": "validator-engineer",
            "signal_type": "validator_gap",
            "severity": "high",
            "evidence_path": "",
            "recommended_skill": "",
            "recommended_role": "",
            "notes": "",
        }
        self.assertFalse(self.signals.signal_matches(row, emitted))


if __name__ == "__main__":
    unittest.main()
