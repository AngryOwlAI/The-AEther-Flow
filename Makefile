PYTHON ?= .venv/bin/python
MEMORY_SCRIPT_DIR := .codex/skills/project-memory-system/scripts
MEMORY_TEST_MODULES := tests.test_memory_operations tests.test_memory_cli_modes tests.test_memory_system tests.test_obsidian_wiki tests.test_validation_orchestration
VALIDATION_PYTHON_SERIES := 3.12
VALIDATION_REQUIREMENT_FILES := requirements.txt requirements-dev.txt
VALIDATION_REQUIRED_DISTRIBUTIONS := PyMuPDF

define VALIDATION_ENVIRONMENT_CHECK
import hashlib
import importlib.metadata as metadata
import json
import os
import pathlib
import platform
import sys

expected_series = tuple(int(part) for part in os.environ["VALIDATION_PYTHON_SERIES"].split("."))
actual_series = sys.version_info[:2]
if actual_series != expected_series:
    print(
        f"Unsupported validation Python {actual_series[0]}.{actual_series[1]}. "
        f"Expected {expected_series[0]}.{expected_series[1]}. "
        "Create a matching virtual environment and run make setup-dev with its Python.",
        file=sys.stderr,
    )
    raise SystemExit(2)

required_distributions = os.environ["VALIDATION_REQUIRED_DISTRIBUTIONS"].split()
installed_distributions = {}
missing_distributions = []
for distribution in required_distributions:
    try:
        installed_distributions[distribution] = metadata.version(distribution)
    except metadata.PackageNotFoundError:
        missing_distributions.append(distribution)
if missing_distributions:
    print(
        "Missing validation dependencies: "
        + ", ".join(missing_distributions)
        + f". Run make setup-dev PYTHON={sys.executable}.",
        file=sys.stderr,
    )
    raise SystemExit(2)

requirement_files = os.environ["VALIDATION_REQUIREMENT_FILES"].split()
dependency_hasher = hashlib.sha256()
for relative_path in requirement_files:
    path = pathlib.Path(relative_path)
    if not path.is_file():
        print(f"Missing dependency specification {relative_path}.", file=sys.stderr)
        raise SystemExit(2)
    dependency_hasher.update(relative_path.encode("utf-8"))
    dependency_hasher.update(b"\0")
    dependency_hasher.update(path.read_bytes())
    dependency_hasher.update(b"\0")
dependency_lock_digest = dependency_hasher.hexdigest()

fingerprint_input = {
    "dependency_lock_digest": dependency_lock_digest,
    "installed_distributions": installed_distributions,
    "python_implementation": platform.python_implementation(),
    "python_version": platform.python_version(),
    "schema_id": "validation_environment_v1",
}
canonical_input = json.dumps(fingerprint_input, sort_keys=True, separators=(",", ":"))
receipt = {
    **fingerprint_input,
    "dependency_specification_files": requirement_files,
    "environment_fingerprint": hashlib.sha256(canonical_input.encode("utf-8")).hexdigest(),
    "gate_id": "validation_environment",
    "provisioning": False,
    "status": "PASS",
}
print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
endef
export VALIDATION_ENVIRONMENT_CHECK

.PHONY: setup-dev validation-environment memory-sync memory-validate-core memory-doctor test-memory validate-memory validate-memory-full validate-project-control validate-html-explainers audit-documentation-surfaces

setup-dev:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) -m pip install -r requirements-dev.txt
	@printf '%s\n' '{"target":"setup-dev","status":"PASS","provisioning":true}'

validation-environment:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing validation Python $(PYTHON). Create a CPython $(VALIDATION_PYTHON_SERIES) virtual environment and run make setup-dev with its Python." >&2; exit 2; }
	@VALIDATION_PYTHON_SERIES="$(VALIDATION_PYTHON_SERIES)" VALIDATION_REQUIREMENT_FILES="$(VALIDATION_REQUIREMENT_FILES)" VALIDATION_REQUIRED_DISTRIBUTIONS="$(VALIDATION_REQUIRED_DISTRIBUTIONS)" $(PYTHON) -c "$$VALIDATION_ENVIRONMENT_CHECK"

memory-sync: validation-environment
	PYTHONPATH="$(MEMORY_SCRIPT_DIR)" $(PYTHON) -c 'import json; from bootstrap_memory_system import memory_sync; receipt = memory_sync().to_dict(); print(json.dumps({"gate_id": "memory_sync", "status": "PASS", "mutated": receipt["mutated"], "local_retrieval_enabled": receipt["local_retrieval_enabled"], "counts": receipt["counts"], "changed": receipt["changed"], "created": receipt["created"], "pruned": receipt["pruned"]}, sort_keys=True))'

memory-validate-core: validation-environment
	PYTHONPATH="$(MEMORY_SCRIPT_DIR)" $(PYTHON) -c 'import json; from bootstrap_memory_system import memory_validate_core; report = memory_validate_core(); print(json.dumps(report.to_dict(), sort_keys=True)); raise SystemExit(0 if report.ok else 1)'

memory-doctor: validation-environment
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/sync_obsidian_vault.py
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/lint_obsidian_vault.py --require-index
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/query_memory.py status --json
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/query_memory.py search "Lorentzian metric" --formats tex,pdf --limit 5 --json
	@printf '%s\n' '{"target":"memory-doctor","status":"PASS","authority":"local_only"}'

test-memory: validation-environment
	$(PYTHON) -m unittest $(MEMORY_TEST_MODULES)
	@printf '%s\n' '{"target":"test-memory","status":"PASS","module_count":5}'

validate-memory: memory-validate-core test-memory
	@printf '%s\n' '{"target":"validate-memory","status":"PASS","profile":"affected-memory-compatibility"}'

validate-memory-full: memory-sync memory-doctor
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/bootstrap_memory_system.py --validate-only
	$(PYTHON) -m unittest discover -s tests
	@printf '%s\n' '{"target":"validate-memory-full","status":"PASS","profile":"full-memory-compatibility"}'

validate-project-control: validation-environment
	$(PYTHON) scripts/project_control/classify_project_changes.py --json
	$(PYTHON) scripts/project_control/collect_project_improvement_signals.py --validate-emitted
	$(PYTHON) scripts/project_control/validate_documentation_impact.py
	$(PYTHON) scripts/project_control/audit_documentation_surfaces.py --skip-local
	$(PYTHON) .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
	$(PYTHON) scripts/spec_depth_lint.py --root .
	$(PYTHON) scripts/validate_publication_process.py --root .
	$(PYTHON) scripts/research_control/validate_research_control.py --check-diff
	$(PYTHON) -m unittest discover -s tests

validate-html-explainers: validation-environment
	$(PYTHON) .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
	$(PYTHON) scripts/spec_depth_lint.py --root .
	$(PYTHON) scripts/validate_publication_process.py --root .

audit-documentation-surfaces: validation-environment
	$(PYTHON) scripts/project_control/audit_documentation_surfaces.py
