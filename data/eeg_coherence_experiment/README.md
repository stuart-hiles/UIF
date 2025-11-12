# UIF EEG Subset — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

**Purpose.** This folder documents the exact EEG subset and preprocessing used in the UIF Companion Experiments to compute informational metrics (ΔI, Γ, λᴿ, R∞, k) under the RSIPP/CHREM pipeline.  
**Note:** We *do not* redistribute raw EEG data. Please obtain EDF files directly from PhysioNet.

## Source (Provenance)
- Dataset: **BCI2000 EEG Motor Movement/Imagery** (v1.0.0)  
  PhysioNet: <https://physionet.org/content/eegmmidb/1.0.0/>  
  DOI: **10.13026/C28G6P**  
- Primary citation:  
  Goldberger AL et al. *PhysioBank, PhysioToolkit, and PhysioNet.* **Circulation** 2000;101(23):e215–e220. doi:10.1161/01.CIR.101.23.e215

## What’s in this folder
- **`subset_manifest.csv`** — exact files/subjects/runs used (relative to PhysioNet structure).  
- **`SHA256SUMS.txt`** — checksums for any **derived** artifacts we place here (never for PhysioNet raw files).  
- **`metadata.json`** — machine-readable metadata (Zenodo-ready).  
- **`physionet_link.txt`** — DOI, URL, license and access date.

## Subset used in UIF
We focused on eyes-open, eyes-closed, and simple task epochs:
- **Subjects:** S001–S020 (baseline); extendable to full S001–S109.
- **Channels:** C3, C4, Cz (primary), with full montage available for replication.
- **Sampling:** 160 Hz, window length 1 s (non-overlapping).
- **Metrics:** Spectral entropy (H), Lempel–Ziv complexity (C), coherence indices (R), ΔI/Γ/λᴿ estimates.

### Example `subset_manifest.csv` header
```csv
subject_id,edf_path,run_id,condition,start_sec,duration_sec,channels,samplerate_hz,notes
S001,/S001/S001R01.edf,R01,eyes_open,0,60,"C3;C4;Cz",160,baseline windowing
S001,/S001/S001R03.edf,R03,eyes_closed,0,60,"C3;C4;Cz",160,alpha baseline
S001,/S001/S001R07.edf,R07,task,0,60,"C3;C4;Cz",160,task windowing
