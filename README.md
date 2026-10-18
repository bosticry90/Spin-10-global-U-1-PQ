# Spin(10) × global U(1)PQ: a work-in-progress gauge/scalar candidate

This repository hosts a short technical discussion note and reproducibility materials for an AI-assisted investigation of a nonsupersymmetric Spin(10) model with global Peccei–Quinn selection rules. The scalar content is a real 54, a complex self-dual 126, a complex 10, and a complex singlet.

**[Read the eight-page technical note, Version 3](paper/spin10_pq_technical_note.pdf)** · [Editable LaTeX source](paper/spin10_pq_technical_note.tex) · [Reproduction guide](reproducibility/README.md)

Updated 17 October 2026, from source checkpoint `22709b33f20484efe16eb4c3592d690c8e0650f3`. The earlier positive-quartic point subsequently failed a perturbativity screen. A different exploratory point has stronger classical certificates but a large one-loop singlet correction. Neither is an established physical benchmark.

The construction follows established GUT and PQ literature, especially [Babu and Khan (2015)](https://arxiv.org/abs/1507.06712). Its scalar potential is a separately specified source-derived variant. Published benchmarks, fermion fits, and unification conclusions are not adopted as results for this variant. No new unification principle or exhaustive novelty claim is asserted.

## Results and limits

| Item | Recorded result | What it establishes |
| --- | --- | --- |
| Scalar action | Complete renormalizable invariant basis; 29 Hermitian coefficient groups, or 34 real coefficient directions before rephasings | A specified scalar construction |
| Stage 1 scalar point | Rank 294, nullity 34, positive physical quadratic modes | Local scalar positivity modulo 33 gauge and one PQ symmetry direction |
| Stage 2 Higgs tuning | Rank 290, nullity 38, one light complex Higgs doublet at quadratic order | An exact quadratic tuning only |
| Relaxed initial Stage 2 quartic | Effective tree-level Higgs quartic ≈ −56.49 | **This initial tuned point is not a local scalar minimum** |
| Earlier positive-quartic point | Rank 290, nullity 38, relaxed quartic ≈ +0.10486; later coherent tree channel has \|a₀\| ≈ 0.76809 > 1/2 | Local tree positivity survives, but this point fails the stated perturbativity screen |
| New exploratory scalar point | Different frozen inputs; 290 positive modes, 38 zeros, relaxed quartic ≈ +0.10744 | A separate classical witness, not an adopted benchmark |
| Complete classical bounds at new point | Full 328-field quartic lower bound with positive margin ≈ 0.00047914; whole scalar-contact norm ≤ 0.47004 < 1/2 | Global quartic positivity and a contact-only bound; preferred vacuum and full gauged scattering remain open |
| Quantum control at new point | Complete selected one-loop singlet pole correction has magnitude/tree squared-mass ratio ≈ 1.40004 | A small correction is unsupported in the declared expansion; no reliable pole mass/width is predicted |
| Gauge matching at earlier positive-quartic point | Maximum inverse-coupling residual ≈ 1.060 at one loop; ≈ 0.745 with two-loop SM running and one-loop thresholds | A mismatch for those inputs; finite two-loop heavy constants remain incomplete. These residuals do not apply to the new point |
| Gauge/PQ structure | Local perturbative Spin(10) gauge-anomaly traces vanish; PQ coefficients N = 12, E = 32, E/N = 8/3; conditional wall count 3 | Representation and ordinary-orbit results; global completion and physical axion cosmology remain open |
| Selected quantum identities | Additional source/ghost poles and scoped Ward/Slavnov checks; latest background extension is conditional on locality of the actual regulated UV pole | Bounded progress, not complete quantum consistency or a proved model-specific locality theorem |

The initial Stage 2 failure does not refute every point of the construction. Gauge matching uses the earlier +0.10486 point, whose subsequent perturbativity failure is retained. Its spectrum, thresholds and loop results are not transferred to the newer exploratory point. Missing finite thresholds are not assumed to rescue the mismatch. Diagnostic fitted scales are not physical predictions.

Global quartic positivity is now certified at one exploratory point. The preferred vacuum, quantum control, complete gauged scattering, full quantum consistency, finite heavy-threshold matching, realistic matter/neutrino inputs, and axion and proton-decay phenomenology remain open. A local RG/log cancellation checks the large singlet correction without making it small. The model has not been established as a physically viable GUT or as experimentally supported.

## What the materials contain

- The updated Version 3 note and editable source, with the original public Version 2 preserved in [paper/archive](paper/archive/).
- Browsable scalar/gauge calculation programs, frozen scalar points, and recorded results.
- The unchanged original source archives plus a versioned update covering the frozen tracked source tree and referenced external research-control materials, including failed attempts.
- SHA-256 manifests and a verifier that authenticate packaged bytes without executing or scientifically accepting the calculations.

This publication is a fixed snapshot of committed evidence through the stated checkpoint. The completed weighted-reference and local-covariant-witness records are included; work after the frozen checkpoint is excluded. Classical certificates and conditional quantum results retain their precise assumptions; earlier failed and blocked evidence remains classified as such. Formal scientific authority remains version 113, at 34 of 39 ledger items. Historical custody is not a global pass.

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

For discussion, useful questions are whether a justified physical-input expansion can control the new point's large singlet correction, and which model-specific locality and finite-threshold calculations are needed before extending the quantum and gauge conclusions.
