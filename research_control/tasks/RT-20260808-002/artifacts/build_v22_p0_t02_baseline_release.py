#!/usr/bin/env python3
"""Build the deterministic V22 P0-T02 internal V21 baseline release.

The scientific payload is read from one immutable Git commit.  This builder
does not edit canonical sources, create a tag, publish a release, or infer any
scientific authority from successful packaging or reproduction.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import fitz


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
CREATED_AT = "2026-08-08T21:32:43Z"
BASELINE_COMMIT = "233e5dd7024fc068032d0afe86d85dc25e2246e9"
BASELINE_TREE = "a7d9c9448de8e204643b093878ba4d84bd58f020"
BASELINE_FINGERPRINT = "f513b6995a1c9c1e408541ef52f78e5d4c5155a2079ec200eca2ff54ac62a9f6"
ASSEMBLY_COMMIT = "bdde326629fd8b1f20e7d32e4c26b1c0f32e8c9a"
PROPOSED_TAG = "v21-scientific-baseline-233e5dd7"
SOURCE_DATE_EPOCH = "1785842868"

OUTPUT_PATHS = {
    "manifest": ARTIFACT_DIR / "v21_terminal_baseline_release_manifest_v1.json",
    "partition": ARTIFACT_DIR / "v21_terminal_baseline_canonical_derivative_partition_v1.json",
    "reproduction": ARTIFACT_DIR / "v21_terminal_baseline_reproduction_receipt_v1.json",
    "freeze_policy": ARTIFACT_DIR / "v21_terminal_baseline_freeze_policy_v1.md",
    "release_notes": ARTIFACT_DIR / "v21_terminal_baseline_release_notes_v1.md",
    "proposed_tag": ARTIFACT_DIR / "v21_terminal_baseline_proposed_tag_v1.yaml",
    "archive": ARTIFACT_DIR / "v21_terminal_scientific_baseline_release_candidate_v1.tar",
    "catalog": ARTIFACT_DIR / "v21_terminal_baseline_release_catalog_v1.json",
}

REGISTRY_PATHS = {
    "tex": "registries/TEX_SOURCE_REGISTRY.csv",
    "markdown": "registries/MARKDOWN_SOURCE_REGISTRY.csv",
    "pdf": "registries/PDF_DERIVATIVE_REGISTRY.csv",
    "html": "registries/HTML_EXPLAINER_REGISTRY.csv",
    "wiki": "registries/WIKI_ARTIFACT_REGISTRY.csv",
}

CURATED_PREFIXES: dict[str, tuple[str, ...]] = {
    "distance_to_gr": ("registries/DISTANCE_TO_GR_LEDGER.csv",),
    "gate_a": ("research_control/tasks/RT-20260724-004/artifacts",),
    "selector_theorem_and_proof_archive": (
        "research_control/tasks/RT-20260723-003/artifacts",
        "research_control/tasks/RT-20260720-018/artifacts/proof",
    ),
    "p5_p6_negative_results_and_gate_b": (
        "research_control/tasks/RT-20260726-001/artifacts",
        "research_control/tasks/RT-20260727-004/artifacts",
    ),
    "p7_postulate_ledger_and_gate_c": (
        "research_control/tasks/RT-20260729-001/artifacts",
    ),
    "p8_obstruction_and_gate_d": (
        "research_control/tasks/RT-20260729-011/artifacts",
    ),
    "p9_benchmarks_and_gate_e": (
        "research_control/tasks/RT-20260731-001/artifacts",
        "research_control/tasks/RT-20260731-004/artifacts",
    ),
    "p13_validation_environment_and_provenance": (
        "research_control/tasks/RT-20260724-003/artifacts",
        "research_control/tasks/RT-20260723-019/artifacts",
        "research_control/tasks/RT-20260724-002/artifacts",
    ),
    "p15_reproducibility_packages": (
        "research_control/tasks/RT-20260802-009/artifacts",
    ),
    "p16_final_scorecards_and_work_ledger": (
        "research_control/tasks/RT-20260804-003/artifacts",
        "research_control/tasks/RT-20260804-004/artifacts",
    ),
}

ASSEMBLY_INPUTS = (
    "research_control/handoffs/handoff-0967.yaml",
    "research_control/tasks/RT-20260808-001/artifacts/v21_terminal_to_v22_intake_bridge_receipt.json",
    "research_control/tasks/RT-20260808-001/jobs/completions/AJC-AJ-RT-20260808-001-001.yaml",
)

SELECTOR_VALIDATOR = (
    "research_control/tasks/RT-20260723-003/artifacts/"
    "validate_selector_minimum_extension_manuscript.py"
)
SELECTOR_MANUSCRIPT = (
    "research_control/tasks/RT-20260723-003/artifacts/"
    "selector_minimum_extension_theorem_manuscript_v1.tex"
)
LEAN_SOURCE = (
    "research_control/tasks/RT-20260720-018/artifacts/proof/SelectorKernel.lean"
)
LEAN_BUILD = (
    "research_control/tasks/RT-20260720-018/artifacts/proof/build_proof.sh"
)
LEAN_BINARY = (
    ROOT
    / ".local/rt-20260720-018-lean/toolchain/"
    "lean-4.30.0-darwin_aarch64/bin/lean"
)
EXPECTED_LEAN_BINARY_SHA256 = (
    "b48bc5ab229bd8b320a224b87e20fc428dba6fa8a1c054bd4fa6def846e19997"
)
EXPECTED_LEAN_SOURCE_SHA256 = (
    "6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356"
)
EXPECTED_LEAN_OBJECT_SHA256 = (
    "3fff7e0bff2e331400ba52305a2f34e3deb93f2b85ac1e3850a1625ef6bd468a"
)
PYTHON_MODEL = (
    "research_control/tasks/RT-20260727-006/artifacts/"
    "source_dynamics_reconstruction_model_archive_v1.py"
)
BENCHMARK_VALIDATOR = (
    "research_control/tasks/RT-20260731-001/artifacts/"
    "validate_p9_t08_benchmark_audit.py"
)
P13_ENVIRONMENT = (
    "research_control/tasks/RT-20260724-003/artifacts/"
    "reproducible_environment_definition.json"
)
P13_REPRODUCTION = (
    "research_control/tasks/RT-20260724-003/artifacts/reproduction_receipt.json"
)
SELECTOR_SOURCE_BUNDLE = (
    "research_control/tasks/RT-20260802-009/artifacts/"
    "p15_t03_selector_theorem_source_bundle_v1.tar"
)


def run_git(*args: str) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def git_bytes(ref: str, path: str) -> bytes:
    return run_git("show", f"{ref}:{path}")


def git_paths(ref: str, prefix: str) -> tuple[str, ...]:
    output = run_git("ls-tree", "-r", "--name-only", ref, "--", prefix)
    return tuple(
        line
        for line in output.decode("utf-8").splitlines()
        if line and "__pycache__" not in line and not line.endswith(".pyc")
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def registry_rows(path: str) -> list[dict[str, str]]:
    raw = git_bytes(BASELINE_COMMIT, path).decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw)))


def safe_relative_path(path: str) -> bool:
    pure = PurePosixPath(path)
    return bool(path) and not pure.is_absolute() and ".." not in pure.parts


def split_declared_paths(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(";") if item.strip())


def verify_git_hash(ref: str, path: str, expected: str) -> bytes:
    if not safe_relative_path(path):
        raise ValueError(f"unsafe repository path: {path!r}")
    data = git_bytes(ref, path)
    actual = sha256_bytes(data)
    if actual != expected:
        raise ValueError(
            f"hash mismatch at {ref}:{path}: expected={expected} actual={actual}"
        )
    return data


def add_archive_member(
    members: dict[str, bytes],
    archive_path: str,
    data: bytes,
) -> None:
    if not safe_relative_path(archive_path):
        raise ValueError(f"unsafe archive path: {archive_path!r}")
    previous = members.get(archive_path)
    if previous is not None and previous != data:
        raise ValueError(f"conflicting archive bytes: {archive_path}")
    members[archive_path] = data


def source_entry(row: dict[str, str], registry: str) -> dict[str, Any]:
    path = row["path"]
    data = verify_git_hash(BASELINE_COMMIT, path, row["source_hash"])
    return {
        "object_id": row["object_id"],
        "path": path,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "registry_path": registry,
        "format": row.get("format", ""),
        "role": row.get("role", ""),
        "authority_status": row.get("authority_status", ""),
        "validation_status": row.get("validation_status", ""),
    }


def derivative_entry(
    row: dict[str, str],
    registry: str,
    expected_hash_fields: Iterable[str],
    source_ids: Iterable[str],
) -> dict[str, Any]:
    path = row["path"]
    data = git_bytes(BASELINE_COMMIT, path)
    actual = sha256_bytes(data)
    for field in expected_hash_fields:
        expected = row.get(field, "").strip()
        if expected and expected != actual:
            raise ValueError(
                f"{registry}:{row.get('object_id')} {field} mismatch: "
                f"expected={expected} actual={actual}"
            )
    return {
        "object_id": row["object_id"],
        "path": path,
        "sha256": actual,
        "bytes": len(data),
        "registry_path": registry,
        "format": row.get("format", ""),
        "authority_status": row.get("authority_status", ""),
        "source_object_ids": sorted({item for item in source_ids if item}),
        "validation_status": row.get("validation_status", ""),
    }


def build_inventory() -> tuple[dict[str, Any], dict[str, Any], dict[str, bytes]]:
    terminal_commit = run_git("rev-parse", f"{BASELINE_COMMIT}^{{commit}}").decode().strip()
    terminal_tree = run_git("rev-parse", f"{BASELINE_COMMIT}^{{tree}}").decode().strip()
    if terminal_commit != BASELINE_COMMIT or terminal_tree != BASELINE_TREE:
        raise ValueError("terminal V21 commit or tree identity mismatch")

    tex_rows = registry_rows(REGISTRY_PATHS["tex"])
    markdown_rows = registry_rows(REGISTRY_PATHS["markdown"])
    pdf_rows = registry_rows(REGISTRY_PATHS["pdf"])
    html_rows = registry_rows(REGISTRY_PATHS["html"])
    wiki_rows = registry_rows(REGISTRY_PATHS["wiki"])

    sources = [
        source_entry(row, REGISTRY_PATHS["tex"]) for row in tex_rows
    ] + [
        source_entry(row, REGISTRY_PATHS["markdown"]) for row in markdown_rows
    ]
    object_index: dict[str, dict[str, Any]] = {
        item["object_id"]: item for item in sources
    }
    if len(object_index) != len(sources):
        raise ValueError("duplicate canonical source object ID")

    pdf_derivatives: list[dict[str, Any]] = []
    for row in pdf_rows:
        source_id = row.get("source_tex_object_id", "")
        item = derivative_entry(
            row,
            REGISTRY_PATHS["pdf"],
            ("source_hash", "pdf_hash"),
            (source_id,),
        )
        source = object_index.get(source_id)
        if source is None:
            raise ValueError(f"PDF source object missing: {source_id}")
        if row.get("source_tex_path") != source["path"]:
            raise ValueError(f"PDF source path mismatch: {row['object_id']}")
        if row.get("source_tex_hash") != source["sha256"]:
            raise ValueError(f"PDF source hash mismatch: {row['object_id']}")
        pdf_derivatives.append(item)
        object_index[item["object_id"]] = item

    html_derivatives: list[dict[str, Any]] = []
    for row in html_rows:
        source_id = row.get("source_basis", "")
        item = derivative_entry(
            row,
            REGISTRY_PATHS["html"],
            ("source_hash", "html_hash"),
            (source_id,),
        )
        source = object_index.get(source_id)
        if source is None:
            raise ValueError(f"HTML source object missing: {source_id}")
        if row.get("source_basis_hash") != source["sha256"]:
            raise ValueError(f"HTML source hash mismatch: {row['object_id']}")
        html_derivatives.append(item)
        object_index[item["object_id"]] = item

    wiki_derivatives: list[dict[str, Any]] = []
    for row in wiki_rows:
        source_id = row.get("source_object_id", "")
        item = derivative_entry(
            row,
            REGISTRY_PATHS["wiki"],
            ("source_hash", "wiki_hash"),
            (source_id,),
        )
        source = object_index.get(source_id)
        if source is None:
            raise ValueError(f"wiki source object missing: {source_id}")
        if row.get("source_path") != source["path"]:
            raise ValueError(f"wiki source path mismatch: {row['object_id']}")
        if row.get("source_object_hash") != source["sha256"]:
            raise ValueError(f"wiki source hash mismatch: {row['object_id']}")
        wiki_derivatives.append(item)
        object_index[item["object_id"]] = item

    derivatives = pdf_derivatives + html_derivatives + wiki_derivatives
    derivative_paths = {item["path"] for item in derivatives}
    declared_generated_paths: set[str] = set()
    declared_sources: dict[str, set[str]] = defaultdict(set)
    for row in tex_rows + markdown_rows + pdf_rows + html_rows:
        for path in split_declared_paths(row.get("generated_outputs", "")):
            declared_generated_paths.add(path)
            declared_sources[path].add(row["object_id"])
    for row in tex_rows:
        if row.get("pdf_path", "").strip():
            path = row["pdf_path"].strip()
            declared_generated_paths.add(path)
            declared_sources[path].add(row["object_id"])
    missing_declared = sorted(declared_generated_paths - derivative_paths)
    declared_control_derivatives: list[dict[str, Any]] = []
    for path in missing_declared:
        data = git_bytes(BASELINE_COMMIT, path)
        item = {
            "object_id": "DECLARED-GENERATED-" + sha256_bytes(path.encode())[:20].upper(),
            "path": path,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "registry_path": "declared_by_registered_source.generated_outputs",
            "format": Path(path).suffix.lstrip(".") or "generated_report",
            "authority_status": "generated_noncanonical",
            "source_object_ids": sorted(declared_sources[path]),
            "validation_status": "PASS_SOURCE_DECLARATION_TRACE",
        }
        declared_control_derivatives.append(item)
    derivatives.extend(declared_control_derivatives)
    derivative_paths.update(item["path"] for item in declared_control_derivatives)

    archive_members: dict[str, bytes] = {}
    repository_paths: dict[str, dict[str, Any]] = {}

    def add_repository_path(path: str, classes: Iterable[str]) -> None:
        data = git_bytes(BASELINE_COMMIT, path)
        item = repository_paths.setdefault(
            path,
            {
                "path": path,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "classes": [],
            },
        )
        item["classes"] = sorted(set(item["classes"]) | set(classes))
        add_archive_member(archive_members, f"repository/{path}", data)

    for item in sources:
        add_repository_path(item["path"], ("registered_canonical_source",))
    for item in derivatives:
        add_repository_path(item["path"], ("registered_generated_derivative",))
    for path in git_paths(BASELINE_COMMIT, "registries"):
        add_repository_path(path, ("canonical_control_registry",))

    curated_categories: dict[str, list[dict[str, Any]]] = {}
    for category, prefixes in CURATED_PREFIXES.items():
        category_paths: set[str] = set()
        for prefix in prefixes:
            category_paths.update(git_paths(BASELINE_COMMIT, prefix))
        if not category_paths:
            raise ValueError(f"curated category has no terminal files: {category}")
        entries: list[dict[str, Any]] = []
        for path in sorted(category_paths):
            data = git_bytes(BASELINE_COMMIT, path)
            add_repository_path(path, (f"curated_evidence:{category}",))
            entries.append(
                {
                    "path": path,
                    "sha256": sha256_bytes(data),
                    "bytes": len(data),
                }
            )
        curated_categories[category] = entries

    assembly_inputs: list[dict[str, Any]] = []
    for path in ASSEMBLY_INPUTS:
        data = git_bytes(ASSEMBLY_COMMIT, path)
        archive_path = f"release-control/assembly-inputs/{path}"
        add_archive_member(archive_members, archive_path, data)
        assembly_inputs.append(
            {
                "path": path,
                "source_commit": ASSEMBLY_COMMIT,
                "archive_path": archive_path,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
            }
        )

    source_counts = {
        "tex": len(tex_rows),
        "markdown": len(markdown_rows),
        "total": len(sources),
    }
    derivative_counts = {
        "pdf": len(pdf_derivatives),
        "html": len(html_derivatives),
        "wiki": len(wiki_derivatives),
        "declared_control_report": len(declared_control_derivatives),
        "total": len(derivatives),
    }
    partition = {
        "schema_id": "v21_terminal_baseline_canonical_derivative_partition_v1",
        "task_id": "RT-20260808-002",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "canonical_source_counts": source_counts,
        "derivative_counts": derivative_counts,
        "declared_generated_path_count": len(declared_generated_paths),
        "unresolved_declared_generated_paths": [],
        "canonical_sources": sorted(sources, key=lambda item: item["object_id"]),
        "derivatives": sorted(derivatives, key=lambda item: item["object_id"]),
        "traceability": {
            "every_derivative_has_registered_source": all(
                item["source_object_ids"] for item in derivatives
            ),
            "every_declared_generated_path_has_derivative_row": True,
            "generated_artifacts_are_independent_authority": False,
        },
        "authority_limits": {
            "canonical_sources_modified": False,
            "generated_derivative_authority_created": False,
            "scientific_status_changed": False,
            "physics_promotion_authorized": False,
        },
    }

    manifest = {
        "schema_id": "v21_terminal_baseline_release_manifest_v1",
        "release_candidate_id": "V21-TERMINAL-SCIENTIFIC-BASELINE-233E5DD7",
        "task_id": "RT-20260808-002",
        "job_id": "AJ-RT-20260808-002-001",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "status": "INTERNAL_IMMUTABLE_BASELINE_CANDIDATE",
        "baseline": {
            "commit": BASELINE_COMMIT,
            "tree": BASELINE_TREE,
            "terminal_goal_fingerprint": BASELINE_FINGERPRINT,
            "proposed_tag": PROPOSED_TAG,
            "tag_created": False,
            "public_release_created": False,
        },
        "canonical_source_counts": source_counts,
        "derivative_counts": derivative_counts,
        "registry_hashes": {
            key: sha256_bytes(git_bytes(BASELINE_COMMIT, path))
            for key, path in sorted(REGISTRY_PATHS.items())
        },
        "repository_archive_inventory": sorted(
            repository_paths.values(), key=lambda item: item["path"]
        ),
        "curated_evidence_categories": curated_categories,
        "assembly_provenance_inputs": assembly_inputs,
        "scientific_status": {
            "Gate_A": "ADOPTED_NARROW_RESEARCH_ARCHITECTURE",
            "Gate_B": "NOT_READY",
            "Gate_C": "PROTECTED_SOURCE_MATTER_PACKAGE_ADOPTED_BY_POSTULATE",
            "Gate_D": "NOT_READY",
            "Gate_E": "NOT_READY",
            "benchmark_case_count": 6,
            "benchmark_inconclusive_count": 6,
            "benchmark_pass_count": 0,
            "independent_replication_count": 0,
            "first_principles_gr_derivation_status": "OPEN_NOT_COMPLETED",
            "gr_source_derived": False,
        },
        "authority_limits": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "proof_authority": False,
            "external_review_completed": False,
            "independent_replication_completed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "tag_creation_authorized": False,
            "public_release_authorized": False,
            "publication_authorized": False,
            "push_authorized": False,
            "external_action_authorized": False,
            "completed_derivation_authorized": False,
        },
    }
    return manifest, partition, archive_members


def sanitized(data: bytes, temp_root: Path) -> bytes:
    return data.replace(str(temp_root).encode("utf-8"), b"{TEMP_ROOT}")


def parse_json_output(data: bytes) -> dict[str, Any]:
    text = data.decode("utf-8", errors="replace").strip()
    if not text:
        return {}
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        start = text.rfind("\n{")
        if start >= 0:
            try:
                value = json.loads(text[start + 1 :])
                return value if isinstance(value, dict) else {}
            except json.JSONDecodeError:
                return {}
    return {}


def command_receipt(
    *,
    profile_id: str,
    display_command: list[str],
    actual_command: list[str],
    cwd: Path,
    temp_root: Path,
    env: dict[str, str] | None = None,
) -> tuple[dict[str, Any], subprocess.CompletedProcess[bytes]]:
    result = subprocess.run(
        actual_command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    stdout = sanitized(result.stdout, temp_root)
    stderr = sanitized(result.stderr, temp_root)
    receipt = {
        "profile_id": profile_id,
        "command": display_command,
        "exit_code": result.returncode,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout_bytes": len(stdout),
        "stdout_sha256": sha256_bytes(stdout),
        "stderr_bytes": len(stderr),
        "stderr_sha256": sha256_bytes(stderr),
    }
    if result.returncode != 0:
        receipt["failure_stdout_excerpt"] = stdout.decode(
            "utf-8", errors="replace"
        )[-2000:]
        receipt["failure_stderr_excerpt"] = stderr.decode(
            "utf-8", errors="replace"
        )[-2000:]
    parsed = parse_json_output(result.stdout)
    if parsed:
        receipt["reported_status"] = parsed.get("status", "")
        for key in (
            "check_count",
            "failed_check_count",
            "error_count",
            "executed_case_count",
            "inconclusive_case_count",
            "benchmark_pass_count",
        ):
            if key in parsed:
                receipt[key] = parsed[key]
    return receipt, result


def extract_terminal_tree(target: Path) -> dict[str, Any]:
    raw = run_git("archive", "--format=tar", BASELINE_COMMIT)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        unsafe = [
            item.name
            for item in members
            if not safe_relative_path(item.name)
            or not (item.isfile() or item.isdir() or item.issym())
        ]
        if unsafe:
            raise ValueError(f"unsafe terminal git archive members: {unsafe[:10]}")
        archive.extractall(target, filter="data")
    forbidden = [
        path
        for path in (target / ".git", target / ".local", target / ".venv")
        if path.exists()
    ]
    if forbidden:
        raise ValueError("clean extraction contains forbidden local state")
    return {
        "git_archive_sha256": sha256_bytes(raw),
        "git_archive_bytes": len(raw),
        "member_count": len(members),
        "git_metadata_embedded": False,
        "local_cache_embedded": False,
        "virtual_environment_embedded": False,
    }


def extract_regular_tar(source: Path, target: Path) -> dict[str, Any]:
    raw = source.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        members = archive.getmembers()
        unsafe = [
            item.name
            for item in members
            if not safe_relative_path(item.name) or not item.isfile()
        ]
        if unsafe:
            raise ValueError(f"unsafe source-bundle members: {unsafe[:10]}")
        archive.extractall(target, filter="data")
    return {
        "archive_sha256": sha256_bytes(raw),
        "archive_bytes": len(raw),
        "member_count": len(members),
    }


def build_reproduction_receipt() -> dict[str, Any]:
    # Preserve the virtual-environment and TeX format-selecting invocation
    # paths. Resolving either symlink would bypass the venv or invoke pdftex
    # as plain TeX instead of selecting the pdflatex format.
    python_executable = Path(sys.executable)
    pdflatex_text = shutil.which("pdflatex")
    if pdflatex_text is None:
        raise ValueError("pdflatex is not available")
    pdflatex = Path(pdflatex_text)
    if not LEAN_BINARY.is_file():
        raise ValueError(f"pinned Lean binary missing: {LEAN_BINARY}")
    if sha256_path(LEAN_BINARY) != EXPECTED_LEAN_BINARY_SHA256:
        raise ValueError("pinned Lean binary hash mismatch")

    profiles: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="v22-p0-t02-clean-source-") as temp_name:
        temp_root = Path(temp_name)
        extracted = temp_root / "terminal-v21"
        extracted.mkdir()
        extraction = extract_terminal_tree(extracted)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
        env["TZ"] = "UTC"
        env.pop("PYTHONPATH", None)

        selector_root = temp_root / "selector-qualifying-source-snapshot"
        selector_root.mkdir()
        selector_bundle = extract_regular_tar(
            extracted / SELECTOR_SOURCE_BUNDLE, selector_root
        )
        theorem, _ = command_receipt(
            profile_id="selector_theorem_validator",
            display_command=[
                "{python}",
                SELECTOR_VALIDATOR,
                "--check",
                "--json",
            ],
            actual_command=[
                str(python_executable),
                str(selector_root / SELECTOR_VALIDATOR),
                "--check",
                "--json",
            ],
            cwd=selector_root,
            temp_root=temp_root,
            env=env,
        )
        changed_source_paths: list[dict[str, Any]] = []
        for path in (
            "ontology/tex/aether_flow_foundations.tex",
            "ontology/tex/aether_flow_geometry.tex",
        ):
            terminal_hash = sha256_path(extracted / path)
            snapshot_hash = sha256_path(selector_root / path)
            changed_source_paths.append(
                {
                    "path": path,
                    "terminal_baseline_sha256": terminal_hash,
                    "qualifying_source_snapshot_sha256": snapshot_hash,
                    "hashes_differ": terminal_hash != snapshot_hash,
                }
            )
        theorem.update(
            {
                "source_snapshot_class": "p15_t03_qualifying_source_bundle",
                "source_bundle_path": SELECTOR_SOURCE_BUNDLE,
                "source_bundle_sha256": selector_bundle["archive_sha256"],
                "source_bundle_member_count": selector_bundle["member_count"],
                "terminal_source_deltas": changed_source_paths,
                "disclosure": "The theorem validator is reproduced against its immutable qualifying P15-T03 source-snapshot bundle. Later terminal ontology-source bytes differ for two declared inputs, so running the historical validator directly against the terminal tree fails closed. The snapshot result does not overwrite or reinterpret either lineage.",
            }
        )
        profiles.append(theorem)

        lean_output = temp_root / "lean-output"
        lean_output.mkdir()
        lean, _ = command_receipt(
            profile_id="lean_selector_kernel_build",
            display_command=[
                "sh",
                LEAN_BUILD,
                "{pinned_lean_4.30.0}",
                "{external_output_dir}",
            ],
            actual_command=[
                "sh",
                str(extracted / LEAN_BUILD),
                str(LEAN_BINARY),
                str(lean_output),
            ],
            cwd=extracted,
            temp_root=temp_root,
            env=env,
        )
        lean_source_hash = sha256_path(extracted / LEAN_SOURCE)
        lean_object = lean_output / "SelectorKernel.olean"
        lean_object_hash = sha256_path(lean_object) if lean_object.is_file() else ""
        lean.update(
            {
                "source_sha256": lean_source_hash,
                "expected_source_sha256": EXPECTED_LEAN_SOURCE_SHA256,
                "proof_object_sha256": lean_object_hash,
                "expected_proof_object_sha256": EXPECTED_LEAN_OBJECT_SHA256,
                "proof_object_reproduced": (
                    lean_source_hash == EXPECTED_LEAN_SOURCE_SHA256
                    and lean_object_hash == EXPECTED_LEAN_OBJECT_SHA256
                ),
            }
        )
        if not lean["proof_object_reproduced"]:
            lean["status"] = "FAIL"
        profiles.append(lean)

        tex_output = temp_root / "tex-output"
        tex_output.mkdir()
        manuscript = extracted / SELECTOR_MANUSCRIPT
        tex, _ = command_receipt(
            profile_id="selector_manuscript_tex_build",
            display_command=[
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                "{external_output_dir}",
                SELECTOR_MANUSCRIPT,
            ],
            actual_command=[
                str(pdflatex),
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(tex_output),
                str(manuscript),
            ],
            cwd=manuscript.parent,
            temp_root=temp_root,
            env=env,
        )
        pdf_path = tex_output / f"{manuscript.stem}.pdf"
        page_count = 0
        if pdf_path.is_file():
            with fitz.open(pdf_path) as document:
                page_count = document.page_count
        tex.update(
            {
                "source_sha256": sha256_path(manuscript),
                "pdf_created": pdf_path.is_file(),
                "page_count": page_count,
                "stdout_capture": "excluded_from_deterministic_receipt_because_pdftex_runtime_identifiers_vary; exit status source hash and rendered page count are retained",
            }
        )
        tex.pop("stdout_bytes", None)
        tex.pop("stdout_sha256", None)
        if not pdf_path.is_file() or page_count <= 0:
            tex["status"] = "FAIL"
        profiles.append(tex)

        model, _ = command_receipt(
            profile_id="source_dynamics_python_model",
            display_command=["{python}", PYTHON_MODEL, "--json"],
            actual_command=[
                str(python_executable),
                str(extracted / PYTHON_MODEL),
                "--json",
            ],
            cwd=extracted,
            temp_root=temp_root,
            env=env,
        )
        profiles.append(model)

        benchmark, _ = command_receipt(
            profile_id="p9_benchmark_audit_validator",
            display_command=["{python}", BENCHMARK_VALIDATOR, "--check", "--json"],
            actual_command=[
                str(python_executable),
                str(extracted / BENCHMARK_VALIDATOR),
                "--check",
                "--json",
            ],
            cwd=extracted,
            temp_root=temp_root,
            env=env,
        )
        profiles.append(benchmark)

    passed = sum(item["status"] == "PASS" for item in profiles)
    failed = [item["profile_id"] for item in profiles if item["status"] != "PASS"]
    p13_environment = git_bytes(BASELINE_COMMIT, P13_ENVIRONMENT)
    p13_reproduction = git_bytes(BASELINE_COMMIT, P13_REPRODUCTION)
    return {
        "schema_id": "v21_terminal_baseline_reproduction_receipt_v1",
        "task_id": "RT-20260808-002",
        "job_id": "AJ-RT-20260808-002-001",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "status": "PASS" if not failed else "COMPLETE_WITH_DISCLOSED_FAILURES",
        "profile_count": len(profiles),
        "passed_profile_count": passed,
        "failed_profile_count": len(failed),
        "failed_profile_ids": failed,
        "source_environment": {
            "target_class": "external_ephemeral_directory",
            "source_tree_materialization": "git_archive_of_pinned_terminal_commit",
            **extraction,
        },
        "runtime": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable_sha256": sha256_path(python_executable),
            "lean_version": "4.30.0",
            "lean_binary_sha256": EXPECTED_LEAN_BINARY_SHA256,
            "pdflatex_version": subprocess.run(
                [str(pdflatex), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            ).stdout.decode("utf-8", errors="replace").splitlines()[0],
            "p13_environment_definition_sha256": sha256_bytes(p13_environment),
            "p13_prior_fresh_environment_receipt_sha256": sha256_bytes(p13_reproduction),
            "limitation": "The source tree is newly materialized outside the checkout. The active hash-locked repository Python runtime and the previously pinned local Lean binary are reused; the prior P13 fresh-environment receipt remains the independent dependency-provisioning evidence.",
        },
        "profiles": profiles,
        "failure_disclosure": {
            "required": bool(failed),
            "exact_failed_profile_ids": failed,
            "suppressed_failure_count": 0,
        },
        "authority_limits": {
            "reproduction_pass_is_operational_evidence_only": True,
            "theorem_truth_inferred": False,
            "external_review_completed": False,
            "independent_replication_completed": False,
            "benchmark_promotion_authorized": False,
            "physics_promotion_authorized": False,
            "publication_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def freeze_policy_bytes() -> bytes:
    return f"""<!-- authority: control -->

