# 📄 UIF Papers — LaTeX Sources
This directory contains the LaTeX source files for the **Unifying Information Field (UIF)** scientific paper series.  
Each paper is stored in its own folder for version tracking, compilation, and DOI-based release management.

| Paper | Title | Filename | Description |
|-------|--------|---------|---------|
| I | **Core Theory** | `Paper_1_CoreTheory` |hfghf
| II | **Symmetry Principles** | `Paper_2_SymmetryPrinciples` |fhfh
| III | **Field and Lagrangian Formalism** | `Paper_3_FieldLagrangian` |hfgf
| IV | **Cosmology and Astrophysical Case Studies** | `Paper_4_Cosmology` |fgh
| V | **Energy and the Potential Field** | `Paper_5_Energy` |ghfg
| VI | **The Seven Pillars and Invariants** | `Paper_6_SevenPillars` |hgfgf
| VII | **Predictions and Experiments** | `Paper_7_PredictionsExperiments` |hfgfg
| — | **Companion Experiments** | `CompanionExperiments` |hgfhf

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
[**10.5281/zenodo.17434413**](https://doi.org/10.5281/zenodo.17434413)

---

### 🧾 License
- **Text and figures:** [Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)  
- **Code, data, and scripts:** [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

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
https://doi.org/10.5281/zenodo.17434413

---

### 🧠 Notes
This structure supports full reproducibility and Zenodo integration:
- Each folder is self-contained and version-locked.  
- The `main.tex` file acts as a shared master template.  
- Future releases (v1.1, v2.0, etc.) can update individual PDFs while preserving DOIs.  
- The `/output/` directory collects compiled PDFs for each tagged release.  
- Zenodo automatically snapshots tagged versions, ensuring DOI traceability.


