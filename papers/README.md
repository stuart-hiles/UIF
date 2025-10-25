# 📄 UIF Papers — LaTeX Sources

This directory contains the LaTeX source files for the **Unifying Information Field (UIF)** paper series:

1. `uif1_core.tex` — *Paper I: Core Theory*  
2. `uif2_symmetry.tex` — *Paper II: Symmetry Principles*  
3. `uif3_field.tex` — *Paper III: Field and Lagrangian Formalism*  
4. `uif4_cosmology.tex` — *Paper IV: Cosmology and Astrophysical Case Studies*  
5. `uif5_energy.tex` — *Paper V: Energy and the Potential Field*  
6. `uif6_pillars.tex` — *Paper VI: The Seven Pillars and Invariants*  
7. `uif7_experiments.tex` — *Paper VII: Predictions and Experiments*

Each paper compiles independently using the shared `main.tex` template and `bib/` references.  
Output PDFs are stored in `/output/` for release builds.

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
Compile any paper locally or via Overleaf:

```bash
pdflatex main.tex

Then select which paper to compile by toggling the \input{papers/...} line in main.tex.

### 📚 Citation
Hiles, S. E. N. (2025). *UIF Series — Initial Publication Set (Papers I–VII and Companion)*  
(Version v1.0) [Computer software]. Zenodo.  
[https://doi.org/10.5281/zenodo.17434413](https://doi.org/10.5281/zenodo.17434413)
