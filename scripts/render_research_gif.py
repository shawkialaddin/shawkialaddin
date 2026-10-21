from pathlib import Path
import math, io
import cairosvg
from PIL import Image

root = Path(__file__).resolve().parents[1]
svg = (root / "assets/profile-research-autonomous.svg").read_text()
# SMIL and CSS are not required for the GIF: each frame is rasterized independently.
svg = svg.replace('width="1600" height="580"', 'width="1600" height="580"')
frames=[]
N=24
for i in range(N):
    p=i/N
    a=2*math.pi*p
    # Animated orbital tracking beacon, pulsing status, and sweeping telemetry.
    x=1200+295*math.cos(a)
    y=292+126*math.sin(a)
    satshift=5*math.sin(a)
    marker=f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#8df6b1" opacity=".12"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#a6ffca"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#ffffff"/></g>'
    beamx=980+480*p
    beam=f'<path d="M {beamx:.1f} 125 V 485" stroke="#a0f5c3" stroke-width="2" opacity=".35"/><path d="M {beamx-25:.1f} 125 V 485" stroke="#a0f5c3" opacity=".12"/>'
    pulse=f'<circle cx="644" cy="65" r="{6+3*math.sin(a)**2:.1f}" fill="#9afbc0" opacity=".5"/>'
    image_svg=svg.replace('</svg>', marker+beam+pulse+'</svg>')
    png=cairosvg.svg2png(bytestring=image_svg.encode(),output_width=1200,output_height=435)
    img=Image.open(io.BytesIO(png)).convert("RGB").quantize(colors=96, method=Image.Quantize.FASTOCTREE)
    frames.append(img)
out=root/"assets/profile-research-animated.gif"
frames[0].save(out,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=2)
print(out, out.stat().st_size, len(frames))
