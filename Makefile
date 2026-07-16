PYTHON ?= .venv/bin/python
MEMORY_SCRIPT_DIR := .codex/skills/project-memory-system/scripts
MEMORY_TEST_MODULES := tests.test_memory_operations tests.test_memory_cli_modes tests.test_memory_system tests.test_obsidian_wiki tests.test_validation_orchestration

.PHONY: setup-dev memory-sync memory-validate-core memory-doctor test-memory validate-memory validate-memory-full validate-project-control validate-html-explainers audit-documentation-surfaces

setup-dev:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) -m pip install -r requirements-dev.txt
	@printf '%s\n' '{"target":"setup-dev","status":"PASS","provisioning":true}'

memory-sync:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Run: make setup-dev PYTHON=$(PYTHON)"; exit 1; }
	PYTHONPATH="$(MEMORY_SCRIPT_DIR)" $(PYTHON) -c 'import json; from bootstrap_memory_system import memory_sync; receipt = memory_sync().to_dict(); print(json.dumps({"gate_id": "memory_sync", "status": "PASS", "mutated": receipt["mutated"], "local_retrieval_enabled": receipt["local_retrieval_enabled"], "counts": receipt["counts"], "changed": receipt["changed"], "created": receipt["created"], "pruned": receipt["pruned"]}, sort_keys=True))'

memory-validate-core:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Run: make setup-dev PYTHON=$(PYTHON)"; exit 1; }
	PYTHONPATH="$(MEMORY_SCRIPT_DIR)" $(PYTHON) -c 'import json; from bootstrap_memory_system import memory_validate_core; report = memory_validate_core(); print(json.dumps(report.to_dict(), sort_keys=True)); raise SystemExit(0 if report.ok else 1)'

memory-doctor:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Run: make setup-dev PYTHON=$(PYTHON)"; exit 1; }
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/sync_obsidian_vault.py
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/lint_obsidian_vault.py --require-index
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/query_memory.py status --json
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/query_memory.py search "Lorentzian metric" --formats tex,pdf --limit 5 --json
	@printf '%s\n' '{"target":"memory-doctor","status":"PASS","authority":"local_only"}'

test-memory:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Run: make setup-dev PYTHON=$(PYTHON)"; exit 1; }
	$(PYTHON) -m unittest $(MEMORY_TEST_MODULES)
	@printf '%s\n' '{"target":"test-memory","status":"PASS","module_count":5}'

validate-memory: memory-validate-core test-memory
	@printf '%s\n' '{"target":"validate-memory","status":"PASS","profile":"affected-memory-compatibility"}'

validate-memory-full: memory-sync memory-doctor
	$(PYTHON) $(MEMORY_SCRIPT_DIR)/bootstrap_memory_system.py --validate-only
	$(PYTHON) -m unittest discover -s tests
	@printf '%s\n' '{"target":"validate-memory-full","status":"PASS","profile":"full-memory-compatibility"}'

validate-project-control:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) scripts/project_control/classify_project_changes.py --json
	$(PYTHON) scripts/project_control/collect_project_improvement_signals.py --validate-emitted
	$(PYTHON) scripts/project_control/validate_documentation_impact.py
	$(PYTHON) scripts/project_control/audit_documentation_surfaces.py --skip-local
	$(PYTHON) .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
	$(PYTHON) scripts/spec_depth_lint.py --root .
	$(PYTHON) scripts/validate_publication_process.py --root .
	$(PYTHON) scripts/research_control/validate_research_control.py --check-diff
	$(PYTHON) -m unittest discover -s tests

validate-html-explainers:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
	$(PYTHON) scripts/spec_depth_lint.py --root .
	$(PYTHON) scripts/validate_publication_process.py --root .

audit-documentation-surfaces:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) scripts/project_control/audit_documentation_surfaces.py
