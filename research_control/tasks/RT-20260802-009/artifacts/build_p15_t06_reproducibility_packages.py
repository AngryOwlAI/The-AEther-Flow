#!/usr/bin/env python3
"""Build deterministic, source-backed P15-T06 publication-candidate bundles.

The bundles are internal release candidates.  They preserve the exact source
snapshot needed by each existing validator while leaving canonical sources,
historical task evidence, and publication authority unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
CREATED_AT = "2026-08-02T14:32:33Z"
ASSEMBLY_REF = "9be11e9cc77a8ab30776fd5598b682b37c42a6e3"

OUTPUT_PATHS = {
    "catalog": ARTIFACT_DIR / "p15_t06_package_catalog_v1.json",
    "source_map": ARTIFACT_DIR / "p15_t06_source_map_v1.json",
    "environment": ARTIFACT_DIR / "p15_t06_environment_recipes_v1.md",
    "license_audit": ARTIFACT_DIR / "p15_t06_license_notice_audit_v1.json",
}

ENVIRONMENT_PATHS = (
    "LICENSE",
    "NOTICES",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "research_control/tasks/RT-20260723-019/artifacts/requirements.lock",
    "research_control/tasks/RT-20260724-002/artifacts/quality-assurance-requirements.lock",
)


@dataclass(frozen=True)
class Candidate:
    plan_task_id: str
    package_id: str
    title: str
    task_path: str
    artifact_ref: str
    source_ref: str
    source_paths: tuple[str, ...]
    reproduction_commands: tuple[tuple[str, ...], ...]
    limitations: tuple[str, ...]

    @property
    def archive_name(self) -> str:
        return f"{self.package_id.lower().replace('-', '_')}_source_bundle_v1.tar"


P15_T01_SOURCES = (
    "ontology/tex/aether_flow_foundations.tex",
    "ontology/tex/aether_flow_dynamics.tex",
    "ontology/tex/aether_flow_consistency.tex",
    "ontology/tex/aether_flow_relativistic_recovery.tex",
    "ontology/tex/aether_flow_geometry.tex",
    "ontology/tex/aether_flow_exact_closure_note.tex",
    "ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
    "ontology/tex/aether_flow_exact_closure_flagship_article.tex",
    "research_control/tasks/RT-20260722-016/artifacts/four_project_success_categories_v1.tex",
    "research_control/tasks/RT-20260722-016/jobs/completions/AJC-AJ-RT-20260722-016-001.yaml",
    "research_control/tasks/RT-20260722-018/artifacts/non_empirical_ontology_success_criteria_v1.tex",
    "research_control/tasks/RT-20260722-018/jobs/completions/AJC-AJ-RT-20260722-018-001.yaml",
    "research_control/tasks/RT-20260722-019/artifacts/no_target_positive_provenance_sufficiency_policy_v1.tex",
    "research_control/tasks/RT-20260722-019/jobs/completions/AJC-AJ-RT-20260722-019-001.yaml",
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/handoffs/handoff-0829.yaml",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "research_control/design/gr_derivation_burden_map.md",
    "markdown/publication-briefs/exact-gr-benchmark-boundary.publication-brief.md",
    "markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md",
)

P15_T02_SOURCES = (
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/design/manuscript_split_boundary_checklist_v16.md",
    "research_control/tasks/RT-20260704-014/artifacts/ai_methodology_manuscript_outline_v15.md",
    "research_control/tasks/RT-20260705-025/artifacts/ai_methodology_manuscript_status_refresh_v16.md",
    "research_control/tasks/RT-20260721-005/artifacts/v21_candidate_lineage_registry.json",
    "research_control/tasks/RT-20260721-006/artifacts/v21_research_attempt_ledger.json",
    "research_control/tasks/RT-20260723-011/artifacts/attempt_rework_dashboard.json",
    "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_ablation_results.json",
    "research_control/tasks/RT-20260723-013/artifacts/p12_t07_methodology_compact_receipt.json",
    "research_control/tasks/RT-20260723-013/jobs/completions/AJC-AJ-RT-20260723-013-001.yaml",
    "research_control/tasks/RT-20260802-007/artifacts/software_system_non_regression_report_v1.json",
    "research_control/tasks/RT-20260802-007/artifacts/performance_rollback_evidence_v1.json",
    "research_control/tasks/RT-20260802-007/artifacts/p13_t08_compact_receipt.json",
    "research_control/tasks/RT-20260802-007/jobs/completions/AJC-AJ-RT-20260802-007-001.yaml",
)

P15_T03_SOURCES = (
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md",
    "research_control/handoffs/handoff-0835.yaml",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_v1.tex",
    "research_control/tasks/RT-20260720-023/artifacts/eqsrc_source_extension_lattice_v1.tex",
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex",
    "research_control/tasks/RT-20260720-027/artifacts/eqsrc_invariant_functor_quotient_smuggling_audit_v1.tex",
    "research_control/tasks/RT-20260722-020/artifacts/negative_result_success_pathway_v1.tex",
    "ontology/tex/aether_flow_foundations.tex",
    "ontology/tex/aether_flow_geometry.tex",
)

P15_T04_SOURCES = (
    "research_control/tasks/RT-20260725-003/artifacts/compact_source_theory_object_v1.tex",
    "research_control/tasks/RT-20260725-007/artifacts/phi_src_semiflow_semantics_v1.tex",
    "research_control/tasks/RT-20260725-008/artifacts/cubic_amplitude_source_dynamics_v1.tex",
    "research_control/tasks/RT-20260725-010/artifacts/cubic_amplitude_structural_analysis_v1.tex",
    "research_control/tasks/RT-20260725-012/artifacts/cubic_amplitude_background_phase_analysis_v1.tex",
    "research_control/tasks/RT-20260725-013/artifacts/source_amplitude_resolution_coarse_graining_v1.tex",
    "research_control/tasks/RT-20260725-014/artifacts/source_dynamics_package_audit_v1.tex",
    "research_control/tasks/RT-20260726-001/artifacts/source_dynamics_milestone_synthesis_v1.tex",
    "research_control/tasks/RT-20260726-002/artifacts/causal_characteristic_target_v1.tex",
    "research_control/tasks/RT-20260726-003/artifacts/source_local_transport_candidate_v1.tex",
    "research_control/tasks/RT-20260726-005/artifacts/one_ray_conformal_insufficiency_v1.tex",
    "research_control/tasks/RT-20260726-007/artifacts/source_scale_calibration_nonselection_v1.tex",
    "research_control/tasks/RT-20260726-009/artifacts/signature_covariance_naturality_obstruction_v1.tex",
    "research_control/tasks/RT-20260726-010/artifacts/uniqueness_covariance_robustness_admissibility_obstruction_v1.tex",
    "research_control/tasks/RT-20260726-011/artifacts/metric_object_naming_decision_v1.yaml",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml",
)

CANDIDATES = (
    Candidate(
        plan_task_id="P15-T01",
        package_id="P15-T01-EXACT-GR-INTERPRETIVE",
        title="Exact-GR interpretive manuscript package",
        task_path="research_control/tasks/RT-20260722-021",
        artifact_ref="1d7e5d81cc75ddf903983dffec8b8a371476c738",
        source_ref="ef41c569efd01f3a5182f114c20dd6edb3ee9973",
        source_paths=P15_T01_SOURCES,
        reproduction_commands=((
            "research_control/tasks/RT-20260722-021/artifacts/validate_exact_gr_interpretive_package.py",
            "--check",
            "--json",
        ),),
        limitations=(
            "The source snapshot predates later canonical edits to foundations, dynamics, and geometry.",
            "The manuscript is a noncanonical internal publication candidate, not an adopted derivation or release authorization.",
        ),
    ),
    Candidate(
        plan_task_id="P15-T02",
        package_id="P15-T02-AI-METHODOLOGY",
        title="AI research-operating-system methodology package",
        task_path="research_control/tasks/RT-20260802-008",
        artifact_ref=ASSEMBLY_REF,
        source_ref=ASSEMBLY_REF,
        source_paths=P15_T02_SOURCES,
        reproduction_commands=(
            (
                "research_control/tasks/RT-20260802-008/artifacts/build_p15_t02_methodology_publication.py",
                "--check",
            ),
            (
                "research_control/tasks/RT-20260802-008/artifacts/validate_p15_t02_methodology_publication.py",
            ),
        ),
        limitations=(
            "The comparison is retrospective and nonrandomized; causal superiority is not identified.",
            "Same-model context variation is not independent or external-human review.",
        ),
    ),
    Candidate(
        plan_task_id="P15-T03",
        package_id="P15-T03-SELECTOR-THEOREM",
        title="Selector minimum-extension theorem package",
        task_path="research_control/tasks/RT-20260723-003",
        artifact_ref="1136e88b329fa9215017a20dd030607a98168503",
        source_ref="1136e88b329fa9215017a20dd030607a98168503",
        source_paths=P15_T03_SOURCES,
        reproduction_commands=((
            "research_control/tasks/RT-20260723-003/artifacts/validate_selector_minimum_extension_manuscript.py",
            "--check",
            "--json",
        ),),
        limitations=(
            "The bundle preserves its qualifying source snapshot; later canonical ontology edits are intentionally excluded.",
            "The theorem packet does not adopt a selector, physical gauge, source law, or global no-go conclusion.",
        ),
    ),
    Candidate(
        plan_task_id="P15-T04",
        package_id="P15-T04-SOURCE-DYNAMICS",
        title="Source-dynamics reconstruction report package",
        task_path="research_control/tasks/RT-20260727-006",
        artifact_ref="832f9cf9ba98061df40cdda2799d5a46661260bc",
        source_ref="832f9cf9ba98061df40cdda2799d5a46661260bc",
        source_paths=P15_T04_SOURCES,
        reproduction_commands=((
            "research_control/tasks/RT-20260727-006/artifacts/validate_source_dynamics_reconstruction_report.py",
            "--check",
            "--json",
        ),),
        limitations=(
            "The reconstruction controls are bounded mathematical comparisons and do not adopt a source law or physical metric.",
            "Gate B remains unmet and validator PASS has operational authority only.",
        ),
    ),
)


def run_git(*args: str) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def resolve_ref(ref: str) -> str:
    return run_git("rev-parse", f"{ref}^{{commit}}").decode("ascii").strip()


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


def json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def add_source(
    members: dict[str, tuple[bytes, str, str]],
    path: str,
    ref: str,
    source_class: str,
) -> None:
    data = git_bytes(ref, path)
    if path in members:
        previous_data, previous_ref, previous_class = members[path]
        if previous_data != data:
            raise ValueError(
                f"conflicting bytes for {path}: {previous_ref}/{previous_class} versus {ref}/{source_class}"
            )
        return
    members[path] = (data, resolve_ref(ref), source_class)


def reproduce_text(candidate: Candidate) -> bytes:
    commands = ["python " + " ".join(parts) for parts in candidate.reproduction_commands]
    command_lines = "\n".join(f"    {command}" for command in commands)
    limitation_lines = "\n".join(f"- {item}" for item in candidate.limitations)
    return f"""# {candidate.title}: reproducibility instructions

