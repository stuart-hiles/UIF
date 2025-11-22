# UIF Quasar–Cosmology Experiment — Baseline Outputs

This folder contains the **baseline cosmology-lite emulator outputs** used in the
UIF Companion for the *Quasar Cosmology Experiment* (Experiment IV in the emulator
sequence; observationally anchored in Experiment VII).

These files represent a single, reproducible 3-D collapse–return run  
(N = 96³, T = 300, seed = 123) used to generate:

- Power spectrum P(k)
- Weak-lensing–like κ maps
- HMF (halo-mass–function–like) clumping statistics
- Summary operator measures (R, pruning, coherence)

All files in this directory are **derived outputs only**.  
No observational quasar data are stored here.

---

## Contents

### 1. Summary Diagnostics

- **summary.json**  
  Canonical metadata for the baseline emulator run.  
  Fields include:
  - `N`: lattice size (96³)  
  - `T`: timesteps (300)  
  - `final_mean_s`: final mean coherence  
  - `total_trace_R`: cumulative informational trace  
  - `total_prunes`: total collapse–return pruning events  
  - `SCIPY_OK`: verification of numerical stability

- **summary.png**  
  Visual summary of the run (mean-s, pruning, basic diagnostics).

---

### 2. Power Spectrum Outputs

- **pk.csv**  
  Baseline power spectrum P(k) derived from the lattice field.  
  Used for comparison with:
  - DRW/variability spectra  
  - EEG P(k)  
  - Goldilocks-band emulator predictions

- **pk.png** (if present)  
  Visualisation of the P(k) curve.

---

### 3. κ-Map Outputs (Weak-Lensing Analogue)

- **kappa_map.png**  
  κ-projection of the coherence field, analogous to weak gravitational lensing.

- **kappa_ps.csv**  
  Power spectrum of the κ-map.

- **kappa_ps.png**  
  Visualisation of the κ power spectrum.

---

### 4. HMF-Like Clumping Statistics

- **hmf.csv**  
  Histogram approximating a toy halo-mass function (FoF on |ΔI|-thresholded regions).

- **hmf.png**  
  HMF visualisation.

These diagnostics are used in the UIF Companion to demonstrate:

- clumping behaviour under collapse–return,
- the preservation of BAO-like structure in synthetic fields,
- parallels with large-scale structure statistics.

---

## How These Outputs Were Generated

All files were produced by running:

    python ut26_cosmo3d.py
    python ut26_cosmo3d_hmf.py
    python plot_kappa.py
    python plot_pk.py

from:

    /UIF/code/quasar_cosmology_experiment/

This baseline run uses the default Goldilocks-band operator settings:

- β = 3.0  
- λ_R ≈ 0.20  
- η* ≈ 0.55  
- Γ ≈ 0.9

These match the calibrations reported in the UIF Companion and Papers III–IV.

---

## Purpose of the Baseline

This baseline is used as the **control lattice** for:

- hysteresis tests  
- receive–return coupling behaviour  
- κ-power suppression plots  
- comparison to real quasar variability operators (Experiment VII)  
- consistency checks across Papers IV–V

It provides the canonical lattice reference for all cosmology-lite comparisons.

---

## Citation

If using these outputs, please cite:

Hiles, S.E.N. (2025).  
"UIF Companion Experiments — Cosmology-Lite Baseline Outputs."  
Zenodo. DOI: 10.5281/zenodo.17434412

---

## Notes

- No quasar light curves exist in this folder — observational data live under  
  `/UIF/data/quasar_cosmology_experiment/`.

- These outputs correspond to emulator-only cosmology runs used to  
  contextualise the quasar variability experiment.
