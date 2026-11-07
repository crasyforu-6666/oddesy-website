#!/usr/bin/env python3
"""Checks the built site in public/ before deploying.

Every indexable page must have exactly one <h1>, a unique title (<= 65 chars) and
meta description (<= 165 chars), a canonical URL, valid JSON-LD, and no broken
internal links.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ""
        self.desc = ""
        self.canonical = ""
        self.noindex = False
        self.links = []
        self.ld = []
        self._in_title = False
        self._in_ld = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", ""):
            self.noindex = True
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "a" and a.get("href", "").startswith("/"):
            self.links.append(a["href"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self.ld.append(self._buf)
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._buf += data


def exists(href):
    path = href.split("#")[0].split("?")[0]
    target = PUBLIC / path.lstrip("/")
    return target.is_file() or (target / "index.html").is_file()


def main():
    errors, titles, descs, count = [], {}, {}, 0
    for f in sorted(PUBLIC.rglob("*.html")):
        rel = "/" + str(f.relative_to(PUBLIC)).replace("index.html", "")
        p = Page()
        p.feed(f.read_text(encoding="utf-8"))
        if p.noindex:
            continue
        count += 1
        if p.h1 != 1:
            errors.append(f"{rel}: {p.h1} <h1> tags")
        if not p.title or len(p.title) > 65:
            errors.append(f"{rel}: title length {len(p.title)}")
        if not p.desc or len(p.desc) > 165:
            errors.append(f"{rel}: description length {len(p.desc)}")
        if not p.canonical:
            errors.append(f"{rel}: missing canonical")
        if p.title in titles:
            errors.append(f"{rel}: duplicate title with {titles[p.title]}")
        if p.desc in descs:
            errors.append(f"{rel}: duplicate description with {descs[p.desc]}")
        titles.setdefault(p.title, rel)
        descs.setdefault(p.desc, rel)
        for block in p.ld:
            try:
                json.loads(block)
            except ValueError:
                errors.append(f"{rel}: invalid JSON-LD")
        for href in set(p.links):
            if not exists(href):
                errors.append(f"{rel}: broken link {href}")
    sitemap = (PUBLIC / "sitemap.xml").read_text()
    for loc in re.findall(r"<loc>https://[^/]+(/[^<]*)</loc>", sitemap):
        if not exists(loc):
            errors.append(f"sitemap lists missing page {loc}")
    for e in errors:
        print("ERROR", e)
    print(f"Checked {count} indexable pages: {'OK' if not errors else str(len(errors)) + ' problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
