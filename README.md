# Spin(10) × global U(1)PQ: a work-in-progress gauge/scalar candidate

This repository shares an AI-assisted investigation of a candidate grand unified model. The plain-language explanation below describes the idea, the progress and the limitations. The technical note and reproducibility materials provide the equations, code and evidence.

**[Read the nine-page technical note, Version 4](paper/spin10_pq_technical_note.pdf)** · [Editable LaTeX source](paper/spin10_pq_technical_note.tex) · [Reproduction guide](reproducibility/README.md)

## A plain-language explanation

This project asks whether one particular mathematical model could provide a consistent high-energy description of electromagnetism and the weak and strong nuclear forces. Those forces are already described successfully by the Standard Model. A grand unified model tries to relate them within a larger structure at much higher energies.

“Spin(10)” names the mathematical symmetry used here. “Peccei–Quinn,” or PQ, names an additional symmetry motivated by the strong CP problem: a symmetry-breaking effect allowed by the usual equations of the strong interaction appears to be extremely small. Established PQ models introduce an axion as part of the proposed explanation. A realistic axion prediction for this particular construction remains unfinished. Spin(10) unification and PQ symmetry are established research ideas; this project investigates a specified variant and its computational checks.

### What has to work?

A proposed model needs much more than equations that look plausible. Its mathematical rules must fit together. Its fields need a suitable stable configuration. Its interactions need to support controlled calculations. It must eventually reproduce known particles and their properties, and the measured strengths of the three forces must be compatible with the proposed unification.

The calculations test these requirements separately. Passing one test does not automatically pass the others.

### What has the project found?

There are useful mathematical results. One exploratory choice of parameters passes several classical scalar tests, including positive masses for the retained massive modes, a positive effective Higgs interaction, and a proof that the quartic part of the potential grows positively at large field values. That last result does not prove that the chosen configuration is the lowest-energy vacuum or remains suitable after quantum corrections.

The tests have also exposed real problems. An earlier Higgs tuning failed when other fields were allowed to adjust. Another point had a positive Higgs quartic but failed the stated perturbativity test. These failures are preserved in the materials.

At the newer classical point, a one-loop correction to the singlet’s squared mass is larger than its tree-level value in the declared expansion. Newer momentum-based checks measure different aspects of the same response and give smaller values. They do not erase the large shift or establish that higher-order corrections are controlled.

Gauge unification remains unresolved. The existing approximate calculation does not make the three force couplings meet. Parts of the more complete two-loop calculation have now been worked out, but essential pieces remain. No successful physical unification benchmark or definitive exclusion of the whole construction follows from the present calculation.

Recent symmetry and quantum-consistency results strengthen the investigation within their stated mathematical domains. They do not yet establish the complete physical quantum theory. The short technical note explains those boundaries.

### What role does AI play?

This is a solo, AI-assisted investigation. LLMs helped develop derivations, write calculation and verification code, and prepare the explanations. The repository owner directs the project and retains responsibility for scientific interpretation and acceptance.

Different computational routes can catch mistakes, but they share model assumptions, some inputs and software, and AI-assisted authorship. They are not independent scientists or outside confirmation. Failed calculations and corrections are part of the record. A program returning “PASS” supports only the test it actually performed.

### What can a reader reasonably conclude?

There is a definite candidate with reproducible, bounded results and documented setbacks. Its physical viability has not been established, and no experimental confirmation is claimed. The value of the work so far is making the proposal explicit, testing it, and identifying what succeeds, what fails, and what still needs evidence.

For details, start with the technical note and reproduction guide linked above. The portable pilot provides a small, self-contained way to rerun one complete classical identity; it does not verify the entire model. Specific feedback on an equation, assumption, calculation or missing test is welcome.

## Technical summary

The scalar content is a real 54, a complex self-dual 126, a complex 10, and a complex singlet, with global Peccei–Quinn selection rules and no supersymmetry.


