"""Turn traces into the text an agent is given: each trace's title and its
calls, with arguments and the result's text, no screenshots and no maps.
The player's own keys are dropped, as gen.py drops them.

usage: python3 digest.py TRACE.zip... > digest.txt
"""
import json
import sys
import zipfile

PLAYER_KEYS = {"device", "driver", "selector", "value"}

for path in sys.argv[1:]:
    with zipfile.ZipFile(path) as z:
        events = [json.loads(l) for l in z.read("trace.trace").decode().splitlines() if l.strip()]
    title = next(e["title"] for e in events if e.get("type") == "context-options")
    after = {e["callId"]: e for e in events if e.get("type") == "after"}
    print(f"## trace: {title}")
    for e in (e for e in events if e.get("type") == "before"):
        params = {k: v for k, v in e.get("params", {}).items() if k not in PLAYER_KEYS}
        a = after.get(e["callId"], {})
        out = a.get("error", {}).get("message") if a.get("error") else a.get("result", "")
        out = " ".join(str(out).split())[:240]
        print(f"- {e['method'].removeprefix('mobium:')} {json.dumps(params, ensure_ascii=False)}")
        print(f"  -> {'ERROR ' if a.get('error') else ''}{out}")
    print()
