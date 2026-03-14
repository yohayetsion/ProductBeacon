# ProductBeacon GTM Engine
## Automation-First Go-To-Market Architecture

---

## The Core Thesis

ProductBeacon sells trust-based, high-ticket fractional product leadership. The conventional wisdom says "don't cold email for consulting." But conventional wisdom assumes manual operations.

With Claude Code automation, we can do what no solo consultant can: run a signal-based outreach engine that combines deep prospect research with personalized, high-quality touches at a sustainable cadence. Not 300 T1s/week like SKYMOD. But not zero either.

**The model: Signal-Triggered, Research-Deep, Low-Volume, Multi-Channel.**

---

## Engine Architecture

The ProductBeacon GTM engine has five automated subsystems that feed each other:

**1. Signal Scanner** — Monitors buying signals daily across multiple sources

**2. Enrichment Pipeline** — Builds deep prospect dossiers with product org intelligence

**3. Outreach Engine** — Signal-triggered email sequences (T1-T4) + referral activation

**4. Content Pipeline** — LinkedIn posts, newsletter, and content assets generated from real work

**5. Nurture System** — Long-term value drip for prospects who engaged but didn't convert

Each subsystem is designed to run through Claude Code with minimal manual intervention.

---

## Subsystem 1: Signal Scanner

### What It Monitors

The signal scanner runs daily, looking for companies showing buying signals for fractional product leadership.

| Signal | Intent Level | Source | Automation Method |
|--------|-------------|--------|-------------------|
| VP Product / CPO departure | Tier 1 (Active Pain) | PDL People API, LinkedIn | PDL title change detection, weekly query |
| "Head of Product" job open 60+ days | Tier 1 | LinkedIn Jobs, Indeed, careers pages | Firecrawl scrape of job boards, filtered by days open |
| Series A-C funding in last 45 days | Tier 1 | Crunchbase API, TechCrunch RSS | Daily API pull, filter by stage + geo |
| 3+ PM roles posted simultaneously | Tier 1 | LinkedIn Jobs, company careers | Keyword + company clustering |
| Founder still "CEO & Head of Product" at 50+ employees | Tier 2 | PDL Company + People API | Automated query: company size > 50, no VP/CPO title |
| No VP Product on LinkedIn at Series B+ company | Tier 2 | PDL | Cross-reference funding stage with leadership titles |
| Recent product stumbles / bad reviews | Tier 2 | G2, Product Hunt, App Store | Firecrawl + sentiment filtering |
| New CEO/CTO at a startup | Tier 2 | PDL, LinkedIn | Title change monitoring |
| Competitor raised a round | Tier 3 | Crunchbase | Cross-reference with target company list |
| Board change / new investor | Tier 3 | Crunchbase, LinkedIn | Periodic monitoring |

### Signal Scanner Output

Each qualified signal produces a prospect record with:
- Company name, URL, funding stage, headcount
- Signal type, signal date, signal source
- Relevance score (0-100)
- Suggested buyer (CEO, CTO, or board member)
- Domain overlap with Yohay's experience

### Implementation

A daily Python script (`signal-scanner.py`) that:
1. Queries PDL, Crunchbase API, and scrapes job boards via Firecrawl
2. Scores each signal against ICP criteria
3. Deduplicates against existing pipeline
4. Outputs qualified prospects into `ProductBeacon/Sales/pipeline/index.json`

---

## Subsystem 2: Enrichment Pipeline

### Layers of Enrichment

Unlike SKYMOD (email + company basics), ProductBeacon needs product org intelligence.

**Layer 1 — Company Profile (Automated)**
- Funding stage, total raised, last round date, investors
- Headcount, industry vertical, tech stack
- Product team size estimate (count PM/designer/researcher on LinkedIn via PDL)

**Layer 2 — Leadership Gap Analysis (Automated)**
- Current product leadership (PDL: who has "Product" in VP+ titles?)
- Gap detection: No VP/CPO? Founder doubles as product lead? Recent departure?
- Hiring signals: Open product roles, duration, reposting frequency

