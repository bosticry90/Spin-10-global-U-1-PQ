# CSB1: dual certificate and interval feasibility

For any real L, put r_i=A_i+B_i*L, with B_i>0. Then

 B_j*r_i-B_i*r_j=B_j*A_i-B_i*A_j,
 max(abs(r_i),abs(r_j)) >= abs(B_j*A_i-B_i*A_j)/(B_i+B_j).

Thus T=max_pairs abs(B_j*A_i-B_i*A_j)/(B_i+B_j) is a lower bound on
min_L max_i abs(r_i). For a maximizing pair(i,j), the candidate
Lstar=-(A_i+A_j)/(B_i+B_j) gives opposite pair residuals of magnitude T.
Evaluating the third component verifies whether this candidate attains the
lower bound. For these positive slopes the interval argument also proves
that a maximizing pair supplies a feasible optimum.

Independently, abs(A_i+B_i*L)<=t is exactly

 I_i(t)=[(-t-A_i)/B_i,(t-A_i)/B_i].

All three constraints hold iff max_i lower_i(t)<=min_j upper_j(t).
Each lower_i and upper_j is affine in t, so the first feasible nonnegative
t is among their rational crossing values and0. Enumerating these values,
then testing the full intersection, gives a primal feasibility certificate.
At the optimum choose the midpoint of the intersection as the witness;
for a unique optimum it is a single point. These algorithms share the
mathematical problem, but have different implementation failure modes.

Use exact Fraction values of the retained decimal coefficient strings. The
normalization is k2_i=r_i/(768*pi^4). Elementary 3<pi<22/7 yields

 T/[768*(22/7)^4] < min_L max_i abs(k2_i) < T/[768*3^4]

when T>0. The endpoint versions with <= suffice at T=0. More importantly,
if intersection_i I_i(768*(22/7)^4) is empty, no L can satisfy all
abs(k2_i)<=1 for the true pi normalization and the frozen coefficient data.

Independent choices L_i=-A_i/B_i zero each component separately. They do
not solve this common-L problem. A positive exact T detects that false
relaxation. Removing the inactive third constraint may leave T unchanged;
that omission control is then insensitive and must be reported as such.

This proof concerns fixed coefficients. Replacing explicit L is not the
same operation as evolving the original MSbar parameters consistently.
Nor does exact rational algebra turn approximate loop coefficients into
exact physical quantities. The independent upstream amplitude checks and
their shared-assumption/precision limits are inherited without promotion.
