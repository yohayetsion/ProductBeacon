# WEM Radar 2026-11-02: Citations ledger

Edition: **WEEKLY** (no periodic prediction check; last check 2026-10-25, next due about 2026-11-14/15). Collection window 2026-10-25 (after ~04:00 UTC) to 2026-11-02 (~06:45 UTC).
One row per load-bearing claim in `radar-2026-11-02.md`. Claim typing per L-077: **Fact** · **Fact-that-was-SAID** (a named party asserted it; the assertion is the fact) · **Estimate** · **Inference** (our reading).
Raw research: `reports/research/2026-11-02-weekly/` (streams A-D: `stream-a-wfm-quality.md`, `stream-b-assist-engagement-public.md`, `stream-c-autonomous-pricing-ma.md`, `stream-d-regulatory-demand.md`; raw search logs `raw-*-search*.md`; call logs `fc-log-*.jsonl`; saved pages under `scrapes/a-d/`). Every date was read off the page itself (`datePublished`, `article:published_time`, printed dateline, EDGAR filing date, PDF metadata, roadmap record fields, Help Center API `edited_at`, GOV.UK API `public_updated_at`), never a search snippet. Stream references (A1, B2 ...) point to finding numbers in each stream file. The orchestrator re-read the Microsoft credit tables (page images), the Microsoft call transcript and release, Sierra, Fin, NYC Rules and the Inquirer pages from the saved copies before writing.

No claim appears in the brief without a row here.

---

## A. Microsoft Contact Center Intelligence credit estimates (streams B1, C3)

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| A1 | Copilot Credits Guide "November 2026" adds a Contact Center Intelligence (CCI) section, "(Public Preview)"; figures are "rough planning estimates" | Fact (document) · Fact-that-was-SAID (estimates) | Microsoft, PDF CreationDate 2026-10-29 10:46 -07:00; HTTP Last-Modified 29 Oct 22:44 GMT; cover "November 2026" | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/bade/documents/products-and-services/en-us/ai/CopilotCreditsGuide.pdf |
| A2 | CCI is the overlay Microsoft sells on other vendors' contact centres ("supports both Microsoft and third-party contact center systems") | Fact-that-was-SAID | Microsoft guide (A1); launch reported 21 Oct (earlier evidence, reported 25 Oct) | (A1) |
| A3 | Customer Assist Agent "supports customer interactions by combining autonomous self-service with real-time assistance to service representatives ... resolves issues, assists representatives during live interactions" | Fact-that-was-SAID | Microsoft guide p. 19 | (A1) |
| A4 | Customer Assist Agent estimates: Low (short digital-chat query, at most one lookup) 2-5; Medium (voice interaction with lookups and one update; transfer context if escalated) 10-15; Heavy (branching voice flow, then "hand off with customer context") 20-25 credits | Fact-that-was-SAID (estimates; read from the table image) | Microsoft guide p. 19 (image `scrapes/c/cci-p19-1-Image187.png`) | (A1) |
| A5 | Quality Assurance Agent: evaluate a closed conversation once 5-10 credits; real-time evaluation 5-10 per turn; "Real-time coaching every turn, with live in-conversation nudges" 10-20 per turn | Fact-that-was-SAID (estimates; table image) | Microsoft guide p. 20 (image `scrapes/c/cci-p20-2-Image191.png`) | (A1) |
| A6 | Pay-as-you-go "Pricing: $0.01/Copilot Credit" | Fact | Microsoft guide | (A1) |
| A7 | Arithmetic: medium voice call ~$0.10-0.15 at list; coaching $0.10-0.20 per turn | Inference (our arithmetic on A4-A6; list price, before pre-purchase discounts) | n/a | n/a |
| A8 | 21 Oct: "Innovations available soon will include real-time evaluations and coaching, contact center agent assist, and more" | Fact-that-was-SAID (earlier evidence, reported 25 Oct) | Microsoft Dynamics 365 blog, `datePublished 2026-10-21T15:00:00Z` | https://www.microsoft.com/en-us/dynamics-365/blog/business-leader/2026/10/21/microsoft-contact-center-intelligence-transforming-customer-experience-at-agentic-speed/ |
| A9 | "The guide prices them before they ship" | Inference (A5, A8: real-time coaching listed as billable and estimated; announced as "available soon") | n/a | n/a |
| A10 | "Buyers now get a cost per conversation for Microsoft's AI running beside another vendor's per-seat contact centre. On a long call, live coaching could cost more than the AI agent itself." | Inference (A2, A4, A5) | n/a | n/a |

