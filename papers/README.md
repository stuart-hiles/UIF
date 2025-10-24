# 📘 UIF Papers (LaTeX Sources)

This directory contains the LaTeX sources for the **Unifying Information Field (UIF)** paper series:

1. `uif1_core.tex` — *Paper I: Core Theory*  
2. `uif2_symmetry.tex` — *Paper II: Symmetry Principles*  
3. `uif3_field.tex` — *Paper III: Field and Lagrangian Formalism*  
4. `uif4_cosmology.tex` — *Paper IV: Cosmology and Astrophysical Case Studies*  
5. `uif5_energy.tex` — *Paper V: Energy and the Potential Field*  
6. `uif6_pillars.tex` — *Paper VI: The Seven Pillars and Invariants*  
7. `uif7_experiments.tex` — *Paper VII: Predictions and Experiments*

Each paper can be compiled independently using the shared `main.tex` template and `bib/` references.  
Output PDFs are stored separately for release builds.

**Compile instructions:**
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
