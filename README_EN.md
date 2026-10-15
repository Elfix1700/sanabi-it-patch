# SANABI Italian translation — fan patch

An **unofficial, free, fan-made** Italian translation of SANABI.
Requires an original copy of the game. No game files are included.

> **Built for version 1.3.53.** On other versions the script skips strings that
> no longer match and tells you so. It never breaks anything: it simply
> translates less.

---

## What it does

The game already ships 11 languages, each with its own slot inside the text
files. This patch puts Italian **into the English slot**. No twelfth language is
added, no new references are created: the file structure stays identical.

**After patching you must select "English" in Options → Language.** That is the
only thing to remember: you pick the entry called English and the game speaks
Italian. All other languages remain intact and working, so you can always go
back.

## Requirements

- Python 3.8 or newer
- UnityPy: `pip install UnityPy`
- A SANABI folder containing `SNB.exe` and `SNB_Data/StreamingAssets/aa/`
- No administrator rights, no internet connection

## Install

### Linux / macOS / Steam Deck

```bash
cd patch_it_sanabi
./run_linux.sh --apply
```

or manually:

```bash
python3 patcher/patch_sanabi_it.py --path /path/to/SANABI --apply
```

### Windows

Double-click `run_windows.bat`, or from a terminal:

```cmd
python patcher\patch_sanabi_it.py --path "C:\path\to\SANABI" --apply
```

### Steam Deck

Same as Linux. If your game lives in
`~/.steam/steam/steamapps/common/SANABI`, the script finds it on its own and
you can omit `--path`.

## Check before applying

```bash
python3 patcher/patch_sanabi_it.py --check
```

Reports how many strings match, per bundle and per chapter. Read-only: it
changes nothing.

## Uninstall

```bash
python3 patcher/patch_sanabi_it.py --restore
```

Restores the original files from the backup folder and verifies SHA-256
hashes. After `--restore` the game is exactly as before.

## Known issues

- The language must be selected manually (see above): Italian goes into the
  English slot, so you pick "English".
- The title screen and the language selector start in your operating system
  language. If you see another language at boot, open Options → Language and
  choose English.
- DLC subtitles are translated like the rest.
- Tested on Linux with Wine. Native Windows and Steam Deck were not tested by
  the author, but the script does nothing Linux-specific.

## Reporting a bug

Open an issue on the GitHub repository stating: game version, chapter, the
English line and the Italian line you see.
