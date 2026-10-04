from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
from pathlib import Path
import urllib.request

root = Path(__file__).resolve().parents[1]
master_path = root / "assets" / "cluster-approved.webp"
src_path = root / ".it-profile.jpg"

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",
    src_path
)

base = Image.open(master_path).convert("RGBA")
src = Image.open(src_path).convert("RGB")

# Technology image zone only. Keep the existing title, cards, quote, IT node,
# central cluster, methodology and sport areas untouched.
x0, y0, x1, y1 = 1115, 155, 1452, 516
tw, th = x1-x0, y1-y0

# Crop the photo to show server racks + the IT profile naturally.
src = ImageOps.fit(src, (tw, th), method=Image.Resampling.LANCZOS, centering=(0.58, 0.50))
src = ImageEnhance.Contrast(src).enhance(1.08)
src = ImageEnhance.Brightness(src).enhance(0.86)
src = ImageEnhance.Color(src).enhance(0.88)
src = src.convert("RGBA")

# Subtle cool-blue grade to match the Technology section.
grade = Image.new("RGBA", src.size, (0, 35, 65, 38))
src = Image.alpha_composite(src, grade)

layer = Image.new("RGBA", base.size, (0,0,0,0))
layer.paste(src, (x0, y0))

# Feather the image into the existing Technology scene.
mask = Image.new("L", base.size, 0)
d = ImageDraw.Draw(mask)
d.rounded_rectangle((x0, y0, x1, y1), radius=28, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(18))
result = Image.composite(layer, base, mask)

# Restore UI/HUD elements exactly from the original master so the photo sits
# inside the section rather than on top of cards/text.
protect = Image.new("L", base.size, 0)
p = ImageDraw.Draw(protect)
p.rectangle((1065, 75, 1438, 182), fill=255)     # TECNOLOGÍA + subtitle
p.rectangle((1432, 86, 1668, 406), fill=255)     # vertical cards
p.rectangle((1310, 430, 1668, 515), fill=255)    # quote panel
p.ellipse((969, 214, 1124, 368), fill=255)       # IT node and glow
protect = protect.filter(ImageFilter.GaussianBlur(3))
result = Image.composite(base, result, protect)

result.convert("RGB").save(master_path, "WEBP", quality=95, method=6)
src_path.unlink(missing_ok=True)

try:
    Path(__file__).unlink()
except Exception:
    pass
