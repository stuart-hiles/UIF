# Quasar Variability Experiment — Data Folder  
### (Supports UIF Companion — Experiment VII)

This folder contains the processed datasets used in **Experiment VII — Quasar Variability and Informational Coherence**, as reported in the UIF Companion paper.  

The experiment tests whether real astrophysical time-series (SDSS Stripe 82 quasars) express the same informational operators  
\(\Delta I, \Gamma, \lambda_R, R_\infty, k\)  
found in the UIF collapse–return emulator and in the human EEG experiment.

Only **analysis-ready CSVs** are included here.  
Raw SDSS light curves are **not redistributed**.

---

## **Purpose**

These datasets support the full variability operator analysis:

- entropy–complexity (H–C) geometry  
- coherence index \(R\) distributions  
- operator recovery:  
  \(\Delta I_{\sigma}, \Gamma_{\tau-M_{\rm BH}}, \lambda_R, R_\infty, k\)  
- logistic ceiling and recharge modelling  
- redshift-split population operator tracking  
- variability-driven cross-domain comparison with EEG operators

This is **Experiment VII** in the UIF Companion.

---

## **Files Included**

### **1. quasar_variability_operators.csv**
Per-redshift-bin operator estimates derived from SDSS Stripe 82 variability metrics.

Columns:
- zbin  
- N (number of quasars)  
- ΔI_sigma_std  
- Γ_tau_MB_slope  
- λR_highR_fraction  
- Rinf_log10sigma_p95  
- k_tau_spread  

Used for:
- operator fingerprint plots  
- cross-domain operator comparisons  
- logistic-model parameter recovery

---

### **2. quasar_raw_HC_all.csv**  
Merged entropy & complexity dataset for all quasars after preprocessing.

Includes:
- spectral entropy \(H\)  
- Lempel–Ziv complexity \(C\)  
- coherence \(R = C/H_{\max}\)  
- τ, σ (DRW parameters)  
- redshift, magnitude  
- derived informational metrics  

Used in:
- Experiment VII H–C planes  
- coherence-distribution plots  
- surrogate analyses (optional)

---

### **3. UT26_quasar_scaling_slopes.csv**  
Slope and intercept fits for:
- τ–M_BH  
- τ–M_i  
- σ–M_i  

Used as supporting diagnostics for operator extraction  
especially Γ and ΔI_σ variability.

---

## **Provenance**

These processed datasets were derived from SDSS Stripe 82:

- **master_QSO_S82.dat**  
- **DB_QSO_S82.dat**  
- DRW parameter files:  
  `s82drw_*.dat`

*For further details please refer to provenance_notes.txt provided in this folder.*  

### **Preprocessing Steps**
1. Import DRW variability tables  
2. Merge with photometric & luminosity metadata  
3. Cross-match redshift, DRW, and photometry catalogs  
4. Quality filtering + median detrending of light curves  
5. Compute variability metrics: τ, σ, Δm, SF(Δt)  
6. Generate:  
   - entropy \(H\)  
   - complexity \(C\)  
   - coherence index \(R\)  
7. Bin by redshift: low, mid, high  
8. Export analysis-ready CSVs to this folder  

---

## **How This Differs From the Scaling Experiment**

- **Scaling** focuses on mass–timescale & luminosity–variability laws  
- **Variability** focuses on informational coherence operators and UIF dynamics  
- Both share a common Stripe 82 foundation  
- Variability uses **time-series-derived informational operators**, not just DRW scalings  

---

## **Required Citations**

### **UIF Companion Experiments Dataset**
Hiles, S.E.N. (2025). *UIF Companion Experiments*. Zenodo.  
DOI: https://doi.org/10.5281/zenodo.17434412

### **SDSS Stripe 82 Quasar Survey**
Cite SDSS and DRW parameter works:  
- Ivezić et al. (2007, 2008)  
- MacLeod et al. (2010, 2012)  
- Schneider et al. (2010)  

---

## **Related UIF Project Folders**

- **Code:**  
  `/UIF/code/quasar_variability_experiment/`

- **Outputs:**  
  `/UIF/output/quasar_variability_experiment/`

- **Related Experiments:**  
  `/UIF/code/quasar_scaling_experiment/`  
  `/UIF/code/quasar_cosmology_experiment/`

---

## Notes

- All files here are **processed**, never raw SDSS data.  
- Figures generated from these CSVs appear in the UIF Companion:  
  - H–C planes  
  - logistic fits  
  - scaling relations  
  - operator fingerprints  
- SHA256 checksums are maintained in:  
  `UIF/output/quasar_variability_experiment/SHA256SUMS.txt`
