#!/usr/bin/env python3
"""Static site generator for the Oddesy Consulting and Services website.

Usage:  python3 src/build.py
Output: public/  (published to the gh-pages branch)

Edit copy in src/content.py; edit styles in src/assets/css/site.css.
"""
import hashlib
import html
import json
import shutil
from datetime import date
from pathlib import Path

from content import SITE, SERVICES, INDUSTRIES, TRAINING
from articles import ARTICLES

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "public"
BASE = f"https://{SITE['domain']}"
TODAY = date.today().isoformat()


def ver(rel):
    """Short content hash so browsers fetch new CSS/JS after every update."""
    return hashlib.md5((SRC / "assets" / rel).read_bytes()).hexdigest()[:8]
e = html.escape

# --------------------------------------------------------------------------
# Icons (24x24 stroke icons drawn for this site)
ICONS = {
    "rocket": '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 15l-3-3c1-4 4-9 13-9 0 9-5 12-9 13z"/><circle cx="15" cy="9" r="1.6"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .6-7.96A6 6 0 0 0 6.1 10.5 3.75 3.75 0 0 0 7 18z"/>',
    "migrate": '<path d="M4 7h12l-3-3"/><path d="M20 17H8l3 3"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1"/><path d="M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
    "code": '<path d="M8 8l-4 4 4 4"/><path d="M16 8l4 4-4 4"/><path d="M13.5 5l-3 14"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.9.4 5 2.8 5 5.8"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6 8.5-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "arrow": '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
    "arrow-ur": '<path d="M7 17L17 7"/><path d="M8 7h9v9"/>',
    "building": '<rect x="4" y="3" width="11" height="18"/><path d="M15 9h5v12h-5"/><path d="M7.5 7h4M7.5 11h4M7.5 15h4"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21a2 2 0 0 1 2-2h13v2"/><path d="M8 7h7M8 11h5"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5z"/>',
    "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONS[name]}</svg>')


AURORA = '<div class="aurora" aria-hidden="true"><span class="b1"></span><span class="b2"></span><span class="b3"></span></div><div class="grid-overlay" aria-hidden="true"></div>'

TECH = ["SAP S/4HANA", "RISE with SAP", "SAP BTP", "SAP Fiori", "Integration Suite", "ABAP Cloud",
        "SAP Analytics Cloud", "SAP Datasphere", "SuccessFactors", "SAP Ariba", "SAP EWM", "SAP Signavio",
        "SAP Build", "SAP Joule"]


# --------------------------------------------------------------------------
# Layout

TRAINING_LINK = f'<a href="{TRAINING["url"]}" target="_blank" rel="noopener">Training <span class="ext">{icon("arrow-ur")}</span><span class="sr">(opens in a new tab)</span></a>'


def nav_html(active):
    svc_links = "".join(
        f'<li><a href="/services/{s["slug"]}/"><span class="mi">{icon(s["icon"])}</span><span><strong>{e(s["nav"])}</strong>'
        f'<small>{e(s["summary"])}</small></span></a></li>' for s in SERVICES)

    def cur(key):
        return ' aria-current="page"' if active == key else ""
    return f'''
<header class="site-header">
  <div class="nav-shell">
    <a href="/" class="brand" aria-label="{e(SITE["name"])} home">
      <img src="/assets/img/logo-mark.svg" alt="" width="34" height="34">
      <span class="brand-text">Oddesy<span>Consulting &amp; Services</span></span>
    </a>
    <nav id="primary-nav" class="primary-nav" aria-label="Main">
      <ul class="menu">
        <li><a href="/about/"{cur("about")}>About</a></li>
        <li class="has-sub">
          <a href="/services/"{cur("services")} class="sub-trigger" aria-haspopup="true">Services <span class="caret" aria-hidden="true"></span></a>
          <div class="mega"><ul>{svc_links}</ul>
            <a class="mega-all" href="/services/">All SAP services {icon("arrow")}</a></div>
        </li>
        <li><a href="/industries/"{cur("industries")}>Industries</a></li>
        <li><a href="/insights/"{cur("insights")}>Insights</a></li>
        <li>{TRAINING_LINK}</li>
        <li><a href="/careers/"{cur("careers")}>Careers</a></li>
        <li><a href="/contact/"{cur("contact")}>Contact</a></li>
      </ul>
      <a href="/contact/" class="btn btn-glow btn-sm nav-cta">Book a call {icon("arrow-ur")}</a>
    </nav>
    <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu"><span></span><span></span></button>
  </div>
</header>'''


def cta_block():
    return f'''
<section class="section cta-section"><div class="container">
  <div class="cta-card reveal">
    {AURORA}
    <div class="cta-content">
      <p class="pill pill-dark"><span class="dot"></span>Free 30-minute consultation</p>
      <h2>Let's map your next <em>SAP move</em>.</h2>
      <p>Talk to a senior consultant about your landscape, timeline and options. Practical advice, no sales pitch.</p>
      <div class="hero-actions center-x">
        <a href="/contact/" class="btn btn-light">Book your consultation {icon("arrow-ur")}</a>
        <a href="mailto:{e(SITE["email"])}" class="btn btn-ghost">{icon("mail")}{e(SITE["email"])}</a>
      </div>
    </div>
  </div>
</div></section>'''


def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES)
    year = date.today().year
    return f'''
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <a href="/" class="brand"><img src="/assets/img/logo-mark.svg" alt="" width="34" height="34">
      <span class="brand-text">Oddesy<span>Consulting &amp; Services</span></span></a>
      <p>Independent SAP consultancy for implementation, migration, integration and support.</p>
      <a class="social" href="{e(SITE["linkedin"])}" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a>
    </div>
    <div><h2 class="footer-h">Services</h2><ul>{svc}</ul></div>
    <div><h2 class="footer-h">Company</h2><ul>
      <li><a href="/about/">About</a></li><li><a href="/industries/">Industries</a></li>
      <li><a href="/insights/">Insights</a></li><li>{TRAINING_LINK}</li>
      <li><a href="/careers/">Careers</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy</a></li></ul></div>
    <div><h2 class="footer-h">Get in touch</h2><ul class="footer-contact">
      <li><a href="mailto:{e(SITE["email"])}">{icon("mail")}{e(SITE["email"])}</a></li>
      <li><a href="tel:{e(SITE["phone_link"])}">{icon("phone")}{e(SITE["phone"])}</a></li>
      <li><span>{icon("pin")}{e(SITE["address"])}</span></li></ul></div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; {year} {e(SITE["name"])}</p>
    <p>SAP, S/4HANA, SAP BTP, RISE with SAP and other SAP products are trademarks of SAP SE. {e(SITE["short"])} is an independent consultancy.</p>
  </div>
  <div class="wordmark" aria-hidden="true">ODDESY</div>
</footer>'''


