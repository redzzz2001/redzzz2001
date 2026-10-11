#!/usr/bin/env python3
"""Gera terminal.svg a partir de frases.txt, sem dependencias externas."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "frases.txt"
DEST = ROOT / "terminal.svg"
phrases = [line.strip() for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
if not phrases:
    raise SystemExit("frases.txt precisa conter ao menos uma frase.")
if any(len(p) > 35 for p in phrases):
    raise SystemExit("Cada frase pode ter no maximo 35 caracteres para caber no terminal.")

slot = 7.0
duration = slot * len(phrases)
base_x = 230.0
char_width = 9.05
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="580" height="174" viewBox="0 0 580 174" role="img" aria-label="Terminal animado">',
    '<rect x="1" y="1" width="578" height="172" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="2"/>',
    '<path d="M15 1 H565 Q579 1 579 15 V43 H1 V15 Q1 1 15 1" fill="#161b22"/>',
    '<path d="M1 43 H579" stroke="#30363d"/>',
    '<circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="43" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>',
    '<text x="290" y="27" font-size="13" fill="#8b949e" font-family="monospace" text-anchor="middle">redzzz@terminal</text>',
    '<text x="22" y="104" font-size="15" font-family="monospace" fill="#e6edf3"><tspan fill="#7ee787">redzzz@PC-do-nick</tspan><tspan>:~$ </tspan></text>',
]
cursor_events = [(0.0, base_x)]

def pct(seconds):
    return f"{seconds / duration:.8f}"

for index, phrase in enumerate(phrases):
    start = index * slot
    n = len(phrase)
    # Digita durante 2.8s; espera 1.1s; apaga de tras para frente durante 1.8s.
    typing_step = min(0.105, 2.8 / n)
    deleting_step = min(0.075, 1.8 / n)
    typing_start = start + 0.30
    deleting_start = start + 4.60
    parts.append(f'<!-- Frase {index + 1}: {escape(phrase)} -->')
    parts.append(f'<text x="{base_x:g}" y="104" font-size="15" font-family="monospace" fill="#e6edf3" xml:space="preserve">')
    for j, ch in enumerate(phrase):
        appear = typing_start + (j + 1) * typing_step
        disappear = deleting_start + (n - j) * deleting_step
        parts.append(
            f'<tspan opacity="0">{escape(ch)}'
            f'<animate attributeName="opacity" calcMode="discrete" dur="{duration:g}s" '
            f'repeatCount="indefinite" keyTimes="0;{pct(appear)};{pct(disappear)};1" '
            f'values="0;1;0;0"/></tspan>'
        )
        cursor_events.append((appear, base_x + (j + 1) * char_width))
        cursor_events.append((disappear, base_x + j * char_width))
    parts.append('</text>')
    cursor_events.append(((index + 1) * slot - 0.001, base_x))

cursor_events.sort()
# Unifica timestamps repetidos para respeitar a ordem crescente exigida pelo SVG.
unique = []
for event in cursor_events:
    if unique and abs(unique[-1][0] - event[0]) < 0.000001:
        unique[-1] = event
    else:
        unique.append(event)
if unique[-1][0] < duration:
    unique.append((duration, base_x))
parts.append(
    f'<rect x="{base_x:g}" y="90" width="9" height="18" fill="#e6edf3">'
    f'<animate attributeName="x" calcMode="discrete" dur="{duration:g}s" repeatCount="indefinite" '
    f'keyTimes="{";".join(pct(t) for t, _ in unique)}" '
    f'values="{";".join(f"{x:.2f}" for _, x in unique)}"/>'
    '<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>'
    '</rect>'
)
parts.append('</svg>')
DEST.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"Gerado {DEST.name} com {len(phrases)} frase(s).")
