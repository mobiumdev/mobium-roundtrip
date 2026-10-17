You are given traces of a `mobium test` run on an Android emulator: every
call the runner made on the device, with its arguments and what it answered.
Each trace is one test; its title is `<file> › <test name>`.

Write the test files those traces came from, as their author would have
written them: one file per file name in the titles. Recover what you can of
how the author wrote them, not only what ran — for example a `beforeEach`
shared by every test in a file, one test run over several cases with
`each`, `expect`s where a trace shows an assertion, and the test names. Use
the format described in the guide below.

Typed text is not in a trace, only its length. Here is what was typed, by
test name, in the order it was typed:

- a bad sign-in is refused, and says why: a wrong password: "mobium", "wrongpass1"
- a bad sign-in is refused, and says why: a short password: "mobium", "abc"
- a bad sign-in is refused, and says why: a short username: "mo", "hunter2"
- the demo account signs in, and out: "mobium", "hunter2"
- focus follows the tap, and a field holds what was typed: "mob"

Answer with one JSON object and nothing else, no prose and no code fence:
keys are the file names, values are each file's content as a JSON object.

# The traces

## trace: form.test.json › a checkbox reaches the state asked for
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_tap {"target": "label=Form Demo"}
  -> tapped label=Form Demo at (540, 1598)
- app_wait_for {"condition": "unchecked", "target": "testid=termsCheck"}
  -> testid=termsCheck is unchecked after 11ms — @e3 Accept terms (checkbox, unchecked)
- app_check {"target": "testid=termsCheck"}
  -> testid=termsCheck is now checked
- app_wait_for {"condition": "checked", "target": "testid=termsCheck"}
  -> testid=termsCheck is checked after 9ms — @e3 Accept terms (checkbox, checked)
- app_wait_for {"condition": "checked", "not": true, "target": "testid=notifyCheck"}
  -> testid=notifyCheck is no longer checked after 10ms

## trace: form.test.json › choosing a radio clears the one before
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_tap {"target": "label=Form Demo"}
  -> tapped label=Form Demo at (540, 1598)
- app_wait_for {"condition": "checked", "target": "testid=planFree"}
  -> testid=planFree is checked after 11ms — @e4 Free (radio, checked)
- app_tap {"target": "testid=planPro"}
  -> tapped testid=planPro at (540, 831)
- app_wait_for {"condition": "checked", "target": "testid=planPro"}
  -> testid=planPro is checked after 9ms — @e5 Pro (radio, checked)
- app_wait_for {"condition": "unchecked", "target": "testid=planFree"}
  -> testid=planFree is unchecked after 9ms — @e4 Free (radio, unchecked)
- app_wait_for {"condition": "count", "count": 3, "target": "role=radio"}
  -> role=radio matches 3 on screen after 8ms

## trace: form.test.json › the dark mode switch goes on and back off
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_tap {"target": "label=Form Demo"}
  -> tapped label=Form Demo at (540, 1598)
- app_check {"target": "testid=darkSwitch"}
  -> testid=darkSwitch is now checked
- app_wait_for {"condition": "checked", "target": "testid=darkSwitch"}
  -> testid=darkSwitch is checked after 9ms — @e7 Dark mode (switch, checked)
- app_check {"checked": false, "target": "testid=darkSwitch"}
  -> testid=darkSwitch is now unchecked
- app_wait_for {"condition": "unchecked", "target": "testid=darkSwitch"}
  -> testid=darkSwitch is unchecked after 7ms — @e7 Dark mode (switch, unchecked)

## trace: login.test.json › a bad sign-in is refused, and says why: a short password
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_fill {"target": "testid=username", "text": "(6 characters, not recorded)"}
  -> typed "mobium" into testid=username
- app_fill {"target": "testid=password", "text": "(3 characters, not recorded)"}
  -> typed 3 characters into testid=password, a password field — not echoed
- app_tap {"target": "testid=loginBtn"}
  -> tapped testid=loginBtn at (540, 1457)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=passError", "text": "Password must be at least 6 characters."}
  -> testid=passError says exactly "Password must be at least 6 characters." after 6ms — @e1 ScrollView (list)
- app_wait_for {"condition": "hidden", "target": "testid=welcomeText"}
  -> testid=welcomeText is hidden after 22ms

## trace: login.test.json › a bad sign-in is refused, and says why: a short username
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_fill {"target": "testid=username", "text": "(2 characters, not recorded)"}
  -> typed "mo" into testid=username
- app_fill {"target": "testid=password", "text": "(7 characters, not recorded)"}
  -> typed 7 characters into testid=password, a password field — not echoed
- app_tap {"target": "testid=loginBtn"}
  -> tapped testid=loginBtn at (540, 1457)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=userError", "text": "Username must be at least 3 characters."}
  -> testid=userError says exactly "Username must be at least 3 characters." after 7ms — @e1 ScrollView (list)
- app_wait_for {"condition": "hidden", "target": "testid=welcomeText"}
  -> testid=welcomeText is hidden after 22ms

