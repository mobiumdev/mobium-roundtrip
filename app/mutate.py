"""Patch MobiumApp's App.tsx with runtime-selected mutants, for the probe only.

The app reads one word from files/roundtrip-mutant.txt in its own data at
start; each mutant is a plausible bug in the Login or Form Demo. With no file
the app behaves as shipped. The patched file is never committed to
mobium-app: apply, build, then `git checkout App.tsx` there.

usage: python3 mutate.py <path to App.tsx>
"""
import sys

MUTANTS = {
    "msg": "a wrong password's message reworded",
    "terms-notify": "ticking Accept terms ticks Email me too",
    "radio-sticky": "Free stays chosen when another plan is chosen",
    "dark-stuck": "the dark mode switch cannot be turned off",
    "logout-keeps": "the username field starts filled in",
    "leaves-front": "the Login Demo opens Android's Settings over the app",
}

EDITS = [
    # The switch, read once as the module loads: every test launches the app afresh.
    ("import {ground, ui} from './theme';\n",
     "import {ground, ui} from './theme';\n"
     "import {Linking} from 'react-native';\n"
     "let MUTANT = '';\n"
     "try {\n"
     "  const mf = new File(Paths.document, 'roundtrip-mutant.txt');\n"
     "  if (mf.exists) MUTANT = mf.textSync().trim();\n"
     "} catch (e) {}\n"),
    ("      setFormErr('Incorrect username or password.');\n",
     "      setFormErr(MUTANT === 'msg' ? 'Incorrect password.' : 'Incorrect username or password.');\n"),
    ("      onPress={() => set(!on)}>\n",
     "      onPress={() => { set(!on); if (MUTANT === 'terms-notify' && id === 'termsCheck') setNotify(!on); }}>\n"),
    ("      accessibilityState={{checked: plan === value}}\n",
     "      accessibilityState={{checked: plan === value || (MUTANT === 'radio-sticky' && value === 'free')}}\n"),
    ("          onValueChange={setDark}\n",
     "          onValueChange={v => setDark(MUTANT === 'dark-stuck' ? true : v)}\n"),
    ("  const [user, setUser] = useState('');\n",
     "  const [user, setUser] = useState(MUTANT === 'logout-keeps' ? 'mobium' : '');\n"
     "  useEffect(() => { if (MUTANT === 'leaves-front') Linking.openSettings(); }, []);\n"),
]


def main(path):
    src = open(path, encoding="utf-8").read()
    for old, new in EDITS:
        if src.count(old) != 1:
            sys.exit(f"expected exactly one occurrence of {old!r}, found {src.count(old)}")
        src = src.replace(old, new)
    open(path, "w", encoding="utf-8").write(src)
    print(f"patched {path} with {len(EDITS)} edits; mutants: {', '.join(MUTANTS)}")


if __name__ == "__main__":
    main(sys.argv[1])
