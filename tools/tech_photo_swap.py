from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
from urllib.request import urlretrieve
from pathlib import Path

root=Path(__file__).resolve().parents[1]
master=root/"assets"/"cluster-approved.webp"
srcfile=root/".it.jpg"
urlretrieve("https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",srcfile)

base=Image.open(master).convert("RGBA")
src=Image.open(srcfile).convert("RGB")

# Widen the source to the right so the profile moves left,
# matching the approved Technology composition.
ext=Image.new("RGB",(src.width+520,src.height),(3,16,28))
ext.paste(src,(0,0))
edge=src.crop((src.width-180,0,src.width,src.height))
edge=edge.resize((520,src.height),Image.Resampling.LANCZOS)
edge=edge.filter(ImageFilter.GaussianBlur(20))
edge=ImageEnhance.Brightness(edge).enhance(.45)
ext.paste(edge,(src.width,0))

photo=ImageOps.fit(ext,(470,375),Image.Resampling.LANCZOS,centering=(0.50,0.48))
photo=ImageEnhance.Brightness(photo).enhance(.80)
photo=ImageEnhance.Contrast(photo).enhance(1.08)
photo=ImageEnhance.Color(photo).enhance(.88).convert("RGBA")
photo=Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,35,68,44)))

layer=Image.new("RGBA",base.size,(0,0,0,0))
layer.paste(photo,(1055,135))

mask=Image.new("L",base.size,0)
d=ImageDraw.Draw(mask)
d.rounded_rectangle((1045,125,1530,520),radius=44,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(18))
out=Image.composite(layer,base,mask)

# Preserve the cluster's native Technology HUD/UI.
keep=Image.new("L",base.size,0)
k=ImageDraw.Draw(keep)
k.rectangle((1040,75,1672,175),fill=255)
k.rectangle((1460,90,1672,410),fill=255)
k.rectangle((1300,420,1672,515),fill=255)
k.ellipse((955,195,1138,382),fill=255)
keep=keep.filter(ImageFilter.GaussianBlur(2))
out=Image.composite(base,out,keep)

out.convert("RGB").save(master,"WEBP",quality=95,method=6)
srcfile.unlink(missing_ok=True)
