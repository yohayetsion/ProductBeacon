#!/usr/bin/env python
"""Assert the site's JSON-LD forms one coherent entity graph.

Written 2026-08-31 after a string-match repair gave one identifier four types.
The publisher fix was applied by matching `"name": "ProductBeacon Research"`,
which appears in Organization, ListItem, WebSite and CollectionPage nodes, so
`.../research/#productbeacon-research` resolved to all four at once. Reading the
diff would not have caught it. Parsing does.

Run from the repo root:  python scripts/check-structured-data.py
Exit code 0 = clean, 1 = at least one failure.
"""
import collections
import io
import json
import os
import re
import subprocess
import sys

PRIVATE = ("prospects/", "planning/", "analysis/", "Product/", "Marketing/", "internal/")
ORG_ID = "https://productbeacon.agency/#productbeacon"
PERSON_ID = "https://productbeacon.agency/#yohay-etsion"
SUPERSEDED = ("governed operator", "professional-services firms")

failures = []
passes = []


def check(ok, label, detail=""):
    (passes if ok else failures).append(label + (": " + detail if detail and not ok else ""))


def walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for value in node.values():
            walk(value, fn)
    elif isinstance(node, list):
        for value in node:
            walk(value, fn)


def main():
    tracked = subprocess.run(["git", "ls-files", "*.html"], capture_output=True, text=True).stdout.split()
    files = [f for f in tracked if not f.startswith(PRIVATE)]

    types_by_id = collections.defaultdict(set)
    pages_by_id = collections.defaultdict(set)
    blocks = invalid = 0

    for path in files:
        html = io.open(path, encoding="utf-8", errors="ignore").read()
        for raw in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html):
            blocks += 1
            try:
                data = json.loads(raw)
            except Exception as error:
                invalid += 1
                failures.append("invalid JSON-LD in %s: %s" % (path, error))
                continue

            def collect(node):
                if "@id" in node and "@type" in node:
                    kind = node["@type"]
                    for one in (kind if isinstance(kind, list) else [kind]):
                        types_by_id[node["@id"]].add(one)
                        pages_by_id[node["@id"]].add(path)

            walk(data, collect)

            lowered = raw.lower()
            for phrase in SUPERSEDED:
                if phrase in lowered:
                    failures.append("superseded positioning in %s: %s" % (path, phrase))

    check(invalid == 0, "every JSON-LD block parses", "%d invalid" % invalid)

    # The assertion that would have caught the regression.
    collisions = {k: v for k, v in types_by_id.items() if len(v) > 1}
    check(not collisions, "every @id maps to exactly one @type",
          "; ".join("%s -> %s" % (k, sorted(v)) for k, v in collisions.items()))

    check(ORG_ID in types_by_id and types_by_id[ORG_ID] == {"Organization"},
          "the organisation identifier exists and is an Organization",
          str(sorted(types_by_id.get(ORG_ID, []))))
    check(PERSON_ID in types_by_id and types_by_id[PERSON_ID] == {"Person"},
          "the person identifier exists and is a Person",
          str(sorted(types_by_id.get(PERSON_ID, []))))

    # A Person node named Yohay Etsion without the shared identifier is a
    # disconnected duplicate of the same human.
    orphans = []
    for path in files:
        html = io.open(path, encoding="utf-8", errors="ignore").read()
        for raw in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html):
            try:
                data = json.loads(raw)
            except Exception:
                continue

            def find(node):
                kind = node.get("@type")
                kinds = kind if isinstance(kind, list) else [kind]
                if "Person" in kinds and node.get("name") == "Yohay Etsion" and "@id" not in node:
                    orphans.append(path)

            walk(data, find)
    check(not orphans, "every Yohay Etsion node carries the shared identifier",
          "%d orphaned on %s" % (len(orphans), sorted(set(orphans))[:4]))

    for label in passes:
        print("PASS " + label)
    for label in failures:
        print("FAIL " + label)
    print("RESULT %d passed, %d failed  (%d JSON-LD blocks across %d pages)"
          % (len(passes), len(failures), blocks, len(files)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
