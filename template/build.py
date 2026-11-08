#!/usr/bin/env python3
"""Come, Follow Me handout builder.

Content lives in a lesson data file (handouts/<year>/src/<NN>-<slug>.py) that
defines LESSON = {...} using the helpers below. Layout lives here. The output
is one self-contained HTML file with template/base.css inlined and only the
lesson's colour tokens overridden in :root.

Commands
    python3 template/build.py build handouts/2026/src/47-hosea-joel.py
        → writes handouts/2026/47-hosea-joel.html, then updates the home page
          list, the week hub page, and the week's badge on the home page.
    python3 template/build.py add examples/daniel-handout.html --week 46 --slug daniel \
        --dates "November 9–15" --start 2026-11-09 --block "Daniel 1–7" \
        --title "There Is No Other God That Can Deliver"
        → publishes a hand-made handout the same way (meta tags, hub link, badge, list).
    python3 template/build.py index
        → regenerates only the home-page "Latest handouts" list.
    python3 template/build.py extract-css examples/daniel-handout.html
        → prints the main <style> block of an existing handout (never the one
          inside <noscript>), for refreshing base.css.

Text markup inside content strings (everything is HTML-escaped first):
    **bold**   *italic*   [[Hosea 2:14–15]]   [[Hosea 2:14–15|vv. 14–15]]
    A [[ref]] becomes a Gospel Library link; a bad reference stops the build.
"""
import html, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "template"))
import scripture  # noqa: E402

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;'
         '9..144,500;9..144,600;9..144,700;9..144,900&family=Inter:wght@400;500;600;700;800'
         '&display=swap" rel="stylesheet">')
NOSCRIPT = '<noscript><style>.reveal{opacity:1!important;transform:none!important;}</style></noscript>'
TOKEN_NAMES = ["night", "night-2", "accent", "accent-soft", "gold", "parch", "parch-2", "ink",
               "ink-soft", "echo", "echo-soft", "gold-soft", "line"]

# ------------------------------------------------------------------ text
_WARNINGS = []


def warn(msg):
    _WARNINGS.append(msg)


def fmt(s):
    """Escape, then apply the mini-markup. Returns HTML."""
    if s is None:
        return ""
    out = html.escape(str(s), quote=False)

    def ref(m):
        ref_txt = html.unescape(m.group(1)).strip()
        label = m.group(2)
        return scripture.link(ref_txt, label.strip() if label else html.escape(ref_txt, quote=False))
    out = re.sub(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]", ref, out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out)
    return out


def paras(*texts):
    return "".join(f"<p>{fmt(t)}</p>" for t in texts if t)


# ------------------------------------------------------------------ block helpers
# Each returns an HTML string; a lesson's section body is a list of these.

def p(text):
    return f"<p>{fmt(text)}</p>"


def lead(text):
    return f'<p class="lead">{fmt(text)}</p>'


def h3(text):
    return f'<h3 style="margin-top:24px">{fmt(text)}</h3>'


def card(tag, *texts, warm=False):
    """Callout card. warm=True for 'hard questions' / honest notes."""
    cls = "card warm" if warm else "card"
    return f'<div class="{cls}"><span class="tag">{fmt(tag)}</span>{paras(*texts)}</div>'


def pull(quote, cite):
    """Short KJV pull-quote. Keep it to one verse or less."""
    if len(quote) > 160:
        warn(f"pull-quote is {len(quote)} chars — keep KJV quotations short")
    return f'<blockquote class="pull">“{fmt(quote)}”<cite>{fmt(cite)}</cite></blockquote>'


def steps(items):
    """Numbered passage timeline. items: [(verse_ref_text, heading, body), ...]"""
    rows = []
    for i, (vv, head, body) in enumerate(items, 1):
        rows.append(f'<div class="step"><span class="badge">{i}</span><div class="vv">{fmt(vv)}</div>'
                    f'<h3>{fmt(head)}</h3><p>{fmt(body)}</p></div>')
    return '<div class="tl">' + "".join(rows) + "</div>"


