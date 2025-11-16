# Quasar Scaling Experiment — Data Folder

This folder contains the processed datasets used in the
**UIF Quasar Scaling Experiments** (mass–timescale and luminosity–variability scaling;
Experiment 6 in the Companion paper).

Only derived and analysis-ready CSVs are stored here.  
Raw SDSS Stripe 82 catalogs are NOT redistributed.

---

## Purpose

These datasets support the scaling analyses in the UIF Companion Experiments,
including:

- τ–M_BH scaling (damped random walk timescale vs. black hole mass)
- τ–M_i and σ–M_i luminosity scaling relations
- bootstrap uncertainty estimation
- slope inference for cosmological operator calibration

---

## Files

### **quasar_raw_HC_all.csv**
A cleaned and merged dataset derived from the SDSS Stripe 82 Southern sample.  
Contains:

- redshift  
- absolute magnitudes  
- DRW parameters (τ, σ)  
- variability metrics  
- coherence-related features  
- host parameters (where available)  

This is the *same base file* used in the quasar coherence experiment,
but is reused here for the scaling fits.

### **ut26_R_binned_boot.csv**
Bootstrap-resampled binned-radius distribution used for slope analysis and  
mass/luminosity scaling verification.

---

## Provenance

The processed datasets here were derived from the following raw SDSS files:

- `master_QSO_S82.dat`  
- `DB_QSO_S82.dat`  
- DRW time-series parameter files: `s82drw_*.dat`

Original SDSS Stripe 82 data courtesy of:

**SDSS Southern Stripe 82 QSO Catalogue**  
https://faculty.washington.edu/ivezic/macleod/qso_s82/

Preprocessing steps included:

1. Import master catalog and DRW variability tables  
2. Merge with photometry and luminosity information  
3. Remove missing/invalid entries  
4. Compute derived fields for scaling analysis  
5. Export final CSVs for UIF experiments

---

## Citation Requirements

If using these data, please cite:

### **UIF Companion Experiments Dataset**
Hiles, S.E.N. (2025). *UIF Companion Experiments*. Zenodo.  
DOI (all versions): https://doi.org/10.5281/zenodo.17434412

### **SDSS Stripe 82 Survey**
Cite the SDSS team as recommended:

- Ivezić et al. (2007, 2008)  
- MacLeod et al. (2010, 2012)  
- Schneider et al. (2010)

---

## Notes

- This directory contains only **processed** and **reduced** datasets.  
- Figures and slope-fit outputs are located in:  
  `UIF/output/quasar_scaling_experiment/`  
- Python scripts used to generate these tables:  
  `UIF/code/quasar_scaling_experiment/`
