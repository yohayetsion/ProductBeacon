"""
Build the State of Cyber 2026 LAUNCH RUNBOOK (internal execution doc).
Reads the agent-workflow output JSON, adds the orchestrator's Amplification & Outreach
layer, and emits a self-contained, ProductBeacon-branded, single-scroll HTML runbook
with copy-to-clipboard blocks and persistent checkboxes. noindex (internal).
"""
import json, html, pathlib, base64

_icon = pathlib.Path("G:/My Drive/Claude/brand-assets/productbeacon-icon.png")
FAVICON = (f'<link rel="icon" type="image/png" href="data:image/png;base64,'
           f'{base64.b64encode(_icon.read_bytes()).decode()}">') if _icon.exists() else ""

OUT_JSON = r"C:\Users\yohay\AppData\Local\Temp\claude\G--My-Drive-Claude\45b5131b-c5ec-4b2c-be40-6a6100a5b4ec\tasks\w3o9rmp8g.output"
HERE = pathlib.Path(__file__).parent
OUT = HERE / "launch-runbook.html"

data = json.loads(pathlib.Path(OUT_JSON).read_text(encoding="utf-8"))["result"]
posts = data["posts_polished"]
sequence = data["sequence"]
networks = data["networks"]
go_live = data["go_live"]
asset_map = data["asset_map"]
metrics = data["metrics"]

LANDING = "https://productbeacon.agency/research/state-of-cyber-2026/"

# --- Orchestrator layer: Amplification & Outreach (per-person, researched) ---
DSPM = LANDING + "dspm.html"
DLP = LANDING + "dlp.html"
CONV = LANDING + "convergence.html"

amp_principle = ("Curated, warm, value-first. No mass email, no templated DMs, nothing that reads as a sell for THIS asset. "
                 "Quality over volume: a handful of high-signal, personalized touches beats a list blast and protects the "
                 "impartial-author positioning the whole report rests on. Every name below is verified current as of the launch; "
                 "channel is LinkedIn DM unless noted. Send from your personal account, spaced out, not in one burst.")

ciso_note = ("CISOs are parked, not dropped. Recommendation: hold CISO outreach until the report has visible social proof "
             "(reshares, an analyst pickup) in week 2 to 3, then reach a small number of warm ones 1:1, individually timed. "
             "Cold CISO DMs during launch week read as a sell and convert worst. Say the word and I will build that list when the timing is right.")

# Send-safety guidance — verified against 2026 LinkedIn limits
send_safety_intro = ("You have LinkedIn Premium, so you can message most of these directly without waiting to connect. On each "
    "profile, check the message button first, then pick the route. This is safe regardless: ten personalized, hand-sent messages "
    "are far below every 2026 limit. Restrictions come from automation and hundreds of identical blasts, not this.")
send_safety_items = [
    "Button says \"Free Message\" (they have Open Profile on): send the full message with the link directly, right now. Free, no credit, no connection needed. Premium allows this at scale, so use it wherever it appears.",
    "Button says \"InMail\": it costs one credit (your allotment by tier: Premium Career 5/mo, Business 15/mo, Sales Navigator 50/mo; unused roll over up to 3x). Spend credits on the highest-value targets.",
    "No credits left, or you prefer the free route: send the SHORT connection request note (in each card, no link, under the ~300-char invite cap), then send the full message with the link once they accept.",
    "Relationship vs one-shot: a connection means they see your launch posts and future content; an InMail is a single touch. For people you want an ongoing tie with, connecting is still worth it. You can also InMail now and connect after they reply.",
    "Pace a few per day across the launch window, keep each one personalized (they already are), and send manually. No automation tools, that is what actually gets accounts restricted.",
    "Warm-up tip for the analysts and newsletter authors: like or comment on a recent post of theirs first, so your name is familiar.",
]

