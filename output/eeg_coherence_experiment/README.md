UIF EEG Output — PhysioNet BCI2000 Motor/Imagery (eegmmidb v1.0.0)

This folder contains all derived outputs used in the UIF Companion Experiments for the EEG coherence study. These files were produced by the RSIPP/CHREM processing pipeline from the PhysioNet BCI2000 EEG Motor Movement/Imagery (eegmmidb v1.0.0) dataset.

Important: No raw EEG is redistributed here. All .edf recordings must be obtained directly from PhysioNet. See /data/eeg_coherence_experiment/README.md for details and provenance.

1. Top-Level Contents (this folder)

These files are the main outputs used in the UIF Companion paper.

EEG_effects_EC_vs_EO.json
– JSON file summarising condition-wise effects (eyes-closed vs eyes-open) in terms of ΔI, Γ and R∞.

EEG_recording_summary_R.csv
– Per-recording coherence metric R for all selected subjects and runs.

EEG_state_summary_R.csv
– Per-state (e.g. eyes-open, eyes-closed, task) summary statistics of R.

EEG_subject_summary_R.csv
– Subject-level aggregation of coherence metrics across recordings.

EEG_surrogates_HCR.csv
– Surrogate-based entropy/complexity/coherence metrics (H, C, R) for baseline and perturbed data.

EEG_windows_HCR.csv
– Windowed (1-second) H, C, R values used to estimate ΔI and Γ.

Fig_EC_minus_EO_hist.png
– Histogram of R(Eyes-Closed) − R(Eyes-Open), showing the shift in coherence.

Fig_EC_vs_EO.png
– Scatter plot of eyes-closed vs eyes-open coherence values.

Fig_EEG_HC_plane.png
– H–C plane with coherence overlaid (UIF operator visualisation).

Fig_pk.png
– Power spectrum P(k) for EEG-derived coherence (analogue to cosmological P(k)).

hmf.csv / hmf.png
– “Halo mass function” style aggregation of coherence/complexity statistics (UIF cross-domain check).

kappa_ps.csv / kappa_ps.png
– Power spectrum of the EEG-based κ field (coherence) and corresponding plot.

kappa_map.png
– 2D κ-map visualisation of EEG coherence structure.

pk.csv
– CSV representation of the P(k) spectrum (frequency vs power).

summary.json
– Machine-readable summary of key UIF operator estimates (ΔI, Γ, β, λᴿ, R∞, k) and global metrics.

summary.png
– Visual overview of the main EEG coherence and operator results (used in the Companion paper).

SHA256SUMS.txt
– SHA-256 checksums for all derived files in this folder and its baseline/ subdirectory (integrity check).

2. baseline/ Subfolder

/baseline/ contains the baseline (v1.0.1) outputs used as a reference in the Companion paper. They are the same types of metrics and figures, but generated from the earlier baseline run of the RSIPP/CHREM pipeline.

Contents include:

EEG_effects_EC_vs_EO.json

EEG_recording_summary_R.csv

EEG_state_summary_R.csv

EEG_subject_summary_R.csv

EEG_surrogates_HCR.csv

EEG_windows_HCR.csv

Fig_EC_minus_EO_hist.png

Fig_EC_vs_EO.png

Fig_EEG_HC_plane.png

README.md describing that baseline snapshot

These files are used to cross-check stability of the operator estimates (ΔI, Γ, λᴿ, R∞, k) across independent runs.

3. How These Outputs Were Generated

All outputs in this folder were produced by running the RSIPP/CHREM EEG pipeline (see /code/eeg_coherence_experiment/ in this repository) with the following key steps:

Data source:

PhysioNet BCI2000 EEG Motor Movement/Imagery Dataset (eegmmidb v1.0.0).

Selected subjects: S001–S0XX (as documented in subset_manifest.csv under /data/eeg_coherence_experiment/).

Preprocessing:

Channels: C3, C4, Cz.

Sampling rate: 160 Hz.

1-s non-overlapping windows.

Standard EEG pre-processing (re-referencing, bandpass filtering as described in the Companion paper).

Metric computation per window:

H — spectral entropy.

C — Lempel–Ziv complexity (sequence-based complexity).

R — coherence‐like measure (UIF coherence operator proxy).

UIF operator estimation:

ΔI — informational difference per window/histogram (from H and R).

Γ — recursion / temporal coherence from window-to-window dynamics.

β — bias / elasticity from softmax fits to state-dependent differences.

λᴿ — receive–return coupling, estimated from surrogate analyses and echo behaviour.

R∞ — coherence ceiling from logistic fits to R(t).

k — recharge / recovery constant from hysteresis / return-to-baseline fits.

Plot generation:

All Fig_*.png figures and CSVs (pk.csv, hmf.csv, kappa_ps.csv) were generated directly from these metrics and saved here.

4. Checksums and Integrity

The file SHA256SUMS.txt contains SHA-256 hashes for all files in this folder and the baseline/ subfolder.
Use standard tools (for example sha256sum) to verify integrity after download.

5. Citation and Provenance

If you use these outputs, please cite:

Hiles, S. E. N. (2025).
UIF Companion Experiments — EEG Coherence Study (Derived Outputs).
In: The Unifying Information Field (UIF) — Companion Experiments.
Zenodo. DOI: 10.5281/zenodo.17478715 (and series DOI 10.5281/zenodo.17434412).

And the original EEG dataset:

Goldberger, A. L., et al. (2000).
PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.
Circulation, 101(23), e215–e220.
DOI: 10.1161/01.CIR.101.23.e215.

6. License

Derived EEG outputs in this folder are released under the Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0) license.

The original PhysioNet data are subject to their own license terms; please consult the PhysioNet website for details.