## B. Microsoft fiscal 2027 first-quarter results (stream B2)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| B1 | Nadella: "Our business model is expanding from per-seat subscriptions to include consumption" | Fact-that-was-SAID | Microsoft investor call transcript, "Wednesday October 28, 2026" | https://www.microsoft.com/en-us/investor/events/fy-2027/earnings-fy-2027-q1 |
| B2 | "The number of Copilot customers actively consuming credits through usage-based billing grew over 75 percent over the quarter" | Fact-that-was-SAID | Same transcript | (B1) |
| B3 | New "Industry solutions cloud" metric "combines revenue from Dynamics 365 together with revenue from LinkedIn Talent Solutions, LinkedIn Sales Solutions, and Healthcare and Life Sciences cloud"; it grew 10% | Fact | Microsoft 10-Q (EDGAR filed 2026-10-28); release Exhibit 99.1 | https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm · https://www.sec.gov/Archives/edgar/data/789019/000119312526436122/msft-ex99_1.htm |
| B4 | Hood: "Industry solutions cloud revenue increased 10% with growth in Dynamics 365 and LinkedIn Talent Solutions, though bookings trends continued to moderate"; guide "mid to high-single digits" | Fact-that-was-SAID | Transcript (B1) | (B1) |
| B5 | July: "Dynamics 365 revenue increased 13% and 12% in constant currency" | Fact-that-was-SAID (earlier quarter) | Microsoft FY26 Q4 call transcript, 29 Jul 2026 | https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4 |
| B6 | Transcript contains no mention of "contact center", "customer service", "Contact Center Intelligence" or "call center" | Fact (count of the saved transcript text) | Stream B count of `scrapes/b/msft-ir-event.html` | (B1) |
| B7 | "Investors can no longer see whether Microsoft's contact-centre push moves Dynamics 365 growth. Its roadmap and price guides are now the main public evidence." | Inference (B3, B6) | n/a | n/a |

## C. Sierra (streams C1, C2)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| C1 | "This week, we hit $400M+ in ARR, adding over $150M+ in ARR in Q3 alone." | Fact-that-was-SAID (unaudited, Sierra's definition) | Sierra blog, `datePublished 2026-10-30T12:50:00Z` | https://sierra.ai/blog/our-customers-ambition-is-accelerating-our-growth |
| C2 | "only five months to double from $200M to $400M"; "almost 50% of the Fortune 50" | Fact-that-was-SAID | Sierra blog 30 Oct | (C1) |
| C3 | "You pay for outcomes, not tokens used — a loan refinanced, an insurance claim paid, a sale closed, a customer retained." | Fact-that-was-SAID | Sierra blog 30 Oct | (C1) |
| C4 | Poppy developed "with over 50 enterprises including Meta, Instinct, Rocket, Shopify, Stripe, and Walmart"; 35 design partners on 9 Oct (earlier evidence, reported 6-9 Oct); led by Sierra and Meta | Fact-that-was-SAID | Sierra blog 30 Oct | (C1) |
| C5 | Personal Agent Protocol: no tag and no release (GitHub API, read 2 Nov); draft 0.3 "In progress" | Fact | GitHub API; protocol changelog | https://personalagentprotocol.org/docs/changelog |
| C6 | Compliance Console for outbound agents: disclosures per channel, contact windows by local time, frequency limits, opt-outs | Fact-that-was-SAID | Sierra blog, `datePublished 2026-10-28T19:44:03Z` | https://sierra.ai/blog/introducing-compliance-console |
| C7 | On Google Cloud Marketplace; "Qualifying Marketplace purchases count toward your Google Cloud commitment" | Fact-that-was-SAID | Sierra blog, `datePublished 2026-10-26T16:38:10Z` | https://sierra.ai/blog/sierra-is-on-google-cloud-marketplace |
| C8 | "Sierra's examples are moving from answering service contacts to outbound sales and collections. Its revenue figures remain its own." | Inference (C3, C6) | n/a | n/a |

