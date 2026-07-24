#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar and save normalized JSON."""
import datetime as dt
import json
import os
import re
import urllib.request
from html.parser import HTMLParser

USERNAME = os.environ.get("GH_PROFILE_USER", "Yashkush06")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.current = None
        self.in_tip = False
        self.tip = ""
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in attrs.get("class", ""):
            self.current = {"date": attrs.get("data-date"), "count": 0, "tip": ""}
        if tag == "tool-tip" and self.current is not None:
            self.in_tip = True
    def handle_data(self, data):
        if self.in_tip:
            self.tip += data
    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.current is not None:
            self.current["tip"] = self.tip.strip()
            match = re.search(r"(\d+) contribution", self.tip)
            self.current["count"] = int(match.group(1)) if match else 0
            if self.current["date"]:
                self.days.append({"date": self.current["date"], "count": self.current["count"]})
            self.current = None
            self.tip = ""
            self.in_tip = False

def streak(days):
    run = best = 0
    for day in days:
        run = run + 1 if day["count"] else 0
        best = max(best, run)
    current = 0
    for day in reversed(days[:-1] if days and not days[-1]["count"] else days):
        if not day["count"]: break
        current += 1
    return current, best

url = f"https://github.com/users/{USERNAME}/contributions"
request = urllib.request.Request(url, headers={"User-Agent": "Yashkush06-profile-art/1.0"})
with urllib.request.urlopen(request, timeout=30) as response:
    parser = CalendarParser(); parser.feed(response.read().decode("utf-8"))
days = sorted(parser.days, key=lambda x: x["date"])
if not days:
    raise SystemExit("GitHub contribution markup returned no calendar cells")
current, longest = streak(days)
payload = {
    "username": USERNAME,
    "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "range": {"start": days[0]["date"], "end": days[-1]["date"]},
    "total_contributions": sum(d["count"] for d in days),
    "current_streak": current,
    "longest_streak": longest,
    "days": days,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
print(f"saved {len(days)} days for {USERNAME}")
