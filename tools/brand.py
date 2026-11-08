"""Splitface brand art: the favicon (a round watch screen split into a coral and a white half,
nudged apart like a split time) and the 1200 x 630 social banner.
Writes app/icon.svg, app/favicon.ico, app/apple-icon.png and public/og.png.
Usage: python3 tools/brand.py  (from the project folder)"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
GROUND = (0x12, 0x12, 0x12)
CORAL = (0xFF, 0x5A, 0x36)
WHITE = (0xFA, 0xFA, 0xFA)
MUTED = (0xA3, 0xA3, 0xA3)

# The mark on a 64 unit grid: a dark disc, and inside it two half discs split by a gap,
# the right half dropped a little like a split on a lap timer
SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="31" fill="#121212"/>
  <path d="M30 12 A20 20 0 0 0 30 52 Z" fill="#FF5A36"/>
  <path d="M34 15 A20 20 0 0 1 34 55 Z" fill="#FAFAFA"/>
</svg>
"""


def mark(size, s=8):
    """The mark as an RGBA image, drawn supersampled."""
    big = size * s
    u = big / 64
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([1 * u, 1 * u, 63 * u, 63 * u], fill=GROUND + (255,))
    # Left half: centered at (30, 32), radius 20, the half left of x = 30
    d.pieslice([10 * u, 12 * u, 50 * u, 52 * u], 90, 270, fill=CORAL + (255,))
    # Right half: centered at (34, 35), radius 20, the half right of x = 34
    d.pieslice([14 * u, 15 * u, 54 * u, 55 * u], 270, 90, fill=WHITE + (255,))
    return img.resize((size, size), Image.LANCZOS)


def banner():
    sys.path.insert(0, os.path.join(ROOT, "tools", "animate"))
    from faces import ALL
    from stills import STILL
    from watchkit import round_mask
    import numpy as np

    W, H = 1200, 630
    y, x = np.mgrid[0:H, 0:W]
    t = np.clip(1 - np.hypot(x - 960, y - 330) / 520, 0, 1) ** 2
    ground = np.ones((H, W, 3)) * GROUND
    ground = ground * (1 - 0.26 * t[..., None]) + np.array(CORAL) * 0.26 * t[..., None]
    img = Image.fromarray(ground.astype(np.uint8), "RGB").convert("RGBA")

    # A fan of faces on the right: one large at the center, two smaller behind it
    layout = [("liquid-battery", 190, 840, 200), ("summit", 190, 1090, 200), ("running-track", 290, 965, 150)]
    for key, size, cx, cy in layout:
        face = round_mask(ALL[key]().render(STILL[key])).resize((size, size), Image.LANCZOS)
        shadow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shadow).ellipse([cx - size / 2, cy + 14, cx + size / 2, cy + size + 14], fill=150)
        img.paste((0, 0, 0, 255), (0, 0), shadow.filter(ImageFilter.GaussianBlur(22)))
        img.alpha_composite(face, (int(cx - size / 2), int(cy)))

    d = ImageDraw.Draw(img)
    label = ImageFont.truetype(f"{FONTS}/PlexMono-Medium.ttf", 20)
    title = ImageFont.truetype(f"{FONTS}/Bricolage-ExtraBold.ttf", 66)
    body = ImageFont.truetype(f"{FONTS}/Bricolage-Regular.ttf", 28)
    logo = mark(56)
    img.alpha_composite(logo, (72, 120))
    d.text((142, 128), "Splitface", font=ImageFont.truetype(f"{FONTS}/Bricolage-ExtraBold.ttf", 40), fill=WHITE)
    cx = 72
    for ch in "FREE GARMIN WATCH FACES":
        d.text((cx, 232), ch, font=label, fill=CORAL)
        cx += label.getlength(ch) + 5
    for i, line in enumerate(["Give your watch", "a better face."]):
        d.text((68, 278 + i * 70), line, font=title, fill=WHITE)
    d.text((72, 452), "51 Garmin watches  ·  by Wiryana", font=body, fill=MUTED)
    return img.convert("RGB")


open(os.path.join(ROOT, "app", "icon.svg"), "w").write(SVG)
mark(256).save(os.path.join(ROOT, "app", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
apple = Image.new("RGBA", (180, 180), GROUND + (255,))
apple.alpha_composite(mark(150), (15, 15))
apple.convert("RGB").save(os.path.join(ROOT, "app", "apple-icon.png"))
banner().save(os.path.join(ROOT, "public", "og.png"), optimize=True)
mark(512).save(os.path.join(ROOT, "public", "splitface-mark.png"))
print("ok")
