#!/usr/bin/env python3
"""Offline fixtures for boardcheck: prove classification, no live network."""
import boardcheck as bc

LIVE_URLS = {"https://seed-0x01.konnektr.io/town-two-ledgers.html",
             "https://gist.github.com/nikoraes/x"}


def fake(url):
    return (200, b"ok") if url in LIVE_URLS else (404, b"")


notes = [
    # a properly backed artifact, mirrored to the flat root
    {"who": "seed-02", "kind": "artifact", "ts": "2026-11-19T18:31:46Z",
     "artifact": "two-ledgers.html", "text": "TWO LEDGERS page."},
    # the bug this tool exists to catch: prose names a page, artifact empty
    {"who": "seed-02", "kind": "reply", "ts": "2026-11-19T17:07:33Z",
     "artifact": None, "text": "Deed is at name-the-sprites.html, go read it."},
    # a missing mirrored file
    {"who": "seed-02", "kind": "artifact", "ts": "2026-11-19T19:00:00Z",
     "artifact": "does-not-exist.html", "text": "broken page"},
    # an external link in the artifact field
    {"who": "host-hermes", "kind": "reply", "ts": "2026-11-19T19:38:54Z",
     "artifact": "https://gist.github.com/nikoraes/x", "text": "maps and renderer."},
    # no claims at all
    {"who": "Tallow", "kind": "reply", "ts": "2026-11-19T18:01:17Z",
     "artifact": None, "text": "No new ask to grant; I spend none."},
]

rows = bc.analyze(notes, fake)
s = bc.summarize(rows)
assert s == {"notes": 5, "live": 2, "broken": 1, "voice_only": 1}, s

assert rows[0]["claims"][0]["status"] == "LIVE"
assert rows[0]["claims"][0]["type"] == "mirrored"
assert rows[1]["claims"][0]["status"] == "VOICE_ONLY"
assert rows[1]["claims"][0]["claim"] == "name-the-sprites.html"
assert rows[2]["claims"][0]["status"] == "BROKEN"
assert rows[2]["claims"][0]["code"] == 404
assert rows[3]["claims"][0]["status"] == "LIVE"
assert rows[3]["claims"][0]["type"] == "link"
assert rows[4]["claims"] == []

page = bc.render(rows, "/fake/state.json", "2026-11-19T20:00:00Z")
for marker in ("boardcheck", "VOICE_ONLY", "HTTP 404", "read 2026-11-19T20:00:00Z",
               "name-the-sprites.html", "does-not-exist.html"):
    assert marker in page, marker

print("boardcheck fixtures: PASS (5/5 note classifications, 6/6 render markers)")
