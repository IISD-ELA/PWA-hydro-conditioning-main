"""Re-export regression tests for the pwa orchestrator package.

Locks in the umbrella import surface — `import pwa` should expose every
canonical public API symbol (configs, run_* functions, result
dataclasses) of the four underlying step packages.

If a future refactor moves a symbol or renames a callable, these tests
fail and force the maintainer to update both the source package AND the
orchestrator's __init__ in lockstep — the alternative is a notebook
user discovering the breakage at runtime.
"""

from __future__ import annotations

import pwa


def test_version_string_is_set() -> None:
    assert pwa.__version__
    assert isinstance(pwa.__version__, str)


def test_all_exports_resolve_to_real_attributes() -> None:
    """Every name in pwa.__all__ should be importable from the package."""
    for name in pwa.__all__:
        assert hasattr(pwa, name), f"pwa.__all__ lists {name!r} but pwa has no such attribute"


# ---------------------------------------------------------------------------
# Step 0 — pwa-tools
# ---------------------------------------------------------------------------


def test_step0_config_is_pwa_tools_class() -> None:
    from pwa_tools.config import PwaConfig as Source
    assert pwa.PwaConfig is Source


def test_step0_runner_is_pwa_tools_function() -> None:
    from pwa_tools.runner import run_step0 as source_run, Step0Result as SourceResult
    assert pwa.run_step0 is source_run
    assert pwa.Step0Result is SourceResult


# ---------------------------------------------------------------------------
# Step 1 — pwa-raven
# ---------------------------------------------------------------------------


def test_step1_symbols_are_pwa_raven_originals() -> None:
    from pwa_raven.nc_processing import (
        NcProcessingConfig as SourceCfg,
        NcProcessingResult as SourceResult,
        run_nc_processing as source_run,
    )
    assert pwa.NcProcessingConfig is SourceCfg
    assert pwa.NcProcessingResult is SourceResult
    assert pwa.run_nc_processing is source_run


# ---------------------------------------------------------------------------
# Step 2 — pwa-raven
# ---------------------------------------------------------------------------


def test_step2_symbols_are_pwa_raven_originals() -> None:
    from pwa_raven.raven_inputs import (
        RavenInputsConfig as SourceCfg,
        RavenInputsResult as SourceResult,
        run_raven_inputs as source_run,
    )
    assert pwa.RavenInputsConfig is SourceCfg
    assert pwa.RavenInputsResult is SourceResult
    assert pwa.run_raven_inputs is source_run


# ---------------------------------------------------------------------------
# Step 3 — pwa-calibration
# ---------------------------------------------------------------------------


def test_step3_symbols_are_pwa_calibration_originals() -> None:
    from pwa_calibration.runner import run_calibration as source_run
    from pwa_calibration.setup import CalibrationConfig as SourceCfg
    assert pwa.CalibrationConfig is SourceCfg
    assert pwa.run_calibration is source_run


# ---------------------------------------------------------------------------
# Shape: callables are callable, configs are classes
# ---------------------------------------------------------------------------


def test_run_functions_are_callable() -> None:
    for name in ("run_step0", "run_nc_processing", "run_raven_inputs", "run_calibration"):
        assert callable(getattr(pwa, name)), f"pwa.{name} should be callable"


def test_config_classes_are_classes() -> None:
    for name in ("PwaConfig", "NcProcessingConfig", "RavenInputsConfig", "CalibrationConfig"):
        attr = getattr(pwa, name)
        assert isinstance(attr, type), f"pwa.{name} should be a class"