Status: internal release candidate; external publication, submission, outreach,
push, and distribution remain human-gated and are not authorized by this bundle.

## Environment

- Python: `>=3.12,<3.13`
- Runtime dependency lock: `research_control/tasks/RT-20260723-019/artifacts/requirements.lock`
- Full quality lock: `research_control/tasks/RT-20260724-002/artifacts/quality-assurance-requirements.lock`
- Install from the extracted bundle root with `python -m pip install --require-hashes -r requirements-dev.txt`.

## Reproduce

Run from the extracted bundle root:

```sh
{command_lines}
```

The expected result is process exit code zero. Validator PASS is operational
evidence only; it is not theorem proof, ontology adoption, benchmark promotion,
publication authority, or completed derivation.

## Limitations

{limitation_lines}

## License and notice

`LICENSE` assigns research and documentation content to CC BY 4.0 and code or
tooling to Apache-2.0, subject to narrower notices. `NOTICES` records attribution
and third-party boundaries. The repository currently tracks the split-license
summary rather than standalone copies of the two standard license texts; stable
license identifiers and official text URLs are recorded in the package catalog.
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


def deterministic_tar(manifest: bytes, reproduce: bytes, members: dict[str, tuple[bytes, str, str]]) -> bytes:
    fileobj = io.BytesIO()
    with tarfile.open(fileobj=fileobj, mode="w", format=tarfile.PAX_FORMAT) as archive:
        archive.addfile(tar_info("PACKAGE_MANIFEST.json", manifest), io.BytesIO(manifest))
        archive.addfile(tar_info("REPRODUCE.md", reproduce), io.BytesIO(reproduce))
        for path in sorted(members):
            data = members[path][0]
            archive.addfile(tar_info(path, data), io.BytesIO(data))
    return fileobj.getvalue()


