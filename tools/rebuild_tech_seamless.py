from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path
import subprocess, urllib.request

root = Path(__file__).resolve().parents[1]
master_path = root / "assets" / "cluster-approved.webp"
clean_path = root / ".clean-base.webp"
src_path = root / ".it-profile.jpg"

# Restore stable master before the Technology paste experiments.
with clean_path.open("wb") as fh:
    subprocess.run(
        ["git","show","e259e84451a02aff345bd319eb798ba4aacd31ea:assets/cluster-approved.webp"],
        stdout=fh, check=True
    )

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",
    src_path
)

base = Image.open(clean_path).convert("RGBA")
src = Image.open(src_path).convert("RGB")
result = base.copy()

# TECHNOLOGY rebuilt directly into the master.
# The composition follows the approved reference; no reference crop is inserted.
X0,Y0,X1,Y1 = 1060,76,1671,516
W,H = X1-X0, Y1-Y0

# Build a continuous technology background from the supplied IT photo.
# Add room on the right so the profile shifts left and cards stay outside the body.
canvas_w = 1450
ext = Image.new("RGB",(canvas_w,src.height),(3,16,28))
ext.paste(src,(0,0))
right = src.crop((src.width-160,0,src.width,src.height)).resize((canvas_w-src.width,src.height),Image.Resampling.LANCZOS)
right = right.filter(ImageFilter.GaussianBlur(24))
right = ImageEnhance.Brightness(right).enhance(.48)
ext.paste(right,(src.width,0))

photo = ImageOps.fit(ext,(W,H),method=Image.Resampling.LANCZOS,centering=(0.47,0.50))
photo = ImageEnhance.Contrast(photo).enhance(1.10)
photo = ImageEnhance.Brightness(photo).enhance(.76)
photo = ImageEnhance.Color(photo).enhance(.87).convert("RGBA")
photo = Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,34,66,52)))

# Seamless mask: opaque through the whole tech area, only feathered at the
# natural left/bottom transitions into the existing HUD.
layer = Image.new("RGBA",base.size,(0,0,0,0))
layer.paste(photo,(X0,Y0))
mask = Image.new("L",base.size,0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((X0,Y0,X1,Y1),radius=26,fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(8))
result = Image.composite(layer,result,mask)

def font(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)

d=ImageDraw.Draw(result,"RGBA")
cyan=(46,213,255,255); cyan2=(84,230,255,255); white=(244,248,250,255); muted=(160,218,232,255)

# Right rail, matching the approved reference and leaving the body unobstructed.
rail_x0=1435
d.rounded_rectangle((rail_x0,94,1662,505),radius=18,fill=(3,18,29,180))

# Header.
d.text((1092,94),"SOLUCIONES QUE IMPULSAN RESULTADOS",font=font(12),fill=muted)
d.text((1092,120),"TECNOLOGÍA",font=font(38,True),fill=cyan)
d.text((1092,160),"SISTEMAS · DESARROLLO · REDES · IA",font=font(15),fill=muted)

# Cards.
labels=["DESARROLLO","SISTEMAS","REDES","SEGURIDAD","IA & DATA","AUTOMATIZACIÓN"]
icons=["</>","▦","⌘","◇","✣","⚙"]
ys=[109,158,207,256,305,354]
d.line((1424,130,1424,388),fill=cyan,width=2)
for y in [130,179,228,277,326,375]:
    d.ellipse((1419,y-5,1429,y+5),fill=(210,252,255,255),outline=cyan,width=1)
for i,(lab,y) in enumerate(zip(labels,ys)):
    d.rounded_rectangle((1436,y,1657,y+42),13,fill=(4,22,34,230),outline=cyan,width=2)
    d.text((1452,y+8),icons[i],font=font(23,True),fill=cyan2)
    d.text((1496,y+12),lab,font=font(13,True),fill=white)

# Statement box.
d.rounded_rectangle((1310,431,1657,505),15,fill=(4,22,34,224),outline=(28,137,184,220),width=2)
d.rectangle((1332,450,1337,478),fill=cyan)
d.text((1352,446),"De la estrategia a la implementación.",font=font(13),fill=white)
d.text((1352,469),"Tecnología al servicio de las personas.",font=font(13,True),fill=cyan2)

# Restore central IT node/orbit precisely from the clean base.
node_mask=Image.new("L",base.size,0)
nd=ImageDraw.Draw(node_mask)
nd.ellipse((963,201,1132,374),fill=255)
node_mask=node_mask.filter(ImageFilter.GaussianBlur(2))
result=Image.composite(base,result,node_mask)

# Preserve the original top HUD line and the natural mountain transition below.
frame=Image.new("L",base.size,0)
fd=ImageDraw.Draw(frame)
fd.rectangle((1045,64,1671,82),fill=255)
fd.rectangle((1045,508,1671,526),fill=255)
frame=frame.filter(ImageFilter.GaussianBlur(1))
result=Image.composite(base,result,frame)

result.convert("RGB").save(master_path,"WEBP",quality=95,method=6)

clean_path.unlink(missing_ok=True)
src_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
