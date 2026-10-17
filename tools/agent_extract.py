"""Write an agent's answer out as test files.

The answer (the `result` of `claude -p --output-format json`) is one JSON
object: for the corpus, file names to file contents; for the branch, one
test file's content. A code fence around it is tolerated and stripped.

usage: python3 agent_extract.py corpus OUT.json DIR      # one file per key
       python3 agent_extract.py branch OUT.json FILE.test.json
"""
import json
import os
import re
import sys

kind, out, dest = sys.argv[1:4]
d = json.load(open(out))
text = re.sub(r"^```(json)?\n|\n```$", "", d["result"].strip())
doc = json.loads(text)
if kind == "corpus":
    os.makedirs(dest, exist_ok=True)
    for name, content in doc.items():
        with open(os.path.join(dest, name), "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        print(os.path.join(dest, name))
else:
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    print(dest)
print(f"cost: ${d.get('total_cost_usd')}, model: {', '.join(d.get('modelUsage', {}))}")
