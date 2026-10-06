from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from urllib.request import urlretrieve
from pathlib import Path
import numpy as np
import cv2

root=Path(__file__).resolve().parents[1]
master=root/"assets"/"cluster-approved.webp"
srcfile=root/".it.jpg"
urlretrieve("https://d2ol7oe51mr4n9.cloudfront.net/user_3IHAZtjGdFzomzk5Pp0lAW9zg6A/94746310-7c1c-4281-be3e-1cc7c81464b4.jpg",srcfile)

base=Image.open(master).convert("RGBA")
src=cv2.imread(str(srcfile))
h,w=src.shape[:2]

mask=np.zeros((h,w),np.uint8)
bg=np.zeros((1,65),np.float64)
fg=np.zeros((1,65),np.float64)
rect=(470,120,w-480,h-125)
cv2.grabCut(src,mask,rect,bg,fg,6,cv2.GC_INIT_WITH_RECT)
alpha=np.where((mask==2)|(mask==0),0,255).astype("uint8")
alpha=cv2.GaussianBlur(alpha,(0,0),2.2)

rgba=cv2.cvtColor(src,cv2.COLOR_BGR2RGBA)
person=Image.fromarray(rgba)
a=Image.fromarray(alpha)
person.putalpha(a)

bbox=a.getbbox()
person=person.crop(bbox)

target_h=345
target_w=int(person.width*target_h/person.height)
person=person.resize((target_w,target_h),Image.Resampling.LANCZOS)

# Build server-room continuation from the native Technology background.
out=base.copy()
patch=base.crop((1090,175,1325,505)).convert("RGB")
patch=patch.resize((280,330),Image.Resampling.LANCZOS)
patch=ImageEnhance.Brightness(patch).enhance(.92).convert("RGBA")

fillmask=Image.new("L",base.size,0)
fd=ImageDraw.Draw(fillmask)
fd.rounded_rectangle((1220,165,1505,510),radius=35,fill=255)
fillmask=fillmask.filter(ImageFilter.GaussianBlur(16))

fill=Image.new("RGBA",base.size,(0,0,0,0))
fill.paste(patch,(1220,175))
out=Image.composite(fill,out,fillmask)

# Place the cutout naturally left of the native card column.
x=1195
y=165
person=ImageEnhance.Brightness(person).enhance(.90)
blue=Image.new("RGBA",person.size,(0,28,55,18))
person=Image.alpha_composite(person,blue)
out.alpha_composite(person,(x,y))

# Restore native HUD, cards, IT node and lower quote exactly.
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
