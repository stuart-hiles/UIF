# UIF Cosmology-Lite Emulator — Code (cosmology_lite_experiment)

This folder contains the Python code for the Informational Difference Calibration experiment (UIF Companion Experiments Paper - Experiment 1) which utilised the Cosmology-Lite synthetic 3-D lattice universe emulator used for operator exploration and validation (Experiments I–V). It generates the synthetic collapse–return fields, operator sweeps, and diagnostic figures that appear in the Companion and in **UIF Paper IV**.

All scripts assume the standard UIF repo layout:

- data in `UIF/data/informational_difference_experiment/`
- outputs in `UIF/output/informational_difference_experiment/`

(You can change the base paths inside the scripts if your layout differs.)

---

## Environment

- Python ≥ 3.9
- NumPy
- SciPy
- Matplotlib

Install with e.g.

```bash
pip install numpy scipy matplotlib

---

###Core Simluator
Main 3-D UIF cosmology-lite emulator.
Evolves a coherence field s(x,t) on a lattice N³ for T timesteps using the UIF operators (ΔI, Γ, β, λᴿ, η*, R∞, k).
Produces per-run diagnostics in the output folder:

- summary.json — parameters and final statistics
- summary.png — quick visual summary
- pk.csv / pk.png — matter power spectrum P(k)
- kappa_ps.csv / kappa_ps.png — κ power spectrum
- hmf.csv / hmf.png — toy halo mass function
- kappa_map.png — κ projection

ut26_cosmo3d_hysteresis.py
Variant of the emulator with a two-phase drive schedule (high-amplitude followed by low-amplitude) used in the hysteresis / memory experiment (Experiment IV).

###Batch runners (experiment drivers)
These scripts orchestrate grids of runs and populate UIF/output/cosmology_lite_experiment/ with the individual run folders.
- run_gamma_sweep.py
Runs a sweep over drive amplitude and frequency (γ), classifying each run as fragile, stable-ceiling, or runaway.
Supports Experiment II — γ-sweep and symmetry thresholds.
- run_threshold_map.py
Runs a grid over collapse threshold η* and retention λᴿ
to map the “Goldilocks” stability band between fragile and runaway regimes.
- Supports Experiment III — Goldilocks stability map.
check_runs.py
Utility that scans the output directory to ensure that all expected runs completed and that the key output files for each run are present.

Each runner has a small configuration block near the top (number of steps, lattice size, parameter grid, base output path). Adjust these if you want to change resolution or directory layout.

####Plot / figure scripts
These scripts consume the consolidated CSV/JSON outputs created by the runners and produce the publication-ready figures.
- plot_gamma_2x2.py
Builds the 2×2 baseline / γ-sweep diagnostic panel (mean coherence vs time, cumulative pruning, P(k), κ projection).
- plot_gamma_sweep_heatmap.py
Produces the γ-sweep heatmaps: pruning activity, final mean coherence, collapse flags, etc.
- plot_threshold_heatmap.py
Produces the η*–λᴿ “Goldilocks” map showing fragile, stable, and runaway regions in operator space.
- plot_hysteresis.py
Uses the hysteresis run outputs (from ut26_cosmo3d_hysteresis.py) to plot:
drive amplitude vs time, coherence response ⟨s⟩, and the hysteresis loop ⟨s⟩ vs amplitude.

Note: The exact filenames for the figures (e.g. Fig_S1_baseline.png, Fig_S2_gamma_sweep.png, Fig_S3_goldilocks.png, Fig_S4_hysteresis.png) are set inside the scripts to match the Companion / Paper IV conventions.

## Workflow

1. Baseline  
   python ut26_cosmo3d.py

2. γ‑sweep  
   python run_gamma_sweep.py  
   python plot_gamma_2x2.py  
   python plot_gamma_sweep_heatmap.py

3. Goldilocks map  
   python run_threshold_map.py  
   python plot_threshold_heatmap.py

4. Hysteresis  
   python ut26_cosmo3d_hysteresis.py  
   python plot_hysteresis.py

5. Integrity check  
   python check_runs.py

## Reproducibility

Matches parameters and outputs in:  
- UIF Companion Experiments — Empirical Validation  
- UIF Paper IV — Cosmology & Astrophysical Case Studies  
Re-running with the same settings reproduces all figures and CSVs.

