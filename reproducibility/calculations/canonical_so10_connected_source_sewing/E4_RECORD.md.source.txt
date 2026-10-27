# Delegated E4 preservation check

Run python -B tools/research_check.py e4 once, without --fresh. Authenticate
the existing sealed checkpoint and authority/custody checks; do not infer
new physics qualification from execution. Expected step exits0,0,0,0,0,2,
terminal COMPLETED/native0, custody exit2/seven references NOTPASS.
Capture complete output, launch ownership and sparse private samples.
Bound300s and8GiB sampled private,350MiB launch floor. Any unexpected
exit, changed custody count or authority mutation fails preservation.
No scientific replay, remote action, promotion or protected activation.
