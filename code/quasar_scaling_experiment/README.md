# UIF Quasar Scaling Experiment — Code

This directory contains all Python scripts used for the UIF Quasar Scaling Experiment. 
These scripts reproduce the quasar mass–timescale relations, logistic scaling fits, 
bootstrap confidence intervals, and the CH-plane reconstructions used in Paper IV 
and the UIF Companion Experiments.

Data for these experiments is located in:
/UIF/data/quasar_scaling_experiment/

Outputs are produced in:
/UIF/output/quasar_scaling_experiment/


Included Scripts
----------------

1. make_Fig_5-1_quasar_CH_plane.py
   Generates the CH-plane reconstruction used in Figure 5.1 (Paper IV).
   Produces heatmaps showing tau, sigma, or coherence vs mass and redshift.
   Requires merged quasar dataset (master_raw.csv or merged_1arcsec.csv).

2. make_Fig_5-2_Logistic_Fit.py
   Produces logistic scaling fits for tau(MBH), tau(iMag), sigma(iMag).
   Outputs PDF/PNG figures and regression CSVs.

3. ut26_fit_bootstrap.py
   Runs bootstrap sampling to compute confidence intervals for:
       - tau–mass scaling slopes
       - tau–luminosity slopes
       - sigma–luminosity slopes
   Produces: ut26_model_fits_boot.csv, ut26_R_binned_boot.csv, and CI visualisations.

4. ut26_fit_coherence_models.py
   Computes the coherence-model fits and collapse-return parameter regressions used 
   to validate UIF scaling predictions.

5. ut26_probe5.py
   Experimental probe script used during development to validate fit behaviour, 
   often run against subsets of the quasar dataset.

6. ut26_quasar_full_run_v4.py
   The full end-to-end pipeline:
       - loads merged quasar dataset
       - cleans and bins data
       - computes tau, sigma statistics
       - performs scaling regressions
       - produces all final CSV outputs used in the UIF Companion
       - calls any required plotting scripts for reproduction


What These Scripts Reproduce
----------------------------

Running this directory's scripts regenerates:
- CH-plane diagnostics (Figure 5.1)
- logistic scaling curves (Figure 5.2)
- slopes vs redshift and magnitude
- tau(MBH) scaling splits: low-z, mid-z, high-z
- sigma vs iMag scaling
- bootstrap confidence intervals
- diagnostic CSVs used in the paper:
      quasar_raw_HC_all.csv
      ut26_model_fits_boot.csv
      ut26_R_binned_boot.csv
      ut26_logistic_bootstrap.json


Requirements
------------

Python >= 3.9

Required packages:
numpy
matplotlib
pandas
scipy

Install via:
pip install numpy matplotlib pandas scipy


Reproducibility Notes
---------------------

• All datasets are external and referenced via manifest in UIF/data/quasar_scaling_experiment  
• All fits use deterministic seeds where applicable  
• Running ut26_quasar_full_run_v4.py reproduces every output figure and CSV in the paper  


License
-------

Code: GPL-3.0  
Documentation: CC-BY-NC 4.0