## D. Fin price page (stream C4)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| D1 | "$0.99 per outcome" unchanged; "Fin Voice is available via sales at $1.99 per voice outcome" present 2 Nov, absent from the 25 Oct copy | Fact (page diff; page undated) | fin.ai/pricing, read 2 Nov 05:19 and 05:33 UTC vs saved 25 Oct copy | https://fin.ai/pricing |
| D2 | "If the conversation is later reopened, the outcome is refunded." | Fact (price-page term) | fin.ai/pricing 2 Nov | (D1) |
| D3 | "If Fin can't answer or fails to perform an action, or if at any point the customer asks to speak to a human, you pay nothing." | Fact (price-page term) | fin.ai/pricing 2 Nov | (D1) |
| D4 | Copilot "$29 per agent/month billed annually, or $35 per agent/month billed monthly"; 25 Oct copy "$35 per user per month" | Fact (page diff) | fin.ai/pricing | (D1) |
| D5 | "Qualifications are $9.99 each" removed from fin.ai/pricing; intercom.com/pricing still shows "$9.99 per qualification" | Fact | fin.ai/pricing; intercom.com/pricing (first read this cycle) | https://www.intercom.com/pricing |
| D6 | Voice price may predate the window on intercom.com (secondary explainer); hence the brief says the fin.ai page "added" it, not that the price is new | Fact-that-was-SAID (secondary; used to scope wording, not printed) | Enjo.ai pricing explainer (search listing) | https://www.enjo.ai/post/intercom-pricing |
| D7 | "The main per-outcome price list now favours the buyer on refunds and human requests. That answers a common objection that outcome prices pay for silence." | Inference (D2, D3) | n/a | n/a |

## E. Comcast layoff notices (stream D2)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| E1 | "Comcast is laying off 634 employees at its Philadelphia headquarters ... The layoffs are to begin taking effect Dec. 31." | Fact-that-was-SAID (Inquirer, citing the Pennsylvania notice) | Philadelphia Inquirer, `datePublished 2026-10-30T11:24-04:00` | https://www.inquirer.com/business/comcast/comcast-layoffs-warn-notice-philadelphia-ai-jobs-20261030.html |
| E2 | Notices for 119 positions in New Jersey, 159 in Washington and 82 in California | Fact-that-was-SAID (Inquirer) | Inquirer 30 Oct | (E1) |
| E3 | Total 994 roles | Inference (our sum of E1 + E2; the brief says "by our sum") | n/a | n/a |
| E4 | "planning to hire for more than 1,100 new positions as part of the restructuring, including more than 500 in Philadelphia, according to the layoff notice" | Fact-that-was-SAID (Inquirer) | Inquirer 30 Oct | (E1) |
| E5 | Washington: "Construction jobs are the largest group"; roles include "fulfillment and customer experience supervisors" | Fact-that-was-SAID (MyNorthwest, citing the Washington notice filed 29 Oct) | MyNorthwest, `datePublished 2026-10-29T13:42-07:00` | https://mynorthwest.com/local/comcast-layoff-washington/4291836 |
| E6 | Statement: "Comcast is fundamentally redesigning our organization to build a more agile company and better serve our customers"; as quoted, no AI mention | Fact-that-was-SAID | MyNorthwest 29 Oct; PhillyVoice `datePublished 2026-10-30T17:11-04:00` | (E5) · https://www.phillyvoice.com/comcast-layoffs-philadelphia-restructuring/ |
| E7 | 22 Oct: CFO tied contact-rate cut to Cresta and Sierra (earlier evidence, reported 25 Oct) | Fact-that-was-SAID | Deadline / Inquirer 22 Oct | https://deadline.com/2026/10/comcast-warns-q4-charge-layoffs-connectivity-1237171103/ |
| E8 | "The first noticed cuts fall mostly on other functions. State notices cover only larger cuts, so this is a minimum." | Inference (E1-E5; WARN thresholds) | n/a | n/a |

