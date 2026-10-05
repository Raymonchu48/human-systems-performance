from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import urllib.request

root=Path(__file__).resolve().parents[1]
master_path=root/"assets"/"cluster-approved.webp"
src_path=root/".it-profile.jpg"
urllib.request.urlretrieve("https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",src_path)

base=Image.open(master_path).convert("RGBA")
src=Image.open(src_path).convert("RGB")

X0,Y0,X1,Y1=1080,76,1671,516
W,H=X1-X0,Y1-Y0

# dark technology base
section=Image.new("RGBA",(W,H),(3,18,29,255))

# Full source scaled to keep servers + full person visible and shifted left of the cards.
photo=src.resize((440,440),Image.Resampling.LANCZOS)
photo=ImageEnhance.Contrast(photo).enhance(1.08)
photo=ImageEnhance.Brightness(photo).enhance(0.80)
photo=ImageEnhance.Color(photo).enhance(0.88).convert("RGBA")
photo=Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,35,65,48)))
section.alpha_composite(photo,(0,0))

# soften the photo into the dark UI rail
fade=Image.new("L",(W,H),0)
fd=ImageDraw.Draw(fade)
fd.rectangle((0,0,440,H),fill=255)
fade=fade.filter(ImageFilter.GaussianBlur(14))

sec2=Image.new("RGBA",(W,H),(3,18,29,255))
sec2=Image.composite(section,sec2,fade)

result=base.copy()
result.paste(sec2,(X0,Y0))

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

d=ImageDraw.Draw(result,"RGBA")
cyan=(48,212,255,255); cyan2=(78,225,255,255); white=(240,246,248,255); muted=(163,218,231,255)

# header
d.text((1100,91),"SOLUCIONES QUE IMPULSAN RESULTADOS",font=font(13),fill=muted)
d.text((1100,116),"TECNOLOGÍA",font=font(39,True),fill=cyan)
d.text((1100,158),"SISTEMAS · DESARROLLO · REDES · IA",font=font(16),fill=muted)

# cards
card_x0,card_x1=1442,1656
labels=["DESARROLLO","SISTEMAS","REDES","SEGURIDAD","IA & DATA","AUTOMATIZACIÓN"]
icons=["</>","▦","⌘","◇","✣","⚙"]
ys=[110,159,208,257,306,355]
for i,(lab,y) in enumerate(zip(labels,ys)):
    d.rounded_rectangle((card_x0,y,card_x1,y+42),13,fill=(4,22,34,232),outline=cyan,width=2)
    d.text((1460,y+8),icons[i],font=font(24,True),fill=cyan2)
    d.text((1506,y+12),lab,font=font(14,True),fill=white)

d.line((1430,130,1430,389),fill=cyan,width=2)
for y in [131,180,229,278,327,376]:
    d.ellipse((1425,y-5,1435,y+5),fill=(205,250,255,255),outline=cyan,width=1)

# lower statement
d.rounded_rectangle((1320,432,1656,505),15,fill=(4,22,34,232),outline=(26,133,182,220),width=2)
d.rectangle((1342,451,1347,477),fill=cyan)
d.text((1362,446),"De la estrategia a la implementación.",font=font(14),fill=white)
d.text((1362,469),"Tecnología al servicio de las personas.",font=font(14,True),fill=cyan2)

# restore central IT node exactly
m=Image.new("L",base.size,0); md=ImageDraw.Draw(m); md.ellipse((965,205,1128,372),fill=255); m=m.filter(ImageFilter.GaussianBlur(2))
result=Image.composite(base,result,m)

# borders
p=Image.new("L",base.size,0); pd=ImageDraw.Draw(p); pd.rectangle((1065,68,1671,83),fill=255); pd.rectangle((1065,510,1671,525),fill=255)
result=Image.composite(base,result,p)

result.convert("RGB").save(master_path,"WEBP",quality=95,method=6)
src_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
