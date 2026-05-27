"""Round 15 Wave B T2: replace author.html hero + body with author bio content."""
import pathlib

p = pathlib.Path('research/author.html')
src = p.read_text(encoding='utf-8')

# Replace hero block
old_hero = """  <p class="hero-eyebrow">ProductBeacon Research</p>
  <h1 class="hero-headline">Methodology</h1>
  <p class="hero-subhead" id="hero-subhead">Sourcing rules, disclosure framework, and refresh cadence for the open-web market research published under the ProductBeacon Research banner.</p>

  <p class="hero-byline" style="margin-top: var(--space-3); font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--slate-400); letter-spacing: 0.05em;">v1.0 &middot; Last updated 2026-05-23 &middot; By Yohay Etsion</p>
</header>"""

new_hero = """  <p class="hero-eyebrow">ProductBeacon Research</p>
  <h1 class="hero-headline">Yohay Etsion</h1>
  <p class="hero-subhead" id="hero-subhead">Author of ProductBeacon Research. Operator first, analyst second.</p>

  <p class="hero-byline" style="margin-top: var(--space-3); font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--slate-400); letter-spacing: 0.05em;">Last updated 2026-05-27</p>
</header>"""

assert old_hero in src, "hero block not found"
src = src.replace(old_hero, new_hero)

m_start = src.find('<section class="methodology-content"')
m_end = src.find('</main>', m_start)
assert m_start > 0 and m_end > 0

H2_STYLE = 'style="font-family: \'IBM Plex Serif\', serif; font-weight: 500; font-size: 32px; color: var(--bright); margin: var(--space-7) 0 var(--space-3);"'
H2_STYLE_FIRST = 'style="font-family: \'IBM Plex Serif\', serif; font-weight: 500; font-size: 32px; color: var(--bright); margin: var(--space-3) 0 var(--space-3);"'
A_AMBER = 'style="color: var(--amber);"'

new_body = f'''<section class="methodology-content" style="max-width: 760px; margin: 0 auto; padding: var(--space-4) var(--space-5) var(--space-7);">

<h2 {H2_STYLE_FIRST}>How I got here</h2>
<p>I spent 17 years inside two product organisations before I started writing about the cyber market from the outside.</p>
<p>At NICE I ran product for the analytics and customer-experience portfolio. At Cognyte (the security intelligence business that spun out of Verint) I led product across the platform. Across both companies I owned roughly 30-person product organisations and roughly USD 200M of portfolio scope. I sat across the table from hundreds of enterprise buyers, sold into governments and regulated verticals, and shipped products that ran in production at scale.</p>
<p>What I learned, over and over, is that the buyer conversation about a category is almost never the conversation the vendor-marketing layer is having. The research on this site is what I would have wanted to read when I was the buyer, the seller, and the product builder, in the same week.</p>

<h2 {H2_STYLE}>What I have written</h2>
<p><strong>Leading the Charge</strong> is my book on running modern product organisations. It is published and available. The argument: product leadership is a set of operating disciplines, not a personality, and the disciplines are teachable.</p>
<p><strong>Vision to Value</strong> is forthcoming in 2026. It is the field manual for turning a product strategy into a system that compounds across quarters instead of resetting every planning cycle. It draws on the same operating patterns I used at NICE and Cognyte.</p>
<p>Both books inform the research voice on this site. The cyber-market reports are not journalism. They are operator analysis grounded in the same patterns the books cover.</p>

<h2 {H2_STYLE}>What this research is, and what it is not</h2>
<p>ProductBeacon Research is open-web research. Every claim in every chapter cites a public source. No vendor sponsors the work. No analyst-relations team previews the chapters. The Verifiable Proxy Rule (see the <a href="/research/methodology.html" {A_AMBER}>methodology page</a>) means every Pattern Claim can be falsified by a named, public event.</p>
<p>What the research deliberately does not cover:</p>
<ul>
<li><strong>Private financials of pre-IPO vendors</strong> beyond what their public filings, customer disclosures, or named press coverage reveal. We do not infer ARR from headcount or guess at burn rates.</li>
<li><strong>Identity, endpoint, network, and SOC categories.</strong> The four chapters (IRM, DLP, DSPM, and the Convergence Synthesis) are bounded by design. Adjacent categories will get their own research surface when warranted.</li>
<li><strong>Vendor product roadmaps under NDA.</strong> If a roadmap detail is not on a public earnings call, a customer-facing keynote, or a regulatory filing, it is not in the report.</li>
<li><strong>Geographies outside North America and Europe.</strong> APAC and LATAM cyber dynamics are sufficiently different that they deserve their own treatment, not a footnote.</li>
</ul>
<p>Biases worth naming: my operator background is enterprise-software, not pure-play security. I read the category through a product-organisation lens, not a threat-intel lens. Readers who want red-team-grounded analysis should treat this site as a complement, not a substitute.</p>

<h2 id="disclosure" {H2_STYLE}>Disclosure</h2>
<p>I serve as Fractional Chief Product Officer at AXIA Security, an insider-risk-management vendor. The IRM chapter of this report covers the IRM category, which includes AXIA. The other three chapters do not. Coverage, ranking, and pattern claims in every chapter are mine alone; AXIA had no editorial input and no review rights, and no vendor pays for inclusion or placement. Sources, citations, and methodology are open at <a href="/research/methodology.html" {A_AMBER}>/research/methodology</a>.</p>

<h2 {H2_STYLE}>Research questions</h2>
<p>Research questions: <a href="mailto:research@productbeacon.agency" {A_AMBER}>research@productbeacon.agency</a></p>
<p>I read every message. I do not run a sales motion off this address. If you are an analyst, operator, or buyer with a question about the methodology or a specific Pattern Claim, this is the right channel.</p>

<h2 {H2_STYLE}>Where to start</h2>
<ul>
<li><strong>Pre-Call Briefing Pack.</strong> 60-minute pre-read. Three Pattern Claims, three buyer choices, the falsifiable tests behind each. <a href="/research/state-of-cyber-2026/pre-call-brief.html" {A_AMBER}>/research/state-of-cyber-2026/pre-call-brief.html</a></li>
<li><strong>Report Digest.</strong> 14-page chapter-by-chapter synthesis. <a href="/research/state-of-cyber-2026/synthesis.html" {A_AMBER}>/research/state-of-cyber-2026/synthesis.html</a></li>
<li><strong>The four chapters.</strong> Insider Risk Management, Data Loss Prevention, Data Security Posture Management, and the Convergence Synthesis. <a href="/research/state-of-cyber-2026/" {A_AMBER}>/research/state-of-cyber-2026/</a></li>
<li><strong>Methodology.</strong> Sourcing rules, the Verifiable Proxy Rule, refresh cadence, disclosure framework. <a href="/research/methodology.html" {A_AMBER}>/research/methodology.html</a></li>
</ul>

</section>
'''

src = src[:m_start] + new_body + src[m_end:]
p.write_text(src, encoding='utf-8')
print('Body replaced. New file size:', len(src))

assert '[GC FRAMING PLACEHOLDER]' not in src, "GC placeholder leaked!"
assert 'Who this is for' not in src, "methodology section leaked!"
print('No placeholder/methodology leak.')
