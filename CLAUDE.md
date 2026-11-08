# Come, Follow Me lesson site — project rules

Weekly lesson handouts for a youth Sunday School class (ages 12–13), The Church of Jesus Christ
of Latter-day Saints, following *Come, Follow Me—For Home and Church*. Published as a static
site (`index.html` home page → month → week hub pages).

**Any request for a lesson or handout ("this week's lesson," "next week's," a date, a week number,
a scripture block) → use the `cfm-handout` skill (`.claude/skills/cfm-handout/SKILL.md`) and run
the whole workflow.** Don't build a handout freehand.

## Layout

```
CLAUDE.md                         this file
.claude/skills/cfm-handout/       the weekly workflow (Parts 2–7)
examples/                         ezekiel-handout.html, daniel-handout.html: the quality bar
template/base.css                 shared design system (extracted from the examples)
template/build.py                 helpers + builder + publisher (home list, week hub, badge)
template/scripture.py             parse/link references; fetch real verse text; check quotes
template/fetch_outline.py         official outline / Scripture Helps → Markdown
template/week.py                  which week is it (Monday–Sunday, taught on the ending Sunday)
template/render_check.js          Playwright: 1000px + 390px screenshots, overflow, print/PDF
handouts/<year>/NN-slug.html      built handouts (one per week)
handouts/<year>/src/NN-slug.py    each handout's content (the LESSON data)
notes/research-log.md             sources per week (append, never overwrite)
notes/outlines/                   fetched outline + Scripture Helps text per week
lessons/<year> - <volume>/…       existing month/week hub pages (+ older handouts, quizzes)
race/                             the Scripture Race reading game (don't touch for lessons)
```

## Non-negotiables

1. **Right week.** Use the real date (`date`, `template/week.py`). Weeks run Mon–Sun and are
   taught on the Sunday that ends them. Confirm the week number against the date range on the
   manual page. If the request is ambiguous, state the week and block before building.
2. **Real research.** Fetch the official outline and Scripture Helps every time; read the actual
   chapters; verify history in ≥2 reputable sources; ≥2 archaeology anchors; log sources in
   `notes/research-log.md`.
3. **Five sections in order:** Historical Summary · Passage Summary · Book of Mormon Parallels
   (Cross-Scripture Connections in BoM/D&C years) · Tie to Come, Follow Me (mirrors the outline) ·
   Tie to Jesus Christ.
4. **Design:** content in the data file, layout in `build.py`/`base.css`. A lesson overrides only
   the 13 `:root` colour tokens. New palette + one SVG motif from the passage's imagery each week.
   Minimal, responsive to 390px, print-friendly, one self-contained file, no external images.
5. **Review before done:** check every reference's real text, every quotation, nothing invented,
   doctrine faithful and interpretations labelled, debated scholarship shown as debated, no
   unverified current callings, age-appropriate. Section 4 matches the fetched outline.
6. **Render check:** `node template/render_check.js …` and *look at* the screenshots and PDF.

## Gotchas

- Handouts contain two `<style>` blocks; the first is inside `<noscript>`. Never grab "the first
  `<style>`". Use `build.py extract-css` (strips `<noscript>`, takes the largest block).
- Print: `.reveal` must be forced visible with `!important` *and* `transition:none`, or a quick
  print can capture a half-faded section. Sections must be allowed to break across pages.
- Network: the sandbox allowlist needs `www.churchofjesuschrist.org` (and reference sites). A
  proxy 403 means the host isn't allowed. Ask to add it; never fill gaps from memory.
- Don't edit `index.html` between the `cfm-handouts` markers by hand; `build.py` regenerates it.
- Commit and push to the session's working branch only; no PRs unless asked.
