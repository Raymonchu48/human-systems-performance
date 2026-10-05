from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import urllib.request

root=Path(__file__).resolve().parents[1]
master_path=root/"assets"/"cluster-approved.webp"
src_path=root/".it-profile.jpg"

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",
    src_path
)

base=Image.open(master_path).convert("RGBA")
src=Image.open(src_path).convert("RGB")

# Technology section
X0,Y0,X1,Y1=1080,76,1671,516
W,H=X1-X0,Y1-Y0

# Extend source canvas to the right before scaling.
# This moves the person left in the final composition while preserving
# the full server rack area on the left.
ext_w=src.width+360
extended=Image.new("RGB",(ext_w,src.height))
extended.paste(src,(0,0))

# Build a soft continuation on the right for the card rail.
edge=src.crop((src.width-220,0,src.width,src.height)).resize((360,src.height),Image.Resampling.LANCZOS)
edge=edge.filter(ImageFilter.GaussianBlur(18))
edge=ImageEnhance.Brightness(edge).enhance(0.52)
extended.paste(edge,(src.width,0))

# Fit to Technology area.
photo=extended.resize((W,H),Image.Resampling.LANCZOS)
photo=ImageEnhance.Contrast(photo).enhance(1.08)
photo=ImageEnhance.Brightness(photo).enhance(0.80)
photo=ImageEnhance.Color(photo).enhance(0.88).convert("RGBA")
photo=Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,32,58,48)))

result=base.copy()
result.paste(photo,(X0,Y0))

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

d=ImageDraw.Draw(result,"RGBA")
cyan=(48,212,255,255); cyan2=(78,225,255,255); white=(240,246,248,255); muted=(163,218,231,255)

# Darker right-side rail so cards sit outside the body.
d.rounded_rectangle((1450,92,1665,505),radius=18,fill=(3,18,29,182))

# Header
d.text((1100,91),"SOLUCIONES QUE IMPULSAN RESULTADOS",font=font(13),fill=muted)
d.text((1100,116),"TECNOLOGÍA",font=font(39,True),fill=cyan)
d.text((1100,158),"SISTEMAS · DESARROLLO · REDES · IA",font=font(16),fill=muted)

# Cards, tightened to the far-right rail.
card_x0,card_x1=1462,1654
labels=["DESARROLLO","SISTEMAS","REDES","SEGURIDAD","IA & DATA","AUTOMATIZACIÓN"]
icons=["</>","▦","⌘","◇","✣","⚙"]
ys=[110,159,208,257,306,355]
for i,(lab,y) in enumerate(zip(labels,ys)):
    d.rounded_rectangle((card_x0,y,card_x1,y+42),13,fill=(4,22,34,235),outline=cyan,width=2)
    d.text((1478,y+8),icons[i],font=font(23,True),fill=cyan2)
    d.text((1518,y+12),lab,font=font(13,True),fill=white)

d.line((1449,130,1449,389),fill=cyan,width=2)
for y in [131,180,229,278,327,376]:
    d.ellipse((1444,y-5,1454,y+5),fill=(205,250,255,255),outline=cyan,width=1)

# Lower statement card fully on the right.
d.rounded_rectangle((1370,432,1654,505),15,fill=(4,22,34,235),outline=(26,133,182,220),width=2)
d.rectangle((1390,451,1395,477),fill=cyan)
d.text((1410,446),"De la estrategia a la implementación.",font=font(13),fill=white)
d.text((1410,469),"Tecnología al servicio de las personas.",font=font(13,True),fill=cyan2)

# Restore IT node exactly from the previous master so it stays aligned.
m=Image.new("L",base.size,0)
md=ImageDraw.Draw(m)
md.ellipse((965,205,1128,372),fill=255)
m=m.filter(ImageFilter.GaussianBlur(2))
result=Image.composite(base,result,m)

# Preserve section borders.
p=Image.new("L",base.size,0)
pd=ImageDraw.Draw(p)
pd.rectangle((1065,68,1671,83),fill=255)
pd.rectangle((1065,510,1671,525),fill=255)
result=Image.composite(base,result,p)

result.convert("RGB").save(master_path,"WEBP",quality=95,method=6)
src_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