# Step-1 connection request notes (<= ~300 chars, NO link, personalized) — keyed by name
connect_notes = {
    "Nishant Doshi": "Hi Nishant, I just published independent, fully cited research on the 2026 data security markets, and Cyberhaven features in the DLP chapter (the lineage thesis and the ramp past $1B). I'd like to connect and share it directly, and fix anything that reads as off.",
    "Yoav Regev": "Hi Yoav, I just published independent, fully cited research on the 2026 data security markets. Sentra sits in the DSPM chapter, in the standalone cluster with Cyera and BigID. I'd like to connect and send it over, and correct anything I got wrong.",
    "Mohit Tiwari": "Hi Mohit, I just published independent research on the 2026 data security markets. Symmetry features in the agentic-AI section as one of three architectural responses moving enforcement to the data layer. I'd like to connect and share it, and fix anything I mischaracterized.",
    "Dimitri Sirota": "Hi Dimitri, I just published independent, fully cited research on the 2026 data security markets. BigID features in the DSPM chapter, in the standalone cluster with Cyera and Sentra. I'd like to connect and send it over, and correct anything that's off.",
    "Karthik Krishnan": "Hi Karthik, I just published independent, fully cited research on the 2026 data security markets, and Concentric AI is named in the DSPM chapter. I'd like to connect and share it directly, and fix anything that reads as inaccurate.",
    "Pranava Adduri": "Hi Pranava, I just published independent, fully cited research on the 2026 data security markets, and Bedrock features in the DSPM chapter. I'd like to connect and send it over to you and Bruno, and correct anything I got wrong.",
    "Francis Odum": "Hi Francis, I've followed your SACR work on the DSPM, DLP, and ITDR convergence. I just published an independent, fully cited read of the same 2026 markets (the absorption chain, the Thoma Bravo stack). I'd love to connect and compare notes, no ask.",
    "Ross Haleliuk": "Hi Ross, long-time Venture in Security reader. I just published an independent, fully cited analysis of the 2026 data security markets, ten falsifiable Pattern Claims across IRM, DLP, and DSPM. I'd like to connect and share it, no ask either way.",
    "Heidi Shey": "Hi Heidi, I've read your Forrester data security work for years, the DLP concept-versus-control framing especially. I just published an independent, fully cited read of the 2026 IRM, DLP, and DSPM markets. I'd like to connect and share it as a data point.",
    "Richard Stiennon": "Hi Richard, given IT-Harvest tracks the whole vendor landscape, I thought this might interest you. I just published an independent, fully cited analysis of the 2026 data security markets, heavy on the M&A. I'd like to connect and share it, no ask.",
}

# Tagging guidance — verified mechanics + Social Media Manager / Growth Marketer consensus
tagging = {
    "verdict": ("Tag ONLY your own @ProductBeacon Page, in the first comment next to the link. Never tag the analyzed vendors "
                "or AXIA. 0 to 1 tags per post. Vendor and analyst reach comes from the founder DMs (they reshare from their own "
                "account), not from tags."),
    "do": [
        "Tag @ProductBeacon in the FIRST COMMENT of Post 1, right next to the report link. It is your own Page and a guaranteed engager, so it is a clean positive signal and it wires the post to the ~24h company-page repost.",
        "Optional on Posts 2 to 4, but do NOT repeat the same tag mechanically on all four (the Authenticity Update reads templated tagging as spam). Use it where it feels natural, skip it otherwise.",
        "Tag ONE human (an analyst or newsletter author) only if they have already confirmed by DM that they will engage. Put it in the body, paired with one line of genuine commentary addressed to them. Otherwise tag nobody.",
    ],
    "dont": [
        "Do NOT tag the six analyzed vendor Pages (Cyberhaven, Sentra, Symmetry, BigID, Concentric, Bedrock) anywhere. It looks like courting the vendors you graded, and a Page that ignores the tag is a reach-negative signal. Their amplification runs through the founder DM layer instead.",
        "Do NOT tag AXIA. It telegraphs the conflict an impartial report must not broadcast.",
        "Do NOT stack tags to chase reach, and never bare-tag without commentary. More ignored tags = less reach, not more.",
    ],
    "howto": [
        "Compose the post body first, with no tags and no link, so the writing stands on its own.",
        "Publish, then add the first comment: the report link plus, on Post 1, @ProductBeacon. Type @, type the name, WAIT for the dropdown, and SELECT the Page (confirm it is the Page, not a person).",
        "Verify the mention rendered as a blue clickable link before you leave. Grey text means the selection did not register and no notification fires; redo it.",
        "The company-page repost ~24h later rides the same thread, no new tags needed.",
    ],
    "why": ("The reach play and the positioning play point the same way: a vendor founder resharing from their own account moves far "
            "more reach than a Page tag nobody acts on, AND it is the strongest third-party endorsement for an author with receipts. "
            "Your scarcest asset is perceived neutrality. Tag your own house, work the vendors privately, let the claims stand naked."),
}

