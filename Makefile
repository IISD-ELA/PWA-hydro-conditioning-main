# Test/build targets for the pwa orchestrator.
#
#   make build        build sdist + wheel (what GitHub CI runs — no siblings needed)
#   make test         re-export unit tests (needs the three step packages installed)
#   make integration  full-pipeline e2e, local-only (needs all step configs + Raven)
#
# The orchestrator's CI is build-only on purpose (no cross-repo PAT); `test`
# and `integration` are local targets for a checkout that has all three repos
# installed. See tests/integration/README.md.
.PHONY: build test integration

build:
	python -m pip install --upgrade build >/dev/null && python -m build

test:
	pytest tests/unit

integration:
	pytest tests/integration
