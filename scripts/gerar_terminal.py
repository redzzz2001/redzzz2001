#!/usr/bin/env python3
"""Gera terminal.svg lendo frases.txt (frases separadas por ' - ')."""
from pathlib import Path
from html import escape
import hashlib
import re

ROOT = Path(__file__).resolve().parent.parent
source = (ROOT / "frases.txt").read_text(encoding="utf-8").strip()
phrases = [p.strip() for p in re.split(r"\s+-\s+", source) if p.strip()]
if not phrases:
    raise SystemExit("Adicione frases ao frases.txt, separadas por ' - '")
if any(len(p) > 35 for p in phrases):
    raise SystemExit("Cada frase deve ter no maximo 35 caracteres")

slot = 7
duration = slot * len(phrases)
char_width = 9.03
def norm(t):
    return f"{t / duration:.8f}"
def compact(points):
    result = []
    for t, value in sorted(points):
        if result and abs(result[-1][0] - t) < 1e-7:
            result[-1] = (t, value)
        else:
            result.append((t, value))
    return result

clips, lines = [], []
cursor = [(0, 0)]
for i, phrase in enumerate(phrases):
    start, n = i * slot, len(phrase)
    points = [(0, 0), (start, 0), (start + .25, 0)]
    for k in range(1, n + 1):
        t = start + .25 + k * min(.1, 2.8 / n)
        points.append((t, k * char_width))
        cursor.append((t, k * char_width))
    points.append((start + 4.5, n * char_width))
    for k in range(n - 1, -1, -1):
        t = start + 4.5 + (n - k) * min(.07, 1.8 / n)
        points.append((t, k * char_width))
        cursor.append((t, k * char_width))
    points.extend([(start + slot - .001, 0), (duration, 0)])
    cursor.append((start + slot - .001, 0))
    points = compact(points)
    clips.append(
        f'<clipPath id="clip{i}"><rect width="0" height="25">'
        f'<animate attributeName="width" calcMode="discrete" dur="{duration}s" '
        f'repeatCount="indefinite" keyTimes="{";".join(norm(t) for t, _ in points)}" '
        f'values="{";".join(f"{v:.2f}" for _, v in points)}"/>'
        '</rect></clipPath>'
    )
    lines.append(
        f'<g transform="translate(211 85)" clip-path="url(#clip{i})">'
        f'<text x="0" y="19" font-family="monospace" font-size="15" '
        f'fill="#e6edf3">{escape(phrase)}</text></g>'
    )
cursor.append((duration, 0))
cursor = compact(cursor)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="174" viewBox="0 0 580 174" role="img" aria-label="Terminal animado">
<!-- ARQUIVO GERADO. Edite frases.txt e execute: python scripts/gerar_terminal.py -->
<defs>{"".join(clips)}</defs>
<rect x="1" y="1" width="578" height="172" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
<path d="M15 1 H565 Q579 1 579 15 V43 H1 V15 Q1 1 15 1" fill="#161b22"/>
<path d="M1 43 H579" stroke="#30363d"/>
<circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="43" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>
<text x="290" y="27" font-size="13" fill="#8b949e" font-family="monospace" text-anchor="middle">redzzz@terminal</text>
<text x="22" y="104" font-size="15" font-family="monospace" fill="#e6edf3"><tspan fill="#7ee787">redzzz@PC-do-nick</tspan><tspan>:~$ </tspan></text>
{"".join(lines)}
<rect x="211" y="90" width="8" height="18" fill="#e6edf3">
<animateTransform attributeName="transform" type="translate" calcMode="discrete" dur="{duration}s" repeatCount="indefinite" keyTimes="{";".join(norm(t) for t, _ in cursor)}" values="{";".join(f"{v:.2f} 0" for _, v in cursor)}"/>
<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>
'''
output = ROOT / "terminal.svg"
output.write_text(svg, encoding="utf-8")
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
version = hashlib.sha256(svg.encode("utf-8")).hexdigest()[:12]
text, count = re.subn(r'\./terminal(?:-v\d+)?\.svg(?:\?v=[a-f0-9]+)?', f'./terminal.svg?v={version}', text)
if count != 1:
    raise SystemExit("Nao encontrei a imagem terminal.svg no README.md")
readme.write_text(text, encoding="utf-8")
print(f"Geradas {len(phrases)} frases. Versao: {version}")