def breadcrumbs(trail):
    items = [("Home", "/")] + trail
    links = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            links.append(f'<li aria-current="page">{e(name)}</li>')
        else:
            links.append(f'<li><a href="{path}">{e(name)}</a></li>')
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p}
                                  for i, (n, p) in enumerate(items)]}
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(links)}</ol></nav>', schema


def org_schema():
    return {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "@id": BASE + "/#organization", "name": SITE["name"], "url": BASE + "/",
        "logo": BASE + "/assets/img/logo-mark.svg", "image": BASE + "/assets/img/og-image.png",
        "email": SITE["email"], "telephone": SITE["phone"],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["address"],
                    "addressLocality": SITE["city"], "addressCountry": SITE["country"]},
        "sameAs": [SITE["linkedin"]],
        "knowsAbout": ["SAP S/4HANA", "RISE with SAP", "SAP BTP", "SAP Integration Suite", "SAP AMS"],
    }


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


PAGES = []


def page(path, title, description, body, active="", schemas=(), cta=True, og_type="website"):
    url = BASE + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                   for s in [org_schema(), *schemas])
    robots = "noindex" if path == "/404.html" else "index, follow, max-image-preview:large"
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#070a14">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(SITE["name"])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/logo-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ver("css/site.css")}">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav_html(active)}
<main id="main">
{body}
{cta_block() if cta else ""}
</main>
{footer_html()}
<script>window.ODDESY = {json.dumps({"formEndpoint": SITE["form_endpoint"], "email": SITE["email"]})};</script>
<script src="/assets/js/site.js?v={ver("js/site.js")}" defer></script>
</body>
</html>
'''
    target = OUT / "404.html" if path == "/404.html" else OUT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    if path != "/404.html":
        PAGES.append(path)


# --------------------------------------------------------------------------
# Shared sections

def page_hero(crumbs_html, eyebrow, h1, lead, cta=True, accent=None):
    title = e(h1)
    if accent and accent in h1:
        title = e(h1).replace(e(accent), f"<em>{e(accent)}</em>", 1)
    btns = (f'<div class="hero-actions"><a href="/contact/" class="btn btn-glow">Talk to an SAP expert {icon("arrow-ur")}</a>'
            f'<a href="tel:{e(SITE["phone_link"])}" class="btn btn-ghost">{icon("phone")}{e(SITE["phone"])}</a></div>') if cta else ""
    return f'''<section class="page-hero dark">{AURORA}<div class="container hero-inner">
  {crumbs_html}
  <p class="pill"><span class="dot"></span>{e(eyebrow)}</p>
  <h1>{title}</h1>
  <p class="lead">{e(lead)}</p>
  {btns}
</div></section>'''


def section_head(eyebrow, title, sub="", center=True, accent=None):
    t = e(title)
    if accent and accent in title:
        t = t.replace(e(accent), f"<em>{e(accent)}</em>", 1)
    return (f'<div class="section-head{" center" if center else ""} reveal"><p class="eyebrow">{e(eyebrow)}</p>'
            f'<h2>{t}</h2>{f"<p>{e(sub)}</p>" if sub else ""}</div>')


def faq_html(faq, heading="Questions, answered"):
    items = "".join(f'<details class="reveal"><summary>{e(q)}<span class="plus">{icon("plus")}</span></summary><p>{e(a)}</p></details>'
                    for q, a in faq)
    return f'''<section class="section"><div class="container faq-wrap">
  <div class="faq-side reveal"><p class="eyebrow">FAQ</p><h2>{e(heading)}</h2>
  <p>Can't find what you're looking for? Our consultants are happy to help.</p>
  <a href="/contact/" class="btn btn-dark">Ask a question {icon("arrow-ur")}</a></div>
  <div class="faq">{items}</div></div></section>'''


def svc_card(s, cls="", h="h3", extra=""):
    return f'''<a class="bento-card spot reveal {cls}" href="/services/{s["slug"]}/">
  <span class="tile">{icon(s["icon"])}</span>
  <{h}>{e(s["name"])}</{h}><p>{e(s["summary"])}</p>{extra}
  <span class="go" aria-hidden="true">{icon("arrow-ur")}</span></a>'''


def services_bento(h="h3"):
    s = SERVICES
    phases = '<div class="phase-pills" aria-hidden="true">' + "".join(
        f'<span class="{c}">{n}</span>' for n, c in
        [("Discover", "done"), ("Prepare", "done"), ("Explore", "done"), ("Realize", "now"), ("Deploy", ""), ("Run", "")]) + "</div>"
    nodes = '<div class="mini-int" aria-hidden="true"><span>CRM</span><span>Bank</span><i></i><b>SAP</b><i></i><span>Web</span><span>EDI</span></div>'
    return f'''<div class="bento">
  {svc_card(s[0], "b-lg", h, phases)}
  {svc_card(s[1], "b-md", h)}
  {svc_card(s[2], "b-md", h)}
  {svc_card(s[3], "b-sm", h, nodes)}
  {svc_card(s[4], "b-sm", h)}
  {svc_card(s[5], "b-sm", h)}
  {svc_card(s[6], "b-wide", h)}
