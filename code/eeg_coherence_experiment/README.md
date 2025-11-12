# 🧠 UIF Code Integration — EEG & Cosmology Experiments

This document outlines the complete structure and upload plan for the **UIF Companion Experiments** repository — integrating both the **EEG coherence experiments** and the **Cosmology-Lite (UT26) emulator** pipelines.  
It provides the directory layout, code organisation, and README templates for each submodule.

---

## 📁 Recommended Repository Layout

```
/code
  /eeg
    ut26_eeg_pipeline.py
    ut26_eeg_p.py
    eeg_subject_level_summary.py
    plot_ec_vs_eo.py
    README.md
    environment.yml        # or requirements.txt
  /cosmo
    ut26_cosmo3d.py
    plot_pk_only.py
    plot_ut26_cosmo_outputs.py
    README.md
    environment.yml        # or requirements.txt
/data
  /eeg_coherence_experiment
    subset_manifest.csv
    metadata.json
    physionet_link.txt
    manifest_README.txt
/output
  /eeg_coherence_experiment
    EEG_recording_summary_R.csv
    EEG_subject_summary_R.csv
    EEG_state_summary_R.csv
    EEG_windows_HCR.csv
    EEG_surrogates_HCR.csv
    EEG_effects_EC_vs_EO.json
    baseline/
      (baseline metrics + plots)
    SHA256SUMS_auto.py
    SHA256SUMS.txt
  /cosmo_baseline
    pk.csv
    kappa_ps.csv
    hmf.csv
    summary.json
    figures/
```

... (content truncated for brevity; full text continues as before)
