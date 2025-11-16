# UIF EEG Subset — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

## Purpose
This folder documents the exact EEG subset and preprocessing used in the UIF Companion
Experiments to compute informational metrics (ΔI, Γ, β, λᴿ, η*, R∞, k) under the RSIPP/CHREM
pipeline.

- **No raw EDF data are redistributed.**
- EDF files must be downloaded directly from PhysioNet.

## Source (Provenance)
Dataset: **BCI2000 EEG Motor Movement/Imagery** (v1.0.0)  
PhysioNet: https://physionet.org/content/eegmmidb/1.0.0/  
DOI: 10.13026/C28G6P

Primary citation:  
Goldberger AL et al. (2000). *PhysioBank, PhysioToolkit, and PhysioNet.*  
Circulation 101(23): e215–e220.  
doi:10.1161/01.CIR.101.23.e215

---

## Folder Contents

| File | Description |
|------|-------------|
| **subset_manifest.csv** | Mapping of subjects/runs → EDF filenames used in UIF |
| **physionet_link.txt** | DOI + source URL + access date |
| **metadata.json** | Top-level subset metadata |
| **metadata_KF_*.json** | Kalman‑filter summaries |
| **metadata_HC_plane.json** | EEG entropy–complexity plane metadata |
| **metadata_kappa.json** | kappa / spectral summaries |
| **metadata_summary.json** | Aggregated subject-level summary |
| **metadata_summary_jobs.json** | Batch-job provenance |
| **subset_README.txt** | Preparation notes |

These files complement the processed outputs stored under:  
`/UIF/output/eeg_coherence_experiment/`

---

## UIF Subset Definition
- **Subjects:** S001–S050 (baseline subset; extensible to S001–S109)  
- **Channels:** C3, C4, Cz  
- **Conditions:** eyes_open, eyes_closed, task  
- **Sampling:** 160 Hz, non‑overlapping 1‑second windows  
- **Metrics computed:**  
  - Spectral entropy (H)  
  - Lempel–Ziv complexity (C)  
  - Coherence indices (R)  
  - ΔI, Γ, λᴿ, η*, k (UIF operators)

Example row:
```
subject,run,state,rec,R
S001,R01,eyes_open,S001R01,0.8111191485
```

---

## Reproducibility
To reproduce this subset:
1. Download EDF files from PhysioNet.
2. Use subset_manifest.csv to select the correct runs.
3. Run `ut26_eeg_pipeline.py` in the UIF code folder.

---

## Citation
Hiles, S.E.N. (2025). *UIF Companion Experiments — EEG Coherence Dataset.*  
Goldberger, A.L., et al. (2000). *PhysioBank, PhysioToolkit, and PhysioNet.*