</div>'''


ACTIVATE = [("Discover", "Explore what S/4HANA can do for you and build a business case leadership can sign off."),
            ("Prepare", "Mobilise the team, plan, governance and system landscape."),
            ("Explore", "Fit-to-standard workshops confirm processes and surface real gaps early."),
            ("Realize", "Configure, build, migrate data and test in short, visible sprints."),
            ("Deploy", "Train users, rehearse cut-over and go live with confidence."),
            ("Run", "Hypercare, AMS support and continuous improvement after go-live.")]


def process_html():
    steps = "".join(f'<li class="step"><span class="node">{i + 1:02d}</span><div><h3>{n}</h3><p>{d}</p></div></li>'
                    for i, (n, d) in enumerate(ACTIVATE))
    return f'''<section class="section"><div class="container process">
  <div class="process-side reveal"><p class="eyebrow">How we deliver</p>
    <h2>A proven path from <em>discovery</em> to run</h2>
    <p>Every engagement follows SAP Activate, SAP's standard methodology, so you always know where you are and what comes next.</p>
    <a href="/contact/" class="btn btn-dark">Plan your project {icon("arrow-ur")}</a></div>
  <ol class="steps">{steps}</ol>
</div></section>'''


WHY = [("target", "Senior-led delivery", "Experienced consultants lead from the first workshop to go-live."),
       ("layers", "Clean-core mindset", "Close to standard, so upgrades stay simple and cheap."),
       ("chart", "Radical transparency", "Weekly status, clear milestones, early warning on risk."),
       ("shield", "Quality and security", "Peer-reviewed configuration and code, security built in."),
       ("clock", "On-time delivery", "Realistic plans and disciplined execution."),
       ("users", "Flexible engagement", "Fixed price, time and materials or a dedicated team.")]


def why_html(title="Why teams choose Oddesy", accent="Oddesy"):
    cards = "".join(f'<div class="feature spot reveal"><span class="tile">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>'
                    for i, t, d in WHY)
    return f'''<section class="section"><div class="container">
  {section_head("Why us", title, accent=accent)}
  <div class="feature-grid">{cards}</div></div></section>'''


def marquee():
    items = "".join(f"<li>{icon('spark')}{t}</li>" for t in TECH)
    return f'''<section class="marquee" aria-label="SAP technologies we work with">
  <div class="marquee-track"><ul>{items}</ul><ul aria-hidden="true">{items}</ul></div></section>'''


def countdown():
    return f'''<section class="section dark countdown-sec">{AURORA}<div class="container countdown-wrap">
  <div class="reveal">
    <p class="pill"><span class="dot warn"></span>Deadline</p>
    <h2>SAP ECC mainstream maintenance ends <em>31 Dec 2027</em>.</h2>
    <p class="lead-sm">Still on ECC? A typical S/4HANA conversion takes 9 to 18 months. The best time to start planning is now.</p>
    <a href="/services/sap-s4hana-migration/" class="btn btn-glow">Plan your migration {icon("arrow-ur")}</a>
  </div>
  <div class="countdown reveal" data-deadline="2027-12-31T23:59:59Z" role="timer" aria-label="Time until end of SAP ECC mainstream maintenance">
    <div><strong data-u="d">--</strong><span>days</span></div>
    <div><strong data-u="h">--</strong><span>hours</span></div>
    <div><strong data-u="m">--</strong><span>minutes</span></div>
    <div><strong data-u="s">--</strong><span>seconds</span></div>
  </div>
</div></section>'''


def fmt_date(iso):
    return date.fromisoformat(iso).strftime("%-d %b %Y")


def article_card(a, h="h3"):
    return f'''<a class="post-card spot reveal" href="/insights/{a["slug"]}/">
  <div class="post-meta"><span class="tag">{e(a["tag"])}</span><span>{a["minutes"]} min read</span></div>
  <{h}>{e(a["h1"])}</{h}><p>{e(a["summary"])}</p>
  <span class="more">Read article {icon("arrow")}</span></a>'''


def insights_teaser(articles=None, title="Insights for SAP decision-makers", accent="SAP decision-makers"):
    arts = articles or ARTICLES[:3]
    cards = "".join(article_card(a) for a in arts)
    return f'''<section class="section"><div class="container">
  {section_head("Insights", title, "Practical guides on S/4HANA, RISE with SAP and running SAP well.", accent=accent)}
  <div class="post-grid">{cards}</div>
  <p class="center-x mt"><a href="/insights/" class="btn btn-dark">All insights {icon("arrow-ur")}</a></p>
