"""
Round 16 D-2 — Set XMP + docinfo metadata on State of Cyber 2026 PDFs.

Sets Title / Author / Subject / Keywords (both XMP and legacy /Info dict)
for PDF discoverability. Reproducible: `python scripts/set-pdf-metadata.py`.
"""

from pathlib import Path
import pikepdf

REPO = Path(__file__).parent.parent
PDF_DIR = REPO / "research" / "state-of-cyber-2026"

AUTHOR = "Yohay Etsion"
SUBJECT = "Independent cybersecurity market research, 2026. Open-web sourced, zero vendor sponsors."

PDFS = {
    "irm.pdf": {
        "title": "State of Cyber 2026: Insider Risk Management",
        "keywords": "insider risk management, IRM vendors 2026, cybersecurity market research, ProductBeacon Research",
    },
    "dlp.pdf": {
        "title": "State of Cyber 2026: Data Loss Prevention",
        "keywords": "data loss prevention, DLP vendors 2026, identity-led DLP, cybersecurity market research, ProductBeacon Research",
    },
    "dspm.pdf": {
        "title": "State of Cyber 2026: Data Security Posture Management",
        "keywords": "DSPM, DSPM Absorption Chain, Cyera, Sentra, BigID, Microsoft Purview, cybersecurity market research, ProductBeacon Research",
    },
    "convergence.pdf": {
        "title": "State of Cyber 2026: Convergence Synthesis",
        "keywords": "cybersecurity convergence, DSPM Absorption Chain, Thoma Bravo Proofpoint, agentic AI data security, ProductBeacon Research",
    },
    "synthesis.pdf": {
        "title": "State of Cyber 2026: Report Digest",
        "keywords": "cybersecurity market research 2026, IRM, DLP, DSPM, convergence, report digest, ProductBeacon Research",
    },
    "pre-call-brief.pdf": {
        "title": "State of Cyber 2026: Pre-Call Briefing Pack",
        "keywords": "DSPM Absorption Chain, Thoma Bravo Proofpoint, agentic AI data security, analyst pre-read, ProductBeacon Research",
    },
    # legacy mirror of pre-call-brief.pdf (301s forward); same metadata
    "brief.pdf": {
        "title": "State of Cyber 2026: Pre-Call Briefing Pack",
        "keywords": "DSPM Absorption Chain, Thoma Bravo Proofpoint, agentic AI data security, analyst pre-read, ProductBeacon Research",
    },
}


def set_meta():
    for name, fields in PDFS.items():
        path = PDF_DIR / name
        if not path.exists():
            print(f"SKIP (not found): {path}")
            continue
        title = fields["title"]
        keywords = fields["keywords"]
        pdf = pikepdf.Pdf.open(str(path), allow_overwriting_input=True)
        # XMP metadata (modern readers + AI/search crawlers)
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = title
            meta["dc:creator"] = [AUTHOR]
            meta["dc:description"] = SUBJECT
            meta["dc:subject"] = [k.strip() for k in keywords.split(",")]
            meta["pdf:Keywords"] = keywords
        # Legacy /Info dict (older readers)
        with pdf.open_metadata():
            pass
        pdf.docinfo["/Title"] = title
        pdf.docinfo["/Author"] = AUTHOR
        pdf.docinfo["/Subject"] = SUBJECT
        pdf.docinfo["/Keywords"] = keywords
        pdf.save()
        pdf.close()
        print(f"OK: {name} -> '{title}'")


if __name__ == "__main__":
    set_meta()
