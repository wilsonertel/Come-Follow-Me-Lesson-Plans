#!/usr/bin/env python3
"""Scripture references: parse them, link them, and fetch their real text.

Used two ways:

* build.py imports `link()` to turn [[Hosea 2:14–15]] markers into Gospel
  Library links (the same URL style as the rest of this site).
* The Part 6 review runs it from the command line to print the actual verse
  text for every reference in a lesson, so each claim can be checked:

      python3 template/scripture.py "Hosea 2:14-15" "Joel 2:28"
      python3 template/scripture.py --lesson handouts/2026/src/47-hosea-joel.py
      python3 template/scripture.py --quotes handouts/2026/src/47-hosea-joel.py

--quotes checks every “quoted phrase” that is followed closely by a [[reference]]
against the real verse text (ignoring case and punctuation; "…" splits a quote
into pieces that must each appear). Bracketed insertions like [His] are skipped.

Fetched chapters are cached in ~/.cache/cfm-scripture/ (one JSON per chapter).
"""
import json, os, re, sys, urllib.request
from html import unescape

GL = "https://www.churchofjesuschrist.org/study/scriptures"
CACHE = os.path.expanduser("~/.cache/cfm-scripture")
UA = "Mozilla/5.0 (cfm-handout-builder)"

# name (and common abbreviations) -> (volume, url slug)
_BOOKS = {
    "ot": [("Genesis", "gen", "Gen."), ("Exodus", "ex", "Ex."), ("Leviticus", "lev", "Lev."),
           ("Numbers", "num", "Num."), ("Deuteronomy", "deut", "Deut."), ("Joshua", "josh", "Josh."),
           ("Judges", "judg", "Judg."), ("Ruth", "ruth", None), ("1 Samuel", "1-sam", "1 Sam."),
           ("2 Samuel", "2-sam", "2 Sam."), ("1 Kings", "1-kgs", "1 Kgs."), ("2 Kings", "2-kgs", "2 Kgs."),
           ("1 Chronicles", "1-chr", "1 Chr."), ("2 Chronicles", "2-chr", "2 Chr."), ("Ezra", "ezra", None),
           ("Nehemiah", "neh", "Neh."), ("Esther", "esth", "Esth."), ("Job", "job", None),
           ("Psalms", "ps", "Ps."), ("Psalm", "ps", None), ("Proverbs", "prov", "Prov."),
           ("Ecclesiastes", "eccl", "Eccl."), ("Song of Solomon", "song", None), ("Isaiah", "isa", "Isa."),
           ("Jeremiah", "jer", "Jer."), ("Lamentations", "lam", "Lam."), ("Ezekiel", "ezek", "Ezek."),
           ("Daniel", "dan", "Dan."), ("Hosea", "hosea", "Hosea"), ("Joel", "joel", None),
           ("Amos", "amos", None), ("Obadiah", "obad", "Obad."), ("Jonah", "jonah", None),
           ("Micah", "micah", None), ("Nahum", "nahum", None), ("Habakkuk", "hab", "Hab."),
           ("Zephaniah", "zeph", "Zeph."), ("Haggai", "hag", "Hag."), ("Zechariah", "zech", "Zech."),
           ("Malachi", "mal", "Mal.")],
    "nt": [("Matthew", "matt", "Matt."), ("Mark", "mark", None), ("Luke", "luke", None),
           ("John", "john", None), ("Acts", "acts", None), ("Romans", "rom", "Rom."),
           ("1 Corinthians", "1-cor", "1 Cor."), ("2 Corinthians", "2-cor", "2 Cor."),
           ("Galatians", "gal", "Gal."), ("Ephesians", "eph", "Eph."), ("Philippians", "philip", "Philip."),
           ("Colossians", "col", "Col."), ("1 Thessalonians", "1-thes", "1 Thes."),
           ("2 Thessalonians", "2-thes", "2 Thes."), ("1 Timothy", "1-tim", "1 Tim."),
           ("2 Timothy", "2-tim", "2 Tim."), ("Titus", "titus", None), ("Philemon", "philem", "Philem."),
           ("Hebrews", "heb", "Heb."), ("James", "james", None), ("1 Peter", "1-pet", "1 Pet."),
           ("2 Peter", "2-pet", "2 Pet."), ("1 John", "1-jn", "1 Jn."), ("2 John", "2-jn", None),
           ("3 John", "3-jn", None), ("Jude", "jude", None), ("Revelation", "rev", "Rev.")],
    "bofm": [("1 Nephi", "1-ne", "1 Ne."), ("2 Nephi", "2-ne", "2 Ne."), ("Jacob", "jacob", None),
             ("Enos", "enos", None), ("Jarom", "jarom", None), ("Omni", "omni", None),
             ("Words of Mormon", "w-of-m", "W of M"), ("Mosiah", "mosiah", None), ("Alma", "alma", None),
             ("Helaman", "hel", "Hel."), ("3 Nephi", "3-ne", "3 Ne."), ("4 Nephi", "4-ne", "4 Ne."),
             ("Mormon", "morm", "Morm."), ("Ether", "ether", None), ("Moroni", "moro", "Moro.")],
    "dc-testament": [("Doctrine and Covenants", "dc", "D&C"), ("Official Declaration", "od", None)],
    "pgp": [("Moses", "moses", None), ("Abraham", "abr", "Abr."),
            ("Joseph Smith—Matthew", "js-m", "JS—M"), ("Joseph Smith—History", "js-h", "JS—H"),
            ("Articles of Faith", "a-of-f", None)],
}
BOOKS = {}
for vol, rows in _BOOKS.items():
    for name, slug, abbr in rows:
        BOOKS[name.lower()] = (vol, slug)
        if abbr:
            BOOKS[abbr.lower()] = (vol, slug)
