# Probe 4, follow-up: `slow-catalog` after every reset — 2026-10-17

Probe 4 (`../2026-10-16-morpho/RESULTS.md`) found every Android
difference under one bug, `slow-catalog`, whose 8-second delay came
only the first time a store showed the catalog. This follow-up makes the
bug fire after every reset, logs the app's process id, and re-runs that
row on both platforms.

**The change** (Morpho Market `slow-catalog-every-reset`, `b658e0e`,
mobiumdev/morpho-market#1): `reset()` clears `catalogShown` and counts itself, and the
catalog loads again on the count (`remember`/`LaunchedEffect` keyed on
it on Android, `.task(id:)` on iOS). The process id is on the bug screen
(`testid=processId`) and logged as `process N: store made` and
`process N: reset` (logcat tag `MorphoMarket`; subsystem
`dev.mobium.shop`). Same devices and Mobium (`bfcb09f`) as probe 4.

## 1. Every test starts in a new process

The runner terminates and launches the app before every test of a file
that names its `app` (Mobium `internal/testrun/run.go`, `runOnce`). The
logs show it worked every time:

| | resets | each just after a new store, ~1 s earlier |
|---|---|---|
| Android (`android-process.log`) | 206 | 205; the other is a hand check of two resets in one process |
| iOS (`ios-process.log`) | 204 | 204 |

So process survival was not what let some Android tests pass under
`slow-catalog` in probe 4, at least not today. The old build
(`229111e`) run twice more on Android under `slow-catalog`, with
ActivityManager's log: 25 of 25 failed both times, and the app's process
started before every test (`old-build/`). The three passes of probe 4
did not reproduce in 50 tries, and their cause is unknown. One
candidate, not measured: the runner ignores `app_terminate`'s error, so
a terminate that failed would leave the old store running.

## 2. The re-run

| Suite | Android: no bug | Android: `slow-catalog` failed | iOS: no bug | iOS: `slow-catalog` failed |
|---|---|---|---|---|
| original | 25 passed | 25 of 25 | 25 passed | 25 of 25 |
| table | 25 passed | 25 of 25 | 25 passed | 25 of 25 |
| Sonnet 5.5 | 25 passed | 25 of 25 | 25 passed | 25 of 25 |
| Haiku 5.5 | 27 passed | 27 of 27 | 27 passed | 27 of 27 |

Every failure is the catalog wait, `testid=catalogList`, at 3 seconds.
**Under `slow-catalog` every suite now agrees with the original on
every cell, on both platforms**: 0 lost, 0 extra. With probe 4's other
15 bugs unchanged, the round trip lost nothing on Morpho Market.

## 3. The first version of the fix broke the bug on iOS

The first iOS run (`ios-first-fix/`) passed `slow-catalog` 25 of 25, in
the original and the table suites: the bug was gone. A reset changes the
task's id, SwiftUI cancels the running task, and `try? await
Task.sleep` returns at once when canceled, so the old task went on to
show the catalog and mark it shown. Android's `delay` throws when
canceled and was not affected. A canceled sleep now returns without
touching anything. The matrix's no-bug control could not have caught
this; only a bug run that should fail could.

## What came of it

| Finding | Bucket | Status |
|---|---|---|
| `slow-catalog`'s verdict depended on the store being new | Morpho Market | fixed, `b658e0e`, mobiumdev/morpho-market#1 |
| A canceled SwiftUI task showed the catalog early | Morpho Market | fixed in the same commit, found by the matrix |
| The runner gives every test a new process, on both platforms | — | measured: 205 of 205, 204 of 204 |
| Probe 4's three Android passes | unknown | not reproduced in 50; `app_terminate`'s ignored error is a candidate |