## F. New York City rule hearing (stream D1)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| F1 | Rules page: hearing "Friday Dec 18 - 11:00am EST"; "Comment by date: December 18, 2026"; 25 Oct saved copy read "Thursday Nov 19 - 11:00am EDT" | Fact (page diff; change date not shown) | NYC Rules, read 2 Nov vs `2026-10-25-bets-check/scrapes/d/nycrules-acss.html` | https://rules.cityofnewyork.us/rule/automated-customer-service-systems/ |
| F2 | Notice PDF still says the hearing "will take place at 11:00 AM on November 19, 2026"; Last-Modified 20 Oct 2026 | Fact | NYC notice PDF | https://rules.cityofnewyork.us/wp-content/uploads/2026/10/DCWP-NOH-Proposed-Rules-Regarding-Automated-Customer-Service-Systems.pdf |
| F3 | JD Supra post: "initially scheduled for November 19th, but was recently pushed back by a month to mid-December"; Wiley: "The deadline to file comments on this proposal is December 18, 2026" | Fact-that-was-SAID | JD Supra (about 30 Oct, from listing); Wiley alert (in window) | https://www.jdsupra.com/legalnews/new-york-city-proposes-rule-to-govern-6211743/ · https://www.wiley.law/alert-New-York-City-Broadens-Its-Consumer-Protection-and-Antitrust-Enforcement-Agenda |
| F4 | "The rule cannot be adopted before the hearing, so the earliest adoption moves back by a month." | Inference (F1) | n/a | n/a |

## G. Scheduling (streams A1, A2, A5, A7)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| G1 | 29 Oct rollout: "Intraday Reschedule Suggestion - Break Adjustments: Resource planners now receive AI-driven recommendations to adjust agent breaks based on live intraday queue conditions" | Fact-that-was-SAID | Talkdesk WFM release notes, entry "October 29, 2026"; Help Center API edited_at 2026-10-30T18:23 | https://support.talkdesk.com/hc/en-us/articles/10465941906203-Release-Notes-Talkdesk-Workforce-Management |
| G2 | "Accept or reject individual recommendations, or Bulk Accept all recommendations for a team at once ... Accept All Teams"; "available in Preview for select customers only" | Fact-that-was-SAID | Talkdesk help articles (edited 30 Oct and 19 Oct) | https://support.talkdesk.com/hc/en-us/articles/360044402991 · https://support.talkdesk.com/hc/en-us/articles/360044402531 |
| G3 | Assembled advert: AI agent that "recommends or takes action"; "We believe AI agents can assist with, and eventually autonomously make, many of these decisions"; "a 0→1 product area" | Fact-that-was-SAID | Assembled job advert, JSON datePosted 2026-10-27 | https://jobs.ashbyhq.com/assembledhq/25d50672-8e19-4c6d-b406-4222dea68ff2 |
| G4 | Microsoft records 576761 and 576748 (October CY2026, alert-only) still "In development" on 2 Nov; 577184 Intraday Agent still "March CY2027" | Fact | Microsoft public roadmap feed, read 2 Nov | https://www.microsoft.com/releasecommunications/api/v1/m365 |
| G5 | Lorikeet comparison page still "intraday is next, not live at launch"; Aspect real-time "Automatic Schedule Updates in Real time (Alpha)" still "Exploring" | Fact (re-read 2 Nov; unchanged) | Lorikeet; Aspect roadmap board | https://www.lorikeetcx.ai/articles/workforce-management-software-support-teams-2026 |
| G6 | Shift bidding: Talkdesk preview (22 Oct), Assembled "Shift bids" (29 Oct), Webex "Multi-Week Shift Bidding" (30 Oct); Assembled order "based on seniority, performance, or another company policy" | Fact-that-was-SAID | Talkdesk release notes; Assembled blog "October 29, 2026"; Webex "What's new", "October 30, 2026" | https://www.assembled.com/blog/shift-bids · https://help.webex.com/en-us/article/o6f77s/What's-new-for-supervisors-in-Webex-Contact-Center |
| G7 | "The shipped frontier is software that drafts schedule changes for a planner to approve in bulk. As far as we can tell, no tracked tool yet acts by itself." | Inference (G1-G5) | n/a | n/a |