# V21 terminal scientific baseline freeze policy

Status: internal release-control policy for the immutable baseline at
`{BASELINE_COMMIT}` / tree `{BASELINE_TREE}`. This policy does not create a
Git tag, public release, publication decision, scientific promotion, or
permission for outward action.

## Frozen lineage

The original terminal commit, tree, release manifest, archive, and receipts
remain immutable. A later correction must never rewrite, replace, amend, or
silently regenerate the frozen baseline under the same identity.

## Only qualifying exception

A baseline-lineage change may be proposed only for a demonstrated security or
reproducibility defect. Scientific disagreement, revised interpretation,
new evidence, prose preference, formatting drift, convenience, or a desired
positive result is not a freeze exception.

A qualifying repair requires all of the following:

1. a tracked defect record with exact affected paths and hashes;
2. reproducible evidence of the security or reproducibility defect;
3. a distinct superseding release record with a new identity and manifest;
4. an explicit mapping from every changed byte to the defect;
5. preservation of the original baseline and its negative scientific status;
6. the normal governed validation and checkpoint transaction; and
7. separate human authority before any tag or public-release execution.

The superseding record may state that it repairs a defect. It may not imply
that V21 derived GR, passed a benchmark, acquired independent replication,
completed external review, or gained publication authority.
""".encode("utf-8")


def release_notes_bytes() -> bytes:
    return f"""<!-- authority: control -->

