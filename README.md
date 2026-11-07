# Oddesy Consulting and Services: website

A multi-page, SEO-friendly static website with a corporate theme.

```
src/content.py      ← all text: business details, services, FAQs, industries
src/build.py        ← page templates, SEO tags, structured data, sitemap
src/assets/         ← CSS, JS, logo, social-share image
public/             ← GENERATED site: upload this folder to your host
```

## Edit and rebuild
1. Open `src/content.py` and fill in `SITE`: **domain**, email, phone, address, LinkedIn URL.
2. Run `python3 src/build.py` (Python 3, no packages needed).
3. Upload the contents of `public/`.

Setting the domain updates canonical URLs, Open Graph tags, structured data, `sitemap.xml`, `robots.txt`
and creates a `CNAME` file for GitHub Pages.

## Pages
| URL | Page |
|---|---|
| `/` | Home |
| `/about/` | About |
| `/services/` | Services hub |
| `/services/sap-s4hana-implementation/` | S/4HANA implementation |
| `/services/rise-with-sap/` | RISE with SAP |
| `/services/sap-s4hana-migration/` | ECC to S/4HANA migration & upgrades |
| `/services/sap-integration/` | SAP integration |
| `/services/sap-support-ams/` | SAP support & AMS |
| `/services/sap-btp-development/` | BTP & custom development |
| `/services/sap-staffing/` | SAP staffing & resource augmentation |
| `/industries/` | Industries |
| `/careers/` | Careers |
| `/contact/` | Contact form |
| `/privacy-policy/` | Privacy policy (template, have it reviewed) |

To add a service, copy one entry in `SERVICES` in `content.py`, change the slug and text, and rebuild.
It automatically appears in the menu, footer, services hub, sitemap and "related services".

## SEO built in
- Unique `<title>` (≤60 chars) and meta description (≤160 chars) on every page
- Exactly one H1 per page and a logical H2/H3 hierarchy
- Clean, keyword-rich URLs; canonical tag on every page
- Structured data (JSON-LD): ProfessionalService, WebSite, Service, FAQPage, BreadcrumbList, ItemList, ContactPage
- Visible breadcrumbs, internal linking (sidebar, related services, footer)
- Open Graph + Twitter card with a 1200×630 share image
- `sitemap.xml`, `robots.txt`, `404.html` (noindex)
- Static HTML: fast, no plugins, works without JavaScript

After going live, submit `https://YOUR-DOMAIN/sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## Contact form
By default the form opens the visitor's email app. To receive submissions directly, create a free
form at Formspree (or similar) and paste its URL into `form_endpoint` in `content.py`, then rebuild.

## Hosting
Netlify, Cloudflare Pages, Vercel or GitHub Pages: publish the `public/` folder.
cPanel/shared hosting: upload the contents of `public/` into `public_html`.
Pages use root-relative links (`/about/`), so preview with a local server rather than double-clicking:
`cd public && python3 -m http.server` → http://localhost:8000
