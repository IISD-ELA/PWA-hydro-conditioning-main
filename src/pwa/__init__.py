"""PWA pipeline orchestrator.

This package has no public Python API of its own. Its job is to declare
the four pipeline packages as dependencies (``pwa-tools``, ``pwa-raven``,
``pwa-calibration``) and expose unified CLI commands (``pwa-step0`` ..
``pwa-step3``, ``pwa-init-step0`` .. ``pwa-init-step3``) so users have
one mental model across every pipeline step.

To use the underlying APIs from Python, import directly from the source
package — e.g. ``from pwa_raven.nc_processing import run_nc_processing``.
"""

__version__ = "0.1.0"
