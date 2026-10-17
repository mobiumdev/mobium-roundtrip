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
`slow-catalog` in probe 4. The old build (`229111e`) run twice more on
Android under `slow-catalog`, with ActivityManager's log: 25 of 25
failed both times, and the app's process started before every test
(`old-build/`).

### The three passes were timing

`app_terminate` was a candidate: on Android it runs `am force-stop` and
reads nothing back, and the runner ignores its error. It was not the
cause. After every terminate measured here the package had no process,
and the logs above show a new one for every test.

In the old build the 8 seconds count from the catalog's first showing,
at launch, and a reset does not restart them. Every test's
`beforeEach` resets the store and waits 3 seconds, so a test passes if
its reset comes late enough after launch that the 8 seconds end inside
the wait. Measured by hand on the old build (terminate, launch, a
pause, reset, wait 3 s), with Android's own log for the time from
process start to the reset link:

| process start → reset | the wait |
|---|---|
| 1.61 s, 1.83 s | failed |
| 2.11 s, 2.61 s, 2.61 s, 2.97 s, 3.10 s, 3.11 s | passed |

The runner's own gap is about 1.3–1.9 s on this clock (`store made` →
`reset`, 1.01–1.55 s for 204 of 205 tests today, the store being made
a fraction of a second after the process starts). So the original test
sat just under a threshold of about 2 seconds, and any test whose steps
before the reset ran slow by half a second passed. Probe 4 ran both
matrices at once; three tests in each Android suite crossing it fits,
though their timings were not recorded. Today's old-build runs
stayed under it, 0 in 50.

The fix makes the threshold irrelevant: the delay starts again at the
reset.

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
| Probe 4's three Android passes | the original test | timing: a reset ≥ ~2 s after launch passed the old build; the runner's gap is ~1.3–1.9 s. `app_terminate` ruled out |
