#!/bin/sh
# Choose MobiumApp's mutant: mutant.sh <name>, or mutant.sh none.
# DEV names the device: an Android serial (default emulator-5554), written
# over `adb root` (the emulator's google_apis image allows it), or an iOS
# simulator's UDID, written into the app's data container on this Mac. The
# app reads the file once, as it starts, from its documents directory.
set -eu
DEV=${DEV:-emulator-5554}
PKG=dev.mobium.mobiumapp
case "$DEV" in
  *-*-*-*-*)  # a simulator's UDID
    xcrun simctl terminate "$DEV" $PKG 2>/dev/null || true
    D=$(xcrun simctl get_app_container "$DEV" $PKG data)/Documents
    mkdir -p "$D"
    if [ "$1" = none ]; then rm -f "$D/roundtrip-mutant.txt"; else echo "$1" > "$D/roundtrip-mutant.txt"; fi
    got=$(cat "$D/roundtrip-mutant.txt" 2>/dev/null || true)
    ;;
  *)
    F=/data/data/$PKG/files/roundtrip-mutant.txt
    adb -s "$DEV" shell am force-stop $PKG
    if [ "$1" = none ]; then
      adb -s "$DEV" shell rm -f $F
    else
      uid=$(adb -s "$DEV" shell stat -c %u /data/data/$PKG | tr -d '\r')
      adb -s "$DEV" shell "echo $1 > $F && chown $uid:$uid $F && chmod 600 $F"
    fi
    got=$(adb -s "$DEV" shell "cat $F 2>/dev/null" | tr -d '\r')
    ;;
esac
# Read it back rather than believe the write.
want=$1; [ "$want" = none ] && want=""
[ "$got" = "$want" ] || { echo "mutant file reads '$got', wanted '$want'" >&2; exit 1; }
echo "mutant: $1"
