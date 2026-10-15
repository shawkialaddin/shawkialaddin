#!/usr/bin/env python3
"""Generate GitHub-compatible editorial sections from the page's real content/data."""
from pathlib import Path
from datetime import date, datetime
import json
import html
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'
FG='#edeeec';MUTED='#abb4bf';SAGE='#accbb0';LINE='#303438'
def start(height,title):return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title"><title id="title">{html.escape(title)}</title><rect width="1200" height="{height}" fill="#101114"/><style>text{{font-family:Arial,sans-serif}}</style>'
def text(x,y,content,size=17,color=MUTED,extra=''):return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{html.escape(content)}</text>'
def rule(y):return f'<path d="M48 {y}H1152" stroke="{LINE}"/>'
def label(y,content):return text(48,y,content,11,FG,'letter-spacing="3.5"')
def save(name,parts): (OUT/name).write_text(''.join(parts)+'</svg>')
def satellite(x,y,scale=1):return f'''<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="#78897e" stroke-width=".8"><path d="M-170 0H170 M0 -105V105 M-120 -70L120 70" stroke="#46524a" stroke-dasharray="1 7"/><g transform="rotate(24) skewY(-18)"><path d="M-28 -26L0 -40L30 -22V26L0 42L-28 24Z M-28 -26L0 -9L30 -22 M0 -9V42 M-28 24L0 8L30 26"/><path d="M-32 -25H-132V27H-32Z M32 -25H132V27H32Z M-112 -25V27 M-92 -25V27 M-72 -25V27 M-52 -25V27 M52 -25V27 M72 -25V27 M92 -25V27 M112 -25V27 M-132 -8H-32 M-132 10H-32 M32 -8H132 M32 10H132 M0 -40V-76 M-12 -76Q0 -54 12 -76"/></g></g>'''
# Extend the corrected hero with the same quiet technical detail used in the approved design.
p=OUT/'profile-header.svg';hero=p.read_text();hero=hero.replace('</svg>',satellite(780,90,.48)+'</svg>') if 'skewY' not in hero else hero;p.write_text(hero)
save('profile-about.svg',[start(162,'About Shawki Aladdin'),label(35,'ABOUT'),text(48,79,'I build backend systems, developer tools, and infrastructure.',20),text(48,112,'My interests include applied AI, cybersecurity, and space systems.',20),rule(155)])
save('profile-projects.svg',[start(105,'Projects: products I am working on'),label(35,'PROJECTS'),text(48,77,'Products I’m working on.',20,FG)])
for name,number,title,description,domain in [('profile-gitroots.svg','01','gitroots','Code governance and access controls for engineering teams.','gitroots.com ↗'),('profile-crypto.svg','02','CryptoRadar','A crypto platform in development.','cryptorader.io ↗')]:
 save(name,[start(100,title+': '+description),text(48,45,number,12,'#78828d','font-family="monospace"'),text(105,46,title,21,FG),text(302,45,description,15),text(1005,45,domain,13,SAGE),rule(91)])
save('profile-research.svg',[start(358,'Ongoing research: offline repair for satellite software'),label(35,'RESEARCH'),text(48,79,'ONGOING',11,SAGE,'letter-spacing="2.5"'),text(48,121,'Offline repair for satellite software',28,FG,'letter-spacing="-.6"'),text(48,162,'Investigating independent patch acceptance for satellite-inspired',17),text(48,190,'applications, separating candidate repair from activation.',17),text(48,237,'Experimental prototype using synthetic fixtures.',14,'#959fa9'),text(48,262,'AI-generated repair and spacecraft integration remain unevaluated.',14,'#959fa9'),text(48,306,'Satellite Repair Lab ↗',14,SAGE),satellite(972,186,1.07),rule(350)])
data=json.loads((ROOT/'site/activity.json').read_text());year=max(map(int,data['years']));days=data['years'][str(year)];first=date(year,1,1);offset=(first.weekday()+1)%7;columns=((date(year,12,31)-first).days+1+offset+6)//7
parts=[start(326,f'Public GitHub contribution calendar for {year}'),label(35,'GITHUB ACTIVITY'),text(1087,35,str(year),14,FG)]
startx=95;pitch=19.7;side=15
for m in range(1,13):
 d=date(year,m,1);col=((d-first).days+offset)//7;parts.append(text(startx+col*pitch,81,d.strftime('%b'),11))
for row,name in enumerate(['Sun','','Tue','','Thu','','Sat']):
 if name:parts.append(text(48,109+row*21,name,10))
colors=['#24292c','#354a3f','#54745b','#7e9f7b','#bbd9b4']
for day in days:
 d=date.fromisoformat(day['date']);index=(d-first).days+offset;col,row=divmod(index,7);parts.append(f'<rect x="{startx+col*pitch:.1f}" y="{97+row*21}" width="{side}" height="15" rx="2" fill="{colors[day["level"]]}"/>')
updated=datetime.fromisoformat(data['updatedAt']).strftime('%d %b %Y');parts.extend([text(48,282,f'Public contribution snapshot · {updated}',11,'#8f99a3'),text(1014,282,'View activity ↗',13,SAGE),rule(318)]);save('profile-activity.svg',parts)
parts=[start(342,'Experiments: pixel field and satellite model. Open the personal page for the interactive versions.'),label(35,'EXPERIMENTS'),text(48,75,'Pixel field',17,FG),text(642,75,'Satellite model',17,FG),'<path d="M600 62V278" stroke="#303438"/>']
import random
r=random.Random(17)
parts.append('<style>.f{animation:float 6s ease-in-out infinite alternate}@keyframes float{to{transform:translate(5px,-9px);opacity:.3}}@media(prefers-reduced-motion:reduce){.f{animation:none}}</style>')
for i in range(90):
 x=r.uniform(58,548);y=r.uniform(100,254);s=r.uniform(2,5);parts.append(f'<rect class="f" x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{SAGE}" opacity="{r.uniform(.18,.8):.2f}" style="animation-delay:-{r.uniform(0,6):.1f}s"/>')
parts.extend([satellite(891,176,.85),text(48,302,'Interactive experiments on the personal page ↗',13,SAGE),rule(334)]);save('profile-experiments.svg',parts)
save('profile-footer.svg',[start(182,'Interests: applied AI, cybersecurity, distributed systems, and space technology'),label(35,'INTERESTS'),text(48,82,'Applied AI   ·   Cybersecurity   ·   Distributed systems   ·   Space technology',17),rule(120),text(48,157,'Shawki Aladdin',12),text(943,157,'Personal page ↗',12,SAGE),text(1100,157,'2026',11,'#78828d')])
print('Generated designed README sections from the real calendar and profile content.')
