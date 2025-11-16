# Quasar Coherence Experiment — Data Folder

This folder contains the **processed coherence dataset** used in the UIF Companion Experiments
(Quasar Coherence Analysis, Section 5).  
Only **derived** data are stored here — raw Stripe 82 catalogs are not redistributed.

## Purpose

These data support the coherence fits, logistic models, and operator reconstructions presented in:

**Hiles, S.E.N. (2025). _UIF Companion Experiments_. Zenodo.**  
DOI (all versions): https://doi.org/10.5281/zenodo.17434412

The dataset here corresponds specifically to **Experiment 5 — Quasar Coherence**.

## Source (Provenance)

Raw photometric and variability data come from the **SDSS Stripe 82 Southern Sample**, originally provided at:

- SDSS Stripe 82 (Southern Sample) QSO light-curve catalog  
  https://faculty.washington.edu/ivezic/macleod/qso_s82/

The file stored here, `quasar_raw_HC_all.csv`, is a **processed, cleaned, merged, and reduced** version of the original SDSS files:

- `master_QSO_S82.dat`  
- `DB_QSO_S82.dat`  
- DRW parameter files: `s82drw_*.dat`

### Processing steps (summarised)
The following preprocessing was applied before inclusion in this repository:

1. Import master QSO metadata  
2. Merge with DRW (damped random walk) stochastic variability parameters  
3. Align calibration fields and remove missing / invalid entries  
4. Compute coherence-related derived variables  
   - mean coherence ⟨s⟩  
   - logistic class indicators  
   - binned-R distributions  
5. Export to a single analysis-ready CSV  
   → `quasar_raw_HC_all.csv`

## Files

| File | Description |
|------|-------------|
| **quasar_raw_HC_all.csv** | Cleaned & merged quasar dataset used for coherence modelling (Experiment 5). Includes magnitudes, DRW params, variability features, and coherence-ready fields. |
| **README.md** | This document. |

## Citation Requirements

If using these data in published work, please cite:

- **UIF Companion Experiments dataset:**  
  Hiles, S.E.N. 2025. *UIF Companion Experiments*. Zenodo.  
  DOI: https://doi.org/10.5281/zenodo.17434412

- **Original SDSS Stripe 82 survey and catalog:**  
  (as recommended by the SDSS team)  
  - Ivezić et al. (2007, 2008)  
  - MacLeod et al. (2010, 2012)  
  - Schneider et al. (2010)

## Notes

- This folder contains only **processed** data.  
- Full reproducibility of coherence figures requires running scripts from:  
  `UIF/code/quasar_coherence_experiment/`
