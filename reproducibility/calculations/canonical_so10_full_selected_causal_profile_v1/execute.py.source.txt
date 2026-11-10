"""Freeze and review the V915 evidence in the active D: workspace."""

import ast
import json
import os
import subprocess
import sys
import threading
import time
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTROL = Path("D:/Codex-Research/ToE-Next/research-control-records/full-selected-causal-profile-v1-2026-11-09")
PK = ROOT / "tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1"
BASE = "caa0b472c005c5b486ee866ef265b4d5bbff1e85"
NAV = ["README.md", "docs/COMMON_RESTORATION_CAMPAIGN_V1.md", "docs/RESEARCH_EXECUTION_HANDOFF_V915.md"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(name, data):
    raw = (json.dumps(data, sort_keys=True) + "\n").encode()
    if len(raw) > 8 * 1024**2:
        name += ".COMPLETE_OVERFLOW_NOTPASS"
    for folder in (HERE, CONTROL):
        with (folder / name).open("xb") as f:
            f.write(raw)
    assert len(raw) <= 8 * 1024**2


def prepare(phase):
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert not git("diff", "--cached", "--name-only")
    if phase == "native":
        assert not git("diff", "--name-only", "HEAD")
        CONTROL.mkdir(exist_ok=False)
        with (CONTROL / "old_git_tree.txt").open("xb") as f:
            f.write(git("ls-tree", "-r", "HEAD"))
        snapshots = ("RECORD.md", "PROOF.md", "causal_profile.py", "execute.py")
        owners = {
            "mixed_w_transport_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "gauge_endpoint_profiles_v1": ("PROOF.md", "validation_receipt.json"),
            "joint_internal_simple_switch_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "internal_massive_switch_v2": ("PROOF.md", "validation_receipt.json"),
            "unit_plateau_feynman_v2": ("PROOF.md", "validation_receipt.json"),
            "exact_outer_ghost_group_v1": ("PROOF.md", "validation_receipt.json"),
            "switched_massive_bridge_v1": ("PROOF.md", "validation_receipt.json"),
            "dressed_exterior_profile_v1": ("PROOF.md", "validation_receipt.json"),
            "ghost_two_color_transition_v2": ("PROOF.md", "validation_receipt.json"),
            "causal_one_loop_sewing": ("DERIVATION.md", "validation_receipt.json"),
        }
        names = {"AGENTS.md", "CHARTER.md", "project_state.json",
                 "docs/RESEARCH_EXECUTION_HANDOFF_V914.md"}
        names.add((PK / "export_a10_e5_antighost_vector.py").relative_to(ROOT).as_posix())
        for owner, paths in owners.items():
            names.update(f"calculations/canonical_so10_{owner}/{path}" for path in paths)
    else:
        assert phase == "validation"
        assert set(git("diff", "--name-only", "HEAD").decode().splitlines()) == set(NAV[:2])
        for name, backup in zip(NAV[:2], ("README_before_final.bytes", "campaign_before_final.bytes")):
            assert (CONTROL / backup).read_bytes().replace(b"\r\n", b"\n") == git("show", "HEAD:" + name)
        first = read(HERE / "preparation_native.json")
        for name, expected in first["sha256"].items():
            assert digest(ROOT / name) == expected, name
        names = set(first["sha256"]) | set(NAV) | {"docs/LOCAL_RESEARCH_CONVENTIONS_V1.md"}
        snapshots = ("RESULT.md",)
    for name in snapshots:
        raw = (HERE / name).read_bytes()
        if name.endswith(".py"):
            ast.parse(raw)
        with (HERE / (name + ".source.txt")).open("xb") as f:
            f.write(raw)
    names.update(path.relative_to(ROOT).as_posix() for path in HERE.iterdir() if path.is_file())
    save(f"preparation_{phase}.json", {
        "base_HEAD": BASE, "sha256": {name: digest(ROOT / name) for name in sorted(names)},
        "scientific_acceptance": "NOT_PERFORMED",
        "limits": {"seconds": 120 if phase == "native" else 180, "e4_seconds": 120,
                   "sampled_private_bytes": 8 * 1024**3, "minimum_available_commit_bytes": 350 * 1024**2,
                   "artifact_bytes": 8 * 1024**2, "packet_bytes": 32 * 1024**2},
    })


def run_worker(check, phase):
    started = time.perf_counter()
    prep = read(HERE / f"preparation_{phase}.json")
    timer = threading.Timer(prep["limits"]["seconds"], lambda: os._exit(124))
    timer.daemon = True
    timer.start()
    assert git("rev-parse", "HEAD").decode().strip() == BASE == prep["base_HEAD"]
    for name, expected in prep["sha256"].items():
        assert digest(ROOT / name) == expected, name
    if phase == "native":
        save("result.json", {"execution_state": "COMPLETED", "checks": check("native")})
        print("STAGE full selected causal profile controls checked", flush=True)
    else:
        review(check, prep, started)
    timer.cancel()


def review(check, prep, started):
    assert not git("diff", "--cached", "--name-only")
    assert git("ls-tree", "-r", "HEAD") == (CONTROL / "old_git_tree.txt").read_bytes()
    for name in ("preparation_native.json", "capture_native.json", "result.json"):
        assert (HERE / name).read_bytes() == (CONTROL / name).read_bytes()
    cap = read(HERE / "capture_native.json")
    assert cap["calculation_completed"] and cap["post_run_observations_qualified"]
    for source in HERE.glob("*.source.txt"):
        assert source.read_bytes() == (HERE / source.name.removesuffix(".source.txt")).read_bytes()
    owners = sorted(n for n in prep["sha256"] if "validation_receipt" in Path(n).name and n.endswith(".json"))
    for name in owners:
        owner = read(ROOT / name)
        if "execution_state" in owner:
            assert owner["execution_state"] == "COMPLETED", name
        else:
            assert owner["status"].startswith("PASS_BOUNDED_"), name
    result = read(HERE / "result.json")
    assert result["execution_state"] == "COMPLETED"
    checks = result["checks"]
    assert checks == check("replay")
    assert checks["exponents"]["minimum_extra_mixed_degree"] == 2
    assert checks["kinetic"]["original_two_switch_forest_retained"]
    assert checks["reference_combination"] == "300*log(M_Sigma/M_Phi)"
    print("STAGE full selected causal profile replay agrees", flush=True)

    command = [sys.executable, "-B", "tools/research_check.py", "e4", "--historical-context",
               "D:/Codex-Research/ToE-Next/research-evidence/e4-context-v4"]
    try:
        e4 = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120)
    except subprocess.TimeoutExpired as err:
        save("e4_timeout.json", {"command": command, "state": "INCOMPLETE_TIMEOUT",
                                 "stdout": (err.stdout or b"").decode("utf-8", errors="replace"),
                                 "stderr": (err.stderr or b"").decode("utf-8", errors="replace")})
        raise
    save("e4_capture.json", {"exit_code": e4.returncode, "stdout": e4.stdout, "stderr": e4.stderr})
    events = [json.loads(line) for line in e4.stdout.splitlines() if line.strip()]
    steps = [event for event in events if event.get("event") == "step_finished"]
    exits = [event["exit_code"] for event in steps]
    assert e4.returncode == 0 and exits == [0, 0, 0, 0, 0, 2]
    custody = next(event for event in steps if event["step"] == "historical_custody")
    assert custody["stdout"].count("RECORDED_DIGEST_UNRESOLVED:") == 7
    hist = git("show", "ef70f255a667b9a81e37b344dc78967ada4ed896:README.md")
    assert sha256(hist).hexdigest() == "4a00e15665bebfc23fb0ae9338770c22d1260610bde6435415c09e21a5a43792"
    assert (ROOT / "README.md").read_bytes().replace(b"\r\n", b"\n").endswith(hist)
    state = digest(ROOT / "project_state.json")
    assert state == "d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8"
    for name, expected in prep["sha256"].items():
        assert digest(ROOT / name) == expected, name
    files = [p for p in HERE.iterdir() if p.is_file()] + [ROOT / name for name in NAV]
    save("validation_receipt.json", {"base_HEAD": BASE, "execution_state": "COMPLETED",
         "evidence_validation": "PASS_FULL_SELECTED_CAUSAL_PROFILE_DEPENDENCE",
         "scientific_acceptance": "NOT_PERFORMED", "state_sha256": state,
         "E4_step_exits": exits, "historical_custody": "SEVEN_UNRESOLVED_NOTPASS", "owner_receipts": owners,
         "checks": checks,
         "files_excluding_pending_receipt_capture": {p.relative_to(ROOT).as_posix(): digest(p) for p in files},
         "elapsed_after_imports": time.perf_counter() - started})


def main():
    phase = sys.argv[1]
    prepare(phase)
    sys.path.insert(0, str(PK))
    from export_a10_e5_antighost_vector import capture

    report = capture([sys.executable, "-B", str(HERE / "causal_profile.py"), phase])
    save(f"capture_{phase}.json", report)
    print(report["stdout_and_stderr"], end="")
    assert report["calculation_completed"] and report["post_run_observations_qualified"]
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) <= 32 * 1024**2


if __name__ == "__main__":
    main()
