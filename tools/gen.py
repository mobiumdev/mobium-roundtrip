"""Generate a mobium test file from traces: the deterministic table, nothing inferred.

Each trace.zip becomes one test. A trace's calls become steps one for one:
the runner's own terminate-and-launch at the start becomes the file's "app",
and the keys the trace adds for its player (device, selector, value) are
dropped. Typed text is not in a trace — only its length — so it becomes a
placeholder, ${text_N}; a values file supplied from outside the trace can
fill it, and the output says which steps needed it.

usage: python3 gen.py OUT.test.json TRACE.zip... [--values values.json]
values.json: {"<test title>": {"text_1": "...", ...}}
"""
import json
import re
import sys
import zipfile

# The player's keys, and the device and driver the runner adds from its
# project config: a test names neither, so it runs on any project.
PLAYER_KEYS = {"device", "driver", "selector", "value", "assertion"}
NOT_RECORDED = re.compile(r"^\((\d+) characters, not recorded\)$")


def calls(trace_zip):
    with zipfile.ZipFile(trace_zip) as z:
        events = [json.loads(l) for l in z.read("trace.trace").decode().splitlines() if l.strip()]
    title = next(e["title"] for e in events if e.get("type") == "context-options")
    befores = [e for e in events if e.get("type") == "before"]
    return title, [(e["method"].removeprefix("mobium:"), e.get("params", {})) for e in befores]


def test_from(trace_zip, values):
    title, cs = calls(trace_zip)
    app = None
    if len(cs) >= 2 and cs[0][0] == "app_terminate" and cs[1][0] == "app_launch" \
            and cs[0][1].get("app") == cs[1][1].get("app"):
        app = cs[0][1]["app"]
        cs = cs[2:]
    steps, placeholders = [], []
    for name, params in cs:
        args = {k: v for k, v in params.items() if k not in PLAYER_KEYS}
        # An expect's reads carry what it asserts (Mobium since CHALLENGES
        # 327); the first attempt becomes the expect, the rest were its polls.
        a = params.get("assertion")
        if a is not None:
            if a.get("attempt", 1) > 1:
                continue
            e = {"tool": name, "arguments": args, "field": a["field"], "equals": a["equals"]}
            for k in ("not", "timeout_ms"):
                if k in a:
                    e[k] = a[k]
            step = {"expect": e}
            if a.get("soft"):
                step["soft"] = True
            steps.append(step)
            continue
        m = NOT_RECORDED.match(str(args.get("text", "")))
        if m:
            key = f"text_{len(placeholders) + 1}"
            placeholders.append({"key": key, "step": len(steps) + 1, "tool": name, "length": int(m.group(1))})
            args["text"] = "${" + key + "}"
        steps.append({"name": name, "arguments": args})
    test = {"name": title.split(" › ", 1)[-1], "steps": steps}
    if placeholders:
        supplied = values.get(test["name"])
        if supplied is None:
            test["description"] = "typed text not in the trace and not supplied: " + ", ".join(
                f"{p['key']} ({p['length']} characters, step {p['step']})" for p in placeholders)
        else:
            test["each"] = [{k: supplied[k] for k in (p["key"] for p in placeholders)}]
            test["description"] = "typed text supplied from outside the trace: " + ", ".join(
                p["key"] for p in placeholders)
    return app, test, placeholders


def main(argv):
    values = {}
    if "--values" in argv:
        i = argv.index("--values")
        values = json.load(open(argv[i + 1]))
        argv = argv[:i] + argv[i + 2:]
    out, traces = argv[0], argv[1:]
    apps, tests = set(), []
    for t in traces:
        app, test, _ = test_from(t, values)
        apps.add(app)
        tests.append(test)
    if len(apps) != 1 or None in apps:
        sys.exit(f"traces do not share one app launched fresh: {apps}")
    doc = {"description": "Generated from traces by tools/gen.py; nothing inferred.",
           "app": apps.pop(), "tests": tests}
    with open(out, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"{out}: {len(tests)} tests")


if __name__ == "__main__":
    main(sys.argv[1:])
