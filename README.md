# Come, Follow Me Lesson Plans

Weekly lesson handouts and teaching helps for **Come, Follow Me — For Home and Church: Old Testament 2026**.

## How It's Organized

Open **[index.html](index.html)** — the home page lists all 12 months of the 2026 curriculum. Every week of the official outline has its own folder and page:

```
index.html                          ← Home page (latest handouts + all 12 months, all 52 weeks)
handouts/<year>/NN-slug.html        ← Handouts built by the template (src/ holds each one's content)
template/                           ← Handout builder: base.css, build.py, research/review/render tools
examples/                           ← The two reference handouts (Ezekiel, Daniel) that set the bar
notes/                              ← research-log.md (sources per week) + fetched outlines
race/                               ← The Scripture Race reading game
lessons/
  2026 - Old Testament/
    January/ … December/            ← One folder per month, with a month overview page
      <dates>-<scriptures>/         ← One folder per week (e.g. july-6-12-2-kings-2-7)
        index.html                  ← Week hub page listing that week's materials
        handouts/                   ← Lesson handout files (HTML and Word)
tools/                              ← Lesson-builder skill bundle
```

## The Scripture Race

**[race/index.html](race/index.html)** is a reading game for the kids, linked from
a card on the home page. It lists every chapter the Come, Follow Me outline
assigns from **August 3 through December 27 — 238 in all**. A student types their
name, picks a car colour, and taps chapters as they read them; their car moves
around the track and the class leaderboard reorders itself. Read all 238 and the
car parks in victory lane.

A pace car shows how far along a student who never fell behind would be, so
"12 chapters behind pace" is visible without anyone doing arithmetic.

Out of the box the race runs in **practice mode**: it works fully, but each device
keeps its own roster. To put the whole class on one live leaderboard, follow
**[race/SETUP.md](race/SETUP.md)** — a free Firebase Realtime Database, pasted into
`race/config.js`. Separate groups can be sent to separate tracks with
`race/index.html?class=whatever`.

Weeks follow the official Come, Follow Me outline at [churchofjesuschrist.org](https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026?lang=eng) — same date ranges, scripture blocks, and lesson titles. Weeks that span two months are filed under the month in which the week ends (matching the Gospel Library app).

## Building a Weekly Handout

Handouts are built from a Python data file by `template/build.py` (see `CLAUDE.md` and
`.claude/skills/cfm-handout/SKILL.md` for the full workflow — Claude Code runs it when asked for
"this week's lesson" or "next week's lesson"):

```bash
python3 template/week.py                                    # which week is it?
python3 template/fetch_outline.py 47 -o notes/outlines/2026-47-outline.md
python3 template/build.py build handouts/2026/src/47-hosea-joel.py
python3 template/scripture.py --lesson handouts/2026/src/47-hosea-joel.py   # review every reference
python3 template/scripture.py --quotes handouts/2026/src/47-hosea-joel.py   # check quotations
node template/render_check.js handouts/2026/47-hosea-joel.html              # screenshots + PDF
```

A build writes the handout, links it from its week page, marks the week ready on the home page,
and refreshes the home page's "Latest handouts" list.

## Adding a New Lesson by Hand

1. Drop the handout file(s) into that week's `handouts/` folder.
2. Add a link to the file on the week's `index.html` hub page.
3. The home page badge for that week can be updated from "Coming soon" to show the handout count.

## Currently Available

| Week | Scriptures | Handouts |
|---|---|---|
| July 6–12 | 2 Kings 2–7 — "There Is a Prophet in Israel" | 2 Kings 2 Youth Handout, 2 Kings 3 Lesson Handout, plus 2 Word docs |
| July 13–19 | 2 Kings 16–25 — "He Trusted in the Lord God of Israel" | 2 Kings 16–25 Lesson Handout |
| August 3–9 | Esther — "Thou Art Come … for Such a Time as This" | Esther Lesson Handout |
| August 10–16 | Job 1–3; 12–14; 19; 21–24; 38–40; 42 — "Yet Will I Trust in Him" | Combined Handout, plus Parts 1–4 (Job 1–3; 12–13 · Job 14; 19 · Job 21–24 · Job 38–40; 42), Weekly Quiz |
| August 31 – September 6 | Psalms 102–103; 110; 116–119; 127–128; 135–139; 146–150 — "Let Every Thing That Hath Breath Praise the Lord" | Psalms 102–150 Lesson Handout, Weekly Quiz |
| September 7–13 | Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12 — "He Shall Direct Thy Paths" | Weekly Quiz (3 short answers + 3 longer responses) |
| November 2–8 | Ezekiel 1–3; 33–34; 36–37; 47 — "A New Spirit Will I Put within You" | Ezekiel Lesson Handout (`handouts/2026/45-ezekiel.html`) |
| November 9–15 | Daniel 1–7 — "There Is No Other God That Can Deliver" | Daniel Lesson Handout (`handouts/2026/46-daniel.html`), Weekly Quiz (3 short answers + 1 longer response) |
| November 16–22 | Hosea 1–6; 10–14; Joel — "I Will Love Them Freely" | Hosea & Joel Lesson Handout (`handouts/2026/47-hosea-joel.html`) |