</div></section>'''


def build_insights():
    crumbs, crumbs_ld = breadcrumbs([("Insights", "/insights/")])
    cards = "".join(article_card(a, "h2") for a in ARTICLES)
    body = page_hero(crumbs, "Insights", "SAP Insights & Guides",
                     "Practical, vendor-neutral guidance on S/4HANA migration, RISE with SAP, clean core and running SAP well.",
                     cta=False, accent="Insights") + f'''
<section class="section"><div class="container"><div class="post-grid">{cards}</div></div></section>'''
    blog_ld = {"@context": "https://schema.org", "@type": "Blog", "name": f"{SITE['name']} Insights",
               "url": BASE + "/insights/", "publisher": {"@id": BASE + "/#organization"},
               "blogPost": [{"@type": "BlogPosting", "headline": a["h1"], "url": f"{BASE}/insights/{a['slug']}/",
                             "datePublished": a["date"]} for a in ARTICLES]}
    page("/insights/", "SAP Insights: S/4HANA, RISE & Clean Core Guides | Oddesy",
         "Practical guides on SAP ECC end of maintenance, S/4HANA migration approaches, RISE with SAP and clean core, from senior SAP consultants.",
         body, "insights", [crumbs_ld, blog_ld])
    for a in ARTICLES:
        build_article(a)


def build_article(a):
    url = f"/insights/{a['slug']}/"
    crumbs, crumbs_ld = breadcrumbs([("Insights", "/insights/"), (a["tag"] + " guide", url)])
    svc = [x for x in SERVICES if x["slug"] in a["services"]]
    related = [x for x in ARTICLES if x is not a][:2]
    faq = "".join(f'<details><summary>{e(q)}<span class="plus">{icon("plus")}</span></summary><p>{e(ans)}</p></details>' for q, ans in a["faq"])
    svc_links = "".join(f'<li><a href="/services/{x["slug"]}/">{icon(x["icon"])}{e(x["name"])}</a></li>' for x in svc)
    body = f'''<section class="page-hero dark article-hero">{AURORA}<div class="container hero-inner narrow">
  {crumbs}
  <p class="pill"><span class="dot"></span>{e(a["tag"])} &middot; {a["minutes"]} min read</p>
  <h1>{e(a["h1"])}</h1>
  <p class="lead">{e(a["summary"])}</p>
  <p class="byline">By the {e(SITE["name"])} team &middot; <time datetime="{a["date"]}">{fmt_date(a["date"])}</time>{f' &middot; Updated <time datetime="{a["updated"]}">{fmt_date(a["updated"])}</time>' if a["updated"] != a["date"] else ""}</p>
</div></section>
<section class="section article-sec"><div class="container article-grid">
  <article class="prose article-body">{a["body"]}
    <h2>Frequently asked questions</h2>
    <div class="faq inline-faq">{faq}</div>
  </article>
  <aside class="sidebar">
    <div class="side-box"><h2 class="side-h">Related services</h2><ul class="side-nav">{svc_links}</ul></div>
    <div class="side-box side-cta">{AURORA}<div class="rel"><h2 class="side-h">Talk to an expert</h2>
      <p>Get a free 30-minute review of your SAP roadmap.</p>
      <a href="/contact/" class="btn btn-light btn-block">Book a call {icon("arrow-ur")}</a></div></div>
  </aside>
</div></section>
<section class="section soft"><div class="container">
  {section_head("Keep reading", "More SAP insights", accent="insights")}
  <div class="post-grid two">{"".join(article_card(x) for x in related)}</div>
</div></section>'''
    post_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"],
               "description": a["description"], "datePublished": a["date"], "dateModified": a["updated"],
               "url": BASE + url, "mainEntityOfPage": BASE + url, "image": BASE + "/assets/img/og-image.png",
               "author": {"@type": "Organization", "name": SITE["name"], "url": BASE + "/"},
               "publisher": {"@id": BASE + "/#organization"}, "articleSection": a["tag"]}
    page(url, a["title"], a["description"], body, "insights", [crumbs_ld, post_ld, faq_schema(a["faq"])], og_type="article")


def training_html():
    feats = [("users", "Live instructor-led batches", "Interactive classes for SAP MM, SAP EWM, or both as a bundle."),
             ("play", "Self-paced programmes", "Recorded courses you can follow on your own schedule."),
             ("user", "1-on-1 mentorship", "Personal guidance to plan and make your move into SAP.")]
    f = "".join(f'<li class="spot">{icon(i)}<div><strong>{t}</strong><span>{d}</span></div></li>' for i, t, d in feats)
    return f'''<section class="section" id="training"><div class="container">
  <div class="training-card reveal">
    {AURORA}
    <div class="training-copy">
      <p class="pill"><span class="dot"></span>Training &amp; mentorship</p>
      <h2>Build your SAP career with <em>hands-on</em> training.</h2>
      <p class="lead-sm">Job-ready {e(TRAINING["title"])} built around real project scenarios, delivered through {e(TRAINING["brand"])}.</p>
      <div class="hero-actions">
        <a href="{TRAINING["url"]}" class="btn btn-light" target="_blank" rel="noopener">Explore training {icon("arrow-ur")}<span class="sr">(opens in a new tab)</span></a>
      </div>
    </div>
    <ul class="training-list">{f}</ul>
  </div>
