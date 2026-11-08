#!/usr/bin/env python3
"""Fetch a Come, Follow Me (or Scripture Helps) page and dump it as plain Markdown.

Usage:
    python3 template/fetch_outline.py 47                    # weekly outline, week 47 (2026 OT)
    python3 template/fetch_outline.py <full-url> [-o out.md]
    python3 template/fetch_outline.py --file saved.html

Prints the page title, every heading (marked [SEMINARY] / [CHILDREN] when the
manual's icon sits beside it), paragraphs, list items, and links as
[text](url). The output is research input, not handout text: read it, then
write the handout's Section 4 from it.
"""
import argparse, re, sys, urllib.request
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:  # pragma: no cover
    sys.exit("fetch_outline.py needs BeautifulSoup: pip install beautifulsoup4")

BASE = "https://www.churchofjesuschrist.org"
MANUAL = BASE + "/study/manual/come-follow-me-for-home-and-church-old-testament-2026/{}?lang=eng"
UA = "Mozilla/5.0 (cfm-handout-builder)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def inline(node, base):
    """Text of a node with links rendered as [text](url)."""
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif isinstance(c, Tag):
            if c.name == "a" and c.get("href"):
                t = inline(c, base).strip()
                out.append(f"[{t}]({urljoin(base, c['href'])})" if t else "")
            elif c.name in ("sup",) and "marker" in " ".join(c.get("class", [])):
                continue
            elif c.name == "img":
                alt = (c.get("alt") or "").lower()
                if "seminary" in alt:
                    out.append(" [SEMINARY ICON] ")
            else:
                out.append(inline(c, base))
    return re.sub(r"\s+", " ", "".join(out))


def dump(html, url):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("div", class_="body-block") or soup.find("article") or soup.body
    lines = []
    title = soup.find("h1")
    if title:
        lines.append("# " + title.get_text(" ", strip=True))
    for el in soup.select("p.title-number, p.intro, p.kicker, p.subtitle"):
        lines.append("> " + inline(el, url).strip())
    pending_flag = ""
    for el in body.find_all(["h2", "h3", "h4", "h5", "p", "li", "img", "figcaption"]):
        if el.name == "img":
            if el.find_parent(["h2", "h3", "h4", "h5"]):
                continue  # inline icon: already printed as [SEMINARY ICON]
            alt = (el.get("alt") or "").lower()
            if "seminary" in alt:
                pending_flag = "[SEMINARY] "
            elif "children section" in alt:
                pending_flag = "[CHILDREN] "
            continue
        if el.name == "p" and el.find_parent(["li", "figcaption"]):
            continue  # printed via the li
        text = inline(el, url).strip()
        if not text:
            continue
        if el.name in ("h2", "h3", "h4", "h5"):
            lvl = int(el.name[1])
            lines.append("")
            lines.append("#" * lvl + " " + pending_flag + text)
            pending_flag = ""
        elif el.name == "li":
            lines.append("- " + text)
        elif el.name == "figcaption":
            lines.append("_[figure] " + text + "_")
        else:
            lines.append(text)
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="week number or URL")
    ap.add_argument("--file", help="read a saved HTML file instead of fetching")
    ap.add_argument("-o", "--out", help="write Markdown here")
    a = ap.parse_args()
    if a.file:
        html, url = open(a.file, encoding="utf-8").read(), BASE
    else:
        url = MANUAL.format(a.target) if a.target and a.target.isdigit() else a.target
        if not url:
            ap.error("give a week number, a URL, or --file")
        html = fetch(url)
    md = f"<!-- source: {url} -->\n" + dump(html, url)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
        print(f"wrote {a.out} ({len(md)} chars)")
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
