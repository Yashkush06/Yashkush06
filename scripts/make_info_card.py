#!/usr/bin/env python3
"""Generate Yash's animated terminal-style profile card."""
import html, os
rows = [("Focus", "AI systems + full-stack"), ("Build", "Multi-agent orchestration"), ("Local", "Privacy-first, on-device AI"), ("Stack", "Python · TypeScript · React"), ("Explore", "LLMs · real-time · edge AI")]
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="480" height="210" viewBox="0 0 480 210" font-family="ui-monospace,Menlo,monospace">', '<style>.row{opacity:0;animation:show .4s ease-out forwards}@keyframes show{to{opacity:1;transform:translateY(0)}}}</style>', '<rect width="100%" height="100%" rx="12" fill="#0d1117"/><rect x=".5" y=".5" width="479" height="209" rx="12" fill="none" stroke="#30363d"/><text x="240" y="24" text-anchor="middle" fill="#7d8590" font-size="12">yash@github: ~$ neofetch</text>']
for i, (key, val) in enumerate(rows):
    y = 58 + i * 28
    parts.append(f'<g class="row" style="animation-delay:{i*.1:.2f}s" transform="translate(0,5)"><text x="22" y="{y}" fill="#ffa657" font-size="13" font-weight="700">{html.escape(key)}</text><text x="112" y="{y}" fill="#c9d1d9" font-size="13">{html.escape(val)}</text></g>')
parts.append('</svg>'); open(os.path.join(os.path.dirname(__file__), "..", "info-card.svg"), "w", encoding="utf-8").write("".join(parts))