**Layer 3 — Relevance Scoring (Automated)**
- Domain overlap: security, intelligence, SaaS, enterprise, AI
- Stage fit: Series A-C, 20-200 employees
- Geography: Israel, US, UK, Europe
- Signal recency: fresher = higher score

**Layer 4 — Buyer Research (Claude Code assisted)**
- Decision maker identification (CEO at <50 employees, CTO/COO at 50-200)
- LinkedIn profile review, career background, recent posts
- The "natural opening" — what makes outreach feel relevant

### Prospect Schema

```
company: string
url: string
fundingStage: string
lastFundingDate: string
lastFundingAmount: string
headcount: number
productTeamSize: number | null
hasVPProduct: boolean
hasCPO: boolean
founderLeadsProduct: boolean
signalType: string
signalDate: string
signalSource: string
relevanceScore: number (0-100)
domainOverlap: string[]
buyer: { name, title, email, linkedin }
```

---

## Subsystem 3: Outreach Engine

### Volume Model

| Metric | Target |
|--------|--------|
| T1s per week | 20-30 |
| Research time per prospect | 20-30 minutes (Claude Code assisted) |
| Follow-ups (T2-T4) | Auto-generated, auto-scheduled |
| Max touches per prospect | 4 (then nurture or silence) |
| Total sequence duration | 30 days |

### Signal-Triggered Email Sequences (T1-T4)

| Touch | Day | Objective | Content |
|-------|-----|-----------|---------|
| T1 | 0 | Get a reply | Signal-specific opening, one proof point, soft CTA |
| T2 | 4-5 | Provide value | Relevant framework or insight, no pitch |
| T3 | 12-14 | Pattern-match story | Case study micro-narrative mapped to their situation |
| T4 | 30 | Graceful close | Door open, link to LinkedIn or Product Org OS |

### How This Differs from SKYMOD/Maad House

| Dimension | SKYMOD / Maad House | ProductBeacon |
|-----------|---------------------|---------------|
| Volume | 50/day (300/week) | 5/day (25/week) |
| Research depth | Company-level | Buyer-personal + product org analysis |
| Email format | HTML branded template | Plain text, peer-to-peer |
| Personalization | Company hook + pitch deck | Signal-specific, deeply researched |
| CTA | Meeting / demo | "Worth a conversation?" |
| Sequence length | T1-T5 (5 touches) | T1-T4 (4 touches max) |
| Tone | Professional vendor | Senior colleague |
| Sign-off | Full signature block | First name only |

### Referral Activation (Parallel Track)

Three segments, each with tailored sequences:

| Segment | Volume | Approach |
|---------|--------|----------|
| VCs / Investors | 20-30 total | 3-touch sequence + free workshop offer |
| Former Colleagues (NICE/Cognyte) | 30-50 total | Single personal email, specific ask |
| Ecosystem Partners (recruiters, agencies) | 10-20 total | 2-touch mutual referral pitch |

---

## Subsystem 4: Content Pipeline

### Why Content Matters Even in an Email-First Engine

Content serves three purposes in this architecture:

1. **Pre-warming:** When a prospect receives T1, they Google you. LinkedIn posts and articles build ambient authority so the email doesn't land cold.

2. **T2 fuel:** Every T2 email shares a relevant piece of content. The content pipeline feeds the outreach engine.

3. **Nurture material:** The content-nurture sequence (Subsystem 5) needs a steady stream of frameworks, case studies, and insights.

### What Claude Code Automates

| Content Type | Cadence | Automation Level |
|-------------|---------|-----------------|
| LinkedIn posts | 3/week | Claude Code drafts from frameworks, case studies, industry observations. Yohay reviews + posts. |
| Newsletter | Monthly | Claude Code drafts from signal scanner insights + engagement learnings. Yohay edits. |
| Case study write-ups | Per engagement | Claude Code structures from engagement notes. Yohay approves. |
| Framework articles | 2/month | Claude Code expands Vision to Value frameworks into standalone pieces. |
| Signal digest (public) | Weekly | Claude Code synthesizes buying signals into anonymized market intelligence. |

### Content Pillars

