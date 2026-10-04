from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import base64, shutil

root = Path(__file__).resolve().parents[1]
base_path = root / "assets" / "cluster-approved.webp"
parts_dir = root / ".tmp" / "portrait2"

# Rebuild approved central portrait source from staged chunks.
payload = "".join(p.read_text().strip() for p in sorted(parts_dir.glob("part*.txt")))
patch_path = root / ".tmp" / "approved-center.webp"
patch_path.write_bytes(base64.b64decode(payload))

base = Image.open(base_path).convert("RGBA")
patch = Image.open(patch_path).convert("RGBA")

# Work only on the central HUMAN · SYSTEMS · PERFORMANCE nucleus.
# The source is cropped to the nucleus itself; side-node fragments are excluded.
patch = patch.crop((14, 8, patch.width - 14, patch.height - 4))
target_size = (414, 414)
patch = patch.resize(target_size, Image.Resampling.LANCZOS)

# Position aligned to the existing central circle in the 1672x941 master.
x, y = 629, 66

# Feathered circular integration: pixels are baked into the master,
# never rendered as a second DOM image/canvas/overlay.
mask = Image.new("L", target_size, 0)
d = ImageDraw.Draw(mask)
d.ellipse((11, 7, target_size[0]-11, target_size[1]-7), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(5.0))

base.paste(patch, (x, y), mask)

# Save one definitive master asset.
base.convert("RGB").save(base_path, "WEBP", quality=94, method=6)

# Remove all temporary staging data.
shutil.rmtree(root / ".tmp", ignore_errors=True)
try:
    Path(__file__).unlink()
except Exception:
    pass
