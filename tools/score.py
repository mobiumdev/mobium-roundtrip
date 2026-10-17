"""Score the matrix: does the generated suite catch the same mutants as the original?

Reads <matrix>/<mutant>/<suite>/junit.xml and prints, per test, which suite
failed under which mutant. A cell where the original fails and the generated
passes is a bug the round trip lost; the reverse is a test that fails for a
reason the original does not have. Under "none" both must pass, or nothing
else in the table means anything.

usage: SUITES="corpus <generated suite>" python3 score.py MATRIX_DIR
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

SUITES = tuple(os.environ.get("SUITES", "corpus generated-withvalues").split())


def results(path):
    out = {}
    for tc in ET.parse(path).getroot().iter("testcase"):
        name = re.sub(r" \[\d+\]$", "", tc.get("name"))
        out[name] = "fail" if tc.find("failure") is not None or tc.find("error") is not None else "pass"
    return out


def main(matrix):
    mutants = sorted(os.listdir(matrix), key=lambda m: (m != "none", m))
    table = {m: {s: results(os.path.join(matrix, m, s, "junit.xml")) for s in SUITES}
             for m in mutants if os.path.isdir(os.path.join(matrix, m))}
    tests = sorted(table["none"][SUITES[0]])
    lost = extra = agree_kill = 0
    print("mutant          | test | original | generated")
    for m, r in table.items():
        killed_o = killed_g = False
        for t in tests:
            o, g = r[SUITES[0]].get(t, "missing"), r[SUITES[1]].get(t, "missing")
            mark = ""
            if m != "none":
                if o == "fail" and g == "pass":
                    mark, lost = "  <-- lost", lost + 1
                elif o == "pass" and g == "fail":
                    mark, extra = "  <-- extra", extra + 1
                elif o == g == "fail":
                    agree_kill += 1
            elif o != "pass" or g != "pass":
                mark = "  <-- control failed"
            killed_o |= o == "fail"
            killed_g |= g == "fail"
            if o == "fail" or g == "fail" or mark:
                print(f"{m:15} | {t} | {o} | {g}{mark}")
        if m != "none":
            print(f"{m:15} | killed by original: {killed_o}, by generated: {killed_g}")
    print(f"\ncells where both fail: {agree_kill}; lost by the round trip: {lost}; failing only when generated: {extra}")


if __name__ == "__main__":
    main(sys.argv[1])
