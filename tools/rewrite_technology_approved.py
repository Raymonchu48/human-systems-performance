from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
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

# Approved Technology geometry, rewritten from scratch in the master.
X0,Y0,X1,Y1=1092,78,1671,516
W,H=X1-X0,Y1-Y0

# Extend source to the right to shift the person left, matching approved reference.
ext_w=1500
extended=Image.new("RGB",(ext_w,src.height))
extended.paste(src,(0,0))
edge=src.crop((src.width-180,0,src.width,src.height)).resize((ext_w-src.width,src.height),Image.Resampling.LANCZOS)
edge=edge.filter(ImageFilter.GaussianBlur(20))
edge=ImageEnhance.Brightness(edge).enhance(0.55)
extended.paste(edge,(src.width,0))

photo=extended.resize((W,H),Image.Resampling.LANCZOS)
photo=ImageEnhance.Contrast(photo).enhance(1.08)
photo=ImageEnhance.Brightness(photo).enhance(0.78)
photo=ImageEnhance.Color(photo).enhance(0.88).convert("RGBA")
photo=Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,34,63,45)))

result=base.copy()
result.paste(photo,(X0,Y0))

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

d=ImageDraw.Draw(result,"RGBA")
cyan=(48,212,255,255); cyan2=(74,225,255,255); white=(244,248,250,255); muted=(163,218,231,255)

# Right UI rail reconstructed exactly in the approved layout.
rail_x0=1414
d.rounded_rectangle((rail_x0,96,1662,505),radius=18,fill=(3,18,29,182))

# Header
d.text((1110,96),"SOLUCIONES QUE IMPULSAN RESULTADOS",font=font(12),fill=muted)
d.text((1110,121),"TECNOLOGÍA",font=font(37,True),fill=cyan)
d.text((1110,161),"SISTEMAS · DESARROLLO · REDES · IA",font=font(15),fill=muted)

# Connector and cards
d.line((1430,132,1430,390),fill=cyan,width=2)
for y in [132,181,230,279,328,377]:
    d.ellipse((1425,y-5,1435,y+5),fill=(205,250,255,255),outline=cyan,width=1)

labels=["DESARROLLO","SISTEMAS","REDES","SEGURIDAD","IA & DATA","AUTOMATIZACIÓN"]
icons=["</>","▦","⌘","◇","✣","⚙"]
ys=[110,159,208,257,306,355]
for i,(lab,y) in enumerate(zip(labels,ys)):
    d.rounded_rectangle((1440,y,1658,y+42),13,fill=(4,22,34,228),outline=cyan,width=2)
    d.text((1456,y+8),icons[i],font=font(23,True),fill=cyan2)
    d.text((1500,y+12),lab,font=font(13,True),fill=white)

# Statement box
d.rounded_rectangle((1322,432,1658,505),15,fill=(4,22,34,225),outline=(26,133,182,220),width=2)
d.rectangle((1344,450,1349,478),fill=cyan)
d.text((1364,446),"De la estrategia a la implementación.",font=font(13),fill=white)
d.text((1364,469),"Tecnología al servicio de las personas.",font=font(13,True),fill=cyan2)

# Restore IT node and orbit exactly from the preexisting master.
mask=Image.new("L",base.size,0)
md=ImageDraw.Draw(mask)
md.ellipse((965,205,1128,372),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(2))
result=Image.composite(base,result,mask)

# Preserve section frame/top and lower transition.
pm=Image.new("L",base.size,0)
pd=ImageDraw.Draw(pm)
pd.rectangle((1060,66,1671,82),fill=255)
pd.rectangle((1060,508,1671,526),fill=255)
result=Image.composite(base,result,pm)

result.convert("RGB").save(master_path,"WEBP",quality=95,method=6)
src_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
