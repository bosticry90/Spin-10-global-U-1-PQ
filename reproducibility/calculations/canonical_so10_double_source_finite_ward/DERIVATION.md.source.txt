# DSW1: actual cotangent operation, loop differentiation and source Ward terms

Prospective; full paired execution and separate gate are required.

Use Lorentzian real physical source variables for the polynomial operation.
At the end apply the same Wick/source continuation as DSF. In particular
qa_M=-Lambda_M+..., bJL_M contains-Ja_M, while JLambda_M=-iJLambda_E,
Ja_M=-Ja_E, Lambda_M=-iLambda_E. Thus bJL_E contains+iJa_E. A sign from
one chart cannot be copied as the sign in the other. The parent two-JL
coefficient itself has the unchanged DSF Euclidean/Lorentzian normalization.

The actual BV bracket gives bphi_i=R_i and bJ_i=leftEuler_phi_i Sigma.
For the present parent only qC and E_Lambda enter:

 E_Lambda_i = leftEuler_Lambda_i GF
            +sum_r Ja_r leftEuler_Lambda_i(qa_r)
            +sum_r JL_r leftEuler_Lambda_i(qLambda_r).

Lambda is even, so its local derivative introduces no odd crossing sign.
The source coefficients precede the actual field-rule words. No other R
depends on Lambda; both the physical/SMA action and newhPi are independent
of it. This direct construction must agree with the separately qualified
E2 auxiliary source columns after the SAME dual coordinate transport.

Let Lambda_raw=A Lambda_phys, JLambda_raw=A^-T JLambda_phys. Then
E_phys=A.T E_raw. Ghost rules use C_raw=Cinv C_phys, qC_phys=Cinv^-1 qC_raw.
The antighost sources use the same source dual. Derivatives and backgrounds
are transported before products are combined; no source is set0 first.

For P=-sum_(i<j,k<l)T_ij;kl JL_i JL_j C_k C_l, apply the odd derivation
with prefix sign(-1)^(sum of preceding parities). This reconstructs the
complete Ward image of the actual relative contact. It includes lower-source
ordinary/GF and source-dependent descendants rather than just a chosen
Ja*JL*C*C projection.

An independent route starts from A_matrix=sum_i,k JL_i C_k K_ik. External
JL,C are odd; hence Tr(A_matrix^2)=-2sumT JLJLCC. Consequently P=Tr(A_matrix^2)/2.
Since A_matrix is even, finite fiber trace cyclicity gives

 bP=Tr(A_matrix bA_matrix),
 bA_matrix=sum_i,k [(E_i)C_k-JL_i(qC_k)] K_ik.

Both K factors may be replaced by their independently action-verified -SF
values; their two minus signs cancel. The replay contracts the SF Gram
tensor AFTER applying these source/field variations, not after reading the
new P or its Ward image. This is the marked-vertex variation of the actual
bubble/box LOCAL comparison. The finite radial factor-log2 was independently
derived in DSF and is not reevaluated or fitted here. A full new continuum
loop calculation is not claimed.

The source-gradient relation has nontrivial companion terms. D_i and b are
odd, so D_i b+bD_i=W_i. The only relevant source derivative of E_l is
D_i E_l=g S_i(l,h)C_h, derived from the actual JL*Lambda*C action. It is
independent of JL, so [D_j,W_i]=0. Therefore

 D_jD_i bP=bD_jD_i P+W_iD_jP-W_jD_iP.

This is verified for the complete exterior source-pair/ghost-triple tensor,
including zeros. Omitting W terms is a control, not an acceptable Ward rule.
Taking only qC on the twice-source-differentiated kernel loses these terms.
The Ja/GF parts have source degree<=1 and drop after two JL derivatives,
but they are retained in the full bP density and its first-source identities.

All local multiple-source parents are the DSF-completed three patterns.
The actual source action is linear, so its cotangent operation preserves
or lowers source degree. Thus the degree2 image above receives no possible
missing contribution from a lower-source parent or an absent degree3 parent.
It specifies the complete highest-source part of the RELATIVE finite Ward
comparison. It need not vanish. Its degree1 part is only this parent's
contribution until the other finite parents are included.

In the fixed joint Schwartz one-loop/first-variation domain, local b commutes
with the comparison operations as previously qualified, including source
Euler terms, metric first jet and the retained inverse/IR defects. Hence
b(Gamma_dim,FP-Gamma_heat,FP)=bC_rel. Extracting source degree2 is legitimate
by the source-degree filtration. This does not assert either absolute
breaking is0, construct every coincident pullback, or prove that P alone is
a classically BRST-invariant counterterm. The scalar/auxiliary GF-v members
remain tied to their frozen reference. Gamma_ref[A] is retained with QA0.

This is not two independent Q applications. Functional source derivatives
are distributions obtained from the same augmented functional; a restriction
of their insertion coordinates to an arbitrary diagonal requires a separate
extension argument. Full nonlinear products/QAP, measure/globalphase,
causal/Lorentzian/physicalvacuum, chiral equivalence and E5/A5 remain open.
