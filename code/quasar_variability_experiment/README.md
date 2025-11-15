UIF Quasar Variability Experiment — Code

Status
------
This directory is currently reserved for future expansion of the UIF quasar variability 
analysis pipeline. No active Python scripts are included in this version of the UIF Series.

Future Work
-----------
The intended purpose of this module is to support variability-driven analyses of quasar 
light curves, including:

 - structure function estimation
 - power spectral density (PSD) fitting
 - time-delay and reverberation-style coherence metrics
 - collapse–return variability signatures across redshift and mass
 - ΔI-driven variability complexion analysis (UIF operator diagnostics)

These will extend the foundations established in the existing scaling and coherence 
experiments.

Where to Find the Current Implementation
----------------------------------------
All quasar-related UIF analyses developed to date are implemented in two active modules:

1. quasar_scaling_experiment
   - logistic fits
   - CH-plane reconstructions
   - mass–timescale and luminosity–sigma scaling relations
   - bootstrap confidence intervals

2. quasar_coherence_experiment
   - coherence models
   - collapse–return fits
   - model comparison and inference

Reproducibility
---------------
Because no executable scripts are included yet, this module does not currently generate 
outputs. When the variability-analysis system is introduced, this directory will include:

 - preprocessing pipelines for multi-epoch quasar light-curves
 - PSD and structure-function estimators
 - UIF operator-based variability diagnostics
 - documentation and required manifests

These components will follow the established UIF Series layout standard used 
throughout /UIF/code/.

License
-------
Code (when added): GPL-3.0  
Documentation: CC-BY-NC 4.0
