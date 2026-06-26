# pwa orchestrator integration tests

The full PWA pipeline, **Step 0 → Step 2**, driven both ways users drive it:
through the `pwa` umbrella namespace (notebooks/scripts) and through the
installed `pwa-*` console scripts (the shell). This is the cross-repo seam —
the steps hand off through the filesystem, so this is where drift between the
three packages shows up.

**Local-only by necessity.** These tests need all three step packages installed
*and* real data + Raven. The orchestrator's GitHub CI is build-only (no
cross-repo PAT), so it never runs them — a developer with all three repos
installed does. They skip cleanly unless every input is present.

## Inputs (environment)

| Variable | Purpose |
|---|---|
| `PWA_STEP0_CONFIG` | filled-in `pwa_config.yml` (Step 0) |
| `PWA_NC_PROCESSING_CONFIG` | filled-in `nc_processing.yml` (Step 1) |
| `PWA_RAVEN_INPUTS_CONFIG` | filled-in `raven_inputs.yml` (Step 2) |
| `PWA_RAVEN_BINARY` | optional explicit Raven path (else PATH) |

Point all three configs at one shared data layout so each step's outputs feed
the next. If any is missing, the suite skips (it won't half-run).

Step 3 (calibration) is excluded — it's a long MPI job with its own
`pwa_calibration` integration test.

## Run

```bash
make integration

# Or directly (all three required):
PWA_STEP0_CONFIG=.../pwa_config.yml \
PWA_NC_PROCESSING_CONFIG=.../nc_processing.yml \
PWA_RAVEN_INPUTS_CONFIG=.../raven_inputs.yml \
  pytest tests/integration -v
```
