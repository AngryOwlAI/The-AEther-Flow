from __future__ import annotations

import argparse
from contextlib import redirect_stderr
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts.validation.models import (
    ValidationFinding,
    ValidationGateResult,
    ValidationRun,
)
from scripts.validation.reporting import (
    DEFAULT_NONPASS_BUDGET_BYTES,
    DEFAULT_PASS_BUDGET_BYTES,
    ReportingOptions,
    add_reporting_arguments,
    console_bytes,
    emit_report,
    options_from_namespace,
    receipt_path,
    render_output,
    render_summary,
    summary_dict,
    write_full_receipt,
)


def make_findings(count: int, *, unicode: bool = False) -> tuple[ValidationFinding, ...]:
    message = "bounded warning" if not unicode else "bounded warning Δ æther 🚀"
    return tuple(
        ValidationFinding(
            finding_id=f"REPORT-WARN-{index:04d}",
            level="WARN",
            code=f"group_{index % 3}",
            message=f"{message} {index}",
        )
        for index in range(count)
    )


def make_run(count: int, *, unicode: bool = False, exit_code: int = 0) -> ValidationRun:
    status = "PASS" if count == 0 else "WARN"
    gate = ValidationGateResult(
        gate_id="compact_reporting",
        status=status,
        severity="blocking",
        exit_code=exit_code,
        findings=make_findings(count, unicode=unicode),
    )
    return ValidationRun(
        run_id="RUN-REPORT-001",
        tree_hash="git-tree-sha1:1111111111111111111111111111111111111111",
        status=status,
        exit_code=exit_code,
        gate_results=(gate,),
        profile="unit-test",
    )


class ValidationModelTests(unittest.TestCase):
    def test_rejects_invalid_or_duplicate_finding_ids(self) -> None:
        with self.assertRaises(ValueError):
            ValidationFinding("lowercase", "WARN", "code", "message")
        finding = ValidationFinding("REPORT-WARN-0001", "WARN", "code", "message")
        with self.assertRaises(ValueError):
            ValidationGateResult("gate", "WARN", findings=(finding, finding))

    def test_run_preserves_explicit_exit_code_and_counts(self) -> None:
        run = make_run(11, exit_code=7)
        self.assertEqual(run.exit_code, 7)
        self.assertEqual(run.finding_count, 11)
        self.assertEqual(run.warning_count, 11)
        self.assertEqual(run.error_count, 0)

    def test_from_gates_uses_canonical_status_priority(self) -> None:
        gates = (
            ValidationGateResult("warn_gate", "WARN"),
            ValidationGateResult("blocked_gate", "BLOCKED_CONFIGURATION", exit_code=2),
        )
        run = ValidationRun.from_gates(
            run_id="RUN-STATUS-001",
            tree_hash="tree",
            exit_code=2,
            gate_results=gates,
        )
        self.assertEqual(run.status, "BLOCKED_CONFIGURATION")

    def test_cache_only_run_aggregates_to_pass(self) -> None:
        run = ValidationRun.from_gates(
            run_id="RUN-CACHE-001",
            tree_hash="tree",
            exit_code=0,
            gate_results=(ValidationGateResult("cache_gate", "CACHE_HIT"),),
        )
        self.assertEqual(run.status, "PASS")


class CompactSummaryTests(unittest.TestCase):
    def test_zero_findings_is_one_line_and_within_pass_budget(self) -> None:
        output = render_summary(make_run(0), Path("receipt.json"))
        self.assertEqual(output.count("\n"), 1)
        self.assertTrue(output.startswith("PASS "))
        self.assertLessEqual(console_bytes(output), DEFAULT_PASS_BUDGET_BYTES)

    def test_finding_boundaries_are_exact(self) -> None:
        for count, more in ((1, 0), (10, 0), (11, 1), (300, 290)):
            with self.subTest(count=count):
                run = make_run(count)
                summary = summary_dict(run, Path("receipt.json"))
                self.assertEqual(len(summary["shown_findings"]), min(count, 10))
                self.assertEqual(summary["more_findings"], more)
                self.assertEqual(summary["counts"]["finding_count"], count)

    def test_three_hundred_findings_stay_within_default_nonpass_budget(self) -> None:
        output = render_summary(make_run(300), Path("receipt.json"))
        self.assertLessEqual(console_bytes(output), DEFAULT_NONPASS_BUDGET_BYTES)
        self.assertIn("more_findings=290", output)

    def test_unicode_is_preserved_and_budgeted_as_utf8(self) -> None:
        output = render_summary(make_run(300, unicode=True), Path("receipt.json"))
        self.assertIn("æther", output)
        self.assertLessEqual(console_bytes(output), DEFAULT_NONPASS_BUDGET_BYTES)
        self.assertEqual(console_bytes("🚀"), 4)

    def test_warning_groups_use_sorted_stable_ids_and_counts(self) -> None:
        summary = summary_dict(make_run(11), Path("receipt.json"))
        self.assertEqual(
            summary["warning_groups"],
            [
                {"stable_id": "group_0", "count": 4},
                {"stable_id": "group_1", "count": 4},
                {"stable_id": "group_2", "count": 3},
            ],
        )

    def test_warning_groups_are_bounded(self) -> None:
        findings = tuple(
            ValidationFinding(
                finding_id=f"REPORT-UNIQUE-{index:04d}",
                level="WARN",
                code=f"unique_{index:04d}",
                message="warning",
            )
            for index in range(300)
        )
        gate = ValidationGateResult("gate", "WARN", findings=findings)
        run = ValidationRun("RUN-GROUPS-001", "tree", "WARN", 0, (gate,))
        summary = summary_dict(run, Path("receipt.json"))
        output = render_summary(run, Path("receipt.json"))
        self.assertEqual(len(summary["warning_groups"]), 10)
        self.assertEqual(summary["more_warning_groups"], 290)
        self.assertLessEqual(console_bytes(output), DEFAULT_NONPASS_BUDGET_BYTES)

    def test_sorting_is_deterministic_across_input_order(self) -> None:
        findings = make_findings(11)
        forward = ValidationGateResult("gate", "WARN", findings=findings)
        reverse = ValidationGateResult("gate", "WARN", findings=tuple(reversed(findings)))
        run_a = ValidationRun("RUN-A", "tree", "WARN", 0, (forward,))
        run_b = ValidationRun("RUN-B", "tree", "WARN", 0, (reverse,))
        shown_a = summary_dict(run_a, Path("receipt"))["shown_findings"]
        shown_b = summary_dict(run_b, Path("receipt"))["shown_findings"]
        ids_a = [finding["finding_id"] for finding in shown_a]
        ids_b = [finding["finding_id"] for finding in shown_b]
        self.assertEqual(ids_a, ids_b)


