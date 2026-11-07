# Blog publishing playbook

This is the exact procedure for publishing one blog post to oddesyconsultingandservices.com.
Scheduled publishing sessions follow it; people can too.

Goal: posts that a senior SAP consultant would be proud to share, that answer what people
actually search for, and that Google sees as genuinely helpful. **Quality over volume, always.**
If a good post cannot be produced in a run, publish nothing and report why.

## 1. Set up

```bash
cd oddesy-website            # the repository root
git pull --rebase origin main
date -u +%F                  # today's date (UTC) is the post date
```

## 2. Pick the topic

1. Open `src/content-plan.json` and take the **first** topic with `"status": "todo"`.
2. List existing posts (`ls src/posts/`) and skim titles. If the topic overlaps heavily with an
   existing post, mark it `"status": "skipped"` with a `"reason"` and take the next one.
3. If fewer than **25** topics are `todo`, research and append 20 new ones (see section 7).

## 3. Research (required)

Use web search before writing. For the chosen keyword:

- Search the keyword itself and look at what currently ranks: which questions do those pages
  answer, and what do they miss? Your post must be **more useful** than them, not a rewrite.
- Collect the questions people ask ("People also ask", forums, SAP Community threads).
- **Verify every factual claim** (dates, version numbers, product names, maintenance deadlines,
  licensing rules) against an authoritative source, preferably SAP itself (sap.com, news.sap.com,
  help.sap.com, support.sap.com, community.sap.com). Note the source URLs.
- Product names and dates change. If sources disagree or you cannot verify something, leave it
  out or say plainly that it should be confirmed with SAP.
- Minimum depth: at least **6 searches** and **open and read at least 4 source pages in full**
  (at least 2 of them from SAP), yourself rather than through a summarising sub-agent. Search
  results alone are not verification. Take the time this needs; a rushed post is worse than none.
- Before writing, list the key facts you will use with the URL that confirms each one, and keep
  that list in your final message.

## 4. Write the post

Create `src/posts/<slug>.html`. The slug is the keyword in lowercase words joined by hyphens
(max 70 chars, no dates unless the topic is date-specific, e.g. `sap-ewm-vs-wm`).

```
title: <max 60 chars, keyword near the start, ends with a hook>
description: <110-160 chars, includes keyword, says what the reader gets>
h1: <natural headline, can be longer than title>
summary: <1-2 sentences for cards>
date: <today, YYYY-MM-DD>
updated: <today>
category: <one of: Migration | Cloud & RISE | Finance | Logistics & Supply Chain | Development & BTP | Integration | AI & Innovation | Support & Operations | Careers & Skills | Industry>
keyword: <the target keyword from the plan>
services: <1-2 service slugs from the plan>
faq: <real question people ask?> || <direct 1-3 sentence answer>
faq: ...   (2-4 FAQs)
---
<p>Opening paragraph: answer the core question in the first 2-3 sentences.</p>
<h2>...</h2>
...
```

### Writing standards

- **1,200-2,000 words** (minimum 1,000 is enforced). Depth over padding.
- Lead with the answer. Short paragraphs. Use `<h2>` for main sections (at least 3), `<h3>` for sub-points,
  lists for steps, and a comparison table (`<div class="table-wrap"><table>…</table></div>`) where it helps.
- Practical and specific: steps, checklists, examples, transaction codes, decision criteria,
  common mistakes. Write as an experienced consultant advising a client.
- British English, plain and direct. No hype, no filler intros, no "in conclusion".
- **Never invent** statistics, survey results, client names, case studies, quotes, testimonials,
  salaries or prices. If you cite a number, it must come from a source you verified, and you link to it.
- Link to **2-3 authoritative external sources** you used (https only), e.g. SAP help or news pages.
- Internal links (at least 3 different pages, enforced): the relevant `/services/<slug>/` pages and
  1-2 related posts at `/blog/<slug>/`. Use descriptive anchor text, not "click here".
- Careers & Skills and Logistics posts may mention SAP MM / EWM training at
  https://youronementor.com once, naturally, where genuinely relevant.
- End with a short "Next steps" or "Key takeaways" section that may point to `/contact/`.
- Allowed HTML only: `p h2 h3 ul ol li strong em a table thead tbody tr th td div.table-wrap blockquote code`.

## 5. Strengthen internal links

Open 1 older post on a closely related topic and add one natural sentence linking to the new post.
Do not change that post's `updated` date for a link-only edit.

## 6. Check, commit, deploy

```bash
scripts/publish.sh check <slug>     # must pass: validator + build + whole-site checks
```

Fix every reported problem and re-run until it passes. Then:

1. Update `src/content-plan.json`: set the topic's `"status": "published"`, `"slug"` and `"published"` date.
2. Commit everything with a message like `Publish blog post: <h1>`.
3. Deploy:

```bash
scripts/publish.sh deploy
```

If the check cannot be made to pass, do **not** deploy. Revert your changes and report the problem.

## 7. Replenishing the topic plan

When fewer than 25 topics are `todo`, research new ones with web search:
SAP news and release updates from the last 3 months, recurring questions on SAP Community,
"People also ask" for the existing categories, and interview/career questions for SAP MM, EWM, FICO,
SD, ABAP and BTP. Add 20 topics with `keyword`, `working_title`, `category`, `intent`
(`informational` or `commercial`), `services` and `"status": "todo"`. Keep categories balanced,
avoid keywords already used, and put the most-searched, most relevant topics first.
