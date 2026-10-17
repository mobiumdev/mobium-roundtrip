# Probe 2: assertions in the trace, an agent, a branch, the docs scenarios — 2026-10-16

**Setup.** `mobium-test` AVD (Pixel 7, Android 15), headless, `emulator-5554`.
MobiumApp: probe 1's mutant build (`app/build/app-mutants.apk`, sha256
`ca02d729…`, built from `mobium-app` `0c6323f` plus `app/mutants.patch`),
the shipped build (`a014fe1e…`) put back afterward. Mobium: `mobiumdev/mobium`
`main` (`76af755`) plus two local branches, neither pushed:

- `trace-password-wording` (`d2924c6`, CHALLENGES 327): an expect's reads carry
  its assertion in `_meta` (`dev.mobium/expect`), and the trace keeps it as
  `assertion` — `field`, `equals`, `not`, `soft`, `timeout_ms`, `attempt`. And
  the trace's help says a *password* is not recorded, not typed text. Used
  for parts 1 and 2.
- `scroll-dialog` (`59daca0`, CHALLENGES 328): found in part 3, below. Used
  for parts 3 and 4.

## 1. Assertions in the trace close the lost cell

The corpus re-traced with `d2924c6` (`01-original-traced/`): the only test
with `expect`s, "the app is in front throughout", now holds
`{"field":"state","equals":"foreground"}` and
`{"field":"app","equals":"dev.mobium.mobiumapp"}`. `tools/gen.py` now turns
an `assertion` back into an `expect` (attempts after the first were its
polls, and are dropped). Generated again → `generated/v2/`.

