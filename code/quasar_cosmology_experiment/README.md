# UIF Quasar Cosmology Experiment — Code

This directory contains all Python scripts used in the UIF Quasar Cosmology Experiment. 
These scripts reproduce every result and figure from the cosmology-lite operator sweeps, 
hysteresis tests, gamma-sweeps, and stability maps used in Paper IV and the UIF Companion Experiments.

Data for these experiments is located in:
/UIF/data/quasar_cosmology_experiment/

Outputs are produced in:
/UIF/output/quasar_cosmology_experiment/


Included Scripts
----------------

1. check_runs.py
   Utility for verifying that each emulator run produced a full diagnostic set 
   (summary JSON, kappa-map, spectra, tau/sigma statistics, etc.).

2. plot_gamma_2x2.py
   Creates the 2×2 gamma-sweep figure (mean coherence, kappa, pruning, dynamics).
   Matches Figure S2 in the UIF Companion.

3. plot_gamma_sweep_heatmap.py
   Generates a heatmap across gamma values showing coherence, kappa amplitude, pruning, and transitions.

4. plot_hysteresis.py
   Plots hysteresis curves for lambda_R and eta* sweeps.
   Used for operator stability analysis.

5. plot_threshold_heatmap.py
   Builds the “regime map” (fragile, stable, runaway) as a function of eta* and lambda_R.
   Matches Figure S3A.

6. run_gamma_sweep.py
   Batch driver for gamma-sweep experiments.
   Runs ut26_cosmo3d.py repeatedly across a gamma grid and saves outputs.

7. run_threshold_map.py
   Sweeps the operator plane (eta*, lambda_R) and generates threshold_map.csv and regime classifications.

8. ut26_cosmo3d.py
   Primary cosmology-lite emulator used for:
       - kappa-maps
       - kappa-spectra
       - coherence metrics
       - pruning histories
       - full summary diagnostics
   This is the core engine for the cosmology experiments.

9. ut26_cosmo3d_hysteresis.py
   Variant of the emulator for controlled hysteresis loops in eta* and lambda_R.


What These Scripts Reproduce
----------------------------

Running the scripts regenerates:
- kappa-maps inside/outside the Goldilocks band
- kappa power spectra
- operator-plane stability maps
- gamma-sweep diagnostics
- logistic surfaces and coherence curves
- hysteresis behaviour
- all cosmology-lite figures from Paper IV and the Companion


Requirements
------------

Python >= 3.9

Required packages:
numpy
matplotlib
scipy (optional for smoothing)

Install via:
pip install numpy matplotlib scipy


Reproducibility Notes
---------------------

- All scripts use deterministic seeds.
- Output directories include summary.json metadata for each run.
- Running the scripts reproduces all published results.


License
-------

Code: GPL-3.0  
Documentation: CC-BY-NC 4.0
