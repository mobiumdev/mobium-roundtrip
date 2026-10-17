"""Build the prompts an agent is given, from their parts — probe 2's part 2
(the corpus) and part 3 (the branch).

  corpus: agent/prompt.md with VALUES (tools/values.json, typed text by test),
          DIGEST (tools/digest.py over the corpus traces) and GUIDE
          (agent/format.md, written for the probe: Mobium's own test-runner
          guide quotes the corpus and would hand over the answer).
  branch: the two traces of corpus-branch/camera.py, agent/format.md, and
          agent/tools.md — every tool's name, arguments and description.

usage: python3 agent_prompt.py corpus TRACE.zip...      > agent/prompt-filled.md
       python3 agent_prompt.py branch PROMPT.zip GRANTED.zip > agent/branch-prompt-filled.md
       python3 agent_prompt.py tools                     > agent/tools.md   (asks `mobium mcp`)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
M = os.environ.get("MOBIUM", os.path.expanduser("~/mobium-public/bin/mobium"))


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def digest(traces):
    return subprocess.run([sys.executable, os.path.join(HERE, "digest.py"), *traces],
                          capture_output=True, text=True, check=True).stdout


def corpus(traces):
    p = read("agent/prompt.md").replace("# The guide to the test format (Mobium's docs/guides/test-runner.md)",
                                        "# The test format")
    v = json.loads(read("tools/values.json"))
    vals = "\n".join(f"- {k}: " + ", ".join(json.dumps(x) for _, x in sorted(d.items())) for k, d in v.items())
    return p.replace("VALUES", vals).replace("DIGEST", digest(traces)).replace("GUIDE", read("agent/format.md"))


def branch(traces):
    return f"""You are given two traces of the same client script, run on an Android
emulator in two device states: once while the app's camera permission was
undecided, so Android showed its permission prompt, and once after it was
granted, so no prompt came. A trace lists every call the script made on the
device, with its arguments and what it answered. The script itself had a
conditional; a trace shows only the path that ran.

Write one Mobium test file — the format is below — that does what the script
did and passes in both states. A test file has no conditionals. Use only
the tools listed below, with their arguments as described.

Answer with one JSON object and nothing else, no prose and no code fence:
the test file's content.

# The traces

{digest(traces)}
# The test format

{read("agent/format.md")}
# The tools

{read("agent/tools.md")}
"""


def tools():
    msgs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "roundtrip", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]
    p = subprocess.Popen([M, "mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    for m in msgs:
        p.stdin.write(json.dumps(m) + "\n")
    p.stdin.flush()
    out = []
    for line in p.stdout:
        d = json.loads(line)
        if d.get("id") == 2:
            for t in d["result"]["tools"]:
                props = ", ".join(t["inputSchema"].get("properties", {}).keys())
                out.append(f"- {t['name']}({props}): {t['description']}")
            break
    p.kill()
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    kind, rest = sys.argv[1], sys.argv[2:]
    sys.stdout.write({"corpus": lambda: corpus(rest), "branch": lambda: branch(rest), "tools": tools}[kind]())
