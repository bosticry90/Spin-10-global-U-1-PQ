# JMF1 replay serialization correction, prospective V2

Primary completed native0 with all source comparisons and type census.
Original replay failed native1 at output-row formatting after its first
tensor comparison: ImmutableSparseNDimArray mutates the dictionary passed to
its constructor, replacing coordinate-tuple keys with flat integer keys.
The following path+key operation then raised TypeError. Original source,
copy, preparation, full native capture and controller_failure stay immutable.
There is no original replay result or original verification receipt.

V2 passes dict(A),dict(B) into the two tensor constructors. The separately
retained coordinate dictionaries then still own their actual typed keys for
canonical serialization. No coefficient, tensor subtraction, full-domain
check, source sign, scientific hypothesis or acceptance test changes. The
completed primary is authenticated and reused; only replay and the previously
unlaunched verifier run. New sources/copies and an extending manifest are
frozen first. Same600s/8GiB/350MiB/16MiB limits. This is an implementation
failure, not a disagreement of the physics or a retrospective original PASS.
