from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import urllib.request

root = Path(__file__).resolve().parents[1]
master = root / "assets" / "cluster-approved.webp"
src_path = root / ".approved-center.png"

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/817fa257-87a2-49cb-97e2-d73d8dd1e258.png",
    src_path
)

base = Image.open(master).convert("RGBA")
src = Image.open(src_path).convert("RGBA")

# Exact geometric mapping from the approved central design to the live cluster.
# Approved source reference nodes:
# F&B center ~ (140,550), IT center ~ (1090,550), SPORT center ~ (640,1030)
# Live master targets:
# F&B center ~ (621,292), IT center ~ (1040,292), SPORT center ~ (836,505)
# Uniform scale ~0.442, top-left ~ (559,49)
src = src.resize((565,528), Image.Resampling.LANCZOS)

layer = Image.new("RGBA", base.size, (0,0,0,0))
layer.paste(src, (559,49))

# Rebuild only the central cluster geometry: main nucleus + the three nodes.
mask = Image.new("L", base.size, 0)
d = ImageDraw.Draw(mask)
d.ellipse((575,30,1095,560), fill=255)   # central ring/nucleus
d.ellipse((552,210,700,370), fill=255)   # F&B
d.ellipse((975,210,1122,370), fill=255)  # IT
d.ellipse((760,438,910,590), fill=255)   # SPORT
mask = mask.filter(ImageFilter.GaussianBlur(3.5))

result = Image.composite(layer, base, mask)
result.convert("RGB").save(master, "WEBP", quality=95, method=6)

src_path.unlink(missing_ok=True)
try:
    Path(__file__).unlink()
except Exception:
    pass
