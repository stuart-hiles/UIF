# UIF EEG Coherence Experiment — Output Archive

**Version:** v1.0.2  
**Linked papers:** [UIF I–VII Series](https://doi.org/10.5281/zenodo.17434413)  
**Primary companion:** [UIF Companion Experiments](https://doi.org/10.5281/zenodo.17478715)

---

## 🧩 Purpose

This folder contains the **derived outputs** from the UIF EEG coherence analyses performed under the RSIPP / CHREM pipeline.  
These data quantify informational coherence and recursion across eyes-open, eyes-closed, and task conditions, forming the empirical basis for UIF operator calibration:

> ΔI (informational difference), Γ (recursion rate), λᴿ (receive–return coupling), η*, R∞, and k (recharge rate).

All files here are **derived** from the *BCI2000 EEG Motor Movement / Imagery Dataset (v1.0.0)* hosted by **PhysioNet**  
[https://physionet.org/content/eegmmidb/1.0.0/](https://physionet.org/content/eegmmidb/1.0.0/)  
DOI: [10.13026/C28G6P](https://doi.org/10.13026/C28G6P)

Raw EEG signals are **not redistributed** in this repository.

---

## 🧠 Contents & Interpretation

| Category | Files | Description |
|-----------|-------|-------------|
| **Baseline reference** | `baseline/*` | Foundational calibration set used to derive operator estimates across EO/EC states. |
| **Operator calibration data** | `EEG_*_R.csv` | Numerical coherence outputs forming ΔI–Γ–λᴿ metrics. |
| **Surrogate tests** | `EEG_surrogates_HCR.csv` | Null-model coherence/entropy for statistical validation. |
| **Extended analyses** | `hmf*`, `pk*`, `kappa*` | Derived informational analogues of cosmological scaling (operator verification). |
| **Visual diagnostics** | `*.png` | Figures directly generated from CSV outputs. |
| **Metadata summaries** | `EEG_effects_EC_vs_EO.json`, `summary.json` | Machine-readable experiment summaries for Zenodo ingestion. |

---

## 🔒 Integrity & Provenance

- **Checksums:** All numeric and graphical outputs are listed in  
  [`SHA256SUMS.txt`](./SHA256SUMS.txt)  
  to ensure reproducibility across environments.  
  (Documentation and README files are *excluded* from checksum tracking.)

- **Pipeline scripts:**  
  Generated using `make_eeg_HC_analysis.ipynb` and  
  `make_eeg_HC_surrogates.ipynb` (see `/code/eeg/`).

- **Upstream dataset:**  
  PhysioNet BCI2000 Motor/Imagery EEG (v1.0.0) — DOI 10.13026/C28G6P  
  License: ODC-By 1.0  
  (Reused under fair academic research terms; raw EDFs accessed 2025-09.)

---

## 🔗 Related UIF Resources

| Component | DOI / Reference | Description |
|------------|----------------|-------------|
| **UIF I – Core Theory** | [10.5281/zenodo.17460040](https://doi.org/10.5281/zenodo.17460040) | Foundational information field framework. |
| **UIF IV – Cosmology & Astrophysical Case Studies** | [10.5281/zenodo.17475119](https://doi.org/10.5281/zenodo.17475119) | Cross-scale coherence analysis (cosmic–biological parallel). |
| **UIF V – Energy & Potential Field** | [10.5281/zenodo.17478131](https://doi.org/10.5281/zenodo.17478131) | Operator calibration and field energetics. |
| **UIF Companion Experiments** | [10.5281/zenodo.17478715](https://doi.org/10.5281/zenodo.17478715) | Methodological and experimental details (RSIPP / CHREM). |

---

## ⚖️ License

- **Derived Data & Visuals:** CC BY-NC 4.0  
- **Source EEG Dataset:** ODC-By 1.0 (PhysioNet)  
- **Code:** GPL-3.0 (see root `LICENSE`)

---

## 📜 Citation

> Hiles S. E. N. (2025). *UIF EEG Coherence Experiment — Output Archive (v1.0.2).*  
> Zenodo. [https://doi.org/10.5281/zenodo.17478715](https://doi.org/10.5281/zenodo.17478715)

---

**Contact:**  
Stuart E. N. Hiles · [GitHub](https://github.com/stuart-hiles/UIF) · [Zenodo](https://zenodo.org/records/17434413)