| Pillar | What It Covers | Why It Converts |
|--------|---------------|-----------------|
| "The Accidental Product Leader" | CTOs and founders doing product by default | Normalizes the pain, positions fractional as the solution |
| "Scaling Past Founder-Led Product" | The inflection point when founder intuition isn't enough | Hits the exact moment they need a fractional CPO |
| "AI-Powered Product Ops" | How Product Org OS changes what a product leader can deliver | Demonstrates the unfair advantage |
| "War Stories" | Anonymized patterns from 17 years at NICE/Cognyte | Content nobody else can write, builds deep trust |

### Content-to-Pipeline Path

```
LinkedIn post catches attention
    → Profile visit → productbeacon.agency link
        → Strategic infrastructure page (9 docs as proof)
            → "Book a diagnostic call" CTA
                → Discovery conversation
```

---

## Subsystem 5: Nurture System

### Who Enters Nurture

- Prospects who replied but didn't book a call
- Discovery calls that didn't convert to proposals
- Referrals where timing wasn't right
- Product Org OS GitHub users / stargazers

### Nurture Sequence (N1-N6)

| Email | Week | Content Type | Purpose |
|-------|------|-------------|---------|
| N1 | 1 | Actionable framework | Prove expertise, give immediate value |
| N2 | 3 | Case study deep-dive | Show real outcomes |
| N3 | 5 | Contrarian insight | Demonstrate original thinking |
| N4 | 7 | Product Org OS highlight | Free tool as trust builder |
| N5 | 9 | Industry analysis | Position as someone with a wide lens |
| N6 | 12 | Gentle re-engagement | Specific, time-bound offer |

After N6: Move to monthly newsletter. Re-enter signal-triggered outreach only if new Tier 1 signal fires.

---

## Weekly Engine Cadence

| Day | Activity | Subsystem |
|-----|----------|-----------|
| **Monday** | Signal scan + prospect qualification. Review signals, qualify 25-30 prospects. | Signal Scanner |
| **Tuesday** | Enrichment + buyer research for qualified prospects. | Enrichment Pipeline |
| **Wednesday** | T1 drafting + test batch to yohay@gmail. LinkedIn content drafting. | Outreach + Content |
| **Thursday** | T1 sends (after approval) + all due follow-ups (T2-T4). LinkedIn posts. | Outreach + Content |
| **Friday** | Pipeline review, metrics check, signal scanner tuning. Newsletter draft (monthly). | Operations |

### Send Windows

| Email Type | Days | Time |
|-----------|------|------|
| Cold outreach (T1-T4) | Tuesday-Thursday | 09:00-11:00 buyer's local time |
| Nurture emails | Tuesday or Thursday | 10:00-12:00 |
| Referral activation | Monday-Wednesday | 09:00-11:00 |

**Weekend block applies** (per Etsion Brands outreach guardrails).

---

## ICP Definition

### Primary Target

| Attribute | Criteria |
|-----------|----------|
| Company stage | Series A through C |
| Funding | $5M-$50M raised |
| Headcount | 20-200 employees |
| Product team | 0-10 people, no VP/CPO |
| Geography | Israel, US, UK, Europe |
| Industries | SaaS, cybersecurity, AI/ML, enterprise software, fintech |
| Buying signal | At least one Tier 1 or two Tier 2 signals |

### Decision Maker

| Company Size | Primary Buyer | Secondary |
|-------------|---------------|-----------|
| < 50 employees | CEO / Founder | CTO |
| 50-200 employees | CTO or COO | Board member / Lead investor |

### Anti-Patterns (Do Not Target)

