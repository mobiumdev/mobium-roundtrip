# Probe 1: the deterministic round trip on the emulator, 2026-10-14

**Setup.** `mobium-test` AVD (Pixel 7, Android 15), headless, `emulator-5554`.
Mobium at `mobiumdev/mobium` `d263c6d` (`~/mobium-public/bin/mobium`, built
for this run). MobiumApp at `mobium-app` `0c6323f`. The corpus is the repository's
two test files (`tests/mobiumapp/login.test.json` and `form.test.json`), 9 tests
once `each` is expanded.

**Method.**
1. Run the originals with `--trace on` → T (`01-original-baseline/`, on the
   shipped APK).
2. `tools/gen.py` turns each trace into one test: one step per call, the
   runner's terminate+launch become `app`, the player keys are dropped.
   Nothing is inferred.
3. Run the generated suite. Run the original again on a MobiumApp build with
   six mutants (`app/mutate.py`, `app/mutants.patch`; APK sha256 `ca02d729…`,
   built from `0c6323f` plus the patch and never committed). The mutant is chosen at run time
   by a file in the app's data, written over `adb root` (`tools/mutant.sh`).
   **Positive control:** with `msg` set, the original wrong-password test
   failed on "Incorrect password." before the matrix ran.
4. `tools/run.sh`: each mutant, and none, × both suites (`03-matrix/`).
5. `tools/compare.py`: trace against trace, call by call, with timings,
   coordinates and refs normalized (`04-…`). **Positive control:** one
   edited locator in a copied trace → reported as DIFFERS (`05-…`).
6. `tools/score.py` → `06-score.txt`.

## Results

| | |
|---|---|
| Generated with nothing but the traces | **refused before running**: 5 of 9 tests type text, and a trace keeps only its length (`02-…`) |
| Generated, typed text supplied separately (`tools/values.json`) | 9 of 9 pass on the build with no mutant |
| Generated vs. original traces, no mutant | 9 of 9 the same calls with the same results |
| Mutants caught (6) | original 6, generated 6 |
| (mutant, test) cells that failed | 12 for the original, 11 for the generated suite: **1 lost**, 0 extra |
| Failure reasons, cell by cell | identical code and message; only the step number moves, by the number of `beforeEach` steps folded into the test |

**The one lost cell** is `leaves-front` × "the app is in front throughout".
The original's two steps are `expect`s, and a trace records an `expect` as
the bare call (`app_state`, `app_current`) and its result, without the field
or the value it asserts. The generated test makes the calls and asserts
nothing, so it passes while the app is behind Settings. The mutant was
still caught here only because other tests failed on it. A suite whose only
check on a behavior is an `expect` would lose that check entirely.

## Findings, by bucket

**The trace is missing information.**
1. **An `expect` loses its assertion.** It is traced as a plain call.
   Recording `field` and `equals` (or `soft`) on the call would close
   the one lost cell. Waits keep every argument, so `wait_for` assertions
   survive intact.
2. **Typed text: the length is kept, the value is not.** This is by design
   (`internal/agent/tracing.go`, `traceBefore`), so a trace alone cannot be
   replayed. The fix is ROADMAP's `secret:NAME` for passwords. For other
   fields there is a design decision to make, see 3.
3. **The redaction is weaker than its description.** The CLI help and the
   `app_trace` schema say text typed into a field "is not recorded, only its
   length". But `traceAfter` keeps the result text, which says
   `typed "mobium" into testid=username`, and the map of the screen shows
   the field's value. Passwords are safe: their result says "not echoed",
   `map` redacts them, and `wrongpass1` appears 0 times in the trace. Either
   the description should say "a password is not recorded", or results and
   maps should be redacted too. That choice is Lana's.
4. **Structure is lost but harmless here.** `beforeEach` is folded into each
   test, `each` is written out as separate tests, and `description`s are
   dropped. None of these changed a verdict in this corpus.

**The codegen table.** Nothing went wrong: every call mapped one to one.

**An agent's misreading.** Not tested yet: no agent was involved.

## Not done

- A test with a branch, the planned case where the trace lacks information.
  Note: the test format has no conditionals, so this needs a client script,
  not a test file.
- The agent round trip (step 3 with an agent instead of `gen.py`), scored
  the same way. Its value is recovering `beforeEach`, `each` and the
  `expect`s, which the table cannot do.
- The docs site's scenarios as a second corpus.
