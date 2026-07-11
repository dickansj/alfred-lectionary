# alfred-lectionary

Alfred workflow for USCCB Bible pages (bible.usccb.org): jump straight to daily Mass readings or any Bible chapter, in the official Catholic lectionary text for the USA.

Requires the [Alfred Powerpack](https://www.alfredapp.com/powerpack/) — Script Filters (which this workflow uses) aren't available in the free version of Alfred.

## Install

1. Clone this repo: `git clone git@github.com:dickansj/alfred-lectionary.git ~/alfred-lectionary`
2. Build the package: `cd ~/alfred-lectionary && zip -X alfred-lectionary.alfredworkflow info.plist resolve.py icon.png`
3. In Finder, go to `~/alfred-lectionary/` and double-click `alfred-lectionary.alfredworkflow`.
4. Alfred opens an import dialog — click **Import Workflow**.

Alfred must already be running for the double-click to trigger the import
dialog. If you edit `resolve.py` or `info.plist` later, re-run step 2 and
re-import — Alfred will offer to overwrite the existing "Lectionary"
workflow (same `bundleid`), so your changes replace it in place.

## Usage

| Input | Opens |
|---|---|
| `lect` | Today's daily Mass readings |
| `lect 5d` | Readings 5 days from today |
| `lect july 31` | Readings for the next July 31 (rolls to next year if already passed) |
| `lect job 8` | Job, chapter 8 |
| `lect 1 kgs 13` | 1 Kings, chapter 13 |

Book names and SBL abbreviations (Society of Biblical Literature style,
e.g. `1 Kgs`, `Isa`) are case-insensitive. All 73 books on
USCCB's Bible pages are supported (including Tobit, Judith, 1-2 Maccabees,
Wisdom, Sirach, and Baruch).

Alfred shows a preview of the resolved title before opening anything —
press Enter to confirm.

## Files

- `resolve.py` — parses the query and prints the Alfred Script Filter JSON
- `info.plist` — the workflow definition (Script Filter → Open URL)
- `icon.png` — the workflow's icon
- `make_icon.py` — one-off script that generated `icon.png`; not part of the workflow itself
- `alfred-lectionary.alfredworkflow` — the packaged, importable workflow;
  gitignored and not tracked here (see Install step 2 to build it)

## Rebuilding the package

After editing `resolve.py` or `info.plist`, repackage with the same command
from Install step 2:

```sh
zip -X alfred-lectionary.alfredworkflow info.plist resolve.py icon.png
```