BOOKS["d&amp;c"] = BOOKS["d&c"]
_NAMES = sorted(BOOKS, key=len, reverse=True)
_BOOK_RE = "|".join(re.escape(n) for n in _NAMES)
REF_RE = re.compile(rf"^\s*({_BOOK_RE})\s+(\d+)(?::\s*([\d\s,–\-]+))?\s*$", re.I)


class RefError(ValueError):
    pass


def parse(ref):
    """'Hosea 2:5–7, 13' -> ('ot', 'hosea', 2, [(5, 7), (13, 13)]).  Verses may be []."""
    m = REF_RE.match(ref.replace("‑", "-"))
    if not m:
        raise RefError(f"can't parse scripture reference: {ref!r}")
    vol, slug = BOOKS[m.group(1).lower()]
    ch = int(m.group(2))
    spans = []
    if m.group(3):
        for part in m.group(3).split(","):
            part = part.strip()
            if not part:
                continue
            a, _, b = part.replace("–", "-").partition("-")
            a = int(a)
            b = int(b) if b.strip() else a
            if b < a:
                raise RefError(f"backwards verse range in {ref!r}")
            spans.append((a, b))
    return vol, slug, ch, spans


def url(ref):
    vol, slug, ch, spans = parse(ref)
    u = f"{GL}/{vol}/{slug}/{ch}?lang=eng"
    if spans:
        ids = ",".join(f"p{a}" if a == b else f"p{a}-p{b}" for a, b in spans)
        u += f"&amp;id={ids}#p{spans[0][0]}"
    return u


def link(ref, label=None):
    """HTML anchor in the site's scripture-link style (class="s")."""
    return (f'<a class="s" href="{url(ref)}" target="_blank" rel="noopener">'
            f'{label if label is not None else ref}</a>')


# ---------------------------------------------------------------- fetching
def _clean(html):
    html = re.sub(r'<span class="verse-number">.*?</span>', "", html, flags=re.S)
    html = re.sub(r"<sup[^>]*>.*?</sup>", "", html, flags=re.S)
    html = re.sub(r"<button.*?</button>", "", html, flags=re.S)
    html = re.sub(r"<svg.*?</svg>", "", html, flags=re.S)
    txt = unescape(re.sub(r"<[^>]+>", "", html))
    return re.sub(r"\s+", " ", txt).strip()


def chapter(vol, slug, ch):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{vol}_{slug}_{ch}.json")
    if os.path.exists(path):
        return {int(k): v for k, v in json.load(open(path)).items()}
    req = urllib.request.Request(f"{GL}/{vol}/{slug}/{ch}?lang=eng", headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    verses = {}
    for m in re.finditer(r'<p class="verse"[^>]*id="p(\d+)"[^>]*>(.*?)</p>', html, re.S):
        verses[int(m.group(1))] = _clean(m.group(2))
    if not verses:
        raise RuntimeError(f"no verses found for {vol}/{slug}/{ch}")
    json.dump(verses, open(path, "w"), ensure_ascii=False, indent=0)
    return verses


def text(ref):
    vol, slug, ch, spans = parse(ref)
    vs = chapter(vol, slug, ch)
    if not spans:
        return f"[whole chapter: {len(vs)} verses] " + vs.get(1, "")[:160] + " …"
    out = []
    for a, b in spans:
        for v in range(a, b + 1):
            if v not in vs:
                raise RefError(f"{ref}: verse {v} does not exist (chapter has {max(vs)})")
            out.append(f"{v} {vs[v]}")
    return "  ".join(out)


REF_MARK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


def refs_in_lesson(path):
    src = open(path, encoding="utf-8").read()
    seen = []
    for m in REF_MARK.finditer(src):
        r = m.group(1).strip()
        if r not in seen:
            seen.append(r)
    return seen


QUOTE_NEAR_REF = re.compile(r"“([^”]{3,})”[^“\[\"]{0,40}?\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


def _norm(t):
    t = re.sub(r"\[[^\]]*\]", " ", t)          # drop [His]-style insertions
    t = t.lower().replace("’", "'")
    t = re.sub(r"[^a-z0-9' ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def check_quotes(path):
    src = open(path, encoding="utf-8").read()
    bad = n = 0
    for m in QUOTE_NEAR_REF.finditer(src):
        quote, ref = m.group(1), m.group(2).strip()
        try:
            hay = _norm(text(ref))
        except Exception as e:
            print(f"✗ {ref}: {e}")
            bad += 1
            continue
        n += 1
        missing = [frag for frag in re.split(r"…|\.\.\.", quote) if _norm(frag) and _norm(frag) not in hay]
        if missing:
            bad += 1
            print(f"✗ “{quote}”  ≠  {ref}\n    not found: {missing}\n    verse: {text(ref)[:300]}\n")
    print(f"{n} quotations checked against their references, {bad} problems")
    print("(quotes not followed by a [[reference]], e.g. talks and the manual, are not checked here)")
    return 1 if bad else 0


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    if argv[0] == "--quotes":
        return check_quotes(argv[1])
    refs = refs_in_lesson(argv[1]) if argv[0] == "--lesson" else argv
    bad = 0
    for r in refs:
        try:
            print(f"■ {r}\n    {text(r)}\n")
        except Exception as e:  # report and keep going
            bad += 1
            print(f"✗ {r}\n    ERROR: {e}\n")
    print(f"{len(refs)} references, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
