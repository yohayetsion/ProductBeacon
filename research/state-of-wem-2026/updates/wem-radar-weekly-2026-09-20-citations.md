# WEM Radar 2026-09-20 — Citations ledger

Edition: **WEEKLY**. Collection window 2026-09-12 → 2026-09-20 (the scheduled 19 Sep run died before research was persisted; this run covers the full window). Last prediction check: 2026-09-12; next due about 2026-10-03 to 2026-10-10.
One row per load-bearing claim in `radar-2026-09-20.md`. Claim typing per L-077: **Fact** · **Fact-that-was-SAID** (a named party asserted it; the assertion is the fact) · **Estimate** · **Inference** (our reading).
Raw research: `reports/research/2026-09-20-weekly/` (streams A-D). Every date was read off the page itself (`datePublished`, `article:published_time` or the printed dateline), never a search snippet.

No claim appears in the brief without a row here.

---

## A. Salesforce (investor session and Dreamforce)

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| A1 | Salesforce held its Dreamforce Investor & Analyst Session on 16 Sep 2026 | Fact | Salesforce IR event page ("September 16, 2026 1:00 PM PT"); deck URL path `2026/Sep/16` | https://investor.salesforce.com/events-and-presentations/events/event-details/2026/Dreamforce-2026-Investor--Analyst-Session-2026-jz1nxEcqq4/default.aspx |
| A2 | The "Agentic" customer stage is described as adopting Agentforce in support "with some seat optimization", with 1.5x-2x spend (ARR) uplift | Fact-that-was-SAID (Salesforce, slide 49) | Salesforce investor deck, 2026-09-16, 66 slides parsed locally | https://s205.q4cdn.com/626266368/files/doc_events/2026/Sep/16/Dreamforce-Investor-Day-2026-Presentation_Final.pdf |
| A3 | Employee-augmenting use cases are monetised as premium seat upgrades; customer-facing agents via Flex Credits, pay-go, outcome-based, AELAs or Salesforce Commit | Fact-that-was-SAID (slide 35) | same deck | (A2) |
| A4 | Premium licence mix 1% (Q1 FY25) → 3% (Q1 FY26) → 5% (Q2 FY27); premium licence ARR $1B+; 60-80% ASP uplift | Fact-that-was-SAID (slide 37). Q1 FY25 = Feb-Apr 2024, rendered "early 2024" | same deck | (A2) |
| A5 | "More Sales, Service, Slack seats"; guidance FY27 $46.1-46.4B footnoted "as of August 2026" = reiterated, not raised | Fact-that-was-SAID (slide 34) · Fact (footnote) | same deck | (A2) |
| A6 | The deck has no standalone Agentforce ARR, no Service seat count, no per-conversation price change | Fact (absence, full-text parse of 66 slides) | same deck | (A2) |
| A7 | Five9 made the fewer-seats-more-spend argument on 11 Sep | Fact-that-was-SAID (carried from 09-12 ledger) | Investing.com transcript, 2026-09-11 | https://www.investing.com/news/transcripts/five9-at-goldman-sachs-communacopia--technology-conference-2026-ai-gains-pace-93CH-4898246 |
| A8 | "Two public vendors now say seat numbers can fall while spending rises; neither figure is audited" | Inference | A2 + A7 | — |
| A9 | Salesforce said on stage its contact-centre service is scheduled to go live in October; no Salesforce release confirms the date | Fact-that-was-SAID via a single trade source · Fact (absence on newsroom) | CX Today, `datePublished 2026-09-16` | https://www.cxtoday.com/ai-automation-in-cx/salesforces-agentic-cx-vision-8-dreamforce-announcements-cx-leaders-need-to-act-on/ |
| A10 | Agentforce Contact Center was first announced in March 2026 (10 Mar) | Fact (date read on CMSWire / Channel Dive result pages by stream C) | stream C finding 2 | (A9) |
| A11 | Casey has resolved five million conversations on help.salesforce.com | Fact-that-was-SAID (Salesforce keynote, via CX Today) | CX Today 2026-09-16 | (A9) |
| A12 | Fin is sold as a named agent beside Casey; Fin resolves 79% of Anthropic's conversations it sees | Fact (portfolio) · Fact-that-was-SAID (79%). Page dated 2026-09-11, one day before the window; carried as context for the October launch, not as an in-window event | Salesforce Newsroom /news/stories/, `datePublished 2026-09-11` | https://www.salesforce.com/news/stories/agentforce-job-ready-ai-agents/ |
| A13 | Koa: first in-house CRM reasoning model, post-trained on NVIDIA Nemotron 3 Super; "three times fewer errors" on Salesforce's own benchmark | Fact · Fact-that-was-SAID (vendor benchmark) | Salesforce Newsroom, 2026-09-15 | https://www.salesforce.com/news/press-releases/2026/09/15/koa-reasoning-model/ |
| A14 | Agentforce Coworker: 100,000 users activated in its first 35 days; no pricing change | Fact-that-was-SAID · Fact (absence) | Salesforce Newsroom, 2026-09-15 | https://www.salesforce.com/news/stories/aiforce-announcement/ |
| A15 | TSA agent: ~100,000 traveller conversations a month, 96% of routine inquiries resolved without escalation | Fact-that-was-SAID | Salesforce Newsroom, 2026-09-14 | https://www.salesforce.com/news/press-releases/2026/09/14/tsa-improves-travel-experience-agentforce/ |
| A16 | Adecco: 2.6M candidate interactions, 35% recruiter time saved | Fact-that-was-SAID (Salesforce deck slide 38) | same deck | (A2) |