# group, name, role, company, channel, linkedin, mention (their specific report appearance), copy, url
people = [
    {"group": "vendors", "name": "Nishant Doshi", "role": "CEO", "company": "Cyberhaven",
     "linkedin": "https://www.linkedin.com/in/nishantdoshi/", "channel": "LinkedIn DM",
     "mention": "DLP chapter: the Cyberhaven lineage thesis and the Series C-to-D ramp past a $1B valuation; also on the convergence map.",
     "url": DLP, "url_label": "DLP chapter",
     "copy": ("Hi Nishant, I published an independent research report on the 2026 data security markets this week, 280 cited sources, "
              "no sponsors. Cyberhaven features in the DLP chapter, including the lineage thesis and the Series C-to-D ramp past a "
              "$1B valuation, and on the convergence map. I wanted to give you a direct heads-up rather than have you find it "
              "secondhand. If anything about Cyberhaven reads as inaccurate, tell me and I will fix it.\n\n" + DLP)},
    {"group": "vendors", "name": "Yoav Regev", "role": "CEO & Co-Founder", "company": "Sentra",
     "linkedin": "https://www.linkedin.com/in/yoav-regev-31718a1/", "channel": "LinkedIn DM",
     "mention": "DSPM chapter: the standalone-DSPM cluster alongside Cyera and BigID; the DSPM-to-data-security-platform arc.",
     "url": DSPM, "url_label": "DSPM chapter",
     "copy": ("Hi Yoav, I just published independent research on the 2026 data security markets, 280 citations, no vendor sponsors. "
              "Sentra sits in the DSPM chapter, in the standalone cluster alongside Cyera and BigID, and your DSPM-to-platform arc is "
              "part of how I frame the market. Sending a direct heads-up, and if I got anything about Sentra wrong, tell me and I "
              "will correct it.\n\n" + DSPM)},
    {"group": "vendors", "name": "Mohit Tiwari", "role": "CEO & Co-Founder", "company": "Symmetry Systems",
     "linkedin": "https://www.linkedin.com/in/mohit-tiwari8/", "channel": "LinkedIn DM",
     "mention": "Agentic-AI Pattern Claim: named as one of three architectural responses moving enforcement to the data layer (your Identity x Data Graph binding agent identities to data access at the storage layer). The strongest, most favorable mention of the set.",
     "url": DSPM, "url_label": "DSPM chapter (agentic claim)",
     "copy": ("Hi Mohit, I published independent research on the 2026 data security markets this week. Symmetry features in the "
              "agentic-AI section as one of three architectural responses moving enforcement to the data layer, your Identity and "
              "Data Graph binding agent identities to data access at the storage layer. I wanted to flag it directly. If I have "
              "mischaracterized anything, tell me and I will fix it.\n\n" + DSPM)},
    {"group": "vendors", "name": "Dimitri Sirota", "role": "CEO & Co-Founder", "company": "BigID",
     "linkedin": "https://www.linkedin.com/in/dimitrisirota", "channel": "LinkedIn DM",
     "mention": "DSPM chapter: the standalone cluster with Cyera and Sentra; also a participant in the DLP convergence.",
     "url": DSPM, "url_label": "DSPM chapter",
     "copy": ("Hi Dimitri, I just published an independent, fully cited read of the 2026 data security markets, no sponsors. BigID "
              "features in the DSPM chapter, in the standalone cluster with Cyera and Sentra, and as a participant in the DLP "
              "convergence. A direct heads-up rather than secondhand. If anything about BigID is off, tell me and I will correct "
              "it.\n\n" + DSPM)},
    {"group": "vendors", "name": "Karthik Krishnan", "role": "CEO & Founder", "company": "Concentric AI",
     "linkedin": "https://www.linkedin.com/in/kkrishnan/", "channel": "LinkedIn DM",
     "mention": "DSPM chapter: named in the DSPM vendor set.",
     "url": DSPM, "url_label": "DSPM chapter",
     "copy": ("Hi Karthik, I published independent research on the 2026 data security markets this week, 280 cited sources and no "
              "vendor sponsors. Concentric AI is named in the DSPM chapter. I wanted to give you a direct heads-up. If anything "
              "about Concentric reads as inaccurate, tell me and I will fix it.\n\n" + DSPM)},
    {"group": "vendors", "name": "Pranava Adduri", "role": "Co-Founder & CTO (CEO: Bruno Kurtic)", "company": "Bedrock Security",
     "linkedin": "https://www.linkedin.com/in/padduri", "channel": "LinkedIn DM",
     "mention": "DSPM chapter: named in the DSPM vendor set (Bedrock Data).",
     "url": DSPM, "url_label": "DSPM chapter",
     "copy": ("Hi Pranava, I just published independent research on the 2026 data security markets, fully cited, no sponsors. "
              "Bedrock features in the DSPM chapter. Sending a direct heads-up to you and Bruno rather than have it surface "
              "secondhand. If I got anything about Bedrock wrong, tell me and I will correct it.\n\n" + DSPM)},

    {"group": "analysts", "name": "Francis Odum", "role": "Founder, Software Analyst Cyber Research (SACR)", "company": "Independent analyst + newsletter",
     "linkedin": "https://www.linkedin.com/in/francis-odum-0a8673100", "channel": "LinkedIn DM or Substack (softwareanalyst.substack.com)",
     "mention": "Best-fit target: his SACR research explicitly covers the DSPM / DLP / ITDR convergence, exactly this report's thesis.",
     "url": LANDING, "url_label": "report landing",
     "copy": ("Hi Francis, I have followed your SACR work on the DSPM, DLP, and ITDR convergence, some of the sharpest in the space. "
              "I just published an independent, fully cited read of the same 2026 markets, including the DSPM absorption chain (six "
              "platform absorbs in fourteen months against Cyera's $9B) and the Thoma Bravo data security stack. Sharing as a data "
              "point, no ask, and curious whether your read of the absorption-versus-standalone split matches mine.\n\n" + LANDING)},
    {"group": "analysts", "name": "Ross Haleliuk", "role": "Author, Venture in Security (21K+ subs); Head of Product, LimaCharlie", "company": "Newsletter heavyweight",
     "linkedin": "https://www.linkedin.com/in/rosshaleliuk", "channel": "LinkedIn DM",
     "mention": "Top cyber-business newsletter; a single mention is outsized reach into founders and investors.",
     "url": LANDING, "url_label": "report landing",
     "copy": ("Hi Ross, long-time Venture in Security reader. I just published an independent, fully cited analysis of the 2026 data "
              "security markets, ten falsifiable Pattern Claims across IRM, DLP, and DSPM (the absorption chain, the Thoma Bravo "
              "stack, agentic AI moving enforcement to the data layer). If any of it is useful for the newsletter it is open access "
              "with the citations underneath, and I am happy to walk through the methodology. No ask either way.\n\n" + LANDING)},
    {"group": "analysts", "name": "Heidi Shey", "role": "Principal Analyst, Forrester (leads data security: DLP, DSPM, data security platforms)", "company": "Forrester",
     "linkedin": "https://www.linkedin.com/in/heidishey", "channel": "LinkedIn (she is active there; formal briefings are gated by Forrester)",
     "mention": "Forrester's data security lead; her DLP concept-versus-control framing is well known. Value-first, not a briefing request.",
     "url": LANDING, "url_label": "report landing",
     "copy": ("Hi Heidi, I have read your Forrester data security work for years, the DLP concept-versus-control framing especially. "
              "I just published an independent, fully cited read of the 2026 IRM, DLP, and DSPM markets. Sharing it as a data point, "
              "not a briefing request, and I would value your view on the DSPM absorption-versus-standalone split if you ever have a "
              "moment.\n\n" + LANDING)},
    {"group": "analysts", "name": "Richard Stiennon", "role": "Chief Research Analyst, IT-Harvest (tracks 3,300+ cyber vendors); Forbes contributor", "company": "IT-Harvest",
     "linkedin": "https://www.linkedin.com/in/stiennon", "channel": "LinkedIn DM",
     "mention": "Tracks the entire vendor landscape and loves M&A data, a strong fit for the report's acquisition-heavy spine.",
     "url": LANDING, "url_label": "report landing",
     "copy": ("Hi Richard, given IT-Harvest tracks the full vendor landscape, I thought this might be useful. I published an "
              "independent, fully cited analysis of the 2026 data security markets, heavy on the M&A: the DSPM absorption chain (six "
              "absorbs in fourteen months), the Cyera $9B counter-thesis, and the Thoma Bravo Proofpoint-plus-Forcepoint stack. Open "
              "access with citations. Sharing as a data point, no ask.\n\n" + LANDING)},
]