def build_candidate(candidate: Candidate) -> tuple[bytes, dict[str, object]]:
    members: dict[str, tuple[bytes, str, str]] = {}
    for path in git_paths(candidate.artifact_ref, candidate.task_path):
        add_source(members, path, candidate.artifact_ref, "candidate_task_record_or_artifact")
    for path in candidate.source_paths:
        add_source(members, path, candidate.source_ref, "candidate_source_snapshot")
    for path in ENVIRONMENT_PATHS:
        add_source(members, path, ASSEMBLY_REF, "package_environment_or_license")

    entries = [
        {
            "path": path,
            "sha256": sha256_bytes(data),
            "byte_count": len(data),
            "git_commit": ref,
            "source_class": source_class,
        }
        for path, (data, ref, source_class) in sorted(members.items())
    ]
    reproduce = reproduce_text(candidate)
    manifest = {
        "schema_id": "v21_p15_t06_reproducibility_bundle_manifest_v1",
        "status": "INTERNAL_RELEASE_CANDIDATE_NOT_EXTERNALLY_RELEASED",
        "created_at": CREATED_AT,
        "plan_task_id": candidate.plan_task_id,
        "package_id": candidate.package_id,
        "title": candidate.title,
        "artifact_commit": resolve_ref(candidate.artifact_ref),
        "source_snapshot_commit": resolve_ref(candidate.source_ref),
        "assembly_commit": resolve_ref(ASSEMBLY_REF),
        "entry_count": len(entries),
        "entries": entries,
        "generated_members": [
            {"path": "REPRODUCE.md", "sha256": sha256_bytes(reproduce), "byte_count": len(reproduce)}
        ],
        "reproduction_commands": [list(parts) for parts in candidate.reproduction_commands],
        "expected_result": "PASS_OPERATIONAL_VALIDATION_ONLY",
        "limitations": list(candidate.limitations),
        "license_mapping": {
            "research_and_documentation": "CC-BY-4.0",
            "code_and_tooling": "Apache-2.0",
            "third_party_material": "retains_original_license_and_notice",
            "scientific_status_effect": "none",
        },
        "authority_limits": {
            "canonical_source_modified": False,
            "historical_evidence_rewritten": False,
            "publication_or_distribution_authorized": False,
            "physics_promotion_authorized": False,
            "proof_authority_created": False,
            "completed_derivation_claim_authorized": False,
        },
        "manifest_scope_note": "PACKAGE_MANIFEST.json is excluded from its own entry hash list; the outer catalog hashes the complete tar bytes.",
    }
    manifest_bytes = json_bytes(manifest)
    archive_bytes = deterministic_tar(manifest_bytes, reproduce, members)
    summary = {
        "plan_task_id": candidate.plan_task_id,
        "package_id": candidate.package_id,
        "title": candidate.title,
        "archive_path": f"research_control/tasks/RT-20260802-009/artifacts/{candidate.archive_name}",
        "archive_sha256": sha256_bytes(archive_bytes),
        "archive_byte_count": len(archive_bytes),
        "entry_count": len(entries) + 2,
        "tracked_entry_count": len(entries),
        "artifact_commit": manifest["artifact_commit"],
        "source_snapshot_commit": manifest["source_snapshot_commit"],
        "reproduction_commands": manifest["reproduction_commands"],
        "expected_result": manifest["expected_result"],
        "limitations": list(candidate.limitations),
        "entries": entries,
    }
    return archive_bytes, summary


