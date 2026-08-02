# Come, Follow Me Lesson Plans

Weekly lesson handouts and teaching helps for **Come, Follow Me — For Home and Church: Old Testament 2026**.

## How It's Organized

Open **[index.html](index.html)** — the home page lists all 12 months of the 2026 curriculum. Every week of the official outline has its own folder and page:

```
index.html                          ← Home page (all 12 months, all 52 weeks)
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

## Adding a New Lesson

1. Drop the handout file(s) into that week's `handouts/` folder.
2. Add a link to the file on the week's `index.html` hub page.
3. The home page badge for that week can be updated from "Coming soon" to show the handout count.

## Currently Available

| Week | Scriptures | Handouts |
|---|---|---|
| July 6–12 | 2 Kings 2–7 — "There Is a Prophet in Israel" | 2 Kings 2 Youth Handout, 2 Kings 3 Lesson Handout, plus 2 Word docs |
| July 13–19 | 2 Kings 16–25 — "He Trusted in the Lord God of Israel" | 2 Kings 16–25 Lesson Handout |
