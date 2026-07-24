PYTHON ?= .venv/bin/python
MEMORY_SCRIPT_DIR := .codex/skills/project-memory-system/scripts
MEMORY_TEST_MODULES := tests.test_memory_operations tests.test_memory_cli_modes tests.test_memory_system_unit tests.test_obsidian_wiki_unit tests.test_validation_orchestration tests.test_validation_doctor
VALIDATION_PYTHON_SERIES := 3.12
VALIDATION_REQUIREMENT_FILES := pyproject.toml research_control/tasks/RT-20260723-019/artifacts/requirements.lock research_control/tasks/RT-20260724-002/artifacts/quality-assurance-requirements.lock requirements.txt requirements-dev.txt
VALIDATION_REQUIRED_DISTRIBUTIONS := PyMuPDF==1.27.2.3 PyYAML==6.0.3
QUALITY_REQUIRED_DISTRIBUTIONS := mypy==2.3.0 ruff==0.16.0
QUALITY_PYTHON_PATHS := scripts/validation/api.py scripts/validation/portability.py scripts/validation/models.py
QUALITY_TEST_PATHS := tests/test_validation_api.py tests/test_validation_portability.py
QUALITY_PORTABILITY_PATHS := $(QUALITY_PYTHON_PATHS) $(QUALITY_TEST_PATHS)
ASSURANCE_REQUIRED_DISTRIBUTIONS := bandit==1.9.4 coverage==7.15.2 hypothesis==6.161.2 mutmut==3.6.0 pip-audit==2.10.1
ASSURANCE_PYTHON_PATHS := scripts/validation/assurance.py scripts/validation/portability.py
ASSURANCE_TEST_PATHS := tests/test_validation_assurance.py tests/test_p13_t05_assurance_properties.py
ASSURANCE_TEST_MODULES := tests.test_validation_assurance tests.test_p13_t05_assurance_properties tests.test_validation_portability
ASSURANCE_BANDIT_PATHS := scripts/validation/assurance.py scripts/validation/portability.py scripts/research_control/checkpoint_research_transaction.py .codex/skills/continue-research-goal/scripts/goal_state.py
ASSURANCE_COVERAGE_FLOOR := 85
VALIDATION_PATHS ?=
VALIDATION_DOCTOR_SCOPE ?= local_retrieval
VALIDATION_DOCTOR_FLAGS ?=

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
version_mismatches = []
for requirement in required_distributions:
    distribution, separator, expected_version = requirement.partition("==")
    try:
        actual_version = metadata.version(distribution)
        installed_distributions[distribution] = actual_version
        if separator and actual_version != expected_version:
            version_mismatches.append(
                f"{distribution}=={actual_version} (expected {expected_version})"
            )
    except metadata.PackageNotFoundError:
        missing_distributions.append(requirement)
if missing_distributions:
    print(
        "Missing validation dependencies: "
        + ", ".join(missing_distributions)
        + f". Run make setup-dev PYTHON={sys.executable}.",
        file=sys.stderr,
    )
    raise SystemExit(2)