# V21 terminal scientific baseline — internal release candidate

Proposed tag: `{PROPOSED_TAG}`. The tag has **not** been created. No public
release, push, submission, reviewer contact, publication, or other outward
action is authorized by this package.

## What this baseline establishes

This archive pins the exact terminal V21 commit `{BASELINE_COMMIT}` and tree
`{BASELINE_TREE}`. It provides complete registered TeX and Markdown source
hash closure, traceable generated PDF/HTML/wiki derivatives, curated Gate and
Distance-to-GR evidence, selected clean-source reproduction, and immutable
release-control metadata.

These are internal provenance and reproducibility results. Same-context AI
critique is not external human review, and the selected reproductions are not
qualifying independent scientific replication.

## Exact scientific status

- Gate A: `ADOPTED_NARROW_RESEARCH_ARCHITECTURE`; this is not adoption of
  physical spacetime or source dynamics.
- Gate B: `NOT_READY`.
- Gate C: `PROTECTED_SOURCE_MATTER_PACKAGE_ADOPTED_BY_POSTULATE`; it remains
  a protected constitutive postulate and is not a source derivation.
- Gate D: `NOT_READY`.
- Gate E: `NOT_READY`.
- Benchmarks: six inconclusive, zero pass, zero independent replication.
- First-principles GR derivation: `OPEN_NOT_COMPLETED`; GR is not source-derived.

