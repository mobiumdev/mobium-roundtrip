"""The docs site's scenarios as a corpus: each one's setup and its command,
run through the CLI under `mobium trace`, exactly as scripts/capture.py runs
them for the reference pages (setups copied from its PLAN, commands from
examples/canonical.json). Only scenarios on Settings or MobiumApp that change
nothing device-wide.

Each trace is saved where compare.py looks, titled "docs.test.json › <tool>[i]".

usage: python3 docs_corpus.py OUT_DIR   (MOBIUM names the binary)
"""
import json
import os
import shlex
import subprocess
import sys

M = os.environ.get("MOBIUM", os.path.expanduser("~/mobium-public/bin/mobium"))
CANON = json.load(open(os.path.expanduser("~/mobium-docs/examples/canonical.json")))
SETTINGS, APP = "com.android.settings", "dev.mobium.mobiumapp"
settings_root = [f"terminate {SETTINGS}", f"launch {SETTINGS}"]


def app_screen(name):
    return [f"terminate {APP}", f"launch {APP}", f"tap 'text={name}'"]


SCENARIOS = [
    ("app_map", 0, settings_root),
    ("app_text", 0, settings_root),
    ("app_find", 0, settings_root),
    ("app_tap", 0, settings_root),
    ("app_scroll_to", 0, settings_root),
    ("app_scroll_to", 1, app_screen("Pager Demo") + ["wait 'label=Card 1'"]),
    ("app_swipe", 0, settings_root),
    ("app_press", 0, settings_root + ["tap 'text=Network & internet'", "wait text=Internet"]),
    ("app_check", 0, app_screen("Form Demo")),
    ("app_wait_for", 2, app_screen("Form Demo") + ["check testid=termsCheck"]),
    ("app_keyboard", 0, app_screen("Login Demo") + ["tap testid=username"]),
    ("app_alert", 1, app_screen("Dialog Demo") + ["tap 'text=Two-button alert'", "wait 'text=Discard changes?'"]),
    ("app_alert", 2, app_screen("Dialog Demo") + ["tap 'text=Three-button alert'", "wait 'text=Save this draft?'"]),
]


def run(cmd):
    argv = [M] + shlex.split(cmd)
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main(out):
    log = open(os.path.join(out, "console.txt"), "w")
    for tool, i, setup in SCENARIOS:
        name = f"{tool}[{i}]"
        cmd = CANON[tool][i]["cli"].removeprefix("mobium ")
        d = os.path.join(out, "artifacts", "trace", name)
        os.makedirs(d, exist_ok=True)
        run(f"trace start --name {shlex.quote('docs.test.json › ' + name)}")
        codes = [run(c)[0] for c in setup]
        code, text = run(cmd)
        run(f"trace stop -o {shlex.quote(os.path.join(d, 'trace.zip'))}")
        print(f"{name}: setup exits {codes}, `{cmd}` exit {code}", file=log)
        print(f"{name}: setup {codes} cmd {code}")
        if tool == "app_alert":
            run("alert dismiss")  # whatever is left up
    log.close()


if __name__ == "__main__":
    main(sys.argv[1])
