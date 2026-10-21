# Compare the exact polynomial residual, not expression-tree spelling

VerifierV1 FAILED on the incomplete-scaling control. SymPy left its two equal
polynomials in different factorizations; direct structural == returned False.
V2 requires expand(lhs-rhs)==0. The mathematical control and every physical
input, tolerance, inequality and resource cap are unchanged. The V1 source,
preparation/controller and complete failed capture remain immutable; it has
no validation receipt. No native worker failed. There was also one earlier
prelaunch failed documentation patch, recorded separately from calculations.