def esc(s):
    return html.escape(str(s))

def copyblock(text, label="Copy"):
    t = esc(text)
    return (f'<div class="copywrap"><button class="copybtn" onclick="cp(this)">{label}</button>'
            f'<pre class="copy">{t}</pre></div>')

# ---------- build sections ----------
def post_card(p):
    chap = p["link_target"]
    parts = [f'<div class="card post" id="post{p["n"]}">']
    parts.append(f'<div class="post-head"><span class="pill">STEP</span><h3>{esc(p["label"])}</h3></div>')
    parts.append('<div class="meta-row">'
                 f'<span class="meta"><b>When</b> {esc(p["timing"])}</span>'
                 f'<span class="meta"><b>Channel</b> {esc(p["channel"])}</span>'
                 f'<span class="meta"><b>OG card</b> {esc(p["og_card"])}</span>'
                 '</div>')
    parts.append('<div class="lbl">The action</div>')
    parts.append(f'<p class="action">Publish from your personal LinkedIn. The body has <b>no link</b> '
                 f'(protects reach); the chapter URL goes in the <b>first comment</b> the moment it is live.</p>')
    parts.append('<div class="lbl">Post text <span class="hint">(copy-paste, em-dash-free)</span></div>')
    parts.append(copyblock(p["body"]))
    parts.append('<div class="lbl">First comment <span class="hint">(paste immediately after posting)</span></div>')
    parts.append(copyblock(p["first_comment"]))
    if p["n"] == 1:
        parts.append('<div class="mentionnote">&#43; In this same first comment, also <b>@-mention ProductBeacon</b>: '
                     'type <code>@ProductBeacon</code> and <b>select the Page from the dropdown</b> so it turns blue '
                     '(typed or pasted text alone will not register). Not redundant with the link: the URL routes readers, '
                     'the mention notifies the Page, creates the entity link, and powers the ~24h repost. '
                     'Optional on later posts, but do not repeat it mechanically on all four.</div>')
    parts.append('<div class="lbl">PB company-page repost <span class="hint">(we-voice, ~24h later)</span></div>')
    parts.append(copyblock(p["pb_repost"]))
    parts.append('<div class="lbl">Hashtags</div>')
    parts.append(copyblock(p["hashtags"]))
    parts.append('<div class="assets">'
                 f'<b>Asset to use</b> &nbsp; Link target: <a href="{esc(chap)}">{esc(chap)}</a> '
                 f'&middot; OG card: <code>research/og/{esc(p["og_card"])}</code></div>')
    parts.append('</div>')
    return "\n".join(parts)

