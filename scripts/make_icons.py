"""Builds Android launcher icons from www/assets/icon.png (run by the GitHub workflow)."""
import os, sys
from PIL import Image, ImageChops

SRC = "www/assets/icon.png"
RES = "android/app/src/main/res"
SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

img = Image.open(SRC).convert("RGBA")
bbox = img.getchannel("A").point(lambda a: 255 if a > 10 else 0).getbbox()
if bbox is None or bbox == (0, 0, img.width, img.height):
    bg = Image.new("RGBA", img.size, img.getpixel((0, 0)))
    bbox = ImageChops.difference(img, bg).convert("L").point(lambda p: 255 if p > 25 else 0).getbbox()
if bbox:
    img = img.crop(bbox)
side = max(img.size)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))

for name, px in SIZES.items():
    d = os.path.join(RES, f"mipmap-{name}")
    os.makedirs(d, exist_ok=True)
    out = canvas.resize((px, px), Image.LANCZOS)
    for f in ("ic_launcher.png", "ic_launcher_round.png", "ic_launcher_foreground.png"):
        out.save(os.path.join(d, f))

print("Icons written for", ", ".join(SIZES))
