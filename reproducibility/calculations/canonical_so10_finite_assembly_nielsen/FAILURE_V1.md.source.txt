# FAN1 V1: Hermitian charge-form transport used an ordinary transpose

Both native workers COMPLETED and saved full observed captures and compressed
tables. The separate verifier FAILED at its first matrix comparison. Vertex
projections theta agree exactly; the transported charge forms and curvature
sources differ in particular diagonal signs. The finite assembly values agree
at the retained precision. No scientific validation receipt was produced.
All original sources/copies/captures/controller traceback remain unchanged.

The WHP input is EXPLICITLY a Hermitian form:
 B_old,ab=Tr[(ad(M_a)P)^dagger ad(M_b)P].
Its inherited C3 basis contains imaginary entries. If V=M*Z, direct expansion
requires B_new=Z^dagger B_old Z. The replay used Z^T B_old Z instead, causing
the observed negative charge norms. This is a basis-type implementation error,
not a new physical sign or an acceptable alternative prescription.

V2 uses the Hermitian left inverse of M and the conjugate-transpose transport.
It also checks explicitly that the normalized physical light frame is real,
that both frames span the same space and that the wrong transpose is detected.
No source normalization, charge coefficient, physical field, tolerance or
acceptance requirement changes. New replay_v2.py preserves replay.py.
The completed primary is authenticated/reused without rerun; only replay and
separate validation are executed under new exclusive frozen artifact names.
The original failure is not relabelled PASS. This avoidable basis-type error
is part of TrackB's engineering/verification record.
