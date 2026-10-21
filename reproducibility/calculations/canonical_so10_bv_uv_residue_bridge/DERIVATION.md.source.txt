# BV Hessian and the complete formal one-loop logarithmic pole

Prospective proof;requires completed native and separate validation. The claim
is about a constructed formal local UV family,not a finite regularized trace.

## Classical operator identity with its actual source terms

Use the existing source-left BV bracket and the actual even source-linear
S=S0+sum J_i R_i. Q=(S,.),Qz_i=EL^L_Ji S,QJ_i=EL^L_zi S,QA=0.
The qualified E2 master FUNCTIONAL is zero with its complete current,not an
identically zero raw density. Differentiate that functional twice with even
arbitrary compact test directions h,k of component parity p_i. Write
H(h,k)=delta_k delta_h S. Prolong Q to h,k by
Qh=delta_h R,Qk=delta_k R and to every ordinary symmetric derivative jet.
Differentiating the first master variation then the second gives

    Q_lift H(h,k)=0.

This is a variational identity:the differentiated master current supplies the
boundary term. Source variations are indispensable:QJ_i=Euler_i S cancels
the Euler_i S times second variation of R_i. No equation of motion or source0
restriction is used. R may be nonlinear and contain jets;it must be independent
of J,as the actual action is. The physical Euler programs enter through QJ and
are retained by the full classical certificate rather than replaced by zeros.

Insert a formal odd epsilon on the LEFT so delta_epsilon=epsilon Q is even.
Let M be the Frechet operator of delta_epsilon z=epsilon R on integrated-field directions.
The right derivative convention is exactly the frozen tangent's
A_ij=right_j R_i=(-1)^(p_i*p_j)left_j R_i. Thus M_ij=epsilon A_ij.
In the bilinear matrix convention h_i H_ij k_j,the left formal adjoint is

    (Msharp)_ij=sum_alpha (-partial)^alpha
                         circ [(-1)^(p_i*(p_j+1))*M_ji,alpha].

The derivatives act on coefficients AND test functions;this is not a plain
transpose. Integration by parts in Q_lift H then gives the congruence

    delta_epsilon H = -Msharp H-H M

as differential operators,under the admitted boundaries. Full-size inputs
have180 first-jet tangent entries,none discarded. Their coefficients are
constant in integrated fields;this is checked from the actual field maps.
The remaining nonlinear Rsecondderivative information is already covered by
the qualified73218-position source Hessian. It is not assumed absent.

## A local residue appropriate to the mixed operator

For each finite external/coupling coefficient,the verified mixed weighted
principal inverse yields classical rational symbols with finite local jets,
integer homogeneous powers and denominators powers of pÂ² on the Wick UV
shell. Local differential vertices/adjoints and symbol compositions stay in
this class. Matrix entries may have different upper orders;weights telescope
in a closed product. At any requested homogeneous degree only finitely many
composition derivatives are needed. No global positive mixed Hessian or
convergent determinant is asserted. The reference witness and its complete
subtraction vertices define the explicit member of this family.

Define r(a)=integral dx average_S3 STr a_-4(x,p),with finite Grassmann
coefficient algebra at each formal degree. This is half the usual angular
residue up to the retained(2pi)^-4 normalization;the scalar UV coefficient
of1/(pÂ²)Â² is1/(16piÂ²) for logLambdaÂ². Constants do not affect a zero identity.

For homogeneous symbols use left composition
 a star b=sum_alpha i^-|alpha|/alpha! (partial_p^alpha a)(partial_x^alpha b).
At alpha0,fiber supertrace is graded cyclic. For higher alpha,integrate by
parts in x,then in p. The last p derivative acts on a function of degree-3
when the total degree is-4. Its S3 integral vanishes:the annulus divergence
theorem has equal flux on its two radii for degree-3. Repeating this moves
all p derivatives and converts the two composition sums into one another,
with the Grassmann fiber sign. Thus r([a,b]_graded)=0 as an INTEGRATED local
functional. The required boundary currents are retained,not raw densityzero.
This coefficient proof applies on the local flat UV shell with compact tests;
it does not assume the closed-manifold/zeta/positive-weight hypotheses.

