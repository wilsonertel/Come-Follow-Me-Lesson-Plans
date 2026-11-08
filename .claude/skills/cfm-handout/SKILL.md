---
name: cfm-handout
description: Build a print-ready Come, Follow Me lesson handout for a youth Sunday School class (ages 12–13), using this repo's template, research, review, and render workflow. Use this whenever the user asks for a Come, Follow Me lesson or handout, "this week's lesson," "next week's lesson," "today's lesson," a lesson for a date, a week number, or a scripture range or block (e.g. "Hosea and Joel," "Amos–Jonah," "Nov 23–29"), a Sunday School or seminary handout, lesson prep, or a scripture deep dive for the class, even if they never say "skill" or "handout." When in doubt, use this skill. Do not freelance a lesson without it.
---

# Come, Follow Me handout: weekly workflow

This skill builds one self-contained HTML handout per week in `handouts/<year>/NN-slug.html`
and publishes it to the site (home page list, week hub page, week badge). The quality bar is
`examples/ezekiel-handout.html` and `examples/daniel-handout.html`. Re-read one of them before
writing if you haven't this session.

Run every step, in order. Don't skip the review (step 6) or the render check (step 7).

## 1. Figure out which week (never assume from memory)

```bash
date                                 # the real date
python3 template/week.py             # this week's + next week's lesson
python3 template/week.py 2026-11-16  # or: the week containing a date / --week 47
```

- Weeks run **Monday–Sunday**. The class is taught on the **Sunday that ends the week**.
  On a Sunday, "today's/this week's lesson" = the week ending today; "next week" = the week
  ending next Sunday.
- Curriculum rotates yearly: Old Testament → New Testament → Book of Mormon → Doctrine and
  Covenants (2026 = Old Testament, 2027 = New Testament, …).
- Manual URL (2026): `https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026/<week>?lang=eng`
  (Nov 2–8 was week 45). **Confirm the date range printed on the fetched page** matches. If it
  doesn't, step the number until it does.
- If the request is at all ambiguous, **state the week, dates, and scripture block before you
  start building**. A handout for the wrong week is the worst failure.
- Check `handouts/<year>/` and the week hub folder so you don't rebuild something that exists.

## 2. Fetch the official outline and Scripture Helps

```bash
python3 template/fetch_outline.py <week> -o notes/outlines/<year>-<week>-outline.md
python3 template/fetch_outline.py "<scripture-helps url>" -o notes/outlines/<year>-<week>-scripture-helps.md
```

The Scripture Helps URL (`.../scripture-helps-old-testament/<slug>?lang=eng`) is linked from the
weekly page: grep the outline file for `scripture-helps`. Read both files fully and record:
exact title; intro theme; **every principle heading** (the one marked `[SEMINARY ICON]` is the
seminary principle); verses and questions under each; Scripture Helps questions (those shown on
the weekly page *and* the full list); "Ideas for Teaching Children" headings; every talk, hymn,
video, picture, and cross-reference. Section 4 must mirror this, not a generic take.

If a fetch fails with a proxy 403/DNS error, the host isn't in the environment's network allowlist.
Ask for it with the environment tools; don't write from memory.

## 3. Read the block and research the history

- Read every chapter in the block: `python3 template/scripture.py "Hosea 1" ...` (cached).
- History: dates, rulers/empire, geography, culture, **≥2 archaeology anchors** (inscriptions,
  tablets, excavations, museum pieces). Verify names and dates in **≥2 reputable sources**
  (encyclopedias, museum pages, scholarly works; Bible Dictionary for Church framing). Wikipedia's
  API works well: `https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=<Title>`.
- Note anything scholars genuinely debate. It goes in the honest-note card.
- **Append** a section for this week to `notes/research-log.md` (never overwrite older weeks):
  each source, what it was used for, and anything left uncertain.

## 4. Write the lesson data file

Copy the shape of `handouts/2026/src/47-hosea-joel.py` to `handouts/<year>/src/<NN>-<slug>.py`.
Content goes in the data; layout is in `template/build.py` helpers:

| helper | use |
|---|---|
| `p`, `lead`, `h3` | paragraphs, italic section lead, sub-headings |
| `card(tag, *paras, warm=False)` | callouts: archaeology anchors, at a glance, honest note / hard questions (`warm=True`) |
| `pull(quote, cite)` | one short KJV pull-quote |
| `steps([(ref, heading, body)])` | numbered passage timeline |
| `parallel_cards([dict(k_ref,k,b_ref,b,teaches)])` | 8–10 two-part parallel cards |
| `points`, `helps`, `resto`, `ideas` | Section 4: principles, Scripture Helps Qs, 3–4 node Restoration timeline, 5–6 teaching ideas |
| `christ([(ref_line, heading, body)])` | Section 5 dark panel, 4–6 entries |

Markup in strings: `**bold**`, `*italic*`, `[[Hosea 2:14–15]]` or `[[Hosea 2:14–15|vv. 14–15]]`
→ Gospel Library link (a bad reference stops the build). Text is HTML-escaped; `&` is fine.

### The five sections, always in this order

1. **Historical Summary of the Period.** When, who's in power, where, and culture. An
   archaeology-anchors card (≥2 anchors). An "at a glance" card if the book needs orienting. An
   honest-note card (warm) for anything debated (authorship, dating, identifications).
