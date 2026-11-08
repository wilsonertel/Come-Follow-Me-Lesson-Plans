#!/usr/bin/env python3
"""Which Come, Follow Me week is it?  (Part 2 of the workflow)

    python3 template/week.py                 # today's lesson + next week's
    python3 template/week.py 2026-11-16      # the week containing a date
    python3 template/week.py --week 47       # a week number in the current year

Rules: weeks run Monday–Sunday and the lesson is taught on the Sunday that
ENDS the week. So on a Sunday, "today's lesson" is the week ending today and
"next week" ends next Sunday. Week 1 of a curriculum year is the week ending
on the first Sunday of January (2026: Dec 29 – Jan 4; Nov 2–8 is week 45).

Rotation: Old Testament, New Testament, Book of Mormon, Doctrine and
Covenants (2026 = Old Testament). The printed number is a best guess from
the calendar: ALWAYS confirm it against the date range on the manual page.
"""
import datetime as dt, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTATION = ["Old Testament", "New Testament", "Book of Mormon", "Doctrine and Covenants"]
SLUG = {"Old Testament": "old-testament", "New Testament": "new-testament",
        "Book of Mormon": "book-of-mormon", "Doctrine and Covenants": "doctrine-and-covenants"}
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]


def week_end(d):
    return d + dt.timedelta(days=(6 - d.weekday()))  # Sunday of d's Mon–Sun week


def curriculum_year(sunday):
    return sunday.year  # the week ending on the first Sunday of January belongs to the new year


def week_info(sunday):
    year = curriculum_year(sunday)
    jan1 = dt.date(year, 1, 1)
    first_sunday = week_end(jan1)
    num = (sunday - first_sunday).days // 7 + 1
    monday = sunday - dt.timedelta(days=6)
    vol = ROTATION[(year - 2026) % 4]
    url = (f"https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-"
           f"{SLUG[vol]}-{year}/{num}?lang=eng")
    if monday.month == sunday.month:
        rng = f"{MONTHS[monday.month-1].title()} {monday.day}–{sunday.day}"
    else:
        rng = f"{MONTHS[monday.month-1].title()} {monday.day} – {MONTHS[sunday.month-1].title()} {sunday.day}"
    return dict(year=year, week=num, volume=vol, monday=monday, sunday=sunday, range=rng, url=url,
                hub=find_hub(year, vol, monday, sunday))


def find_hub(year, vol, monday, sunday):
    """The site's week folder, e.g. lessons/2026 - Old Testament/November/november-16-22-hosea-..."""
    base = os.path.join(ROOT, "lessons", f"{year} - {vol}", MONTHS[sunday.month - 1].title())
    if not os.path.isdir(base):
        return None
    if monday.month == sunday.month:
        prefix = f"{MONTHS[monday.month-1]}-{monday.day}-{sunday.day}-"
    else:
        prefix = f"{MONTHS[monday.month-1]}-{monday.day}-{MONTHS[sunday.month-1]}-{sunday.day}-"
    for name in sorted(os.listdir(base)):
        if name.startswith(prefix):
            return os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
    return None


def show(label, info):
    print(f"{label}: week {info['week']} · {info['range']}, {info['year']} · {info['volume']}")
    print(f"   taught Sunday {info['sunday']:%a %b %d, %Y}")
    print(f"   manual: {info['url']}   (confirm the date range on the page!)")
    print(f"   week hub: {info['hub'] or '(none found)'}")


def main(argv):
    today = dt.date.today()
    if argv[:1] == ["--week"]:
        first = week_end(dt.date(today.year, 1, 1))
        show("Requested", week_info(first + dt.timedelta(weeks=int(argv[1]) - 1)))
    elif argv:
        show("Requested", week_info(week_end(dt.date.fromisoformat(argv[0]))))
    else:
        this = week_end(today)
        print(f"Today is {today:%A, %B %d, %Y}.")
        show("This week's lesson", week_info(this))
        show("Next week's lesson", week_info(this + dt.timedelta(days=7)))


if __name__ == "__main__":
    main(sys.argv[1:])