The exact-GR target-side benchmark remains available for comparison. This
does not establish an unscoped effective metric, universal matter coupling,
Einstein-equation derivation, positive benchmark result, empirical novelty,
external validation, or completed derivation.

## Freeze rule

The baseline is immutable. Only a demonstrated security or reproducibility
defect may support a distinct superseding record, and the original baseline
must remain preserved. See `FREEZE_POLICY.md` in the release candidate.
""".encode("utf-8")


def proposed_tag_bytes() -> bytes:
    return f"""schema_id: "v21_terminal_baseline_proposed_tag_v1"
task_id: "RT-20260808-002"
plan_task_id: "P0-T02"
created_at: "{CREATED_AT}"
status: "PROPOSED_NOT_CREATED"
tag_name: "{PROPOSED_TAG}"
target_commit: "{BASELINE_COMMIT}"
target_tree: "{BASELINE_TREE}"
annotated_tag_message: "V21 terminal scientific baseline; internal negative-status release candidate"
tag_exists_at_build: false
tag_creation_authorized: false
public_release_authorized: false
publication_authorized: false
push_authorized: false
external_action_authorized: false
required_before_execution:
  - "separate explicit human check and authorization"
  - "revalidate manifest archive and exact target commit"
  - "confirm release notes preserve the negative scientific status"
