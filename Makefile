PYTHON ?= .venv/bin/python

.PHONY: setup spec spec-check quint-test quint-verify lint test skills-check repo-check host-assets-check reference-check verify

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	npm ci --ignore-scripts

spec:
	$(PYTHON) tools/quintflow.py generate

spec-check:
	$(PYTHON) tools/quintflow.py check

quint-test:
	$(PYTHON) tools/quintflow.py test

quint-verify:
	$(PYTHON) tools/quintflow.py verify

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m unittest discover -s tests -v

skills-check:
	$(PYTHON) tools/validate_repo.py --skills-only

repo-check:
	$(PYTHON) tools/validate_repo.py

host-assets-check:
	$(PYTHON) tools/generate_host_assets.py check

reference-check:
	$(PYTHON) .agents/skills/generate-implementation-design/scripts/reference_inventory.py .agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json --out .agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.md --check

verify: reference-check quint-verify lint test repo-check host-assets-check
