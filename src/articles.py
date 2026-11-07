"""Insights articles. Each becomes /insights/<slug>/.

Body is simple HTML: use <h2>, <h3>, <p>, <ul>/<ol>, <table>.
Keep facts accurate and dated; update `updated` when you revise an article.
"""

ARTICLES = [
    {
        "slug": "sap-ecc-end-of-maintenance-2027",
        "title": "SAP ECC End of Maintenance 2027: What It Means & What to Do",
        "description": "SAP ECC 6.0 mainstream maintenance ends on 31 December 2027. Learn your support options, the risks of waiting and a practical plan for moving to S/4HANA.",
        "h1": "SAP ECC End of Maintenance in 2027: What It Means and What to Do Next",
        "summary": "Mainstream maintenance for SAP ECC ends on 31 December 2027. Here is what changes, what your options are and how to plan a move that does not rush your business.",
        "date": "2026-11-08",
        "updated": "2026-11-08",
        "minutes": 7,
        "services": ["sap-s4hana-migration", "rise-with-sap"],
        "tag": "Migration",
        "body": """
<p>If your business still runs SAP ECC 6.0, the clock is ticking. SAP's <strong>mainstream maintenance for SAP Business Suite 7 (including ECC 6.0 enhancement packages 6 to 8) ends on 31 December 2027</strong>. After that date, the system will not suddenly stop working, but the support you rely on changes and the cost of standing still starts to rise.</p>
<p>This guide explains what the deadline really means, the options SAP offers, and a realistic plan for moving to SAP S/4HANA without putting your operations at risk.</p>

<h2>What "end of mainstream maintenance" actually means</h2>
<p>Mainstream maintenance is the standard support included in your SAP maintenance contract. It covers legal and regulatory updates, security patches, support packages and access to SAP support for issues. When it ends, SAP stops delivering new legal changes and fixes for those releases as part of standard support.</p>
<p>For businesses in regulated industries, or in countries where tax and e-invoicing rules change frequently, losing legal updates is often the biggest practical risk.</p>

<h2>Your options after 2027</h2>
<h3>1. Extended maintenance (to end of 2030)</h3>
<p>SAP offers optional extended maintenance for ECC 6.0 EHP 6 to 8 until the end of 2030, at an additional fee on top of your existing maintenance. It buys time, but it costs more each year and does not move you closer to S/4HANA.</p>
<h3>2. Customer-specific maintenance</h3>
<p>Systems not covered by mainstream or extended maintenance fall into customer-specific maintenance. Support continues for known issues, but new legal changes and fixes for new problems are generally no longer delivered. For most businesses this is a risky place to be.</p>
<h3>3. RISE with SAP and the private cloud transition option</h3>
<p>SAP has also announced transition options for customers who commit to moving to S/4HANA through RISE with SAP, including longer support for ECC running in a private cloud while the move is completed. Terms and eligibility are set by SAP, so confirm the details for your contract before relying on them.</p>
<h3>4. Move to SAP S/4HANA</h3>
<p>The long-term answer for almost every ECC customer is S/4HANA, either on-premise, in a private cloud through RISE, or in S/4HANA Cloud public edition. The question is not whether to move but how and when.</p>

<h2>Why waiting is expensive</h2>
<ul>
  <li><strong>Consultant demand will peak.</strong> Thousands of organisations face the same deadline. Experienced S/4HANA consultants will be harder to find and more expensive the closer you get to 2027.</li>
  <li><strong>Projects take longer than expected.</strong> A typical conversion takes 9 to 18 months, plus time for assessment, budgeting and approvals.</li>
  <li><strong>Extended maintenance adds cost without adding value.</strong> Money spent keeping ECC alive is not spent on improving processes.</li>
  <li><strong>Technical debt keeps growing.</strong> Every new custom development on ECC is another object to analyse and remediate later.</li>
</ul>

<h2>A practical 5-step plan</h2>
<ol>
  <li><strong>Run a readiness assessment.</strong> Use SAP's Readiness Check and custom code analysis to understand simplification items, add-ons and code that must change.</li>
  <li><strong>Choose your migration approach.</strong> Brownfield conversion, greenfield re-implementation or selective data transition. See our guide to <a href="/insights/brownfield-vs-greenfield-s4hana-migration/">brownfield vs greenfield</a>.</li>
  <li><strong>Decide your deployment model.</strong> On-premise, RISE with SAP private cloud or public cloud. Each has different costs and flexibility.</li>
  <li><strong>Clean up before you move.</strong> Archive old data, retire unused custom code and fix master data quality. This shortens the project and reduces risk.</li>
  <li><strong>Plan cut-over early.</strong> Agree downtime windows with the business, rehearse with mock conversions and plan hypercare.</li>
</ol>

<h2>Key takeaways</h2>
<ul>
  <li>ECC 6.0 mainstream maintenance ends on <strong>31 December 2027</strong>; optional extended maintenance runs to the end of 2030 at extra cost.</li>
  <li>Your ECC system keeps running, but legal updates and new fixes become the main risk.</li>
  <li>Start with an assessment now: it is low cost and gives you the facts to plan budget and timing.</li>
</ul>
""",
        "faq": [
            ("When does SAP ECC mainstream maintenance end?", "Mainstream maintenance for SAP ECC 6.0 enhancement packages 6 to 8 ends on 31 December 2027."),
            ("Will SAP ECC stop working after 2027?", "No. The system keeps running, but standard support such as legal updates and new fixes changes unless you buy extended maintenance or move to S/4HANA."),
            ("How long does an ECC to S/4HANA migration take?", "A typical conversion takes 9 to 18 months depending on system size, custom code and the approach chosen, plus time for assessment and planning."),
        ],
    },
    {
        "slug": "brownfield-vs-greenfield-s4hana-migration",
        "title": "Brownfield vs Greenfield vs Selective S/4HANA Migration",
        "description": "Compare brownfield conversion, greenfield implementation and selective data transition for SAP S/4HANA: costs, risks, timelines and how to choose.",
        "h1": "Brownfield vs Greenfield vs Selective Data Transition: Choosing Your S/4HANA Approach",
        "summary": "The three ways to get to S/4HANA compared side by side, with the questions that decide which one is right for you.",
        "date": "2026-11-08",
        "updated": "2026-11-08",
        "minutes": 8,
        "services": ["sap-s4hana-migration", "sap-s4hana-implementation"],
        "tag": "Migration",
        "body": """
<p>Every move from SAP ECC to SAP S/4HANA starts with one big decision: do you convert your existing system, start again, or do something in between? The choice affects your budget, timeline, risk and how much your processes improve. This guide compares the three main approaches.</p>

<h2>The three approaches at a glance</h2>
<div class="table-wrap"><table>
  <thead><tr><th></th><th>Brownfield (system conversion)</th><th>Greenfield (new implementation)</th><th>Selective data transition</th></tr></thead>
  <tbody>
    <tr><th>What it is</th><td>Convert your existing ECC system to S/4HANA</td><td>Build a new S/4HANA system and migrate selected data</td><td>Build a new S/4HANA shell and move selected configuration and data</td></tr>
    <tr><th>Historical data</th><td>Kept in full</td><td>Usually open items and balances only</td><td>Chosen by you (by company, year or object)</td></tr>
    <tr><th>Process redesign</th><td>Limited, can be done later</td><td>Full redesign on SAP best practice</td><td>Partial, where it adds value</td></tr>
    <tr><th>Typical effort</th><td>Lowest</td><td>Highest</td><td>Medium to high</td></tr>
    <tr><th>Best for</th><td>Stable, well-run processes</td><td>Outdated processes, heavy customisation</td><td>Mergers, carve-outs, multi-system consolidation</td></tr>
  </tbody>
</table></div>

<h2>Brownfield: system conversion</h2>
<p>A brownfield conversion takes your current ECC system, including configuration, custom code and history, and technically converts it to S/4HANA using SAP's Software Update Manager and related tools.</p>
<h3>Advantages</h3>
<ul><li>Fastest route with the least business disruption.</li><li>All historical data stays available.</li><li>Users keep familiar processes, reducing training effort.</li></ul>
<h3>Watch-outs</h3>
<ul><li>You carry existing custom code and workarounds into the new system.</li><li>Simplification items (for example, Business Partner replacing customer and vendor master) still require work.</li><li>Process improvement is postponed rather than avoided.</li></ul>

<h2>Greenfield: new implementation</h2>
<p>Greenfield means implementing S/4HANA fresh, usually based on SAP best practices and fit-to-standard workshops, then migrating master data and open balances.</p>
<h3>Advantages</h3>
<ul><li>A clean core with minimal custom code, which makes future upgrades easier.</li><li>An opportunity to standardise and simplify processes.</li><li>The natural fit for S/4HANA Cloud public edition.</li></ul>
<h3>Watch-outs</h3>
<ul><li>Longer and more expensive, with more change management.</li><li>Historical data needs a separate archive or reporting solution.</li></ul>

<h2>Selective data transition: the middle path</h2>
<p>Selective data transition (sometimes called "bluefield" or hybrid) builds a new S/4HANA system and moves only what you choose, such as certain company codes, years of history, or reusable configuration. It typically uses specialist tools and partners.</p>
<p>It is especially useful when you want to merge several ECC systems into one, separate a business unit, or redesign some processes while keeping history for others.</p>

<h2>Five questions that decide your approach</h2>
<ol>
  <li><strong>How well do your current processes serve the business?</strong> If well, brownfield is attractive. If not, lean greenfield.</li>
  <li><strong>How much custom code do you run, and how much is actually used?</strong> Usage analysis often shows a large share is unused.</li>
  <li><strong>How important is historical data in the live system?</strong></li>
  <li><strong>Are you planning organisational changes</strong> such as acquisitions, divestments or consolidation?</li>
  <li><strong>Which deployment model are you targeting?</strong> Public cloud generally means greenfield.</li>
</ol>

<h2>Our recommendation</h2>
<p>Do not choose on instinct. A short readiness assessment, covering custom code usage, simplification items, data volumes and business priorities, will usually make the right answer clear and give you a defensible business case.</p>
""",
        "faq": [
            ("What is a brownfield S/4HANA migration?", "A brownfield migration, or system conversion, technically converts your existing SAP ECC system to S/4HANA, keeping configuration, custom code and historical data."),
            ("What is a greenfield S/4HANA implementation?", "Greenfield means implementing a new S/4HANA system from scratch, usually on SAP best practices, and migrating only master data and open balances."),
            ("Which S/4HANA migration approach is cheapest?", "Brownfield is usually the lowest-effort route, but total cost depends on custom code, data volumes and how much process change you need."),
        ],
    },
    {
        "slug": "rise-with-sap-explained",
        "title": "RISE with SAP Explained: What's Included & What to Ask",
        "description": "What is RISE with SAP? A plain-English guide to what the subscription includes, what remains your responsibility and the key questions to ask before you sign.",
        "h1": "RISE with SAP Explained: What's Included and What to Ask Before You Sign",
        "summary": "A plain-English guide to the RISE with SAP subscription, what it covers, what it doesn't, and the questions that protect you in negotiation.",
        "date": "2026-11-08",
        "updated": "2026-11-08",
        "minutes": 7,
        "services": ["rise-with-sap", "sap-support-ams"],
        "tag": "Cloud",
        "body": """
<p>RISE with SAP is SAP's subscription offering for moving to SAP S/4HANA Cloud. It bundles software, infrastructure and a set of services into one contract with one point of accountability. For many organisations it simplifies the move to S/4HANA, but it is important to understand exactly what you are buying.</p>

<h2>What RISE with SAP includes</h2>
<ul>
  <li><strong>SAP S/4HANA Cloud</strong> in the private or public edition, licensed as a subscription.</li>
  <li><strong>Infrastructure</strong> hosted on a hyperscaler such as Microsoft Azure, AWS or Google Cloud, or in an SAP data centre.</li>
  <li><strong>Technical managed services</strong> for the infrastructure, database and SAP basis layer, such as backups, patching and system availability, as defined in the contract.</li>
  <li><strong>SAP Business Technology Platform credits</strong> for extensions and integration.</li>
  <li><strong>Business process tools</strong> such as process insights and SAP Signavio capabilities, depending on the package.</li>
</ul>

<h2>What usually remains your responsibility</h2>
<p>This is where many surprises happen. RISE does not run your business processes for you. Typically you or your implementation partner still own:</p>
<ul>
  <li>Functional configuration, process design and implementation of changes.</li>
  <li>Application support for users (incidents, how-to questions, enhancements).</li>
  <li>Custom code, interfaces and third-party integrations.</li>
  <li>Data migration and data quality.</li>
  <li>Testing, training and organisational change management.</li>
  <li>User and role administration, depending on the responsibility matrix.</li>
</ul>
<p>Always review SAP's <strong>roles and responsibilities document</strong> line by line, and make sure every task has an owner: SAP, your partner, or your internal team.</p>

<h2>Private edition vs public edition</h2>
<p>The <strong>private edition</strong> offers more flexibility: broader functional scope, industry solutions and the ability to extend and modify where needed. It is the usual choice for brownfield conversions. The <strong>public edition</strong> is more standardised, receives regular SAP updates and suits organisations willing to adopt standard processes with minimal custom code.</p>

<h2>Questions to ask before you sign</h2>
<ol>
  <li>How was our <strong>sizing</strong> calculated (users and system size), and how do we add users later?</li>
  <li>Which tasks in the <strong>responsibility matrix</strong> are not covered by SAP, and who will do them?</li>
  <li>What <strong>service levels</strong> apply to availability, backup and recovery, and what happens if they are missed?</li>
  <li>How many <strong>non-production systems</strong> are included, and at what size?</li>
  <li>What does the <strong>migration</strong> itself cost, and is it included or separate?</li>
  <li>What are the <strong>exit and renewal terms</strong>, and how will prices change at renewal?</li>
  <li>How will we use the <strong>BTP credits</strong> before they expire?</li>
</ol>

<h2>Is RISE with SAP right for you?</h2>
<p>RISE is a strong fit if you want to move to a subscription model, reduce infrastructure management and adopt SAP innovations faster. It may be less attractive if you already have efficient hosting, very specific infrastructure requirements or significant existing licence investments. An independent assessment compares RISE with the alternatives using your real costs.</p>
""",
        "faq": [
            ("What is RISE with SAP?", "RISE with SAP is SAP's subscription offering that bundles S/4HANA Cloud, hosting infrastructure, technical managed services, BTP credits and process tools in one contract."),
            ("Does RISE with SAP include application support?", "Generally no. RISE covers technical managed services for the infrastructure and basis layer. Functional application support and changes usually remain with you or your partner."),
            ("What is the difference between RISE private and public edition?", "Private edition offers broader scope and more flexibility to extend the system; public edition is standardised, regularly updated and suited to organisations adopting standard processes."),
        ],
    },
    {
        "slug": "sap-clean-core-explained",
        "title": "SAP Clean Core Explained: Why It Matters for S/4HANA",
        "description": "What does clean core mean in SAP S/4HANA? Learn the principles, the benefits for upgrades and cost, and practical steps to move towards a clean core.",
        "h1": "SAP Clean Core Explained: What It Means and Why It Matters",
        "summary": "Clean core is the principle behind upgrade-friendly SAP systems. Here's what it means in practice and how to move towards it, step by step.",
        "date": "2026-11-08",
        "updated": "2026-11-08",
        "minutes": 6,
        "services": ["sap-btp-development", "sap-s4hana-implementation"],
        "tag": "Development",
        "body": """
<p>"Clean core" has become one of the most important ideas in SAP S/4HANA projects. It is SAP's recommended way to keep your ERP system stable, upgradeable and ready for innovation, while still meeting requirements that standard SAP does not cover.</p>

<h2>What does clean core mean?</h2>
<p>A clean core is an SAP system that stays as close to standard as possible. Instead of modifying SAP's own code or building tightly coupled custom objects inside the ERP, extensions are built on <strong>stable, released interfaces</strong>, either side by side on SAP Business Technology Platform (BTP) or in-stack using modern, upgrade-safe ABAP.</p>
<p>Clean core is not only about code. It also covers:</p>
<ul>
  <li><strong>Processes:</strong> adopting SAP best practices where they fit.</li>
  <li><strong>Data:</strong> good master data quality and governance.</li>
  <li><strong>Integration:</strong> using released APIs and standard integration tools.</li>
  <li><strong>Operations:</strong> keeping the system current and well documented.</li>
</ul>

<h2>Why it matters</h2>
<ul>
  <li><strong>Faster, cheaper upgrades.</strong> Fewer modifications means less testing and fewer surprises with each release.</li>
  <li><strong>Access to innovation.</strong> New SAP features and AI capabilities are easier to adopt on a standard system.</li>
  <li><strong>Lower total cost of ownership.</strong> Less custom code to maintain and support.</li>
  <li><strong>Cloud readiness.</strong> S/4HANA Cloud, and especially the public edition, requires a clean-core approach.</li>
</ul>

<h2>Where should extensions live?</h2>
<h3>Key user extensibility</h3>
<p>Custom fields, simple logic and forms created with SAP's in-app tools. Ideal for small, business-driven changes.</p>
<h3>Developer extensibility (ABAP Cloud)</h3>
<p>In-stack development using the ABAP RESTful Application Programming Model and released APIs only. Suited to extensions that need to be close to SAP data and processes.</p>
<h3>Side-by-side extensibility on SAP BTP</h3>
<p>Separate applications, workflows and portals that connect to S/4HANA through APIs. Best for customer and supplier portals, mobile apps, complex workflows and anything that changes often.</p>

<h2>How to move towards a clean core</h2>
<ol>
  <li><strong>Measure usage.</strong> Identify which custom objects are actually used. Unused code can often be retired.</li>
  <li><strong>Classify what remains.</strong> Decide what can be replaced by standard functionality, rebuilt on released APIs, or moved to BTP.</li>
  <li><strong>Set governance.</strong> Define development guidelines and a review process so new code follows clean-core rules.</li>
  <li><strong>Improve step by step.</strong> Clean core is a journey: tackle the highest-value areas first, often during an S/4HANA move.</li>
</ol>
""",
        "faq": [
            ("What is clean core in SAP?", "Clean core means keeping the SAP system close to standard and building extensions on stable, released interfaces, either in-stack with ABAP Cloud or side by side on SAP BTP."),
            ("Why is clean core important?", "It makes upgrades faster and cheaper, reduces maintenance cost and makes it easier to adopt new SAP innovations and move to the cloud."),
            ("Do I need clean core for S/4HANA Cloud public edition?", "Yes. The public edition only allows extensions through released, upgrade-stable interfaces, so a clean-core approach is required."),
        ],
    },
]