def parallel_cards(items):
    """Two-part parallel cards.
    items: [dict(k_ref=, k=, b_ref=, b=, teaches=), ...]  (k = passage, b = echo)"""
    if not 8 <= len(items) <= 10:
        warn(f"{len(items)} parallel cards (aim for 8–10)")
    cards = []
    for it in items:
        cards.append(
            '<div class="pcard">'
            f'<div class="row k"><div class="mini">{fmt(it["k_ref"])}</div><p>{fmt(it["k"])}</p></div>'
            f'<div class="row b"><div class="mini">{fmt(it["b_ref"])}</div><p>{fmt(it["b"])}</p></div>'
            f'<div class="teach"><b>Teaches:</b> {fmt(it["teaches"])}</div></div>')
    return '<div class="grid">' + "".join(cards) + "</div>"


def points(items):
    """Outline principles. items: [(heading, body), ...] — heading shown bold."""
    lis = "".join(f"<li><strong>{fmt(h)}</strong> {fmt(b)}</li>" for h, b in items)
    return f'<ul class="points">{lis}</ul>'


def helps(items):
    """Scripture Helps questions. items: [(question, pointer_or_None), ...]"""
    lis = []
    for q, ptr in items:
        lis.append(f"<li>{fmt(q)}" + (f" <em>({fmt(ptr)})</em>" if ptr else "") + "</li>")
    return '<ul class="helps">' + "".join(lis) + "</ul>"


def resto(nodes):
    """Restoration mini-timeline. nodes: [(year, title, desc), ...] — 3–4 nodes."""
    if not 3 <= len(nodes) <= 4:
        warn(f"{len(nodes)} Restoration timeline nodes (aim for 3–4)")
    parts = []
    for yr, tt, ds in nodes:
        parts.append(f'<div class="rnode"><div class="yr">{fmt(yr)}</div><div class="tt">{fmt(tt)}</div>'
                     f'<div class="ds">{fmt(ds)}</div></div>')
    return '<div class="resto">' + '<div class="rarrow">▸</div>'.join(parts) + "</div>"


_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 6"/></svg>')


def ideas(items):
    """Teaching ideas for ages 12–13. items: [(title, body), ...] — 5–6 items."""
    if not 5 <= len(items) <= 6:
        warn(f"{len(items)} teaching ideas (aim for 5–6)")
    if not any(re.search(r"this week|invite", b, re.I) for _, b in items):
        warn("no teaching idea contains an invitation to act this week")
    lis = "".join(f"<li>{_CHECK}<strong>{fmt(t)}</strong> {fmt(b)}</li>" for t, b in items)
    return f'<ul class="ideas">{lis}</ul>'


def christ(entries):
    """Dark 'Tie to Jesus Christ' panel. entries: [(ref_line, heading, body), ...] — 4–6."""
    if not 4 <= len(entries) <= 6:
        warn(f"{len(entries)} Jesus Christ entries (aim for 4–6)")
    inner = "".join(f'<p class="ref">{fmt(r)}</p><h3>{fmt(h)}</h3><p>{fmt(b)}</p>' for r, h, b in entries)
    return f'<div class="christ">{inner}</div>'


def raw(html_str):
    """Escape hatch for a one-off bit of HTML (use sparingly)."""
    return html_str


# ------------------------------------------------------------------ page
ICONS = [
    '<path d="M4 19V6a2 2 0 0 1 2-2h9l5 5v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2Z"/><path d="M14 4v5h5"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    '<path d="M12 6c-1.6-1.2-3.6-2-6-2v13c2.4 0 4.4.8 6 2"/><path d="M12 6c1.6-1.2 3.6-2 6-2v13c-2.4 0-4.4.8-6 2"/><path d="M12 6v13"/>',
    '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5 5-2Z"/>',
    '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
]
PRINT_BTN = ('<button class="printbtn" onclick="window.print()" aria-label="Print handout"><svg width="16" '
             'height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 '
             '0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v8H6z"/></svg>'
             'Print</button>')
# Scroll reveal with failsafes: no IntersectionObserver → show; beforeprint → show; 2.5 s → show.
REVEAL_JS = """<script>(function(){var els=document.querySelectorAll('.reveal');function showAll(){els.forEach(function(el){el.classList.add('in');});}
if(!('IntersectionObserver' in window)){showAll();return;}var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.08,rootMargin:'0px 0px -5% 0px'});
els.forEach(function(el){io.observe(el);});window.addEventListener('beforeprint',showAll);if(window.matchMedia){var mq=window.matchMedia('print');if(mq.addListener)mq.addListener(function(m){if(m.matches)showAll();});}setTimeout(showAll,2500);})();</script>"""


