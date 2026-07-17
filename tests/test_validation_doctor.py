from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from scripts.validation import doctor


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "obsidian_wiki" / "mini_repo"
FIXED_TIME = "2099-01-01T00:00:00Z"


def successful_advisory_runner(
    command: list[str] | tuple[str, ...],
    cwd: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    return {
        "command": list(command),
        "cwd": str(cwd),
        "timeout_seconds": timeout_seconds,
        "exit_code": 0,
        "stdout": "",
        "stderr": "",
        "timed_out": False,
    }


class ValidationDoctorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        temporary_root = Path(self.temporary_directory.name)
        self.repo_root = temporary_root / "mini_repo"
        shutil.copytree(FIXTURE_ROOT, self.repo_root)
        self.receipt_root = temporary_root / "receipts"
        self.vault = doctor.memory.vault_root(self.repo_root)
        self.index_path = doctor.memory.memory_index_path(self.repo_root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def prepare_fresh_local_state(self) -> None:
        doctor.memory.write_generated_registries(
            self.repo_root,
            doctor.memory.load_rows_by_registry(self.repo_root),
            FIXED_TIME,
            write_semantic_text=True,
        )
        rows_by_registry = doctor.memory.load_rows_by_registry(self.repo_root)
        doctor.memory.write_vault(self.repo_root, self.vault, rows_by_registry)
        doctor.memory.build_memory_index(self.repo_root, self.index_path)

    def run_doctor(
        self,
        *,
        refresh: bool = False,
        run_id: str = "RUN-DOCTOR-UNIT",
    ) -> tuple[dict[str, object], dict[str, object]]:
        compact, receipt_path, _receipt_sha256 = doctor.run_doctor(
            self.repo_root,
            refresh=refresh,
            vault=self.vault,
            index_path=self.index_path,
            receipt_root=self.receipt_root,
            run_id=run_id,
            advisory_runner=successful_advisory_runner,
        )
        return compact, json.loads(receipt_path.read_text(encoding="utf-8"))

    @staticmethod
    def result_status(receipt: dict[str, object], gate_id: str) -> str:
        results = receipt["results"]
        assert isinstance(results, list)
        return next(
            str(result["status"])
            for result in results
            if isinstance(result, dict) and result.get("gate_id") == gate_id
        )

    def local_state_hashes(self) -> dict[str, str]:
        paths = sorted(
            path
            for root in (self.vault, self.index_path.parent)
            if root.exists()
            for path in ([root] if root.is_file() else root.rglob("*"))
            if path.is_file()
        )
        return {
            path.relative_to(self.repo_root).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in paths
        }

    def nonlocal_state_hashes(self) -> dict[str, str]:
        return {
            path.relative_to(self.repo_root).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in sorted(self.repo_root.rglob("*"))
            if path.is_file()
            and not doctor.is_within(path, self.repo_root / ".local")
        }

    def test_fresh_local_state_passes_with_checkpoint_separation(self) -> None:
        self.prepare_fresh_local_state()

        compact, receipt = self.run_doctor()

        self.assertEqual(compact["status"], "PASS")
        self.assertEqual(compact["core_validation_status"], "PASS")
        self.assertEqual(compact["local_retrieval_status"], "PASS")
        self.assertEqual(compact["warn_count"], 0)
        self.assertFalse(receipt["separation"]["checkpoint_transaction_selected"])
        self.assertEqual(
            receipt["separation"]["doctor_checkpoint_obligation_overlap"], []
        )

    def test_default_run_does_not_mutate_local_retrieval_state(self) -> None:
        self.prepare_fresh_local_state()
        before = self.local_state_hashes()

        compact, receipt = self.run_doctor(run_id="RUN-DOCTOR-READ-ONLY")

        self.assertEqual(compact["status"], "PASS")
        self.assertEqual(before, self.local_state_hashes())
        self.assertTrue(receipt["separation"]["read_only_default"])
        self.assertEqual(
            self.result_status(receipt, "local_retrieval_sync"), "SKIPPED"
        )

    def test_stale_source_warns_without_demoting_core_validation(self) -> None:
        self.prepare_fresh_local_state()
        source = self.repo_root / "README.md"
        source.write_text(
            source.read_text(encoding="utf-8") + "\nStale local mirror probe.\n",
            encoding="utf-8",
        )

        compact, receipt = self.run_doctor(run_id="RUN-DOCTOR-STALE")

        self.assertEqual(compact["status"], "WARN")
        self.assertEqual(compact["core_validation_status"], "PASS")
        self.assertEqual(compact["local_retrieval_status"], "WARN")
        self.assertEqual(
            self.result_status(receipt, "memory_status_diagnostic"), "WARN"
        )
        self.assertEqual(
            self.result_status(receipt, "local_retrieval_lint"), "WARN"
        )

    def test_missing_index_warns_and_preserves_core_pass(self) -> None:
        self.prepare_fresh_local_state()
        self.index_path.unlink()

        compact, receipt = self.run_doctor(run_id="RUN-DOCTOR-MISSING")

        self.assertEqual(compact["status"], "WARN")
        self.assertEqual(compact["core_validation_status"], "PASS")
        self.assertEqual(compact["local_retrieval_status"], "WARN")
        self.assertEqual(
            self.result_status(receipt, "memory_search_diagnostic"), "WARN"
        )

    def test_malformed_index_is_an_advisory_warning(self) -> None:
        self.prepare_fresh_local_state()
        self.index_path.write_bytes(b"not a SQLite database")

        compact, receipt = self.run_doctor(run_id="RUN-DOCTOR-MALFORMED")

        self.assertEqual(compact["status"], "WARN")
        self.assertEqual(compact["core_validation_status"], "PASS")
        self.assertEqual(
            self.result_status(receipt, "memory_search_diagnostic"), "WARN"
        )

    def test_explicit_refresh_rebuilds_missing_local_state(self) -> None:
        self.prepare_fresh_local_state()
        shutil.rmtree(self.vault)
        self.index_path.unlink()
        before_nonlocal = self.nonlocal_state_hashes()

        compact, receipt = self.run_doctor(
            refresh=True,
            run_id="RUN-DOCTOR-REFRESH",
        )

        self.assertEqual(compact["status"], "PASS")
        self.assertTrue(self.vault.is_dir())
        self.assertTrue(self.index_path.is_file())
        self.assertEqual(before_nonlocal, self.nonlocal_state_hashes())
        self.assertEqual(
            self.result_status(receipt, "local_retrieval_sync"), "PASS"
        )
        self.assertFalse(receipt["separation"]["read_only_default"])

    def test_refresh_rejects_targets_outside_local_before_writing(self) -> None:
        unsafe_vault = self.repo_root / "tracked-vault"

        result = doctor.refresh_diagnostic(
            self.repo_root,
            unsafe_vault,
            self.index_path,
            requested=True,
        )

        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(unsafe_vault.exists())

    def test_search_failure_is_an_advisory_warning(self) -> None:
        self.prepare_fresh_local_state()
        with mock.patch.object(
            doctor.memory,
            "search_index",
            side_effect=RuntimeError("synthetic search failure"),
        ):
            compact, receipt = self.run_doctor(run_id="RUN-DOCTOR-SEARCH-FAIL")

        self.assertEqual(compact["status"], "WARN")
        self.assertEqual(compact["core_validation_status"], "PASS")
        self.assertEqual(
            self.result_status(receipt, "memory_search_diagnostic"), "WARN"
        )

    def test_requested_refresh_failure_is_a_maintenance_failure(self) -> None:
        self.prepare_fresh_local_state()
        with mock.patch.object(
            doctor,
            "refresh_local_retrieval",
            side_effect=RuntimeError("synthetic refresh failure"),
        ):
            compact, receipt = self.run_doctor(
                refresh=True,
                run_id="RUN-DOCTOR-REFRESH-FAIL",
            )

        self.assertEqual(compact["status"], "FAIL")
        self.assertEqual(
            self.result_status(receipt, "local_retrieval_sync"), "FAIL"
        )

    def test_json_cli_output_is_one_compact_line(self) -> None:
        compact = {
            "schema_id": "validation_doctor_compact_summary_v1",
            "status": "WARN",
            "scope": "local_retrieval",
            "check_count": 10,
            "warn_count": 1,
            "fail_count": 0,
        }
        output = io.StringIO()
        with mock.patch.object(
            doctor,
            "run_doctor",
            return_value=(compact, Path(".local/receipt.json"), "abc"),
        ), redirect_stdout(output):
            exit_code = doctor.main(["--json"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(output.getvalue().splitlines()), 1)
        self.assertEqual(json.loads(output.getvalue()), compact)


if __name__ == "__main__":
    unittest.main()
