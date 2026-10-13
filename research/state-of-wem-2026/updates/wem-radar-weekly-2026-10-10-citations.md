# WEM Radar 2026-10-10 — Citations ledger

Edition: **WEEKLY** (no periodic prediction check; last check 2026-10-03, 7 days earlier). Collection window 2026-10-03 (after ~04:00 UTC) → 2026-10-10.
One row per load-bearing claim in `radar-2026-10-10.md`. Claim typing per L-077: **Fact** · **Fact-that-was-SAID** (a named party asserted it; the assertion is the fact) · **Estimate** · **Inference** (our reading).
Raw research: `reports/research/2026-10-10-weekly/` (streams A-D, raw search logs `raw-*-search.md`, call logs `fc-log-*.jsonl`, saved pages under `scrapes/a-d/`). Every date was read off the page itself (`datePublished`, `article:published_time`, the printed dateline, EDGAR filing date, or a roadmap record's `created` field), never a search snippet.

No claim appears in the brief without a row here.

---

## A. Personal Agent Protocol

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| A1 | Sierra and Meta announced the Personal Agent Protocol on 6 Oct: "an open standard Meta and Sierra are developing along with industry partners at Genesys, Instinct, Rocket, Shopify, Stripe, and Walmart that defines how personal agents interact with businesses" | Fact | Sierra, `datePublished 2026-10-06T17:32:00Z` | https://sierra.ai/blog/introducing-personal-agent-protocol |
| A2 | Meta's own partner list names Genesys, NiCE, Decagon, Rocket, Shopify, Stripe and Walmart | Fact-that-was-SAID (CMSWire reporting Meta's post; Meta's page blocked to free read) | CMSWire, `datePublished 2026-10-06T21:31:29Z` | https://www.cmswire.com/contact-center/genesys-joins-sierra-meta-on-open-standard-for-personal-ai-agents-01/ |
| A3 | Sessions run on OAuth; the customer chooses "read-only or write access"; the personal agent identifies itself "so the company always knows when an agent is acting for a customer" | Fact | Sierra 6 Oct; Sierra 9 Oct (`datePublished 2026-10-09T19:56:06Z`) | (A1) · https://sierra.ai/blog/poppy |
| A4 | 9 Oct: draft published ("Poppy") and 35 additional design partners announced, incl. OpenAI, Zendesk, Bank of America, Visa | Fact | Sierra 9 Oct | https://sierra.ai/blog/poppy |
| A5 | Decagon open-sourced PACT, "co-developed and supported by Instinct", and is joining "the Personal Agent Protocol working group" (6 Oct) | Fact | Decagon, `datePublished 2026-10-06T15:00:00Z` | https://decagon.ai/blog/introducing-the-personal-agent-consent-trust-protocol-pact |
| A6 | Sierra's fleming-1 "detects when the caller on a phone call is another agent" (8 Oct) | Fact-that-was-SAID | Sierra, `datePublished 2026-10-08T17:32:00Z` | https://sierra.ai/blog/caller-id-in-the-age-of-agents |
| A7 | Tony Bates (Genesys CEO): "Personal AI is creating a new front door to the enterprise." | Fact-that-was-SAID | Sierra 6 Oct | (A1) |
| A8 | Salesforce on neither list; 9 Oct: "personal agents are only as reliable as the business agents waiting to greet them at the front door" | Fact (absence, both lists read) · Fact-that-was-SAID | Salesforce, `datePublished 2026-10-09T18:30:00+00:00` | https://www.salesforce.com/news/stories/personal-ai-agents-evolution/ |
| A9 | "A contact-centre platform joined a standard led by an AI-agent startup. The standard settles identity and permission, not whose agent answers." | Inference (A1, A3; a personal agent may route via website, APIs or the company's agent per Sierra 9 Oct) | — | — |
| A10 | Personal agents that cannot finish on a website "may call the company's support line or open its web chat" | Fact-that-was-SAID (Sierra) | Sierra 6 Oct | (A1) |
| A11 | First specification version planned "later this month" | Fact-that-was-SAID (plan) | Sierra 6 Oct | (A1) |

## B. Lorikeet Workforce Manager and workforce management

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| B1 | Launched 7 Oct; builds the roster "from your actual ticket and call volume, then checks every shift against your team's working rules ... before you publish" | Fact | Lorikeet, `datePublished 2026-10-07` | https://www.lorikeetcx.ai/blog/introducing-workforce-manager |
| B2 | "Built for support teams of 20+ agents running live chat or phones"; shortfalls "up to 12 months ahead" | Fact | Lorikeet 7 Oct | (B1) |
| B3 | "By 9 October, Workforce Manager will manage the day as it happens ... notify you so you can decide, propose a fix for one-click approval, or apply the fix itself" | Fact-that-was-SAID (a plan; shipping not verified: no dated Lorikeet post on 9-10 Oct found in the blog index read 10 Oct) | Lorikeet 7 Oct; blog index `scrapes/c/lk-blog-1010.html` | (B1) |
| B4 | No published price (price page and `/pricing.md` read 10 Oct) and no named customer | Fact (absence) | Lorikeet price page | https://www.lorikeetcx.ai/pricing |
| B5 | "We're building Lorikeet into an AI CX leader that manages your human team and your AI agents together" | Fact-that-was-SAID | Lorikeet 7 Oct | (B1) |
| B6 | Aspect roadmap lists "Aspect Intelligence: Automatic Schedule Updates in Real time (Alpha)" as "Exploring"; August preview (25 Aug, already reported) "recommends" | Fact (page undated; last changed 21 Aug per sitemap) · Fact (carried) | Aspect roadmap, read 10 Oct | https://www.aspect.com/roadmap |
| B7 | "First offer in our coverage of software changing the live schedule by itself" | Inference (checked against the radar's reported list: Aspect, Assembled, Cisne, Microsoft, NiCE items claim recommendations or narrow actions only) | `_already-reported.md` | — |
| B8 | Cisne: Jim Nystrom "has joined as Chief Revenue Officer"; formerly "Executive Vice President of Global Sales at Five9"; Cisne unifies planning "across the entire hybrid workforce" | Fact · Fact-that-was-SAID | Cisne, `datePublished 2026-10-05T21:39:48Z` | https://www.cisne.ai/post/cisne-names-industry-veteran-jim-nystrom-chief-revenue-officer |
| B9 | Assembled Dynamic Routing applies "the queue-level business hours already configured in Assembled Workforce Management" to offer live chat or email; "available now for chat agents" | Fact-that-was-SAID (LATE CATCH: on-page 1 Oct, not in 3 Oct edition) | Assembled, on-page "October 1, 2026" | https://www.assembled.com/blog/dynamic-routing |

## C. Fin 4

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| C1 | Fin owned by Salesforce since 10 Sep | Fact (carried; reported 12 Sep) | 12 Sep ledger | — |
| C2 | Fin 4 launched 7 Oct; proactive outreach ("Fin now onboards, activates, and re-engages your customers"); Human in the Loop "Confidence score" | Fact | Fin, on-page "7 October 2026" | https://fin.ai/blog/introducing-fin-4 |
| C3 | "Fin now has 12,000 customers, resolves more than 10 million conversations a month, and averages a 76% resolution rate." | Fact-that-was-SAID | Fin, on-page "8 October 2026" | https://fin.ai/blog/pioneer-2026-fin-4-operator-and-the-evolution-of-human-work |
| C4 | "Fin's average resolution rate across all customers is 67%, with early-stage teams achieving 76%" | Fact-that-was-SAID | Fin learning centre, `datePublished 2026-10-09` | https://fin.ai/learn/how-to-test-ai-agent-before-deployment |
| C5 | "a very clear path to a fully agentic customer experience" in which 90-95% of customer communication "will not involve a human" | Fact-that-was-SAID | Fin 7 Oct | (C2) |
| C6 | $0.99 per outcome unchanged; Pro add-on "From $ 99" → "From $ 100" per month | Fact (page read 10 Oct 13:10 UTC, diffed by script against 3 Oct copy) | Fin pricing | https://fin.ai/pricing |
| C7 | Two pages differ by nine points in two days; cite only with page and date | Inference | C3, C4 | — |

## D. Deals and funding

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| D1 | Automation Anywhere "entry into a definitive agreement to acquire Boost.ai from Nordic Capital"; close "expected ... in Q4 2026, subject to customary regulatory approvals"; terms not disclosed | Fact | Boost.ai (release mirror), dateline "October 7, 2026"; Destination CRM `2026-10-07` ("Financial terms ... were not disclosed") | https://boost.ai/announcements/automation-anywhere-to-acquire-boost.ai/ · https://www.destinationcrm.com/Articles/CRM-News/CRM-Across-the-Wire/Automation-Anywhere-to-Acquire-Boost.ai-176924.aspx |
| D2 | Boost.ai: chat and voice AI agents and agent assist; strength in Europe in financial services, telecoms, insurance | Fact-that-was-SAID · Fact (site navigation lists "Agent Assist") | Boost.ai release | (D1) |
| D3 | "approximately 600 live AI agents, and has supported more than 150 million automated conversations" | Fact-that-was-SAID | SiliconANGLE, `datePublished 2026-10-08T18:05:27Z` | https://siliconangle.com/2026/10/08/automation-anywhere-acquires-boost-ai-to-expand-customer-facing-voice-ai/ |
| D4 | Second such purchase after Aisera (late 2025) | Fact-that-was-SAID | Release | (D1) |
| D5 | "New exit route for mid-sized specialists" | Inference | D1-D4 | — |
| D6 | TCN: billing consolidated "starting October 1, 2026"; "Full native integration will take time" | Fact-that-was-SAID (NEW BEAT on 1 Oct deal) | TCN, `datePublished 2026-10-07T13:00:00+00:00` | https://www.tcn.com/blog/tcn-abstrakt-bringing-next-generation-ai-agent-assist-to-the-contact-center/ |
| D7 | Flyle "raised ¥1.88 billion ($12.6 million) in Series A"; investors incl. Salesforce Ventures | Fact-that-was-SAID (secondary; Flyle's own release not opened; round's own announcement date not established) | FinTech Observer, `datePublished 2026-10-09T08:50:42Z` | https://www.fintechobserver.com/megabanks-participate-in-flyles-jpy-1-88bn-series-a-to-expand-ai-agents-in-contact-centers/ |
| D8 | Genesys acquired Pinkfish on 30 Jun; 500+ integrations, 25,000 MCP tools; terms undisclosed | Fact-that-was-SAID (LATE CATCH; Genesys release not located) | CMSWire, `datePublished 2026-06-30T12:30Z` | https://www.cmswire.com/contact-center/genesys-acquires-pinkfish-to-boost-agentic-ai/ |

## E. Colorado and California

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| E1 | "On October 6, 2026, the DOL released an interim draft of the rules"; comments close "October 26, 2026 at 11:59 P.M. MST"; rules "shall become effective January 1, 2027"; hearing 26 Oct | Fact | Colorado AG page (`article:modified_time 2026-10-08T15:58Z`); interim draft | https://coag.gov/ai/ · https://coag.gov/app/uploads/2026/10/2026.10.06-ADMT-Chatbot-Act-Rulemaking-Interim-Draft-Redline.pdf |
| E2 | "tools used by individuals solely to summarize, organize, translate, draft, route, or present information for human review [or] administrative processing are excluded from the definition of ADMT" | Fact (redline; whether newly inserted or carried over not separable in extract) | Interim draft | (E1) |
| E3 | Promotion example: decision maker sees each score; "It is presumed that the ADMT output Materially Influenced the Consequential Decision because the decision maker was presented with the score" | Fact | Interim draft | (E1) |
| E4 | Cover page asks for "an effective alternative to the rebuttable presumption" | Fact | Cover page dated "October 6, 2026" | https://coag.gov/app/uploads/2026/10/2026.09.28-Interim-Rules-Cover-Letter_updated-v2.docx |
| E5 | Two-human-reviewer promotion example still requires adverse-outcome disclosure | Fact | Interim draft | (E1) |
| E6 | Chatbot rules: "narrow and discrete topic" such as "a status update about a purchase, answering a billing question, or scheduling an appointment" | Fact | Interim draft | (E1) |
| E7 | No formal grace period ("the laws go into effect on January 1, 2027 per the statute"); AG policy "to focus on egregious and intentional violations" | Fact | Cover page | (E4) |
| E8 | "Scores that managers see before people decisions will need documented human judgment. Summaries and routing do not." | Inference (E2, E3, E5; draft, not final) | — | — |
| E9 | Epstein Becker Green: "Call-center sentiment analysis ... [among] the likeliest trouble spots"; "a conservative approach is to apply the prohibition to all workers of a California employer pending further guidance" | Fact-that-was-SAID | Epstein Becker Green, on-page "October 7, 2026" | https://www.ebglaw.com/insights/publications/four-new-california-laws-reshape-the-rules-for-workplace-ai |
| E10 | No vendor renaming/limiting/removing an emotion feature; no California agency guidance | Fact (absence; streams B and D targeted searches; DIR, EDD, Governor newsroom 5-9 Oct) | streams B finding 5, D finding 10 | — |

## F. Demand side

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| F1 | "Global call center headcount is 5.3% below its December 2023 peak"; eight year-on-year falls in 70 quarter-end readings since 2009, all in the last eight quarters | Fact-that-was-SAID · Estimate (modelled from online professional profiles) | Revelio Labs, `datePublished 2026-10-06T16:00Z` | https://www.reveliolabs.com/news/ai-and-work/after-a-decade-of-growth-global-call-center-employment-is-shrinking/ |
| F2 | 12 middle-income countries: call-centre headcount stalled or fell after ChatGPT while other office work grew; "We cannot observe which firms replace people with chatbots" | Fact-that-was-SAID | Revelio Labs | (F1) |
| F3 | Concentrix Q4 guide: "constant currency revenue decline for the quarter ranging from (5.0)% to (3.0)%"; $1,050.0M goodwill impairment "primarily resulting from the trading range for the Company's stock price and market capitalization" | Fact (LATE CATCH: 29 Sep) | Concentrix 8-K Ex. 99.1, dateline "Sept. 29, 2026" | https://www.sec.gov/Archives/edgar/data/1803599/000180359926000147/exhibit991q32026.htm |
| F4 | CEO Chris Caldwell: "While we are aggressively disrupting our own traditional business, the underlying new business is stronger and healthier." | Fact-that-was-SAID | Concentrix release | (F3) |
| F5 | TTEC: revolving commitments reduced "by $15 million, to $960 million"; margin increase to 6.250% "will take effect on November 16, 2026 unless a subsequent amendment ... provides otherwise" (3.250% until 15 Nov) | Fact | TTEC 8-K, EDGAR filing date 2026-10-07 | https://www.sec.gov/Archives/edgar/data/1013880/000110465926114376/0001104659-26-114376-index.htm |
| F6 | 3M reorganising customer service under global hubs, Manila first; CEO (July): "partnering with an external provider to run them at scale using automation and AI" | Fact-that-was-SAID | Star Tribune, `datePublished 2026-10-08T10:00Z` | https://www.startribune.com/3m-layoffs-customer-service-division-philiippines/601898409 |
| F7 | Challenger: AI "fifth-most cited reason with 3,961 cuts in September, about 9%"; "120,136 ... approximately 21% of all cuts" year to date | Fact-that-was-SAID (LATE CATCH: 1 Oct) | Challenger, Gray & Christmas, WordPress `date 2026-10-01T04:30` | https://www.challengergray.com/blog/job-cuts-fall-in-september-hiring-plans-up-3-over-2025-on-weak-early-seasonal-hiring/ |
| F8 | HubSpot: ~7% of workforce, "nearly 660 HubSpotters"; "This is not driven by AI-related efficiencies"; outcomes shift "is transforming product, pricing" | Fact (8-K Item 2.05) · Fact-that-was-SAID | HubSpot 8-K Ex. 99.1, filed 2026-10-06 | https://www.sec.gov/Archives/edgar/data/1404655/000119312526414965/d183135dex991.htm |
| F9 | ISG: BPO "rising 12% to $2.1 billion" in Q3 | Fact-that-was-SAID (via trade report; Business Wire original blocked) | Outsource Accelerator, `date 2026-10-09T21:00` | https://news.outsourceaccelerator.com/isg-index-q3-2026/ |
| F10 | French telemarketing consent rule (in force 11 Aug): ~10,000 jobs Morocco, ~5,000 Tunisia | Estimate (union figures; LATE CATCH: 30 Sep) | UNI Global Union, `datePublished 2026-09-30` | https://uniglobalunion.org/news/new-french-law-leads-to-job-losses-in-morocco-and-tunisia/ |
| F11 | "Evidence of fewer human seats is growing, but employers rarely name AI as the cause." | Inference (F1-F10) | — | — |

## G. Quality scoring

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| G1 | IDC: "some vendors that formerly fit squarely into this evaluation's requirements are refocusing on providing AI agents instead"; no vendors named | Fact-that-was-SAID (IDC quoted by Genesys) | Genesys, dateline "Oct. 6, 2026" | https://www.genesys.com/company/newsroom/announcements/genesys-recognized-as-a-leader-in-the-2026-idc-marketscape-for-worldwide-conversational-intelligence-and-analytics |
| G2 | Amazon Connect suggests changes to evaluation forms; "helps managers automatically score human and AI agents fairly and accurately" | Fact · Fact-that-was-SAID | AWS What's New, "Posted on: Oct 9, 2026" | https://aws.amazon.com/about-aws/whats-new/2026/10/amazon-connect-customer-automated-checks-evaluation-forms/ |
| G3 | Microsoft Quality Evaluation "now supports recurring frequency"; bulk and sampled evaluations; status "Launched", "October CY2026" | Fact | Microsoft roadmap record 573267, `created 2026-10-05T23:03:05` | https://www.microsoft.com/releasecommunications/api/v1/m365 |
| G4 | Parloa Relationship Score: "one score out of 100", built on Lens's "50+ performance, quality, and compliance-related LLM-judged diagnostic evaluations"; older metrics "say little about how the conversation actually felt"; no price or customer figures | Fact · Fact-that-was-SAID · Fact (absence) | Parloa, `first_published_at 2026-10-08` | https://www.parloa.com/blog/relationship-score-for-ai-led-customer-experience/ |
| G5 | Zenarate release 8 Oct: "did the problem get solved?"; TruGreen onboarding -50%; Sallie Mae attrition -32% | Fact-that-was-SAID (vendor figures; NEW BEAT on 1 Oct item) | PR Newswire, `datePublished 2026-10-08T09:10-04:00` | https://www.prnewswire.com/news-releases/zenarate-unveils-new-vision-built-on-one-simple-question-for-human-and-ai-customer-service-did-the-problem-get-solved-302902481.html |
| G6 | "Quality measurement is moving to one standard for people and bots" | Inference (G1-G5) | — | — |

## H. Pricing lane

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| H1 | No tracked vendor reverted to per-seat; nine price pages read 10 Oct 13:10 UTC and diffed by script against 3 Oct copies (Salesforce Agentforce, Salesforce contact centre overview and pricing, Fin, Zendesk, Lorikeet, Microsoft D365 Contact Center, Genesys, NiCE CXone) | Fact | stream C finding 7; `scrapes/c/` | https://www.salesforce.com/agentforce/pricing/ · https://www.zendesk.com/pricing/ · https://www.lorikeetcx.ai/pricing · https://www.microsoft.com/en-us/dynamics-365/products/contact-center/pricing · https://www.genesys.com/pricing · https://www.nice.com/pricing |
| H2 | Microsoft: Sales Development Agent "will start consuming Copilot credits on November 16, 2026"; Service Agent autonomous capabilities in private preview for "a select group of Frontier customers"; "Outside business hours, it resolves what it can and escalates" | Fact | Microsoft, `datePublished 2026-10-08T15:00:00+00:00` | https://www.microsoft.com/en-us/copilot/blog/2026/10/08/bringing-crm-into-the-flow-of-work-and-agents-into-business-process-for-sales-and-service-teams/ |
| H3 | Sierra: Horizon is "Sierra's outcomes-based model at scale: you pay for results, not tokens"; no price list | Fact-that-was-SAID · Fact (absence) | Sierra, `datePublished 2026-10-06T18:01:51Z` | https://sierra.ai/blog/summit-recap-2026 |
| H4 | Salesforce contact-centre pricing: all 75 non-USD cells "Not currently available in this region" | Fact (read 10 Oct) | Salesforce | https://www.salesforce.com/service/contact-center/pricing/ |
| H5 | HubSpot: no price change announced | Fact (absence in memo and 8-K) | F8 | — |

## I. Deployment and other company developments

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| I1 | Florida Prepaid: Agentforce Voice "is now the first point of contact for 75% of business-hours calls"; AI calls ~1.6 min vs 10.9 min human; ~35% of chat representatives redeployed to revenue roles; article "made possible by our sponsor Salesforce" | Fact-that-was-SAID (vendor-sponsored) | Nextgov sponsored content, `datePublished 2026-10-05T09:00:00` | https://www.nextgov.com/sponsors/2026/10/florida-prepaids-call-center-never-closes-thanks-agentforce-voice/415808/ |
| I2 | "First point of contact counts the calls the AI answers, not the calls it resolves" | Inference | I1 | — |
| I3 | Sierra summit: Curie and Fleming models; Tandem Voice; partner ecosystem; "almost 50% of the Fortune 50" | Fact · Fact-that-was-SAID | Sierra 6 Oct (recap and partners posts) | https://sierra.ai/blog/summit-recap-2026 · https://sierra.ai/blog/the-sierra-partner-ecosystem |
| I4 | Cresta: Conductor built "on the Claude Agent SDK"; "cuts initial deployment time roughly in half" | Fact-that-was-SAID | Cresta, on-page "October 5, 2026" | https://cresta.com/blog/bringing-ai-agent-development-to-more-teams-with-cresta-and-anthropic |
| I5 | NiCE: investor page "No current upcoming events" (read 10 Oct; last trade 9 Oct); no Q3 date; Actimize unconfirmed | Fact (absence) | NiCE investors (public page; no LinkedIn) | https://www.nice.com/company/investors |
| I6 | Five9: newest release 26 Aug; no 8-K since 6 Aug; CX Connect Americas, New York, 12-13 Oct | Fact | EDGAR CIK 1288847; Five9 events page | https://www.five9.com/about/events |

## J. What to watch

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| J1 | Observe.AI 13-14 Oct | Fact (carried from 3 Oct ledger K1) | — | — |
| J2 | Microsoft FY27 Q1 results 28 Oct | Fact | Microsoft investor relations (stream B quiet checks) | — |
| J3 | Evidence line: Lorikeet bears on autonomous intraday scheduling, last assessed "weakened" (3 Oct check) | Inference · Fact (3 Oct assessment) | 3 Oct brief | — |
| J4 | New companies pending triage: Boost.ai, Flyle, Meta, Cinareo (Aspect partner page, undated) | Fact | D1, D7, A2; https://www.aspect.com/page/cinareo-x-aspect | — |

---

## Not used (recorded so they are not mistaken for misses)

- **Google Gemini at Work (Home Depot, Verizon):** vendor claims with no rates; low weight.
- **Sprinklr CEO planned share sale (Form 4, 10b5-1):** routine.
- **Microsoft Quality Evaluation for custom records (preview Oct, GA Jan 2027):** in research notes only.
- **Verint automated QM buyer's guide (9 Oct) and Cresta QM page:** marketing pages, no release. Verint re-stamped ~50 old releases (date trap).
- **Centrical CEO interview (8 Oct):** interview, vendor figures; Series D is 2 Jun (date trap).
- **NovelVox Five9 ISV status:** partner-announced, low weight.
- **Siena "agent of record" (VentureBeat headline):** page 429, unread.
- **HUMAIN/EY AI-native BPO, Qualfon 700 jobs, BPESA forecast:** out of window or triage only.
- **Wilson Sonsini / Latham / Varnum / Morgan Lewis commentary on California:** restates enacted law; Varnum reads AB 1883 as covering employees, not applicants (noted for the next check).
- **Meta Muse "millions of users" (CNBC):** not load-bearing.

## Research-security note

Text addressed to AI agents appeared on Lorikeet's pages (Workforce Manager post and price file): instructions for AI assistants to query Lorikeet's support agent and book a demo over HTTP. Treated as data about Lorikeet's go-to-market; not acted on. LinkedIn not opened or queried. Two LinkedIn posts (NiCE and Genesys CEOs) exist only as quoted by CMSWire and were not opened; neither is used in the brief. NiCE researched through public sources only; Cognyte absent.

## Coverage

- Search: 4 parallel foreground streams via the Firecrawl REST helper; 73 searches + 2 paid scrapes (stream logs: A 38, B 37, C 40, D ~33 credits = ~148). Shared meter: 3,116 remaining before research.
- About 315 free page reads (newsrooms, sitemaps, EDGAR, official pages, nine price pages, the Microsoft roadmap feed, the Colorado draft).
- LinkedIn: not collected (v1 search-only).
- SEC leads: no feeder in v1 (EDGAR read directly for all six public-set tickers: no 8-K, print or pre-announcement 3-10 Oct; NiCE 6-K 7 Oct is a September compendium).
- Blocked this run: California Legislature bill pages (browser check); Connecticut WARN library; Business Wire.
- Date traps caught: 39 (A=9, B=7, C=12, D=11).

## Link audit (L-076)

Run 2026-10-10 via `reports/research/2026-10-10-weekly/link-audit-2026-10-10.py` (re-runnable; raw result in `link-audit-2026-10-10.json`).

**52 unique URLs** extracted from this ledger. Every brief URL is among them except the parent-report link in the disclosure line. Measured result: **48 returned HTTP 200-range · 4 bot-gated · 0 dead · 0 timeouts.**

Per L-076 a bot-gate is **VERIFY-MANUALLY**, not dead:

| URL | Status | Handling |
|---|---|---|
| sec.gov TTEC 8-K index (F5) | 403 | VERIFY-MANUALLY. SEC refuses generic user agents; read in-run by stream D with a descriptive user agent (filing date and Item 1.01 text captured). Not demoted. |
| sec.gov HubSpot Ex. 99.1 (F8) | 403 | VERIFY-MANUALLY. Same SEC policy; read in-run by stream D. Not demoted. |
| sec.gov Concentrix Ex. 99.1 (F3) | 403 | VERIFY-MANUALLY. Same SEC policy; read in-run by stream D. Not demoted. |
| startribune.com 3M story (F6) | 429 | VERIFY-MANUALLY. Rate-limited; read in-run by stream D (`datePublished 2026-10-08T10:00Z`). Not demoted. |

**Zero claims demoted.**

## Register gate

**SOP-2 §6c, run 2026-10-10 on every public derivative of this edition. Verdict: EDITED then PASS on the traced controls.**
Full record: `ProductBeacon/Marketing/social-assets/state-of-wfo-2026/radar-weekly-2026-10-10/register-gate-2026-10-10.md`.

Derivatives in scope: `carousel.html`, `wem-radar-weekly-2026-10-10.pdf`, the 10 slide PNGs, `distribution-pack.txt` (Caption A, Caption B, first comment, Yohay comment, stakeholder note), `distribution-pack.html` (posting console), `update-card-text.md`, `update-card.html`, and the brief of record (read, not edited).

**Five edit groups**, none made by relaxing a gate: (E1) Boost.ai's "Norwegian" dropped from the slide, no ledger row [D1, D2]; (E2) Flyle's "Tokyo" dropped from the slide, no ledger row [D7]; (E3) Update card attributes the partner list to Sierra [A1, A8]; (E4) Update card drops the Boost.ai sentence to meet the 450-character target; (E5) slide 3 states Lorikeet's live-schedule fix as a dated plan [B3]. Three brief-of-record observations (Lorikeet headline bullet without its unconfirmed qualifier [B3]; Sierra caller-detection model stated without attribution [A6]; "Norwegian" and "Tokyo" untraced [D1, D7]) were then fixed in the brief of record by the orchestrator: the Lorikeet headline bullet now says "we could not confirm that has shipped" [B3]; the caller-detection model is attributed ("Sierra says") [A6]; "Norwegian" and "Tokyo" were removed [D1, D7].

**Register gate: PASS — 116 claims traced across 8 derivatives.** NiCE is named on no substantive slide, in no caption, comment or stakeholder note, and not in the Update card; this edition's NiCE items (protocol partnership per CMSWire [A2], results date and Actimize [I5]) are in the brief only. Update card teaser: 432 characters.