## H. Channels and partners (streams C5, C6, B5)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| H1 | Parloa platform "is now available as an SAP Solution Extension under the name 'SAP Conversational Agent Management by Parloa'" | Fact | Parloa release, dateline "October 26, 2026" | https://www.parloa.com/parloa-in-the-press/SAP-conversational-agent-management-by-parloa/ |
| H2 | McKinsey and Parloa alliance | Fact | PR Newswire, `datePublished 2026-10-28T11:57Z` | https://www.prnewswire.com/news-releases/mckinsey-and-parloa-announce-alliance-for-customer-facing-ai-technology-302921401.html |
| H3 | Decagon Partner Community; "available on AWS Marketplace, Google Cloud Marketplace, Databricks Marketplace, and OpenAI Marketplace" where customers "can apply existing commitments" | Fact-that-was-SAID | Decagon blog, `datePublished 2026-10-30T15:30Z` | https://decagon.ai/blog/decagon-partner-community |
| H4 | "More than 80% of traffic on Decagon runs through models built in-house"; no buyer, deal or denial update on the reported sale | Fact-that-was-SAID · Fact (absence, two searches + blog index) | Decagon blog, `datePublished 2026-10-29T20:27Z` | https://decagon.ai/blog/a-better-payment-experience-from-reminder-to-resolution |
| H5 | Cresta "end-to-end self-service for developers building AI agents in-house or for their clients"; Atento ("as we build an AI agent workforce for our clients") and TELUS Digital quoted | Fact-that-was-SAID | Cresta press, "October 29, 2026" | https://cresta.com/press/cresta-opens-its-ai-agent-platform-with-end-to-end-self-service-for-developers |
| H6 | "Large buyers can now pay for these agents from budgets they already hold with SAP and the cloud providers. Outsourcers are building on specialist platforms rather than only reselling suites." | Inference (H1, H3, H5, C7) | n/a | n/a |

## I. AI agents planned and scored like staff (streams A3, A5, A7, B6, C7, C8)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| I1 | RingCX: "Forecast staffing needs across AI and human agent capacity together"; "Score every AI agent interaction against the same rubric used for human agents"; showcased at ICMI 28-29 Oct, no GA date or price | Fact-that-was-SAID · Fact (absence) | RingCentral release (Business Wire via Yahoo), dateline "October 28, 2026" | https://finance.yahoo.com/technology/ai/articles/ringcentral-orchestrates-ai-human-agents-120000879.html |
| I2 | Webex "Analyzer introduced AI Agent reporting" (containment, escalation, error, abandonment, response time) | Fact-that-was-SAID | Webex "What's new", "October 26, 2026" | https://help.webex.com/en-us/article/o6f77s/What's-new-for-supervisors-in-Webex-Contact-Center |
| I3 | Roadmap record 575290 (created 28 Oct, November CY2026): "Detect hallucinations, failed verifications, policy violations, and escalation drivers" | Fact | Microsoft roadmap feed, read 2 Nov | https://www.microsoft.com/releasecommunications/api/v1/m365 |
| I4 | Agent Fabric: Agent Evals, "Agent Kill Switch", Model Wallet "hard limits that stop requests before costs exceed budget" | Fact-that-was-SAID | Salesforce news, `datePublished 2026-10-27T13:00Z` | https://www.salesforce.com/news/stories/agent-fabric-catch-failures-control-ai-costs/ |
| I5 | Trademark Global: "42% of interactions handled by the agent are completed without employee assistance"; Agent Copilot on handoff | Fact-that-was-SAID (denominator: interactions the agent handles) | Genesys release, dateline "Oct. 29, 2026" | https://www.genesys.com/company/newsroom/announcements/trademark-global-connects-customer-journeys-across-brands-and-retailers-with-genesys-cloud-agentic-virtual-agent |

## J. Workplace AI rules (stream D3, D9, re-checks)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| J1 | Hearing 26 Oct; "the Office will consider all written comments received on or before October 26, 2026 at 11:59 P.M. MST"; docket "Adopted rule" field empty | Fact | coag.gov `article:modified_time 2026-10-27T21:46:10Z`; Colorado SoS docket 2026-00360 read 2 Nov | https://coag.gov/ai/ · https://www.coloradosos.gov/CCR/eDocketDetails.do?trackingNum=2026-00360 |
| J2 | US Chamber letter (26 Oct) seeks changes (Rule 6.1(A) "overbroad trigger"); industry headlines on edits and delay; EPIC, CFA and Fairplay urged stronger rules | Fact-that-was-SAID | US Chamber PDF; Privacy Daily / MLex headlines (not opened) | https://www.uschamber.com/assets/documents/US-Chamber-10.26.26-Comments-Colorado-ADMT-and-Chatbot-Act.pdf |
| J3 | Colorado rules aimed at 1 Jan 2027 | Fact-that-was-SAID (MLex headline "ahead of January deadline"; earlier evidence) | Stream D3 | n/a |
| J4 | EU: no enforcement found on Art. 5(1)(f); AI Act page "Last update 19 October 2026", enforcement page 20 Oct | Fact (absence) | European Commission pages read 2 Nov | https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act |
| J5 | California: more law-firm guidance (Nixon Peabody, Hunton, Daily Journal, Dickinson Wright); no vendor product change found | Fact (absence of vendor change) | Stream D re-checks | n/a |
| J6 | UK monitoring consultation: `public_updated_at` still 8 Jul 2026; no government response | Fact | GOV.UK content API, read 2 Nov | https://www.gov.uk/government/consultations/make-work-pay-workplace-monitoring-technologies |
| J7 | Chile Boletín 17.381-03: newest step 6 May 2026, no indicaciones listed; CNC submission: "Puede haber contratación local, pero también automatización o menor atención humana" | Fact · Fact-that-was-SAID | Senate tracking service, read 2 Nov; CNC PDF created 19 Oct (LATE CATCH) | https://tramitacion.senado.cl/wspublico/tramitacion.php?boletin=17381 |

