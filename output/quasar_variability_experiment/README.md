# UIF Quasar Variability Experiment — Output Directory
*(Experiment VII in the UIF Companion Paper)*

This directory contains all derived outputs from the  
**UIF Quasar Variability Experiment** (Experiment VII), which analyses  
**SDSS Stripe 82 multi-epoch quasar light curves** to recover the full  
UIF operator fingerprint  
(ΔIσ, Γ, λR, R∞, k)  
across low-z, mid-z, and high-z populations.

All outputs were generated using the scripts in:

/UIF/code/quasar_variability_experiment/

Only processed (derived) data are included here.  
No raw SDSS data are redistributed. For provenance, see:

/UIF/data/quasar_variability_experiment/README.md

---

## 1. Top-Level Contents

### 📊 Operator Extraction Tables

**quasar_variability_operators.csv**  
The main operator table for Experiment VII. Includes, for each redshift bin:

- ΔIσ (standardised variability richness)
- Γ (τ–MBH recursion slope)
- λR (high-R fraction)
- R∞ (95th percentile log σ; coherence-ceiling proxy)
- k (τ-spread; recharge proxy)

These values populate Table 8 in the Companion paper.

---

### 📄 HC-Plane Geometry (Figures S12)

- exp7_quasar_variability_HC_low-z.png
- exp7_quasar_variability_HC_mid-z.png
- exp7_quasar_variability_HC_high-z.png
- exp7_quasar_variability_HC_all.png

These reveal the structured, mid-entropy, high-complexity distribution  
distinct from phase-randomised surrogates.

---

### 📊 R-Histogram Distributions (Fig. S10)

- exp7_quasar_variability_R_hist_zbins.png

Population-level coherence distributions used to evaluate  
operator shifts with cosmic time.

---

### 📈 Operator Fingerprints (Figures S6–S7)

- exp7_quasar_variability_op_DeltaI.png
- exp7_quasar_variability_op_Gamma.png
- exp7_quasar_variability_op_lambdaR.png
- exp7_quasar_variability_op_Rinf.png
- exp7_quasar_variability_op_k.png

Combined versions:

- exp7_quasar_variability_operators_bars.png
- exp7_quasar_variability_operators_radar.png

These correspond to Figures S6 and S7 in the paper, and summarise  
the quasar operator manifold.

---

### 📈 Scaling-Relation Figures (Fig. S11)

- exp7_Fig_quasar_tau_vs_MBH.png
- exp7_Fig_quasar_tau_vs_Mi.png
- exp7_Fig_quasar_sigma_vs_Mi.png

---

### 📁 Summary / Derived Tables

- quasar_variability_tau_M_MBH_summary.csv
- quasar_variability_scalings.csv
- quasar_variability_scales.csv
- summary.json

---

### 🧪 Additional Derived Plots

Multiple HC and operator diagnostic plots included in this folder  
(e.g., HC_all, HC_low-z, HC_mid-z, HC_high-z variants).

---

## 2. How These Outputs Were Generated

Scripts used:

uif_quasar_variability.py  
uif_quasar_variability_hc.py  
uif_quasar_variability_operators.py  
uif_quasar_variability_operators_plots.py  
uif_quasar_variability_plots.py  
uif_quasar_variability_scaling.py  
uif_quasar_variability_scalings.py

Pipeline steps:

1. Import SDSS Stripe 82 multi-epoch light curves  
2. Construct entropy–complexity (H,C) planes  
3. Estimate UIF operators (ΔIσ, Γ, λR, R∞, k)  
4. Generate barplots & radar plots  
5. Generate HC geometry (S12)  
6. Generate coherence-distribution and scaling figures (S10–S11)

This completes the astrophysical validation of the UIF operator manifold.

---

## 3. Integrity

Checksum validation available via project-level Zenodo archive:

sha256sum <file>

---

## 4. Citation

Hiles, S.E.N. (2025).  
*UIF Companion Experiments — Quasar Variability Outputs.*  
Zenodo. DOI: 10.5281/zenodo.17434412

SDSS Stripe 82 variability catalogs:  
MacLeod et al. (2010, 2012), Ivezić et al. (2007–2010)

---

## 5. License

Processed outputs: **CC BY-NC 4.0**  
SDSS data follow SDSS data-use policy.
