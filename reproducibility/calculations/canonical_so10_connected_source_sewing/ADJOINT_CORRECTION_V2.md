# Adjoint execution V2: cached coefficient encoding

V1 failed before writing adjoint_result.json. The coefficient expression
helper is memoized and accepts an immutable tuple, while the new caller
passed a list after removing the common single g10 factor. V2 passes the
same exact coefficient entries as a tuple. No coefficient, comparison,
physical assumption, claimed rank or resource limit changes. V1 source,
capture and controller failure remain FAILED. The exact qB versus qLambda
comparison had completed before this encoding error; it is rechecked in V2.