2. **Passage Summary.** `steps`, one per narrative movement or teaching, with verse refs. A
   warm **"Hard questions students may ask"** card with faithful, scholarly answers. One short
   KJV pull-quote.
3. **Book of Mormon Parallels** (Bible years) or **Cross-Scripture Connections** (BoM/D&C
   years; build.py titles it from `volume`). 8–10 cards: passage detail → echo with exact refs →
   one-line "Teaches:". Every card must rest on a real doctrinal pattern. Cut stretches.
4. **Tie to Come, Follow Me.** Outline title and intro theme. Each principle with verses,
   questions, cited talks (flag the seminary one). Scripture Helps questions with pointers to
   where the handout answers them. Children's-section headings. A **Latter-day connections**
   card (D&C, Bible Dictionary, footnotes, temple and Restoration ties). A 3–4 node Restoration
   timeline. **5–6 teaching ideas for ages 12–13**: hands-on, discussion, small groups, and
   **one invitation to act this week**.
5. **Tie to Jesus Christ.** 4–6 entries: ref line (OT passage · NT/BoM/D&C echo), heading,
   short paragraph. Use types and shadows where legitimate and **label them as types**; label
   interpretations as interpretations.

Header (from `LESSON`): eyebrow "Come, Follow Me · [Volume] [Year] · Youth Sunday School" (auto),
`h1` = book name(s), `kicker`, chip = outline title + dates (auto), one-sentence `hook`, and a
simple inline SVG drawn from **this passage's own imagery**. `band`: ~5 dated events.
`sources`: footer list. The Print button and reveal script are automatic.

### Design rules

- Minimal and clean. Override **only the 13 colour tokens** in `tokens`; never add per-lesson CSS.
- New palette + one signature SVG motif from the passage's imagery every week (Ezekiel: river
  teal + temple gold; Daniel: Ishtar-Gate lapis + furnace orange; Hosea/Joel: dawn rose + lily +
  dew). Note the idea in `palette_note`.
- Keep the SVG under ~220px tall, viewBox-based, no external images. Fade hard edges.
- Fonts (Fraunces + Inter), responsiveness, print rules, and the reveal failsafe (2.5 s +
  `beforeprint`) live in `template/base.css` / `build.py`. Don't fork them per lesson.

## 5. Build

```bash
python3 template/build.py build handouts/<year>/src/<NN>-<slug>.py
```

This writes `handouts/<year>/<NN>-<slug>.html`, links it from the week hub page (the `week_hub`
folder from `week.py`), marks the week ready on the home page, and regenerates the home page's
"Latest handouts" list (newest first). Fix every `WARNING:` it prints (counts out of range, no
invitation, short palette).

## 6. Accuracy and doctrinal review (mandatory)

```bash
python3 template/scripture.py --lesson handouts/<year>/src/<NN>-<slug>.py   # every ref + its real text
python3 template/scripture.py --quotes handouts/<year>/src/<NN>-<slug>.py   # quotes vs. their verses
```

- **Every reference:** read the printed verse text and confirm it says what the handout claims.
  Wrong verse numbers are the most common error.
- **Every quotation:** KJV/BoM quotes short and exact (`--quotes` flags mismatches; name
  glosses and manual headings show up too and are fine once checked). Conference talks and the
  manual: paraphrase; at most a short phrase in quotes, checked against `notes/outlines/`.
- **Nothing invented:** no unverified talks, dates, artifacts, quotations. Can't verify → cut it
  or mark it uncertain.
- **Doctrine:** faithful to Church teaching; interpretations labelled; debated scholarship
  presented as debated.
- **Current events:** don't name the current living prophet or anyone's *current* calling unless
  verified today. "The living prophet" is fine. Attributing a talk to its speaker as titled at the
  time ("President Russell M. Nelson, April 2018") is fine.
- **Audience:** concrete and clear for 12–13 year olds; hard passages handled honestly and
  constructively, never sensationalized.
- **Section 4 vs. outline:** title, principles (and seminary flag), questions, talks, Scripture
  Helps questions, children's headings all match the fetched files.

## 7. Verify the render (look at it)

```bash
node template/render_check.js handouts/<year>/<NN>-<slug>.html
```

Renders at 1000px and 390px, checks overflow, hidden sections, SVG clipping, section count, and
print (button hidden, nothing hidden, colour-exact), and writes screenshots + a PDF to `.renders/`
(git-ignored). **Then actually look**: slice the full-page PNGs (PIL) and read them; make a PDF
contact sheet (`pdftoppm -r 50 -png`) and check pagination. Fix anything off, rebuild, recheck.
Google Fonts may be blocked in the sandbox; fallback fonts in screenshots are expected.

## 8. Finish

- Commit the handout, its `src/` data file, `notes/outlines/*`, `notes/research-log.md`, and the
  updated `index.html` + week hub page; push to the working branch.
- **Publish it (the owner's standing instruction; don't ask first):**
  ```bash
  git fetch origin main && git checkout -B main origin/main
  git merge --no-ff <working-branch> -m "Merge the <Book> lesson handout for <dates>" -m "<attribution lines>"
  git push origin main && git checkout <working-branch>
  ```
  Then confirm the GitHub "pages build and deployment" run for that merge commit succeeds
  (GitHub MCP `actions_list` → `list_workflow_runs`). If the merge conflicts, stop and tell the user.
- Report to the user: (1) the file path (and that it's live), (2) a 4–5 line summary of what's in it, (3) everything
  flagged as uncertain during review.
