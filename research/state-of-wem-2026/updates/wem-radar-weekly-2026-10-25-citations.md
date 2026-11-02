# WEM Radar 2026-10-25 — Citations ledger

Edition: **WEEKLY + PERIODIC PREDICTION CHECK** (last check 2026-10-03, 22 days earlier). Collection window 2026-10-18 (after ~06:00 UTC) → 2026-10-25 (~05:30 UTC). Prediction evidence: everything since 2026-10-03 (this week plus the 10 and 18 Oct ledgers).
One row per load-bearing claim in `radar-2026-10-25.md`. Claim typing per L-077: **Fact** · **Fact-that-was-SAID** (a named party asserted it; the assertion is the fact) · **Estimate** · **Inference** (our reading).
Raw research: `reports/research/2026-10-25-bets-check/` (streams A-D: `stream-a-wfm-quality.md`, `stream-b-assist-engagement-public.md`, `stream-c-autonomous-pricing-ma.md`, `stream-d-regulatory-demand.md`; raw search logs `raw-*-search.md`; call logs `fc-log-*.jsonl`; saved pages under `scrapes/a-d/`). Every date was read off the page itself (`datePublished`, `article:published_time`, printed dateline, EDGAR filing date, a roadmap record's `created` field, GOV.UK API `public_updated_at`, or the GitHub API), never a search snippet. Stream row references (A1, B2 ...) point to the finding numbers in each stream file.

No claim appears in the brief without a row here.

---

## A. Microsoft Contact Center Intelligence

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| A1 | Public preview announced 21 Oct: "Microsoft CCI adds purpose-built agents, quality, and analytics to existing contact centers. We've taken the agentic capabilities built into Dynamics 365 Contact Center and extended them to work with any other contact center through an open connector." | Fact (launch) · Fact-that-was-SAID (description) | Microsoft Dynamics 365 blog (Darya Mazandarany), `datePublished 2026-10-21T15:00:00Z` | https://www.microsoft.com/en-us/dynamics-365/blog/business-leader/2026/10/21/microsoft-contact-center-intelligence-transforming-customer-experience-at-agentic-speed/ |
| A2 | "Connectors make it easy to integrate Microsoft CCI with contact center vendors like Five9, Cisco WebEx Contact Center, and Avaya"; Siemens Healthineers layers it "onto the Genesys and ServiceNow platforms that we have enabled" | Fact-that-was-SAID | Microsoft blog 21 Oct | (A1) |
| A3 | Quality agent will "Evaluate both agentic and human-led interactions"; same "Multimodal Agent Score (MAS) quality bar ... across both human and AI agents"; "evaluates historical self-service conversations today ... with real-time evaluation coming soon" | Fact-that-was-SAID | Microsoft blog 21 Oct | (A1) |
| A4 | "agentic capabilities in Microsoft CCI are usage-based through Copilot Credits"; no price list published (CXM 23 Oct: "No pricing has been announced") | Fact-that-was-SAID · Fact (absence) | Microsoft blog 21 Oct; CXM roundup `datePublished 2026-10-23` | (A1) · https://cxm.world/customer-experience/customer-experience-news-roundup-contact-centre-ai/ |
| A5 | "Innovations available soon will include real-time evaluations and coaching, contact center agent assist, and more" | Fact-that-was-SAID (plan) | Microsoft blog 21 Oct | (A1) |
| A6 | "available now in global public preview, with the exception of Austria"; no reason given | Fact | Microsoft blog 21 Oct | (A1) |
| A7 | Ignite 17-20 Nov | Fact | Microsoft (stream C finding 2) | — |
| A8 | Independent analyst: overlay "targets the AI layer where CCaaS vendors are building their next wave of revenue" | Estimate (analyst view; used for context in research, not printed) | Futurum (Keith Kirkpatrick), "Publication Date: October 22, 2026" | https://futurumgroup.com/insights/microsoft-contact-center-intelligence-takes-aim-at-ccaas-ai/ |
| A9 | "Microsoft is separating the AI from the contact centre. The host vendor keeps the human seat, while Microsoft bills its AI by use." | Inference (A1, A2, A4) | — | — |

## B. New York City proposed rule

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| B1 | DCWP proposed rule published in the City Record 20 Oct; requires "easy access to a human representative" | Fact | NYC DCWP release, dateline "October 20, 2026"; rule text | https://www.nyc.gov/site/dca/news/072-26/mamdani-administration-proposes-ban-ai-customer-service-doom-loops |
| B2 | Disclosure that the consumer is talking to an automated system; rebuttable presumption of violation unless "a single-step transfer mechanism" (e.g. "Press 0") "and the estimated wait time if the consumer is placed in a queue" | Fact (proposed text, 6 RCNY 5-310 to 5-313) | Notice of hearing PDF | https://rules.cityofnewyork.us/wp-content/uploads/2026/10/DCWP-NOH-Proposed-Rules-Regarding-Automated-Customer-Service-Systems.pdf |
| B3 | Logs kept three years; annual aggregates incl. interactions "resolved without the use of a single-step transfer mechanism" and consumers with "previous covered interactions in the preceding 72 hours" | Fact (proposed text) | Notice PDF | (B2) |
| B4 | Penalties $525 / $1,050 / $3,500; applies to any company doing business in the city | Fact-that-was-SAID (Gothamist from a DCWP briefing) | Gothamist `datePublished 2026-10-20T16:04Z` | https://gothamist.com/news/nyc-proposes-crackdown-down-on-ai-customer-service-chatbots |
| B5 | Hearing 19 Nov 11:00; notice: comments "on or before November 19, 2026"; rules page: "Comment by date: December 18, 2026" (conflict) | Fact | NYC Rules page; notice PDF | https://rules.cityofnewyork.us/rule/automated-customer-service-systems/ |
| B6 | "If adopted, the reports would count a contact as resolved only with no transfer and no repeat within 72 hours. Someone would also have to staff the human queue to a stated wait." | Inference (B2, B3) | — | — |

## C. Comcast

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| C1 | CFO Jason Armstrong, Q3 call 22 Oct: "reduced customer service contact rates by roughly 20% and eliminated more than 30 million service interactions year to date versus the prior year" | Fact-that-was-SAID | Deadline `datePublished 2026-10-22T21:35Z` (Comcast transcript not opened) | https://deadline.com/2026/10/comcast-warns-q4-charge-layoffs-connectivity-1237171103/ |
| C2 | Comcast "has partnered with Cresta and Sierra"; "central to our new operating model" | Fact-that-was-SAID | Philadelphia Inquirer `datePublished 2026-10-22T12:24-04:00` | https://www.inquirer.com/business/comcast-reorganization-workforce-costs-layoffs-20261022.html |
| C3 | Job cuts planned in cable, broadband and wireless; fourth-quarter charge of more than $1 billion; no job number | Fact-that-was-SAID (Bloomberg via Los Angeles Times; also Deadline) | Los Angeles Times `datePublished 2026-10-22T21:47Z` | https://www.latimes.com/entertainment-arts/business/story/2026-10-22/comcast-job-cuts-broadband-losses-charge |
| C4 | "Executives did not directly address the potential for layoffs ... sources have told The Inquirer that workforce cuts are expected and some are already taking place" | Fact-that-was-SAID | Inquirer 22 Oct | (C2) |
| C5 | "A very large buyer now ties lower contact volume to named AI suppliers. Its measure is contacts avoided, not problems solved." | Inference (C1, C2) | — | — |

## D. Zoom

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| D1 | "Unified Context Layer, which gives human and AI agents a shared memory of the customer" | Fact-that-was-SAID | Zoom CX release `datePublished 2026-10-20T16:30:41Z` | https://news.zoom.com/zoomtopia-cx-2026/ |
| D2 | Quality Management for third-party cases: "Zoom AI can score cases and tickets, detect topics, and analyze sentiment across work involving multiple interactions, agents, and back-office teams ... (Available now.)" | Fact-that-was-SAID | Zoom CX release 20 Oct | (D1) |
| D3 | "Quality Management AI Roleplay lets agents practice voice scenarios before handling them with customers ... assess performance against criteria such as empathy and policy adherence ... (Available now.)" | Fact-that-was-SAID | Zoom CX release 20 Oct | (D1) |
| D4 | Spend-based model: "one annual spending pool covering agents, seats, applications, and AI capabilities" (Michelle Couture via CX Foundation); not in Zoom's two releases, CX recap blog or pricing page | Fact-that-was-SAID (single trade source) · Fact (absence on Zoom pages) | CX Foundation `datePublished 2026-10-20T16:59:54Z` | https://cxfoundation.com/news/zoom-unified-context-layer |
| D5 | Zoom acquired Onyx (open-source enterprise search and knowledge platform), 23 Oct; no price or terms stated | Fact | Zoom newsroom `article:published_time 2026-10-23T12:56:30Z` | https://news.zoom.com/zoom-acquires-onyx-adding-open-source-enterprise-knowledge-search-to-zoom-ai-services/ |
| D6 | "AI role-play practice now comes inside a large suite's quality product. Specialist training vendors lose one more point of difference." | Inference (D3) | — | — |

## E. Salesforce

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| E1 | UK page: Contact Centre £100; Contact Centre Plus £200 ("Included Workforce and Quality Management"); EU page €125 / €250 | Fact (read 25 Oct ~02:39 UTC) | Salesforce UK / EU pages | https://www.salesforce.com/uk/service/contact-center/ · https://www.salesforce.com/eu/service/contact-center/ |
| E2 | On 18 Oct those pages showed no local prices; "Not currently available in this region" fell from 36 to 12 occurrences; remaining 12 are AUD and JPY cells | Fact (script diff of `2026-10-18-weekly/scrapes/c/` vs `2026-10-25-bets-check/scrapes/c/`; 18 Oct ledger A5) | Saved copies | — |
| E3 | Quality Management add-on $50 / €50 / £40 per user per month (also AU$70, ¥6,000, 500 kr); overview: "Automatically review 100% of human and AI agent interactions against defined quality standards"; absent from the 18 Oct copy | Fact (pages undated) | Salesforce price and overview pages | https://www.salesforce.com/service/contact-center/pricing/ · https://www.salesforce.com/service/contact-center/ |
| E4 | "Agentforce Coworker User License ... standalone SKU with predictable per-user pricing. $50 USD/User/Month"; absent from the 18 Oct copy | Fact | Salesforce Agentforce pricing | https://www.salesforce.com/agentforce/pricing/ |
| E5 | Customer-facing "Conversations ... $ 2 USD/Per conversation" unchanged | Fact | Agentforce pricing (diff vs 18 Oct copy) | (E4) |
| E6 | No Salesforce release announcing either add-on found in the newsroom feed (newest 19-22 Oct) | Fact (absence; research note, not printed) | Salesforce newsroom | — |
| E7 | Braze: definitive agreement 20 Oct, ~$5.66B enterprise value, $47.50 cash per share; close expected in Salesforce FY2028 | Fact | Salesforce release `datePublished 2026-10-20T12:00Z`; 8-K filed 20 Oct | https://www.salesforce.com/news/press-releases/2026/10/20/salesforce-signs-definitive-agreement-to-acquire-braze/ · https://www.sec.gov/Archives/edgar/data/1108524/000119312526425881/d516983d8k.htm |
| E8 | "Salesforce now charges per user for staff tools and per use for AI that serves customers. It prices scoring of its AI agents per human user." | Inference (E1-E5) | — | — |

## F. Personal agents

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| F1 | "Version 0.2 Published October 24, 2026"; draft 0.3 "In progress" with changes tagged "Breaking" | Fact | Personal Agent Protocol changelog | https://personalagentprotocol.org/docs/changelog |
| F2 | GitHub: no releases, no tags, one repository (no reference implementation); design-partner list unchanged; Salesforce and Microsoft not listed | Fact (GitHub API read 25 Oct; script comparison of partner list) | GitHub; protocol site | https://github.com/personal-agent-protocol/personal-agent-protocol |
| F3 | Salesforce: "Personal Agents Will Drive More Contact Center Traffic Than They Offset" | Fact-that-was-SAID | Salesforce story `datePublished 2026-10-19T19:30Z` | https://www.salesforce.com/news/stories/personal-agents-to-drive-more-contact-center-traffic/ |
| F4 | Decagon: "For some request types, that's already increasing contact volume and handle time"; Decagon points to its own PACT protocol | Fact-that-was-SAID | Decagon blog `datePublished 2026-10-20T18:46Z` | https://decagon.ai/blog/a-guide-to-serving-personal-agents |
| F5 | Lorikeet-commissioned survey, ~2,000 US adults (30 Sep-8 Oct): "6.3% said an AI had contacted the company itself" | Fact-that-was-SAID (vendor-commissioned) | Lorikeet blog `datePublished 2026-10-19` | https://www.lorikeetcx.ai/blog/consumers-are-already-sending-ai-to-deal-with-companies |
| F6 | "Two vendors now say personal agents add contacts rather than remove them. That is a new input for staffing plans." | Inference (F3, F4) | — | — |

## G. Scheduling

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| G1 | Roadmap record 577184 "Manage intraday operations with AI agent": "Automates corrective actions such as adjusting schedules, rescheduling breaks, or reallocating service representatives"; status "In development"; GA "March CY2027"; public preview listed "September CY2026"; created 2026-10-20T23:00:34 | Fact (record) · Fact-that-was-SAID (description, plan) | Microsoft public roadmap feed, read 25 Oct ~02:34 UTC | https://www.microsoft.com/releasecommunications/api/v1/m365 |
| G2 | No public preview or documentation page for an intraday agent in the Dynamics 365 Contact Center docs (file list read 25 Oct) | Fact (absence) | MicrosoftDocs GitHub | https://github.com/MicrosoftDocs/dynamics-365-contact-center/tree/main/contact-center/use |
| G3 | Records 576761 and 576748 (volume-spike alerts; intraday performance report) still "In development", target "October CY2026", on 25 Oct | Fact | Roadmap feed | (G1) |
| G4 | Volume spike alerts "don't reroute conversations, change staffing, or modify the published schedule" | Fact-that-was-SAID | Microsoft Learn (`ms.date 08/19/2026`) | https://learn.microsoft.com/en-us/dynamics365/contact-center/use/workforce-management-use-volume-spike-alerts |
| G5 | Record 578073 (overnight shifts, Launched): "Improve migration readiness from Verint, Genesys, NICE, UKG, and Calabrio"; created 2026-10-23 | Fact-that-was-SAID | Roadmap feed | (G1) |
| G6 | Aspect homecare case: "3,717 automatic schedule updates from May through August 2026", "64.2% of 5,790 total schedule updates"; "Preserve analyst review for ambiguous events" | Fact-that-was-SAID (anonymous customer, vendor-published) | Aspect, JSON-LD `datePublished` "Oct 21, 2026" | https://www.aspect.com/resources/how-a-homecare-software-provider-automated-schedule-exception-handling-with-aspect |
| G7 | Aspect Canadian case: "3,412 of 6,123 recorded schedule updates were automatic, representing 55.7%"; "The workforce team continued to investigate each flagged event and apply the appropriate final reason" | Fact-that-was-SAID | Aspect, `datePublished` "Oct 21, 2026" | https://www.aspect.com/resources/how-a-canadian-financial-services-provider-improved-schedule-exception-coverage-with-aspect |
| G8 | Lorikeet comparison page `dateModified 2026-10-23T04:54` still reads "New in October 2026; intraday is next, not live at launch" | Fact | Lorikeet | https://www.lorikeetcx.ai/articles/workforce-management-software-support-teams-2026 |
| G9 | "A large vendor has now dated scheduling software that acts by itself. Every shipped tool we track still alerts, suggests or flags." | Inference (G1-G8; also Cisne and Microsoft items reported 18 Oct) | — | — |

## H. Quality and coaching

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| H1 | Unnamed insurer scores "100% of customer interactions"; "automated the equivalent of 300,000 analyst hours, representing approximately 155 full-time employees and nearly $9 million in annual value" | Fact-that-was-SAID (anonymous customer; value is Verint's estimate) | Verint release, on-page "October 22, 2026", `datePublished 2026-10-22T12:44:14` | https://www.verint.com/press-room/2026-press-releases/insurance-provider-generates-12-million-value-verint-qm-intelligence/ |
| H2 | Dave Singer: "AI giving brands more capacity to focus on coaching humans"; release silent on what happened to the analysts | Fact-that-was-SAID · Fact (absence) | Verint 22 Oct | (H1) |
| H3 | Microsoft shipped supervisor "edit and override" of evaluation results incl. "AI agent-generated" evaluations, tracked "through audit signals" (record status Launched; record dates 22-23 Oct, availability earlier) | Fact | Microsoft roadmap feed records 577802 / 578070 / 577799 / 577800 | (G1) |
| H4 | Centrical Workforce Orchestration System, 19 Oct: builds "KPIs, learning, coaching, role-play simulations, certifications, and challenges" across "people and AI agents"; "Leaders review and approve the program before it goes into effect" | Fact-that-was-SAID | Agile Brand Guide (release text) `datePublished 2026-10-19T15:50Z`; Directors Club 19 Oct | https://agilebrandguide.com/centrical-launches-workforce-orchestration-system-to-turn-business-goals-into-measurable-frontline-outcomes/ |
| H5 | "one unnamed retailer recorded an eight-point increase in customer satisfaction score within one month" | Fact-that-was-SAID | IT Brief, on-page 23 Oct | https://itbrief.news/story/centrical-launches-ai-workforce-orchestration-system |

## I. Workplace AI rules

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| I1 | Aspect: "Inferring contact center agents' emotions from their voice or facial expressions is prohibited under the EU AI Act"; advises "limiting emotion detection to the customer's side of the call" | Fact-that-was-SAID (vendor guidance; Aspect's reading of the law) | Aspect, JSON-LD `datePublished` "Oct 20, 2026", on-page "Last updated on October 20, 2026" (site build stamp 14 Oct; first publication 14-20 Oct) | https://www.aspect.com/resources/what-does-the-eu-ai-act-mean-for-workforce-management-and-quality-monitoring |
| I2 | First vendor in this radar's coverage to publicly advise customers to keep emotion detection off agents; advice, not a product change | Inference (I1; coverage since 29 Jul) | — | — |
| I3 | No contact-centre vendor found renaming, limiting, geo-fencing or switching off an emotion, sentiment or wellbeing feature (streams B and D) | Fact (negative search, scoped to vendors checked) | Streams B, D | — |
| I4 | Zoom's case scoring will "analyze sentiment" | Fact-that-was-SAID | Zoom CX release | (D2) |
| I5 | DWT: enforcement by the Labor Commissioner and public prosecutors; "injunctive relief, punitive damages, and reasonable attorneys' fees and costs, and violators face a $500 penalty per violation"; ban effective 1 Jan 2027 | Fact-that-was-SAID (one firm's reading; chaptered text not read this run) · Fact (date, carried from 3 Oct ledger A1-A7) | Davis Wright Tremaine (URL path 2026/10; day not on page) | https://www.dwt.com/blogs/employment-labor-and-benefits/2026/10/california-ai-workplace-laws-2027 |
| I6 | EU: no enforcement action, fine or interpretation under Art. 5(1)(f) or Art. 50(3); AI Act page "Last update 19 October 2026" added notice of EN 18286:2026 (quality management for high-risk AI providers) | Fact (negative check) · Fact | European Commission pages (enforcement page updated 20 Oct; standard notice "Publication 19 October 2026") | https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act · https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal |
| I7 | UK: "automatically unfair to dismiss someone in order to make a change to contractual shift patterns" (night 11pm-6am, day, weekend, weekday); availability windows out of scope; in force with fire-and-rehire protections "in March 2027" | Fact (government response, 22 Oct) | GOV.UK, API `public_updated_at 2026-10-22T10:20` | https://www.gov.uk/government/consultations/make-work-pay-fire-and-rehire-changes-to-expenses-benefits-and-shift-patterns |
| I8 | April 2027: "banning blacklists drafted using AI"; guaranteed hours and short-notice shift payment timings "will be updated following the consultation process" | Fact | GOV.UK timeline update, `public_updated_at 2026-10-22T10:49` | https://www.gov.uk/government/publications/implementing-the-plan-to-make-work-pay-and-employment-rights-act/plan-to-make-work-pay-and-employment-rights-act-timeline-update |
| I9 | UK monitoring consultation: still `closed_consultation`, no outcome (change history only "First published") | Fact | GOV.UK content API, read 25 Oct | https://www.gov.uk/api/content/government/consultations/make-work-pay-workplace-monitoring-technologies |
| I10 | Colorado: Regulatory Analysis released 21 Oct; "compliance costs ... will vary considerably" (no figures); comments through 26 Oct and continue "through the last day of the formal rulemaking hearing" if it runs past 26 Oct | Fact | Colorado AG page `article:modified_time 2026-10-21T21:52Z`; analysis dated 21 Oct | https://coag.gov/ai/ · https://coag.gov/app/uploads/2026/10/2026.10.21-Final-Regulatory-Analysis.pdf |
| I11 | Connecticut Public Act 26-73 in force 1 Oct: employers must name "the specific worksite location(s) where electronic monitoring occurs" | Fact-that-was-SAID (law firm summary; LATE CATCH, in force 1 Oct) | Epstein Becker Green, on-page "October 20, 2026" | https://www.ebglaw.com/insights/publications/reminder-changes-to-connecticuts-electronic-monitoring-statute-now-in-effect |
| I12 | Chile: bill would "prohibit subcontracting teleoperator services that operate outside national territory"; Senate Economy Committee amendment deadline 2 Nov | Fact-that-was-SAID (Outsource Accelerator citing the Senate's 14 Oct update; LATE CATCH) | Outsource Accelerator WordPress date 2026-10-20 | https://news.outsourceaccelerator.com/chile-senate-call-center-ban/ |
| I13 | "Pressure on emotion features is arriving through vendor advice and buyers' contracts, not enforcement." | Inference (I1, I3, I6; 18 Oct ledger I1-I4 law-firm advice on vendor contracts) | — | — |
| I14 | SB 951 effective date check (stream D flag): Newsweek (22 Oct) says 1 Jan 2028. Littler and Fisher Phillips both say the changes take effect 1 Jan 2027; 1 Jan 2028 is the EDD report deadline. Our 3 Oct line stands; no correction | Fact (re-read 25 Oct) | Littler; Fisher Phillips | https://www.littler.com/news-analysis/asap/california-amends-its-warn-act-again · https://www.fisherphillips.com/en/insights/insights/california-employers-will-soon-need-to-say-when-ai-causes-a-mass-layoff |

## J. Outsourcers and buyers

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| J1 | Conduent "completed a refinancing of its existing $357 million senior secured revolving credit facilities" and added "$90 million of additional commitments"; maturity "May 31, 2029"; closing 23 Oct | Fact | Conduent 8-K filed 23 Oct | https://www.sec.gov/Archives/edgar/data/1677703/000167770326000142/cndt-20261023.htm |
| J2 | Replaces the extension to 30 Oct reported 18 Oct (18 Oct ledger J3) | Fact (thread) | 18 Oct ledger | — |
| J3 | CEO Harsha V. Agadi: "premier AI-led and technology-enabled business process partner"; the filing's terms do not mention AI | Fact-that-was-SAID · Fact (absence in Item 1.01 text) | Exhibit 99.1, dateline "Oct. 23, 2026" | https://www.sec.gov/Archives/edgar/data/1677703/000167770326000142/0001677703-26-000142.txt |
| J4 | TTEC Digital GovEx: "more than 40 prebuilt conversational AI agents"; "resolve public service requests from start to finish"; no price or customer | Fact-that-was-SAID | GlobeNewswire via Yahoo Finance, dateline "AUSTIN, Texas, Oct. 20, 2026" | https://finance.yahoo.com/technology/ai/articles/ttec-digital-unveils-40-ai-213000856.html |
| J5 | ArvatoConnect CEO Debra Maxwell "aims for 70% of interactions to be handled by technology and 30% by people"; "average handling times may need to increase" | Fact-that-was-SAID (via CNBC) | CNBC `datePublished 2026-10-24T05:00Z` | https://www.cnbc.com/2026/10/24/ai-customer-service-jobs-work.html |
| J6 | Fusion CX listing 22 Oct: issue ₹289; high ₹313.15 (BSE) / ₹312.95 (NSE); last ₹289.75 / ₹289.65 | Fact | Chittorgarh (exchange data), `dateModified` 23 Oct | https://www.chittorgarh.com/ipo/fusion-cx-ipo/ |
| J7 | Consumer Cellular survey (US adults 50+, customers and prospects; sample size not stated): 43% "completely resolved", 43% "real, live person", 4% speed | Fact-that-was-SAID (buyer-commissioned) | PR Newswire, dateline "SCOTTSDALE, Ariz., Oct. 20, 2026" | https://www.prnewswire.com/news-releases/consumer-alert-the-ai-customer-service-race-could-be-costing-companies-customers-302913632.html |
| J8 | Barclays reducing headcount by 5,000; CEO "said the job cuts were the result of technology investments"; contact centres not named | Fact-that-was-SAID | Computer Weekly, "Published: 22 Oct 2026 11:45" | https://www.computerweekly.com/news/366652509/Barclays-to-cut-5000-jobs-and-employ-more-artificial-intelligence |
| J9 | Beige Book: "Five Districts reported that some firms had either reduced staffing levels (through attrition), delayed hiring, or anticipated less job creation after increasing productivity by investing in AI" (LATE CATCH, released 14 Oct) | Fact | Federal Reserve | https://www.federalreserve.gov/monetarypolicy/beigebook202610-summary.htm |
| J10 | Costa Rica: stronger colón raised payroll costs "by 35% to 40%" (La Nación via Outsource Accelerator); Servinform cutting ~10% of staff after losing most Endesa work "under the sector's usual tendering and pricing dynamics" (Forbes España via Outsource Accelerator); neither cites AI | Fact-that-was-SAID | Outsource Accelerator, WordPress dates 2026-10-20 and 2026-10-23 | https://news.outsourceaccelerator.com/costa-rica-free-zones-bpo-jobs/ · https://news.outsourceaccelerator.com/servinform-spain-layoffs-endesa/ |
| J11 | "The clearest AI effect this week is on contact volume at a large buyer. Job losses at outsourcers still have several causes." | Inference (C1-C3, J6-J10) | — | — |

## K. Pricing, other companies and results dates

| # | Claim | Type | Source | URL |
|---|---|---|---|---|
| K1 | No reversal from per-resolution to per-seat; twelve price-page files from seven vendors re-read 25 Oct ~02:32-02:39 UTC (Salesforce ×4 contact centre + Agentforce, Fin, Zendesk, Lorikeet ×2, Microsoft, Genesys, NiCE) | Fact (diff vs 18 Oct copies) | Stream C finding 7 | https://fin.ai/pricing · https://www.zendesk.com/pricing/ · https://www.lorikeetcx.ai/pricing · https://www.microsoft.com/en-us/dynamics-365/products/contact-center/pricing · https://www.genesys.com/pricing · https://www.nice.com/pricing |
| K2 | Lorikeet: "Escalations to a person and unresolved tickets are not charged"; prices unchanged (machine-readable file byte-identical; HTTP Last-Modified 23 Oct) | Fact | Lorikeet pricing | https://www.lorikeetcx.ai/pricing |
| K3 | Sierra-Stripe: "have a conversation, pay, and get their receipt all on the same call"; "When patients start a payment with Kora, Cedar's agent, 71.3% of those calls end in a successful payment" | Fact-that-was-SAID (vendor-published customer figure) | Sierra blog `datePublished 2026-10-20T16:21Z`; The Next Web 20 Oct | https://sierra.ai/blog/from-conversation-to-payment-sierra-and-stripe |
| K4 | Decagon Experiment Hub, 22 Oct: "know exactly which change moved resolution, CSAT and quality"; no buyer, deal or round on the reported sale | Fact-that-was-SAID · Fact (absence, blog index) | Decagon `datePublished 2026-10-22T15:30Z` | https://decagon.ai/blog/experiment-hub |
| K5 | Gartner Magic Quadrant for CCaaS (19 Oct 2026), per vendor releases: NiCE, Genesys, Five9 Leaders; Microsoft Visionary; Zoom Niche Player | Fact-that-was-SAID (vendor-reported positioning) | NiCE 21 Oct; Genesys 22 Oct; Five9 22 Oct; Zoom blog 23 Oct; Microsoft blog list 22 Oct | https://www.five9.com/news/news-releases/five9-named-leader-2026-gartnerr-magic-quadranttm-contact-center-service-ninth · https://www.genesys.com/company/newsroom/announcements/genesys-named-a-leader-in-the-gartner-magic-quadrant-for-contact-center-as-a-service-for-12th-consecutive-year · https://www.zoom.com/en/blog/zoom-cx-2026-gartner-magic-quadrant-for-ccaas/ |
| K6 | Peopleware: ResQ "schedule[d] 900+ advisors from client headcount targets and took on two new campaigns without adding planners" | Fact-that-was-SAID | Peopleware, dateline "London, UK, October 20th, 2026" | https://www.peopleware.com/peopleware-customer-resq-to-present-how-it-schedules-900-advisors-without-a-demand-forecast-at-ccexpo-2026-in-london |
| K7 | TruAgents "oversubscribed $3.4 million seed round led by ManchesterStory"; announcement date not stated | Fact-that-was-SAID | Dealroom `datePublished 2026-10-24T16:27Z` | https://dealroom.co/news/165597-truagents-raises-3-4m-seed-to-bring-compliant-ai-conversations-to-regula/ |
| K8 | Automation Anywhere / Boost.ai: "Completion is expected in Q4 2026, subject to regulatory approvals" | Fact-that-was-SAID | VUX `datePublished 2026-10-20T10:16:08Z` | https://vux.ai/inside-automation-anywhere-boost-ai-acquisition-plans/ |
| K9 | NiCE investor page "No current upcoming events" (read 25 Oct); Five9 no results-date release (newsroom newest 22 Oct) | Fact (absence) | NiCE investors; Five9 newsroom | https://www.nice.com/company/investors · https://www.five9.com/news/news-releases |
| K10 | TaskUs 4 Nov (01net syndication); TP 5 Nov, TTEC 5 Nov (ad-hoc-news); IBEX 5 Nov (scanx). Company pages blocked; not verified at source | Fact-that-was-SAID (secondary sources) | Stream D quiet checks | — |

## L. Prediction updates (all assessments are Inference)

Source: ProductBeacon Research, 25 Oct (our own assessments). Basis: the 3 Oct assessments plus evidence in the 10 Oct, 18 Oct and 25 Oct ledgers. The stream proposals are in the four stream files; one disagreement is recorded at L7.

| # | Prediction (tracker id) | Assessment 25 Oct (was 3 Oct) | Evidence rows |
|---|---|---|---|
| L1 | One shared human/AI engine (`one-engine-product-surface`) | Strong support (unchanged) | A3, D1, D2, H4; 18 Oct G4 (Five9 menu); 10 Oct (Amazon Connect one evaluation form) |
| L2 | Repricing and seat displacement (`repricing-real-displacement-contested`) | Supported, qualified (unchanged) | Pricing: K1, E3-E5, A4. Displacement for: C1-C3, J4, J8. Against or confounding: J6, J9, J10; 18 Oct J5 (TP 29th site) |
| L3 | Disproof test (`unified-falsification-h1-2027`) | Not triggered (unchanged) | K1, E5; clean probes 10 and 18 Oct. E4 (Coworker per user) is employee-facing and never per resolution, so it does not fire the test |
| L4 | AI changes quality teams' work (`auto-qa-reallocation`) | Strong support (unchanged) | H1, H2, A3, H3 |
| L5 | Specialists defend through depth (`independent-depth-defense`) | Mixed (unchanged) | Suite side: A1-A3, G5. Specialists: no new depth release in window (stream A quiet checks: CallMiner nothing at LISTEN West; Observe.AI, Level AI, Assembled quiet); 18 Oct H1 (CallMiner release) |
| L6 | Independent middle consolidates (`vanishing-wildcard`) | Early signs (unchanged) | No quality-specialist acquisition (stream A); K8 (conversational AI); 18 Oct FourNet/SVL (channel) |
| L7 | Autonomous intraday scheduling (`autonomous-intraday-frontier`) | Weakened (unchanged). **Stream A proposed Mixed** on G1. Orchestrator kept Weakened: G1 is a plan; its listed September preview has no public page (G2); Lorikeet's "by 9 October" self-acting mode is still "not live" (G8); shipped tools alert (G3, G4) or flag exceptions for analysts (G6, G7). Disproof condition kept separate: a dated release of intraday software that changes staffing or schedules without per-change approval. Not met. | G1-G8 |
| L8 | Verint/Calabrio integration (`two-wfm-stack-integration`) | Unchanged | Verint 22 Oct release footer lists "CALABRIO" as a separate trademark (stream A finding 5); G5 lists Verint and Calabrio separately |
| L9 | Planning combines people and AI (`blended-workforce-planning-unit`) | Strong support (unchanged) | B2 (wait estimate for the human queue), F3, F4, J5, H4 |
| L10 | Emotion-AI restrictions (`emotion-ai-wall`) | Supported (unchanged). Stream B proposed "Supported, qualified" on the product side only; stream D kept Supported on the law side. Combined: Supported, with the qualification that no feature has been withdrawn | I1-I6, I13 |
| L11 | Coaching competes on outcomes (`coaching-outcome-contest`) | Supported, qualified (unchanged) | H4, H5, D2/D3 (findings to coaching); all outcomes vendor-reported |
| L12 | Simulation protects independents (`simulation-independent-wedge`) | Weakened (unchanged) | D3; H4 (role-play bundled) |
| L13 | Assist coordinates a shared engine (`control-surface-not-engine`) | Strong support (unchanged) | A2 ("Customer Assist Agent that resolves autonomously or empowers human representatives in real time", Microsoft blog), D1 |
| L14 | Automated summaries drive adoption (`auto-summary-beachhead`) | Strong support (unchanged) | No new after-call-work figure since the 12 Sep check (streams B on 20 Sep, 26 Sep, 3 Oct, 10 Oct, 18 Oct, 25 Oct) |
| L15 | Human assist stays in seat prices (`seat-question-boundary`) | Supported, qualified (unchanged) | A4, A5 (assist pricing not stated), D4 (single trade source) |
| L16 | Outcome pricing replaces seats (`seat-reset-priced`) | Supported where published (unchanged) | K1, K2, E5; Sierra, Decagon and Parloa publish no list price |
| L17 | Who acts determines the charging model (`one-engine-gated-by-who-acts`) | Strong support (unchanged) | A4 + A2 (host seats stay), E1-E5 |
| L18 | Completion replaces deflection (`fulfillment-not-deflection`) | Supported, qualified (unchanged) | For: K3, B3, J5, J7, K4. Against: C1 (contacts eliminated); 18 Oct Tottenham 20%. Rates vendor-reported, 20%-76% |
| L19 | Tally: twelve supported (six strong), one early signs, one mixed, two weakened, one unchanged, one not triggered; no change since 3 Oct | Inference (count of L1-L18) | — |

## M. What to watch

| # | Item | Type | Source |
|---|---|---|---|
| M1 | Colorado comments and hearing 26 Oct | Fact | I10 |
| M2 | Microsoft results 28 Oct; ServiceNow results 28 Oct after close | Fact (Microsoft, already known) · Fact-that-was-SAID (ServiceNow date via Yahoo Finance / 24/7 Wall St preview, 24 Oct) | Stream B finding 8; stream C quiet checks |
| M3 | Microsoft October intraday records by 31 Oct | Fact (target "October CY2026") | G3 |
| M4 | Chile amendment deadline 2 Nov | Fact-that-was-SAID | I12 |
| M5 | TaskUs, TP, TTEC, IBEX 4-5 Nov (secondary); Parloa WAVE Summit 4-5 Nov, Brooklyn | Fact-that-was-SAID | K10; stream C watch list (Parloa blog) |
| M6 | TTEC margin step-up 16 Nov unless amended | Fact (carried, 18 Oct ledger) | — |
| M7 | Ignite 17-20 Nov | Fact | A7 |
| M8 | NYC hearing 19 Nov | Fact | B5 |
| M9 | Salesforce Casey fixes and ANZ launch, November | Fact-that-was-SAID (carried, 18 Oct A1, A6) | — |
| M10 | 1 Jan 2027: AB 1883 and AB 1609; Colorado rules | Fact (carried, 3 Oct ledger) | — |
| M11 | March 2027: Microsoft Intraday Agent GA (plan); UK shift-pattern protections | Fact-that-was-SAID · Fact | G1, I7 |
| M12 | New companies (pending triage, not added to target registry): ArvatoConnect, TruAgents, Onyx, ResQ, Consumer Cellular | — | J5, K7, D5, K6, J7 |

## Not used (recorded so they are not mistaken for misses)

- **Genesys security notice (19 Oct)**: excluded under the no-breach rule; not researched.
- **ServiceNow "50 percent of net new business is already non-seat-based"**: secondary (24/7 Wall St preview); when McDermott said it is not established. Not printed.
- **The Information report that Salesforce may charge when customers use their own AI agents**: seen only as a social post (25 Oct), paywalled. Not printed.
- **American Express ~3,500 job cuts**: headlines only, articles not opened. Not printed.
- **Walmart letting AI agents shop from November**: secondary (CXM), primary page not opened. Not printed.
- **Verint Non-Financial Misconduct Insight**: employee-communications monitoring for financial-services conduct risk; availability date not verified. Held for a later edition.
- **Talkdesk "automated intraday re-optimization"** (release note 19 Oct): no describing document found. Held; check next week.
- **Sprinklr VOC Agent Suite in Gemini Enterprise (22 Oct)**: listening/marketing, not contact-centre WEM.
- **Google Agent Assist companion agent GA (30 Sep, late catch)**: no price change; low weight.
- **Inspiro Bicol expansion, ISG Asia Pacific index, Genesys Philippine survey**: low weight or vendor survey.
- **UKG frontline AI tools, Prohuman/Protocall**: search snippets only, dates not verified.
- **Salesforce Listen Labs/Loops closes, Zoom partner programme, Microsoft Field Service Scheduling Operations Agent**: context only.
- **Australian UTS "Drawing the line" report**: research report, not a rule.

## Research-security note

No text addressed to an AI was found in any fetched page (all four streams). LinkedIn was not used. NiCE was researched through public sources only (nice.com press, pricing and investor pages, SEC EDGAR, the public protocol partner list). Cognyte was not touched.

## Link audit (L-076)

Run 2026-10-25 via `reports/research/2026-10-25-bets-check/link-audit-2026-10-25.py` (re-runnable; raw result in `link-audit-2026-10-25.json`).

**73 unique URLs** extracted from this ledger. Every brief URL is among them except the parent-report link in the disclosure line. Measured result: **69 returned HTTP 200-range · 4 bot-gated · 0 dead · 0 timeouts.**

Per L-076 a bot-gate is **VERIFY-MANUALLY**, not dead:

| URL | Status | Handling |
|---|---|---|
| computerweekly.com Barclays story (J8) | 403 | VERIFY-MANUALLY. Read in-run by stream D ("Published: 22 Oct 2026 11:45"). Not demoted. |
| sec.gov Salesforce 8-K (E7) | 403 | VERIFY-MANUALLY. SEC refuses generic user agents; read in-run by stream B with a descriptive user agent. Not demoted. |
| sec.gov Conduent 8-K and full submission (J1, J3) | 403 | VERIFY-MANUALLY. Same; read in-run by stream D. Not demoted. |

**Zero claims demoted.**

## Register gate

**SOP-2 §6c, run 2026-10-25 by an independent reviewer (not the pack builder) on every public derivative of this edition. Verdict: EDITED then PASS.**
Full record: `ProductBeacon/Marketing/social-assets/state-of-wfo-2026/radar-weekly-2026-10-25/register-gate-2026-10-25.md`.

| Derivative | Claims traced | Result |
|---|---|---|
| Carousel (`carousel.html`, 11 PNGs, `wem-radar-weekly-2026-10-25.pdf`) | 108 (+15 Sources-slide publisher names) | EDITED (E1-E12: hedge pairing, vendor voice and exact quotation, scope of absolutes), then PASS |
| Caption A | 22 | EDITED (E13-E14: vendor voice; Inference as fact and scope), then PASS |
| Caption B | 2 | PASS |
| First comment | 1 | PASS |
| Yohay comment | 2 | PASS |
| Stakeholder note | 2 | PASS |
| Update card (text and HTML), 421 characters | 6 | PASS |
| Posting console | mirrors the five blocks | PASS |

E15 moved the protected-span proposals to the corrected wording (red test on a reverted copy: 14 content failures, as intended). Nineteen brief-of-record observations were then applied by the orchestrator to `radar-2026-10-25.md`: Microsoft "in public preview" and "Microsoft says it bills them on usage credits" [A1, A4]; Zoom's shared memory attributed [D1]; the shipped-tool absence scoped "As far as we can tell ... we track ... when demand shifts" [G9, L7]; Microsoft's real-time scoring attributed and help for human agents "available soon", not "coming soon" (misquote fixed) [A3, A5]; New York's rule as a proposal with a presumption of breach [B1, B2]; Comcast heading to the finance chief's words [C1]; "did not directly address" [C4]; Zoom case scoring in Zoom's own words [D2]; "Aspect says" and "schedule updates" [G6, G7]; one-engine table row split Microsoft / Zoom [L1]; Aspect's EU reading "from their voice or facial expressions" [I1]; "no contact-centre vendor" and "Zoom says" [I3, I4]; "Centrical says" [H4]; Consumer Cellular "customers and prospects", no sample size [J7]; Federal Reserve "five of its twelve districts" [J9]; "Sierra says" [K3]; Colorado "comments stay open until it ends" [I10]. Earlier, from the pack builder's notes: the two Comcast quotes split by outlet (Deadline, Inquirer) [C1, C2] and the price-page method wording moved out of reader copy.

NiCE: 0 on slides 2-10, captions, comments, stakeholder note, card and console; cover compact line and closing full Integrity Wall only (disclose-once, DR-2026-228). The Microsoft migration quote is paraphrased on the slide ("among"). No em dashes; only `[first name]` and `[LINKEDIN POST URL]` placeholders.

**Register gate: PASS — 143 claims traced across 8 derivatives.**
