PYTHON ?= .venv/bin/python

.PHONY: setup spec spec-check quint-test quint-verify lint test skills-check repo-check host-assets-check verify

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

verify: quint-test lint test repo-check host-assets-check