def seq_rows():
    # Forward actions only — drop the Pre-launch rows (already done this session).
    rows = []
    for s in sequence:
        if s["phase"].startswith("Pre-launch"):
            continue
        rows.append(f'<tr><td class="when">{esc(s["when"])}</td><td><span class="phase">{esc(s["phase"])}</span></td>'
                    f'<td>{esc(s["action"])}</td><td class="ch">{esc(s["channel"])}</td></tr>')
    return "\n".join(rows)

def done_items():
    # These were completed THIS session — shown as confirmed, not as to-dos.
    out = []
    for g in go_live:
        out.append(f'<li class="dn">{esc(g["item"])}</li>')
    return "\n".join(out)

def tagging_card():
    def li(items, cls):
        return "".join(f'<li class="{cls}">{esc(x)}</li>' for x in items)
    return ('<div class="card tagcard">'
            '<div class="post-head"><span class="pill">TAGGING</span><h3>Tagging company Pages &mdash; the right way</h3></div>'
            f'<p class="action"><b>Verdict:</b> {esc(tagging["verdict"])}</p>'
            '<div class="taggrid">'
            f'<div class="tagcol do"><div class="lbl">Do</div><ul class="tl">{li(tagging["do"],"ok")}</ul></div>'
            f'<div class="tagcol dont"><div class="lbl">Don\'t</div><ul class="tl">{li(tagging["dont"],"no")}</ul></div>'
            '</div>'
            f'<div class="lbl">How to tag</div><ol class="howto">{"".join(f"<li>{esc(s)}</li>" for s in tagging["howto"])}</ol>'
            f'<p class="why" style="margin-top:12px"><b>Why:</b> {esc(tagging["why"])}</p>'
            '</div>')

def person_cards(group):
    out = []
    for p in [x for x in people if x["group"] == group]:
        pill = "alt" if group == "vendors" else "alt2"
        out.append('<div class="card amp">')
        out.append(f'<div class="post-head"><span class="pill {pill}">{esc(p["company"])}</span>'
                   f'<h3>{esc(p["name"])}</h3></div>')
        out.append('<div class="meta-row">'
                   f'<span class="meta"><b>Role</b> {esc(p["role"])}</span>'
                   f'<span class="meta"><b>Channel</b> {esc(p["channel"])}</span>'
                   f'<span class="meta"><b>Profile</b> <a href="{esc(p["linkedin"])}">{esc(p["linkedin"].split("//")[-1])}</a></span>'
                   '</div>')
        out.append(f'<p class="why"><b>In the report:</b> {esc(p["mention"])}</p>')
        cn = connect_notes.get(p["name"], "")
        n = len(cn)
        out.append('<div class="lbl">Full message <span class="hint">(with link &middot; send via Free Message / InMail, or after they accept)</span></div>')
        out.append(copyblock(p["copy"]))
        out.append(f'<div class="lbl">Connection request note <span class="hint">(free route &middot; no link &middot; {n}/300 chars)</span></div>')
        out.append(copyblock(cn))
        out.append(f'<div class="assets"><b>How</b> &nbsp; open <a href="{esc(p["linkedin"])}">{esc(p["name"])} on LinkedIn</a> '
                   f'&rarr; if the button says <b>Free Message</b>, send the full message; if <b>InMail</b>, spend a credit or '
                   f'send the connection note and message after they accept &middot; link: <a href="{esc(p["url"])}">{esc(p["url_label"])}</a></div>')
        out.append('</div>')
    return "\n".join(out)

def network_cards():
    out = []
    for nw in networks:
        out.append('<div class="card net">')
        out.append(f'<div class="post-head"><span class="pill alt2">PROFILE</span><h3>{esc(nw["name"])}</h3></div>')
        out.append(f'<p class="action"><b>Where to update:</b> {esc(nw["update_location"])}</p>')
        out.append('<div class="lbl">Suggested profile text <span class="hint">(copy-paste)</span></div>')
        out.append(copyblock(nw["suggested_text"]))
        out.append(f'<div class="assets"><b>Asset</b> &nbsp; {esc(nw["asset"])}</div>')
        out.append(f'<p class="rate">{esc(nw["rate_note"])}</p>')
        out.append('</div>')
    return "\n".join(out)

def metric_items():
    h72 = [m for m in metrics if m.startswith("First 72h")]
    w4 = [m for m in metrics if m.startswith("First 4 weeks")]
    def li(items):
        return "\n".join(f'<li>{esc(m.split("—",1)[1].strip())}</li>' for m in items)
    return (f'<h4>First 72 hours</h4><ul>{li(h72)}</ul>'
            f'<h4>First 4 weeks</h4><ul>{li(w4)}</ul>')

