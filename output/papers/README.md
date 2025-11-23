# 📄 UIF Papers — LaTeX Sources and Outputs
This directory contains the LaTeX source files for the **Unifying Information Field (UIF)** scientific paper series.  
Each paper is stored in its own folder for version tracking, compilation, and DOI-based release management.

# 📄 UIF Papers — LaTeX Sources and Outputs

This directory contains the LaTeX source files for the **Unifying Information Field (UIF)** scientific paper series.  
Each paper is organised in its own folder for version tracking, compilation, and DOI-based release management.

---

## 📘 Table of Papers

| Paper | Title | LaTeX Filename | PDF | DOI |
|------|--------|----------------|------|------|
| I | **Core Theory** | `uif1_core.tex` | `UIF_Paper_1_CoreTheory.pdf` | https://doi.org/10.5281/zenodo.17460040 |
| II | **Symmetry Principles** | `uif2_core.tex` | `UIF_Paper_2_SymmetryPrinciples.pdf` | https://doi.org/10.5281/zenodo.17468871 |
| III | **Field & Lagrangian Formalism** | `uif3_field.tex` | `UIF_Paper_3_Lagrangian.pdf` | https://doi.org/10.5281/zenodo.17471559 |
| IV | **Cosmology & Astrophysical Case Studies** | `uif4_cosmology.tex` | `Paper_4_Cosmology.pdf` | https://doi.org/10.5281/zenodo.17475119 |
| V | **Energy & the Potential Field** | `uif5_energy.tex` | `Paper_5_Energy.pdf` | https://doi.org/10.5281/zenodo.17478131 |
| VI | **The Seven Pillars & Invariants** | `uif6_pillars.tex` | `Paper_6_SevenPillars.pdf` | https://doi.org/10.5281/zenodo.17478484 |
| VII | **Predictions & Experiments** *(forthcoming)* | `uif7_predictions.tex` | `Paper_7_PredictionsExperiments.pdf` | *TBC* |
| — | **Companion Experiments** | `companion_uif.tex` | `CompanionExperiments.pdf` | https://doi.org/10.5281/zenodo.17478715 |

---

## 📄 **Paper Descriptions**

### **Paper I — Core Theory**
Foundational operator grammar (ΔI, Γ, β, λR) and the collapse–return dynamics defining the informational substrate of UIF.

### **Paper II — Symmetry Principles**
Establishes the conservation and invariance structure of UIF and introduces the informational Noether correspondence.

### **Paper III — Field & Lagrangian Formalism**
Continuous variational formulation, Euler–Lagrange derivations, receive–return terms, and the canonical UIF field equations.

### **Paper IV — Cosmology & Astrophysical Case Studies**
Applies UIF to cosmology: M87 coherence, CMB phase-residuals, quasar variability, dark-sector coupling, and receive–return effects.

### **Paper V — Energy & the Potential Field**
Defines the operator-level informational–energetic mapping, potential functions, and the conversion coefficient α linking energy and ΔI.

### **Paper VI — The Seven Pillars & Invariants**
Unifies all operators into an invariant architecture across physical, biological, cognitive, and artificial systems.

### **Paper VII — Predictions & Experiments** *(forthcoming)*
Cross-domain validation framework: coherence decay constants, stochastic resonance, collapse thresholds, and proto-agency signatures.

### **Companion Experiments**
Empirical validation datasets, symbolic notebooks, emulator sweeps, quasar/EEG operator calibration, and reproducibility scripts.

---

Each folder includes:
- LaTeX source (`UIF_Paper_X_<Title>.tex`)
- Local bibliography file (`paperX.bib`)
- Output PDF (`UIF_Paper_X_<Title>.pdf`)
- Local README with DOI, version, and metadata

All papers compile independently using the shared `main.tex` template and `/bib/` reference directory.  
Compiled PDFs are exported to `/output/` for release packaging.

---

### ⚠️ Preprint Status
All UIF papers are **pre-release research manuscripts** shared for open scientific communication.  
They have **not yet undergone peer review** and should be cited as *preprints* via the Zenodo DOI:  
[**10.5281/zenodo.17434412**](https://doi.org/10.5281/zenodo.17434412)

---

### 🧾 License
- **Text and figures:** [Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)  
- **Code, data, and scripts:** [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
Copyright (C) 2005 Stuart E. N. Hiles
---

### ⚙️ Build Instructions
To compile any paper locally or in Overleaf:

```
pdflatex main.tex
```

Then edit the `\input{papers/...}` line in `main.tex` to select which paper to build.  
For example:

```
\input{papers/Paper_1_CoreTheory/UIF_Paper_1_CoreTheory}
```
---

📚 Citation
Hiles, S. E. N. (2025). UIF Series — Initial Publication Set (Papers I–VII and Companion).
Version v1.0 (October 2025). Zenodo.
https://doi.org/10.5281/zenodo.17434412

---

### 🧠 Notes
This structure supports full reproducibility and Zenodo integration:
- Each folder is self-contained and version-locked.  
- The `main.tex` file acts as a shared master template.  
- Future releases (v1.1, v2.0, etc.) can update individual PDFs while preserving DOIs.  
- The `/output/` directory collects compiled PDFs for each tagged release.  
- Zenodo automatically snapshots tagged versions, ensuring DOI traceability.



