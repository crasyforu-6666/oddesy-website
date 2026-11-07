#!/usr/bin/env python3
"""Static site generator for the Oddesy Consulting and Services website.

Usage:  python3 src/build.py
Output: public/  (upload this folder to any static host)

Edit copy in src/content.py; edit styles in src/assets/css/site.css.
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

from content import SITE, SERVICES, INDUSTRIES

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "public"
BASE = f"https://{SITE['domain']}"
TODAY = date.today().isoformat()
e = html.escape

# --------------------------------------------------------------------------
# Icons (simple 24x24 stroke icons drawn for this site)
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
    "building": '<rect x="4" y="3" width="11" height="18"/><path d="M15 9h5v12h-5"/><path d="M7.5 7h4M7.5 11h4M7.5 15h4"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONS[name]}</svg>')


# --------------------------------------------------------------------------
# Layout

def nav_html(active):
    svc_links = "".join(
        f'<li><a href="/services/{s["slug"]}/">{icon(s["icon"])}<span><strong>{e(s["nav"])}</strong>'
        f'<small>{e(s["summary"])}</small></span></a></li>' for s in SERVICES)
    def cls(key):
        return ' aria-current="page"' if active == key else ""
    return f'''
<header class="site-header">
  <div class="topbar"><div class="container topbar-inner">
    <span>SAP consulting, implementation and support</span>
    <span class="topbar-links"><a href="mailto:{e(SITE["email"])}">{icon("mail")}{e(SITE["email"])}</a>
    <a href="tel:{e(SITE["phone_link"])}">{icon("phone")}{e(SITE["phone"])}</a></span>
  </div></div>
  <div class="container nav">
    <a href="/" class="brand" aria-label="{e(SITE["name"])} home">
      <img src="/assets/img/logo-mark.svg" alt="" width="40" height="40">
      <span class="brand-text"><strong>ODDESY</strong><small>Consulting &amp; Services</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav id="primary-nav" class="primary-nav" aria-label="Main">
      <ul class="menu">
        <li><a href="/"{cls("home")}>Home</a></li>
        <li><a href="/about/"{cls("about")}>About</a></li>
        <li class="has-sub">
          <a href="/services/"{cls("services")} class="sub-trigger" aria-haspopup="true">Services <span class="caret" aria-hidden="true"></span></a>
          <div class="mega"><ul>{svc_links}</ul>
            <a class="mega-all" href="/services/">View all SAP services {icon("arrow")}</a></div>
        </li>
        <li><a href="/industries/"{cls("industries")}>Industries</a></li>
        <li><a href="/careers/"{cls("careers")}>Careers</a></li>
        <li><a href="/contact/"{cls("contact")}>Contact</a></li>
      </ul>
      <a href="/contact/" class="btn btn-primary nav-cta">Get a free consultation</a>
    </nav>
  </div>
</header>'''


def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES)
    year = date.today().year
    return f'''
<section class="cta-band">
  <div class="container cta-inner">
    <div><h2>Ready to plan your next SAP move?</h2>
    <p>Book a free 30-minute consultation with a senior SAP consultant. No sales pitch, just practical advice.</p></div>
    <a href="/contact/" class="btn btn-light">Book your consultation</a>
  </div>
</section>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <a href="/" class="brand brand-light"><img src="/assets/img/logo-mark.svg" alt="" width="40" height="40">
      <span class="brand-text"><strong>ODDESY</strong><small>Consulting &amp; Services</small></span></a>
      <p>{e(SITE["name"])} is an independent SAP consultancy helping organisations implement, migrate, integrate and support SAP solutions.</p>
      <a class="social" href="{e(SITE["linkedin"])}" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a>
    </div>
    <div><h2 class="footer-h">Services</h2><ul>{svc}</ul></div>
    <div><h2 class="footer-h">Company</h2><ul>
      <li><a href="/about/">About us</a></li><li><a href="/industries/">Industries</a></li>
      <li><a href="/careers/">Careers</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy policy</a></li></ul></div>
    <div><h2 class="footer-h">Contact</h2><ul class="footer-contact">
      <li>{icon("mail")}<a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></li>
      <li>{icon("phone")}<a href="tel:{e(SITE["phone_link"])}">{e(SITE["phone"])}</a></li>
      <li>{icon("pin")}<span>{e(SITE["address"])}</span></li></ul></div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; {year} {e(SITE["name"])}. All rights reserved.</p>
    <p>SAP, S/4HANA, SAP BTP, RISE with SAP and other SAP products are trademarks of SAP SE. {e(SITE["short"])} is an independent consultancy.</p>
  </div>
</footer>'''


def breadcrumbs(trail):
    """trail: list of (name, path). Returns (html, schema)."""
    items = [("Home", "/")] + trail
    links = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            links.append(f'<li aria-current="page">{e(name)}</li>')
        else:
            links.append(f'<li><a href="{path}">{e(name)}</a></li>')
    schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
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


def page(path, title, description, body, active="", schemas=(), og_type="website"):
    url = BASE + path
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                   for s in [org_schema(), *schemas])
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a2342">
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
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav_html(active)}
<main id="main">
{body}
</main>
{footer_html()}
<script>window.ODDESY = {json.dumps({"formEndpoint": SITE["form_endpoint"], "email": SITE["email"]})};</script>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''
    target = OUT / path.strip("/") / "index.html" if path != "/404.html" else OUT / "404.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    if path != "/404.html":
        PAGES.append(path)


PAGES = []


def page_hero(crumbs_html, eyebrow, h1, lead, cta=True):
    btns = (f'<div class="hero-actions"><a href="/contact/" class="btn btn-primary">Talk to an SAP expert</a>'
            f'<a href="tel:{e(SITE["phone_link"])}" class="btn btn-outline-light">{icon("phone")}Call us</a></div>') if cta else ""
    return f'''<section class="page-hero"><div class="container">
  {crumbs_html}
  <p class="eyebrow">{e(eyebrow)}</p>
  <h1>{e(h1)}</h1>
  <p class="lead">{e(lead)}</p>
  {btns}
</div></section>'''


def faq_html(faq, heading="Frequently asked questions"):
    items = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    return f'<section class="section"><div class="container narrow"><h2 class="center">{e(heading)}</h2><div class="faq">{items}</div></div></section>'


def service_cards(services, heading_level=3):
    h = f"h{heading_level}"
    return "".join(f'''<a class="svc-card" href="/services/{s["slug"]}/">
  <span class="svc-icon">{icon(s["icon"])}</span>
  <{h}>{e(s["name"])}</{h}><p>{e(s["summary"])}</p>
  <span class="more">Learn more {icon("arrow")}</span></a>''' for s in services)


ACTIVATE = [("Discover", "Explore what S/4HANA can do and build the business case."),
            ("Prepare", "Set up the project team, plan, governance and system landscape."),
            ("Explore", "Fit-to-standard workshops to confirm processes and gaps."),
            ("Realize", "Configure, build, migrate data and test in sprints."),
            ("Deploy", "Train users, rehearse cut-over and go live."),
            ("Run", "Hypercare, support and continuous improvement.")]


def activate_html():
    steps = "".join(f'<li><span class="step-n">{i + 1:02d}</span><h3>{n}</h3><p>{d}</p></li>'
                    for i, (n, d) in enumerate(ACTIVATE))
    return f'''<section class="section alt"><div class="container">
  <div class="section-head center"><p class="eyebrow">Delivery approach</p>
  <h2>A proven path from discovery to run</h2>
  <p>Every project follows SAP Activate, SAP's standard implementation methodology, so you always know where you are and what comes next.</p></div>
  <ol class="timeline">{steps}</ol></div></section>'''


WHY = [("target", "Senior-led delivery", "Experienced consultants lead your project from the first workshop to go-live."),
       ("layers", "Clean-core mindset", "We keep your SAP system close to standard so upgrades stay simple."),
       ("chart", "Transparent reporting", "Weekly status, clear milestones and early warning on risks."),
       ("shield", "Quality and security", "Peer-reviewed configuration and code, with security built in."),
       ("clock", "On-time delivery", "Realistic plans and disciplined execution keep projects on schedule."),
       ("users", "Flexible engagement", "Fixed price, time and materials, or dedicated team models.")]


def why_html(title="Why organisations choose Oddesy"):
    cards = "".join(f'<div class="why-card">{icon(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in WHY)
    return f'''<section class="section"><div class="container">
  <div class="section-head center"><p class="eyebrow">Why us</p><h2>{e(title)}</h2></div>
  <div class="why-grid">{cards}</div></div></section>'''


# --------------------------------------------------------------------------
# Pages

def build_home():
    industries = "".join(f'<li>{icon("building")}<span>{e(n)}</span></li>' for n, _ in INDUSTRIES[:8])
    home_faq = [
        ("What does an SAP consulting company do?", "An SAP consulting company helps organisations select, implement, migrate, integrate and support SAP software. That includes process design, system configuration, custom development, data migration, training and ongoing support."),
        ("Do you work with small and mid-sized businesses?", "Yes. Much of our work is with mid-sized companies that need senior SAP expertise without the overhead of a large global integrator."),
        ("Can you work remotely?", "Yes. We deliver onsite, remotely or in a hybrid model, and we adapt our working hours to your time zone."),
        ("How do we start?", "Book a free consultation. We will discuss your goals, review your current landscape and suggest practical next steps, usually followed by a short written proposal."),
    ]
    body = f'''
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Independent SAP consulting partner</p>
      <h1>SAP Consulting Services that move your business forward</h1>
      <p class="lead">From S/4HANA implementation and RISE with SAP to integration and long-term support, {e(SITE["name"])} helps organisations get more value from SAP with less risk.</p>
      <div class="hero-actions">
        <a href="/contact/" class="btn btn-primary">Get a free consultation</a>
        <a href="/services/" class="btn btn-outline-light">Explore our services</a>
      </div>
      <ul class="hero-points">
        <li>{icon("check")}Senior SAP consultants</li>
        <li>{icon("check")}Onsite, remote or hybrid</li>
        <li>{icon("check")}Fixed-price or flexible models</li>
      </ul>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="hv-card hv-main">
        <div class="hv-head"><span></span><span></span><span></span></div>
        <p class="hv-title">S/4HANA programme</p>
        <div class="hv-row"><span>Discover</span><i style="--w:100%"></i></div>
        <div class="hv-row"><span>Prepare</span><i style="--w:100%"></i></div>
        <div class="hv-row"><span>Explore</span><i style="--w:100%"></i></div>
        <div class="hv-row"><span>Realize</span><i style="--w:64%"></i></div>
        <div class="hv-row"><span>Deploy</span><i style="--w:12%"></i></div>
      </div>
      <div class="hv-card hv-badge">{icon("shield")}<div><strong>Clean core</strong><small>Upgrade-ready design</small></div></div>
      <div class="hv-card hv-badge hv-badge-2">{icon("link")}<div><strong>Integrated</strong><small>CRM, banks, e-commerce</small></div></div>
    </div>
  </div>
</section>

<section class="pillars"><div class="container pillar-grid">
  <div>{icon("target")}<h2 class="h3">Tailored solutions</h2><p>Designs built around how your business actually works.</p></div>
  <div>{icon("link")}<h2 class="h3">Seamless integration</h2><p>SAP connected to every system and partner you use.</p></div>
  <div>{icon("headset")}<h2 class="h3">Reliable support</h2><p>SLA-based support that keeps operations running.</p></div>
  <div>{icon("shield")}<h2 class="h3">Long-term partnership</h2><p>One team from strategy through go-live and beyond.</p></div>
</div></section>

<section class="section"><div class="container">
  <div class="section-head center"><p class="eyebrow">Our services</p>
  <h2>End-to-end SAP consulting services</h2>
  <p>Whether you are starting fresh, moving from ECC or improving a live system, we have the specialists to help.</p></div>
  <div class="svc-grid">{service_cards(SERVICES)}</div>
</div></section>

<section class="section alt"><div class="container split">
  <div>
    <p class="eyebrow">About {e(SITE["short"])}</p>
    <h2>Senior SAP expertise without the big-firm overhead</h2>
    <p>{e(SITE["name"])} brings together SAP consultants who have delivered implementations, migrations and support programmes across many industries. You work directly with the people doing the work, not a layer of account managers.</p>
    <p>We focus on practical outcomes: systems that users adopt, processes that run faster and SAP landscapes that are ready for the next upgrade.</p>
    <a href="/about/" class="btn btn-secondary">More about us</a>
  </div>
  <ul class="check-list">
    <li>{icon("check")}<div><strong>Functional coverage</strong><span>FI/CO, MM, SD, PP, QM, PM, EWM, PS and SuccessFactors</span></div></li>
    <li>{icon("check")}<div><strong>Technical depth</strong><span>ABAP, Fiori/UI5, SAP BTP, Integration Suite and Basis</span></div></li>
    <li>{icon("check")}<div><strong>Cloud ready</strong><span>RISE with SAP, S/4HANA Cloud public and private editions</span></div></li>
    <li>{icon("check")}<div><strong>Flexible delivery</strong><span>Projects, managed services and resource augmentation</span></div></li>
  </ul>
</div></section>

{why_html()}
{activate_html()}

<section class="section"><div class="container">
  <div class="section-head center"><p class="eyebrow">Industries</p><h2>SAP solutions for your industry</h2>
  <p>We adapt SAP best practices to the specific processes, regulations and partners of your sector.</p></div>
  <ul class="ind-grid">{industries}</ul>
  <p class="center mt"><a href="/industries/" class="btn btn-secondary">See all industries</a></p>
</div></section>

{faq_html(home_faq)}
'''
    page("/", "SAP Consulting Services | S/4HANA, RISE & AMS | Oddesy",
         "SAP consulting company offering S/4HANA implementation, RISE with SAP, ECC migration, SAP integration, BTP development and AMS support.",
         body, "home", [faq_schema(home_faq),
                        {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": BASE + "/"}])


def build_about():
    crumbs, crumbs_ld = breadcrumbs([("About", "/about/")])
    body = page_hero(crumbs, "About us", f"About {SITE['name']}",
                     "An independent SAP consultancy built on senior expertise, honest advice and long-term partnerships.") + f'''
<section class="section"><div class="container split">
  <div>
    <h2>Who we are</h2>
    <p>{e(SITE["name"])} is an SAP consulting firm that helps organisations implement, modernise and run SAP. Our team combines functional process knowledge with strong technical skills, so business and IT requirements are solved together.</p>
    <p>We were founded on a simple idea: clients deserve experienced consultants who give straight answers, plan realistically and stay accountable for results.</p>
  </div>
  <div class="panel">
    <h3>Our mission</h3>
    <p>To make SAP simpler, faster and more valuable for the businesses that depend on it.</p>
    <h3>Our vision</h3>
    <p>To be the SAP partner clients recommend first, because we delivered what we promised.</p>
  </div>
</div></section>

<section class="section alt"><div class="container">
  <div class="section-head center"><p class="eyebrow">Our values</p><h2>How we work with clients</h2></div>
  <div class="why-grid">
    <div class="why-card">{icon("target")}<h3>Outcome first</h3><p>We measure success by business results, not hours billed.</p></div>
    <div class="why-card">{icon("shield")}<h3>Integrity</h3><p>Honest advice, even when it means recommending less work.</p></div>
    <div class="why-card">{icon("users")}<h3>Partnership</h3><p>We work as an extension of your team and share knowledge openly.</p></div>
    <div class="why-card">{icon("layers")}<h3>Craftsmanship</h3><p>Clean, documented, upgrade-safe solutions.</p></div>
    <div class="why-card">{icon("chart")}<h3>Continuous learning</h3><p>Our consultants keep pace with every SAP release.</p></div>
    <div class="why-card">{icon("clock")}<h3>Reliability</h3><p>We do what we say, when we say we will do it.</p></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="section-head center"><p class="eyebrow">Expertise</p><h2>What we specialise in</h2></div>
  <div class="svc-grid">{service_cards(SERVICES)}</div>
</div></section>
'''
    page("/about/", "About Us | SAP Consulting Experts | Oddesy Consulting",
         "Meet Oddesy Consulting and Services, an independent SAP consultancy delivering S/4HANA implementation, migration, integration and support.",
         body, "about", [crumbs_ld])


def build_services_hub():
    crumbs, crumbs_ld = breadcrumbs([("Services", "/services/")])
    body = page_hero(crumbs, "Services", "SAP Consulting Services",
                     "A complete range of SAP services, from strategy and implementation to integration, development and ongoing support.") + f'''
<section class="section"><div class="container">
  <div class="svc-grid">{service_cards(SERVICES, 2)}</div>
</div></section>
<section class="section alt"><div class="container">
  <div class="section-head center"><p class="eyebrow">Engagement models</p><h2>Work with us your way</h2></div>
  <div class="model-grid">
    <div class="model"><h3>Fixed-price projects</h3><p>Defined scope, deliverables and price. Ideal for implementations, migrations and rollouts.</p></div>
    <div class="model"><h3>Time and materials</h3><p>Flexible capacity for evolving requirements, billed on actual effort.</p></div>
    <div class="model"><h3>Managed services</h3><p>Monthly AMS retainer with agreed service levels and reporting.</p></div>
    <div class="model"><h3>Dedicated team</h3><p>Consultants who work exclusively on your programme, onsite or remote.</p></div>
  </div>
</div></section>
{activate_html()}
'''
    item_list = {"@context": "https://schema.org", "@type": "ItemList",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["name"],
                                      "url": f'{BASE}/services/{s["slug"]}/'} for i, s in enumerate(SERVICES)]}
    page("/services/", "SAP Services: Implementation, Migration & Support | Oddesy",
         "Explore our SAP services: S/4HANA implementation, RISE with SAP, ECC to S/4HANA migration, SAP integration, BTP development, AMS support and SAP staffing.",
         body, "services", [crumbs_ld, item_list])


def build_service(s):
    crumbs, crumbs_ld = breadcrumbs([("Services", "/services/"), (s["nav"], f'/services/{s["slug"]}/')])
    side = "".join(f'<li><a href="/services/{o["slug"]}/"{" aria-current=page" if o is s else ""}>{e(o["nav"])}</a></li>'
                   for o in SERVICES)
    offerings = "".join(f'<div class="offer">{icon("check")}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>'
                        for t, d in s["offerings"])
    benefits = "".join(f'<div class="why-card">{icon(ic)}<h3>{e(t)}</h3><p>{e(d)}</p></div>'
                       for ic, (t, d) in zip(["target", "chart", "clock", "shield"], s["benefits"]))
    overview = "".join(f"<p>{e(p)}</p>" for p in s["overview"])
    related = [o for o in SERVICES if o is not s][:3]
    body = page_hero(crumbs, "SAP services", s["h1"], s["lead"]) + f'''
<section class="section"><div class="container with-sidebar">
  <div class="content">
    <h2>Overview</h2>
    {overview}
    <h2>What we offer</h2>
    <div class="offer-grid">{offerings}</div>
  </div>
  <aside class="sidebar">
    <div class="side-box"><h2 class="h4">Our services</h2><ul class="side-nav">{side}</ul></div>
    <div class="side-box side-cta"><h2 class="h4">Need advice?</h2>
      <p>Speak to a senior SAP consultant about your project.</p>
      <a href="/contact/" class="btn btn-light btn-block">Contact us</a>
      <a class="side-phone" href="tel:{e(SITE["phone_link"])}">{icon("phone")}{e(SITE["phone"])}</a></div>
  </aside>
</div></section>
<section class="section alt"><div class="container">
  <div class="section-head center"><p class="eyebrow">Benefits</p><h2>What you gain</h2></div>
  <div class="why-grid four">{benefits}</div>
</div></section>
{activate_html() if s["slug"] in ("sap-s4hana-implementation", "rise-with-sap", "sap-s4hana-migration") else why_html("Why choose Oddesy")}
{faq_html(s["faq"])}
<section class="section alt"><div class="container">
  <div class="section-head center"><h2>Related services</h2></div>
  <div class="svc-grid three">{service_cards(related)}</div>
</div></section>
'''
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"],
              "serviceType": s["name"], "description": s["description"],
              "url": f'{BASE}/services/{s["slug"]}/',
              "provider": {"@id": BASE + "/#organization"}, "areaServed": "Worldwide"}
    page(f'/services/{s["slug"]}/', s["title"], s["description"], body, "services",
         [crumbs_ld, svc_ld, faq_schema(s["faq"])])


def build_industries():
    crumbs, crumbs_ld = breadcrumbs([("Industries", "/industries/")])
    cards = "".join(f'<article class="ind-card">{icon("building")}<h2 class="h3">{e(n)}</h2><p>{e(d)}</p></article>'
                    for n, d in INDUSTRIES)
    body = page_hero(crumbs, "Industries", "SAP Solutions for Every Industry",
                     "Industry knowledge matters as much as SAP knowledge. We tailor SAP best practices to the processes, regulations and partners of your sector.") + f'''
<section class="section"><div class="container"><div class="ind-cards">{cards}</div></div></section>
{why_html()}'''
    page("/industries/", f"Industries We Serve | SAP Industry Solutions | {SITE['short']}",
         "SAP consulting for manufacturing, automotive, energy, EPC, retail, trading, textiles, real estate, pharma and more. Industry-specific S/4HANA solutions.",
         body, "industries", [crumbs_ld])


def build_careers():
    crumbs, crumbs_ld = breadcrumbs([("Careers", "/careers/")])
    roles = ["SAP FI/CO Consultant", "SAP MM / SD Consultant", "SAP PP / QM Consultant", "SAP ABAP Developer",
             "SAP Fiori / UI5 Developer", "SAP BTP & Integration Consultant", "SAP Basis Administrator",
             "SAP Project Manager"]
    role_html = "".join(f'<li>{icon("users")}<span>{r}</span></li>' for r in roles)
    body = page_hero(crumbs, "Careers", "SAP Careers at Oddesy",
                     "Join a team of SAP professionals who care about doing great work for clients and growing their skills.", cta=False) + f'''
<section class="section"><div class="container split">
  <div>
    <h2>Why work with us</h2>
    <ul class="check-list plain">
      <li>{icon("check")}<div><strong>Real responsibility</strong><span>Work directly with clients on meaningful projects.</span></div></li>
      <li>{icon("check")}<div><strong>Learning and certification</strong><span>Time and support to keep your SAP skills current.</span></div></li>
      <li>{icon("check")}<div><strong>Flexible working</strong><span>Remote, hybrid and onsite opportunities.</span></div></li>
      <li>{icon("check")}<div><strong>Supportive team</strong><span>Senior consultants who share knowledge generously.</span></div></li>
    </ul>
  </div>
  <div class="panel">
    <h2 class="h3">Profiles we regularly hire</h2>
    <ul class="role-list">{role_html}</ul>
    <p>Send your CV and a short note about your SAP experience to
    <a href="mailto:{e(SITE["careers_email"])}">{e(SITE["careers_email"])}</a>.</p>
  </div>
</div></section>'''
    page("/careers/", f"SAP Jobs & Careers | {SITE['name']}",
         "Explore SAP jobs at Oddesy Consulting: FI/CO, MM, SD, PP, ABAP, Fiori, BTP, integration and Basis roles with remote and hybrid options.",
         body, "careers", [crumbs_ld])


def build_contact():
    crumbs, crumbs_ld = breadcrumbs([("Contact", "/contact/")])
    options = "".join(f"<option>{e(s['name'])}</option>" for s in SERVICES)
    body = page_hero(crumbs, "Contact", "Contact Our SAP Consultants",
                     "Tell us about your project and a senior consultant will get back to you within one business day.", cta=False) + f'''
<section class="section"><div class="container contact-grid">
  <div class="contact-info">
    <h2>Get in touch</h2>
    <p>Whether you are planning an S/4HANA move, need help with a live system or want to add SAP experts to your team, we are happy to talk.</p>
    <ul class="contact-cards">
      <li>{icon("mail")}<div><strong>Email us</strong><a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></div></li>
      <li>{icon("phone")}<div><strong>Call us</strong><a href="tel:{e(SITE["phone_link"])}">{e(SITE["phone"])}</a></div></li>
      <li>{icon("pin")}<div><strong>Office</strong><span>{e(SITE["address"])}</span></div></li>
    </ul>
  </div>
  <form class="contact-form" id="contact-form" novalidate>
    <h2 class="h3">Send us a message</h2>
    <div class="row2">
      <div class="field"><label for="name">Full name *</label><input id="name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="email">Work email *</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    </div>
    <div class="row2">
      <div class="field"><label for="company">Company</label><input id="company" name="company" autocomplete="organization"></div>
      <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="field"><label for="interest">Service of interest</label>
      <select id="interest" name="interest">{options}<option>Something else</option></select></div>
    <div class="field"><label for="message">How can we help? *</label><textarea id="message" name="message" rows="5" required></textarea></div>
    <button type="submit" class="btn btn-primary btn-block">Send message</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>'''
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact " + SITE["name"],
                  "url": BASE + "/contact/", "about": {"@id": BASE + "/#organization"}}
    page("/contact/", f"Contact Us | SAP Consulting Enquiries | {SITE['short']}",
         "Contact Oddesy for SAP S/4HANA implementation, migration, integration and support. Email, call or send an enquiry for a free consultation.",
         body, "contact", [crumbs_ld, contact_ld])


def build_privacy():
    crumbs, crumbs_ld = breadcrumbs([("Privacy policy", "/privacy-policy/")])
    body = page_hero(crumbs, "Legal", "Privacy Policy", f"How {SITE['name']} collects and uses personal information.", cta=False) + f'''
<section class="section"><div class="container narrow prose">
  <p><em>Last updated: {TODAY}. This is a starter template; please have it reviewed for your jurisdiction before publishing.</em></p>
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
         body, "", [crumbs_ld])


def build_404():
    body = f'''<section class="page-hero"><div class="container">
  <p class="eyebrow">Error 404</p><h1>Page not found</h1>
  <p class="lead">The page you are looking for may have moved. Try one of these instead:</p>
  <div class="hero-actions"><a href="/" class="btn btn-primary">Home</a><a href="/services/" class="btn btn-outline-light">SAP services</a><a href="/contact/" class="btn btn-outline-light">Contact</a></div>
</div></section>'''
    page("/404.html", f"Page not found | {SITE['name']}", "The requested page could not be found.", body)
    (OUT / "404.html").write_text((OUT / "404.html").read_text().replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">'))


def build_meta_files():
    prio = {"/": "1.0", "/services/": "0.9"}
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
    build_industries(); build_careers(); build_contact(); build_privacy(); build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