def environment_recipe(package_summaries: Iterable[dict[str, object]]) -> str:
    rows = "\n".join(
        f"| {item['plan_task_id']} | `{item['archive_path']}` | `{item['source_snapshot_commit']}` |"
        for item in package_summaries
    )
    return f"""---
authority: control
artifact_id: P15-T06-ENVIRONMENT-RECIPES-V1
status: internal_release_candidate
plan_task_id: P15-T06
created_at: {CREATED_AT}
publication_authorized: false
physics_promotion_authorized: false
---

# P15-T06 environment and clean-room recipes

These recipes reproduce four internal publication candidates from exact source
snapshots. They do not edit canonical sources or authorize external release.

## Bound archives

| Candidate | Archive | Source snapshot |
| --- | --- | --- |
{rows}

## Runtime

Use CPython 3.12. The project metadata requires `>=3.12,<3.13`. Exact runtime
and quality dependencies are recorded in the two bundled hash locks:

- `research_control/tasks/RT-20260723-019/artifacts/requirements.lock`
- `research_control/tasks/RT-20260724-002/artifacts/quality-assurance-requirements.lock`

From a clean directory, extract one archive and run:

```sh
tar -xf <archive>.tar
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-dev.txt
```

Then run the exact command in the archive's `REPRODUCE.md`. P15-T02 uses only
the Python standard library; the other candidate validators require PyYAML.
TeX compilation is outside this task: the packages validate tracked source and
evidence bytes, not generated PDF derivatives.

## Determinism and authority

Archive members are sorted and use fixed metadata (`mtime=0`, uid/gid zero,
mode `0644`). `PACKAGE_MANIFEST.json` binds every tracked member to a SHA-256
and exact Git commit. Later canonical-source evolution is not substituted into
older packages. Validator PASS remains operational evidence only.
"""


