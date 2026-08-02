PYTHON ?= .venv/bin/python
SKILL_VALIDATOR ?= /home/t-tsuji/.codex/skills/.system/skill-creator/scripts/quick_validate.py

.PHONY: setup catalog catalog-check spec spec-check standards standards-check review-check test skills-check repo-check benchmark-certify benchmark-check audit verify

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

catalog:
	$(PYTHON) tools/devflow.py catalog

catalog-check:
	$(PYTHON) tools/devflow.py catalog --check

spec:
	$(PYTHON) .agents/skills/maintain-canonical-requirements/scripts/specflow.py generate

spec-check:
	$(PYTHON) .agents/skills/maintain-canonical-requirements/scripts/specflow.py check

standards:
	$(PYTHON) .agents/skills/verify-against-engineering-standards/scripts/standardsflow.py generate

standards-check:
	$(PYTHON) .agents/skills/verify-against-engineering-standards/scripts/standardsflow.py check

review-check:
	$(PYTHON) governance/reviews/validate.py --root . --commit HEAD

test:
	$(PYTHON) -m unittest discover -s tests -v

skills-check:
	$(PYTHON) tools/validate_repo.py --skills-only

repo-check:
	$(PYTHON) tools/validate_repo.py

benchmark-certify:
	$(PYTHON) -m benchmarks.harness.certify --root . --write

benchmark-check:
	$(PYTHON) -m benchmarks.harness.certify --root . --check
	$(PYTHON) -m unittest discover -s tests/benchmark -v

audit:
	$(PYTHON) tools/devflow.py audit

verify: catalog-check spec-check standards-check review-check benchmark-check test repo-check audit
