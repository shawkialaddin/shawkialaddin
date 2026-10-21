from pathlib import Path
import math, io, re
import cairosvg
from PIL import Image

root=Path(__file__).resolve().parents[1]
source=(root/"assets/profile-research-autonomous.svg").read_text()
# Remove the original flat satellite group, retaining the rest of the layout.
source=re.sub(r'<g class="sat">.*?(?=<circle cx="870")', '<!-- SATELLITE_REPLACEMENT -->', source, count=1, flags=re.S)
# Avoid reliance on font-dependent symbols, which previously rendered as squares.
source=source.replace('〈/〉 Candidate Repair','Candidate Repair').replace('◇ Independent Validation','Independent Validation').replace('▥ Controlled Activation','Controlled Activation').replace('Satellite Repair Lab ↗','Satellite Repair Lab >')
# Ensure the detailed satellite artwork sits in the same coordinate space as the guide lines.
def poly(points, fill, stroke="#98abb6", sw=1.6):
    return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def interpolate(p,q,t):
    return (p[0]*(1-t)+q[0]*t,p[1]*(1-t)+q[1]*t)
def fmt(p): return f"{p[0]:.1f},{p[1]:.1f}"
def panel(tl,tr,br,bl,cols=8,rows=5):
    p=poly(" ".join(map(fmt,(tl,tr,br,bl))),"#111b22","#b9cbd0",2)
    # The cell grid uses bilinear interpolation so perspective remains consistent.
    for j in range(1,cols):
        t=j/cols
        a=interpolate(tl,tr,t); b=interpolate(bl,br,t)
        p+=f'<path d="M{fmt(a)} L{fmt(b)}" stroke="#617782" stroke-width=".85"/>'
    for j in range(1,rows):
        t=j/rows
        a=interpolate(tl,bl,t); b=interpolate(tr,br,t)
        p+=f'<path d="M{fmt(a)} L{fmt(b)}" stroke="#617782" stroke-width=".85"/>'
    # Dark solar-cell panels with occasional electrical traces and visible metallic border.
    p+=f'<path d="M{fmt(tl)} L{fmt(tr)} L{fmt(br)}" fill="none" stroke="#e0eaeb" stroke-width="1" opacity=".55"/>'
    return p

def satellite(t):
    bob=7*math.sin(t*2*math.pi)
    v=f'<g transform="translate(0 {bob:.2f})">'
    # Long central booms visibly attach the solar wings to the chassis.
    v+='<path d="M1090 292 L1142 315 M1284 307 L1322 328" stroke="#c6d8dc" stroke-width="7"/>'
    v+='<path d="M1090 292 L1142 315 M1284 307 L1322 328" stroke="#26343c" stroke-width="3"/>'
    # Solar wings, drawn as actual angled planes with distinct frame depth.
    v+=panel((880,174),(1095,253),(1095,391),(880,312),8,5)
    v+=poly("880,312 1095,391 1102,395 887,316","#1a2830","#7f969d",.9)
    v+=panel((1312,270),(1516,342),(1516,482),(1312,412),8,5)
    v+=poly("1312,412 1516,482 1523,479 1319,409","#1c2931","#8298a1",.9)
    # Corner posts, top / left / right body faces with real 3-point box perspective.
    v+=poly("1135,246 1205,209 1294,247 1225,283","#29333a","#c3d6d8",2.4)
    v+=poly("1135,246 1225,283 1225,406 1135,368","#19262d","#bdd0d3",2.4)
    v+=poly("1225,283 1294,247 1294,367 1225,406","#101b22","#c5d6d9",2.4)
    # Recessed panels give tangible face depth.
    v+=poly("1150,268 1210,293 1210,383 1150,356","#101b21","#637b85",1.1)
    v+=poly("1238,293 1281,272 1281,355 1238,379","#182831","#69818b",1.1)
    for i in range(4):
        x=1158+i*13
        v+=f'<path d="M{x} {272+i*5} v82" stroke="#49616a" stroke-width="1"/>'
    v+='<path d="M1249 301 L1271 290 V349 L1249 360 Z" fill="#0d181f" stroke="#526c74"/>'
    # Structural plating seams and screws.
    v+='<path d="M1144 249 L1224 282 L1286 249 M1225 283 V406" fill="none" stroke="#f1f7f4" stroke-width="1.1" opacity=".8"/>'
    for x,y in [(1143,257),(1217,289),(1217,393),(1287,258),(1287,359),(1143,363)]:
        v+=f'<circle cx="{x}" cy="{y}" r="3.0" fill="#d5e2e2"/><circle cx="{x}" cy="{y}" r="1.2" fill="#25333a"/>'
    # Antenna mast with an elliptic dish and visibly concave support struts.
    v+='<path d="M1204 218 V153" stroke="#cadadd" stroke-width="3"/>'
    v+='<ellipse cx="1204" cy="150" rx="50" ry="14" fill="#172128" stroke="#d7e4e5" stroke-width="2"/>'
    v+='<path d="M1154 150 Q1204 201 1254 150 M1178 160 L1204 182 L1230 160" fill="none" stroke="#a9c0c4" stroke-width="1.4"/>'
    v+='<path d="M1204 134 V106" stroke="#d5e2e3" stroke-width="2"/><circle cx="1204" cy="103" r="3" fill="#c7e8da"/>'
    v+='</g>'
    return v

