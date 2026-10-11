#!/usr/bin/env python3
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parent.parent
phrases = [s.strip() for s in (ROOT / "frases.txt").read_text(encoding="utf-8").splitlines() if s.strip() and not s.lstrip().startswith("#")]
if not phrases: raise SystemExit("frases.txt vazio")
if any(len(s)>35 for s in phrases): raise SystemExit("Limite de 35 caracteres por frase")
duration = len(phrases)*7
base = 230
def t(v): return f"{v/duration:.8f}"
p = ['<svg xmlns="http://www.w3.org/2000/svg" width="580" height="174" viewBox="0 0 580 174">',
'<rect x="1" y="1" width="578" height="172" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="2"/>',
'<path d="M15 1 H565 Q579 1 579 15 V43 H1 V15 Q1 1 15 1" fill="#161b22"/>',
'<path d="M1 43 H579" stroke="#30363d"/>',
'<circle cx="22" cy="22" r="6" fill="#ff5f57"/><circle cx="43" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>',
'<text x="290" y="27" font-size="13" fill="#8b949e" font-family="monospace" text-anchor="middle">redzzz@terminal</text>',
'<text x="22" y="104" font-size="15" font-family="monospace" fill="#e6edf3"><tspan fill="#7ee787">redzzz@PC-do-nick</tspan><tspan>:~$ </tspan></text>']
cursor=[(0,base)]
for i,s in enumerate(phrases):
    n=len(s); start=i*7; step=min(.105,2.8/n); back=min(.075,1.8/n); begin=start+.3; erase=start+4.6
    for k in range(1,n+1):
        a=begin+k*step
        b=begin+(k+1)*step if k<n else erase+back
        if k<n:
            c=erase+(n-k)*back; d=erase+(n-k+1)*back
            keys=f"0;{t(a)};{t(b)};{t(c)};{t(d)};1"; vals="0;1;0;1;0;0"
        else:
            keys=f"0;{t(a)};{t(b)};1"; vals="0;1;0;0"
        p.append(f'<text x="{base}" y="104" font-size="15" font-family="monospace" fill="#e6edf3" opacity="0" xml:space="preserve">{escape(s[:k])}<animate attributeName="opacity" calcMode="discrete" dur="{duration}s" repeatCount="indefinite" keyTimes="{keys}" values="{vals}"/></text>')
        cursor.append((a,base+k*9.05))
        cursor.append((erase+(n-k)*back,base+k*9.05))
    cursor.append((start+7-.001,base))
cursor.sort()
unique=[]
for e in cursor:
    if unique and abs(unique[-1][0]-e[0])<.000001: unique[-1]=e
    else: unique.append(e)
if unique[-1][0]<duration: unique.append((duration,base))
keys=";".join(t(v) for v,_ in unique)
vals=";".join(f"{x:.2f}" for _,x in unique)
p.append(f'<rect x="{base}" y="90" width="9" height="18" fill="#e6edf3"><animate attributeName="x" calcMode="discrete" dur="{duration}s" repeatCount="indefinite" keyTimes="{keys}" values="{vals}"/><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
p.append("</svg>")
(ROOT/"terminal.svg").write_text("\n".join(p)+"\n",encoding="utf-8")
print("Gerado SVG com",len(phrases),"frases")
