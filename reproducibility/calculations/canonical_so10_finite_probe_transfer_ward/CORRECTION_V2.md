# Replay serialization correction

Original primary completed. Original replay reached output serialization
after its assertions, then failed: its independently rank-factorized sparse
matrix carries SymPy Integer indices, which JSON does not serialize. The
original native.py/source copy, preparation, primary completed evidence,
replay full failed capture and controller_failure.json remain unchanged.
There is no original scientific validation receipt and no original replay
quantum output. Do not relabel that run PASS because earlier assertions ran.

A subsequent shell-quoted generator command failed PowerShell parsing before
Python launched; it wrote no generated source. The file-based generate_v2.py
avoids that quoting problem. This is a separate orchestration error, not a
second mathematical failure or a change to the completed primary result.

V2 converts matrix output indices explicitly with int(i),int(j). It changes
no coefficient, algebra assertion, analytic assumption, physical input or
180-second/8-GiB/350-MiB/12-MiB limit. New native_v2.py, verifier_v2.py,
continuation preparer/controller and copies are frozen separately before
execution. Only replay is repeated. Completed original primary is reused
after hash authentication. The new verifier compares it with replay_v2.
All failures retain their exact captures and original manifest bindings.
