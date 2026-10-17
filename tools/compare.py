"""Compare two runs' traces, test by test: did the generated test do what the original did?

A call matches when its tool and arguments are the same (less the keys the
trace adds for its player) and its result is the same once timings,
coordinates and refs are taken out. Prints one line per test and every
difference.

usage: python3 compare.py ORIGINAL_REPORT_DIR GENERATED_REPORT_DIR
"""
import glob
import json
import os
import re
import sys
import zipfile

PLAYER_KEYS = {"device", "driver", "selector", "value"}
NOISE = [
    (re.compile(r"after \d+(\.\d+)?m?s"), "after <t>"),
    (re.compile(r"at \(\d+, \d+\)"), "at (<x>, <y>)"),
    (re.compile(r"@e\d+"), "@e<n>"),
]


def trace_calls(zpath):
    with zipfile.ZipFile(zpath) as z:
        events = [json.loads(l) for l in z.read("trace.trace").decode().splitlines() if l.strip()]
    title = next(e["title"] for e in events if e.get("type") == "context-options")
    afters = {e["callId"]: e for e in events if e.get("type") == "after"}
    out = []
    for e in events:
        if e.get("type") != "before":
            continue
        a = afters.get(e["callId"], {})
        result = a.get("result", "") or ""
        if a.get("error"):
            result = "ERROR " + json.dumps(a["error"])
        for rx, sub in NOISE:
            result = rx.sub(sub, result)
        params = {k: v for k, v in e.get("params", {}).items() if k not in PLAYER_KEYS}
        out.append((e["method"].removeprefix("mobium:"), params, result))
    return title.split(" › ", 1)[-1], out


def by_test(report):
    tests = {}
    for z in glob.glob(os.path.join(report, "artifacts", "trace", "*", "trace.zip")):
        name, calls = trace_calls(z)
        tests[re.sub(r" \[\d+\]$", "", name)] = calls
    return tests


def main(orig_dir, gen_dir):
    orig, gen = by_test(orig_dir), by_test(gen_dir)
    same = 0
    for name in sorted(set(orig) | set(gen)):
        a, b = orig.get(name), gen.get(name)
        if a is None or b is None:
            print(f"MISSING  {name}: only in {'original' if b is None else 'generated'}")
            continue
        diffs = []
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else None
            y = b[i] if i < len(b) else None
            if x != y:
                diffs.append(f"    call {i + 1}:\n      original:  {x}\n      generated: {y}")
        if diffs:
            print(f"DIFFERS  {name} ({len(a)} calls vs {len(b)})")
            print("\n".join(diffs))
        else:
            same += 1
            print(f"SAME     {name} ({len(a)} calls)")
    print(f"{same} of {len(set(orig) | set(gen))} tests made the same calls with the same results")


if __name__ == "__main__":
    main(*sys.argv[1:3])