HTMLDOC = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
{FAVICON}
<title>State of Cyber 2026 — Launch Runbook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0F172A;--bg2:#111c33;--card:#16223b;--card2:#1b2942;--bd:rgba(148,163,184,.18);
--amber:#F59E0B;--amber2:#FBBF24;--tx:#E8EEF7;--mut:#94A3B8;--mut2:#64748B;}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--tx);line-height:1.55;
background-image:radial-gradient(900px 500px at 80% -10%,rgba(245,158,11,.08),transparent);}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 22px 120px}}
header.top{{padding:56px 0 30px;border-bottom:1px solid var(--bd)}}
.kicker{{font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--amber)}}
h1{{font-size:42px;font-weight:800;letter-spacing:-.02em;margin:12px 0 8px;line-height:1.08}}
.sub{{color:var(--mut);font-size:18px;max-width:760px}}
.tagrow{{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}}
.tag{{font-family:'JetBrains Mono',monospace;font-size:12px;padding:6px 12px;border:1px solid rgba(245,158,11,.35);
border-radius:6px;color:var(--amber2);background:rgba(245,158,11,.08)}}
nav.toc{{position:sticky;top:0;z-index:50;background:rgba(15,23,42,.86);backdrop-filter:blur(12px);
border-bottom:1px solid var(--bd);margin:0 -22px 0;padding:12px 22px;display:flex;gap:8px;flex-wrap:wrap}}
nav.toc a{{font-size:13px;color:var(--mut);text-decoration:none;padding:5px 11px;border-radius:6px;border:1px solid transparent}}
nav.toc a:hover{{color:var(--tx);border-color:var(--bd);background:var(--card)}}
section{{padding:42px 0 8px;border-bottom:1px solid var(--bd)}}
.shead{{display:flex;align-items:baseline;gap:14px;margin-bottom:6px}}
.snum{{font-family:'JetBrains Mono',monospace;color:var(--amber);font-size:15px;font-weight:700}}
h2{{font-size:27px;font-weight:800;letter-spacing:-.01em}}
.sdesc{{color:var(--mut);margin:6px 0 22px;max-width:780px}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:22px 22px 18px;margin-bottom:18px}}
.post-head{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.post-head h3{{font-size:20px;font-weight:700}}
.pill{{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:.1em;
padding:4px 9px;border-radius:5px;background:var(--amber);color:#1a1206}}
.pill.alt{{background:rgba(34,211,238,.16);color:#67e8f9;border:1px solid rgba(34,211,238,.35)}}
.pill.alt2{{background:rgba(167,139,250,.16);color:#c4b5fd;border:1px solid rgba(167,139,250,.35)}}
.meta-row{{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:14px}}
.meta{{font-size:13px;color:var(--mut)}}.meta b{{color:var(--tx);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;display:block;color:var(--mut2);margin-bottom:1px}}
.lbl{{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
color:var(--amber2);margin:16px 0 7px;font-weight:700}}
.hint{{color:var(--mut2);text-transform:none;letter-spacing:0;font-weight:500}}
.action{{color:var(--tx);font-size:15px;margin-bottom:2px}}.why{{color:var(--mut);font-size:14px;margin-top:8px}}
.copywrap{{position:relative}}
pre.copy{{font-family:Inter,sans-serif;white-space:pre-wrap;background:var(--bg2);border:1px solid var(--bd);
border-radius:10px;padding:15px 16px;font-size:14.5px;color:#dbe4f0;line-height:1.6}}
.copybtn{{position:absolute;top:9px;right:9px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;
letter-spacing:.06em;background:var(--amber);color:#1a1206;border:none;border-radius:6px;padding:5px 11px;cursor:pointer;z-index:2}}
.copybtn:hover{{background:var(--amber2)}}.copybtn.done{{background:#22c55e;color:#06210f}}
.assets{{margin-top:14px;font-size:13.5px;color:var(--mut);background:var(--bg2);border-radius:9px;padding:11px 14px;border:1px solid var(--bd)}}
.assets b{{color:var(--amber2)}}.assets a{{color:#7dd3fc;word-break:break-all}}.assets code{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#cbd5e1}}
.rate{{margin-top:11px;font-size:13px;color:var(--amber2);background:rgba(245,158,11,.07);border-left:3px solid var(--amber);padding:8px 13px;border-radius:0 7px 7px 0}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{text-align:left;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;
color:var(--mut2);padding:9px 12px;border-bottom:1px solid var(--bd)}}
td{{padding:11px 12px;border-bottom:1px solid var(--bd);vertical-align:top;color:var(--tx)}}
td.when{{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--mut);white-space:nowrap}}
td.ch{{color:var(--mut);font-size:13px;white-space:nowrap}}
.phase{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--amber2);background:rgba(245,158,11,.1);padding:2px 8px;border-radius:5px}}
.check{{display:flex;gap:12px;align-items:flex-start;padding:13px 15px;background:var(--card);border:1px solid var(--bd);
border-radius:10px;margin-bottom:9px;cursor:pointer}}
.check input{{margin-top:4px;width:17px;height:17px;accent-color:var(--amber);flex:none}}
.check .confirm{{color:var(--mut);font-size:13px;font-weight:400}}
.callout{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.3);border-radius:12px;padding:16px 19px;margin-bottom:20px;font-size:15px;color:#f8e9cf}}
.callout b{{color:var(--amber2)}}
.callout.safe{{background:rgba(34,197,94,.07);border-color:rgba(34,197,94,.3);color:#d7f5e1}}
.callout.safe b{{color:#86efac}}
.safelist{{margin:10px 0 0;list-style:none}}
.safelist li{{padding:6px 0 6px 22px;position:relative;font-size:13.5px;color:#d7f5e1;border-bottom:1px solid rgba(148,163,184,.1)}}
.safelist li::before{{content:'';position:absolute;left:3px;top:13px;width:7px;height:7px;background:#22c55e;border-radius:2px}}
ul{{margin:6px 0 18px 2px;list-style:none}}ul li{{padding:7px 0 7px 22px;position:relative;color:var(--tx);font-size:14.5px;border-bottom:1px solid rgba(148,163,184,.08)}}
ul li::before{{content:'';position:absolute;left:2px;top:15px;width:7px;height:7px;background:var(--amber);border-radius:2px}}
h4{{font-family:'JetBrains Mono',monospace;font-size:13px;letter-spacing:.06em;color:var(--amber2);margin:18px 0 4px;text-transform:uppercase}}
.foot{{padding:34px 0 0;color:var(--mut2);font-size:13px}}
.note{{color:var(--mut);font-size:13.5px;margin:-6px 0 20px}}
.grouphead{{font-size:19px;font-weight:700;margin:26px 0 4px;display:flex;align-items:center;gap:11px}}
.gtag{{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:.06em;color:var(--amber2);
background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);padding:3px 9px;border-radius:5px}}
.amp .post-head h3{{font-size:19px}}
.mentionnote{{margin:9px 0 2px;font-size:13px;color:#f8e9cf;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.28);border-radius:9px;padding:10px 13px}}
.mentionnote code{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#fde68a;background:rgba(0,0,0,.25);padding:1px 5px;border-radius:4px}}
.tagcard{{border-color:rgba(245,158,11,.32);background:linear-gradient(180deg,rgba(245,158,11,.05),var(--card))}}
.taggrid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:6px}}
.tl{{margin:0;list-style:none}}.tl li{{padding:7px 0 7px 24px;position:relative;font-size:13.5px;border-bottom:1px solid rgba(148,163,184,.08);color:var(--tx)}}
.tl li::before{{position:absolute;left:2px;top:7px;font-weight:800;background:none;width:auto;height:auto;content:''}}
.tl li.ok::before{{content:'\\2713';color:#22c55e}}.tl li.no::before{{content:'\\2715';color:#f87171}}
ol.howto{{margin:4px 0 4px 18px;padding:0}}ol.howto li{{padding:5px 0 5px 6px;font-size:13.5px;color:var(--tx);border-bottom:1px solid rgba(148,163,184,.08)}}
@media(max-width:640px){{.taggrid{{grid-template-columns:1fr}}}}
.donebanner{{background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.28);border-radius:14px;padding:18px 22px;margin:26px 0 4px}}
.dh{{display:flex;align-items:center;gap:11px;font-size:17px;font-weight:700;color:#86efac}}
.dchk{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:#22c55e;color:#06210f;font-size:15px;font-weight:800;flex:none}}
.dnote{{color:var(--mut);font-size:13.5px;margin:8px 0 12px}}
.donelist{{margin:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:2px 22px}}
.donelist li.dn{{padding:5px 0 5px 22px;position:relative;color:var(--mut);font-size:13px;border:none}}
.donelist li.dn::before{{content:'\\2713';position:absolute;left:0;top:5px;color:#22c55e;font-weight:800;background:none;width:auto;height:auto}}
@media(max-width:640px){{.donelist{{grid-template-columns:1fr}}}}
</style></head>
<body><div class="wrap">

<header class="top">
  <div class="kicker">ProductBeacon Research &middot; Internal Launch Runbook</div>
  <h1>State of Cyber 2026 — Launch Action Plan</h1>
  <p class="sub">Step by step: each move, the exact copy to paste, and the asset to attach. Built by the product-marketing,
  copy, business-development, and operations agents. The report is live; this is the execution layer.</p>
  <div class="tagrow"><span class="tag">4 POSTS + REPOSTS</span><span class="tag">4 OUTREACH LAYERS</span>
  <span class="tag">5 EXPERT NETWORKS</span><span class="tag">EM-DASH-FREE</span><span class="tag">RATE HELD $800/HR</span></div>
</header>

<nav class="toc">
  <a href="#timeline">1 · Timeline</a>
  <a href="#posts">2 · The posts</a>
  <a href="#amp">3 · Amplification</a>
  <a href="#networks">4 · Expert networks</a>
  <a href="#metrics">5 · Metrics</a>
</nav>

<section id="timeline">
  <div class="shead"><span class="snum">01</span><h2>What to do next — the launch sequence</h2></div>
  <p class="sdesc">Forward actions only (the prep above is closed). Posts run Tuesdays from your personal account; the PB company page reposts ~24h later. Expert networks and vendor outreach run in parallel. <b>First action: publish Post 1.</b></p>
  <div class="card" style="padding:6px 6px 2px">
  <table><thead><tr><th>When</th><th>Phase</th><th>Action</th><th>Channel</th></tr></thead>
  <tbody>{seq_rows()}</tbody></table></div>
</section>

<section id="posts">
  <div class="shead"><span class="snum">02</span><h2>The four posts</h2></div>
  <p class="sdesc">Post 1 launches the report; Posts 2 to 4 are the Pattern Claims, one per week. Each card has the post body, the first-comment link, the PB we-voice repost, hashtags, and the exact asset.</p>
  {"".join(post_card(p) for p in posts)}
</section>

<section id="amp">
  <div class="shead"><span class="snum">03</span><h2>Amplification &amp; outreach <span class="hint" style="font-size:15px">— 10 named people, per-person copy</span></h2></div>
  <p class="sdesc">Beyond the organic posts: a small, curated, warm layer of 1:1 engagement. Each person is researched and current; the message is written for them and cites their specific appearance in the report. Send from your personal account, spaced out.</p>
  <div class="callout"><b>Operating rule.</b> {esc(amp_principle)}</div>
  <div class="callout safe"><b>Will this get my account flagged? No.</b> {esc(send_safety_intro)}
    <ul class="safelist">{"".join(f"<li>{esc(x)}</li>" for x in send_safety_items)}</ul>
  </div>

  <h3 class="grouphead">Vendors &middot; factual heads-up <span class="gtag">6 people</span></h3>
  <p class="note">A heads-up that you cited them, plus a correction offer. This lands as research, not promotion, and often earns a reshare from the vendor's own page. Run these around the DSPM / convergence posts (week 2 to 3). <b>Hold</b> Cyera, Varonis, and Mimecast until Guy coordinates AX-1 at AXIA.</p>
  {person_cards("vendors")}

  <h3 class="grouphead">Analysts &amp; newsletter &middot; value-first <span class="gtag">4 people</span></h3>
  <p class="note">No ask. Share as a data point against their published view; for the newsletter authors, offer the methodology walk-through. One pickup here compounds reach into the buyer and investor audience.</p>
  {person_cards("analysts")}

  <h3 class="grouphead">CISOs &middot; parked <span class="gtag">decide week 2 to 3</span></h3>
  <div class="callout" style="background:rgba(148,163,184,.08);border-color:var(--bd);color:var(--mut)">{esc(ciso_note)}</div>
</section>

<section id="networks">
  <div class="shead"><span class="snum">04</span><h2>Expert-network profile updates</h2></div>
  <p class="sdesc">Cite the published report on every network you are on. This feeds the analyst-call funnel. Profile-update only this quarter; rate stays $800/hr (re-anchor in Q4, gated on the book shipping plus a few paid calls). Field names vary by portal — labels below are the nearest-match target.</p>
  <p class="note"><b>Note:</b> you wrote "GCG" — read as <b>GLG</b>. Covering the five networks you use. Add or drop as needed.</p>
  {network_cards()}
</section>

<section id="metrics">
  <div class="shead"><span class="snum">05</span><h2>Metrics to watch</h2></div>
  <p class="sdesc">What tells you the launch is working.</p>
  <div class="card">{metric_items()}</div>
</section>

<div class="foot">
  ProductBeacon Research &middot; internal execution document (noindex) &middot; report live at
  <a href="{LANDING}" style="color:#7dd3fc">{LANDING}</a><br>
  Generated for Yohay Etsion. Em-dash ban and weekend-send block apply. No vendor outreach to Cyera / Varonis / Mimecast until Guy coordinates AX-1 at AXIA.
</div>

</div>
<script>
function cp(b){{const t=b.parentNode.querySelector('pre.copy').innerText;
navigator.clipboard.writeText(t).then(()=>{{const o=b.textContent;b.textContent='Copied';b.classList.add('done');
setTimeout(()=>{{b.textContent=o;b.classList.remove('done')}},1400)}})}}
document.querySelectorAll('.check input').forEach(c=>{{const k='soc-rb-'+c.dataset.k;
c.checked=localStorage.getItem(k)==='1';c.addEventListener('change',()=>localStorage.setItem(k,c.checked?'1':'0'))}});
</script>
</body></html>"""

OUT.write_text(HTMLDOC, encoding="utf-8")
print("wrote", OUT, f"({OUT.stat().st_size} bytes)")
