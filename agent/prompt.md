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

VALUES

Answer with one JSON object and nothing else, no prose and no code fence:
keys are the file names, values are each file's content as a JSON object.

# The traces

DIGEST

# The guide to the test format (Mobium's docs/guides/test-runner.md)

GUIDE
