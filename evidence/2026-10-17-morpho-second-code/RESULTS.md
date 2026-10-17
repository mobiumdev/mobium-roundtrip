# Probe 4, follow-up: a bug for Haiku's refactor — 2026-10-17

Probe 4 (`../2026-10-16-morpho/RESULTS.md`, §3 and §5) found that Haiku
5.5 rewrote "codes refused, each saying why" as an `each` of three cases,
and that no bug in Morpho Market's 16 told the two versions apart. This
follow-up adds one that does, and runs every suite under it.

**The two tests.** The original (`corpus-morpho/shop.test.json`) fills a
cart once and types three codes into it in turn: MOBIUM5 ("Add $6.00 more
to use this code."), then EXPIRED20 ("That code has expired."), then
FREESTUFF ("That code isn't valid."). Haiku's
(`generated/morpho-agent-haiku/shop.test.json`) runs the same steps three
times, one code per case, each from a reset store. Haiku's never types a
code over a refused one.

**The bug** (Morpho Market branch `second-code-message`, `6776565`):
`stale-code-message`, a code refused after another refused code keeps the
first one's message. It is in `applyCode` on both platforms, and SPEC.md's
bug table says which test catches it and why only that one can. Same
devices as probe 4; Mobium `bfcb09f`.

## The run

Each suite with no bug on, then with `stale-code-message` on
(`tools/morpho_run.sh`; `matrix-{android,ios}/`):

| Suite | no bug, Android / iOS | `stale-code-message`: failed, Android / iOS | lost |
|---|---|---|---|
| original | 25 / 25 passed | 1 / 1 | — |
| table (`gen.py`) | 25 / 25 passed | 1 / 1 | 0 |
| Sonnet 5.5 | 25 / 25 passed | 1 / 1 | 0 |
| Haiku 5.5 | 27 / 27 passed | **0 / 0** | **1** |

Every failure is the same step on both platforms: the wait for "That code
has expired." times out after 3 seconds with the message still "Add $6.00
more to use this code." (step 10 of 14 in the original and Sonnet's, 13
of 17 in the table's, which inlines `beforeEach`). The scores are
`score-{android,ios}-<suite>.txt`.

**Haiku's suite misses the bug on both platforms**: the first bug a
generated suite has missed on Morpho Market. It still catches the other
16, and all 27 of its cases pass with no bug on; only a bug that depends
on the order of the codes shows the difference. The table and Sonnet,
which kept the one session, catch it.

## What it shows

- **A refactor that reads as tidier can test less.** Three cases with a
  fresh cart each look like the same three checks, and every bug the app
  had agreed. What was lost is the sequence itself: a code typed over a
  refused one. Nothing in a test's pass/fail with no bug on could have
  shown it, and only a mutant aimed at the difference did.
- **The matrix found it only once the bug set could.** Probe 4 reported
  Haiku's refactor as 0 lost against 16 bugs, which was true and was not
  evidence that the meaning was kept. A bug set is a yardstick; a gap in
  it reads as agreement.

## What came of it

| Finding | Bucket | Status |
|---|---|---|
| Haiku's `each` refactor misses a bug the original catches | agent | measured: 1 lost on both platforms; the table and Sonnet catch it |
| Morpho Market had no bug that depends on a second code | the bug set | added: `stale-code-message`, `second-code-message` `6776565`, not pushed |
| The refactor as an eval task | [mobium-evals](https://github.com/mobiumdev/mobium-evals) | not done |

## Not done

- More than one Haiku run: whether it refactors this test every time is
  unmeasured.
- The TV app, which has no coupon test.

## What is kept

Here: this file, the JUnit result of every run, the matrix logs and the
scores. Console output and screenshots of failures are not kept; see
[the evidence README](../README.md).