| Suite (`03-matrix-v2/`, every suite on today's binary) | Cells failed | Lost | Extra |
|---|---|---|---|
| original (`corpus`) | 12 | — | — |
| table, `gen.py` with assertions (`generated-v2`) | 12 | **0** | 0 |

Probe 1 lost one cell, `leaves-front` × "the app is in front throughout".
It is now caught, with the original's message word for word: `expected
app_state's state to be "foreground", and after 10s state is "background"`.

## 2. An agent writes the test from the traces

`tools/digest.py` turns each trace into its calls, arguments and results as
text (no screenshots, no maps). `agent/prompt.md` asks for the test files
"as their author would have written them", with the typed text supplied as
in probe 1. **The format is described in `agent/format.md`, written for this
probe, with Settings examples**: Mobium's own test-runner guide quotes the
corpus — its Form Demo example is the corpus's first test word for word —
and would have handed over the answer. One run each, `claude -p`, no tools.

| | beforeEach | each (3 cases) | expects | descriptions | Cells | Lost | Extra | Cost |
|---|---|---|---|---|---|---|---|---|
| original | 2 files | 1 test | 2 | 4 | 12 | — | — | — |
| Sonnet 5.5 (`generated/agent-sonnet/`) | 2 files | 1 test | 2 | 0 | 12 | **0** | 0 | $0.088 |
| Haiku 5.5 (`generated/agent-haiku/`) | 2 files | 1 test | 2 | 0 | 12 | **0** | 0 | $0.006 |

Both recovered the structure the table cannot: the shared `beforeEach`
(including the iOS dialog rule, which never fires on Android), the three
bad sign-ins folded back into one test over `each`, and the two `expect`s.
Sonnet's login file differs from the original only in the case key
(`${case}` for `${why}`) and the shorthand spelling. Haiku put the error's
testid inside the case (`"target": "testid=loginError"`) instead of
`testid=${error}`. No descriptions: a trace does not hold them, and neither
agent made any up.

**What this does not show.** One run per model, on a nine-test corpus whose
test names already say which tests share a file. The `each` cases are named
in the titles ("…: a wrong password"), which makes folding them easy.

## 3. The branch: a client script, two device states

`corpus-branch/camera.py` (Python client): open the Dialog Demo, tap Camera
permission, **if** a dialog comes up within 3 s press "While using the app",
then scroll up to the outcome line and wait for `camera: granted`. Android
shows the prompt only while the permission is undecided, so the state picks
the path: `reset-permissions` gives the prompt, `grant … camera` does not,
read back from `dumpsys package` each time (`tools/branch.sh`, `07-branch/`).

| | prompt state | granted state |
|---|---|---|
| the original script | pass | pass |
| test from the prompt trace | pass | **fail**: `app_alert` button — "there is no dialog to press a button on" |
| test from the granted trace | **fail** — see below | pass |
| Sonnet, given both traces and every tool's description | pass | pass |
| Haiku, the same | pass | pass |
| a dialog rule, written by hand (`generated/branch/dialogs-rule.test.json`) | **fail**, then pass after the fix | pass |

Each trace holds one path, and the test made from it passes only in the state
it was recorded in. That was the expected result, and it is a positive
control for the comparison.

**Both agents removed the branch instead of keeping it.** Each put
`grant camera` first, so the prompt never comes, and passed in both states.
But the prompt path is no longer tested: the original would fail if "While
using the app" stopped granting the camera, and theirs cannot see it. Asked
for one test file that passes in both states, that is a reasonable reading,
and the wrong one if the prompt was the point. Neither used `app_dialogs`,
which keeps the branch, though the prompt listed it.

**The hand-written rule found a Mobium defect (CHALLENGES 328).** With the
rule declared, the scroll to the outcome line failed three times in three:
"swiping up moved from dev.mobium.mobiumapp to
com.google.android.permissioncontroller instead of scrolling — the area being
swiped does not scroll that way". The prompt came up under the first swipe.
Rules were consulted only when resolving a target, never by the scroll loop.
The test from the granted trace met the same gap with the prompt already up:
"no element matches testid=dialogOutcome and nothing on this screen scrolls".
Both remedies could not work. Fixed on `scroll-dialog` (`08-scroll-dialog-fix/`):

- the rule's test passes 3 of 3 with the prompt, and in the granted state;
- the test from the granted trace is now refused naming the prompt, 3 of 3:
  "a dialog is over the app — "Allow MobiumApp to take pictures and record
  video?" — …";
- the unit test fails on all four of its cases without the fix. The first
  version of the fix answered the dialog and then called the list ended,
  since the swipe that met the dialog moved nothing; the device caught that,
  and the unit test's fake now behaves as the device did.

So a test file *can* hold this kind of branch: "a dialog may come; answer
it" is a dialog rule. A branch on anything else still needs a script.

## 4. The docs site's scenarios

13 scenarios from `~/mobium-docs` that touch only Settings or MobiumApp and
change nothing device-wide. Each is `capture.py`'s setup plus the canonical
command, run through the CLI under `mobium trace` (`tools/docs_corpus.py`,
`09-docs/`).

| | |
|---|---|
| Generated tests (two files, one per app) | 13 of 13 pass |
| Trace against trace | **13 of 13 the same calls with the same results** |
| Mutants caught, MobiumApp's six scenarios | **1 of 6**, by accident: `leaves-front` put Settings over the Login Demo, and the keyboard scenario's tap found no username field |

The docs' scenarios replay perfectly and test nothing. They are examples, one
command each, with no assertion. As a corpus they score only the first level
in the README (replays), and confirm its warning: a replay with no
assertions passes every time. They become a second corpus only when each
gains the check its page implies, as the five-language translations would
need too.

## What came of it

| Finding | Bucket | Where |
|---|---|---|
| An `expect` lost its assertion in the trace | trace missing information | CHALLENGES 327, `d2924c6` |
| The trace's help promised typed text was not recorded | — (description) | CHALLENGES 327, `d2924c6` |
| A dialog mid-scroll was blamed on the list, and rules skipped it | a Mobium defect | CHALLENGES 328, `59daca0` |
| Agents meet a branch by removing it | agent | a task for [mobium-evals](https://github.com/mobiumdev/mobium-evals) |
| `gen.py` now writes `expect`s back | codegen table | `tools/gen.py` |

## Not done

- More agent runs per model (one each here), and a corpus whose titles do not
  give the grouping away.
- An eval task from part 3: two traces of one script, scored on whether the
  prompt path is still tested, not only on passing both states.
- Assertions for the docs scenarios, so they count as tests.
