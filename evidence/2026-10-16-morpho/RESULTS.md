# Probe 4: the round trip on Morpho Market — 2026-10-16 and 17

**Setup.** Mobium `mobiumdev/mobium` `main` at `bfcb09f` (#219–#225).
Morpho Market `mobiumdev/morpho-market` at `229111e`, the Android and
SwiftUI apps built from it. Android: the `mobium-test` AVD
(`emulator-5554`). iOS: the iPhone 17 Pro simulator, iOS 26.5
(`457C7DC2-C706-45D9-8D68-1D26953E28B1`), WebDriverAgent.

**The corpus** is Morpho Market's own suite, unchanged
(`corpus-morpho/`): two files, 25 tests, 365 steps, a three-step
`beforeEach` in each. It is ten times probes 1–3's corpus, and it
covers pricing, coupons, shipping, stock, the cart badge and payment.

**The bugs** are the app's own 16, each switched on by a deep link
(`mobiumshop://bugs?off=all`, then `?on=<bug>`), so one build serves
the whole matrix on each platform (`tools/morpho_run.sh`). That is
17 rows (no bug, then each bug) × 4 suites × 2 platforms: 136 runs.

## 1. Recording a trace needs a longer timeout

The first recording, at the suite's 1-minute per-test timeout, failed
9 of 25 on Android and 12 of 25 on iOS, every failure a timeout
(`00-first-recording/`). Tracing takes a screenshot and a read around
every call, so a traced test is several times slower. Re-recorded with
`--timeout 4m`, both passed 25 of 25: 20m7s on Android, 28m33s on iOS
(`01-original-traced-{android,ios}/`). The matrix runs untraced, at
1 minute.

## 2. One generated test serves both platforms, again

Typed text is recorded only as its length, so `tools/values_from.py`
reads the 78 typed values (17 tests) out of the original tests into
`tools/morpho-values.json`, and `gen.py` fills them in through `each`.

**The tests generated from the iOS traces are byte-identical to the
ones generated from the Android traces** (`generated/morpho-ios-v2/`
and `generated/morpho-v2/`, both files), as in probe 3. The table
inlines each `beforeEach` into its tests: 440 steps, 25 × 3 more than
the original.

## 3. The agents rewrote the suite almost exactly

Both agents were given both trace digests, the values file and every
tool's description (`agent/morpho-prompt-filled.md`, 60 KB), through
`claude -p`, once each.

| | Tests | Cases | Steps | Same as the original | Cost | Time |
|---|---|---|---|---|---|---|
| original | 25 | 25 | 365 | — | — | — |
| Sonnet 5.5 (`generated/morpho-agent-sonnet/`) | 25 | 25 | 365 | **25 of 25**, `beforeEach` too | $0.26 | 49 s |
| Haiku 5.5 (`generated/morpho-agent-haiku/`) | 25 | 27 | 360 | 23 of 25, `beforeEach` too | $0.017 | 60 s |

"Same" means the same steps in the same order once the short and long
forms of a step are counted alike (`{"wait_for": "x"}` and
`{"wait_for": {"target": "x"}}`) and descriptions are set aside. Sonnet
wrote the long form in five places and dropped the descriptions;
otherwise its suite is the original.

Haiku changed two tests:
- **"codes refused, each saying why"** became an `each` of three cases,
  one per code, each starting from an empty cart. The original types
  the three codes in one session and checks the discount line is
  hidden only after the expired one; Haiku's checks it after every
  code. It also dropped one 3-second timeout to the default.
- **"out of stock cannot be added"** gained a first step waiting for the
  catalog, which `beforeEach` already does.

## 4. The matrix

| Suite | Android: tests failed, lost, extra | iOS: tests failed, lost, extra | Bugs caught |
|---|---|---|---|
| original | 40 / — / — | 43 / — / — | 16 of 16 on both |
| table (`gen.py`) | 40 / 3 / 3 | 43 / **0** / 0 | 16 of 16 on both |
| Sonnet 5.5 | 38 / 4 / 2 | 43 / **0** / 0 | 16 of 16 on both |
| Haiku 5.5 | 40 / 0 / 3 | 43 / **0** / 0 | 16 of 16 on both |

A cell is one test under one bug; a test's `each` cases fold into it,
failing if any case fails (§6). "Tests failed" counts cells over the 16
bugs, not every case. With no bug, every suite passed on both platforms:
25, 25, 25 and 27 tests, about 7.5 minutes each on Android and 10 on
iOS. The scores are `score-{android,ios}-<suite>.txt`.

**On iOS the round trip lost nothing and added nothing**, for all three
generated suites. **On Android every difference is under one bug,
`slow-catalog`**, and outside it all three suites match the original
cell for cell.

### Why `slow-catalog` differs on Android

The bug delays the catalog by 8 seconds **the first time a process shows
it** (`Shop.kt:49`, `catalogShown`; the same in `Shop.swift`). Every
test's `beforeEach` resets the store and waits 3 seconds for the
catalog. So a test fails under this bug only if its app process is new.

| | original | table | Sonnet | Haiku |
|---|---|---|---|---|
| Android, tests failing under `slow-catalog` | 22 of 25 | 22 of 25 | 20 of 25 | 26 of 27 cases |
| iOS | 25 of 25 | 25 of 25 | 25 of 25 | 27 of 27 |

On iOS every test met the delay. On Android a few tests in each suite
passed, and they were different tests each time. Every failure in every
suite is the same `beforeEach` timeout, and Morpho Market's own Android
matrix (`evidence/android-bug-matrix/` in its repository) has the
original failing 25 of 25. So which Android tests a `slow-catalog` run
fails varies from run to run, the original's included, and the six lost
and eight extra cells are that variation, not the round trip.

The weakness is in the original test, which assumes every test starts in
a new process. *Follow-up, 2026-10-17 (`../2026-10-17-morpho-reset/`): the
bug now fires after every reset, and every suite agrees with the original
under it on both platforms. The runner gave every test a new process, and
the three passes did not reproduce.* Why an Android process sometimes survived a test is not
measured; logging the app's process id before each test would tell.

## 5. What a bigger corpus showed

- **Fidelity held at 25 tests.** Probes 2 and 3 had 9 tests; here
  the table and both agents kept every bug caught on both platforms,
  and Sonnet reproduced the suite exactly.
- **The agents kept the structure, not the words.** Both kept
  `beforeEach`, which the table cannot recover from a trace. Both
  dropped the original's 15 step descriptions, as both did in probe 2;
  Haiku wrote a description of its own for every test instead.
- **Haiku's refactor changed the test's meaning and was not caught.**
  Splitting one session of three codes into three fresh sessions tests
  something slightly different (no code is typed over another), and no
  bug in the 16 tells the two apart. A mutant that misbehaves only on
  a second code would.
- **Recording is slower than running.** A test suite that fits its
  own timeout may not fit it traced (§1).

## 6. A scoring fix, and probes 2 and 3 re-scored

`tools/score.py` keyed each JUnit case by name, so a test's `each` cases
(`name [1]`, `name [2]` …) overwrote each other, and the last one's
verdict stood. Haiku's three-case test exposed it. Now a case's index is
dropped and the test fails if any case fails. Probes 2 and 3 re-scored
with the fix: unchanged, 12/0/0 on Android and 11/0/0 on iOS for every
suite.

## What came of it

| Finding | Bucket | Status |
|---|---|---|
| The table and both agents catch 16 of 16 bugs on both platforms | — | measured: 0 lost on iOS, 0 lost outside `slow-catalog` on Android |
| One trace-derived test serves both platforms, at 25 tests | — | measured: byte-identical |
| Sonnet rewrote 25 of 25 tests exactly; Haiku 23 of 25 | agent | measured |
| Haiku's `each` changed a test's meaning, and no bug noticed | agent / the bug set | a mutant for it, and a task for [mobium-evals](https://github.com/mobiumdev/mobium-evals) |
| `slow-catalog`'s Android verdicts depend on whether the store is new | the original test | fixed in Morpho Market `b658e0e`; re-run 0 lost on both platforms (`../2026-10-17-morpho-reset/`) |
| Recording needs a longer timeout than running | runner | noted; `--timeout 4m` here |
| `score.py` overwrote `each` cases | the scorer | fixed; probes 2 and 3 unchanged |

## Not done

- The Fire TV test (125 steps) and the TV apps.
- A real phone.
- More than one agent run per model.

## What is kept

Here: this file, the JUnit result of every run, the scores and the short
outputs it cites. The traces and screenshots (1.4 GB) are not kept; see
[the evidence README](../README.md). The agents' prompt
(`agent/morpho-prompt-filled.md`) holds the trace digests they worked
from, and the generated suites are in `generated/`.
