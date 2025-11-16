# Quasar Cosmology Experiment Data

This folder contains the observational datasets used in the UIF Quasar Cosmology Experiment. 
These datasets were derived from the Sloan Digital Sky Survey (SDSS) Stripe 82 Quasar catalog and 
were used to calibrate the cosmology-lite emulator (UIF Experiments I–V).

---

## Description

The following three CSV files included here are **processed derivatives** of the standard 
SDSS Stripe 82 quasar catalogs. They are NOT raw SDSS products.

They were constructed by:
1. Importing the master SDSS Stripe 82 QSO catalog (`master_QSO_S82.csv`)
2. Extracting calibrated photometry and variability parameters
3. Creating a clean cross-matched table of QSO positions and i-band photometry
4. Performing a 1-arcsec astrometric merge between RA/Dec and photometry tables

The processed files provided here are:

- `i_dat_raw.csv`  
  Extracted SDSS i-band photometry (calibrated magnitudes; Stripe 82)

- `master_raw.csv`  
  Cleaned, column-selected version of the master Stripe 82 QSO catalog

- `merged_1arcsec.csv`  
  Final astrometrically matched dataset (1-arcsec match), used for:
  - HC-plane maps
  - logistic fits
  - slope extraction
  - variability–mass–luminosity scaling

These files provide the observational anchor for UIF’s quasar coherence and scaling experiments.

---

## Contents

### Included (processed data)
- `i_dat_raw.csv`
- `master_raw.csv`
- `merged_1arcsec.csv`

### Not included (raw SDSS)
The following raw catalogs MUST be obtained directly from SDSS:

- Stripe 82 QSO catalog (`master_QSO_S82.csv`)
- SDSS DR7/DR9 spectroscopic QSO catalogs
- Raw Stripe 82 photometric time-series

These are excluded due to:
- licensing considerations  
- data volume  
- SDSS requirement that users download from official sources  

Links are provided below.

---

## How These Files Are Used

The processed datasets serve as the input to:
- Quasar HC-plane coherence analysis  
- Logistic modeling of coherence vs. luminosity/mass  
- Bootstrap uncertainty estimation  
- Scaling-law extraction (τ–M_bh, τ–iMag, σ–iMag)  
- Cosmology-lite emulator validation and operator calibration  

These data correspond to the observational side of UIF Experiments I–V.

---

## Obtain Raw Data (SDSS)

Raw SDSS datasets may be downloaded from:

- SDSS DR7 Data Release:  
  https://classic.sdss.org/dr7/

- Stripe 82 Database Access:  
  https://classic.sdss.org/dr7/products/value_added/stripe82/

- SDSS SkyServer (CASJobs):  
  https://skyserver.sdss.org/

---

## Citation

If you use these datasets, please cite SDSS as follows:

**Abazajian, K. et al. (SDSS Collaboration) 2009.**  
*The Seventh Data Release of the Sloan Digital Sky Survey.*  
ApJS 182, 543.  
https://doi.org/10.1088/0067-0049/182/2/543

Optional (specific to Stripe 82 quasar variability):
**MacLeod, C. et al. 2010.**  
*Modeling the Time Variability of SDSS Stripe 82 Quasars.*  
ApJ 721, 1014.

And cite UIF:

**Hiles, S.E.N. (2025).**  
*UIF Companion Experiments – Cosmology-Lite Emulator Dataset.*  
Zenodo. DOI: 10.5281/zenodo.[to-be-minted].

---
