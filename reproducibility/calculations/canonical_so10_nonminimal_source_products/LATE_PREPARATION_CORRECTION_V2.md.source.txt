# Late overlap preparation V2: use the historical manifest's actual schema

The original late preparer stopped before launching a worker: it expected
new_files_sha256 in UCV's final receipt, but that older receipt records
verification metadata. Its source/copies and exact controller KeyError
remain. No late scientific capture or result was produced.

UCV's actual final_review_preparation.json binds both classical tables and
vertices_v2.py by absolute input_sha256 paths. V2 authenticates those
original recorded bindings, not freshly rebound historical policy bytes.
The mathematical comparison is unchanged. The new worker differs only in
its preparation filename. Preserve all original sources and metadata;
resource and acceptance limits do not change. This was a provenance-schema
implementation error, not a failed mathematical comparison.
