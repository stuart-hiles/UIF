UIF EEG Coherence Experiment — Code
===================================

This folder contains the Python code used to generate the EEG results in the
UIF Companion Experiments (Empirical Validation of Papers I–IV).

The scripts here implement the RSIPP/CHREM-style pipeline that:
- reads EEG recordings from the PhysioNet BCI2000 motor/imagery dataset,
- extracts 1-second windows,
- computes informational metrics (H, C, R),
- produces subject/recording/state summaries,
- generates the figures used in the UIF Companion (EC vs EO, H–C plane, etc.).

For DATA and OUTPUTS, see:
- data/eeg_coherence_subset/        (manifests + metadata)
- output/eeg_coherence_experiment/  (derived CSVs, figures, SHA256SUMS.txt)

This folder is code-only.


------------------------------------------------------------
Repository Layout (relevant paths)
------------------------------------------------------------

/code/
  eeg_coherence_experiment/
    ut26_eeg_pipeline.py
    ut26_eeg_p.py
    eeg_subject_level_summary.py
    plot_ec_vs_eo.py
    README.md

/data/
  eeg_coherence_subset/
    subset_manifest.csv
    metadata.json
    physionet_link.txt

/output/
  eeg_coherence_experiment/
    baseline/
      EEG_recording_summary_R.csv
      EEG_state_summary_R.csv
      EEG_subject_summary_R.csv
      EEG_surrogates_HCR.csv
      EEG_windows_HCR.csv
      Fig_EC_vs_EO.png
      Fig_EC_minus_EO_hist.png
      Fig_EEG_HC_plane.png
      EEG_effects_EC_vs_EO.json
      README.md
    hmf.csv
    kappa_ps.csv
    pk.csv
    (plots .png)
    SHA256SUMS.txt
    README.md


------------------------------------------------------------
Script Overview
------------------------------------------------------------

ut26_eeg_pipeline.py
    Main processing pipeline. Loads EDFs from the subset manifest,
    extracts windows, computes H/C/R, writes window-level outputs.

ut26_eeg_p.py
    Helper functions for entropy, Lempel-Ziv complexity, coherence,
    surrogate construction. Imported by pipeline.

eeg_subject_level_summary.py
    Aggregates window-level data into recording-, state-, and
    subject-level summaries.

plot_ec_vs_eo.py
    Generates EC vs EO plots, histogram, and H–C plane visualisation.


------------------------------------------------------------
Dependencies
------------------------------------------------------------

Python >= 3.9
numpy
scipy
pandas
matplotlib
seaborn
(optional) mne for EDF loading


------------------------------------------------------------
Running the Pipeline
------------------------------------------------------------

python ut26_eeg_pipeline.py
python eeg_subject_level_summary.py
python plot_ec_vs_eo.py

Outputs will appear under:
output/eeg_coherence_experiment/


------------------------------------------------------------
Reproducibility
------------------------------------------------------------

Input provenance:
    data/eeg_coherence_subset/subset_manifest.csv
    data/eeg_coherence_subset/metadata.json

Output integrity:
    output/eeg_coherence_experiment/SHA256SUMS.txt


------------------------------------------------------------
UIF Context
------------------------------------------------------------

EEG-derived H/C/R metrics provide biological-scale validation of UIF operator
behaviour across Papers I–IV, confirming:
- lawful ΔI → Γ relationships,
- coherence ceiling R∞ behaviour,
- return-rate k under alternating states,
- alignment with the quasar-scale informational dynamics.
