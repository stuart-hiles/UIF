# UIF EEG Subset — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

**Purpose**  
This folder documents the exact EEG subset and preprocessing used in the *UIF Companion Experiments* to compute informational metrics (ΔI, Γ, λᴿ, R∞, k) under the RSIPP/CHREM pipeline.

> ⚠️ *No raw EEG data are redistributed.*  
> Obtain EDF files directly from PhysioNet (see provenance below).

---

## 🧩 Source (Provenance)

- Dataset: **BCI2000 EEG Motor Movement/Imagery** (v1.0.0)  
  PhysioNet: <https://physionet.org/content/eegmmidb/1.0.0/>  
  DOI: **10.13026/C28G6P**  

- Primary citation:  
  Goldberger A.L. *et al.* (2000). *PhysioBank, PhysioToolkit, and PhysioNet.*  
  **Circulation**, 101(23): e215–e220.  
  doi:[10.1161/01.CIR.101.23.e215](https://doi.org/10.1161/01.CIR.101.23.e215)

---

## 📂 Folder Contents

| File | Description |
|------|--------------|
| **`subset_manifest.csv`** | Subject/run manifest (relative to PhysioNet paths). |
| **`metadata.json`** | Full machine-readable metadata (v1.0.2, Zenodo-ready). |
| **`metadata_*.json`** | Derived experiment descriptors — `kappa`, `H–C plane`, `surrogates`, `hmf`, `p(k)`, and `summary`. |
| **`manifest_README.txt`** | Human-readable data manifest linking this folder to `/output/eeg_coherence_experiment`. |
| **`SHA256SUMS.txt`** | Public checksums for derived artifacts only. (Raw EDF checksums retained privately.) |
| **`physionet_link.txt`** | DOI, URL, license, and access date for the original dataset. |

---

## 🧠 Subset Used in UIF

- **Subjects:** S001–S020 (baseline subset; scalable → S001–S109)  
- **Channels:** C3, C4, Cz (primary; full 64-ch montage optional)  
- **Sampling:** 160 Hz (1 s non-overlapping windows)  
- **Metrics:** Spectral entropy (H), Lempel–Ziv complexity (C), coherence (R), and derived ΔI/Γ/λᴿ operators.  

### Example `subset_manifest.csv` header
```csv
subject_id,edf_path,run_id,condition,start_sec,duration_sec,channels,samplerate_hz,notes
S001,/S001/S001R01.edf,R01,eyes_open,0,60,"C3;C4;Cz",160,baseline windowing
S001,/S001/S001R03.edf,R03,eyes_closed,0,60,"C3;C4;Cz",160,alpha baseline
S001,/S001/S001R07.edf,R07,task,0,60,"C3;C4;Cz",160,task windowing
