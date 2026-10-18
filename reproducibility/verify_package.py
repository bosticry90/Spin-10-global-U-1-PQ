"""Read-only release and source-byte authentication, without scientific execution."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest_stream(stream):
    digest = hashlib.sha256()
    size = 0
    for data in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(data)
        size += len(data)
    return digest.hexdigest(), size


def main():
    release = json.loads((ROOT / "provenance/publication_manifest_v2.json").read_text())
    base = json.loads((ROOT / "provenance/source_manifest_v1.json").read_text())
    update = json.loads((ROOT / "provenance/source_manifest_v2.json").read_text())
    mismatches = []
    for entry in release["release_files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            mismatches.append("missing:" + entry["path"])
            continue
        with path.open("rb") as stream:
            actual = digest_stream(stream)
        if actual != (entry["sha256"], entry["size_bytes"]):
            mismatches.append("release:" + entry["path"])
    manifest_bytes = (ROOT / "provenance/source_manifest_v1.json").read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != update["base_manifest_sha256"]:
        mismatches.append("base manifest binding")
    base_by = {entry["path"]: entry for entry in base["files"]}
    update_entries = [e for e in update["files"] if e["storage"] == "UPDATE_V2"]
    update_entries += update["external_files"] + update["historical_files"]
    for entry in update["files"]:
        if entry["storage"] == "BASE_V1":
            old = base_by.get(entry["path"])
            if old is None or any(entry[key] != old[key] for key in ("sha256", "size_bytes", "archive")):
                mismatches.append("current source/base binding:" + entry["path"])
    checked = 0
    for manifest, entries in ((base, base["files"]), (update, update_entries)):
        for part in manifest["archives"]:
            path = ROOT / "reproducibility" / part["filename"]
            with path.open("rb") as stream:
                actual = digest_stream(stream)
            if actual != (part["sha256"], part["size_bytes"]):
                mismatches.append("archive bytes:" + part["filename"])
            expected = [e for e in entries if e["archive"] == part["filename"]]
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                if len(names) != len(set(names)) or set(names) != {e["path"] for e in expected}:
                    mismatches.append("archive inventory:" + part["filename"])
                for entry in expected:
                    try:
                        with archive.open(entry["path"]) as stream:
                            actual = digest_stream(stream)
                    except KeyError:
                        mismatches.append("missing archive member:" + entry["path"])
                        continue
                    if actual != (entry["sha256"], entry["size_bytes"]):
                        mismatches.append("archive member:" + entry["path"])
                    checked += 1
    print(json.dumps({
        "execution_state": "FAILED" if mismatches else "COMPLETED",
        "byte_authentication": "MISMATCH" if mismatches else "AUTHENTICATED_PACKAGED_BYTES",
        "release_files_checked": len(release["release_files"]),
        "archive_members_checked": checked,
        "current_source_files": len(update["files"]),
        "external_files": len(update["external_files"]),
        "historical_files": len(update["historical_files"]),
        "mismatches": mismatches,
        "scientific_calculations_rerun": False,
        "scientific_acceptance": "NOT_PERFORMED",
        "director_acceptance": "NOT_INFERRED",
    }, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
