#!/usr/bin/env python3
"""Cria um GIF de terminal a partir de frases.txt, sem SVG."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import re

ROOT = Path(__file__).resolve().parent.parent
phrases = [s.strip() for s in (ROOT / "frases.txt").read_text(encoding="utf-8").splitlines() if s.strip() and not s.lstrip().startswith("#")]
if not phrases:
    raise SystemExit("frases.txt esta vazio")
if any(len(s) > 35 for s in phrases):
    raise SystemExit("Cada frase deve ter no maximo 35 caracteres")

fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
font = ImageFont.truetype(fontpath, 16)
small = ImageFont.truetype(fontpath, 12)
W, H = 580, 174
bg = "#0d1117"
def frame(phrase, cursor=True):
    im = Image.new("RGB", (W, H), "#090d13")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, W-2, H-2), radius=14, fill=bg, outline="#30363d", width=2)
    d.rounded_rectangle((2, 2, W-3, 44), radius=12, fill="#161b22")
    d.rectangle((2, 32, W-3, 44), fill="#161b22")
    d.line((2, 44, W-3, 44), fill="#30363d")
    for x,c in [(22,"#ff5f57"),(43,"#febc2e"),(64,"#28c840")]:
        d.ellipse((x-6, 16, x+6, 28), fill=c)
    label = "redzzz@terminal"
    bb=d.textbbox((0,0),label,font=small)
    d.text(((W-(bb[2]-bb[0]))/2,16),label,font=small,fill="#8b949e")
    prompt = "redzzz@PC-do-nick"
    suffix = ":~$ "
    x=22
    d.text((x,86),prompt,font=font,fill="#7ee787")
    x+=d.textlength(prompt,font=font)
    d.text((x,86),suffix,font=font,fill="#e6edf3")
    x+=d.textlength(suffix,font=font)
    d.text((x,86),phrase,font=font,fill="#e6edf3")
    x+=d.textlength(phrase,font=font)
    if cursor:
        d.rectangle((int(x),88,int(x)+8,104),fill="#e6edf3")
    return im

frames=[]
times=[]
def add(s,ms):
    frames.append(frame(s,True))
    times.append(ms)
for phrase in phrases:
    add("",250)
    for i in range(1,len(phrase)+1):
        add(phrase[:i],100)
    add(phrase,1100)
    for i in range(len(phrase)-1,-1,-1):
        add(phrase[:i],65)
    add("",450)

output=ROOT/"terminal.gif"
frames[0].save(output,save_all=True,append_images=frames[1:],duration=times,loop=0,optimize=True,disposal=2)
version=hashlib.sha256(output.read_bytes()).hexdigest()[:12]
readme=ROOT/"README.md"
s=readme.read_text(encoding="utf-8")
s,n=re.subn(r'\./terminal\.(?:svg|gif)(?:\?v=[a-f0-9]+)?',f'./terminal.gif?v={version}',s)
if n!=1:
    raise SystemExit("Nao foi possivel encontrar uma unica imagem do terminal no README")
readme.write_text(s,encoding="utf-8")
print(f"GIF gerado com {len(phrases)} frases; versao {version}")
