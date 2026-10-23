# Report serialization failure, preserved

After all S3A1 scientific workers passed, the first result-report writer
used Path.open('x',newline='\n') without an explicit encoding. Windows
cp1252 raised UnicodeEncodeError for U+2248 (approximately-equal sign) at
position1859. Its exec command exited1; the intended RESULT.md was created
with0 bytes and no report content. That exact empty artifact is preserved
as failed_result_draft_v1.md (SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855).

The corrected writer explicitly uses encoding='utf-8', newline='\n' and
exclusive creation for the new RESULT.md. No frozen scientific source,
input, native table/capture, validation receipt, parameter, target or gate
was edited or rerun. This is an engineering/report-save failure, not a
failed scientific calculation. The original error is preserved in the
Codex tool transcript; no successful scientific receipt is inferred from
that failed command. Later byte seals must include both this record and
the empty failed artifact. The goal and protected authority remain unchanged.

The same review found that the already-bound S3M1/S3U1 result reports had
been successfully saved in CP1252, including its byte for superscript2.
Those originals remain byte-identical because later preparations bind them.
UTF8-readable RESULT_UTF8.md mirrors are appended beside them, with exactly
the same decoded text; they are navigation copies, not requalified evidence.
All scientific JSON/source/tables/captures and their hashes are unaffected.
The encoding manifest is REPORT_ENCODING_MIRRORS.json. Future report writers
must use explicit UTF8/binary output rather than the Windows locale default.
