# Probe 4, follow-up: does Haiku fold the coupon test every time? — 2026-10-17

Probe 4 ran each agent once. Haiku 5.5's one suite folded "codes refused,
each saying why" into an `each` of three fresh carts, and
`../2026-10-17-morpho-second-code/` showed the fold misses
`stale-code-message`. This asks whether that was one run's chance. The
prompt is probe 4's, unchanged (`agent/morpho-prompt-filled.md`), given
through `claude -p` from an empty folder: five more Haiku runs and two more
Sonnet 5.5 runs (`agent/`, written out by `tools/agent_extract.py` to
`generated/`).

## The coupon test

| Run | folded into `each` | its coupon test under `stale-code-message`, on the emulator |
|---|---|---|
| Haiku 1 (probe 4) | yes | passes: **missed** (`../2026-10-17-morpho-second-code/`) |
| Haiku 2 | yes | passes: **missed** |
| Haiku 3 | no, the original's steps | fails: caught |
| Haiku 4 | yes | passes: **missed** |
| Haiku 5 | no, the original's steps | fails: caught |
| Haiku 6 | yes | passes: **missed** |
| Sonnet 1 (probe 4) | no | fails: caught |
| Sonnet 2, 3 | no, the original's steps | fail: caught |

**Haiku folds it in 4 runs of 6, and every fold misses the bug**; Sonnet
kept the one session in 3 of 3. All four folds are the same shape: cases
of `code` and `message`, a fresh cart each, and the discount line checked
hidden after every code. Every coupon test passed with no bug on (3 cases
for a fold, 1 test otherwise). The fold is a habit of the model, not one
run's accident, so a test it writes can lose a sequence the original
checked.

## A second finding: four Haiku suites do not load

`{"keyboard": {"key": "enter"}}`, ten times in the original's checkout
file and once in its shop file, became `{"keyboard": "enter"}` in Haiku
runs 2, 3, 4 and 6. `keyboard` has no one main argument, so `mobium test`
refuses the file before anything runs (exit 2): `"keyboard" has no one
main argument (it takes hide, key, text); write {"keyboard": {...}} with
them named`. The traces show the call only in its long form, and the
format the agents were given (`agent/format.md`) says a string is a tool's
"main argument" without saying which tools have one; Mobium's own guide
says how it is chosen and that a tool without one is refused. Probe 4's
Haiku run and run 5 kept the long form; no Sonnet run shortened it.

So four of Haiku's six suites would run nothing: the refusal is Mobium's
correct answer, and its message names the fix. To run their coupon tests
here, each was taken out with its file's `app` and `beforeEach`, as the
agent wrote them (`device/coupon-alone-files/`), and run alone
(`device/coupon-alone/`). Runs 3 and 5 and both Sonnet runs were run
through the whole suite filtered to that test (`device/whole-suite-filtered/`,
where the four refusals are kept too).

## What came of it

| Finding | Bucket | Status |
|---|---|---|
| Haiku folds a one-session test into fresh cases in 4 of 6 runs; every fold misses `stale-code-message` | agent | measured; Sonnet 0 of 3 |
| Haiku shortens `keyboard` to a form that does not exist in 4 of 6 runs | agent / `agent/format.md` | measured; Mobium refuses the file with the fix named; `format.md` now says which string goes where |
| Mobium's test-runner guide does not say a case starts from a fresh app | Mobium's docs | proposed: a paragraph in "One test over several cases: `each`", on the Mobium branch `each-starts-over`; mobium-evals `verify` on t25: Sonnet folded 2 of 3 before it and 0 of 3 after, but its pass rate stayed 1 of 3, since two trials kept the file and gave no answer (a flaw in the harness's finish schema); Haiku 3 of 3 both |
| The refactor as an eval task | [mobium-evals](https://github.com/mobiumdev/mobium-evals) | t25 (`dc36d2c`): controls as expected; asked to shorten the one test with the constraint stated, Haiku kept the sequence 3 of 3 and Sonnet folded 1 of 3 — the fold depends on how the test is asked for |

## What is kept

Here: the agents' answers, the suites written from them, and the JUnit
results of every device run. Console output and screenshots of failures
are not kept; see [the evidence README](../README.md). Cost: Haiku $0.017–0.019 and about a minute a run; Sonnet
$0.27 and under a minute.
