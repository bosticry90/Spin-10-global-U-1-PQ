# Post-calculation editorial patch rejection

Execution classification: rejected documentation edit, not scientific worker
or verifier failure. No frozen script/input/table/receipt changed. The tool
rejected this whole patch because its second context did not match the text:

```diff
*** Update File: calculations/canonical_so10_vector_scalar_quartic/RESULT.md
@@
 No g10 or subtraction scale was chosen. Coefficients below are rounded for
 reading; both authenticated amplitude tables retain50 decimal digits.
+Here F2 in Gamma is physical curvature. The two external couplings are
+stripped in Lambda, as in VQP1 and the existing FCI/HTB normalization; do not
+multiply the older contributions by an extra g10^2 when assembling them.
@@
 common-error limitations.
```

Exact diagnostic: `apply_patch verification failed: Failed to find expected
lines in .../RESULT.md: common-error limitations.` The successful subsequent
patch uses the actual full line and adds the inherited-heat qualification.
This event does not alter either completed scientific receipt.
