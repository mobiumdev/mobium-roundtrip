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
A string goes to `target` when the tool has one, else to its one required
string argument, else to its only argument; a tool with none of these
refuses a string, so `{"keyboard": {"key": "enter"}}` and `{"swipe":
{"direction": "up"}}` are written with their arguments named.

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