## K. Outsourcers and buyers (streams D4-D8)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| K1 | Concentrix Live Voice Translation; "60+ languages" | Fact-that-was-SAID | Concentrix release, `datePublished 2026-10-27T17:55Z` | https://www.concentrix.com/about/press-release/concentrix-breaks-the-language-barrier-with-live-voice-translation/ |
| K2 | "results are delivering 97%+ productivity levels, well above enterprise benchmarks"; no baseline | Fact-that-was-SAID | Concentrix release | (K1) |
| K3 | Capgemini Q3 revenue €6,073M, +12.6% reported, WNS and Cloud4C contributing; "double-digit growth on a like-for-like basis in Intelligent Business Operations"; headcount 417,500, "down 5,900 compared to the end of 2025"; "Clients are transforming their business operations with agentic AI" | Fact · Fact-that-was-SAID | Capgemini release, dateline "Paris, October 30, 2026" | https://www.capgemini.com/news/press-releases/q3-2026-momentum-drives-upgrade-in-capgeminis-2026-outlook/ |
| K4 | Virgin Media O2 may cut up to 4,000 of 16,000 UK jobs; "majority of affected positions are expected to be non-customer-facing"; results "on Tuesday" (3 Nov) | Fact-that-was-SAID (unconfirmed; Share Talk summarising Sky News and others) | Share Talk, `datePublished 2026-11-01T11:37Z` | https://www.share-talk.com/virgin-media-o2-prepares-to-cut-4000-jobs-as-22bn-debt-pile-drives-major-restructuring/ |
| K5 | NatWest ~1,000 jobs cut in three months, 1,400 in 2026; CEO links to AI; Cora "has handled 52,000 credit card-related customer issues" | Fact-that-was-SAID | Share Talk, `datePublished 2026-10-30T11:11Z` | https://www.share-talk.com/natwest-cuts-1000-jobs-in-three-months-as-ai-transformation-accelerates/ |
| K6 | Pakistan call centre and BPO receipts "$101.315 million ... up 23.6 percent" in Q1 FY2026-27 (State Bank of Pakistan data) | Fact-that-was-SAID | ProPakistani, `datePublished 2026-10-26T12:05Z` | https://propakistani.pk/2026/10/26/overseas-clients-pay-big-money-to-pakistan-call-centres-in-3-months/ |

## L. Pricing (stream C9)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| L1 | No tracked vendor moved from per-resolution/per-outcome back to per-seat; Salesforce (5 pages), Zendesk, Lorikeet, Microsoft and NiCE pages unchanged | Fact (page diffs vs 25 Oct copies, read 2 Nov) | Stream C9 (12 files, 7 vendors) | https://www.salesforce.com/agentforce/pricing/ · https://www.zendesk.com/pricing/ · https://www.lorikeetcx.ai/pricing · https://www.microsoft.com/en-us/dynamics-365/products/contact-center/pricing · https://www.nice.com/pricing |
| L2 | Genesys heading "AI tokens" renamed "Experience Units"; seat prices $75-240 unchanged; page Last Modified 10/30/2026 | Fact | genesys.com/pricing, read 2 Nov | https://www.genesys.com/pricing |
| L3 | "By our count, vendors now price AI work in at least five units: outcomes, conversations, credits, committed minutes and tokens." | Inference (D1, L1, A6; Five9 committed minutes, earlier evidence reported 6 Aug and 11 Sep; Genesys tokens L2) | n/a | n/a |

