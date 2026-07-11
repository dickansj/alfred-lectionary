#!/usr/bin/env python3
"""Alfred Script Filter: resolve `lect` queries into USCCB bible.usccb.org URLs."""

import json
import re
import sys
from datetime import date, timedelta

MONTHS = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

# (usccb slug, display name, extra aliases: SBL abbreviations + alternate full names)
BOOKS = [
    ("genesis", "Genesis", ["Gen"]),
    ("exodus", "Exodus", ["Exod"]),
    ("leviticus", "Leviticus", ["Lev"]),
    ("numbers", "Numbers", ["Num"]),
    ("deuteronomy", "Deuteronomy", ["Deut"]),
    ("joshua", "Joshua", ["Josh"]),
    ("judges", "Judges", ["Judg"]),
    ("ruth", "Ruth", []),
    ("1samuel", "1 Samuel", ["1 Sam"]),
    ("2samuel", "2 Samuel", ["2 Sam"]),
    ("1kings", "1 Kings", ["1 Kgs"]),
    ("2kings", "2 Kings", ["2 Kgs"]),
    ("1chronicles", "1 Chronicles", ["1 Chr"]),
    ("2chronicles", "2 Chronicles", ["2 Chr"]),
    ("ezra", "Ezra", []),
    ("nehemiah", "Nehemiah", ["Neh"]),
    ("tobit", "Tobit", ["Tob"]),
    ("judith", "Judith", ["Jdt"]),
    ("esther", "Esther", ["Esth"]),
    ("1maccabees", "1 Maccabees", ["1 Macc"]),
    ("2maccabees", "2 Maccabees", ["2 Macc"]),
    ("job", "Job", []),
    ("psalms", "Psalms", ["Ps", "Pss", "Psalm"]),
    ("proverbs", "Proverbs", ["Prov"]),
    ("ecclesiastes", "Ecclesiastes", ["Eccl", "Qoh", "Qoheleth"]),
    ("songofsongs", "Song of Songs", ["Song", "Cant", "Song of Solomon", "Canticles"]),
    ("wisdom", "Wisdom", ["Wis"]),
    ("sirach", "Sirach", ["Sir"]),
    ("isaiah", "Isaiah", ["Isa"]),
    ("jeremiah", "Jeremiah", ["Jer"]),
    ("lamentations", "Lamentations", ["Lam"]),
    ("baruch", "Baruch", ["Bar"]),
    ("ezekiel", "Ezekiel", ["Ezek"]),
    ("daniel", "Daniel", ["Dan"]),
    ("hosea", "Hosea", ["Hos"]),
    ("joel", "Joel", []),
    ("amos", "Amos", []),
    ("obadiah", "Obadiah", ["Obad"]),
    ("jonah", "Jonah", []),
    ("micah", "Micah", ["Mic"]),
    ("nahum", "Nahum", ["Nah"]),
    ("habakkuk", "Habakkuk", ["Hab"]),
    ("zephaniah", "Zephaniah", ["Zeph"]),
    ("haggai", "Haggai", ["Hag"]),
    ("zechariah", "Zechariah", ["Zech"]),
    ("malachi", "Malachi", ["Mal"]),
    ("matthew", "Matthew", ["Matt"]),
    ("mark", "Mark", []),
    ("luke", "Luke", []),
    ("john", "John", []),
    ("acts", "Acts of the Apostles", ["Acts"]),
    ("romans", "Romans", ["Rom"]),
    ("1corinthians", "1 Corinthians", ["1 Cor"]),
    ("2corinthians", "2 Corinthians", ["2 Cor"]),
    ("galatians", "Galatians", ["Gal"]),
    ("ephesians", "Ephesians", ["Eph"]),
    ("philippians", "Philippians", ["Phil"]),
    ("colossians", "Colossians", ["Col"]),
    ("1thessalonians", "1 Thessalonians", ["1 Thess"]),
    ("2thessalonians", "2 Thessalonians", ["2 Thess"]),
    ("1timothy", "1 Timothy", ["1 Tim"]),
    ("2timothy", "2 Timothy", ["2 Tim"]),
    ("titus", "Titus", []),
    ("philemon", "Philemon", ["Phlm"]),
    ("hebrews", "Hebrews", ["Heb"]),
    ("james", "James", ["Jas"]),
    ("1peter", "1 Peter", ["1 Pet"]),
    ("2peter", "2 Peter", ["2 Pet"]),
    ("1john", "1 John", []),
    ("2john", "2 John", []),
    ("3john", "3 John", []),
    ("jude", "Jude", []),
    ("revelation", "Revelation", ["Rev"]),
]