def section_titles(volume):
    third = ("Book of Mormon Parallels" if volume in ("Old Testament", "New Testament")
             else "Cross-Scripture Connections")
    return ["Historical Summary of the Period", "Passage Summary", third,
            "Tie to Come, Follow Me", "Tie to Jesus Christ"]


def section(num, title, blocks):
    body = "\n".join(blocks)
    return (f'<section class="block reveal"><div class="sec-head"><span class="sec-num">{num}</span>\n'
            f'<svg class="sec-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[num - 1]}</svg>\n'
            f'<h2 class="sec">{title}</h2></div><div class="rule"></div>\n{body}\n</section>')


def hero(L):
    h = L["hero"]
    return (f'<header class="hero"><div class="hero-inner"><div>\n'
            f'<div class="eyebrow">Come, Follow Me · {L["volume"]} {L["year"]} · Youth Sunday School</div>'
            f'<h1>{fmt(h["h1"])}</h1><p class="kicker">{fmt(h["kicker"])}</p>\n'
            f'<span class="theme-chip"><b>“{fmt(L["outline_title"])}”</b> · {fmt(L["dates"])}</span>'
            f'<p class="hook">{fmt(h["hook"])}</p></div>\n'
            f'<div class="hero-art" aria-hidden="true">{h["svg"]}</div></div></header>')


def band(L):
    b = L["band"]
    if not 4 <= len(b["events"]) <= 6:
        warn(f'{len(b["events"])} timeline-band events (aim for about 5)')
    stops = ['<div class="stop"><div class="dot"></div>'
             f'<div class="nm">{fmt(d)}</div><div class="ds">{fmt(t)}</div></div>' for d, t in b["events"]]
    return (f'<div class="band"><div class="journey"><span class="jlabel">{fmt(b["label"])}</span>'
            + '<div class="arrow">▸</div>'.join(stops) + "</div></div>")


def tokens_css(tokens):
    unknown = set(tokens) - set(TOKEN_NAMES)
    if unknown:
        raise SystemExit(f"unknown colour tokens: {sorted(unknown)} (allowed: {TOKEN_NAMES})")
    missing = [t for t in TOKEN_NAMES if t not in tokens]
    if missing:
        warn(f"palette leaves these tokens at base.css defaults: {missing}")
    return ":root{" + "".join(f"--{k}:{v};" for k, v in tokens.items()) + "}"