## M. Other companies and results dates (streams B3, B4, B7, B8, C10, C11)

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| M1 | Uniphore CEO: revenue "about 160% in 12 months, nearing $2 billion in total bookings" | Fact-that-was-SAID (page description; bookings undefined) | CNBC video page, `datePublished 2026-10-28T11:42Z` | https://www.cnbc.com/video/2026/10/27/umesh-sachdev-uniphore-ceo-a-fortt-knox-update.html |
| M2 | Sprinklr survey of 807 US practitioners: 92% met or exceeded expectations; "Only 27% said they could quantify a result precisely" | Fact-that-was-SAID (vendor-commissioned) | Sprinklr release, "October 28, 2026" | https://www.sprinklr.com/newsroom/sprinklr-research-92-of-organizations-claim-ai-delivered-improved-customer-experience-only-27-can-prove-it/ |
| M3 | NiCE Q3 results "on Wednesday, November 4, 2026, before the opening" | Fact | Business Wire via Yahoo, `datePublished 2026-10-28T12:00Z` | https://finance.yahoo.com/markets/stocks/articles/nice-provides-webcast-dial-details-120000284.html |
| M4 | NiCE AGM notice: "Mr. Gabi Seligsohn, who is nominated for election to the Board for the first time"; AGM 3 Dec | Fact | NiCE 6-K, EDGAR filed 2026-10-29 | https://www.sec.gov/Archives/edgar/data/1003935/000117891326004911/exhibit_99-1.htm |
| M5 | Ciklum "strategic technology partnership with NiCE" for EMEA | Fact-that-was-SAID | PR Newswire, `datePublished 2026-10-27T14:02Z` | https://www.prnewswire.com/sv/pressmeddelanden/ciklum-and-nice-partner-to-bring-agentic-ai-to-enterprise-customer-experiences-302919432.html |
| M6 | Five9 Q3 "Thursday, November 5, 2026"; Zoom Q3 FY27 "Monday, November 23, 2026, after the market closes"; Sprinklr, Salesforce no date | Fact | Yahoo copies, `datePublished 2026-10-26T20:05Z` and `2026-10-29T20:05Z`; EDGAR/newsrooms | https://finance.yahoo.com/markets/stocks/articles/five9-report-third-quarter-2026-200500035.html · https://finance.yahoo.com/markets/stocks/articles/zoom-release-financial-results-third-200500192.html |
| M7 | Omnichat $10M Series A led by Openspace Capital | Fact-that-was-SAID | The Top Voices, `datePublished 2026-10-27T14:00Z` | https://thetopvoices.com/news/omnichat-raises-10m-series-a-ai-agent-platform |

## N. Prediction evidence

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| N1 | Microsoft meters live coaching (A5) and an agent that also assists representatives (A3, A4) by use; Zendesk usage-priced translation (earlier evidence, reported 10 Sep) was the first exception; together they are exceptions to "human assist stays in seat prices" | Inference | n/a | n/a |

## O. What to watch

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| O1 | Virgin Media O2 results 3 Nov | Fact-that-was-SAID | Share Talk (K4) | n/a |
| O2 | TaskUs 4 Nov; TTEC, Conduent, Genpact 5 Nov | Fact-that-was-SAID (secondary: MarketBeat, Business Wire headline, Moomoo) | Stream D quiet checks | n/a |
| O3 | Parloa WAVE Summit US 4-5 Nov | Fact-that-was-SAID | Parloa blog | n/a |
| O4 | TTEC margin step-up 16 Nov unless amended | Fact (earlier evidence, reported 18 Oct) | n/a | n/a |
| O5 | Microsoft Ignite 17-20 Nov | Fact (earlier evidence) | n/a | n/a |
| O6 | Salesforce ANZ launch November | Fact-that-was-SAID (earlier evidence) | n/a | n/a |
| O7 | NiCE AGM 3 Dec (M4); NYC 18 Dec (F1); California laws and Colorado target 1 Jan 2027 (J3) | Fact | as cited | n/a |
| O8 | New companies: RingCentral (I1), Omnichat (M7), Ciklum (M5), Reindeer AI (CX Network roundup, 30 Oct; "Self Evolve" platform) | Fact-that-was-SAID | Streams A, B, C | n/a |

