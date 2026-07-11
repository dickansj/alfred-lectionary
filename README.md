# alfred-lectionary

Alfred workflow for jumping straight to USCCB (bible.usccb.org) pages.

## Install

1. In Finder, go to this folder (`/Users/joe/Projects/alfred-lectionary/`).
2. Double-click `alfred-lectionary.alfredworkflow`.
3. Alfred opens an import dialog — click **Import Workflow**.

Alfred must already be running for the double-click to trigger the import
dialog. If you edit `resolve.py` or `info.plist` later, re-run the zip
command below and re-import — Alfred will offer to overwrite the existing
"Lectionary" workflow (same `bundleid`), so your changes replace it in place.

## Usage

| Input | Opens |
|---|---|
| `lect` | Today's daily Mass readings |
| `lect 5d` | Readings 5 days from today |
| `lect july 31` | Readings for the next July 31 (rolls to next year if already passed) |
| `lect job 8` | Job, chapter 8 |
| `lect 1 kgs 13` | 1 Kings, chapter 13 |

Book names and SBL abbreviations are case-insensitive. All 73 books on
USCCB's Bible pages are supported (including Tobit, Judith, 1-2 Maccabees,
Wisdom, Sirach, and Baruch).

Alfred shows a preview of the resolved title before opening anything —
press Enter to confirm.

## Files

- `resolve.py` — parses the query and prints the Alfred Script Filter JSON
- `info.plist` — the workflow definition (Script Filter → Open URL)
- `alfred-lectionary.alfredworkflow` — the packaged, importable workflow

## Rebuilding the package

After editing `resolve.py` or `info.plist`, repackage with:

```sh
zip -X alfred-lectionary.alfredworkflow info.plist resolve.py
```
