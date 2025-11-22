# UIF EEG Coherence Experiment — Baseline Outputs

This folder contains the baseline outputs for the UIF EEG Coherence Experiment (Experiment VI).  
These files represent the canonical, reproducible RSIPP/CHREM run used in the UIF Companion Experiments to quantify:

- Eyes-Closed vs Eyes-Open coherence shifts
- H–C–R operator fingerprints
- Subject / state / recording-level summaries
- Surrogate distributions
- P(k), kappa, and HMF-style spectral diagnostics

All files here are derived outputs only.  
Raw EEG signals are not redistributed — see `/UIF/data/eeg_coherence_experiment/` for manifests and provenance.

---

## Contents

### 1. Summary & Effect-Size Files
- EEG_effects_EC_vs_EO.json  
  Paired-sample EC−EO effects with bootstrap 95% CI and Cohen’s d.  
  Fields include:
  - mean_diff_EC_minus_EO
  - CI95_bootstrap
  - cohen_d_paired

- summary.json (if present)  
  Aggregated operator metrics for the baseline run.

---

### 2. Window-, State-, Subject-, and Recording-Level Tables

These are the core HCR datasets used in the UIF Companion plots:

- EEG_windows_HCR.csv  
  Per-window entropy H, complexity C, and coherence R.

- EEG_state_summary_R.csv  
  Mean coherence per state (EC, EO, task).

- EEG_subject_summary_R.csv  
  Subject-level coherence summaries.

- EEG_recording_summary_R.csv  
  Recording-level aggregates.

- EEG_surrogates_HCR.csv  
  Surrogate distribution used for statistical testing and null-model calibration.

---

### 3. Baseline Figures

All figures included in the UIF Companion:

- Fig_EC_vs_EO.png  
  Scatter comparison of EC vs EO coherence.

- Fig_EC_minus_EO_hist.png  
  Histogram of EC−EO coherence differences.

- Fig_EEG_HC_plane.png  
  H–C plane projection for the EEG dataset.

- Fig_pk.png (if present)  
  Spectral density P(k) comparison.

---

## How These Outputs Were Generated

All files were produced by running:

    python ut26_eeg_pipeline.py
    python eeg_subject_level_summary.py
    python plot_ec_vs_eo.py
    python plot_pk_only.py

from:

    /UIF/code/eeg_coherence_experiment/

These scripts:

- load EDF filenames via subset_manifest.csv  
- extract 1-second windows  
- compute H, C, R per window  
- generate subject/state/recording summaries  
- produce EC–EO comparison plots  
- compute spectral diagnostics  

---

## Integrity

Baseline integrity is checked using hashes stored in:

    UIF/output/eeg_coherence_experiment/SHA256SUMS.txt

Verify with:

    sha256sum -c SHA256SUMS.txt

---

## Citation

If using these outputs, please cite:

Hiles, S.E.N. (2025).  
"UIF Companion Experiments — EEG Coherence Outputs."  
Zenodo. DOI: 10.5281/zenodo.17434412

Underlying dataset:

Goldberger et al. (2000). PhysioNet: Components of a New Research Resource for Complex Physiologic Signals.  
PhysioNet / BCI2000 Motor Imagery Dataset.

---

## Notes

- These are baseline outputs used to anchor Experiment VI in the UIF Companion.  
- They provide the canonical EC/EO effect size used to compare EEG vs quasars.  
- No EDF files are stored here; only derived HCR tables and figures.
