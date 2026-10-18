# WEM Radar 2026-10-18 — Citations ledger

Edition: **WEEKLY** (no periodic prediction check; last check 2026-10-03, 15 days earlier; next due 2026-10-24). Collection window 2026-10-10 (after ~14:00 UTC) → 2026-10-18 (~06:30 UTC).
One row per load-bearing claim in `radar-2026-10-18.md`. Claim typing per L-077: **Fact** · **Fact-that-was-SAID** (a named party asserted it; the assertion is the fact) · **Estimate** · **Inference** (our reading).
Raw research: `reports/research/2026-10-18-weekly/` (streams A-D, raw search logs `raw-*-search.md`, call logs `fc-log-*.jsonl`, saved pages under `scrapes/a-d/`). Every date was read off the page itself (`datePublished`, `article:published_time`, the printed dateline, EDGAR filing date, a roadmap record's `created` field, or the GitHub API), never a search snippet.

No claim appears in the brief without a row here.

---

## A. Salesforce contact centre in Europe

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| A1 | "On October 16, we're making our native Contact Center generally available in Europe, going live across 30+ European countries including the UK ... with Australia and New Zealand following in November." | Fact-that-was-SAID (plan stated 13 Oct for 16 Oct) | Salesforce blog (Annie Weinberger), `datePublished 2026-10-13T23:38:16Z` | https://www.salesforce.com/blog/service-cloud-fall-2026-releases/ |
| A2 | Global price page: Contact Center $125 / €125 / 1,250 kr / £100 per user per month; Contact Center Plus ("with workforce engagement management") $250 / €250 / 2,500 kr / £200; AUD and JPY cells "Not currently available in this region" | Fact (page read 18 Oct 02:27 UTC) | Salesforce price page | https://www.salesforce.com/service/contact-center/pricing/ |
| A3 | Workforce management add-on priced in every listed currency: $50 / €50 / AU$70 / 6,000 yen / 500 kr / £40 per user per month | Fact (read 18 Oct) | Salesforce price page | (A2) |
| A4 | Change is new: 3 Oct saved copy of the price page carries one "£" character and no local prices; 18 Oct copy carries seven; last week's record (10 Oct 13:10 UTC) says every non-USD cell read "Not currently available in this region" | Fact (orchestrator check, `grep -c "£"` on `2026-10-03-bets-check/scrapes/c/sf-cc-pricing.html` vs `2026-10-18-weekly/scrapes/c/sf-cc-pricing.html`; 10 Oct ledger) | Saved copies; 10 Oct stream C | — |
| A5 | UK page and EU page still show "Not currently available in this region" in every non-USD cell | Fact (read 18 Oct 03:25 UTC) | Salesforce UK / EU pages | https://www.salesforce.com/uk/service/contact-center/ · https://www.salesforce.com/eu/service/contact-center/ |
| A6 | "Coming in November", Casey will rank contact reasons, then build and test fixes; "A human approves every change." | Fact-that-was-SAID (plan) | Salesforce blog 13 Oct | (A1) |
| A7 | Customer-facing Agentforce is metered (Flex Credits, per conversation); no price change this week | Fact (read 18 Oct; diffed against untouched 10 Oct copy `2026-10-10-weekly/scrapes/c/sf-agentforce-pricing.html`) | Salesforce Agentforce pricing | https://www.salesforce.com/agentforce/pricing/ |
| A8 | "Salesforce now competes for contact-centre seats in Europe. Its price list keeps two units: human staff pay per seat, while its customer-facing AI is billed on credits." | Inference (A1, A2, A7) | — | — |

## B. Decagon

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| B1 | Decagon "has hired a bank to evaluate acquisition interest"; "held early discussions with cloud software giant ServiceNow"; early talks with other companies. Unconfirmed | Fact-that-was-SAID (Business Insider, citing people familiar; subscriber wall; carried by PYMNTS) | Business Insider, `datePublished 2026-10-13`; PYMNTS `2026-10-13T23:40:22Z` | https://www.businessinsider.com/ai-agent-company-decagon-hired-investment-bank-acquisition-interest-2026-10 · https://www.pymnts.com/news/acquiring/2026/servicenow-denies-reports-of-takeover-interest-in-ai-agent-startup-decagon/ |
| B2 | Amit Zavery (ServiceNow president): "To be clear, ServiceNow has no interest or intention of purchasing Decagon." | Fact-that-was-SAID | PYMNTS 13 Oct | (B1) |
| B3 | Business Insider story "updated to reflect that ServiceNow says it is no longer in talks with Decagon" | Fact | Business Insider | (B1) |
| B4 | "if a deal does not materialize, Decagon could instead raise a new funding round"; Decagon did not comment | Fact-that-was-SAID · Fact (no Decagon blog post after 7 Oct) | Business Insider; Decagon blog index read 18 Oct | (B1) |
| B5 | $250 million Series D at $4.5 billion valuation, January 2026 | Fact (as cited by PYMNTS from Decagon's January blog) | PYMNTS 13 Oct | (B1) |
| B6 | Salesforce bought Fin last month (closed 10 Sep) | Fact (carried; reported 12 Sep) | 12 Sep ledger | — |
| B7 | "A sale of Decagon would leave buyers with fewer large independent AI customer-service vendors." | Inference (B1, B6) | — | — |

## C. Personal Agent Protocol

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| C1 | Launched by Sierra and Meta on 6 Oct | Fact (carried; reported 10 Oct, A1) | 10 Oct ledger | — |
| C2 | Public GitHub repository created 14 Oct 2026 12:55 UTC; Apache 2.0; 20 commits 14-17 Oct; no releases | Fact | GitHub API `created_at` | https://github.com/personal-agent-protocol/personal-agent-protocol |
| C3 | Labelled "Draft 0.1": "Any part of it can change before a stable version" | Fact (read 18 Oct) | personalagentprotocol.org | https://personalagentprotocol.org/docs/spec |
| C4 | Spec 7.8: each message's sender must be "agent" when the personal agent wrote it, "human only when it carries the User's own words"; spec 7.9: request for a person sets status "queued"; "If no one is available, the status goes back to idle" | Fact | personalagentprotocol.org spec | (C3) |
| C5 | Lorikeet: "Today Lorikeet adds support for the Personal Agent Protocol ... It is live on Lorikeet now"; "Today ChatGPT cannot speak Poppy" | Fact · Fact-that-was-SAID | Lorikeet, `article:published_time 2026-10-12` | https://www.lorikeetcx.ai/blog/personal-agent-protocol |
| C6 | Zendesk Open Service Directory, "a specification and public directory of verified support destinations" for AI assistants; "Zendesk will adopt these protocols" | Fact · Fact-that-was-SAID | Zendesk blog, `datePublished 2026-10-13` | https://www.zendesk.com/blog/product-news/open-service-directory/ |
| C7 | Parloa: "We're building Parloa's Personal Agent Middleware" | Fact-that-was-SAID | Parloa, `datePublished 2026-10-15T14:30Z` | https://www.parloa.com/blog/ensuring-reliable-service-when-personal-ai-agents-are-your-customers/ |
| C8 | Wonderful: "Agent Access is open to design partners" | Fact | Wonderful, `<time> 2026-10-12` | https://www.wonderful.ai/blog-articles/wonderful-agents-can-now-work-with-your-customers-agents |
| C9 | Design-partner list names Genesys, NiCE, Sierra and Zendesk among technology providers; Salesforce and Microsoft absent | Fact (list read 18 Oct) | personalagentprotocol.org | (C3) |
| C10 | "The draft writes a request for a human into the standard. Contact centres should expect personal agents that ask for a person on purpose." | Inference (C4) | — | — |

## D. Starlink and Grok Voice

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| D1 | "Starlink call centers use Grok Voice to answer 20,000 customer calls every day across multiple languages. Roughly 70% are resolved with no human in the loop" | Fact-that-was-SAID (supplier) | xAI, on-page "Oct 14, 2026", `datePublished 2026-10-14` | https://x.ai/news/grok-voice-3 |
| D2 | "A single agent built on Grok Voice 3.0 verifies customers, troubleshoots hardware, issues credits, and ships replacement equipment." | Fact-that-was-SAID | xAI 14 Oct | (D1) |
| D3 | "$0.08 / min ($4.80 / hr)" | Fact (list price on the release) | xAI 14 Oct | (D1) |
| D4 | No definition of "resolved"; no repeat-contact rate | Fact (absence on the release) | xAI 14 Oct | (D1) |
| D5 | "A claimed figure for a whole support line, not a pilot. A per-minute price adds one more unit beside seats, credits and resolutions." | Inference (D1, D3) | — | — |

## E. Fin

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| E1 | 10 Oct read: "Fin's average resolution rate across all customers is 67%, with early-stage teams achieving 76%"; "trusted by 8,000+ businesses resolving over 1 million conversations per week" | Fact (carried; 10 Oct ledger C4 and saved copy) | Fin learning page, `datePublished 2026-10-09` | https://fin.ai/learn/how-to-test-ai-agent-before-deployment |
| E2 | 18 Oct read: "Fin's average resolution rate across all customers is 76%, and it improves approximately 1% per month."; "trusted by 12,000+ businesses resolving over 2 million conversations per week" | Fact-that-was-SAID | Fin learning page | (E1) |
| E3 | `datePublished` and `dateModified` both still 2026-10-09 | Fact (script diff of 10 Oct copy `2026-10-10-weekly/scrapes/c/fin-learn-test.html` vs 18 Oct copy) | Fin learning page metadata | (E1) |
| E4 | "The lower figure was removed, not explained." | Inference (E1-E3) | — | — |

## F. Scheduling

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| F1 | Lorikeet's own row: "New in October 2026; intraday is next, not live at launch"; article says vendor facts "checked on 8 October 2026" | Fact-that-was-SAID | Lorikeet article, `article:published_time 2026-10-08` | https://www.lorikeetcx.ai/articles/workforce-management-software-support-teams-2026 |
| F2 | Launch post unchanged (dateModified 2026-10-08T02:51): "By 9 October, Workforce Manager will manage the day as it happens"; no later dated post, release note (newest 11 Mar 2026), price or named customer | Fact (read 18 Oct) | Lorikeet launch post; release notes; blog index; price page | https://www.lorikeetcx.ai/blog/introducing-workforce-manager · https://www.lorikeetcx.ai/release-notes |
| F3 | Microsoft roadmap: seven "Workforce engagement management" records created 16 Oct; first WFM records seen on the feed in this radar's run | Fact (records' `created` fields) | Microsoft roadmap feed | https://www.microsoft.com/releasecommunications/api/v1/m365 |
| F4 | Record 576761 ("October CY2026"): "When volume remains above forecast for the configured number of intervals, selected recipients receive an in-app notification"; Learn page: "to notify supervisors". Record 576748: interval report comparing forecast, required and scheduled staffing | Fact | Microsoft roadmap; Microsoft Learn `ms.date 2026-08-19` | (F3) · https://learn.microsoft.com/en-us/dynamics365/contact-center/use/workforce-management-use-volume-spike-alerts |
| F5 | Cisne "Accredited Five9 ISV Partner available on the Five9 CX Marketplace"; "modeling variable bot containment rates"; "Algorithmic Intraday Rebalancing ... recommending schedule adjustments" | Fact · Fact-that-was-SAID | Cisne, `datePublished 2026-10-13T17:56:29Z` | https://www.cisne.ai/post/cisne-joins-five9-isv-partner-ecosystem-to-deliver-next-generation-workforce-orchestration |
| F6 | Aspect (26 Feb 2026): "The initial release of Aspect Intelligence includes Automatic Schedule Updates"; product page: "Automatically updates schedules when predefined workforce conditions are met"; "Coming Soon: Intraday Automation" | Fact-that-was-SAID (LATE CATCH, true date 26 Feb 2026) | Aspect resource post (on-page "Feb 26, 2026"); product page (sitemap 22 Jun) | https://www.aspect.com/resources/introducing-aspect-intelligence-closing-the-gap-between-signal-and-action · https://www.aspect.com/workforce-management/aspect-intelligence |
| F7 | Clarification of two published 10 Oct statements: Aspect's August preview "recommends" changes (10 Oct B6) and Lorikeet's offer as "the first offer in our coverage of software changing the live schedule by itself" (10 Oct B7); both hold only for demand-driven intraday changes, not for Aspect's rule-based edits (F6) | Fact (published 10 Oct brief, live at productbeacon.agency/research/state-of-wem-2026/updates/) · Inference | 10 Oct brief | https://productbeacon.agency/research/state-of-wem-2026/updates/wem-radar-weekly-2026-10-10-brief.html |
| F8 | "Software that changes the schedule by itself when live demand shifts is still a promise among the vendors we track. Edits triggered by customer-set rules already exist." | Inference (F1-F6; Aspect roadmap "Automatic Schedule Updates in Real time (Alpha)" still "Exploring", read 18 Oct) | — | https://www.aspect.com/roadmap |

## G. Agent assist

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| G1 | Deputy Agent launched 13 Oct; "refund requests, to transaction disputes, to insurance claim appeals"; works for days or weeks ("When work has to wait for documents or approval, Deputy preserves each workflow's progress") | Fact · Fact-that-was-SAID | PR Newswire, `datePublished 2026-10-13T08:59-04:00`; Cresta blog 13 Oct | https://www.prnewswire.com/news-releases/cresta-launches-deputy-agent-an-ai-agent-that-keeps-working-long-after-the-customer-hangs-up-302906336.html · https://cresta.com/blog/meet-deputy-agent-a-long-running-ai-agent-built-for-customer-operations |
| G2 | It "works alongside employees during live interactions, takes handoffs, or runs independently"; "Your business rules decide which actions happen automatically and which wait for review" | Fact-that-was-SAID | Cresta blog (Ping Wu) 13 Oct | (G1) |
| G3 | No price or availability date; Aqua Finance "see an opportunity"; Sunbit "excites me" | Fact (absence) · Fact-that-was-SAID | Release and blog | (G1) |
| G4 | Five9 site now groups "Agentic AI agents" and "Human agent assist" under "Engage"; "GenAI evaluations & coaching" and "Forecasting & scheduling" under "Optimize"; 10 Oct saved copy used the old menu; sitemap lastmod 15 Oct; no release | Fact (observation; switch between 10 and 15 Oct) | Five9 platform page and sitemap; `2026-10-10-weekly/scrapes/b/five9-events.html` | https://www.five9.com/platform |
| G5 | Five9 "2026 Consumer CX Report": 3,000 consumers (US, UK, Germany), Hanover Research, April 2026; trust "rising from 26% when no human option exists to 55% when one is reachable" | Fact-that-was-SAID (vendor-commissioned) | Five9, dateline "October 14, 2026" | https://www.five9.com/news/news-releases/new-five9-research-reveals-consumers-embrace-ai-customer-service-trust-still |
| G6 | "Both vendors now present help for human agents and autonomous AI as parts of one product." | Inference (G2, G4) | — | — |

## H. Quality and analytics

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| H1 | CallMiner deeper AI Assist analysis and "Redesigned RealTime Command Post"; British Gas: "Tasks that previously took hours of manual analysis can now be completed in minutes." | Fact · Fact-that-was-SAID | CallMiner, dateline "October 14, 2026" | https://callminer.com/news/press-releases/callminer-advances-cx-intelligence-and-agent-augmentation-with-new-ai-powered-capabilities |
| H2 | Verint says it was named a Leader in IDC MarketScape conversational intelligence and analytics 2026; release names no Calabrio product | Fact-that-was-SAID · Fact | Verint, `datePublished 2026-10-14T12:37:51Z` | https://www.verint.com/press-room/2026-press-releases/idc-marketscape-names-verint-leader-2026/ |
| H3 | Record 576842 ("Launched", created 16 Oct): "The quality evaluation skill of the Quality Assurance Agent now includes real-time coaching" | Fact | Microsoft roadmap | (F3) |
| H4 | FourNet acquired SVL (15 Oct); SVL expertise "in interaction recording, analytics and workforce management"; terms not disclosed | Fact · Fact-that-was-SAID | FourNet, `article:published_time 2026-10-15`; IT Brief UK 16 Oct | https://fournet.co.uk/news-events/2026/10/15/fournet-expands-65m-customer-experience-and-ai-business-with-svl-acquisition/ · https://itbrief.co.uk/story/fournet-acquires-svl-business-solutions-in-fifth-deal |

## I. Workplace AI rules

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| I1 | Zaller Law: "Where I do see it come up is in sales and customer service environments that record calls or video meetings, then grade the representative." | Fact-that-was-SAID | California Employment Law Report, `article:published_time 2026-10-17T00:57Z` | https://www.californiaemploymentlawreport.com/2026/10/california-bans-ai-that-reads-employees-moods-ab-1883-five-takeaways-from-our-2027-new-laws-masterclass/ |
| I2 | "A tool that analyzes the guest's sentiment is a different question than one that scores the employee's tone ... the employee-facing piece is what triggers AB 1883." | Fact-that-was-SAID | Zaller 17 Oct | (I1) |
| I3 | "Inventory features, not just products"; contract term requiring vendor notice before new analytics are enabled; AB 1883 effective 1 Jan 2027 | Fact-that-was-SAID · Fact (carried effective date) | Zaller 17 Oct | (I1) |
| I4 | CDF: "Ask vendors to confirm in writing whether any workplace surveillance tool analyzes emotional state ... and disable or replace those features before year-end." | Fact-that-was-SAID | CDF Labor Law, on-page "October 16, 2026" | https://www.cdflaborlaw.com/blog/new-california-employment-laws-for-2027-what-employers-need-to-know |
| I5 | No contact-centre or WEM vendor found renaming, limiting or geo-fencing an emotion, sentiment or wellbeing feature for California | Fact (absence; week-restricted search + Google News) | Stream D | — |
| I6 | techUK: definition "captures routine operational tools and applications such as running payroll, scheduling, workforce planning"; "government should create non-statutory guidance" | Fact-that-was-SAID | techUK, `datePublished 2026-10-13T16:00Z` | https://www.techuk.org/insights/news/getting-workplace-monitoring-technology-right |
| I7 | Consultation still closed with no outcome; closed 30 Sep (16 Oct `updated_at` was a technical republish; `public_updated_at` 8 Jul) | Fact | GOV.UK content API, read 18 Oct | https://www.gov.uk/government/consultations/make-work-pay-workplace-monitoring-technologies |
| I8 | Colorado: AG page `article:modified_time` still 2026-10-08; comments and hearing 26 Oct | Fact | Colorado AG, read 18 Oct; 10 Oct ledger | https://coag.gov/ai/ |
| I9 | "Quality and coaching tools that score both the customer's sentiment and the agent's tone are exposed. Lawyers' advice points to pressure through buyers' contracts first." | Inference (I1-I5) | — | — |

## J. Outsourcers

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| J1 | Foundever (about 130,000 staff) appoints Pierre Barrial CEO, former president and CEO of IDEMIA; "we can accelerate AI deployment" | Fact · Fact-that-was-SAID | Foundever, dateline "Miami, FL, October 13, 2026" | https://foundever.com/news/foundever-appoints-pierre-barrial-as-chief-executive-officer/ |
| J2 | August 2026 recapitalisation cut "nearly $900 million" of gross debt | Fact-that-was-SAID (LATE CATCH, 19 Aug) | Outsource Accelerator, WordPress date 2026-08-19; Foundever release confirms "In August 2026, the company completed a recapitalization" | https://news.outsourceaccelerator.com/foundever-debt-recapitalization/ |
| J3 | Conduent Amendment No. 4 extends revolving commitments "scheduled to mature on October 15, 2026 to October 30, 2026"; lenders "are finalizing the refinancing"; no AI mention | Fact | SEC EDGAR 8-K filed 2026-10-15 | https://www.sec.gov/Archives/edgar/data/1677703/000167770326000134/cndt-20261014.htm |
| J4 | TELUS Digital "will serve as an implementation partner"; enterprises "contract directly with the company for the platform itself and engage TELUS Digital for implementation" | Fact | PR Newswire, dateline "Oct. 14, 2026" | https://www.prnewswire.com/news-releases/telus-digital-partners-with-parloa-to-help-enterprises-build-and-manage-ai-agents-for-stronger-customer-relationships-302907430.html |
| J5 | TP 29th Philippine site, "expected to create more than 1,000 jobs" | Fact-that-was-SAID (TP via Outsource Accelerator citing The Manila Times) | Outsource Accelerator, 2026-10-13 | https://news.outsourceaccelerator.com/tp-pasay-29th-site/ |
| J6 | Fusion CX ₹702 crore issue, 4.68 times subscribed (16 Oct); total income ₹1,851.83 crore vs ₹1,352.03 crore (+37%), year to 31 Mar 2026 | Fact (as compiled from offer documents; prospectus not opened) | Chittorgarh, `dateModified` 16 Oct | https://www.chittorgarh.com/ipo/fusion-cx-ipo/ |
| J7 | GSAJ: jobs fell from peak 60,000 to about 40,000; president "rejected the claim that AI was mainly to blame, pointing instead to operational inefficiencies, high electricity costs and weak international promotion" | Fact-that-was-SAID (via Outsource Accelerator citing Jamaica Observer) | Outsource Accelerator, 2026-10-17 | https://news.outsourceaccelerator.com/jamaica-bpo-jobs-1bn-goal/ |
| J8 | Aneel Bhusri: "a lot of the low-level automation jobs that have been outsourced, that's where I worry the most" | Fact-that-was-SAID | Rediff (PTI), `datePublished 2026-10-15T19:53+05:30` | https://www.rediff.com/business/report/workday-ceo-ai-will-replace-low-cost-outsourced-jobs/20261015.htm |
| J9 | "The strain on outsourcers is uneven. Indebted firms are restructuring around AI while others still add seats and raise money." | Inference (J1-J7; TTEC 7 Oct and Concentrix 29 Sep carried) | — | — |

## K. Pricing and public set

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| K1 | No tracked vendor moved from per-resolution or per-outcome back to per-seat; ten pages re-read 18 Oct (Salesforce Agentforce, contact-centre price and overview, Fin, Zendesk, Lorikeet page and price file, Microsoft D365 Contact Center, Genesys, NiCE) | Fact (script diff; baselines: untouched 10 Oct Agentforce copy; 3 Oct copies for the rest, see incident note) | Stream C finding 9 | https://fin.ai/pricing (and A2, A7) |
| K2 | Only change: GBP, EUR and SEK prices added to the seat-priced contact centre; per-conversation price for customer-facing AI unchanged | Fact | A2, A4, A7 | — |
| K3 | "Beginning December 1, 2026, new Microsoft 365 Copilot ... offers can be purchased without a qualifying Microsoft 365 base subscription ... priced the same" | Fact | Microsoft Partner Center, "Date : October 14, 2026" | https://learn.microsoft.com/en-us/partner-center/announcements/2026-october |
| K4 | Default usage-based billing for new Copilot Business licences from 1 Dec ("previously communicated as November 2"); "will initially not be available in Australia, Belgium, Brazil, France, Germany, India, Italy, Korea, the Netherlands, Poland, and Spain" | Fact | Microsoft Partner Center, "Update 10/14" | (K3) |
| K5 | Tottenham Hotspur: "20% of interactions resolved by Agentforce alone"; "When Ask Spurs can't resolve a question, it hands the conversation seamlessly to a human agent on the Tottenham Hotspur Support team." | Fact-that-was-SAID (vendor release) | Salesforce, `datePublished 2026-10-15T07:00Z` | https://www.salesforce.com/news/press-releases/2026/10/15/tottenham-hotspur-becomes-agentic-enterprise-with-agentforce/ |
| K6 | AlloBrain (Paris) raised $7 million led by Varsity; platform combines "real-time advisor assistance, quality analysis across all conversations, 24/7 AI agents" | Fact · Fact-that-was-SAID | Startup.eu, on-page "Oct 14, 2026"; Dealroom | https://www.startup.eu/investments/allobrain-7-m-10-2026 |
| K7 | NiCE investors page: "No current upcoming events. Stay tuned." (no Q3 results date); every Actimize hit in window resolved to the 23 Sep reports | Fact (read 18 Oct) | NiCE investors page | https://www.nice.com/investors |
| K8 | Five9: no Q3 results-date announcement found; no 8-K since 6 Aug | Fact (absence; EDGAR submissions read 18 Oct) | SEC EDGAR | — |

## L. Watch list and evidence line

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| L1 | Zoomtopia 20-22 Oct (virtual by region) | Fact | Zoom event pages (stream B quiet checks) | — |
| L2 | LISTEN West "Oct. 20–21 in Dallas, Texas" | Fact | CallMiner release (H1) | (H1) |
| L3 | Colorado 26 Oct; Microsoft results 28 Oct; Conduent 30 Oct (J3); TTEC 16 Nov and Microsoft Sales Development Agent credits 16 Nov (carried, 10 Oct ledger); Microsoft 1 Dec (K3); California and Colorado 1 Jan 2027 (carried) | Fact | As cited | — |
| L4 | Automation Anywhere / Boost.ai close "expected ... in Q4 2026"; not closed (press room newest 7 Oct) | Fact (carried; checked 18 Oct) | Automation Anywhere press room | — |
| L5 | New companies pending triage: AlloBrain (K6), Wonderful (C8), xAI Grok Voice (D1), Fusion CX (J6; subsidiary Omind builds quality automation and WFM tools), FourNet (H4) | Fact | As cited | — |
| L5b | Correction: 10 Oct edition listed "Observe.AI on 13 and 14 October"; Observe.AI's TransformX page gives 24-26 February 2026 (Caesars Forum, Las Vegas) | Fact (10 Oct brief line 136, published) · Fact (Observe.AI page read 18 Oct) | Observe.AI | https://www.observe.ai/transformx |
| L6 | Evidence line: Salesforce Europe and Starlink bear on one-engine and displacement predictions; intraday stops at alerts and recommendations | Inference (A, D, F) | — | — |

---

## Corrections and internal notes

- **Observe.AI event date (watch list, 10 Oct brief):** last week's brief listed "Observe.AI on 13 and 14 October". Observe.AI's own TransformX page gives 24-26 Feb 2026 (Las Vegas). The 13-14 Oct date was carried from the 3 Oct ledger (K1) without a primary source. The 10 Oct edition IS published (live HTTP 200 at `productbeacon.agency/research/state-of-wem-2026/updates/wem-radar-weekly-2026-10-10-brief.html`, checked 18 Oct), so the brief carries one correction sentence (L5b). The orchestrator first misread the hub folder (the hub moved from `state-of-wfo-2026` to `state-of-wem-2026`); the pack worker caught it. A "Fall 2026 TransformX" virtual partner session is listed for 5 Nov (sitemap, modified 15 Oct); not carried into the brief.
- **Stream B's Salesforce price-page comparison is void:** stream B compared the US contact-centre price page with the "10 Oct saved copy", but that file had been overwritten with the 18 Oct page by stream C at 02:27 UTC (incident below). The orchestrator re-checked against the 3 Oct copy (A4); stream C's reading stands.
- **Assembled as a Five9 partner:** stream A wrote that Five9 has had Assembled as a WFM partner "since April". No record of this exists in the radar's files; the claim was dropped from the brief.

## Incident: overwritten price-page baselines

Stream C's shell command lost its folder change and saved nine 18 Oct price-page reads into `2026-10-10-weekly/scrapes/c/`, overwriting last week's copies: `fin-pricing.html`, `genesys-pricing.html`, `lk-pricing.md`, `lorikeet-pricing.html`, `ms-d365cc-pricing.html`, `nice-pricing.html`, `sf-cc-overview.html`, `sf-cc-pricing.html`, `zendesk-pricing.html` (file times 2026-10-18 05:27 local). `sf-agentforce-pricing.html` and `fin-learn-test.html` were untouched. This week's pages were compared with the 3 Oct copies instead. The 10 Oct versions can be restored from Google Drive version history ("Manage versions"). Next week's baseline is `2026-10-18-weekly/scrapes/c/`.

## Not used (recorded so they are not mistaken for misses)

- **Salesforce acquires Loops (12 Oct):** analytics for Tableau; outside the WEM lane.
- **Parloa-Epic integration (12 Oct), ASAPP CMO (14 Oct), Level AI advisory board (14 Oct):** low materiality.
- **Sprinklr director open-market purchase (150,000 shares, 13 Oct) and Voss Capital below 5% of Five9 (filed 16 Oct):** routine filings; in research notes.
- **Genesys summarisation-model deprecation notice (12 Oct) and Telecom Reseller interview (16 Oct):** no product move.
- **Guardian (13 Oct) on companies slowing AI rollouts; Harvard JOLT digest on chatbot "gatekeepers":** commentary, not moves.
- **8x8 WFM customer growth claim (CX Today, 16 Oct):** excluded vendor, no base.
- **Aspect blog on personal agents and demand (15 Oct):** positioning.
- **Parloa study "fewer than 9% of chatbot conversations reached resolution":** vendor study, undated; not load-bearing.
- **PolyAI ranking, Five9 and Genesys workplace awards:** positioning.

## Research-security note

Text addressed to AI agents appeared again on Lorikeet's pages (Workforce Manager post and machine-readable price file: an endpoint for AI assistants and HTTP sign-up instructions). Treated as data about Lorikeet's go-to-market; not acted on. LinkedIn not opened or queried. NiCE researched through public sources only (press index, investors page, sitemaps, price page, the protocol partner list); Cognyte absent.

## Coverage

- Search: 4 parallel foreground streams via the Firecrawl REST helper (MCP server failed to connect). Credits: A 40, B 40, C 36, D 28 (13 searches + 2 paid scrapes) = 144. Meter before research: 5,625 (new billing period from 12 Oct).
- About 310 free page reads (newsrooms, sitemaps, EDGAR for the six public-set tickers and four outsourcers, ten price pages, the Microsoft roadmap feed, the AWS What's New feed, GitHub API, GOV.UK API, Colorado AG page).
- The custom date-range filter (`cdr:1`) was accepted but did not limit results; streams used `qdr:w` and covered 10-11 Oct by direct reads.
- LinkedIn: not collected (v1 search-only).
- SEC leads: no feeder in v1 (EDGAR read directly: no 8-K, 6-K, 10-Q or results-date announcement from NICE, FIVN, CRM, CXM, MSFT, ZM in window).
- Blocked this run: Colorado comment site (script-rendered, also failed as a paid scrape); Business Wire; StockTitan; Five9 and Zoom investor sites; CU Today.
- Date traps caught: 43 (A=9, B=12, C=10, D=12).

## Link audit (L-076)

Run 2026-10-18 via `reports/research/2026-10-18-weekly/link-audit-2026-10-18.py` (re-runnable; raw result in `link-audit-2026-10-18.json`).

**50 unique URLs** extracted from this ledger (before the correction rows were added; the two added URLs, the Observe.AI TransformX page and the 10 Oct brief, were read 200 in-run). Every brief URL is among them except the parent-report link in the disclosure line. Measured result: **48 returned HTTP 200-range · 2 bot-gated · 0 dead · 0 timeouts.**

Per L-076 a bot-gate is **VERIFY-MANUALLY**, not dead:

| URL | Status | Handling |
|---|---|---|
| californiaemploymentlawreport.com AB 1883 post (I1-I3) | 403 | VERIFY-MANUALLY. Browser check blocks generic clients; read in-run by stream D through a paid scrape (`article:published_time 2026-10-17T00:57Z`). Not demoted. |
| sec.gov Conduent 8-K (J3) | 403 | VERIFY-MANUALLY. SEC refuses generic user agents; read in-run by stream D with a descriptive user agent. Not demoted. |

**Zero claims demoted.**

## Register gate

**SOP-2 §6c, run 2026-10-18 by an independent reviewer (not the pack builder) on every public derivative of this edition. Verdict: EDITED then PASS.**
Full record: `ProductBeacon/Marketing/social-assets/state-of-wfo-2026/radar-weekly-2026-10-18/register-gate-2026-10-18.md`.

| Derivative | Claims traced | Result |
|---|---|---|
| Carousel (`carousel.html`, 11 PNGs, `wem-radar-weekly-2026-10-18.pdf`) | 99 | EDITED (E1-E8: hedge pairing, Inference as fact, scope of absolutes, vendor voice), then PASS |
| Caption A | 21 | EDITED (E9-E10: Inference as fact, scope of absolutes), then PASS |
| Caption B | 2 | PASS |
| First comment | 0 | PASS |
| Yohay comment | 2 | PASS |
| Stakeholder note | 3 | PASS |
| Update card (text and HTML), 430 characters | 7 | PASS |
| Posting console | mirrors the five blocks | PASS |

E11 moved the protected-span proposals to the corrected wording (red test confirmed the checker fails on revert). Nine brief-of-record observations were then applied by the orchestrator to `radar-2026-10-18.md`: the scheduling absence hedged ("As far as we can tell") [F8]; Australia and New Zealand attributed to Salesforce's plan [A1]; Cresta's customers "speak of 'an opportunity' and excitement" [G3]; Aspect "says its February release included" [F6]; "Cisne says" [F5]; the California absence scoped to "contact-centre or WEM vendor ... emotion, sentiment or wellbeing" [I5]; "Cresta says it keeps working" [G1]; TP's jobs "which TP expects ..., Outsource Accelerator reports" [J5]; the Microsoft clause removed from the headline bullet (its section bullet already reads "alert supervisors and report staffing against forecast") [F4].

NiCE: 0 on slides 2-10, captions, comments, stakeholder note, card and console; cover compact line and closing full Integrity Wall only (disclose-once, DR-2026-228). No em dashes; only `[first name]` and `[LINKEDIN POST URL]` placeholders.

**Register gate: PASS — 134 claims traced across 8 derivatives.**
