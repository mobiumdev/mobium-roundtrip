"""Write the values file gen.py and the agents need, from the original tests.

A trace keeps typed text only as its length, so the text has to come from
outside it. For MobiumApp it was written by hand (tools/values.json); for a
larger corpus it is read from the original test files: per test name, every
text a step typed (fill, type, keyboard), in order, as text_1, text_2, ...
That is the same information, taken mechanically, and nothing else.

usage: python3 values_from.py TEST.json... > values.json
"""
import json
import sys

TYPING = {"fill", "type", "keyboard"}

out = {}
for path in sys.argv[1:]:
    doc = json.load(open(path))
    pre = [s for s in doc.get("beforeEach", [])]
    for t in doc["tests"]:
        texts = []
        for s in pre + t["steps"]:
            if not isinstance(s, dict):
                continue
            for k in TYPING & s.keys():
                v = s[k]
                if isinstance(v, dict) and isinstance(v.get("text"), str):
                    texts.append(v["text"])
        if texts:
            out[t["name"]] = {f"text_{i + 1}": x for i, x in enumerate(texts)}
json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
print()
