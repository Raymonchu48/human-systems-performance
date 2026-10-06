from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
from urllib.request import urlretrieve
from pathlib import Path

root=Path(__file__).resolve().parents[1]
master=root/"assets"/"cluster-approved.webp"
srcfile=root/".it.jpg"
urlretrieve("https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",srcfile)

base=Image.open(master).convert("RGBA")
src=Image.open(srcfile).convert("RGB")
photo=ImageOps.fit(src,(455,355),Image.Resampling.LANCZOS,centering=(0.54,0.48))
photo=ImageEnhance.Brightness(photo).enhance(.72)
photo=ImageEnhance.Contrast(photo).enhance(1.08)
photo=ImageEnhance.Color(photo).enhance(.86).convert("RGBA")
photo=Image.alpha_composite(photo,Image.new("RGBA",photo.size,(0,35,68,48)))

layer=Image.new("RGBA",base.size,(0,0,0,0))
layer.paste(photo,(1065,155))

mask=Image.new("L",base.size,0)
d=ImageDraw.Draw(mask)
d.rounded_rectangle((1055,145,1525,515),radius=40,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(18))
out=Image.composite(layer,base,mask)

# Preserve native HUD/UI from the original cluster.
keep=Image.new("L",base.size,0)
k=ImageDraw.Draw(keep)
k.rectangle((1050,75,1672,175),fill=255)
k.rectangle((1460,90,1672,410),fill=255)
k.rectangle((1300,420,1672,515),fill=255)
k.ellipse((955,195,1138,382),fill=255)
keep=keep.filter(ImageFilter.GaussianBlur(2))
out=Image.composite(base,out,keep)

out.convert("RGB").save(master,"WEBP",quality=95,method=6)
srcfile.unlink(missing_ok=True)