def page(L):
    css = open(os.path.join(ROOT, "template", "base.css"), encoding="utf-8").read()
    secs = L["sections"]
    if len(secs) != 5:
        raise SystemExit(f"a handout has exactly five sections, got {len(secs)}")
    titles = section_titles(L["volume"])
    body = "\n".join(section(i + 1, titles[i], blocks) for i, blocks in enumerate(secs))
    meta = "".join(f'<meta name="cfm:{k}" content="{html.escape(str(v))}">' for k, v in [
        ("year", L["year"]), ("week", L["week"]), ("dates", L["dates"]),
        ("block", L["scripture_block"]), ("outline-title", L["outline_title"]), ("start", L["start"])])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{html.escape(L["title"])}</title>
{meta}
{FONTS}
{NOSCRIPT}
<style>
{css}
/* ---- this lesson's palette ({html.escape(L.get("palette_note", ""))}) ---- */
{tokens_css(L["tokens"])}
</style></head><body>
{hero(L)}
{band(L)}
<div class="wrap">
{body}
</div>
<footer><div class="wrap"><b>{fmt(L["scripture_block"])} — “{fmt(L["outline_title"])}.”</b> Sources: {fmt(L["sources"])} Prepared for youth Sunday School, ages 12–13.</div></footer>
{PRINT_BTN}
{REVEAL_JS}
</body></html>
"""


# ------------------------------------------------------------------ CSS extraction
def extract_main_style(doc):
    """Return the handout's main stylesheet.

    The examples carry TWO <style> blocks: a tiny one inside <noscript> that
    comes first, and the real one. Searching for the first <style> grabs the
    wrong block, so strip <noscript> sections first and take the largest
    remaining <style>."""
    no_ns = re.sub(r"<noscript\b.*?</noscript>", "", doc, flags=re.S | re.I)
    blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", no_ns, flags=re.S | re.I)
    if not blocks:
        raise SystemExit("no <style> block found outside <noscript>")
    return max(blocks, key=len).strip("\n")


# ------------------------------------------------------------------ publishing
def load_lesson(path):
    spec = importlib.util.spec_from_file_location("lesson", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LESSON


def out_path(L):
    return os.path.join(ROOT, "handouts", str(L["year"]), f'{L["week"]:02d}-{L["slug"]}.html')


def read_meta(path):
    doc = open(path, encoding="utf-8").read()
    meta = dict(re.findall(r'<meta name="cfm:([\w-]+)" content="([^"]*)">', doc))
    meta["path"] = os.path.relpath(path, ROOT).replace(os.sep, "/")
    return meta


IDX_START, IDX_END = "<!-- cfm-handouts:start -->", "<!-- cfm-handouts:end -->"


def rebuild_index():
    """Regenerate the newest-first handout list on the home page (between markers)."""
    idx = os.path.join(ROOT, "index.html")
    doc = open(idx, encoding="utf-8").read()
    if IDX_START not in doc:
        raise SystemExit("index.html has no cfm-handouts markers")
    items = []
    hroot = os.path.join(ROOT, "handouts")
    for year in sorted(os.listdir(hroot)) if os.path.isdir(hroot) else []:
        ydir = os.path.join(hroot, year)
        if not os.path.isdir(ydir):
            continue
        for f in os.listdir(ydir):
            if f.endswith(".html"):
                items.append(read_meta(os.path.join(ydir, f)))
    items.sort(key=lambda m: (int(m.get("year", 0)), int(m.get("week", 0))), reverse=True)
    lis = "\n".join(
        f'      <li><a href="{html.escape(m["path"])}"><span class="lh-dates">{m.get("dates", "")}</span>'
        f'<span class="lh-scrip">{m.get("block", "")}</span>'
        f'<span class="lh-title">&ldquo;{m.get("outline-title", "")}&rdquo;</span></a></li>' for m in items)
    block = (f'{IDX_START}\n  <div class="wrap latest" id="latest">\n'
             f'    <div class="m-head"><h2>Latest handouts</h2><span class="count">{len(items)} built</span></div>\n'
             f'    <ul class="lh">\n{lis}\n    </ul>\n  </div>\n  {IDX_END}')
    doc = doc[:doc.index(IDX_START)] + block + doc[doc.index(IDX_END) + len(IDX_END):]
    open(idx, "w", encoding="utf-8").write(doc)
    print(f"index.html: {len(items)} handout(s) listed, newest first")


def link_week_hub(L, out):
    """Add the handout to its week hub page and mark the week ready on the home page."""
    hub_dir = L.get("week_hub")
    if not hub_dir:
        return
    hub = os.path.join(ROOT, hub_dir, "index.html")
    if not os.path.exists(hub):
        warn(f"week hub not found: {hub_dir}")
        return
    doc = open(hub, encoding="utf-8").read()
    rel = os.path.relpath(out, os.path.join(ROOT, hub_dir)).replace(os.sep, "/")
    if rel not in doc:
        li = (f'      <li><a href="{rel}">\n        <span class="fico html">HTML</span>\n'
              f'        <span><span class="fname">{html.escape(L["scripture_block"])} &mdash; Lesson Handout</span>'
              f'<br><span class="fkind">Web handout — view &amp; print</span></span>\n      </a></li>\n')
        if '<ul class="files">' in doc:
            doc = doc.replace('<ul class="files">\n', '<ul class="files">\n' + li, 1)
        else:
            doc = re.sub(r'<p class="empty">.*?</p>', '<ul class="files">\n' + li + '    </ul>', doc, count=1, flags=re.S)
        open(hub, "w", encoding="utf-8").write(doc)
        print(f"linked from {hub_dir}/index.html")
    n = doc.count('<span class="fico')
    # home-page week card
    idx = os.path.join(ROOT, "index.html")
    home = open(idx, encoding="utf-8").read()
    href = f'href="{hub_dir}/index.html"'
    m = re.search(r'<a class="wcard[^"]*" ' + re.escape(href) + r'>(.*?)</a>', home, flags=re.S)
    if not m:
        warn("week card not found on home page")
        return
    card_html = m.group(0)
    new = card_html.replace('<a class="wcard"', '<a class="wcard ready"', 1)
    new = re.sub(r'<span class="badge [^"]*">[^<]*</span>',
                 f'<span class="badge ready">{n} handout{"s" if n != 1 else ""}</span>', new, count=1)
    home2 = home.replace(card_html, new, 1)
    # month pill in the top nav: highlight months that have materials
    month = os.path.basename(os.path.dirname(hub_dir.rstrip("/"))).lower()
    home2 = home2.replace(f'<a href="#{month}">', f'<a href="#{month}" class=has>', 1)
    if home2 != home:
        open(idx, "w", encoding="utf-8").write(home2)
        print(f"home page: week card marked ready ({n} handout{'s' if n != 1 else ''})")


def build(path):
    L = load_lesson(path)
    doc = page(L)
    out = out_path(L)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    print(f"wrote {os.path.relpath(out, ROOT)} ({len(doc) // 1024} KB)")
    link_week_hub(L, out)
    rebuild_index()
    for w in _WARNINGS:
        print("WARNING:", w)
    return out


PRINT_FIX = """
/* cfm-print-fix (added by build.py add) */
@media print{.reveal,.reveal.in{opacity:1!important;transform:none!important;transition:none!important;}
  section.block{break-inside:auto;} .sec-head,.rule,h3,.christ .ref,.step .vv{break-after:avoid;}
  .pull,.points li,.ideas li,.helps li,.resto,footer{break-inside:avoid;} .christ{break-inside:auto;}}
