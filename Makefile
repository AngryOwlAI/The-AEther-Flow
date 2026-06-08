PYTHON ?= .venv/bin/python

.PHONY: validate-memory

validate-memory:
	@test -x "$(PYTHON)" || { printf '%s\n' "Missing $(PYTHON). Create the local environment with: python3 -m venv .venv"; exit 1; }
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
	$(PYTHON) .codex/skills/project-memory-system/scripts/sync_obsidian_vault.py
	$(PYTHON) .codex/skills/project-memory-system/scripts/lint_obsidian_vault.py --require-index
	$(PYTHON) -m unittest discover -s tests
	$(PYTHON) .codex/skills/project-memory-system/scripts/query_memory.py status --json
	$(PYTHON) .codex/skills/project-memory-system/scripts/query_memory.py search "Lorentzian metric" --formats tex,pdf --limit 5 --json
