# Verification harness correction

Review V1 failed at line 49. The endpoint table intentionally retains
empty JLambda columns as part of its zero complement. The verifier applied
its assertion that an AFFINE endpoint must be Ja to these empty columns
as well. There was no nonzero JLambda affine endpoint in the data.

V2 skips a column only when its stored endpoint polynomial is empty,
before checking that each nonzero affine endpoint has source Ja. All
90-column coverage, exact route equality, derivative-shape and nonzero
coefficient checks remain. Native sources/data are unchanged. The original
review/capture/controller failure and source copies remain FAILED, with
no original validation_receipt.json. Limits remain review 180 seconds,
8 GiB sampled private, 350 MiB launch floor; no scientific condition is
weakened or physical input changed.
