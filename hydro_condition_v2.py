"""Step 0 hydro-conditioning pipeline — declarative v2 entry point.

Sister script to ``hydro_condition.py`` (the legacy interactive runner).

Differences from v1:
  * Configuration comes from a YAML file (``pwa_config.yml`` by default),
    not from interactive ``input()`` prompts.
  * Uses the new modular ``pwa_tools.runner.run_step0`` API, which
    activates the bug fixes added during the 2026 cleanup project
    (BUG-001 through BUG-021 — see the upstream bug-tracker).
  * Fails fast if expected input files are missing — saves the user
    from a 30-minute LiDAR resample crashing on a missing shapefile.
  * Status output goes through the standard ``logging`` module, so
    log level, format, and routing are user-configurable.

Usage::

    # Generate a config interactively (one-time setup)
    python -m pwa_tools.init_config pwa_config.yml

    # Run the pipeline
    python hydro_condition_v2.py
    python hydro_condition_v2.py --config pwa_config.yml --wetlands
    python hydro_condition_v2.py --log-level DEBUG

The legacy v1 script remains in place for users who depend on the
interactive workflow; it will be deprecated once Thomas signs off on
the v2 UX.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from pwa_tools.config import PwaConfig
from pwa_tools.runner import run_step0


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the PWA Step 0 hydro-conditioning pipeline.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("pwa_config.yml"),
        help="Path to the pwa_config.yml file (default: ./pwa_config.yml).",
    )
    parser.add_argument(
        "--wetlands",
        action="store_true",
        help="Also generate the wetland polygons shapefile (not required for Raven).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(message)s",
    )

    if not args.config.is_file():
        print(
            f"Config file not found: {args.config}\n"
            "Generate one with: python -m pwa_tools.init_config pwa_config.yml",
            file=sys.stderr,
        )
        return 1

    config = PwaConfig.from_yaml(args.config)
    result = run_step0(config, generate_wetlands=args.wetlands)

    print()
    print(f"Depression depths : {result.depression_depths}")
    print(f"Depression raster : {result.depression_raster}")
    if result.wetlands is not None:
        print(f"Wetland polygons  : {result.wetlands}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
