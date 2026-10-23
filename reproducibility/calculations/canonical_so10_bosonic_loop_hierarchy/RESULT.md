# BLH1: the retained bosonic loop hierarchy fails at both diagnostic points

The completed bosonic two-loop correction exceeds the tree kinetic term in
all six tested gauge/coupling positions. It also exceeds the one-loop term
in every position. Thus the existing fixed-reference bosonic truncation is
not perturbatively ordered at x=g10^2=1/2 or1,L=0. This is an explicit
negative diagnostic, not merely a warning about large printed coefficients.

Evidence validation receipt `validation_receipt.json`, SHA256
`5ac4b5961476d7aa152fdd3e0fd0ca3fed7a707834e086816120ebd6064f5e9f`,
status QUALIFIED_BOSONIC_LOOP_HIERARCHY_DIAGNOSTIC. Arithmetic/evidence
validation completed; the preregistered necessary hierarchy conditions fail
6/6. These statuses are different. Scientific/director acceptance is
NOT_PERFORMED; project_state.json/state113/authority34/39 are unchanged.

In BMC's already qualified normalization, write the background kinetic term
relative to its tree coefficient as K=1+k1+k2, where

 k1=-x*lambda1/(48*pi^2), k2=-x*lambda2/(768*pi^4).

The primary uses the completed FCT/FAN primary inputs and this kinetic map.
Replay uses their separately qualified replay inputs, starts from the
inverse-alpha shifts and divides each by4*pi/x. No inversion of a truncated
series, duplicate one-loop square, scale adjustment or physical fit enters.
The complete bosonic lambda2 includes all nine families and HTB once under
the original MSbar/tadpole convention. Unfinished VSG data were not used.

| x | Gauge factor | One-loop k1 | Two-loop k2 | abs(k2/k1) |
| --- | --- | ---: | ---: | ---: |
| 1/2 | U1 | -0.215602 | 21.210377 | 98.38 |
| 1/2 | SU2 | -0.038353 | 6.138535 | 160.05 |
| 1/2 | SU3 | -0.066810 | 4.909815 | 73.49 |
| 1 | U1 | -0.308300 | 49.278335 | 159.84 |
| 1 | SU2 | 0.015471 | 20.369589 | 1316.60 |
| 1 | SU3 | -0.056806 | 14.330519 | 252.27 |

All values are at the original fixed L=0 parent/scalar reference. The
tree-relative failure does not depend on an accidentally small one-loop
denominator. The positive value of1+k1+k2 is not evidence of convergence;
retaining that finite expression as an exact resummation would introduce
unsupported higher-order information. This screen does not calculate it as
a physical prediction or use it to rescue gauge matching.

Both routes agree at all60 retained numerical positions within1e-35;
maximum scaled difference6.88513091457252e-46 reflects inherited FAN table
precision. The six hierarchy classifications are derived from the actual
values, not required to be favorable or unfavorable by the verifier. Wrong
loop-factor and missing-external-x controls are nonzero where sensitive;
the x=1 external-x control is explicitly insensitive, while x=1/2 detects it.

No new BLH calculation failed or remained incomplete. Primary/replay/gate
elapsed after imports1.7852040/1.8051063/1.7999799s. Each short capture has
only one process sample:434,176/393,216/405,504bytes. Those launch-time
samples do not measure peak working memory. Available commit at launch was
over6.3GB; sampled8GiB,600s and24MiB-package bounds were not exhausted.
Preparations bind6030/6037 inputs; the compact package is about2.32MB.
Complete external captures: bosonic-loop-hierarchy-v1-2026-10-22. Readiness
and a local commit remain deferred until the live VSG work is terminal.

This rules out treating these two retained bosonic truncations as controlled
threshold predictions. It does not establish failure at every positive
coupling, a new scalar point or every allowed renormalization prescription.
It does not determine uncomputed fermion/heavy-vector contributions, justify
assigning them compensating values, or establish the full model's failure.
Matter/flavor remains human-paused; no missing term was silently set to zero.
Full physical C1, refit, unification and E5/A5 remain unqualified.

The normalization theorem, loop coefficients and physical assumptions are
inherited. The new evidence is their explicit, reproducible perturbative
interpretation, not independent verification of the whole action. Shared
software, inputs and AI authorship remain limitations. Prior scalar and tree
unitarity warnings, quartet failure, HB1/C5 block, custodyexit2/sevenNOTPASS
and all failed historical evidence are preserved. No external action.
