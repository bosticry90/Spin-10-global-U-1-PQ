"""Reproduce the complete actual DH identity using only this bundle and stdlib."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import sys
import threading
import time

BUNDLE = Path(__file__).resolve().parent
sys.path.insert(0, str(BUNDLE))
from exact_algebra import Algebra, ONE, SQUARES, combine, multiply_coefficients, parse_coefficient, require, scale


def read_json(path, maximum=64 * 1024**2):
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as stream:
            raw = stream.read(maximum + 1)
    else:
        raw = path.read_bytes()
    require(len(raw) <= maximum, "oversized JSON payload")
    return json.loads(raw)


def install_read_boundary():
    state = {"reference_open_allowed": False, "outside_attempts": []}
    runtime_roots = {Path(sys.base_prefix).resolve(), Path(sys.prefix).resolve()}

    def audit(event, arguments):
        if event != "open" or not arguments or not isinstance(arguments[0], (str, bytes)):
            return
        path = Path(os.fsdecode(arguments[0])).resolve()
        mode = arguments[1] if len(arguments) > 1 else None
        flags = arguments[2] if len(arguments) > 2 else 0
        writing = isinstance(mode, str) and any(letter in mode for letter in "wax+")
        writing = writing or (type(flags) is int and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
        if writing:
            raise PermissionError("PILOT_WRITE_DENIED: " + str(path))
        if path == BUNDLE / "reference_result.json.gz" and not state["reference_open_allowed"]:
            raise PermissionError("REFERENCE_RESULT_OPENED_BEFORE_COMPUTATION")
        if not path.is_relative_to(BUNDLE) and not any(path.is_relative_to(root) for root in runtime_roots):
            state["outside_attempts"].append(str(path))
            raise PermissionError("UNDECLARED_OUTSIDE_READ: " + str(path))

    sys.addaudithook(audit)
    return state


def authenticate_files(manifest, include_reference=False):
    for name, expected in manifest["files_sha256"].items():
        relative = Path(name)
        require(not relative.is_absolute() and ".." not in relative.parts and relative.name == name, "invalid bundle path")
        path = BUNDLE / relative
        require(path.is_file(), "missing payload: " + name)
        if name == "reference_result.json.gz" and not include_reference:
            continue
        require(sha256(path.read_bytes()).hexdigest() == expected, "altered bundle file: " + name)


def fixtures(algebra):
    for mask in range(32):
        first = (((0, 0, mask), Fraction(1)),)
        squared = multiply_coefficients(first, first)
        expected = 1
        for bit, prime in enumerate(SQUARES):
            if mask & (1 << bit):
                expected *= prime
        require(squared == (((0, 0, 0), Fraction(expected)),), "radical square fixture")
        for other in range(32):
            second = (((0, 0, other), Fraction(1)),)
            require(multiply_coefficients(first, second) == multiply_coefficients(second, first), "radical product fixture")
    require(parse_coefficient("I**2 + sqrt(7)**2 - 6") == (), "exact parser fixture")
    for text in ("0.5", "__import__('os')", "sqrt(11)", "g10**xi", "1/xi", "sqrt(xi)"):
        try:
            parse_coefficient(text)
        except (ValueError, SyntaxError, ZeroDivisionError):
            pass
        else:
            raise ValueError("invalid expression accepted: " + text)
    word = tuple(algebra.token(name) for name in ("C0", "ub12", "x_Phi_0"))
    polynomial = {(1, word): ONE}
    images = {algebra.index["ub12"]: algebra.index["zz_da12"]}
    right = algebra.action(polynomial, images, "slot")
    require(right == algebra.action(polynomial, images, "left"), "even versus left fixture")
    require(right != algebra.action(polynomial, images, "slot", wrong_odd=True), "odd prefix fixture insensitive")
    require(algebra.canonical((word[0], word[0]))[1] == 0, "Grassmann nilpotence fixture")
    return True


def parse_inputs(data):
    geometry = data["geometry"]
    algebra = Algebra(geometry["names"], geometry["parities"])
    pairs = geometry["field_source_h_k"]
    require(len(pairs) == 643 and len({row[0] for row in pairs}) == 643 and len({row[1] for row in pairs}) == 643, "incomplete canonical pairs")
    fields = {row[0] for row in pairs}
    sources = {row[1] for row in pairs}
    require(not fields & sources, "field/source overlap")
    h = {field: hh for field, source, hh, kk in pairs}
    k = {field: kk for field, source, hh, kk in pairs}
    eps = geometry["epsilon_ids"]
    require(len(eps) == 45 and all(algebra.names[n] == f"zz_da{i:02}" for i, n in enumerate(eps)), "wrong epsilon carrier")
    anti = {algebra.index[f"ub{i}"]: eps[i] for i in range(12, 45)}
    for field, source, hh, kk in pairs:
        require(algebra.names[hh] == "zz_h_" + algebra.names[field] and algebra.names[kk] == "zz_k_" + algebra.names[field], "wrong tangent map")
        require(algebra.parities[field] == algebra.parities[hh] == algebra.parities[kk] and algebra.parities[source] == 1 - algebra.parities[field], "wrong pair parity")
    gf = algebra.rows(data["gauge_fixing_density"])
    breaking = algebra.rows(data["classical_sourcefree_breaking"], True)
    mixed = algebra.rows(data["complete_mixed_Hessian_insertion"], True)
    master_raw = data["master_field_maps"]
    require(set(master_raw) == {algebra.names[field] for field in fields}, "missing master field column")
    master = {source: algebra.rows(master_raw[algebra.names[field]]) for field, source, hh, kk in pairs}
    kernels = {algebra.index[name]: algebra.rows(rows, True) for name, rows in data["all33_kernel_maps"].items()}
    require(len(kernels) == 479 and sum(map(len, kernels.values())) == 2589, "incomplete kernels")
    require(set(kernels) <= sources, "kernel is not a source column")
    for source, polynomial in kernels.items():
        for (g, word), value in polynomial.items():
            require(g in (0, 1) and sum(n in set(eps[12:]) for n, jets in word) == 1, "invalid kernel word")
            require(sum(algebra.parities[n] for n, jets in word) % 2 == algebra.parities[source], "kernel parity mismatch")
    hashes = {
        "GF": algebra.fingerprint(gf),
        "B": algebra.fingerprint(breaking),
        "C": algebra.fingerprint(mixed),
        "R": {algebra.names[source]: algebra.fingerprint(value) for source, value in master.items()},
        "V": {algebra.names[source]: algebra.fingerprint(value) for source, value in kernels.items()},
    }
    require(hashes == data["established_engine_input_hashes"], "raw-input transcription differs from qualified operands")
    return algebra, gf, breaking, mixed, master, kernels, anti, h, k, eps


def reproduce(data, method):
    algebra, gf, breaking, mixed, master, kernels, anti, h, k, eps = parse_inputs(data)
    fixtures(algebra)
    print("STAGE portable complete_actual_inputs_and_exact_fixtures", flush=True)
    breaking_hessian = algebra.action(algebra.action(breaking, h, method), k, method)
    assembled = combine(breaking_hessian, mixed)
    direct_gf = algebra.action(algebra.action(algebra.action(gf, anti, method), h, method), k, method)
    source = {}
    for source_id, kernel in kernels.items():
        second = algebra.action(algebra.action(master[source_id], h, method), k, method)
        if second:
            source = combine(source, algebra.product(kernel, second))
    direct = combine(direct_gf, scale(source, -1))
    require(direct == assembled, "complete action Hessian identity failed")
    require(assembled != breaking_hessian and assembled != mixed and bool(source), "actual omission controls insensitive")
    require(algebra.action(gf, anti, "slot", wrong_odd=True) != algebra.action(gf, anti, method), "actual wrong-prefix control insensitive")
    for g, word in assembled:
        require(sum(algebra.names[n].startswith("zz_h_") for n, jets in word) == 1 and sum(algebra.names[n].startswith("zz_k_") for n, jets in word) == 1, "missing fluctuation direction")
        require(sum(n in set(eps[12:]) for n, jets in word) == 1, "missing broken direction")
    per = [{
        "g": g,
        "breaking_hessian_positions": sum(order == g for order, word in breaking_hessian),
        "mixed_positions": sum(order == g for order, word in mixed),
        "complete_DH_positions": sum(order == g for order, word in assembled),
        "direct_GF_antighost_positions": sum(order == g for order, word in direct_gf),
        "source_master_correction_positions": sum(order == g for order, word in source),
    } for g in range(4)]
    census = Counter((g, tuple(sorted(algebra.names[n][5:][0] for n, jets in word if algebra.names[n].startswith(("zz_h_", "zz_k_")))), sum(len(jets) for n, jets in word)) for g, word in assembled)
    return algebra, assembled, source, per, [[g, list(pair), jets, count] for (g, pair, jets), count in sorted(census.items())]


def main():
    require(__debug__, "optimized execution would disable historical-style assertions; use ordinary Python")
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--method", choices=("slot", "left"), default="slot")
    arguments.add_argument("--probe-outside", help=argparse.SUPPRESS)
    args = arguments.parse_args()
    started = time.perf_counter()
    timer = threading.Timer(180, lambda: os._exit(124))
    timer.daemon = True
    timer.start()
    boundary = install_read_boundary()
    if args.probe_outside:
        Path(args.probe_outside).read_bytes()
        raise ValueError("outside read unexpectedly accepted")
    manifest = read_json(BUNDLE / "manifest.json", 1024**2)
    require(manifest["schema"] == "PORTABLE_COMPLETE_DH_BUNDLE_V1", "wrong bundle")
    authenticate_files(manifest)
    data = read_json(BUNDLE / "inputs.json.gz")
    algebra, actual, source, per, census = reproduce(data, args.method)
    actual_hash = algebra.fingerprint(actual)
    print("STAGE portable whole99256_identity_computed_before_reference_open", flush=True)
    boundary["reference_open_allowed"] = True
    authenticate_files(manifest, include_reference=True)
    reference = read_json(BUNDLE / "reference_result.json.gz")
    receipt_bytes = gzip.decompress((BUNDLE / "upstream_receipt.json.gz").read_bytes())
    require(sha256(receipt_bytes).hexdigest() == manifest["upstream_receipt_sha256"], "upstream receipt bytes changed")
    receipt = json.loads(receipt_bytes)
    require(receipt["execution_state"] == "COMPLETED" and receipt["actual_DH_positions"] == 99256, "unqualified upstream reference")
    require(actual == algebra.decode_compact(reference["whole_actual_DH_compact"]), "whole reference tensor differs")
    require(actual_hash == receipt["actual_DH_sha256_exact_cells"] == reference["whole_actual_DH_sha256_exact_cells"], "reference hash differs")
    require(per == reference["complete_Hessian_order_census"] and census == reference["field_pair_jet_census"], "incomplete order or jet coverage")
    require(algebra.fingerprint(source) == reference["actual_source_correction_sha256_exact_cells"], "source Hessian correction differs")
    require(not boundary["outside_attempts"], "outside dependency attempted")
    result = {
        "schema": "PORTABLE_COMPLETE_DH_REPRODUCTION_V1",
        "execution_state": "COMPLETED",
        "method": args.method,
        "complete_actual_DH_positions": len(actual),
        "complete_actual_DH_sha256": actual_hash,
        "whole_order_census": per,
        "every_coefficient_and_implicit_zero_matches": True,
        "all_packaged_inputs_match_established_engine": True,
        "all643_field_maps_all33_directions_and_jets_retained": True,
        "reference_opened_after_complete_computation": True,
        "unexpected_outside_reads": [],
        "workspace_writes": 0,
        "runtime_dependencies": "Python standard library and this closed bundle only",
        "python": sys.version,
        "platform": platform.platform(),
        "elapsed_after_imports": time.perf_counter() - started,
        "scope": "Complete classical DH identity; upstream physical/action interpretation inherited",
        "new_UV_loop_QAP_contact_or_E5_acceptance": False,
    }
    print("RESULT " + json.dumps(result, sort_keys=True, separators=(",", ":")), flush=True)
    timer.cancel()


if __name__ == "__main__":
    main()