## trace: login.test.json › a bad sign-in is refused, and says why: a wrong password
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_fill {"target": "testid=username", "text": "(6 characters, not recorded)"}
  -> typed "mobium" into testid=username
- app_fill {"target": "testid=password", "text": "(10 characters, not recorded)"}
  -> typed 10 characters into testid=password, a password field — not echoed
- app_tap {"target": "testid=loginBtn"}
  -> tapped testid=loginBtn at (540, 1457)
- app_wait_for {"condition": "text", "exact": true, "target": "testid=loginError", "text": "Incorrect username or password."}
  -> testid=loginError says exactly "Incorrect username or password." after 7ms — @e1 ScrollView (list)
- app_wait_for {"condition": "hidden", "target": "testid=welcomeText"}
  -> testid=welcomeText is hidden after 21ms

## trace: login.test.json › focus follows the tap, and a field holds what was typed
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_tap {"target": "testid=username"}
  -> tapped testid=username at (540, 1090)
- app_wait_for {"condition": "focused", "target": "testid=username"}
  -> testid=username is focused after 8ms — @e3 username (input)
- app_wait_for {"condition": "focused", "not": true, "target": "testid=password"}
  -> testid=password is no longer focused after 8ms
- app_type {"target": "testid=username", "text": "(3 characters, not recorded)"}
  -> typed "mob" into testid=username
- app_wait_for {"condition": "value", "target": "testid=username", "text": "mob"}
  -> testid=username holds "mob" after 9ms — @e3 mob (input)
- app_wait_for {"condition": "text", "not": true, "target": "testid=username", "text": "mobium"}
  -> testid=username no longer contains "mobium" after 8ms

## trace: login.test.json › the app is in front throughout
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_state {"app": "dev.mobium.mobiumapp", "assertion": {"attempt": 1, "equals": "foreground", "field": "state"}}
  -> dev.mobium.mobiumapp is in front
- app_current {"assertion": {"attempt": 1, "equals": "dev.mobium.mobiumapp", "field": "app"}}
  -> dev.mobium.mobiumapp

## trace: login.test.json › the demo account signs in, and out
- app_terminate {"app": "dev.mobium.mobiumapp"}
  -> terminated dev.mobium.mobiumapp
- app_launch {"app": "dev.mobium.mobiumapp"}
  -> launched dev.mobium.mobiumapp
- app_dialogs {"press": "Not Now", "when": "Save Password"}
  -> 1 dialog rule(s) when "Save Password": press "Not Now" (answered 0)
- app_tap {"target": "label=Login Demo"}
  -> tapped label=Login Demo at (540, 814)
- app_fill {"target": "testid=username", "text": "(6 characters, not recorded)"}
  -> typed "mobium" into testid=username
- app_fill {"target": "testid=password", "text": "(7 characters, not recorded)"}
  -> typed 7 characters into testid=password, a password field — not echoed
- app_tap {"target": "testid=loginBtn"}
  -> tapped testid=loginBtn at (540, 1457)
- app_wait_for {"target": "testid=welcomeText", "timeout_ms": 15000}
  -> testid=welcomeText is visible after 5ms
- app_tap {"target": "testid=logoutBtn"}
  -> tapped testid=logoutBtn at (540, 618)
- app_wait_for {"condition": "value", "target": "testid=username", "text": ""}
  -> testid=username holds "" after 6ms — @e3 username (input)



# The test format

A test file is JSON:

    {
      "app": "<package>",            // stopped and launched fresh before every test
      "beforeEach": [<step>...],     // optional: run before each test's own steps
      "tests": [
        {"name": "...", "description": "...", "steps": [<step>...],
         "each": [{"key": "value", ...}, ...]}   // optional, see below
      ]
    }

A step is one tool call, in the long form
`{"name": "app_tap", "arguments": {"target": "text=Network & internet"}}`, or
the shorthand: one key, the tool's name without `app_`, whose value is its
arguments or, as a string, its main argument — `{"tap": "text=Network &
internet"}`, `{"fill": {"target": "testid=search", "text": "wifi"}}`.

An assertion is an `app_wait_for` step —
`{"wait_for": {"target": "text=Internet", "condition": "visible"}}` — or an
expect, which reads a read-only tool until a field of its structured answer
equals a value:

    {"expect": {"tool": "app_state", "arguments": {"app": "com.android.settings"},
                "field": "state", "equals": "foreground", "not": false, "timeout_ms": 5000}}

`"soft": true` beside a step records an assertion's failure and goes on.

`each` runs a test once per case. `${key}` in any string of its steps (and in
its name) is that case's value:

    {"name": "search finds ${what}",
     "each": [{"what": "wifi"}, {"what": "bluetooth"}],
     "steps": [{"fill": {"target": "testid=search", "text": "${what}"}},
               {"wait_for": {"target": "text=${what}", "condition": "visible"}}]}

A test with `each` and no `${key}` in its name has its cases numbered.

