PYTHON ?= .venv/bin/python

.PHONY: setup catalog catalog-check spec spec-check standards standards-check review-check test skills-check repo-check host-assets-check as-built-check consistency-check audit verify

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

host-assets-check:
	$(PYTHON) tools/generate_host_assets.py check

as-built-check:
	$(PYTHON) .agents/skills/generate-implementation-design/scripts/qualityflow.py thresholds
	$(PYTHON) .agents/skills/generate-implementation-design/scripts/qualityflow.py suppressions --root .

consistency-check:
	$(PYTHON) tools/audit_consistency.py

audit:
	$(PYTHON) tools/devflow.py audit

verify: setup catalog-check spec-check standards-check review-check test repo-check host-assets-check as-built-check consistency-check audit