</div></section>'''


# --------------------------------------------------------------------------
# Pages

def build_home():
    chips = "".join(f'<li class="chip reveal">{icon("building")}{e(n)}</li>' for n, _ in INDUSTRIES)
    home_faq = [
        ("What does an SAP consulting company do?", "An SAP consulting company helps organisations select, implement, migrate, integrate and support SAP software. That includes process design, configuration, custom development, data migration, training and ongoing support."),
        ("Do you work with small and mid-sized businesses?", "Yes. Much of our work is with mid-sized companies that need senior SAP expertise without the overhead of a large global integrator."),
        ("Can you work remotely?", "Yes. We deliver onsite, remotely or in a hybrid model, and adapt our working hours to your time zone."),
        ("How do we start?", "Book a free consultation. We discuss your goals, review your landscape and suggest practical next steps, usually followed by a short written proposal."),
    ]
    body = f'''
<section class="hero dark">
  {AURORA}
  <div class="container hero-inner center">
    <p class="pill reveal"><span class="dot"></span>S/4HANA &middot; RISE with SAP &middot; BTP &middot; AMS</p>
    <h1 class="reveal">SAP transformation,<br><em>engineered</em> for what's next.</h1>
    <p class="lead reveal">{e(SITE["name"])} helps ambitious organisations implement, migrate and run SAP with senior expertise, clean-core design and zero drama.</p>
    <div class="hero-actions center-x reveal">
      <a href="/contact/" class="btn btn-glow">Get a free consultation {icon("arrow-ur")}</a>
      <a href="/services/" class="btn btn-ghost">Explore services</a>
    </div>
    <ul class="hero-points reveal">
      <li>{icon("check")}Senior SAP consultants</li>
      <li>{icon("check")}Onsite, remote or hybrid</li>
      <li>{icon("check")}Fixed-price or flexible</li>
    </ul>
  </div>
  <div class="container"><div class="dash-wrap reveal" aria-hidden="true">
    <div class="dash">
      <div class="dash-bar"><span></span><span></span><span></span><em>S/4HANA programme cockpit</em></div>
      <div class="dash-body">
        <aside class="dash-side"><i class="on"></i><i></i><i></i><i></i><i></i></aside>
        <div class="dash-main">
          <div class="dash-kpis">
            <div><small>Readiness</small><strong>78%</strong><div class="ring" style="--p:78"></div></div>
            <div><small>Custom code remediated</small><strong>1,240</strong><span class="up">+18% this sprint</span></div>
            <div><small>Interfaces tested</small><strong>46 / 52</strong><span class="up">On track</span></div>
          </div>
          <div class="dash-grid">
            <div class="dash-chart"><small>Mock load reconciliation</small>
              <svg viewBox="0 0 300 100" preserveAspectRatio="none"><defs><linearGradient id="lg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#7c8cff" stop-opacity=".55"/><stop offset="1" stop-color="#7c8cff" stop-opacity="0"/></linearGradient></defs>
              <path d="M0 80 C30 75 45 60 70 62 S120 40 150 42 S200 22 230 25 S280 10 300 8 L300 100 L0 100Z" fill="url(#lg)"/>
              <path class="draw" d="M0 80 C30 75 45 60 70 62 S120 40 150 42 S200 22 230 25 S280 10 300 8" fill="none" stroke="#9aa7ff" stroke-width="2.5"/></svg></div>
            <div class="dash-list"><small>Phase status</small>
              <p><b class="g"></b>Explore<span>Complete</span></p>
              <p><b class="b"></b>Realize<span>Sprint 4 / 6</span></p>
              <p><b></b>Deploy<span>Scheduled</span></p>
              <p><b></b>Hypercare<span>Planned</span></p></div>
          </div>
        </div>
      </div>
    </div>
    <div class="float f1">{icon("shield")}<div><strong>Clean core</strong><small>Upgrade-ready design</small></div></div>
    <div class="float f2">{icon("link")}<div><strong>All systems connected</strong><small>CRM, banks, e-commerce</small></div></div>
  </div></div>
</section>

{marquee()}

<section class="section"><div class="container">
  {section_head("What we do", "End-to-end SAP services, one accountable team", "Whether you are starting fresh, moving off ECC or improving a live system, we have the specialists to help.", accent="one accountable team")}
  {services_bento()}
</div></section>

{countdown()}

<section class="section"><div class="container split">
  <div class="reveal">
    <p class="eyebrow">About {e(SITE["short"])}</p>
    <h2>Senior SAP expertise, <em>without</em> the big-firm overhead.</h2>
    <p class="muted">You work directly with the people doing the work, not a layer of account managers. We focus on practical outcomes: systems users adopt, processes that run faster and landscapes ready for the next upgrade.</p>
    <a href="/about/" class="btn btn-dark">More about us {icon("arrow-ur")}</a>
  </div>
  <div class="stack">
    <div class="stack-item spot reveal"><span class="tile">{icon("layers")}</span><div><strong>Functional coverage</strong><span>FI/CO, MM, SD, PP, QM, PM, EWM, PS, SuccessFactors</span></div></div>
    <div class="stack-item spot reveal"><span class="tile">{icon("code")}</span><div><strong>Technical depth</strong><span>ABAP Cloud, Fiori/UI5, SAP BTP, Integration Suite, Basis</span></div></div>
    <div class="stack-item spot reveal"><span class="tile">{icon("cloud")}</span><div><strong>Cloud ready</strong><span>RISE with SAP, S/4HANA Cloud public &amp; private editions</span></div></div>
    <div class="stack-item spot reveal"><span class="tile">{icon("users")}</span><div><strong>Flexible delivery</strong><span>Projects, managed services and team augmentation</span></div></div>
  </div>