authority_note: "Metadata preparation only; this record is not a tag or release."
""".encode("utf-8")


def tar_info(name: str, data: bytes) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mode = 0o644
    return info


def build_archive(members: dict[str, bytes]) -> tuple[bytes, dict[str, Any]]:
    index_entries = [
        {
            "path": path,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
        }
        for path, data in sorted(members.items())
    ]
    index = {
        "schema_id": "v21_terminal_baseline_archive_index_v1",
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "indexed_member_count": len(index_entries),
        "entries": index_entries,
        "authority_limits": {
            "archive_is_independent_scientific_authority": False,
            "tag_created": False,
            "public_release_created": False,
            "physics_promotion_authorized": False,
        },
    }
    index_data = json_bytes(index)
    all_members = dict(members)
    all_members["ARCHIVE_INDEX.json"] = index_data
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:", format=tarfile.GNU_FORMAT) as archive:
        for name, data in sorted(all_members.items()):
            archive.addfile(tar_info(name, data), io.BytesIO(data))
    return buffer.getvalue(), index


def build_outputs() -> dict[str, bytes]:
    manifest, partition, archive_members = build_inventory()
    reproduction = build_reproduction_receipt()
    freeze_policy = freeze_policy_bytes()
    release_notes = release_notes_bytes()
    proposed_tag = proposed_tag_bytes()

    component_bytes = {
        "manifest": json_bytes(manifest),
        "partition": json_bytes(partition),
        "reproduction": json_bytes(reproduction),
        "freeze_policy": freeze_policy,
        "release_notes": release_notes,
        "proposed_tag": proposed_tag,
    }
    release_member_names = {
        "manifest": "release-control/RELEASE_MANIFEST.json",
        "partition": "release-control/CANONICAL_DERIVATIVE_PARTITION.json",
        "reproduction": "release-control/REPRODUCTION_RECEIPT.json",
        "freeze_policy": "release-control/FREEZE_POLICY.md",
        "release_notes": "release-control/RELEASE_NOTES.md",
        "proposed_tag": "release-control/PROPOSED_TAG.yaml",
    }
    for key, archive_name in release_member_names.items():
        add_archive_member(archive_members, archive_name, component_bytes[key])
    archive, archive_index = build_archive(archive_members)
    component_bytes["archive"] = archive

    catalog = {
        "schema_id": "v21_terminal_baseline_release_catalog_v1",
        "task_id": "RT-20260808-002",
        "job_id": "AJ-RT-20260808-002-001",
        "plan_task_id": "P0-T02",
        "created_at": CREATED_AT,
        "status": "PASS_INTERNAL_RELEASE_CANDIDATE_BUILT",
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "proposed_tag": PROPOSED_TAG,
        "archive": {
            "path": str(OUTPUT_PATHS["archive"].relative_to(ROOT)),
            "sha256": sha256_bytes(archive),
            "bytes": len(archive),
            "member_count": archive_index["indexed_member_count"] + 1,
            "indexed_member_count": archive_index["indexed_member_count"],
            "archive_index_sha256": sha256_bytes(json_bytes(archive_index)),
            "deterministic_metadata": {
                "mtime": 0,
                "uid": 0,
                "gid": 0,
                "mode": "0644",
                "path_order": "bytewise_sorted_python_string_order",
            },
        },
        "components": {
            key: {
                "path": str(OUTPUT_PATHS[key].relative_to(ROOT)),
                "sha256": sha256_bytes(data),
                "bytes": len(data),
            }
            for key, data in sorted(component_bytes.items())
            if key != "archive"
        },
        "reproduction_status": reproduction["status"],
        "reproduction_profile_count": reproduction["profile_count"],
        "reproduction_pass_count": reproduction["passed_profile_count"],
        "reproduction_failed_profile_ids": reproduction["failed_profile_ids"],
        "tag_exists_at_build": False,
        "tag_created": False,
        "public_release_created": False,
        "authority_limits": manifest["authority_limits"],
    }
    component_bytes["catalog"] = json_bytes(catalog)
    return component_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    outputs = build_outputs()
    stale: list[str] = []
    if args.write:
        for key, data in outputs.items():
            OUTPUT_PATHS[key].write_bytes(data)
    else:
        for key, data in outputs.items():
            path = OUTPUT_PATHS[key]
            if not path.is_file() or path.read_bytes() != data:
                stale.append(str(path.relative_to(ROOT)))

    catalog = json.loads(outputs["catalog"])
    summary = {
        "schema_id": "v22_p0_t02_baseline_release_build_summary_v1",
        "status": "PASS" if not stale else "FAIL",
        "mode": "write" if args.write else "check",
        "baseline_commit": BASELINE_COMMIT,
        "baseline_tree": BASELINE_TREE,
        "archive_sha256": catalog["archive"]["sha256"],
        "archive_bytes": catalog["archive"]["bytes"],
        "archive_member_count": catalog["archive"]["member_count"],
        "reproduction_status": catalog["reproduction_status"],
        "reproduction_pass_count": catalog["reproduction_pass_count"],
        "stale_outputs": stale,
        "tag_created": False,
        "public_release_created": False,
        "authority": "operational_release_control_only",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