if version_mismatches:
    print(
        "Validation dependency version mismatch: "
        + ", ".join(version_mismatches)
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

define QUALITY_ENVIRONMENT_CHECK
import importlib.metadata as metadata
import json
import os
import sys

installed = {}
problems = []
for requirement in os.environ["QUALITY_REQUIRED_DISTRIBUTIONS"].split():
    distribution, _, expected_version = requirement.partition("==")
    try:
        actual_version = metadata.version(distribution)
    except metadata.PackageNotFoundError:
        problems.append(f"missing {requirement}")
        continue
    installed[distribution] = actual_version
    if actual_version != expected_version:
        problems.append(f"{distribution}=={actual_version} (expected {expected_version})")
if problems:
    print(
        "Quality dependency check failed: "
        + ", ".join(problems)
        + f". Run make setup-dev PYTHON={sys.executable}.",
        file=sys.stderr,
    )
    raise SystemExit(2)
print(
    json.dumps(
        {
            "gate_id": "quality_environment",
            "installed_distributions": installed,
            "provisioning": False,
            "status": "PASS",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)
endef
export QUALITY_ENVIRONMENT_CHECK

define ASSURANCE_ENVIRONMENT_CHECK
import importlib.metadata as metadata
import json
import os
import sys

installed = {}
problems = []
for requirement in os.environ["ASSURANCE_REQUIRED_DISTRIBUTIONS"].split():
    distribution, _, expected_version = requirement.partition("==")
    try:
        actual_version = metadata.version(distribution)
    except metadata.PackageNotFoundError:
        problems.append(f"missing {requirement}")
        continue
    installed[distribution] = actual_version
    if actual_version != expected_version:
        problems.append(f"{distribution}=={actual_version} (expected {expected_version})")
if problems:
    print(
        "Assurance dependency check failed: "
        + ", ".join(problems)
        + f". Run make setup-dev PYTHON={sys.executable}.",
        file=sys.stderr,
    )
    raise SystemExit(2)
print(
    json.dumps(
        {
            "gate_id": "assurance_environment",
            "installed_distributions": installed,
            "provisioning": False,
            "status": "PASS",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)
endef
export ASSURANCE_ENVIRONMENT_CHECK

.PHONY: setup-dev validation-environment quality-environment quality-lint quality-type quality-portability quality-tests validate-quality assurance-environment assurance-lint assurance-type assurance-coverage assurance-adversarial assurance-code-security validate-assurance audit-assurance-dependencies audit-assurance-mutations memory-sync memory-validate-core memory-doctor test-memory validate-memory validate-memory-full validate-fast validate-affected validate-checkpoint-plan validate-full validate-doctor validate-project-control validate-project-control-legacy validate-html-explainers audit-documentation-surfaces
.NOTPARALLEL: validate-project-control validate-quality validate-assurance

setup-dev:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) -m pip install --require-hashes -r requirements-dev.txt
	@printf '%s\n' '{"target":"setup-dev","status":"PASS","provisioning":true}'

validation-environment:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing validation Python $(PYTHON). Create a CPython $(VALIDATION_PYTHON_SERIES) virtual environment and run make setup-dev with its Python." >&2; exit 2; }
	@VALIDATION_PYTHON_SERIES="$(VALIDATION_PYTHON_SERIES)" VALIDATION_REQUIREMENT_FILES="$(VALIDATION_REQUIREMENT_FILES)" VALIDATION_REQUIRED_DISTRIBUTIONS="$(VALIDATION_REQUIRED_DISTRIBUTIONS)" $(PYTHON) -c "$$VALIDATION_ENVIRONMENT_CHECK"

quality-environment: validation-environment
	@QUALITY_REQUIRED_DISTRIBUTIONS="$(QUALITY_REQUIRED_DISTRIBUTIONS)" $(PYTHON) -c "$$QUALITY_ENVIRONMENT_CHECK"

quality-lint: quality-environment
	$(PYTHON) -m ruff check $(QUALITY_PYTHON_PATHS) $(QUALITY_TEST_PATHS)

quality-type: quality-environment
	$(PYTHON) -m mypy $(QUALITY_PYTHON_PATHS)

quality-portability: quality-environment
	$(PYTHON) -m scripts.validation.portability $(foreach path,$(QUALITY_PORTABILITY_PATHS),--path $(path)) --json

quality-tests: quality-environment
	$(PYTHON) -m unittest -v tests.test_validation_api tests.test_validation_portability

validate-quality: quality-lint quality-type quality-portability quality-tests
	@printf '%s\n' '{"target":"validate-quality","status":"PASS","python_series":"$(VALIDATION_PYTHON_SERIES)","scope":"incremental"}'

assurance-environment: validation-environment
	@ASSURANCE_REQUIRED_DISTRIBUTIONS="$(ASSURANCE_REQUIRED_DISTRIBUTIONS)" $(PYTHON) -c "$$ASSURANCE_ENVIRONMENT_CHECK"

assurance-lint: assurance-environment
	$(PYTHON) -m ruff check $(ASSURANCE_PYTHON_PATHS) $(ASSURANCE_TEST_PATHS)

assurance-type: assurance-environment
	$(PYTHON) -m mypy scripts/validation/assurance.py

assurance-coverage: assurance-environment
	@mkdir -p .local/assurance
	$(PYTHON) -m coverage erase
	$(PYTHON) -m coverage run -m unittest -v $(ASSURANCE_TEST_MODULES)
	$(PYTHON) -m coverage json --fail-under=$(ASSURANCE_COVERAGE_FLOOR) -o .local/assurance/coverage.json
	$(PYTHON) -m scripts.validation.assurance coverage --input .local/assurance/coverage.json --minimum-percent $(ASSURANCE_COVERAGE_FLOOR)

assurance-adversarial: assurance-environment
	$(PYTHON) -m unittest -v tests.test_semantic_smuggling_adversarial_suite

assurance-code-security: assurance-environment
	@mkdir -p .local/assurance
	$(PYTHON) -m bandit -q -lll -f json -o .local/assurance/bandit-high.json $(ASSURANCE_BANDIT_PATHS)
	$(PYTHON) -m scripts.validation.assurance bandit --input .local/assurance/bandit-high.json

validate-assurance: assurance-lint assurance-type assurance-coverage assurance-adversarial assurance-code-security
	@printf '%s\n' '{"target":"validate-assurance","status":"PASS","coverage_floor":$(ASSURANCE_COVERAGE_FLOOR),"scope":"bounded"}'

audit-assurance-dependencies: assurance-environment
	@mkdir -p .local/assurance
	$(PYTHON) -m pip_audit --require-hashes -r requirements-dev.txt -f json -o .local/assurance/pip-audit.json
	$(PYTHON) -m scripts.validation.assurance pip-audit --input .local/assurance/pip-audit.json

audit-assurance-mutations: assurance-environment
	@mkdir -p .local/assurance
	$(PYTHON) -m mutmut run 'scripts.validation.assurance.x_evaluate_mutation*'
	$(PYTHON) -m mutmut results --all true > .local/assurance/mutmut-results-all.txt
	$(PYTHON) -m scripts.validation.assurance mutmut --input .local/assurance/mutmut-results-all.txt --target-prefix scripts.validation.assurance.x_evaluate_mutation__ --minimum-percent 100

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
	@printf '%s\n' '{"target":"test-memory","status":"PASS","module_count":6}'

validate-memory: memory-validate-core test-memory
	@printf '%s\n' '{"target":"validate-memory","status":"PASS","profile":"affected-memory-compatibility"}'

validate-memory-full: memory-sync memory-doctor
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/bootstrap_memory_system.py --validate-only
	$(PYTHON) -m unittest discover -s tests
	@printf '%s\n' '{"target":"validate-memory-full","status":"PASS","profile":"full-memory-compatibility"}'

validate-fast: validation-environment
	$(PYTHON) -m scripts.validation.cli plan --profile fast --paths $(VALIDATION_PATHS) --explain

validate-affected: validation-environment
	$(PYTHON) -m scripts.validation.cli plan --profile affected --paths $(VALIDATION_PATHS) --explain

validate-checkpoint-plan: validation-environment
	$(PYTHON) -m scripts.validation.cli plan --profile checkpoint --staged --explain

validate-full: validation-environment
	$(PYTHON) -m scripts.validation.cli plan --profile full --paths --explain

validate-doctor: validation-environment
	@$(PYTHON) -m scripts.validation.cli plan --profile doctor --scope $(VALIDATION_DOCTOR_SCOPE) --explain >/dev/null
	$(PYTHON) scripts/validation/doctor.py --scope $(VALIDATION_DOCTOR_SCOPE) $(VALIDATION_DOCTOR_FLAGS)

validate-project-control: validate-full validate-project-control-legacy
	@printf '%s\n' '{"target":"validate-project-control","status":"PASS","compatibility_wrapper":true,"deprecated":true,"planner_profile":"full","execution_authority":"legacy"}'

validate-project-control-legacy: validation-environment
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
