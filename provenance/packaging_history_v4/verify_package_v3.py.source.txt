"""Authenticate the complete publication and source chain; no scientific execution."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CURRENT_SOURCE = "source_manifest_v3.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest_stream(stream):
    digest = hashlib.sha256()
    size = 0
    for data in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(data)
        size += len(data)
    return digest.hexdigest(), size


def source_layers():
    layers = []
    filename = CURRENT_SOURCE
    seen = set()
    while filename:
        if filename in seen or Path(filename).name != filename:
            raise ValueError("Invalid source-manifest ancestry")
        seen.add(filename)
        path = ROOT / "provenance" / filename
        manifest = read_json(path)
        layers.append((filename, manifest))
        filename = manifest.get("previous_manifest", manifest.get("base_manifest"))
        if filename:
            data = (ROOT / "provenance" / filename).read_bytes()
            expected = manifest.get("previous_manifest_sha256", manifest.get("base_manifest_sha256"))
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("Source-manifest ancestry hash mismatch: " + filename)
    return list(reversed(layers))


def main():
    release = read_json(ROOT / "provenance/publication_manifest_v3.json")
    layers = source_layers()
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
    checked = 0
    previous = {}
    for filename, manifest in layers:
        entries = manifest["files"] + manifest.get("external_files", []) + manifest.get("historical_files", [])
        own_archives = {part["filename"] for part in manifest["archives"]}
        current = {}
        for entry in entries:
            if entry["path"] in current:
                mismatches.append("duplicate current-view path:" + entry["path"])
            current[entry["path"]] = entry
            if entry["archive"] not in own_archives:
                prior = previous.get(entry["path"])
                if prior is None or any(entry[key] != prior[key] for key in ("sha256", "size_bytes", "archive")):
                    mismatches.append("inherited source binding:" + entry["path"])
        for part in manifest["archives"]:
            path = ROOT / "reproducibility" / part["filename"]
            with path.open("rb") as stream:
                if digest_stream(stream) != (part["sha256"], part["size_bytes"]):
                    mismatches.append("archive bytes:" + part["filename"])
            expected = [entry for entry in entries if entry["archive"] == part["filename"]]
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
        previous = current
    current = layers[-1][1]
    print(json.dumps({
        "execution_state": "FAILED" if mismatches else "COMPLETED",
        "byte_authentication": "MISMATCH" if mismatches else "AUTHENTICATED_PACKAGED_BYTES",
        "release_files_checked": len(release["release_files"]),
        "source_manifest_layers": len(layers),
        "archive_members_checked": checked,
        "current_source_files": len(current["files"]),
        "external_files": len(current["external_files"]),
        "historical_files": len(current["historical_files"]),
        "mismatches": mismatches,
        "scientific_calculations_rerun": False,
        "scientific_acceptance": "NOT_PERFORMED",
        "director_acceptance": "NOT_INFERRED",
    }, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
