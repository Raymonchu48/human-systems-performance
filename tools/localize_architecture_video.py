"""Localize the Spanish animation, preserving its geometry and label styling.
Run from the repository root. Requires opencv-python-headless, Pillow and ffmpeg.
"""
from pathlib import Path
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'assets/arquitectura-tres-planetas-cinematografico.mp4'
out=ROOT/'en/assets/arquitectura-tres-planetas-cinematografico.mp4'
cap=cv2.VideoCapture(str(source))
ok,first=cap.read()
assert ok
fps=cap.get(cv2.CAP_PROP_FPS)
fontdir='/usr/share/fonts/opentype/urw-base35/'
serif=ImageFont.truetype(fontdir+'NimbusRoman-Regular.otf',44)
bold=ImageFont.truetype(fontdir+'NimbusSans-Bold.otf',26)
small=ImageFont.truetype(fontdir+'NimbusSans-Regular.otf',11)
meta=ImageFont.truetype(fontdir+'NimbusSans-Regular.otf',12)
# Original title bounds and broad, non-overlapping motion search windows.
labels=[((167,372,336,398),(140,270,420,425),'TECHNOLOGY','SYSTEMS / INNOVATION'),
        ((790,275,912,302),(740,220,1100,400),'SPORT','HEALTH / PERFORMANCE'),
        ((734,490,897,517),(480,450,920,560),'HOSPITALITY','MANAGEMENT / EVENTS')]
templates=[cv2.cvtColor(first[y1:y2,x1:x2],cv2.COLOR_BGR2GRAY) for (x1,y1,x2,y2),_,_,_ in labels]
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','-','-an','-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
cap.set(cv2.CAP_PROP_POS_FRAMES,0)
count=0
while True:
    ok,frame=cap.read()
    if not ok: break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    mask=np.zeros(gray.shape,np.uint8)
    def erase(box,threshold=130):
        x1,y1,x2,y2=box
        crop=frame[y1:y2,x1:x2].astype(np.int16)
        # Remove glyph pixels and their thin outlines; never blank a rectangular panel.
        glyph=((crop.min(axis=2)>threshold)&((crop.max(axis=2)-crop.min(axis=2))<65)).astype(np.uint8)*255
        mask[y1:y2,x1:x2]|=glyph
    mask[84:124,70:580]=255
    mask[443:454,511:770]=255
    mask[679:696,1032:1113]=255
    positions=[]
    for ((x1,y1,x2,y2),(sx1,sy1,sx2,sy2),title,subtitle),template in zip(labels,templates):
        res=cv2.matchTemplate(gray[sy1:sy2,sx1:sx2],template,cv2.TM_CCOEFF_NORMED)
        _,score,_,point=cv2.minMaxLoc(res)
        assert score>.7,(count,title,score)
        x,y=point[0]+sx1,point[1]+sy1
        cx=x+(x2-x1)/2
        erase((x-3,y-3,x+(x2-x1)+3,y+29),140)
        half=71 if title=='TECHNOLOGY' else 66
        mask[y+34:y+48,int(cx)-half:int(cx)+half]=255
        positions.append((cx,y,title,subtitle))
    mask=cv2.dilate(mask,np.ones((5,5),np.uint8))
    clean=cv2.inpaint(frame,mask,5,cv2.INPAINT_TELEA)
    im=Image.fromarray(cv2.cvtColor(clean,cv2.COLOR_BGR2RGB))
    draw=ImageDraw.Draw(im)
    draw.text((74,87),'Three disciplines. One vision.',font=serif,fill='#eeede2',anchor='lt')
    draw.text((640,444),'STRATEGY / PEOPLE / INNOVATION',font=meta,fill='#acb3ab',anchor='mt')
    draw.text((1072,682),'360° PROFILE',font=meta,fill='#acb3ab',anchor='mt')
    for cx,y,title,subtitle in positions:
        draw.text((cx,y+3),title,font=bold,fill='#f0f2e8',anchor='mt',stroke_width=1,stroke_fill='#273026')
        draw.text((cx,y+38),subtitle,font=small,fill='#e0e4d7',anchor='mt')
    proc.stdin.write(im.tobytes())
    if count in (0,48,168): im.save('/tmp/architecture-en-%d.png'%count)
    count+=1
proc.stdin.close()
assert proc.wait()==0
assert count==192,count
print('Rendered',count,'frames,',out.stat().st_size,'bytes')
