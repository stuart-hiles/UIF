UIF Bibliography Files — BibTeX Sources

This directory contains the BibTeX citation files used across the Unifying Information Field (UIF) scientific paper series and Companion Experiment volumes. Each file corresponds to one UIF paper, supporting clear versioning, clean citations, and reproducible builds for arXiv, Zenodo, and journal submissions.

All .bib files follow a consistent naming pattern:
paperN.bib          → UIF Paper N
companion.bib       → UIF Companion Experiments

------------------------------------------------------------
Contents
------------------------------------------------------------

File               | Used In                                           | Description
------------------ | -------------------------------------------------- | -----------------------------------------------
paper1.bib         | UIF Paper I — Core Theory                         | Operator grammar (ΔI, Γ, β, λR), collapse–return dynamics, information theory.
paper2.bib         | UIF Paper II — Symmetry Principles                | Invariance, Noether structure, symmetry breaking, informational conservation.
paper3.bib         | UIF Paper III — Field & Lagrangian Formalism      | Variational principles, Euler–Lagrange derivations, informational PDEs.
paper4.bib         | UIF Paper IV — Cosmology & Case Studies           | Quasar variability, cosmological coherence, CMB residuals, dark-sector coupling.
paper5.bib         | UIF Paper V — Energy & Potential Field            | Energetic formalism, curvature of informational potential, α constant, coherence ceilings.
paper6.bib         | UIF Paper VI — Seven Pillars & Invariants         | Invariant architecture, agency, recursion, topology, cross-domain coherence.
companion.bib      | UIF Companion Experiments                          | Emulator references, calibration scripts, empirical coherence datasets.

------------------------------------------------------------
Usage Notes
------------------------------------------------------------

• Each paper imports only its own .bib file for modularity.
• The UIF Companion may draw from multiple .bib files when required.
• All BibTeX entries use consistent formatting:
  – DOI fields
  – Escaped TeX characters
  – Normalised author metadata
  – Journal-compatible reference structure

------------------------------------------------------------
Citation Workflow
------------------------------------------------------------

1. Each paper loads its bibliography with:
   \UIFbib{paperN}

2. arXiv and Zenodo builds pull .bib files from this directory automatically.

3. Updating a .bib file here propagates to all compiled PDFs that use it.

------------------------------------------------------------
Versioning
------------------------------------------------------------

All .bib files in this directory are maintained under Git version control.

Commit messages should reference the relevant UIF paper or Zenodo release when making updates. 
------------------------------------------------------------
