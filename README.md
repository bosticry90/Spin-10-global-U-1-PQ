# Spin(10) × global U(1)PQ: a work-in-progress gauge/scalar candidate

This repository hosts a short technical discussion note and reproducibility materials for an AI-assisted investigation of a nonsupersymmetric Spin(10) model with global Peccei–Quinn selection rules. The scalar content is a real 54, a complex self-dual 126, a complex 10, and a complex singlet.

**[Read the six-page technical note](paper/spin10_pq_technical_note.pdf)** · [Editable LaTeX source](paper/spin10_pq_technical_note.tex) · [Reproduction guide](reproducibility/README.md)

The construction follows established GUT and PQ literature, especially [Babu and Khan (2015)](https://arxiv.org/abs/1507.06712). Its scalar potential is a separately specified source-derived variant. Published benchmarks, fermion fits, and unification conclusions are not adopted as results for this variant. No new unification principle or exhaustive novelty claim is asserted.

## Results and limits

| Item | Recorded result | What it establishes |
| --- | --- | --- |
| Scalar action | Complete renormalizable invariant basis; 29 Hermitian coefficient groups, or 34 real coefficient directions before rephasings | A specified scalar construction |
| Stage 1 scalar point | Rank 294, nullity 34, positive physical quadratic modes | Local scalar positivity modulo 33 gauge and one PQ symmetry direction |
| Stage 2 Higgs tuning | Rank 290, nullity 38, one light complex Higgs doublet at quadratic order | An exact quadratic tuning only |
| Relaxed initial Stage 2 quartic | Effective tree-level Higgs quartic ≈ −56.49 | **This initial tuned point is not a local scalar minimum** |
| Later positive-quartic point | Rank 290, nullity 38, positive heavy masses and relaxed Higgs quartic ≈ +0.10486 | A distinct local tree-level scalar benchmark; global boundedness and full physical viability remain open |
| Gauge matching | Maximum inverse-coupling residual ≈ 1.060 at one loop; ≈ 0.745 with two-loop SM running and one-loop thresholds | A concrete mismatch for the frozen inputs; the complete gauge-unification verdict remains unresolved |
| Symmetry and quantum checks | Selected classical covariant identities and one-loop scalar operator closure pass within stated scopes; particular component-action and normalization candidates fail | Bounded mathematical results, not complete quantum consistency |

The initial Stage 2 failure does not refute every point of the scalar construction. A later point passes the local relaxed-quartic test, and the gauge-matching calculations use that later point's spectrum. Missing finite two-loop heavy thresholds are not assumed to rescue its gauge mismatch. Diagnostic fitted scales are not physical predictions.

Global boundedness, loop control of the locally acceptable light-Higgs point, complete quantum consistency, finite heavy-threshold matching, a realistic numerical matter/neutrino sector, and axion and proton-decay phenomenology remain open. The model has not been established as a physically viable GUT or as experimentally supported.

## What the materials contain

- The corrected Version 2 technical note and its editable source.
- Browsable scalar/gauge calculation programs, frozen scalar points, and recorded results.
- A compressed source/evidence snapshot covering the supporting local imports, frozen inputs, and manifest-bound files for the note's selected quantum statements.
- SHA-256 manifests and a verifier that authenticate packaged bytes without executing or scientifically accepting the calculations.

This publication is a fixed snapshot. New uncommitted vector/ghost calculations that were still undergoing qualification when the note was prepared are excluded from its earned claims. Earlier failed and blocked evidence remains classified as such; historical custody is not presented as a global pass.

The [reproduction guide](reproducibility/README.md) distinguishes byte checks, quick computational checks, expensive replays, and historical Git-custody limits. It records exactly which checks were performed for packaging.

## AI assistance and authorship

This is solo work shared by the repository owner, with LLM assistance in calculation development, code, verification work, and writing. Different computational routes share model inputs, some tensor/arithmetic implementations, libraries, and an analyst. They are not independent scientists or external verification. Scientific direction and acceptance remain the human author's responsibility.

## Literature

- K. S. Babu and S. Khan, *A Minimal Non-Supersymmetric SO(10) Model: Gauge Coupling Unification, Proton Decay and Fermion masses*, Phys. Rev. D 92, 075018 (2015). [arXiv:1507.06712](https://arxiv.org/abs/1507.06712).
- R. D. Peccei and H. R. Quinn, *CP Conservation in the Presence of Pseudoparticles*, Phys. Rev. Lett. 38, 1440 (1977). [DOI](https://doi.org/10.1103/PhysRevLett.38.1440).
- A. Ernst, A. Ringwald and C. Tamarit, *Axion Predictions in SO(10) × U(1)PQ Models*, JHEP 02 (2018) 103. [arXiv:1801.04906](https://arxiv.org/abs/1801.04906).
- W. Martens, *Towards a Two-Loop Matching of Gauge Couplings in Grand Unified Theories*, JHEP 01 (2011) 104. [arXiv:1011.2927](https://arxiv.org/abs/1011.2927).
- M. Luo and Y. Xiao, *Two-loop Renormalization Group Equations in the Standard Model*, Phys. Rev. Lett. 90, 011601 (2003). [arXiv:hep-ph/0207271](https://arxiv.org/abs/hep-ph/0207271).
- D. Buttazzo et al., *Investigating the near-criticality of the Higgs boson*, JHEP 12 (2013) 089. [arXiv:1307.3536](https://arxiv.org/abs/1307.3536).

For discussion, two focused questions are which analytic constraints on heavy-field relaxation can screen other scalar points, and what controlled finite-threshold calculation or bound is needed before assessing the frozen gauge mismatch.