## B. Pricing lane

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| B1 | Core $195, Advanced $395, Max $550 per user per month, each with a yearly Flex Credit allowance (500k / 1M / 2.75M per org); announced 3 Sep 2026 (out of window, stated as such in the brief) | Fact | Salesforce Newsroom, `datePublished 2026-09-03` | https://www.salesforce.com/news/stories/salesforce-simplifies-editions-2026/ |
| B2 | The editions were shown to investors this week | Fact (deck, 16 Sep; stream B parsed the deck; stream D saw the table in a search excerpt only, so B's parse is the basis) | (A2) | (A2) |
| B3 | Moor Insights: Salesforce "is sticking with its Flex Credit system but is also adding user-based bundles… That is an interesting hedge" | Fact-that-was-SAID | Moor Insights & Strategy, `datePublished 2026-09-18` | https://moorinsightsstrategy.com/field-notes/at-dreamforce-2026-salesforce-goes-all-in-on-agentic-ai/ |
| B4 | HubSpot plans to keep shifting to a hybrid of seats and credits; pilot with new customers in the Nordics and Benelux | Fact-that-was-SAID, SECONDARY source only (HubSpot IR returned 403); brief says "MarketBeat reports" and "reportedly" | MarketBeat, 2026-09-18 | https://www.marketbeat.com/instant-alerts/event-hubspot-unveils-ai-agent-strategy-lifts-2030-margin-targets-at-analyst-day-2026-09-18/ |
| B5 | HubSpot's own 16 Sep release contains no price | Fact (absence) | stream D finding 6 | (B4) |
| B6 | No tracked vendor reverted from outcome to seat pricing; Fin ($0.99) and Zendesk price pages unchanged | Fact (reversal-language sweep returned zero; pages are UNDATED, "show no change" = compared with last week's reading) | stream D pricing section | https://fin.ai/pricing |
| B7 | "Outcome pricing is not retreating; large vendors are wrapping AI usage inside a seat price" | Inference | B1-B4 | — |

## C. Regulation

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| C1 | AB 1609 enrolled and presented to the Governor 14 Sep 2026 at 1:30 p.m.; not signed, not vetoed as read 20 Sep | Fact | California Legislative Information, status page | https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260AB1609 |
| C2 | AB 1609 terms: >$500M gross annual revenue; no representing a chatbot as human; simple way to request a human in business hours; good-faith effort to connect within 15 minutes or appointment within one business day; holds ≤15 min and ≤1 hour cumulative; $5,000 / $10,000 penalties; public-prosecutor enforcement, no private right of action; exemptions | Fact (enrolled text, B&P Code §§22625-22628) | California Legislative Information, bill text | https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260AB1609 |
| C3 | A bill in the Governor's possession after 1 Sep becomes law if not returned by 30 Sep | Fact (Cal. Const. art. IV §10(b)(2); carried from 09-12 ledger) | California Constitution | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CONS&sectionNum=SEC.%2010.&article=IV |
| C4 | "First tracked law to set a minimum for human availability in large contact centres" | Inference (bounded to laws this radar tracks) | C2 | — |
| C5 | AB 1883, SB 947, SB 951 still with the Governor, unsigned, as read 20 Sep 02:32 UTC | Fact | California Legislative Information | https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260AB1883 · https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB947 · https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB951 |
| C6 | Governor's 18 Sep update acted on 106 bills (82 signed, 24 vetoed by stream D's parse); none of the tracked bills among them | Fact (read via Internet Archive capture 2026-09-19; site blocks plain fetches) | Office of the Governor, 2026-09-18 | https://www.gov.ca.gov/2026/09/18/governor-newsom-issues-legislative-update-9-18-26/ |
| C7 | A secondary tracker (Transparency Coalition, 18 Sep) lists AB 1883 as signed; official record shows otherwise | Fact (both pages read). Brief names no tracker; a public error worth one correcting sentence per the reporting standard | stream D date traps | (C5) |
| C8 | UK Joint Committee on Human Rights AI report published 14 Sep 2026; cites CWU evidence of tools flagging call-centre workers for failing to "upsell"; Government has two months to respond | Fact · Fact-that-was-SAID (union evidence) | UK Parliament, 2026-09-14 | https://publications.parliament.uk/pa/jt5902/jtselect/jtrights/160/report.html |
| C9 | Colorado revised ADMT draft due by 23 Sep; not published as of 20 Sep | Fact | Colorado AG | https://coag.gov/ai/ |
| C10 | Connecticut PA 26-15 live 1 Oct; state DOL notice page dated Aug 2025, no AI mention, no form | Fact (absence) | stream D negatives | — |
| C11 | EU: no Art. 5(1)(f) enforcement action surfaced in the official sources checked | Fact (absence, bounded to sources checked) | stream D negatives | — |
| C12 | Kistler v. Eightfold: no ruling (last docket entry 12 Aug) — NOT in the brief (no change) | Fact | stream D | — |

## D. Quality, analytics and other company moves

| # | Claim | Type | Source (publisher, date) | URL |
|---|---|---|---|---|
| D1 | CallMiner's first press release since 23 Jun 2026 (84 days = twelve weeks), dated 15 Sep; opening line "the global leader in customer experience (CX) automation powered by deep conversation intelligence" | Fact (dateline only, no metadata) | CallMiner, 2026-09-15 | https://callminer.com/news/press-releases/survey-99-of-cx-organizations-use-automation-but-only-24-say-it-delivers-very-positive-customer-experiences |
| D2 | Survey with Vanson Bourne: 99% use automation, 24% "very positive", 95% say humans add more value in at least one interaction type; no sample size in the release | Fact-that-was-SAID (vendor-commissioned survey) | (D1) | (D1) |
| D3 | CallMiner named a Strong Performer in Forrester's customer-feedback Wave, Q3 2026; first appearance | Fact-that-was-SAID (CallMiner; Forrester report paywalled, not read) | CallMiner, 2026-09-17 | https://callminer.com/news/press-releases/callminer-named-a-strong-performer-in-customer-feedback-management-and-analytics-report-by-top-analyst-firm |
| D4 | Medallia only Leader; Cresta a Contender | Fact-that-was-SAID (CX Today summary) | CX Today, `article:published_time 2026-09-18` | https://www.cxtoday.com/customer-analytics-intelligence/customer-analytics-intelligence-ai-cx-trends/ |
| D5 | "Conversation analytics graded as an alternative to surveys"; CallMiner + Observe.AI (8 Sep) moving from scoring to acting | Inference | D1-D4 + 09-12 ledger | — |
| D6 | Decagon São Paulo office; Mercado Libre named as voice customer (Brazilian Portuguese, replacing IVR); no volumes | Fact · Fact-that-was-SAID | Decagon blog, 2026-09-15 | https://decagon.ai/blog/decagon-expands-into-brazil |
| D7 | Wonderful: three agents for Mercado Libre Vehículos Mexico on WhatsApp in ten weeks; ~99% without human intervention "in its first runs" | Fact-that-was-SAID (early-run figure) | Wonderful blog, 2026-09-15 | https://www.wonderful.ai/blog-articles/mercado-libre-and-wonderful-built-an-ai-native-operation |
| D8 | "A large buyer is splitting work between vendors" | Inference | D6 + D7 | — |
| D9 | NiCE: Merlin Entertainments, issue resolution 75%→95%, call answer rate 78%→93% "over the past year" on CXone | Fact-that-was-SAID (NiCE). PUBLIC newsroom only | NiCE, `datePublished 2026-09-15` | https://www.nice.com/press-releases/merlin-entertainments-elevates-the-guest-experience-across-its-global-attractions-with-nice-cxone |
| D10 | Sierra AIUC-1 certification, Schellman audit, technical evaluations at least quarterly | Fact-that-was-SAID | Sierra blog, 2026-09-17 | https://sierra.ai/blog/sierra-achieves-aiuc-1-certification |
| D11 | Parloa Zones | Fact-that-was-SAID | Parloa blog, 2026-09-17 | https://www.parloa.com/blog/parloa-zones-deploy-ai-globally-with-data-residency-you-can-prove/ |
| D12 | Zendesk Specialized AI Agents; 1M+ custom-agent executions in seven weeks; no price | Fact-that-was-SAID · Fact (absence) | Zendesk, `article:published_time 2026-09-14` | https://www.zendesk.com/newsroom/press-releases/zendesk-introduces-specialized-ai-agents-purpose-built-for-your-business/ |
| D13 | Five9 fell 5.7% on 18 Sep with no company news; nothing published since 11 Sep remarks (newest release 26 Aug) | Fact (price move; newsroom parsed). The AI-written article's causal story is NOT used | Quiver Quantitative, 2026-09-18 | https://www.quiverquant.com/news/Five9+slides+5.7%25+as+insider-sale+filings+and+litigation+overhang+weigh+on+sentiment |
| D14 | Teneo AI: lender Capital Four took 939,642,102 new shares for ~SEK 290M debt; ≈29.9% of the enlarged 3.14B share count | Fact · Inference (the percentage is our arithmetic) | Teneo AI release via TradingView, 2026-09-16 | https://www.tradingview.com/news/modular_finance:a8ca334d4dd39:0-teneo-ai-announces-the-outcome-of-directed-share-issues-and-the-completion-of-refinancing/ |
| D15 | Daily Kos republished the 7 Sep Capital & Main LanguageLine story on 13 Sep; no new reporting, no NiCE response, no new employer statement | Fact | Daily Kos, 2026-09-13 | https://www.dailykos.com/stories/2026/9/13/800096420/tech/ai-hasnt-replaced-these-interpreters-but-it-has-degraded-their-working-conditions/ |
| D16 | Verint/Calabrio: no press release for 26 days; no combined product | Fact (absence) | stream A N1 | — |
| D17 | Solidroad + Unwrap partnership, 15 Sep | Fact | PR Newswire, 2026-09-15 | https://www.prnewswire.com/news-releases/solidroad-and-customer-intelligence-platform-unwrap-partner-to-turn-insight-into-action-302878604.html |
| D18 | Listen Labs: no agreement, denial or collapse | Fact (absence) | stream C N1 | — |
| D19 | No acquisition, funding round, earnings print or exec move among tracked vendors | Fact (absence across four streams; bounded to the tracked universe) | streams A-D negatives | — |

## Link audit (L-076)

Run 2026-09-20 via `reports/research/2026-09-20-weekly/link-audit-2026-09-20.py` (re-runnable; raw result in `link-audit-2026-09-20.json`).

**34 unique URLs** extracted from this ledger. Measured result: **31 returned HTTP 200-range · 3 returned a bot-gate (403) · 0 dead · 0 timeouts.**

Per L-076 a bot-gate is **VERIFY-MANUALLY**, not dead. Every gated URL was read successfully in-run:

| URL | Status | Handling |
|---|---|---|
| investor.salesforce.com (Dreamforce investor session event page, A1) | 403 | VERIFY-MANUALLY. Read in-run. Claim NOT demoted. |
| publications.parliament.uk (Joint Committee on Human Rights AI report, C8) | 403 | VERIFY-MANUALLY. Read in-run. Claim NOT demoted. |
| investing.com (Five9 Goldman Sachs transcript, A7) | 403 | VERIFY-MANUALLY. Read in-run. Claim NOT demoted. |

**Zero claims demoted.**

---

## Register gate

**SOP-2 §6c, run 2026-09-20 on every public derivative of this edition. Verdict: EDITED then PASS on the traced controls.**
Full record: `ProductBeacon/Marketing/social-assets/state-of-wfo-2026/radar-weekly-2026-09-20/register-gate-2026-09-20.md`.

Derivatives in scope: `carousel.html`, `wem-radar-weekly-2026-09-20.pdf`, the 9 slide PNGs, `distribution-pack.txt` (Caption A, Caption B, first comment, Yohay comment, stakeholder note), `distribution-pack.html` (posting console), `update-card-text.md`, `update-card.html`.

**Five copy edits**, none made by relaxing a gate: (E1) slide 6 headline "CallMiner now leads with automation." became "CallMiner repositions around automation.", because "leads" read alone is a leadership claim this ledger does not make [D1]; (E2) slide 7 "Sierra passed an independent audit" became "Sierra says it passed an independent audit" [D10 is Fact-that-was-SAID]; (E3) the stakeholder note's "No price has been published." had no row here and became "Salesforce has not published a release confirming the date." [A9]; (E4) the Update card teaser gained "It is neither signed nor vetoed, and" so the status travels with the mechanism [C1, C3], final length 426 characters; (E5) Caption B "a market analyst" became "an analyst", because the posting console's Caption B form gate keys on that role phrase and misread the caption's form. That last one is a gate-routing fix, not a register defect.

**Passed with a note for the owner, not edited:** the unattributed description of Salesforce's charging model [A3]; the unhedged slide 3 headline whose hedge sits in the first bullet [A9]; "are spreading" on two vendors [B1, B4, B7]; the slide 5 headline without "good-faith effort" [C2]; the compressed CallMiner self-description quote [D1]; the unlabelled closing headline [A8, C4].

**Controls asserted:** hedge pairing on every surface that states a vendor figure; no Inference presented as fact (five "Our view:" reads and one "Watch:"); absolutes scoped to the vendors and laws this radar tracks; zero em dashes; zero process language; the former employer is named on no substantive slide and in no caption, comment, note or teaser.

**Gate results after the edits:** carousel data, HTML and layout gates 46 OK, 0 FAIL (9 slides) · `verify-pdf.py` 39 OK, 0 FAIL · readability gate `--strict` 0 FAIL, 0 WARN · `build_console.py` 24 OK, 0 FAIL · `check-protected-spans.py` 2 byte assertions and 83 other assertions run, 26 self-test mutations rejected, **14 rows red and CORRECT** (`gc_validated` is false on every row of this fresh draft classification; SOP-2 §5a is non-agent-clearable).

**Gate re-cuts, none loosening a rule, each shown able to fail:** the builder's and the PDF verifier's expected former-employer count moves from ONE back to ZERO with the predicate and red fixtures kept; the LanguageLine "floor" slide assertion, which had no referent, is replaced by a guard that fails if that story returns to a slide; the dateline regex carries this edition's names; the PDF verifier's second sources control moves from "Ynetnews" (not in this ledger) to "Quiver Quantitative" (row D13, backs no slide, both proved live); the console's stale-copy probes point at the 12 September pack and all five must be present there; the console's Caption A probes are this edition's findings; the pack verifier compares `report.md` with the brief of record and the console blocks with `distribution-pack.txt`, in place of the 12 September experiment prose; the brief-link verifier checks this edition's list prices in place of the 12 September Lorikeet amounts.

**Nothing has been deployed, pushed, posted or emailed.** Publication remains subject to SOP-2 §5.5 and the §5a protected-spans classification. Posting is the owner's call.
