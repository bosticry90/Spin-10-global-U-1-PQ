"""Read-only package byte checks. This does not execute scientific calculations."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "provenance/publication_manifest_v1.json").read_text(encoding="utf-8"))
    mismatches = []
    for entry in manifest["release_files"]:
        path = ROOT / entry["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    source_manifest = json.loads((ROOT / "provenance/source_manifest_v1.json").read_text(encoding="utf-8"))
    for part in source_manifest["archives"]:
        snapshot = ROOT / "reproducibility" / part["filename"]
        with zipfile.ZipFile(snapshot) as archive:
            entries = [e for e in source_manifest["files"] if e["archive"] == part["filename"]]
            if set(archive.namelist()) != {e["path"] for e in entries}:
                mismatches.append("archive file inventory:" + part["filename"])
            for entry in entries:
                try:
                    data = archive.read(entry["path"])
                except KeyError:
                    mismatches.append(entry["path"])
                    continue
                if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                    mismatches.append("archive:" + entry["path"])
    print(json.dumps({
        "execution_state": "FAILED" if mismatches else "COMPLETED",
        "byte_authentication": "MISMATCH" if mismatches else "AUTHENTICATED_PACKAGED_BYTES",
        "release_files_checked": len(manifest["release_files"]),
        "source_files_checked": len(source_manifest["files"]),
        "mismatches": mismatches,
        "scientific_calculations_rerun": False,
        "scientific_acceptance": "NOT_PERFORMED",
        "director_acceptance": "NOT_INFERRED",
    }, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