def normalize(s):
    s = s.lower().strip().replace(".", "")
    return re.sub(r"\s+", " ", s)


def build_book_index():
    index = {}
    for slug, display, aliases in BOOKS:
        for candidate in [display] + aliases:
            for key in (normalize(candidate), normalize(candidate).replace(" ", "")):
                index[key] = (slug, display)
    return index


BOOK_INDEX = build_book_index()


def reading_url(d):
    return "https://bible.usccb.org/bible/readings/{}.cfm".format(d.strftime("%m%d%y"))


def chapter_url(slug, chapter):
    return "https://bible.usccb.org/bible/{}/{}".format(slug, chapter)


def item(title, subtitle, arg=None, valid=True):
    result = {"title": title, "subtitle": subtitle, "valid": valid}
    if arg is not None:
        result["arg"] = arg
    return result


def resolve_month_day(month, day):
    today = date.today()
    year = today.year
    for _ in range(8):
        try:
            candidate = date(year, month, day)
        except ValueError:
            year += 1
            continue
        if candidate >= today:
            return candidate
        year += 1
    return None


def resolve(query):
    query = query.strip()

    if query == "":
        d = date.today()
        return item(
            "Open Readings for {}".format(d.strftime("%A, %B %-d, %Y")),
            "USCCB Daily Mass Readings",
            reading_url(d),
        )

    tokens = query.split()

    m = re.fullmatch(r"(\d+)d", tokens[0], re.IGNORECASE) if len(tokens) == 1 else None
    if m:
        d = date.today() + timedelta(days=int(m.group(1)))
        return item(
            "Open Readings for {}".format(d.strftime("%A, %B %-d, %Y")),
            "USCCB Daily Mass Readings ({} days from today)".format(m.group(1)),
            reading_url(d),
        )

    if len(tokens) == 2 and tokens[0].lower() in MONTHS:
        day_match = re.fullmatch(r"(\d{1,2})(?:st|nd|rd|th)?", tokens[1], re.IGNORECASE)
        if day_match:
            month = MONTHS[tokens[0].lower()]
            day = int(day_match.group(1))
            d = resolve_month_day(month, day)
            if d is None:
                return item(
                    "Invalid date: {} {}".format(tokens[0], tokens[1]),
                    "That day doesn't exist in that month.",
                    valid=False,
                )
            return item(
                "Open Readings for {}".format(d.strftime("%A, %B %-d, %Y")),
                "USCCB Daily Mass Readings",
                reading_url(d),
            )

    if len(tokens) >= 2 and tokens[-1].isdigit():
        chapter = int(tokens[-1])
        descriptor = normalize(" ".join(tokens[:-1]))
        book = BOOK_INDEX.get(descriptor) or BOOK_INDEX.get(descriptor.replace(" ", ""))
        if book:
            slug, display = book
            return item(
                "Open {}, Chapter {}".format(display, chapter),
                "USCCB Bible (NABRE)",
                chapter_url(slug, chapter),
            )
        return item(
            "Book not recognized: \"{}\"".format(" ".join(tokens[:-1])),
            'Use a full book name or SBL abbreviation, e.g. "job 8" or "1 kgs 13"',
            valid=False,
        )

    return item(
        "No match for \"{}\"".format(query),
        'Try nothing (today), "5d" (5 days ahead), "july 31", or "job 8"',
        valid=False,
    )


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps({"items": [resolve(query)]}))


if __name__ == "__main__":
    main()
