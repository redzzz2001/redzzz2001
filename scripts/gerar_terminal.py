#!/usr/bin/env python3
"""Gera terminal.svg a partir de frases.txt, com digitação por caracteres inteiros."""
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parent.parent
phrases = [s.strip() for s in (ROOT / "frases.txt").read_text(encoding="utf-8").splitlines() if s.strip() and not s.lstrip().startswith("#")]
if not phrases:
    raise SystemExit("frases.txt esta vazio")
if any(len(s) > 35 for s in phrases):
    raise SystemExit("Cada frase deve ter ate 35 caracteres")
slot = 7.0
duration = slot * len(phrases)
base = 211.0
char_width = 9.03

def norm(t):
    return f"{t / duration:.8f}"

parts = [
'<svg xmlns="http://www.w3.org/2000/svg" width="580" height="174" viewBox="0 0 580 174" role="img" aria-label="Terminal animado">',
'<defs>',
]
cursor = [(0.0, base)]
for i, phrase in enumerate(phrases):
    n = len(phrase)
    start = i * slot
    type_step = min(.10, 2.8 / n)
    erase_step = min(.07, 1.8 / n)
    type_start = start + .25
    erase_start = start + 4.5
    # A largura so muda em passos: nunca ha interpolacao/deslizamento.
    points = [(0.0, 0.0), (type_start, 0.0)]
    for k in range(1, n + 1):
        tm = type_start + k * type_step
        points.append((tm, k * char_width))
        cursor.append((tm, base + k * char_width))
    points.append((erase_start, n * char_width))
    for k in range(n - 1, -1, -1):
        tm = erase_start + (n - k) * erase_step
        points.append((tm, k * char_width))
        cursor.append((tm, base + k * char_width))
    points.append(((i + 1) * slot, 0.0))
    if i < len(phrases) - 1:
        points.append((duration, 0.0))
    keys = ";".join(norm(t) for t, _ in points)
    values = ";".join(f"{v:.2f}" for _, v in points)
    parts.append(
        f'<clipPath id="clip{i}"><rect x="0" y="0" width="0" height="25">'
        f'<animate attributeName="width" calcMode="discrete" dur="{duration:g}s" '
        f'repeatCount="indefinite" keyTimes="{keys}" values="{values}"/>'
        '</rect></clipPath>'
    )
    cursor.append(((i + 1) * slot - .001, base))
parts += [
'</defs>',
'<rect x="1" y="1" width="578" height="172" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="2"/>',
'<path d="M15 1 H565 Q579 1 579 15 V43 H1 V15 Q1 1 15 1" fill="#161b22"/>',
'<path d="M1 43 H579" stroke="#30363d"/>',
'<circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="43" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>',
'<text x="290" y="27" font-size="13" fill="#8b949e" font-family="monospace" text-anchor="middle">redzzz@terminal</text>',
'<text x="22" y="104" font-size="15" font-family="monospace" fill="#e6edf3"><tspan fill="#7ee787">redzzz@PC-do-nick</tspan><tspan>:~$ </tspan></text>',
]
for i, phrase in enumerate(phrases):
    parts.append(
        f'<g transform="translate({base:g} 85)" clip-path="url(#clip{i})">'
        f'<text x="0" y="19" font-size="15" font-family="monospace" fill="#e6edf3" xml:space="preserve">{escape(phrase)}</text></g>'
    )
cursor.sort()
dedup = []
for item in cursor:
    if dedup and abs(item[0] - dedup[-1][0]) < 1e-7:
        dedup[-1] = item
    else:
        dedup.append(item)
if dedup[-1][0] < duration:
    dedup.append((duration, base))
parts.append(
    f'<rect x="{base:g}" y="90" width="9" height="18" fill="#e6edf3">'
    f'<animate attributeName="x" calcMode="discrete" dur="{duration:g}s" repeatCount="indefinite" '
    f'keyTimes="{";".join(norm(t) for t, _ in dedup)}" '
    f'values="{";".join(f"{x:.2f}" for _, x in dedup)}"/>'
    '<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>'
    '</rect>'
)
parts.append('</svg>')
(ROOT / "terminal.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"Geradas {len(phrases)} frases")