- Pre-seed or bootstrapped (can't afford fractional)
- 500+ employees (need full-time, not fractional)
- Already has VP Product + CPO (no gap)
- Consumer apps (Yohay's expertise is enterprise/B2B)
- Companies that just hired a Head of Product in last 3 months

---

## Metrics Dashboard

### Pipeline Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Signals detected / week | 50-100 | Signal scanner output |
| Qualified prospects / week | 25-30 | After ICP filtering |
| T1s sent / week | 20-30 | Pipeline tracking |
| Reply rate (cold) | > 15% | Replies / T1s sent |
| Positive reply rate | > 8% | Interested replies / T1s sent |
| Discovery calls / month | 4-6 | From all channels combined |
| Proposals sent / quarter | 3-5 | Post-discovery conversion |
| Clients won / quarter | 1-2 | Closed deals |

### Channel Attribution

Track the source of every discovery call:

| Channel | Expected Contribution |
|---------|----------------------|
| Signal-triggered outreach | 40-50% of conversations |
| Referrals (VC, colleagues, partners) | 25-35% of conversations |
| Inbound from content (LinkedIn, newsletter) | 15-25% of conversations |
| Product Org OS / GitHub | 5-10% of conversations |

---

## Implementation Roadmap

### Phase 0: Infrastructure (Week 1)

- Set up yohay@productbeacon.agency email via Outlook
- Create ProductBeacon pipeline schema (extend existing infrastructure)
- Configure PDL queries for product leadership gap detection
- Set up Crunchbase API access (or alternative funding data source)

### Phase 1: Manual Foundation (Weeks 2-4)

- Hand-craft first 10 T1 emails to establish voice and templates
- Send referral activation to 20 former colleagues
- Begin LinkedIn posting cadence (3/week)
- Track everything manually to validate signal quality

### Phase 2: Automation (Weeks 5-8)

- Build `signal-scanner.py` (job postings + funding signals)
- Integrate enrichment pipeline with PDL
- Set up follow-up generation (T2-T4) per existing SKYMOD infrastructure
- Launch content-nurture sequence for warm prospects

### Phase 3: Optimization (Weeks 9-16)

- Add Tier 2 signals to scanner (leadership gaps, founder-as-CPO detection)
- A/B test email approaches (signal types, CTAs, proof points)
- Build public signal digest (content marketing + authority building)
- Launch VC referral sequence

### Phase 4: Scale (Months 4-6)

- Refine ICP based on reply data and conversion patterns
- Add new signal sources (G2 reviews, product launches, tech stack changes)
- Explore LinkedIn automation (connection requests synced with email outreach)
- Build "Product Org Health Check" as lead magnet

---

## Subsystem 6: Extended Automated Channels

Beyond email, Claude Code can automate five additional channels that multiply reach with minimal manual effort.

### Channel 1: LinkedIn Content Automation

**Why it matters:** LinkedIn is where the ICP lives. 3 posts/week builds ambient authority so when T1 lands, the prospect has already seen Yohay's name. LinkedIn is the pre-warming engine for cold email.

**Automation approach:** CDP-based browser automation (same architecture as the existing `baoyu-post-to-x` skill for X/Twitter). Claude Code drafts posts from real engagement work, frameworks, and case studies. Yohay reviews, then automated posting handles scheduling and publishing.

| Content Type | Cadence | Source Material |
|-------------|---------|----------------|
| Methodology insight | 1/week | Vision to Value frameworks, Product Org OS capabilities |
| War story / pattern recognition | 1/week | Anonymized engagement learnings, NICE/Cognyte experience |
| Industry commentary / contrarian take | 1/week | Signal scanner data, market observations |

**Conversion path:** Post impression → profile visit → productbeacon.agency link → strategic infrastructure page → "Book a diagnostic call"

### Channel 2: Programmatic SEO

**Why it matters:** Long-tail search captures high-intent buyers Googling their exact problem. "Fractional CPO for cybersecurity startups" has low competition and high intent. Once pages are live, they generate leads with zero ongoing effort.

**Automation approach:** Claude Code generates 20-30 landing pages targeting specific verticals, company stages, and geographies. Deploy to GitHub Pages (same hosting as ProductBeacon site). Each page is a tailored value proposition with relevant case studies and a booking CTA.

**Target page templates:**

| Pattern | Examples | Search Intent |
|---------|----------|---------------|
| Fractional CPO for [industry] | "Fractional CPO for cybersecurity", "...for fintech", "...for SaaS" | Buyer knows they need fractional, searching by industry fit |
| Fractional product leader [city] | "Fractional product leader Tel Aviv", "...London", "...New York" | Location-based search |
| Interim VP Product [situation] | "Interim VP Product after departure", "...during Series A" | Situation-based search |
| Alternative to [pain] | "Alternative to hiring a full-time CPO", "CTO doing product work" | Problem-aware, solution-seeking |

**Implementation:** Use `/programmatic-seo` skill to design templates, Claude Code generates page content, deploy via `gh-pages` to ProductBeacon repo.

### Channel 3: X/Twitter Content

**Why it matters:** Cross-posting LinkedIn content to X doubles reach for near-zero marginal effort. Product and startup communities are active on X. Product Org OS announcements get traction with the developer-adjacent audience.

**Automation approach:** Already built. `baoyu-post-to-x` skill uses CDP-based Chrome automation. Adapt LinkedIn posts for X format (shorter, more direct). Thread format for frameworks and case studies.

| Content Type | X Adaptation |
|-------------|-------------|
| LinkedIn methodology post | Compress to 280 chars + thread for depth |
| War story | Single punchy tweet with link to full post |
| Product Org OS update | GitHub release note + link |
| Signal digest | "This week in product leadership gaps" thread |

### Channel 4: Podcast Guest Pitching

**Why it matters:** One podcast appearance to 5,000 listeners beats months of cold email. It's the highest-leverage trust-building channel for a solo consultant. And the pitching itself is just email outreach to a different ICP.

**Automation approach:** Same email engine, different target list. Claude Code researches 50-100 product/startup/leadership podcasts, identifies relevant recent episodes, and drafts personalized pitches referencing specific episodes.

**Target podcasts (categories):**

| Category | Examples | Pitch Angle |
|----------|----------|-------------|
| Product management | Lenny's Podcast, Product Thinking, This Is Product Management | "17 years of product org leadership, now augmented by AI" |
| Startup leadership | The Twenty Minute VC, SaaStr, Founder Coffee | "Why your startup needs a fractional CPO before a full-time one" |
| AI in business | AI-powered workflows, practical AI | "I built an 82-agent AI system that does product org work" |
| Israeli tech | Techie Tuesdays, Startup Camel | Local angle, NICE/Cognyte pedigree |

**Sequence:** Same T1-T3 structure as prospect outreach, adapted for podcast hosts. Research the show, reference a specific episode, pitch a specific topic, offer a unique angle.

### Channel 5: Newsletter / Signal Digest

**Why it matters:** A weekly or monthly newsletter is a owned-audience channel. Every subscriber is a warm prospect or referral source. The signal scanner already produces the raw material.

**Automation approach:** Claude Code synthesizes signal scanner data + engagement learnings into a "Product Leadership Signal" digest. Anonymized market intelligence about product org trends, leadership changes, and patterns. Send via existing email infrastructure (Outlook CLI or Gmail CLI).

**Content structure:**

```
Subject: Product Leadership Signal - Week of [date]

This week's patterns:
- [X] Series A-C companies posted VP Product roles
- [Y] product leadership changes detected
- Trend: [observation about the market]

Framework of the week:
[One actionable framework from Vision to Value]

Case study spotlight:
[Anonymized mini case study, 3-4 sentences]

---
Yohay Etsion | ProductBeacon
productbeacon.agency
```

**Growth mechanic:** Add cold outreach prospects to the newsletter BEFORE emailing them. When T1 lands, they've already received 1-2 value-packed digests. The email doesn't feel cold anymore.

### Channel Summary: Automation Levels

| Channel | Automation Level | Claude Code Role | Yohay's Role |
|---------|-----------------|-----------------|--------------|
| Email outreach (T1-T4) | High | Draft, enrich, schedule, send | Review + approve test batch |
| LinkedIn posts | High | Draft content, schedule via CDP | Quick review before post |
| Programmatic SEO pages | Full | Generate, deploy to GitHub Pages | One-time review of templates |
| X/Twitter posts | Full | Adapt LinkedIn content, post via CDP | Minimal (cross-post) |
| Podcast pitching | High | Research shows, draft pitches, send | Record the actual episode |
| Newsletter / Signal digest | High | Generate from signal scanner data | Light edit before send |
| Signal monitoring | Full | Daily automated scans | Review qualified signals |
| Referral activation | Medium | Draft emails | Personal touch on each |
| Nurture sequences | High | Generate content, schedule sends | Approve sequence content |

---

## Reusable Infrastructure

### What Carries Over from SKYMOD/Maad House

| Component | Reusability |
|-----------|-------------|
| Pipeline schema + tracking | High (extend with PB-specific fields) |
| `send-t1-batch.py` (atomic send + pipeline update) | Direct reuse |
| `generate-followups.py` (T2-T4 generation) | Adapt templates |
| `validate-batch.py` (pre-send checks) | Direct reuse |
| `daily-gtm-run.py` orchestrator | Extend for PB |
| Hunter.io / PDL enrichment | Direct reuse + new queries |
| Outlook CLI for sending | Direct reuse (new account) |
| Test batch approval flow | Direct reuse |

### What's New

| Component | Purpose |
|-----------|---------|
| `signal-scanner.py` | Daily buying signal detection |
| Product org enrichment queries | PDL queries for leadership gap analysis |
| LinkedIn content drafting pipeline | Claude Code generates post drafts |
| Prospect dossier generator | Deep research briefs per prospect |
| Nurture sequence engine | Bi-weekly value drip management |

---

## Key Principles

1. **Signal-first, not list-first.** Never email without a trigger. Every T1 references why you're reaching out NOW.

2. **Plain text, peer tone.** No HTML templates, no branding, no images. You're a senior colleague, not a vendor.

3. **4 touches max.** T1-T4 over 30 days. After that, nurture or silence. Never re-enter cold sequence.

4. **One proof point per email.** Never the full resume. Rotate: "17 years at NICE/Cognyte" OR "$106K in 8 weeks" OR "82 AI agents."

5. **Research quality > send volume.** 25 deeply researched emails beat 250 generic ones at this price point.

6. **Content pre-warms the email.** LinkedIn posts ensure prospects have seen your name before T1 lands.

7. **The diagnostic call IS the sales mechanism.** Everything in the engine drives toward a 30-minute conversation where Yohay demonstrates CPO-caliber thinking live.

8. **Automate everything except judgment.** Claude Code handles signal detection, enrichment, drafting, scheduling. Yohay reviews and approves.

---

## Next Steps

### Phase 0: Infrastructure (Week 1)
- [ ] Set up yohay@productbeacon.agency email via Outlook
- [ ] Create ProductBeacon pipeline schema (extend existing infrastructure)
- [ ] Configure PDL queries for product leadership gap detection
- [ ] Set up Crunchbase API access for funding signal data

### Phase 1: Email Engine (Weeks 2-4)
- [ ] Hand-craft first 10 T1 emails to establish voice
- [ ] Build signal scanner MVP (`signal-scanner.py` — job postings + funding rounds)
- [ ] Launch referral activation to 20 former NICE/Cognyte colleagues
- [ ] Send VC referral sequence to 10-15 investors

### Phase 2: Content Channels (Weeks 3-6)
- [ ] Build LinkedIn CDP posting automation (adapt from X/Twitter skill)
- [ ] Begin LinkedIn posting cadence (3/week)
- [ ] Launch X/Twitter cross-posting
- [ ] Generate first batch of programmatic SEO pages (10 industry verticals)
- [ ] Deploy SEO pages to ProductBeacon GitHub Pages

### Phase 3: Scale Channels (Weeks 5-8)
- [ ] Launch newsletter / signal digest (weekly or bi-weekly)
- [ ] Research and pitch 20 podcasts
- [ ] Build content-nurture sequence for warm prospects
- [ ] Integrate follow-up generation (T2-T4) with existing infra

### Phase 4: Optimization (Weeks 9-16)
- [ ] Add Tier 2 signals to scanner
- [ ] A/B test email approaches by signal type
- [ ] Refine ICP based on reply data and conversion patterns
- [ ] Build "Product Org Health Check" interactive lead magnet
- [ ] Expand programmatic SEO to 30+ pages