</div></section>

{process_html()}
{why_html()}

<section class="section soft"><div class="container">
  {section_head("Industries", "Built for how your industry works", "We adapt SAP best practices to the processes, regulations and partners of your sector.", accent="your industry")}
  <ul class="chips">{chips}</ul>
  <p class="center-x mt"><a href="/industries/" class="btn btn-dark">Explore industries {icon("arrow-ur")}</a></p>
</div></section>

{insights_teaser()}
{training_html()}
{faq_html(home_faq)}
'''
    page("/", "SAP Consulting Services | S/4HANA, RISE & AMS | Oddesy",
         "SAP consulting company offering S/4HANA implementation, RISE with SAP, ECC migration, SAP integration, BTP development and AMS support.",
         body, "home", [faq_schema(home_faq),
                        {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": BASE + "/"}])


def build_about():
    crumbs, crumbs_ld = breadcrumbs([("About", "/about/")])
    values = [("target", "Outcome first", "We measure success by business results, not hours billed."),
              ("shield", "Integrity", "Honest advice, even when it means recommending less work."),
              ("users", "Partnership", "We work as an extension of your team and share knowledge openly."),
              ("layers", "Craftsmanship", "Clean, documented, upgrade-safe solutions."),
              ("chart", "Always learning", "Our consultants keep pace with every SAP release."),
              ("clock", "Reliability", "We do what we say, when we say we will.")]
    vals = "".join(f'<div class="feature spot reveal"><span class="tile">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)
    body = page_hero(crumbs, "About us", f"About {SITE['name']}",
                     "An independent SAP consultancy built on senior expertise, honest advice and long-term partnerships.",
                     accent="Oddesy") + f'''
<section class="section"><div class="container split">
  <div class="reveal">
    <p class="eyebrow">Who we are</p>
    <h2>Consultants who give <em>straight answers</em>.</h2>
    <p class="muted">{e(SITE["name"])} helps organisations implement, modernise and run SAP. Our team combines functional process knowledge with strong technical skills, so business and IT requirements are solved together.</p>
    <p class="muted">We were founded on a simple idea: clients deserve experienced consultants who plan realistically and stay accountable for results.</p>
  </div>
  <div class="stack">
    <div class="glass-card reveal"><p class="eyebrow">Mission</p><h3>Make SAP simpler, faster and more valuable for the businesses that depend on it.</h3></div>
    <div class="glass-card reveal"><p class="eyebrow">Vision</p><h3>Be the SAP partner clients recommend first, because we delivered what we promised.</h3></div>
  </div>
</div></section>
<section class="section soft"><div class="container">
  {section_head("Values", "How we work with clients", accent="How we work")}
  <div class="feature-grid">{vals}</div>
</div></section>
<section class="section"><div class="container">
  {section_head("Expertise", "What we specialise in", accent="specialise")}
  {services_bento()}
</div></section>'''
    page("/about/", "About Us | SAP Consulting Experts | Oddesy Consulting",
         "Meet Oddesy Consulting and Services, an independent SAP consultancy delivering S/4HANA implementation, migration, integration and support.",
         body, "about", [crumbs_ld])


def build_services_hub():
    crumbs, crumbs_ld = breadcrumbs([("Services", "/services/")])
    models = [("Fixed-price projects", "Defined scope, deliverables and price. Ideal for implementations and rollouts."),
              ("Time & materials", "Flexible capacity for evolving requirements, billed on actual effort."),
              ("Managed services", "Monthly AMS retainer with agreed service levels and reporting."),
              ("Dedicated team", "Consultants working exclusively on your programme, onsite or remote.")]
    mod = "".join(f'<div class="feature spot reveal"><span class="num">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>'
                  for i, (t, d) in enumerate(models))
    body = page_hero(crumbs, "Services", "SAP Consulting Services",
                     "From strategy and implementation to integration, development and long-term support: every SAP capability you need, from one accountable team.",
                     accent="Services") + f'''
<section class="section"><div class="container">{services_bento("h2")}</div></section>
<section class="section soft"><div class="container">
  {section_head("Engagement models", "Work with us your way", accent="your way")}
  <div class="feature-grid four">{mod}</div>
</div></section>
{process_html()}'''
    item_list = {"@context": "https://schema.org", "@type": "ItemList",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["name"],
                                      "url": f'{BASE}/services/{s["slug"]}/'} for i, s in enumerate(SERVICES)]}
    page("/services/", "SAP Services: Implementation, Migration & Support | Oddesy",
         "Explore our SAP services: S/4HANA implementation, RISE with SAP, ECC to S/4HANA migration, SAP integration, BTP development, AMS support and SAP staffing.",
         body, "services", [crumbs_ld, item_list])


def build_service(s):
    crumbs, crumbs_ld = breadcrumbs([("Services", "/services/"), (s["nav"], f'/services/{s["slug"]}/')])
    side = "".join(f'<li><a href="/services/{o["slug"]}/"{" aria-current=page" if o is s else ""}>{icon(o["icon"])}{e(o["nav"])}</a></li>'
                   for o in SERVICES)
    offerings = "".join(f'<div class="offer spot reveal"><span class="num">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                        for i, (t, d) in enumerate(s["offerings"]))
    benefits = "".join(f'<div class="feature spot reveal"><span class="tile">{icon(ic)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
                       for ic, (t, d) in zip(["target", "chart", "clock", "shield"], s["benefits"]))
    overview = "".join(f'<p>{e(p)}</p>' for p in s["overview"])
    related = [o for o in SERVICES if o is not s][:3]
    rel = "".join(svc_card(o) for o in related)
    body = page_hero(crumbs, "SAP services", s["h1"], s["lead"]) + f'''
