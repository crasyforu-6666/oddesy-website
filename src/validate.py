#!/usr/bin/env python3
"""Quality gate for blog posts. Run before every publish:

    python3 src/validate.py            # check every post
    python3 src/validate.py <slug>...  # check specific posts (stricter: new-post rules)

Exits non-zero and prints every problem if anything fails.
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import SERVICES  # noqa: E402
from posts import CATEGORIES, POSTS_DIR, parse  # noqa: E402

MIN_WORDS_NEW = 1000
MIN_WORDS_ANY = 700
SIMILARITY_LIMIT = 0.25
BANNED = [
    "in today's fast-paced", "in today’s fast-paced", "delve", "game-changer", "game changer", "unlock the power",
    "in conclusion", "ever-evolving", "ever evolving", "navigate the complexities", "look no further",
    "revolutionize", "revolutionise", "seamlessly integrate", "it's important to note", "it is important to note",
    "in the realm of", "tapestry", "embark on", "unleash", "supercharge", "lorem ipsum", "as an ai",
]
SERVICE_SLUGS = {s["slug"] for s in SERVICES}
STATIC_PATHS = {"/", "/about/", "/services/", "/industries/", "/careers/", "/contact/", "/privacy-policy/", "/blog/"} | {
    f"/services/{s}/" for s in SERVICE_SLUGS}


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip().lower()


def shingles(text, k=6):
    w = re.findall(r"[a-z0-9]+", text)
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def check(post, all_posts, strict):
    errs = []
    slug = post["slug"]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) or len(slug) > 70:
        errs.append("slug must be lowercase words joined by hyphens, max 70 chars")
    if len(post["title"]) > 60:
        errs.append(f"title is {len(post['title'])} chars (max 60)")
    if not 110 <= len(post["description"]) <= 160:
        errs.append(f"description is {len(post['description'])} chars (need 110-160)")
    if len(post["h1"]) > 110:
        errs.append("h1 longer than 110 chars")
    if post["category"] not in CATEGORIES:
        errs.append(f"category '{post['category']}' not in {CATEGORIES}")
    bad_svc = [s for s in post["services"] if s not in SERVICE_SLUGS]
    if bad_svc:
        errs.append(f"unknown services: {bad_svc}")
    for k in ("date", "updated"):
        try:
            date.fromisoformat(post[k])
        except ValueError:
            errs.append(f"{k} is not YYYY-MM-DD")
    if post["updated"] < post["date"]:
        errs.append("updated is earlier than date")
    if not 2 <= len(post["faq"]) <= 5 or any(not q or not a for q, a in post["faq"]):
        errs.append("need 2-5 faq lines in the form 'faq: Question? || Answer.'")

    body = post["body"]
    min_words = MIN_WORDS_NEW if strict else MIN_WORDS_ANY
    if post["words"] < min_words:
        errs.append(f"only {post['words']} words (min {min_words})")
    if re.search(r"<h1[\s>]", body, re.I):
        errs.append("body must not contain <h1> (the page already has one)")
    if len(re.findall(r"<h2[\s>]", body, re.I)) < 3:
        errs.append("body needs at least 3 <h2> sections")
    if re.search(r"<script|<style|style=|<iframe|onclick=", body, re.I):
        errs.append("no scripts, iframes or inline styles in posts")
    if re.search(r"<table", body, re.I) and body.count('class="table-wrap"') < body.lower().count("<table"):
        errs.append('wrap every <table> in <div class="table-wrap">')
    lower = text_of(body + " " + post["title"] + " " + post["description"])
    hits = [b for b in BANNED if b in lower]
    if hits:
        errs.append(f"banned filler phrases: {hits}")
    if re.search(r"\b(TODO|TBD|XXX|\[insert|\[citation)", body, re.I):
        errs.append("placeholder text left in body")

    # links
    known = STATIC_PATHS | {f"/blog/{p['slug']}/" for p in all_posts}
    internal = re.findall(r'href="(/[^"#?]*)', body)
    broken = [h for h in internal if h not in known]
    if broken:
        errs.append(f"broken internal links: {broken}")
    if strict and len(set(internal)) < 3:
        errs.append("link to at least 3 different internal pages (services and other posts)")
    for h in re.findall(r'href="(https?://[^"]+)"', body):
        if h.startswith("http://"):
            errs.append(f"external link must be https: {h}")

    # uniqueness
    others = [p for p in all_posts if p["slug"] != slug]
    if any(p["keyword"].strip().lower() == post["keyword"].strip().lower() for p in others):
        errs.append(f"keyword '{post['keyword']}' already targeted by another post")
    if any(p["title"].lower() == post["title"].lower() for p in others):
        errs.append("title duplicates another post")
    mine = shingles(text_of(body))
    for p in others:
        theirs = shingles(text_of(p["body"]))
        if mine and theirs:
            sim = len(mine & theirs) / len(mine | theirs)
            if sim > SIMILARITY_LIMIT:
                errs.append(f"too similar to '{p['slug']}' ({sim:.0%} overlap)")
    return errs


def main(argv):
    all_posts = [parse(p) for p in sorted(POSTS_DIR.glob("*.html"))]
    targets = [p for p in all_posts if p["slug"] in argv] if argv else all_posts
    if argv and len(targets) != len(argv):
        found = {p["slug"] for p in targets}
        print(f"Not found: {[a for a in argv if a not in found]}")
        return 1
    failed = 0
    for p in targets:
        errs = check(p, all_posts, strict=bool(argv))
        if errs:
            failed += 1
            print(f"FAIL {p['slug']}")
            for x in errs:
                print(f"   - {x}")
        else:
            print(f"ok   {p['slug']} ({p['words']} words)")
    print(f"\n{len(targets) - failed}/{len(targets)} posts passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
