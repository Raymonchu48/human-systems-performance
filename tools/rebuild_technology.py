from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from pathlib import Path
import urllib.request, math

root = Path(__file__).resolve().parents[1]
master_path = root / "assets" / "cluster-approved.webp"
src_path = root / ".it-profile.jpg"

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",
    src_path
)

base = Image.open(master_path).convert("RGBA")
src = Image.open(src_path).convert("RGB")

# Technology section bounds. Rebuild the entire section so no pixels
# from the old hooded-person image survive.
X0, Y0, X1, Y1 = 1080, 76, 1671, 516
W, H = X1-X0, Y1-Y0

# Build background from the supplied IT profile image.
bg = ImageOps.fit(src, (W, H), method=Image.Resampling.LANCZOS, centering=(0.56, 0.50))
bg = ImageEnhance.Contrast(bg).enhance(1.10)
bg = ImageEnhance.Brightness(bg).enhance(0.72)
bg = ImageEnhance.Color(bg).enhance(0.82).convert("RGBA")
blue = Image.new("RGBA", bg.size, (0, 35, 65, 60))
bg = Image.alpha_composite(bg, blue)

# Add a darker right rail for UI cards.
rail = Image.new("RGBA", bg.size, (0,0,0,0))
rd = ImageDraw.Draw(rail)
rd.rectangle((360,0,W,H), fill=(3,18,29,150))
bg = Image.alpha_composite(bg, rail)

result = base.copy()
result.paste(bg, (X0,Y0))

# Fonts
def font(size,bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

d = ImageDraw.Draw(result, "RGBA")
cyan=(48,212,255,255); cyan2=(78,225,255,255); white=(240,246,248,255)
muted=(163,218,231,255); dark=(3,18,29,220)

# Header
d.text((1100,91),"SOLUCIONES QUE IMPULSAN RESULTADOS",font=font(13,False),fill=muted)
d.text((1100,116),"TECNOLOGÍA",font=font(39,True),fill=cyan)
d.text((1100,158),"SISTEMAS · DESARROLLO · REDES · IA",font=font(16,False),fill=muted)

# Keep the person/photo visible in center-right, and draw card rail.
card_x0, card_x1 = 1442, 1656
labels = ["DESARROLLO","SISTEMAS","REDES","SEGURIDAD","IA & DATA","AUTOMATIZACIÓN"]
ys = [110,159,208,257,306,355]
icons = ["</>","▦","⌘","◇","✣","⚙"]
for i,(lab,y) in enumerate(zip(labels,ys)):
    d.rounded_rectangle((card_x0,y,card_x1,y+42),radius=13,fill=(4,22,34,220),outline=cyan,width=2)
    d.text((1460,y+8),icons[i],font=font(24,True),fill=cyan2)
    d.text((1506,y+12),lab,font=font(14,True),fill=white)

# Lower statement card
d.rounded_rectangle((1320,432,1656,505),radius=15,fill=(4,22,34,225),outline=(26,133,182,220),width=2)
d.rectangle((1342,451,1347,477),fill=cyan)
d.text((1362,446),"De la estrategia a la implementación.",font=font(14,False),fill=white)
d.text((1362,469),"Tecnología al servicio de las personas.",font=font(14,True),fill=cyan2)

# Cyan connector line down the left/right of the cards
d.line((1430,130,1430,389),fill=cyan,width=2)
for y in [131,180,229,278,327,376]:
    d.ellipse((1425,y-5,1435,y+5),fill=(205,250,255,255),outline=cyan,width=1)

# Restore the central IT node and its ring from the pre-edit master,
# so it remains perfectly aligned with the main cluster.
node_mask = Image.new("L", base.size, 0)
nm = ImageDraw.Draw(node_mask)
nm.ellipse((965,205,1128,372),fill=255)
node_mask=node_mask.filter(ImageFilter.GaussianBlur(2))
result=Image.composite(base,result,node_mask)

# Restore thin top/bottom section boundaries from original master.
protect=Image.new("L",base.size,0); pd=ImageDraw.Draw(protect)
pd.rectangle((1065,68,1671,83),fill=255)
pd.rectangle((1065,510,1671,525),fill=255)
protect=protect.filter(ImageFilter.GaussianBlur(1))
result=Image.composite(base,result,protect)

result.convert("RGB").save(master_path,"WEBP",quality=95,method=6)
src_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