<section class="section"><div class="container with-sidebar">
  <div class="content">
    <div class="reveal"><p class="eyebrow">Overview</p><h2>Why it matters</h2>{overview}</div>
    <div class="reveal"><p class="eyebrow mt">Scope</p><h2>What we offer</h2></div>
    <div class="offer-grid">{offerings}</div>
  </div>
  <aside class="sidebar">
    <div class="side-box"><h2 class="side-h">All services</h2><ul class="side-nav">{side}</ul></div>
    <div class="side-box side-cta">{AURORA}<div class="rel"><h2 class="side-h">Need advice?</h2>
      <p>Speak to a senior SAP consultant about your project.</p>
      <a href="/contact/" class="btn btn-light btn-block">Contact us {icon("arrow-ur")}</a>
      <a class="side-phone" href="tel:{e(SITE["phone_link"])}">{icon("phone")}{e(SITE["phone"])}</a></div></div>
  </aside>
</div></section>
<section class="section soft"><div class="container">
  {section_head("Benefits", "What you gain", accent="gain")}
  <div class="feature-grid four">{benefits}</div>
</div></section>
{process_html() if s["slug"] in ("sap-s4hana-implementation", "rise-with-sap", "sap-s4hana-migration") else why_html("Why choose Oddesy")}
{faq_html(s["faq"])}
{insights_teaser([a for a in ARTICLES if s["slug"] in a["services"]] , "Related reading", "reading") if any(s["slug"] in a["services"] for a in ARTICLES) else ""}
<section class="section soft"><div class="container">
  {section_head("Related", "Explore related services", accent="related")}
  <div class="bento three">{rel}</div>
</div></section>'''
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"],
              "serviceType": s["name"], "description": s["description"],
              "url": f'{BASE}/services/{s["slug"]}/',
              "provider": {"@id": BASE + "/#organization"}, "areaServed": "Worldwide"}
    page(f'/services/{s["slug"]}/', s["title"], s["description"], body, "services",
         [crumbs_ld, svc_ld, faq_schema(s["faq"])])


def build_industries():
    crumbs, crumbs_ld = breadcrumbs([("Industries", "/industries/")])
    cards = "".join(f'<article class="feature spot reveal"><span class="tile">{icon("building")}</span><h2 class="h3">{e(n)}</h2><p>{e(d)}</p></article>'
                    for n, d in INDUSTRIES)
    body = page_hero(crumbs, "Industries", "SAP Solutions for Every Industry",
                     "Industry knowledge matters as much as SAP knowledge. We tailor SAP best practices to the processes, regulations and partners of your sector.",
                     accent="Every Industry") + f'''
<section class="section"><div class="container"><div class="feature-grid">{cards}</div></div></section>
{why_html()}'''
    page("/industries/", "Industries We Serve | SAP Industry Solutions | Oddesy",
         "SAP consulting for manufacturing, automotive, energy, EPC, retail, trading, textiles, real estate, pharma and more. Industry-specific S/4HANA solutions.",
         body, "industries", [crumbs_ld])


def build_careers():
    crumbs, crumbs_ld = breadcrumbs([("Careers", "/careers/")])
    roles = ["SAP FI/CO Consultant", "SAP MM / SD Consultant", "SAP PP / QM Consultant", "SAP ABAP Developer",
             "SAP Fiori / UI5 Developer", "SAP BTP & Integration Consultant", "SAP Basis Administrator", "SAP Project Manager"]
    role_html = "".join(f'<li class="role reveal"><span>{r}</span><em>Remote / Hybrid</em>{icon("arrow-ur")}</li>' for r in roles)
    perks = [("target", "Real responsibility", "Work directly with clients on meaningful projects."),
             ("chart", "Learning & certification", "Time and support to keep your SAP skills current."),
             ("clock", "Flexible working", "Remote, hybrid and onsite opportunities."),
             ("users", "Supportive team", "Senior consultants who share knowledge generously.")]
    perk_html = "".join(f'<div class="feature spot reveal"><span class="tile">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in perks)
    body = page_hero(crumbs, "Careers", "Build your SAP career at Oddesy",
                     "Join a team of SAP professionals who care about great work for clients and keep growing their skills.",
                     cta=False, accent="SAP career") + f'''
<section class="section"><div class="container">
  {section_head("Why join", "A team that invests in you", accent="invests in you")}
  <div class="feature-grid four">{perk_html}</div>
</div></section>
<section class="section soft"><div class="container narrow">
  {section_head("Open profiles", "Roles we regularly hire for", accent="regularly hire")}
  <ul class="roles">{role_html}</ul>
  <p class="center-x mt muted">Send your CV and a short note about your SAP experience to&nbsp;<a href="mailto:{e(SITE["careers_email"])}">{e(SITE["careers_email"])}</a></p>
