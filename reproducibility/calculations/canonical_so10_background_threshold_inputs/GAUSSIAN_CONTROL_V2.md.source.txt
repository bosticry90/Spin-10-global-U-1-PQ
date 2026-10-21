# Prospective V2 validation supplement

Both native runs and the full independent coefficient replay passed. No failed
execution is being replaced. Before final qualification add a distinct exact
Gaussian/Legendre control for the graph signs, to test the ghost-sunset sign
and the removal of 1PR dumbbells rather than merely reading inventory factors.
Original sources, preparations, captures and receipt remain byte-identical.
Same verifier180s/8GiB sampled/350MiB launch/4MiB package bounds.

In zero dimensions use S=x^2/(2G)+lambda*x^3/6+k*x^4/24, ghost determinant
1+u*x/a, and J=hbar*j. Exact Gaussian moments <x^(2n)>=(2n-1)!!(hbar G)^n
give, at order hbar in logZ,

    B=5lambda^2 G^3/24-k G^2/8-u lambda G^2/(2a)
      +j^2 G/2-j lambda G^2/2+u j G/a.

The vanishing mean fixes j=lambda G/2-u/a, not j=0. At mean zero Gamma=-hbar
logZ, hence its hbar^2 coefficient is

    k G^2/8-lambda^2 G^3/12+u^2 G/(2a^2).

This independently derives the quartic, boson-sunset and oriented ghost-sunset
weights with all lower connected/tadpole pieces retained until the Legendre
transform. Wrong ghost-loop sign and omission of Legendre subtraction change
the result. It is a combinatorial control for the universal Wick proof, not a
new field-theory integral or physical threshold. Include exact real-model
tensor/f sign mutants and document the projection insensitive to T's
antisymmetric part. Reuse the already passed whole-tensor verifier without
rerunning the native calculations; authenticate all earlier completed bytes.
