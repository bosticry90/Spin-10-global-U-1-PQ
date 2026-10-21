"""Verify release, then assemble its current source view in an empty directory."""
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import zipfile
from verify_package import ROOT, CURRENT_SOURCE, main as verify


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -B reproducibility/assemble_source.py NEW_EMPTY_DIRECTORY")
    target = Path(sys.argv[1]).resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise SystemExit("Destination must be new or empty; no files were modified.")
    if verify():
        raise SystemExit("Package verification failed; no files were extracted.")
    manifest = json.loads((ROOT / "provenance" / CURRENT_SOURCE).read_text(encoding="utf-8"))
    entries = manifest["files"] + manifest["external_files"] + manifest["historical_files"]
    for entry in entries:
        relative = PurePosixPath(entry["path"])
        out = (target / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not out.is_relative_to(target):
            raise SystemExit("Unsafe manifest path: " + entry["path"])
    target.mkdir(parents=True, exist_ok=True)
    grouped = {}
    for entry in entries:
        grouped.setdefault(entry["archive"], []).append(entry)
    for filename, members in grouped.items():
        with zipfile.ZipFile(ROOT / "reproducibility" / filename) as archive:
            for entry in members:
                out = target / entry["path"]
                out.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(entry["path"]) as source, out.open("xb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
    print(json.dumps({"execution_state": "COMPLETED", "destination": str(target),
                      "files_written": len(entries), "scientific_acceptance": "NOT_PERFORMED"}))


if __name__ == "__main__":
    main()
