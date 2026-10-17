#!/bin/sh
# The matrix: every mutant (and none) x the original suite and the generated one.
# usage: tools/run.sh EVIDENCE_DIR [mutant...]
set -u
OUT=$1; shift
M=${MOBIUM:-$HOME/mobium-public/bin/mobium}
MUTANTS=${*:-none msg terms-notify radio-sticky dark-stuck logout-keeps leaves-front}
for m in $MUTANTS; do
  tools/mutant.sh "$m" || exit 1
  trace=off; [ "$m" = none ] && trace=on
  for suite in ${SUITES:-corpus generated-withvalues}; do
    d=$OUT/$m/$suite
    mkdir -p "$d"
    "$M" test --config cfg-$suite.json --trace $trace --reporter list,json,junit,html --output "$d" > "$d/console.txt" 2>&1
    echo "$m $suite exit=$? $(tail -2 "$d/console.txt" | head -1)"
  done
done
tools/mutant.sh none
