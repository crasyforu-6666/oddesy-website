"""Load blog posts from src/posts/*.html.

File format (front matter, a line with ---, then the HTML body):

    title: <SEO title, max 60 chars>
    description: <meta description, 120-160 chars>
    h1: <on-page headline>
    summary: <1-2 sentence teaser shown on cards>
    date: YYYY-MM-DD            (posts dated in the future are not published yet)
    updated: YYYY-MM-DD
    category: <one of CATEGORIES>
    keyword: <primary search phrase>
    services: <service slug>, <service slug>
    faq: <question> || <answer>     (repeat 2-4 times)
    ---
    <p>Body HTML using h2, h3, p, ul, ol, table (wrapped in div.table-wrap), a, strong.</p>
"""
import re
from datetime import date
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent / "posts"

CATEGORIES = [
    "Migration",
    "Cloud & RISE",
    "Finance",
    "Logistics & Supply Chain",
    "Development & BTP",
    "Integration",
    "AI & Innovation",
    "Support & Operations",
    "Careers & Skills",
    "Industry",
]

REQUIRED = ["title", "description", "h1", "summary", "date", "updated", "category", "keyword", "services"]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse(path):
    raw = path.read_text(encoding="utf-8")
    head, sep, body = raw.partition("\n---\n")
    if not sep:
        raise ValueError(f"{path.name}: missing '---' separator line")
    meta = {"faq": [], "slug": path.stem, "file": path}
    for line in head.splitlines():
        if not line.strip():
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if key == "faq":
            q, _, a = val.partition("||")
            meta["faq"].append((q.strip(), a.strip()))
        else:
            meta[key] = val
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        raise ValueError(f"{path.name}: missing {', '.join(missing)}")
    meta["services"] = [s.strip() for s in meta["services"].split(",") if s.strip()]
    meta["body"] = body.strip()
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    meta["words"] = words
    meta["minutes"] = max(3, round(words / 220))
    meta["cat_slug"] = slugify(meta["category"])
    return meta


def load(include_future=False, today=None):
    today = today or date.today().isoformat()
    posts = [parse(p) for p in sorted(POSTS_DIR.glob("*.html"))]
    if not include_future:
        posts = [p for p in posts if p["date"] <= today]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts
