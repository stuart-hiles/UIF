# UIF EEG Output — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

This folder contains all derived outputs used in the UIF Companion Experiments for the EEG coherence study.
These files were produced by the RSIPP/CHREM pipeline using the PhysioNet BCI2000 EEG Motor Movement/Imagery dataset (eegmmidb v1.0.0).

Important: No raw EEG is redistributed here. All .edf recordings must be obtained directly from PhysioNet.
See /data/eeg_coherence_experiment/README.md for provenance and data-access details.

1. Top-Level Contents (this folder)

These files represent the final processed outputs analysed in the UIF Companion paper.

## Summary and metrics files

- EEG_effects_EC_vs_EO.json
Condition-wise differences (eyes-closed minus eyes-open), including ΔI, Γ and R∞ estimates.

- EEG_recording_summary_R.csv
Coherence metric 
𝑅
R per recording.

- EEG_state_summary_R.csv
Summary of 
𝑅
R by state (eyes-open, eyes-closed, task).

- EEG_subject_summary_R.csv
Subject-level aggregation of coherence values.

- EEG_surrogates_HCR.csv
Surrogate-based entropy/complexity/coherence metrics (H, C, R).

- EEG_windows_HCR.csv
1-second windows of H, C, R used to estimate ΔI and Γ.

## Contents

### 🔶 **Figures**

- Fig_EC_minus_EO_hist.png – Histogram of coherence differences EC−EO.

- Fig_EC_vs_EO.png – Scatter plot of EC vs EO coherence.

- Fig_EEG_HC_plane.png – H–C plane visualisation with EEG coherence.

- Fig_pk.png – Power spectrum 
𝑃
(
𝑘
)
P(k) of EEG-derived coherence.

Additional CSV/PNG outputs

hmf.csv / hmf.png – UIF-style HMF coherence distribution.

kappa_map.png – 2D coherence (κ) map.

kappa_ps.csv / kappa_ps.png – κ power spectrum.

pk.csv – Power spectrum data for 
𝑃
(
𝑘
)
P(k).

summary.json / summary.png – High-level summary of UIF operator estimates.

Integrity file

SHA256SUMS.txt
Checksums for all files in this directory and in the baseline/ folder.

2. Baseline Subfolder

/baseline/ contains the earlier (“v1.0.1”) baseline run of the same EEG processing pipeline.

Includes:

EEG_effects_EC_vs_EO.json

EEG_recording_summary_R.csv

EEG_state_summary_R.csv

EEG_subject_summary_R.csv

EEG_surrogates_HCR.csv

EEG_windows_HCR.csv

Fig_EC_minus_EO_hist.png

Fig_EC_vs_EO.png

Fig_EEG_HC_plane.png

README.md (baseline description)

This baseline snapshot is used to validate stability of operator estimation (ΔI, Γ, λᴿ, R∞, k).

3. How These Outputs Were Generated

All files in this folder were produced by running the UIF EEG pipeline (/code/eeg_coherence_experiment/) with:

Dataset: PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

Channels: C3, C4, Cz

Sampling rate: 160 Hz

Window size: 1 second (non-overlapping)

Metrics per window:

H — spectral entropy

C — Lempel–Ziv complexity

R — coherence proxy (UIF coherence operator analogue)

UIF operator estimation:

ΔI – informational difference

Γ – recursion rate / temporal coherence

β – bias/elasticity from softmax fits

λᴿ – receive–return coupling

R∞ – coherence ceiling

k – recharge / recovery constant

All figures (Fig_*.png, hmf.png, kappa_map.png, etc.) were generated directly from these metrics.

4. Checksums

SHA256SUMS.txt provides SHA-256 hashes for all files in this folder and the baseline folder.
Use sha256sum or an equivalent utility to verify file integrity.

5. Citation

If you use these outputs, please cite:

Hiles, S.E.N. (2025).
UIF Companion Experiments — EEG Coherence Study (Derived Outputs).
Zenodo. DOI: 10.5281/zenodo.17478715
(Or cite all versions via series DOI 10.5281/zenodo.17434412.)

And the dataset:

Goldberger, A. L., et al. (2000).
PhysioBank, PhysioToolkit, and PhysioNet.
Circulation, 101(23): e215–e220.
https://doi.org/10.1161/01.CIR.101.23.e215

6. License

All derived EEG outputs are released under CC BY-NC 4.0.
Original PhysioNet data are governed by the PhysioNet license.
