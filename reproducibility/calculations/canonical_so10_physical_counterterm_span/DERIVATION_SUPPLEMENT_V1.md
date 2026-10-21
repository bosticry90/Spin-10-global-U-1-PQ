# Explicit census endpoints and control interpretation

This supplements the frozen derivation without changing its inputs or equations.
The native census covers36 coarse field/derivative carriers and47 ordinary-jet
placements, not36 independent invariant operators. Internal index tensors are
constrained by the Noether equations, not counted by those carrier numbers.

For each carrier let nv=nA+nB, nx its scalar count and nd its derivative count.
Only nv+nx+nd<=4 with nv+nd even occurs in the metric-only class. Coefficient
dimension is4-nv-nx-nd. The proof endpoints are exhaustive:

* nv=0: nd=0 is the scalar potential, including a separately retained constant;
  nx=1,nd=2 is a boundary; nx=2,nd=2 is the scalar kinetic bilinear. No other
  scalar-only derivative carrier is allowed by the bound and Lorentz parity.
* nx=0,nv=1: the nd=1 or3 metric contractions are divergences. nv=2,nd=0
  is a vector mass carrier, excluded by the affine parameter jet. nv=2,nd=2
  is curl/longitudinal; nv=3,nd=1 and nv=4,nd=0 are its gauge completions.
  For different physical/background connections, independent gauge identities
  remove the cross carrier; there is no invariant linear physical adjoint tensor.
* nx=1,nv=1,nd=1: B*d x or A*d x is a dimension3 carrier. Its leading affine
  parameter variation has a coefficient times Box x. Independent full-x jets
  force it to zero; no vacuum-shift Stueckelberg rule is present in qx.
  The scalar-linear Box x divergence cannot cancel it. The same argument first
  removes these terms with every allowed dimension-one coefficient.
* nx=1,nv=2,nd=0: the dimension3 scalar/vector-mass carrier then has no surviving
  derivative companion. Its independent affine parameter-jet coefficient
  forces zero. Global tensor contractions alone would not prove this exclusion.
* nx=2,nv=1,nd=1 and nx=2,nv=2,nd=0: for physical B these are exactly the
  scalar kinetic completion. For any external A, physical gauge invariance
  reduces them to a physical bilinear current and its possible A^2 companion.
  The highest background A power removes A^2, then off-shell divergence removes
  the current. A scalar Noether current is not identically conserved.

All remaining integer carriers are forbidden by parity/dimension. Ordinary
IBP identifies the different placements within these classes; no coefficient
requiring negative mass dimension or an explicit spacetime coordinate is used.
Rank4 Lorentz contractions use the three metric pairings. The counterterm's
actual metric grammar excludes parity-odd descent carriers; the local/global
theta and boundary questions are expressly not identified with this exclusion.

The native key `omitted_g_dPsi_nonboundary_control` stores the Euler witness
for REVERSING the sign of -g*d_g Psi: its density is2*q(g*d_g Psi). Independent
validation must also test literal omission, whose remainder is exactly half
that density and is separately nonzero. This is a control-label clarification;
the frozen native bytes and mathematical normalization are unchanged.
