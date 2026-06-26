"""Fixtures for the pwa orchestrator's cross-repo integration tests.

These are the tests that **cannot** run in GitHub CI: they need all three step
packages installed *and* real watershed data + the Raven binary. The
orchestrator's CI is build-only by design (no cross-repo PAT), so this suite is
strictly local — exactly where it belongs, since a developer running it has all
three repos installed.

The pipeline steps hand off through the filesystem, so the developer points
each step's config at a shared data layout and we run them in order:

* ``PWA_STEP0_CONFIG``          — filled-in pwa_config.yml      (Step 0)
* ``PWA_NC_PROCESSING_CONFIG``  — filled-in nc_processing.yml   (Step 1)
* ``PWA_RAVEN_INPUTS_CONFIG``   — filled-in raven_inputs.yml    (Step 2)
* ``PWA_RAVEN_BINARY`` (optional) — explicit Raven path; else resolved on PATH.

The ``pipeline_configs`` fixture skips unless *all three* configs are present,
so a partial setup is a clean skip rather than a confusing half-run.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

_CONFIG_ENV_VARS = {
    "step0": "PWA_STEP0_CONFIG",
    "nc_processing": "PWA_NC_PROCESSING_CONFIG",
    "raven_inputs": "PWA_RAVEN_INPUTS_CONFIG",
}


@pytest.fixture
def pipeline_configs() -> dict[str, Path]:
    """Resolve all three step config paths, or skip if any is missing."""
    resolved: dict[str, Path] = {}
    missing: list[str] = []
    for step, env_var in _CONFIG_ENV_VARS.items():
        value = os.environ.get(env_var)
        if not value:
            missing.append(env_var)
            continue
        path = Path(value)
        if not path.is_file():
            pytest.fail(f"{env_var}={value!r} is not a file")
        resolved[step] = path
    if missing:
        pytest.skip(
            "Full-pipeline integration needs all step configs. Missing: "
            + ", ".join(missing)
            + ". Point each at a filled-in config sharing one data layout."
        )
    return resolved


@pytest.fixture(scope="session")
def raven_on_path() -> None:
    """Skip unless a Raven binary is resolvable (PWA_RAVEN_BINARY or PATH)."""
    if os.environ.get("PWA_RAVEN_BINARY"):
        return
    if shutil.which("Raven") or shutil.which("Raven.exe"):
        return
    pytest.skip(
        "Raven binary not found. Install Raven, put it on PATH, "
        "or set PWA_RAVEN_BINARY."
    )
