# UIF Quasar Scaling Experiment — Output Directory

This folder contains all processed outputs from the quasar variability–scaling
experiment described in the UIF Companion paper (Section 5). These outputs were
generated using the cleaned SDSS Stripe 82 dataset and UIF quasar–scaling
pipeline located in `/code/quasar_scaling_experiment/`.

All files here are *derived* data and figures — no raw SDSS data are
redistributed. See `/data/quasar_scaling_experiment/README.md` for provenance.

---

## 1. Top-Level Contents

### 📊 Scaling Analysis Tables

- **UT26_quasar_scaling_slopes.csv**  
  Best-fit slopes for the relationships:  
  - τ vs MBH  
  - τ vs i-band luminosity  
  - σ vs luminosity  
  separated into low-z, mid-z, and high-z bins.

  Columns include:  
  `relation, zbin, slope, n`  
  where `n` is number of quasars contributing to the fit.

---

### 📄 Figures / PDF Output

- **UT26_quasar_scaling_figures_clean.pdf**  
  Publication-ready figure set containing:  
  - τ–MBH scaling curves  
  - τ–iMag relations  
  - σ–iMag relations  
  - Redshift-stratified scaling comparisons  
  These correspond to Figure 5 in the UIF Companion paper.

---

### 📁 Processed Input Tables (for reproducibility)

These CSVs reproduce exactly the subset used for the scaling experiment:

- **i_dat_raw.csv**  
  Cleaned single-epoch photometric and variability parameters per quasar  
  (imported from DRW fits).

- **master_raw.csv**  
  Metadata table including redshift, absolute magnitude, black hole mass,
  bolometric luminosity (from Shen et al. 2008), and quality flags.

- **merged_1arcsec.csv**  
  Final merged table with one row per quasar after cross-matching, filtering,
  and removing duplicates closer than 1 arcsec.

These correspond to the cleaned dataset used to compute τ and σ scaling
relations in the UIF paper.

---

## 2. How These Outputs Were Generated

All results in this directory were produced by running:

- python ut26_fit_bootstrap.py
- python make_Fig_5-1_quasar_CH_plane.py
- python make_Fig_5-2_Logistic_Fit.py
- python ut26_quasar_full_run_v4.py

The pipeline performed:

- DRW parameter extraction (τ, σ²)  
- Merging of multi-epoch Stripe 82 photometry  
- Removal of outliers, low-quality fits, and blended sources  
- Redshift binning into low-z / mid-z / high-z  
- Linear regression in log–log space  
- Extraction of slopes and uncertainties  
- Generation of final publication-ready figures

This scaling analysis forms the empirical validation of UIF coherence–recursion
predictions at astrophysical scales.

---

## 3. Integrity

Checksums for these files will be included in the top-level UIF Zenodo archive.  
Use `sha256sum` or equivalent when validating downloaded copies.

---

## 4. Citation

If you use these outputs, please cite:

**Hiles, S.E.N. (2025).**  
*UIF Companion Experiments — Quasar Scaling Outputs.*  
Zenodo. DOI: 10.5281/zenodo.17478715  
(Or cite all UIF releases via DOI 10.5281/zenodo.17434412.)

And the SDSS Stripe 82 sources:

**Ivezić, Ž. et al. (2007–2010).**  
*SDSS Stripe 82 Variable Source Catalogs.*

And DRW parameter catalog:

**Shen, Y. et al. (2008).**  
(Black hole masses and bolometric luminosities — SDSS DR5 Quasar Catalog)

---

## 5. License

All processed outputs are released under **CC BY-NC 4.0**.  
Original SDSS data follow the SDSS data use policy.