class ReceiptTests(unittest.TestCase):
    def test_pass_run_can_preserve_297_advisory_findings(self) -> None:
        findings = make_findings(297)
        gate = ValidationGateResult(
            gate_id="task_index_validation",
            status="PASS",
            exit_code=0,
            findings=findings,
        )
        run = ValidationRun(
            run_id="RUN-TASK-INDEX-297",
            tree_hash="working-sha256:" + "1" * 64,
            status="PASS",
            exit_code=0,
            gate_results=(gate,),
            profile="shadow_planner",
        )

        self.assertEqual(run.status, "PASS")
        self.assertEqual(run.warning_count, 297)
        self.assertEqual(len(run.to_full_receipt()["gate_results"][0]["findings"]), 297)

    def test_full_receipt_preserves_all_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_full_receipt(make_run(300), Path(directory))
            receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["counts"]["finding_count"], 300)
        self.assertEqual(len(receipt["gate_results"][0]["findings"]), 300)
        self.assertFalse(receipt["authority"]["physics_claim_authority"])

    def test_receipt_path_is_bounded_under_tree_and_run(self) -> None:
        path = receipt_path(make_run(0), Path(".local/validation-receipts"))
        self.assertEqual(
            path,
            Path(
                ".local/validation-receipts/"
                "git-tree-sha1-1111111111111111111111111111111111111111/"
                "RUN-REPORT-001/full.json"
            ),
        )

    def test_atomic_replace_leaves_no_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_full_receipt(make_run(1), Path(directory))
            leftovers = list(path.parent.glob("*.tmp"))
        self.assertEqual(leftovers, [])

    def test_atomic_replace_failure_is_bounded_and_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = StringIO()
            with mock.patch("scripts.validation.reporting.os.replace", side_effect=OSError("denied")):
                exit_code = emit_report(make_run(0), receipt_root=Path(directory), stream=output)
            leftovers = list(Path(directory).rglob("*.tmp"))
        self.assertEqual(exit_code, 2)
        self.assertEqual(leftovers, [])
        self.assertIn("BLOCKED_CONFIGURATION receipt_write_failed", output.getvalue())
        self.assertLess(console_bytes(output.getvalue()), 512)

    def test_emit_preserves_represented_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = StringIO()
            exit_code = emit_report(make_run(11, exit_code=7), receipt_root=Path(directory), stream=output)
        self.assertEqual(exit_code, 7)
        self.assertIn("findings=11", output.getvalue())


class ReporterModeTests(unittest.TestCase):
    def test_common_flags_are_mutually_exclusive(self) -> None:
        parser = argparse.ArgumentParser()
        add_reporting_arguments(parser)
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["--quiet", "--summary"])

    def test_namespace_maps_every_mode(self) -> None:
        parser = argparse.ArgumentParser()
        add_reporting_arguments(parser)
        expectations = {
            "--summary": "summary",
            "--json-summary": "json-summary",
            "--full-json": "full-json",
            "--receipt": "receipt",
            "--quiet": "quiet",
        }
        for flag, mode in expectations.items():
            with self.subTest(flag=flag):
                self.assertEqual(options_from_namespace(parser.parse_args([flag])).mode, mode)

    def test_json_summary_is_bounded_but_full_json_is_complete(self) -> None:
        run = make_run(300)
        receipt = Path("receipt.json")
        compact = json.loads(render_output(run, receipt, ReportingOptions("json-summary")))
        full = json.loads(render_output(run, receipt, ReportingOptions("full-json")))
        self.assertEqual(len(compact["shown_findings"]), 10)
        self.assertEqual(compact["more_findings"], 290)
        self.assertEqual(len(full["gate_results"][0]["findings"]), 300)

    def test_receipt_and_quiet_modes(self) -> None:
        run = make_run(0)
        receipt = Path("receipt.json")
        self.assertEqual(render_output(run, receipt, ReportingOptions("receipt")), "receipt.json\n")
        self.assertEqual(render_output(run, receipt, ReportingOptions("quiet")), "")


if __name__ == "__main__":
    unittest.main()
