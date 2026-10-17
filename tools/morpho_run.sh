#!/bin/sh
# Probe 4's matrix: Morpho Market's bugs (and none) × the suites named in
# SUITES. A bug is switched by Morpho's own deep link, which every test's
# reset leaves alone, so it stays on for the whole run; every test starts
# from a reset store. The bugs are read from the app's source, as Morpho's
# own tests/matrix.sh reads them.
# usage: [DEV=<udid>] SUITES="morpho morpho-generated" tools/morpho_run.sh EVIDENCE_DIR [bug...]
#   DEV: the device the links go to (default emulator-5554); each suite's
#   config (cfg-<suite>.json) names the device the tests run on.
set -u
OUT=$1; shift
M=${MOBIUM:-$HOME/mobium-public/bin/mobium}
DEV=${DEV:-emulator-5554}
MORPHO=${MORPHO:-$HOME/morpho-market-public}
ON="--device $DEV"
case "$DEV" in *-*-*-*-*) ON="$ON --driver wda" ;; esac
BUGS=${*:-$(sed -n 's/^    Bug("\([a-z-]*\)".*/\1/p' "$MORPHO/android/shared/src/main/java/dev/mobium/shop/Bugs.kt")}
[ -n "$BUGS" ] || { echo "no bugs found" >&2; exit 1; }
TIMEOUT=${TIMEOUT:-1m}  # untraced, as Morpho's own matrix runs
for b in none $BUGS; do
  for suite in ${SUITES:?name the suites}; do
    # Every suite starts from the bug it is scored under: a test that
    # switched bugs itself cannot leak into the next suite's run.
    "$M" open "mobiumshop://bugs?off=all" $ON >/dev/null || exit 1
    [ "$b" = none ] || "$M" open "mobiumshop://bugs?on=$b" $ON >/dev/null || exit 1
    d=$OUT/$b/$suite
    mkdir -p "$d"
    "$M" test --config cfg-$suite.json --timeout "$TIMEOUT" --reporter list,junit --output "$d" > "$d/console.txt" 2>&1
    echo "$b $suite exit=$? $(tail -2 "$d/console.txt" | head -1)"
  done
done
"$M" open "mobiumshop://bugs?off=all" $ON >/dev/null