def build_outputs() -> dict[Path, bytes]:
    archive_outputs: dict[Path, bytes] = {}
    package_summaries: list[dict[str, object]] = []
    for candidate in CANDIDATES:
        archive_bytes, summary = build_candidate(candidate)
        archive_path = ARTIFACT_DIR / candidate.archive_name
        archive_outputs[archive_path] = archive_bytes
        package_summaries.append(summary)

    catalog_items = [{key: value for key, value in item.items() if key != "entries"} for item in package_summaries]
    catalog = {
        "schema_id": "v21_p15_t06_reproducibility_package_catalog_v1",
        "status": "PACKAGE_BUILD_COMPLETE_VALIDATION_REQUIRED",
        "created_at": CREATED_AT,
        "task_id": "RT-20260802-009",
        "plan_task_id": "P15-T06",
        "assembly_commit": resolve_ref(ASSEMBLY_REF),
        "package_count": len(catalog_items),
        "packages": catalog_items,
        "license_identifiers": ["CC-BY-4.0", "Apache-2.0"],
        "official_license_text_urls": {
            "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "Apache-2.0": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        },
        "external_release_authorized": False,
        "publication_authorized": False,
        "physics_promotion_authorized": False,
    }
    source_map = {
        "schema_id": "v21_p15_t06_source_map_v1",
        "status": "EXACT_GIT_AND_SHA256_BINDINGS",
        "created_at": CREATED_AT,
        "task_id": "RT-20260802-009",
        "plan_task_id": "P15-T06",
        "packages": [
            {
                "plan_task_id": item["plan_task_id"],
                "package_id": item["package_id"],
                "artifact_commit": item["artifact_commit"],
                "source_snapshot_commit": item["source_snapshot_commit"],
                "entries": item["entries"],
            }
            for item in package_summaries
        ],
        "canonical_authority_note": "Paths retain the authority they had at the named snapshot; package copies and generated derivatives are not independent authority.",
    }
    license_bytes = git_bytes(ASSEMBLY_REF, "LICENSE")
    notices_bytes = git_bytes(ASSEMBLY_REF, "NOTICES")
    license_audit = {
        "schema_id": "v21_p15_t06_license_notice_audit_v1",
        "status": "PASS_SPLIT_LICENSE_AND_NOTICE_BOUND",
        "created_at": CREATED_AT,
        "task_id": "RT-20260802-009",
        "plan_task_id": "P15-T06",
        "package_count": len(package_summaries),
        "license_sha256": sha256_bytes(license_bytes),
        "notices_sha256": sha256_bytes(notices_bytes),
        "research_and_documentation_license": "CC-BY-4.0",
        "code_and_tooling_license": "Apache-2.0",
        "repository_owner_attribution_present": True,
        "third_party_boundary_present": True,
        "scientific_claim_boundary_present": True,
        "standalone_standard_license_texts_tracked_in_source_repository": False,
        "standalone_text_limitation": "The tracked LICENSE names but does not include the referenced LICENSES directory. Each bundle carries LICENSE and NOTICES plus stable license identifiers and official text URLs; external release remains human-gated.",
        "third_party_payloads_included": False,
        "external_primary_literature_copied": False,
        "redistribution_basis": "Explicit repository-owner split-license grant in bundled LICENSE, with attribution and third-party limits in bundled NOTICES.",
        "external_release_authorized": False,
        "scientific_status_changed": False,
    }

    outputs = {
        **archive_outputs,
        OUTPUT_PATHS["catalog"]: json_bytes(catalog),
        OUTPUT_PATHS["source_map"]: json_bytes(source_map),
        OUTPUT_PATHS["environment"]: environment_recipe(package_summaries).encode("utf-8"),
        OUTPUT_PATHS["license_audit"]: json_bytes(license_audit),
    }
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    stale: list[str] = []
    for path, expected in outputs.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    result = {
        "schema_id": "v21_p15_t06_package_build_result_v1",
        "status": "PASS" if not stale else "FAIL",
        "output_count": len(outputs),
        "package_count": len(CANDIDATES),
        "stale_outputs": stale,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not stale else 1


if __name__ == "__main__":
    raise SystemExit(main())
