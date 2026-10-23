# Preserved operational index-gate failure

All six S4F/S4A native calculations and separate validators completed and
qualified their declared scientific scopes. The end-of-turn raw/index byte
checks also matched all60 new files. The subsequent git diff --cached
--check formatting command exited2 solely for a new blank line at EOF in
S4F data.py:107 and its identical immutable data.py.source.txt snapshot.

The original seal.py, precommit manifest and the reproduced complete failed
index capture are preserved in external control folder
scalar-quartic-amplitude-v1-2026-10-21. This is an OPERATIONAL formatting-
gate failure, not a failed amplitude, verifier, scientific normalization or
resource gate. The frozen source bytes are not edited to remove the blank.

Append-only seal_v2.py verifies that the original git diagnostic contains
EXACTLY these two EOF-blank warnings, then applies git's blank-at-eof-only
formatting exception while retaining all other whitespace checks. It also
authenticates the original failed manifest/source/capture and every original
new file hash, and repeats the full raw/index/HEAD custody and unchanged-
old-evidence checks. No input, calculation, scientific condition, acceptance
threshold or physical scheme changes. Its updated manifest additionally
binds this explanation. No failed scientific evidence is relabeled PASS.
