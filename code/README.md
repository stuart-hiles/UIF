UIF Code — Experiment Pipelines
===================================

This directory contains the full Python-based experiment pipelines used in the
Unifying Information Field (UIF) Companion Experiments.
Each submodule corresponds to a distinct class of experiments: EEG coherence,
cosmology-lite simulations, quasar coherence, quasar cosmology, quasar scaling,
and quasar variability (Experiment VII).

The folder structure mirrors the organisation described in the UIF Companion paper and
supports full reproducibility of all reported results.

---

## Contents

### 1. `informational_difference_calibration_experiment/`
Python scripts for running and analysing the UIF cosmology-lite emulator:

- collapse–return field simulation (`ut26_cosmo3d.py`)
- hysteresis probes
- γ-sweeps
- stability threshold maps (η* × λR)
- H–C plane extraction and ΔI / R∞ diagnostics
- figure-generation scripts for emulator outputs

These scripts generate the results under:
UIF/output/cosmology_lite_experiment/

---

### 2. `eeg_coherence_experiment/`
RSIPP/CHREM-style pipelines implementing the EEG coherence analysis (Experiment VI):

- 1-second window extraction
- entropy–complexity (H–C) plane construction
- surrogate distributions (phase randomisation)
- ΔI, Γ, λR, R∞, k estimation
- EC vs EO coherence comparisons
- operator fingerprint generation

Matches the dataset and manifests stored under:
UIF/data/eeg_coherence_experiment/

Outputs are written to:
UIF/output/eeg_coherence_experiment/

---

### 3. `quasar_coherence_experiment/`
Scripts used to fit UIF collapse–return coherence models to SDSS Stripe 82 quasars:

- CH-plane reconstruction
- logistic / linear model comparisons
- ΔI-based collapse–return signatures for quasar light curves
- operator extraction for coherence behaviour

Outputs align with:
UIF/output/quasar_coherence_experiment/

---

### 4. `quasar_cosmology_experiment/`
Python scripts and utilities used in the UIF quasar cosmology experiment:

- H–C plane diagnostics for cosmology-facing operators
- logistic R(z) fits
- bootstrapped confidence intervals
- variability-linked cosmological diagnostics
- ΔIσ and R∞ behaviour across lookback time

Corresponding outputs are stored in:
UIF/output/quasar_cosmology_experiment/

---

### 5. `quasar_scaling_experiment/`
Implements the mass–timescale, luminosity–sigma, and coherence scaling analyses:

- τ–MBH regressions
- τ–Mi and σ–Mi scaling relations
- operator-linked slopes for Γ, λR, ΔIσ
- HC-plane extraction for scaling datasets
- bootstrap CIs for all relations

Supports the datasets in:
UIF/data/quasar_scaling_experiment/

---

### 6. `quasar_variability_experiment/`
(Experiment VII — fully implemented)

Python pipeline for the SDSS Stripe 82 quasar variability operator recovery:

- computation of H, C, R for ~9,258 quasars
- ΔIσ (variability–richness) extraction
- recursion Γ via τ–MBH slope
- receive–return coupling λR via high-R fractions
- coherence ceiling R∞ via p95 log-σ
- recharge rate k via τ-spread
- operator fingerprint plots
- H–C geometry (low/mid/high-z)
- scaling relations (τ–MBH, τ–Mi, σ–Mi)
- R-histograms across redshift bins

Corresponding outputs are written to:
UIF/output/quasar_variability_experiment/

This module completes the empirical validation arc for Papers I–V
and provides the astrophysical operator measurements used in UIF VI–VI.

---

### 8. `geometric_torsion_experiment/`
(Experiment VIII — new cross-domain test of the UIF torsion invariant)

Python pipeline implementing the **geometric torsion (τ_d)** analysis across  
EEG operator trajectories (local biological systems) and  
Stripe 82 quasar operator trajectories (cosmic substrate systems):

- ingestion of EEG and quasar operator tables
- Z-score normalization of operator trajectories within each domain
- construction of 3-point operator curves  
  \( O = (\Delta I,\; \Gamma,\; \lambda_R) \)
- computation of **geometric torsion**  
  \( \tau_d = \frac{(\Delta O_1 \times \Delta O_2)_z}{\|\Delta O_1\|\,\|\Delta O_2\|} \)
- 10,000-sample **bootstrap resampling** using operator uncertainties  
  to estimate 68% confidence intervals
- domain-wise torsion recovery:
  - **τ_EEG** for EO → TASK → EC  
  - **τ_QSO** for High-z → Mid-z → Low-z
- construction of the 3-panel torsion geometry figure:
  - *Panel A:* EEG operator trajectory  
  - *Panel B:* Quasar operator trajectory  
  - *Panel C:* Normalised cross-domain comparison (τ_d overlap)
- supplementary torsion-anomaly figure showing  
  Ω_τ (informational load torsion) across states

Outputs are written to:  
`UIF/output/geometric_torsion_experiment/`

This experiment provides the **first empirical test of the torsion term** \( \tau_I \)  
predicted by the UIF informational Lagrangian, linking **Papers III and VI**  
and supplying the geometric-invariant evidence referenced in **UIF VII**.

---

## Reproducibility Notes

All experiment modules follow the same structure:

/UIF/code/<experiment>/
    *.py              # reproducible scripts
    plot_*.py         # figure-generation scripts
    *_operators.py    # operator extraction
    README.md         # documentation for that module

Data ingestion, manifests, and metadata live under:
UIF/data/<experiment>/

Figures, CSVs, summaries, and checksum files live under:
UIF/output/<experiment>/

All experiments support full reproducibility with the manifest files,
metadata JSONs, and SHA256SUMS validation included in the repository.

---

## License

- Code: GPL-3.0
- Documentation: CC BY-NC 4.0

---

For operator definitions, experimental rationale, and reproducibility details,
see the UIF Companion Experiments paper and UIF Papers I–VII.