</div></section>'''
    page("/careers/", f"SAP Jobs & Careers | {SITE['name']}",
         "Explore SAP jobs at Oddesy Consulting: FI/CO, MM, SD, PP, ABAP, Fiori, BTP, integration and Basis roles with remote and hybrid options.",
         body, "careers", [crumbs_ld])


def build_contact():
    crumbs, crumbs_ld = breadcrumbs([("Contact", "/contact/")])
    options = "".join(f"<option>{e(s['name'])}</option>" for s in SERVICES)
    body = page_hero(crumbs, "Contact", "Let's talk about your SAP goals",
                     "Tell us about your project and a senior consultant will get back to you within one business day.",
                     cta=False, accent="SAP goals") + f'''
<section class="section"><div class="container contact-grid">
  <div class="contact-info reveal">
    <p class="eyebrow">Get in touch</p>
    <h2>We'd love to <em>hear</em> from you.</h2>
    <p class="muted">Planning an S/4HANA move, need help with a live system, or want SAP experts on your team? Let's talk.</p>
    <ul class="contact-cards">
      <li class="spot"><span class="tile">{icon("mail")}</span><div><small>Email</small><a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></div></li>
      <li class="spot"><span class="tile">{icon("phone")}</span><div><small>Phone</small><a href="tel:{e(SITE["phone_link"])}">{e(SITE["phone"])}</a></div></li>
      <li class="spot"><span class="tile">{icon("pin")}</span><div><small>Office</small><span>{e(SITE["address"])}</span></div></li>
    </ul>
  </div>
  <form class="contact-form reveal" id="contact-form" novalidate>
    <h2 class="h3">Send us a message</h2>
    <div class="row2">
      <div class="field"><input id="name" name="name" autocomplete="name" placeholder=" " required><label for="name">Full name *</label></div>
      <div class="field"><input id="email" name="email" type="email" autocomplete="email" placeholder=" " required><label for="email">Work email *</label></div>
    </div>
    <div class="row2">
      <div class="field"><input id="company" name="company" autocomplete="organization" placeholder=" "><label for="company">Company</label></div>
      <div class="field"><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder=" "><label for="phone">Phone</label></div>
    </div>
    <div class="field select"><select id="interest" name="interest">{options}<option>Something else</option></select><label for="interest">Service of interest</label></div>
    <div class="field"><textarea id="message" name="message" rows="5" placeholder=" " required></textarea><label for="message">How can we help? *</label></div>
    <button type="submit" class="btn btn-glow btn-block">Send message {icon("arrow-ur")}</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>'''
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact " + SITE["name"],
                  "url": BASE + "/contact/", "about": {"@id": BASE + "/#organization"}}
    page("/contact/", "Contact Us | SAP Consulting Enquiries | Oddesy",
         "Contact Oddesy for SAP S/4HANA implementation, migration, integration and support. Email, call or send an enquiry for a free consultation.",
         body, "contact", [crumbs_ld, contact_ld], cta=False)


def build_privacy():
    crumbs, crumbs_ld = breadcrumbs([("Privacy policy", "/privacy-policy/")])
    body = page_hero(crumbs, "Legal", "Privacy Policy", f"How {SITE['name']} collects and uses personal information.", cta=False) + f'''
<section class="section"><div class="container narrow prose">
  <p><em>Last updated: {TODAY}. This is a starter template; please have it reviewed for your jurisdiction.</em></p>
  <h2>Information we collect</h2>
  <p>When you contact us through this website we collect the details you provide, such as your name, email address, company, phone number and message.</p>
  <h2>How we use it</h2>
  <p>We use this information only to respond to your enquiry, provide our services and, where you have agreed, keep you informed about relevant services. We do not sell personal data.</p>
  <h2>Cookies</h2>
  <p>This website does not set marketing or tracking cookies. If analytics are added in future, this policy will be updated.</p>
  <h2>Data retention</h2>
  <p>We keep enquiry data only as long as necessary for the purposes above or as required by law.</p>
  <h2>Your rights</h2>
  <p>You may request access to, correction of or deletion of your personal data by emailing <a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a>.</p>
</div></section>'''
    page("/privacy-policy/", f"Privacy Policy | {SITE['name']}",
         f"Privacy policy for {SITE['name']}: what information we collect through this website and how we use it.",
         body, "", [crumbs_ld], cta=False)


def build_404():
    body = f'''<section class="page-hero dark full">{AURORA}<div class="container hero-inner center">
  <p class="pill"><span class="dot warn"></span>Error 404</p><h1>This page took a <em>different route</em>.</h1>
  <p class="lead">The page you are looking for may have moved. Try one of these instead:</p>
  <div class="hero-actions center-x"><a href="/" class="btn btn-glow">Home</a><a href="/services/" class="btn btn-ghost">SAP services</a><a href="/contact/" class="btn btn-ghost">Contact</a></div>
</div></section>'''
    page("/404.html", f"Page not found | {SITE['name']}", "The requested page could not be found.", body, cta=False)


def build_meta_files():
    prio = {"/": "1.0", "/services/": "0.9", "/insights/": "0.8"}
    urls = "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>"
                   f"<priority>{prio.get(p, '0.8' if p.startswith('/services/') else '0.6')}</priority></url>\n"
                   for p in PAGES)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    if "YOUR-DOMAIN" not in SITE["domain"]:
        (OUT / "CNAME").write_text(SITE["domain"] + "\n")
    (OUT / ".nojekyll").write_text("")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    build_home(); build_about(); build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_insights()
    build_industries(); build_careers(); build_contact(); build_privacy(); build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
