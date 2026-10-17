#!/bin/sh
# The branch case: camera.py run with the prompt and without, each trace
# turned into a test by gen.py, and every test run in both states.
# usage: tools/branch.sh EVIDENCE_DIR
set -u
OUT=$1
M=${MOBIUM:-$HOME/mobium-public/bin/mobium}
APP=dev.mobium.mobiumapp
export MOBIUM_BIN_PATH=$M PYTHONPATH=$HOME/mobium-public/clients/python
mkdir -p "$OUT" generated/branch
state() {  # prompt | granted
  if [ "$1" = prompt ]; then "$M" reset-permissions $APP >/dev/null; else "$M" grant $APP camera >/dev/null; fi
  # Read it back rather than believe the command.
  echo "state: $1 ($(adb -s emulator-5554 shell dumpsys package $APP | grep 'android.permission.CAMERA: granted' | head -1 | tr -s ' '))"
}
for s in prompt granted; do
  state $s
  python3 corpus-branch/camera.py "$OUT/original-$s.zip" > "$OUT/original-$s.txt" 2>&1
  echo "original script, state $s: exit=$?"
done
for s in prompt granted; do
  python3 tools/gen.py generated/branch/from-$s.test.json "$OUT/original-$s.zip"
done
echo '{"testDir": "generated/branch", "projects": [{"name": "android", "device": "emulator-5554"}]}' > cfg-branch.json
for s in prompt granted; do
  state $s
  for t in from-prompt from-granted ${EXTRA:-}; do
    d=$OUT/run-$t-in-$s
    "$M" test --config cfg-branch.json generated/branch/$t.test.json --reporter list,json,junit --output "$d" > "$d.txt" 2>&1
    echo "test $t, state $s: exit=$? $(grep -E '^\s+(ok|x|fail)' "$d.txt" | head -1 | cut -c1-160)"
    [ "$s" = granted ] || state $s >/dev/null   # each run in the prompt state starts undecided
  done
done