frames=[]
N=30
for i in range(N):
    t=i/N
    a=t*2*math.pi
    x=1200+310*math.cos(a); y=294+138*math.sin(a)
    # A tracking dot follows the orbit while the satellite itself gently floats.
    moving=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#a0eabb"/><circle cx="{x:.2f}" cy="{y:.2f}" r="11" fill="none" stroke="#8ed6a5" opacity=".28"/>'
    pulse=f'<circle cx="644" cy="65" r="{5+2*math.sin(a)**2:.2f}" fill="#94ddb0" opacity=".7"/>'
    art=source.replace('<!-- SATELLITE_REPLACEMENT -->',satellite(t))
    art=art.replace('</svg>',moving+pulse+'</svg>')
    png=cairosvg.svg2png(bytestring=art.encode(),output_width=1440,output_height=522)
    frame=Image.open(io.BytesIO(png)).convert('RGB').quantize(colors=128,method=Image.Quantize.FASTOCTREE)
    frames.append(frame)
out=root/"assets/profile-research-animated.gif"
frames[0].save(out,save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=2)
print("Generated",out,out.stat().st_size,"bytes",len(frames),"frames")


# Satellite-only artwork. The research heading, copy, badges and links are real README elements.
# A 700x440 viewBox isolates the spacecraft and removes the old full-banner text.
isolated=[]
for i in range(N):
    t=i/N
    a=2*math.pi*t
    x=1200+280*math.cos(a)
    y=294+115*math.sin(a)
    scene=f'''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="440" viewBox="850 85 700 440">
    <rect x="850" y="85" width="700" height="440" fill="#0d1117"/>
    <ellipse cx="1200" cy="294" rx="305" ry="128" fill="none" stroke="#344b51" stroke-width="1" stroke-dasharray="7 8"/>
    <ellipse cx="1200" cy="294" rx="260" ry="150" transform="rotate(-17 1200 294)" fill="none" stroke="#26393e" stroke-width="1"/>
    <path d="M1200 90 V517 M867 294 H1535" stroke="#2c3c42" stroke-width=".7" stroke-dasharray="5 12"/>
    {satellite(t)}
    <circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#9cdcb5"/>
    </svg>'''
    im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=scene.encode(),output_width=560,output_height=352))).convert("RGB")
    isolated.append(im.quantize(colors=128,method=Image.Quantize.FASTOCTREE))
satout=root/"assets/research-satellite-only.gif"
isolated[0].save(satout,save_all=True,append_images=isolated[1:],duration=90,loop=0,optimize=True,disposal=2)
print("Generated isolated satellite",satout,satout.stat().st_size)
