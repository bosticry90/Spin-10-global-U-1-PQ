# Two finite differences that cannot be adjusted by a local affine subtraction

The qualified unchanged-point closure leaves the complete one-loop singlet
self-energy in the form

 Pi(s)=A_local+sum_b d_b/(32*pi²) sum_ij |D_bij|² L(s;x_i,x_j),
 L(s;x,y)=integral_0^1 du log[(u*x+(1-u)*y-u*(1-u)*s-i0)/Q²].

A_local includes the seagull; the complete pole also needs its separate
vacuum-source insertion. Both are momentum independent. A finite kinetic
normalization contributes a real linear polynomial in s. With a=6/5, the
coefficients of E and T sum to zero, and their momentum-weighted sums also
vanish. Thus these combinations of the complete function equal the same
combinations of only its bubbles, even in the presence of ANY c0+c1*s.
They do not determine the constant or slope and do not authorize subtracting
them from the already qualified pole. No on-shell scheme is adopted.

Let A=u*x+(1-u)*y, q=u*(1-u). The Euclidean single-pair kernel is

 e(x,y)=integral du log[((A+qa)*(A+3qa))/(A+2qa)^2]
       =integral du log[1-(qa/(A+2qa))^2].

For nonnegative squared masses it lies between log(3/4) and0. A massless
pair attains the lower value. Positive coefficient weights imply E<=0.
The complete E remains IR finite because its three momenta are nonzero.

The timelike combination uses

 t(x,y)=L(a;x,y)-3L(-a;x,y)+2L(-2a;x,y).

Its imaginary part is the original timelike cut, since the Euclidean terms
are real. For a massless pair, t=log4-i*pi. Dropping the absorptive part is
therefore a detectable error even if a real finite subtraction looks small.

## Independent spectral calculation

For one scalar pair set T0=(sqrt(x)+sqrt(y))², U0=(sqrt(x)-sqrt(y))² and

 beta(sigma)=sqrt[(1-T0/sigma)*(1-U0/sigma)] for sigma>=T0.

The imaginary part of L is -pi*beta(s) above threshold. Differentiating its
Feynman integral twice, or extending its discontinuity with two subtractions,
gives the convergent affine-annihilating dispersions

 e=-integral_T0^infinity beta(sigma)*2a²/
          [(sigma+a)(sigma+2a)(sigma+3a)] d sigma,

 Re t=-PV integral_T0^infinity beta(sigma)*6a²/
          [(sigma-a)(sigma+a)(sigma+2a)] d sigma,
 Im t=-pi*beta(a)*Theta(a-T0).

The rational kernels follow by combining1/(sigma-s) with the SAME finite-
difference coefficients. Their large-sigma falloff makes the subtraction
polynomial irrelevant. The minus sign agrees with the declared scalar
B_SS=-B convention, not a chosen cancellation sign.

For T0<a, remove the principal-value singularity analytically. Write
beta=beta(a)+(sigma-a)*R(sigma), where

 R=[2(x+y)/(a*sigma)-(x-y)²*(sigma+a)/(a²*sigma²)]/[beta(sigma)+beta(a)].

The constant integral is

 J0=-log[abs(T0-a)*(T0+2a)^2/(T0+a)^3].

Then Re t=-beta(a)*J0-integral6a²*R/[(sigma+a)(sigma+2a)].
This has no numerical principal-value cancellation. The massless pair is
handled by its exact expression. For T0>=a there is no interior pole.
The map sigma=T0/(1-z²),0<=z<=1 gives finite integration intervals; its
threshold endpoint is handled by the actual canceled rational expression.

## Third representation and controls

For Euclidean b>0 the polynomial A+q*b factors as
b*(u-r_minus)*(r_plus-u), with roots outside[0,1]. Its logarithmic integral
is log(b)+f(r_minus)+f(r_plus),

 f(r)=(1-r)log|1-r|+r log|r|-1, with0log0=0.

The corresponding timelike quadratic gives real-root logarithms and cut
length, or an arctangent primitive for complex conjugate roots. The separate
verifier derives these from elementary integration, not native quadrature.

For equal heavy squared masses x=y=X, expansion gives
e=-a²/(30X²)+O(a³/X³), Re t=-a²/(10X²)+O(a³/X³), Im t=0.
This follows from integral q² du=1/30 and the finite-difference second
moments2a² and6a², with the log's second-order factor-1/2.

For the actual pure-S reference, v²=3/5 and lambdaS=1 give the PQ pair
weight(2lambdaS*v)²=12/5 and radial pair weight(6lambdaS*v)²=108/5.
These anchor the neutral-block/cut normalization independently of its
numerical eigenvectors. Other blocks are retained; none is assigned zero
because its mass is large. Seagull/source omission is intentionally
insensitive here and remains a separate pole requirement.

The result is not a physical observable, a complete error bound, a proof of
LSZ or quantum control. It quantifies two nonlocal aspects of the actual
fixed-point two-point function. Even a small E can coexist with a sizable T
cut, local mass correction or slope. Perturbative same-bare input translations
change the loop kernel only at the next order; arbitrary physical changes of
couplings are outside this comparison. No new subtraction prescription,
global field redefinition or phenomenological input is selected.

[Martin, equations3.1-3.3](https://arxiv.org/pdf/hep-ph/0312092) supplies the
inherited scalar self-energy normalization. Published theory and qualified
input data are shared premises, not independently validated by these new
integral checks. Agreement tests representation, normalization and numerical
errors; it does not establish that Spin10 describes nature.
