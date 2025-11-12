UIF EEG Coherence Experiment — Data Manifest (v1.0.2)
------------------------------------------------------

This folder documents the exact data provenance and derived experiment
structure for the UIF EEG coherence analysis used in the Companion paper.

Source dataset:
    PhysioNet BCI2000 EEG Motor Movement/Imagery (v1.0.0)
    DOI: 10.13026/C28G6P
    https://physionet.org/content/eegmmidb/1.0.0/

Contents:
    subset_manifest.csv      → Index of EEG subjects/runs used in UIF analysis
    metadata.json            → Full dataset provenance and UIF operator context
    metadata_*.json          → Derived experiment stubs (κappa, H–C, surrogate, HMF, p(k), summary)
    SHA256SUMS.txt           → Checksums for derived artifacts (CSV/PNG/JSON)
    physionet_link.txt       → DOI and license information for the source data

Relationship to repository:
    /data/eeg_coherence_experiment/   — Provenance + metadata only
    /output/eeg_coherence_experiment/ — Derived UIF results (no raw EDF files)

All data herein are redistributed under CC-BY-NC 4.0.
Raw EEG must be obtained directly from PhysioNet.
