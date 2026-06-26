"""End-to-end: the full PWA pipeline, Step 0 → Step 2, driven two ways.

Why this exists
---------------
Nothing else tests the pipeline as a whole. Each repo tests its own step, and
the orchestrator's unit tests only check that ``import pwa`` re-exports the
right symbols. But the steps hand off through the filesystem (Step 0's
depression-depths shapefile and Step 1's GridWeights feed Step 2), and that
seam — across three independently-developed packages — is exactly where drift
hides. These tests run the real steps in order on real data and assert each
handoff artifact actually lands.

Two entry points, because users have two:

* ``test_pipeline_chain_python_api`` — the notebook/scripting path, via the
  ``pwa`` umbrella namespace.
* ``test_pipeline_chain_cli`` — the shell path, via the installed ``pwa-*``
  console scripts (also proves entry-point registration).

Step 3 (calibration) is intentionally excluded — it's a 24-hour MPI job with
its own ``pwa_calibration`` integration test; including it here would make the
pipeline test untenable to run.

Local-only; both skip unless all three step configs and the Raven binary are
present (see ``conftest.py``).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.slow
def test_pipeline_chain_python_api(pipeline_configs, raven_on_path):
    """Run Steps 0→1→2 through the ``pwa`` namespace; assert each handoff lands."""
    import pwa

    # Step 0 — hydro-conditioning. Produces the depression-depths shapefile
    # that Step 2 consumes.
    step0 = pwa.run_step0(pwa.PwaConfig.from_yaml(pipeline_configs["step0"]))
    assert Path(step0.depression_depths).is_file(), "Step 0 depression depths missing"

    # Step 1 — NetCDF processing. Produces GridWeights.txt for Step 2.
    nc = pwa.run_nc_processing(
        pwa.NcProcessingConfig.from_yaml(pipeline_configs["nc_processing"])
    )
    assert Path(nc.grid_weights).is_file(), "Step 1 GridWeights missing"

    # Step 2 — Raven input generation. Consumes the above; produces the model.
    inputs = pwa.run_raven_inputs(
        pwa.RavenInputsConfig.from_yaml(pipeline_configs["raven_inputs"])
    )
    for label in ("rvi", "rvp", "rvh", "rvc"):
        assert Path(getattr(inputs, label)).is_file(), f"Step 2 {label} missing"


@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.slow
def test_pipeline_chain_cli(pipeline_configs, raven_on_path):
    """Run Steps 0→1→2 through the installed ``pwa-*`` console scripts.

    Invoked via ``python -m`` so the test uses the same interpreter/venv it runs
    under (the entry-point modules back the console scripts one-to-one).
    """
    steps = [
        ("pwa_tools.run_step0", pipeline_configs["step0"]),
        ("pwa_raven.run_nc_processing", pipeline_configs["nc_processing"]),
        ("pwa_raven.run_raven_inputs", pipeline_configs["raven_inputs"]),
    ]
    for module, config in steps:
        completed = subprocess.run(
            [sys.executable, "-m", module, "--config", str(config)],
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, (
            f"{module} failed (exit {completed.returncode}).\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