"""


def add_existing(src, year, week, slug, dates, start, block, title, volume="Old Testament", hub=None):
    """Publish a hand-made handout: copy it to handouts/<year>/NN-slug.html with cfm: meta tags,
    then link it from its week hub, mark the week ready, and refresh the home-page list."""
    doc = open(src, encoding="utf-8").read()
    doc = re.sub(r'<meta name="cfm:[^"]*" content="[^"]*">', "", doc)
    meta = "".join(f'<meta name="cfm:{k}" content="{html.escape(str(v))}">' for k, v in [
        ("year", year), ("week", week), ("dates", dates), ("block", block),
        ("outline-title", title), ("start", start)])
    doc = re.sub(r"(</title>)", r"\1\n" + meta.replace("\\", "\\\\"), doc, count=1)
    # older hand-made handouts lack the print fixes in base.css: add them to the main
    # stylesheet (the LAST </style>; the first one belongs to <noscript>)
    if "cfm-print-fix" not in doc:
        i = doc.rfind("</style>")
        doc = doc[:i] + PRINT_FIX + doc[i:]
    if hub is None:
        import week as wk  # template/week.py
        hub = wk.week_info(wk.week_end(__import__("datetime").date.fromisoformat(start)))["hub"]
    L = dict(year=year, week=week, slug=slug, scripture_block=block, week_hub=hub)
    out = out_path(L)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    print(f"wrote {os.path.relpath(out, ROOT)} (from {src})")
    link_week_hub(L, out)
    rebuild_index()
    for w in _WARNINGS:
        print("WARNING:", w)


def main(argv):
    if len(argv) >= 2 and argv[0] == "build":
        build(argv[1])
    elif argv[:1] == ["add"]:
        import argparse
        ap = argparse.ArgumentParser(prog="build.py add")
        ap.add_argument("src")
        for a in ("--week", "--slug", "--dates", "--start", "--block", "--title"):
            ap.add_argument(a, required=True)
        ap.add_argument("--year", type=int, default=2026)
        ap.add_argument("--volume", default="Old Testament")
        o = ap.parse_args(argv[1:])
        add_existing(o.src, o.year, int(o.week), o.slug, o.dates, o.start, o.block, o.title, o.volume)
    elif argv[:1] == ["index"]:
        rebuild_index()
    elif len(argv) >= 2 and argv[0] == "extract-css":
        print(extract_main_style(open(argv[1], encoding="utf-8").read()))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
