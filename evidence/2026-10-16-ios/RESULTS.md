# Probe 3: the round trip on an iOS simulator — 2026-10-16

**Setup.** iPhone 17 Pro simulator, iOS 26.5
(`457C7DC2-C706-45D9-8D68-1D26953E28B1`), WebDriverAgent. Mobium
`mobiumdev/mobium` `main` at `74ce9e9`, which has #219 and #220. MobiumApp
built for the simulator in Release from `mobium-app` `0c6323f` plus
`app/mutants.patch`: the same commit and the same six mutants as Android
(`app/build/ios-mutants.app`, not in git; `App.tsx` reverted after the
build). The mutant switch is the same file, written into the app's data
container on the Mac and read back (`tools/mutant.sh`, with `DEV` set to the
UDID).

**Positive control.** With `msg` on, the original wrong-password test failed
on "its text is "Incorrect password."" (`00-positive-control.txt`).

## 1. One generated test serves both platforms

The corpus traced on iOS (`01-original-traced/`). Every traced call on iOS
carries `"driver": "wda"`, which the runner adds from the project config,
as it adds `device`. `gen.py` copied it into every step, which would have
tied every generated test to WebDriverAgent. Now `gen.py` drops `driver`
with `device` (so do `digest.py` and `compare.py`), and the Android output is
unchanged by the edit.

After that, **the tests generated from the iOS traces are byte-identical to
the ones generated from the Android traces** (`generated/ios-v2/` and
`generated/v2/`, both files). The same test, traced on two platforms, gives
the same test back.

A mistake caught on the way: the first iOS recording used a binary built
before #219, and its traces had no assertions. Rebuilt from `main`, the "in
front" test's trace holds both.

## 2. The matrix on iOS

Four suites, each under the six mutants and under none (`03-matrix/`). The
agents' tests are the ones written from the **Android** traces in probe 2,
run unchanged on iOS.

| Suite | Cells failed | Lost | Extra | Mutants killed |
|---|---|---|---|---|
| original (`ios-corpus`) | 11 | — | — | 6 of 6 |
| table, from the iOS traces (`ios-generated-ios-v2`) | 11 | **0** | 0 | 6 of 6 |
| Sonnet 5.5, from the Android traces | 11 | **0** | 0 | 6 of 6 |
| Haiku 5.5, from the Android traces | 11 | **0** | 0 | 6 of 6 |

Under "none" all four passed 9 of 9.

**11 cells, not Android's 12.** Under `leaves-front` the original's "the app
is in front throughout" passes on iOS. Watched by hand: after the Login Demo
opens, MobiumApp is in front at 0.3 s and Settings is in front by 0.9 s.
Both of the test's `expect`s pass on their first read, before Settings
arrives. On Android Settings comes sooner. So on iOS the test checks only
the first moment, not "throughout". The weakness is in the original test,
and every generated suite reproduced it faithfully.

**A failure that names the wrong cause** (a lead, not fixed): under
`leaves-front`, one original test failed with "typed "mobium" and the field
holds "username" — iOS dropped a keystroke". Nothing was dropped: the app
left the front while the field was being typed into, and what was read back
was the field's placeholder. Same shape as CHALLENGES 324 and 325.

## 3. The branch on iOS

`corpus-branch/camera.py` now takes the device and presses the platform's
own yes: "Allow" on iOS, "While using the app" on Android (`07-branch/`).

| | prompt state | granted state |
|---|---|---|
| the original script | pass, pressed "Allow" | pass, pressed nothing |
| test from the prompt trace | pass | **fail**: "there is no dialog to press a button on" |
| test from the granted trace | **fail**: see below | pass |
| Sonnet's test (probe 2: grant camera first) | **fail**: "camera" cannot be set on iOS | **fail**, the same |
| Haiku's test (the same idea) | **fail**, the same | **fail**, the same |
| dialog rules, one per platform's prompt, by hand | pass | pass |

- As on Android, each trace's test passes only in its own state.
- **The agents' answer does not carry to iOS.** Both met the branch by
  granting the camera first, so the prompt never comes. Mobium refuses that
  on a simulator: "the iOS simulator has no camera privacy service". Removing
  the branch was not only a loss of intent; it was not portable either.
- **Dialog rules are.** One file declaring both platforms' rules (`when`
  "take pictures" → "While using the app", `when` "access the Camera" →
  "Allow") passed in both states on iOS.

**How the states were set.** The prompt state is `mobium reset-permissions`.
The granted state was meant to be `mobium grant … camera`, which is refused
on the simulator for the reason above. The permission was granted by the
prompt-state runs answering "Allow", and the results confirm it: in that
state the prompt trace's test found no dialog, and the script pressed
nothing.

**A lead for Mobium** (not fixed): with the prompt up and no rule, the test
from the granted trace failed with "no element matches testid=dialogOutcome
— scrolled up to the start of the list (1 scroll)". The dialog was not
named. CHALLENGES 328's fix asks for a dialog when a scroll finds nothing to
scroll or the app changes: those are Android's signals. On iOS an alert sits
inside the app's own tree, so neither fires. The iOS case wants its own
check.

## What came of it

| Finding | Bucket | Status |
|---|---|---|
| iOS traces carry `driver` on every call | codegen table | fixed in `gen.py`, `digest.py`, `compare.py` |
| One trace-derived test serves both platforms | — | measured: byte-identical |
| Agent tests written from Android traces hold on iOS | agent | 11 of 11, 0 lost, both models |
| "In front throughout" checks only the first moment on iOS | the original test | to tighten in Mobium's `tests/mobiumapp/` |
| A keystroke blamed for an app that left the front | Mobium defect | fixed as CHALLENGES 331, merged as mobiumdev/mobium#223 (`5a0ee12`); verified on the simulator (12 of 15 failures name Settings, 3 find it in front first, none blame a keystroke; 9 of 9 with no mutant, twice) |
| A scroll under an iOS alert blames the list | Mobium defect (328's iOS twin) | fixed as CHALLENGES 330, merged as mobiumdev/mobium#222 (`9421543`); verified on the simulator (named 2 of 2, the rule passing 2 of 2) and on Android (unchanged) |
| Agents' "grant first" is refused on iOS | agent | strengthens the eval task from probe 2 |

## Not done

- The docs scenarios on iOS: `capture.py`'s setups are Android's (Settings,
  Android's own apps).
- A real iPhone.
