# UIF Quasar Coherence Experiment — Derived Outputs (Stripe 82)

This folder contains all **derived outputs** used in the *UIF Companion Experiments* for the **Quasar Coherence Study**.
These results were produced by processing the merged SDSS Stripe 82 quasar dataset through the UIF coherence‑operator pipeline.

No raw SDSS data are redistributed here.  
For provenance and access details, see:  
`/data/quasar_coherence_experiment/README.md`.

---

## 1. Summary of Contents (this folder)

### Primary Operator Outputs
- **ut26_R_binned_boot.csv** — Binned bootstrap estimates of coherence metric *R* across luminosity/mass bins.
- **ut26_model_fits_boot.csv** — Logistic‑model fits used to estimate β (bias/elasticity), λᴿ (receive–return coupling), and R∞.
- **ut26_logistic_bootstrap.json** — Full bootstrap inference record for operator stability.
- **ut26_coherence_logistic_boot_CI.png** — Visualisation of logistic‑fit confidence intervals.

---

## 2. Supporting Files (Figures, Maps, Spectra)

- **Fig_EC_minus_EO_hist.png** — Histogram of coherence shift (EC−EO).
- **Fig_EC_vs_EO.png** — Scatter comparison of EC vs EO coherence metrics.
- **Fig_EEG_HC_plane.png** — H–C plane used for EEG vs quasar operator comparison.
- **Fig_pk.png** — Power spectrum P(k) derived from quasar coherence.
- **hmf.csv / hmf.png** — HMF‑style coherence distribution.
- **kappa_map.png** — 2‑D κ‑map.
- **kappa_ps.csv / kappa_ps.png** — κ power spectrum.
- **pk.csv** — Raw P(k) values.
- **summary.json / summary.png** — Summary of UIF operator estimates.
- **SHA256SUMS.txt** — SHA‑256 hashes for file‑integrity verification.

---

## 3. How These Outputs Were Generated

Pipeline used:  
`/code/quasar_coherence_experiment/`

### Dataset
- **SDSS Stripe 82 Southern Sample**
- Derived tables: `i_dat_raw.csv`, `master_raw.csv`, `merged_1arcsec.csv`

### Processing Steps
- Light‑curve cleaning & multi‑epoch matching
- Computation of entropy **H**, complexity **C**, coherence **R**
- Logistic and bootstrap modelling for operator estimation
- HC‑plane and κ‑map generation
- Power‑spectrum computation

### UIF Operators Generated
- **ΔI** — informational difference  
- **Γ** — recursion / temporal coherence  
- **β** — bias elasticity  
- **λᴿ** — receive–return coupling  
- **R∞** — coherence ceiling  
- **k** — recharge constant  

---

## 4. Checksums

Verify all files using:

```
sha256sum -c SHA256SUMS.txt
```

---

## 5. Citation

**UIF Companion Experiments — Quasar Coherence Study (Derived Outputs)**  
Hiles, S.E.N. (2025). Zenodo.  
DOI: *10.5281/zenodo.17478715*  
(or cite all versions via *10.5281/zenodo.17434412*)

### Underlying dataset:
SDSS Stripe 82 Quasar Light Curves  
MacLeod et al. (2010), ApJ 721:1014

---

## 6. License
- Derived outputs: **CC BY‑NC 4.0**  
- SDSS data: SDSS DR policy

