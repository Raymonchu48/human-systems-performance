from PIL import Image
from pathlib import Path
import urllib.request

root=Path(__file__).resolve().parents[1]
master_path=root/"assets"/"cluster-approved.webp"
ref_path=root/".approved-tech.png"

urllib.request.urlretrieve(
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/be4a4b86-b71f-42d9-ac27-d8fb18102ee9.png",
    ref_path
)

master=Image.open(master_path).convert("RGBA")
ref=Image.open(ref_path).convert("RGBA")

# Exact approved Technology crop from the user-approved reference.
crop=ref.crop((1280,110,2035,660))

# Exact Technology region in the 1672x941 cluster master.
target=(1065,75,1672,517)
crop=crop.resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.LANCZOS)

# Rewrite the region directly into the master. No extra DOM layer/canvas/image.
master.paste(crop,(target[0],target[1]))
master.convert("RGB").save(master_path,"WEBP",quality=95,method=6)

ref_path.unlink(missing_ok=True)
try: Path(__file__).unlink()
except Exception: pass
