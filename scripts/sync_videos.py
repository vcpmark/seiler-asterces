#!/usr/bin/env python3
"""Pull the channel's public RSS feed and write videos.json for the page.

YouTube's Atom feed returns the 15 most recent uploads with no API key.
Run by .github/workflows/sync-videos.yml on a schedule; safe to run locally:

    python3 scripts/sync_videos.py            # fetch from YouTube
    python3 scripts/sync_videos.py feed.xml   # parse a saved feed instead
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CHANNEL_ID = "UCA-0GFM18n5SFP9ZQ51LTWQ"
HANDLE = "@secretsarelies9681"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
OUT = Path(__file__).resolve().parent.parent / "videos.json"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "seiler-asterces-site/1.0 (+github pages)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def text(el, path):
    node = el.find(path, NS)
    return (node.text or "").strip() if node is not None and node.text else ""


def parse(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    channel_title = text(root, "a:title")
    videos = []
    for entry in root.findall("a:entry", NS):
        vid = text(entry, "yt:videoId")
        if not vid:
            continue
        group = entry.find("media:group", NS)
        thumb = ""
        views = None
        description = ""
        if group is not None:
            t = group.find("media:thumbnail", NS)
            if t is not None:
                thumb = t.get("url", "")
            description = text(group, "media:description")
            stats = group.find("media:community/media:statistics", NS)
            if stats is not None and stats.get("views", "").isdigit():
                views = int(stats.get("views"))
        videos.append({
            "id": vid,
            "title": text(entry, "a:title"),
            "published": text(entry, "a:published"),
            "thumbnail": thumb,
            "views": views,
            "description": description[:400],
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    videos.sort(key=lambda v: v["published"], reverse=True)
    return {
        "channel": {
            "title": channel_title,
            "handle": HANDLE,
            "id": CHANNEL_ID,
            "url": f"https://www.youtube.com/{HANDLE}",
        },
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "videos": videos,
    }


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        raw = Path(src).read_bytes() if src else fetch(FEED_URL)
        data = parse(raw)
    except Exception as e:  # noqa: BLE001 - keep the old file if the feed is unreachable
        print(f"sync failed, keeping existing videos.json: {e}", file=sys.stderr)
        return 0 if OUT.exists() else 1

    if not data["videos"]:
        print("feed returned no videos; keeping existing videos.json", file=sys.stderr)
        return 0

    # Don't churn commits on the timestamp alone.
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text())
            if old.get("videos") == data["videos"] and old.get("channel") == data["channel"]:
                print(f"no change ({len(data['videos'])} videos)")
                return 0
        except json.JSONDecodeError:
            pass

    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.name}: {len(data['videos'])} videos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
