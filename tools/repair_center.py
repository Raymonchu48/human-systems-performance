from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import subprocess, shutil

root = Path(__file__).resolve().parents[1]
current_path = root / "assets" / "cluster-approved.webp"
clean_path = root / ".clean-master.webp"

# Recover the last clean approved cluster before the portrait integration.
with clean_path.open("wb") as fh:
    subprocess.run(
        ["git","show","8612f9f673b6b653822cd41901404b292b7bc56d:assets/cluster-approved.webp"],
        stdout=fh, check=True
    )

clean = Image.open(clean_path).convert("RGBA")
source = Image.open(current_path).convert("RGBA")
result = clean.copy()

# Replace only the INSIDE of the central nucleus.
# F&B, IT and SPORT are deliberately outside this mask.
mask = Image.new("L", clean.size, 0)
d = ImageDraw.Draw(mask)
d.ellipse((660, 70, 1012, 446), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(7))

result.paste(source, (0,0), mask)

# Re-protect the three HUD nodes and their immediate orbit area from the clean master.
protect = Image.new("L", clean.size, 0)
p = ImageDraw.Draw(protect)
p.ellipse((550, 215, 684, 355), fill=255)   # F&B
p.ellipse((987, 214, 1123, 356), fill=255)  # IT
p.ellipse((768, 447, 904, 585), fill=255)   # SPORT
protect = protect.filter(ImageFilter.GaussianBlur(3))
result.paste(clean, (0,0), protect)

result.convert("RGB").save(current_path, "WEBP", quality=95, method=6)

clean_path.unlink(missing_ok=True)
try:
    Path(__file__).unlink()
except Exception:
    pass
