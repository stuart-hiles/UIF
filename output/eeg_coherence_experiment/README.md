# UIF EEG Output — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

This directory contains all **derived outputs** used in the *UIF Companion Experiments* for the EEG coherence analysis.
These files were produced by the **RSIPP/CHREM pipeline** using the PhysioNet **BCI2000 Motor Movement/Imagery** dataset (eegmmidb v1.0.0).

> Note: No raw EEG is redistributed here. All `.edf` recordings must be obtained directly from PhysioNet.
> See `/data/eeg_coherence_experiment/README.md` for provenance, licensing, and access details.

---

## 1. Top-Level Contents (Derived Outputs)
These files represent the **final processed outputs** analysed in the UIF Companion paper.

### Summary & Metric Files
- EEG_effects_EC_vs_EO.json — Condition-wise EC−EO differences; ΔI, Γ, R∞ estimates.
- EEG_recording_summary_R.csv — Coherence metric R per recording.
- EEG_state_summary_R.csv — State-level coherence summaries.
- EEG_subject_summary_R.csv — Subject-level coherence values.
- EEG_surrogates_HCR.csv — Surrogate-based entropy, complexity, and coherence metrics (H, C, R).
- EEG_windows_HCR.csv — Windowed H, C, R estimates.

---

## 2. Figures
- Fig_EC_minus_EO_hist.png — EC−EO histogram  
- Fig_EC_vs_EO.png — EC vs EO coherence  
- Fig_EEG_HC_plane.png — H–C plane  
- Fig_pk.png — Power spectrum P(k)  
- hmf.csv / hmf.png — HMF-style coherence distribution  
- kappa_map.png — κ map  
- kappa_ps.csv / kappa_ps.png — κ power spectrum  
- pk.csv — Power spectrum data  
- summary.json / summary.png — Operator summary  

---

## 3. Integrity File
- SHA256SUMS.txt — SHA-256 checksums for all outputs and for the `/baseline/` folder.

---

## 4. Baseline Subfolder
Contains the earlier **baseline run (v1.0.1)** of the EEG pipeline.

Includes:
- EEG_effects_EC_vs_EO.json
- EEG_recording_summary_R.csv
- EEG_state_summary_R.csv
- EEG_subject_summary_R.csv
- EEG_surrogates_HCR.csv
- EEG_windows_HCR.csv
- Figures (same as top-level)
- README.md (baseline notes)

Purpose: validate operator stability (ΔI, Γ, λᴿ, R∞, k).

---

## 5. How Outputs Were Generated
Pipeline: `/code/eeg_coherence_experiment/`

Dataset: PhysioNet BCI2000 Motor/Imagery  
Channels: C3, C4, Cz  
Sampling: 160 Hz  
Window: 1 second  

Metrics:
- H — spectral entropy  
- C — Lempel–Ziv complexity  
- R — coherence proxy  

Operator estimation:
ΔI, Γ, β, λᴿ, R∞, k

All figures produced automatically.

---

## 6. Checksums
`SHA256SUMS.txt` contains SHA-256 hashes for all files in this directory and the `/baseline/` directory.

---

## 7. Citation
Hiles, S.E.N. (2025).  
*UIF Companion Experiments — EEG Coherence Study (Derived Outputs).*  
Zenodo: https://doi.org/10.5281/zenodo.17478715

Dataset citation:  
Goldberger, A.L., et al. (2000).  
*PhysioBank, PhysioToolkit, and PhysioNet.*  
Circulation, 101(23): e215–e220.  
https://doi.org/10.1161/01.CIR.101.23.e215

---

## 8. License
- Derived outputs: CC BY-NC 4.0  
- PhysioNet data: PhysioNet license (must be downloaded from source)