Updated 20 October 2026, from source checkpoint `7562f42c14ef1ab5a946fbfc4534509f3378c76b`. The earlier positive-quartic point subsequently failed a perturbativity screen. A different exploratory point has stronger classical certificates but a large one-loop singlet correction. Neither is an established physical benchmark.

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
| Quantum control at new point | Local-inclusive one-loop singlet pole shift ≈ 140%; separate affine-subtraction-independent Euclidean/timelike combinations ≈ 1.94% / 20.27% | Distinct diagnostics, not contradictory estimates or a higher-order error bound; no reliable physical pole prediction |
| Gauge matching at earlier positive-quartic point | Maximum inverse-coupling residual ≈ 1.060 at one loop; ≈ 0.745 with two-loop SM running and one-loop thresholds | A mismatch for those inputs; finite two-loop heavy constants remain incomplete. These residuals do not apply to the new point |
| Gauge/PQ structure | Local perturbative Spin(10) gauge-anomaly traces vanish; PQ coefficients N = 12, E = 32, E/N = 8/3; conditional wall count 3 | Representation and ordinary-orbit results; global completion and physical axion cosmology remain open |
| Formal one-loop consistency | Complete local logarithmic UV Slavnov identity, actual parity-even bosonic counterterm closure, and constructed compact causal/QAP/normalization results in their declared domains | Material progress beyond the previous locality prerequisite; full source/global/physical E5/A5 requirements remain unqualified |
| Two-loop threshold primitives | VVVV, VVSS, VSS and ghost–scalar families have scoped amplitude results at the older +0.10486 point | An inventory of four of nine families, not four complete physical thresholds; full finite C1 and unification remain unresolved |

The initial Stage 2 failure does not refute every point of the construction. Gauge matching uses the earlier +0.10486 point, whose subsequent perturbativity failure is retained. Its spectrum, thresholds and loop results are not transferred to the newer exploratory point. Missing finite thresholds are not assumed to rescue the mismatch. Diagnostic fitted scales are not physical predictions.

Global quartic positivity is now certified at one exploratory point. The preferred vacuum, quantum control, complete gauged scattering, full quantum consistency, finite heavy-threshold matching, realistic matter/neutrino inputs, and axion and proton-decay phenomenology remain open. The new momentum combinations cancel local affine subtractions without deleting the large local-inclusive shift or its absorptive cut. A nonzero internal Yukawa carrier prevents claiming a complete two-loop singlet error bound without the missing matter inputs. Uniform scalar weakening is not a demonstrated quantum-control rescue. The model has not been established as a physically viable GUT or as experimentally supported.

## What the materials contain

- The updated Version 4 note and editable source, with public Versions 2 and 3 preserved in [paper/archive](paper/archive/).
- Browsable scalar/gauge calculation programs, frozen scalar points, and recorded results.
- The unchanged original source archives plus a versioned update covering the frozen tracked source tree and referenced external research-control materials, including failed attempts.
- A [closed portable Hessian pilot](reproducibility/portable_dh_v1/README.md), requiring Python 3.11+ and only the standard library.
- SHA-256 manifests and a verifier that authenticate packaged bytes without executing or scientifically accepting the calculations.

This publication is a fixed snapshot of committed evidence through the stated checkpoint. The [V421 handoff](reproducibility/RESEARCH_EXECUTION_HANDOFF_V421.md) supplies the frozen continuation context; work after that checkpoint is excluded. Classical certificates and conditional quantum results retain their precise assumptions; earlier failed and blocked evidence remains classified as such. Formal scientific authority remains version 113, at 34 of 39 ledger items. Historical custody is not a global pass.

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

The C1 amplitude program uses the older point and a fixed background-field Feynman-gauge reference; it is separate from the newer exploratory point and the formal 643-field nonlinear-source construction. No old spectrum, partial primitive or normalization prescription is silently transferred between them. Remaining graph families, counterterm remainders, finite insertions, EFT matching and the final conversion to C1 are not set to zero.

For discussion, useful questions are how to define controlled physical inputs while retaining the singlet cut, and how to finish the primitive/counterterm/EFT layers without double counting.