## Not used (recorded so they are not mistaken for misses)

- SaaSRise headline "Sierra Hits $400M ARR As ServiceNow Shares Crash 27%": the ServiceNow share move was not verified against a primary source; ServiceNow is not tracked. Not printed.
- Marriott customer-relations cuts (One Mile at a Time, 29 Oct): single report, company refused scale, cause appears to be offshoring, unconfirmed. Kept in research only.
- EXL and transcosmos results: secondary summaries only.
- Salesforce agreement to acquire Rune Technologies (29 Oct): defence logistics, not WEM.
- Verint Everest Group WFM "Leader" (LATE CATCH, 22 Oct): analyst badge with no product or customer move.
- Cisne validated Avaya Infinity integration (27 Oct; NEW BEAT on 1 Oct item) and Assembled–Nextiva integration (27 Oct): small channel steps; kept in research.
- Webex custom metrics in performance management: product detail, not material.
- Coldi (raising, not closed); Call Coach IQ, Scala.ai (snippets only).
- Microsoft record 576605 (real-time analytics, supervisor acts): no change to the scheduling picture.

## Research-security note

- Lorikeet's release-notes page carries a block of instructions addressed to AI assistants (stream A). Ignored as data. fin.ai/ai-instructions surfaced in search (stream C); not opened.
- No LinkedIn query or visit for any company; NiCE researched through public sources only (nice.com, SEC EDGAR, Business Wire via Yahoo, PR Newswire). Cognyte not touched.

## Link audit (L-076)

Run 2 Nov 2026 (`research/2026-11-02-weekly/link-audit-2026-11-02.py`, JSON beside it): 62 unique URLs. 50 returned 200-range. 10 bot-gated (403): MyNorthwest, NYC Rules, three Talkdesk Help Center pages, three SEC EDGAR documents, two Share Talk pages. All ten were read in-run and saved under `scrapes/` (Talkdesk through the Help Center API). VERIFY-MANUALLY, not dead. Colorado Secretary of State docket returned 500 to the audit (session-based page); read in-run and saved (`scrapes/d/co-edocket.html`). One true 404, the GOV.UK monitoring consultation, was a wrong slug in this ledger and is corrected above (`make-work-pay-workplace-monitoring-technologies`, `public_updated_at` 2026-07-08, from the saved API copy). No claim demoted. Every brief URL is in the ledger except the parent-report link in the disclosure line.

## Register gate

**SOP-2 §6c, run 2026-11-02 by an independent reviewer (not the pack builder) on every public derivative of this edition. Verdict: EDITED then PASS.**
Full record: `ProductBeacon/Marketing/social-assets/state-of-wfo-2026/radar-weekly-2026-11-02/register-gate-2026-11-02.md`.

| Derivative | Claims traced | Result |
|---|---|---|
| Carousel (`carousel.html`, 11 PNGs, `wem-radar-weekly-2026-11-02.pdf`) | 90 (+16 Sources-slide publisher names) | EDITED (E1-E3: scope of absolutes on slides 6 and 7 [E5, G7]; hedge pairing on slide 8 [I1]), then PASS |
| Caption A | 16 | EDITED (E4: Talkdesk preview qualifier restored and its mechanism attributed [G1, G2]; scheduling absence scoped [G7]), then PASS |
| Caption B | 2 | PASS |
| First comment | 1 | PASS |
| Yohay comment | 2 | PASS |
| Stakeholder note | 2 | PASS |
| Update card (text and HTML), 414 characters | 6 | PASS |
| Posting console | mirrors the five blocks | PASS (rebuilt) |

E5 moved protected-span proposal span-47 to the corrected wording. The same three corrections were applied to the brief of record (lines 60, 81, 93-94: "only customer-service roles", "acts by itself when demand shifts", "RingCentral showed both at a trade show ... with no ship date or price"); the brief HTML and PDF were rebuilt. The scheduling scope follows the 18 and 25 October gates: Aspect's rule-based automatic schedule updates act by themselves on exception records.

NiCE: 0 on slides 2-10, captions, comments, stakeholder note, card and console; cover compact line and closing full Integrity Wall only (disclose-once, DR-2026-228). No em dashes; only `[first name]` and `[LINKEDIN POST URL]` placeholders.

**Register gate: PASS — 119 claims traced across 8 derivatives.**