The graded tangent times epsilon is an even matrix. Therefore only even
cyclicity is needed in the Hessian argument. Its formal adjoint is also a
DIFFERENTIAL operator:nonnegative integer p powers only. Consequently
r(M)=r(Msharp)=0. This is a degree statement,not declaring a divergent trace
of delta(0) to be zero. The inverse is the full formal parametrix/born inverse
of H,with G H=H G=1 in the local symbol algebra. Errors smoothing to arbitrary
negative order have no residue at any fixed coefficient.

## From the actual ordered heat family to the pole

The frozen full one-loop interaction functional is
 (i/2)sum_n>=1(-1)^(n+1)/n STr[(F Gref F V)^n],V=H-Kref,
with separate Gamma_ref[A] retained. At each finite external/coupling degree
there are finitely many relevant vertices/symbol terms. Q leaves external A,
Kref[A] and its heat generator fixed. It commutes with ordinary derivatives.
Thus Q varies ALL actual V,including the source Hessian,not the regulator.

The qualified ordered-multiheat theorem gives precisely the unheated degree-4
symbol as the leading log,with all other heat-derivative terms finite or power
terms and a uniformly integrable UV remainder. Its argument extends to the
complete local differential delta_epsilon V by the same finite-jet class and
weight count;odd coefficients are finite algebraic factors and epsilon makes
the full variation even. No extra negative heat powers or logp appear.
At the residue level cyclicity now combines all n variation positions,
canceling1/n. Summing the complete inverse series gives

    delta_epsilon Gamma1_log=(i/2)*(1/(16piÂ²))*r(G delta_epsilon H).

This is an equality of formal UV coefficients,not a noncommuting finite
trace identity. Gamma_ref remains but has Q variation zero because QA=0;
no logK complex-power theorem is required. All reference-subtraction vertices
must be kept so that G is the inverse of the ACTUAL H,not a selected block.

Apply the congruence and only the proved cyclic residue:

    r(G delta_epsilon H)
      =-r(G Msharp H)-r(G H M)
      =-r(Msharp)-r(M)=0.

Extract epsilon. If the stated actual-class hypotheses and checks hold,this
proves Q Gamma1_log=0 for the COMPLETE one-loop local-log family,modulo the
currents,including its source-free and source-dependent fields/orders. It does
not give individual unmeasured tensors or prove that a current partial Gamma
already equals this complete functional. No coefficient is fitted to a zero.

## A control that excludes the dangerous finite inference

Take Fourier shifts U_k and B=U_-k/pÂ² on flat4D. With a fixed scalar heat
weight exp(-t pÂ²),the trace of their commutator has density

 I(t,k)=integral d4p/(2pi)^4 exp(-t pÂ²)[1/pÂ²-1/(p+k)Â²]
       =[t kÂ²-1+exp(-t kÂ²)]/(16piÂ²*tÂ²*kÂ²).

Its leading log is zero,but its finite limit is kÂ²/(32piÂ²),not zero. Both
IR singularities are locally integrable in4D. Completing the Gaussian square
in a Schwinger parameter proves the formula;independent shift/radial reasoning
checks its expansion. The degree-4 angular residue of the translated
propagator cancels exactly. Finite weighted traces are not residue traces.

The actual finite-cutoff relation remains
 Q Gamma1=I1(B_Lambda)-(V_Lambda,Gamma1)-i div_heat R.
The nonlinear source correction can be nonzero and is retained. A log-only
zero cannot remove finite breaking,renormalized contacts,normalizations or
measure obligations. The specified BRST heat trace zero is a separate qualified
result;it is not the nonzero general even source-primitive trace.

## Interpretation and limits

A completed proof here would close ONE simultaneous formal one-loop UV
consistency requirement. It would not qualify the whole source-free finite
Slavnov identity,QAP,all-order prescription,full contact module,measure,
Lorentzian/causal/adiabatic/physical IR or quantum A5 equivalence. It would not
set b0 or kappa,measure295 color tensors,repair the old quartet normalization,
or resolve scalar quantum control/gauge matching. Authority remains34/39.

Cardona,Ducourtioux,Paycha section1 distinguishes local Wodzicki(super)residues
from noncyclic weighted finite traces:https://arxiv.org/html/math-ph/0207029 .
The argument above supplies a local symbol proof for the actual mixed class;
it does not adopt that paper's global elliptic/zeta hypotheses or import a
full QAP. Troost--Van Proeyen https://arxiv.org/html/hep-th/9307126 supports
retained-antifield regulator analysis,not this model's scientific acceptance.
