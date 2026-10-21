# Complete actual Hessian reproduction pilot

This closed bundle reproduces the entire 99,256-position classical identity

    delta_antighost GF'' - sum_J V_J R_J'' = B_sourcefree'' + C

for all 33 broken directions, all 643 integrated field maps, all retained
orders and jets. C contains both required mixed terms. Every coefficient and
implicit zero is compared with the qualified ef70f25 result after computation.

Copy this entire directory to another directory, including a path with spaces.
From that directory run:

```text
python -I -S -B run.py --method slot
python -I -S -B run.py --method left
```

Python 3.11+ syntax and the Python standard library are sufficient; no pip,
SymPy, Git, personal source directories or repository checkout is used at
runtime. The actual tested version/platform are recorded by each run. A
different operating system or Python version is not certified without a run.
The script rejects optimized execution and enforces a 180-second worker limit.
The project controller separately observes the 8-GiB private-memory limit.

The manifest hashes every bundled source and compressed payload. Inputs are
complete exact raw action projections with declared field/parity/source maps.
A restricted AST parser evaluates only rational numbers, the fixed radical
basis, coupling and width powers. No source text is evaluated as Python code.
The package rejects missing/altered files, undeclared outside reads and writes.
The reference coefficient table cannot be opened before the result is computed.

The input exporter checked EVERY projected coefficient and its established
normal-form hash against the qualified engine. Origin paths in the archived
receipt are historical provenance labels, never files opened by the pilot.
The archived receipt and expected result are unchanged bytes, deterministically
gzip-compressed. The manifest is a reproduction input manifest, not an alternate
scientific authority or a cryptographic signature.

This pilot does not reproduce the 727,722-position scalar pole, the complete
quantum functional, the upstream representation/action proofs, the UV theorem,
renormalized products, QAP or E5/A5. It inherits the physical interpretation of
its qualified action projections. Both portable methods share inputs and exact
arithmetic; they are not independent scientists or independent validation of
those physical premises. Source and data are specific to this bounded pilot;
this directory is not a new universal QFT framework.
