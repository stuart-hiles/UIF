# UIF Output Directory

This directory contains all *derived outputs* produced by the UIF Companion Experiments
across informational difference calibration (cosmology-lite), EEG, quasar, and coherence-scaling studies. These outputs mirror
the structure of `/UIF/data/` and correspond directly to the scripts in `/UIF/code/`.

Each subfolder contains its own README.md with detailed descriptions of:
- generated figures
- intermediate CSVs
- operator estimates (ΔI, Γ, λᴿ, β, R∞, k)
- baseline comparisons
- integrity hashes
- reproducibility instructions

All outputs are fully reproducible using the code in `/UIF/code/` and the data in `/UIF/data/`.

---

## 📁 Directory Structure

### `/informational_difference_calibration_experiement/`
Outputs from the UIF *cosmology-lite* emulator:
- HC-plane maps  
- γ-sweep curves  
- threshold maps  
- κ power spectra  
- CSVs, PNGs, summary JSON  
- `baseline/` snapshot for regression testing  

These outputs are fully synthetic (no external datasets required).

---

### `/eeg_coherence_experiment/`
Outputs from the EEG coherence analysis pipeline:
- state/recording/subject coherence summaries  
- surrogate-based H–C–R metrics  
- 1-second H, C, R windows for ΔI and Γ  
- H–C plane plots and P(k) spectra  
- `SHA256SUMS.txt` integrity ledger  
- complete `baseline/` run for operator stability checks  

No raw EEG is included.

---

### `/informational_difference_calibration_experiemnt/`
Outputs from quasar coherence estimation:

### `/quasar_coherence_experiment/`
Outputs from quasar coherence estimation:
- logistic fits  
- HC-plane reconstructions  
- bootstrapped confidence intervals  
- coherence-model coefficients  
- diagnostic PNGs  

Derived from processed SDSS Stripe 82 inputs.

---

### `/quasar_cosmology_experiment/`
Outputs used for cosmology validation using real quasar variability:
- κ-maps  
- γ-sweep curves  
- threshold maps  
- HMF, P(k), summary JSON  
- baseline emulator comparison  

These outputs compare Stripe 82 light curves with UIF cosmology-lite predictions.

---

### `/quasar_scaling_experiment/`
Outputs supporting quasar scaling experiments (Figure 5.x in the UIF Companion paper):
- bootstrapped logistic fits across mass/luminosity bins  
- CH-plane reconstructions  
- slope tables  
- publication-ready figures  

---

### `/quasar_variability_experiment/`
Reserved for future variability experiments (structure-function, DRW, extended timescales).

This folder is intentionally **empty**.

---

## 🔍 Licensing Notes

- All derived outputs in this directory are released under **CC BY-NC 4.0**.  
- Outputs based on external datasets (e.g., PhysioNet EEG, SDSS photometry) inherit those datasets’ original licensing restrictions.  
- No restricted raw data are redistributed.

---

## 📌 Summary

This folder is the unified collection of all UIF-derived results.  
It ensures:
- clear mapping between `/code`, `/data`, and `/output`  
- reproducibility for all experiments  
- clean separation between raw data and derived products  
- structured organisation for Zenodo publication

Refer to each subfolder’s README.md for experiment-specific details.
