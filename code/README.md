# UIF Code — Experiment Pipelines

This directory contains the full set of Python-based experiment pipelines used in the 
Unifying Information Field (UIF) Companion Experiments. Each submodule corresponds to a 
distinct class of experiments: EEG coherence, cosmology-lite simulations, quasar 
coherence, quasar scaling, and placeholders for future variability studies.

The folder structure mirrors the organisation described in the UIF Companion paper and 
supports full reproducibility of all reported results.

---

## Contents

### 1. `cosmology_lite_experiment/`
Python scripts for running and analysing the UIF cosmology-lite emulator:

- collapse–return field simulation (`ut26_cosmo3d.py`)
- hysteresis probes
- γ-sweeps
- threshold maps (η* × λR)
- figure-generation scripts for the emulator diagnostics

These scripts generate the output files stored under:
`/UIF/output/cosmology_lite_experiment/`.

---

### 2. `eeg_coherence_experiment/`
Pipelines implementing the RSIPP/CHREM-based EEG processing:

- subject-level summaries
- H–C plane construction
- surrogate distributions
- ΔI, Γ, λR and R∞ estimation
- reproducible figure outputs

Matches the dataset and manifest files stored under:
`/UIF/data/eeg_coherence_experiment/`.

---

### 3. `quasar_coherence_experiment/`
Scripts used to fit the UIF collapse–return coherence models to SDSS Stripe 82 quasars:

- coherence model definitions
- curve fitting and model comparison
- ΔI-based collapse–return signatures for astronomical time series

Outputs align with:
`/UIF/output/quasar_coherence_experiment/`.

---

### 4. `quasar_cosmology_experiment/`
Python scripts and analysis utilities used for the UIF quasar cosmology experiment:

- CH-plane reconstruction
- logistic fits
- bootstrapped confidence intervals
- variability-related diagnostics for collapsed runs

Corresponding outputs are stored in:
`/UIF/output/quasar_cosmology_experiment/`.

---

### 5. `quasar_scaling_experiment/`
Implements the mass–timescale, luminosity–sigma, and coherence scaling analyses:

- CH-plane extraction
- logistic parameter fits
- scaling-law regressions
- bootstrap CIs for all relations

Supports the data in:
`/UIF/data/quasar_scaling_experiment/`.

---

### 6. `quasar_variability_experiment/`
**Reserved for future work.**  
This module will host scripts for:

- structure functions
- PSD fitting
- variability-based operator estimation
- ΔI-variability diagnostics

Currently included as a placeholder to maintain API stability across UIF versions.

---

## Reproducibility Notes

All experiment modules follow a standard structure:

```
/UIF/code/<experiment>/
    run_*.py          # reproducible experiment drivers
    plot_*.py         # figure-generation scripts
    *_models.py       # model definitions / likelihoods
    *_bootstrap.py    # statistical inference tools
    README.md         # documentation for that module
```

Data ingestion, manifests, and checksum validation live in:
`/UIF/data/<experiment>/`.

Experiment artefacts and diagnostic figures are written to:
`/UIF/output/<experiment>/`.

The same run-tags used in the UIF Companion paper will reproduce all published figures.

---

## License

- Code: **GPL-3.0**
- Documentation: **CC BY-NC 4.0**

---

For details on operators, experiment design, and run-tag definitions, see the UIF 
Companion Experiments paper.

