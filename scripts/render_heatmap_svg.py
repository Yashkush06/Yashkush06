#!/usr/bin/env python3
"""Render contribution JSON as a self-contained animated SVG heatmap."""
import datetime as dt
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "contrib-heatmap.svg")
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 12, 3

def level(n):
    return 0 if n == 0 else 1 if n <= 5 else 2 if n <= 15 else 3 if n <= 30 else 4 if n <= 50 else 5

data = json.load(open(DATA, encoding="utf-8")); days = data["days"]
first = dt.date.fromisoformat(days[0]["date"]); lead = (first.weekday() + 1) % 7
grid = [None] * lead
for day in days: grid.append(day)
while len(grid) % 7: grid.append(None)
cols = len(grid) // 7; width = 30 + cols * (CELL + GAP) + 30; height = 30 + 20 + 7 * (CELL + GAP) + 86
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace,Menlo,monospace">', '<style>.cell{opacity:0;animation:in .45s ease-out forwards}@keyframes in{to{opacity:1;transform:translateY(0)}}}</style>', f'<rect width="100%" height="100%" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="#30363d"/><text x="{width/2}" y="20" fill="#7d8590" font-size="12" text-anchor="middle">Yashkush06@github: ~/contributions --graph</text>']
for i, day in enumerate(grid):
    if day is None: continue
    x = 30 + (i // 7) * (CELL + GAP); y = 38 + (i % 7) * (CELL + GAP); delay = (i // 7) * .018 + (i % 7) * .045
    parts.append(f'<rect class="cell" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{COLORS[level(day["count"])]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
total = data["total_contributions"]
parts += [f'<text x="30" y="{height-42}" fill="#39d353" font-size="13"><tspan font-weight="700">{total:,}</tspan><tspan fill="#7d8590"> contributions in the last year</tspan></text>', f'<text x="30" y="{height-20}" fill="#7d8590" font-size="12">current streak <tspan fill="#22d3ee">{data["current_streak"]} days</tspan> · longest <tspan fill="#22d3ee">{data["longest_streak"]} days</tspan></text>', '</svg>']
open(OUT, "w", encoding="utf-8").write("".join(parts)); print(f"wrote {OUT}")
