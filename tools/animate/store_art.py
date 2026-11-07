"""Connect IQ Store art for every face, in the landing page's look (dark ground, coral label,
Bricolage Grotesque): a 1440 x 720 hero image, plus the screenshots flattened onto black.
Usage: python3 store_art.py  (from tools/animate)"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from faces import ALL
from stills import STILL
from watchkit import round_mask

FONTS = "/private/tmp/claude-501/-Users-hangryindonesia/428c9728-5e59-4914-9146-8d548c1c144a/scratchpad/brandfonts"
GROUND = (0x12, 0x12, 0x12)
CORAL = (0xFF, 0x5A, 0x36)
WHITE = (0xFA, 0xFA, 0xFA)
MUTED = (0xA3, 0xA3, 0xA3)
FOLDERS = {"running-track": "Running Track", "orbit": "Orbit", "topo-map": "Topo Map", "liquid-battery": "Liquid Battery",
           "oversize-type": "Oversize Type", "matchday": "Matchday", "pool-lanes": "Pool Lanes", "race-bib": "Race Bib",
           "summit": "Summit", "flight-path": "Flight Path"}
TAGLINES = {
    "running-track": "Your steps run a lap around the track.",
    "orbit": "The hour and minute orbit the center.",
    "topo-map": "Contour lines climb to your step goal.",
    "liquid-battery": "The screen fills to your battery level.",
    "oversize-type": "Giant numerals, cropped by the round screen.",
    "matchday": "The time on a scoreboard, over the pitch.",
    "pool-lanes": "Lane ropes, sunlit water, your last swim.",
    "race-bib": "A tilted race bib with your time on it.",
    "summit": "Your hiker climbs with every step.",
    "flight-path": "Two time zones and a plane flying your steps.",
    "sticker-bomb": "Your stats, slapped on as stickers.",
    "arcade-hud": "Your day as a retro platformer.",
    "waypoint-map": "A trail map with today's route.",
    "chess-clock": "A blitz clock, and it's your move.",
    "origami": "Folded paper, a crane and big bold time.",
    "toy-bricks": "The time, built from toy bricks.",
    "traffic-light": "Your stats glow in a city signal.",
    "shot-clock": "Game time on a courtside scoreboard.",
    "tennis-court": "Match time, seen from above the court.",
    "watermelon": "A juicy slice of summer on your wrist.",
    "jakarta": "Monas at sunset, on your wrist.",
    "singapore": "Marina Bay after dark, on your wrist.",
    "kuala-lumpur": "Twin towers at dusk, on your wrist.",
    "paris": "The Eiffel Tower at dawn, on your wrist.",
    "san-francisco": "The Golden Gate in the fog, on your wrist.",
    "sydney": "Sydney Harbour by day, on your wrist.",
}
W, H = 1440, 720


def glow(cx, cy, r):
    y, x = np.mgrid[0:H, 0:W]
    t = np.clip(1 - np.hypot(x - cx, y - cy) / r, 0, 1) ** 2
    img = np.ones((H, W, 3)) * GROUND
    img = img * (1 - 0.24 * t[..., None]) + np.array(CORAL) * 0.24 * t[..., None]
    return Image.fromarray(img.astype(np.uint8), "RGB")


def hero(key, name, face=None, tag="FORERUNNER 165  ·  WATCH FACE"):
    img = glow(1060, 360, 520).convert("RGBA")
    face = round_mask(face if face is not None else ALL[key]().render(STILL[key])).resize((560, 560), Image.LANCZOS)
    # A soft shadow under the screen
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).ellipse([780, 100, 1340, 660], fill=140)
    from PIL import ImageFilter
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img.paste((0, 0, 0, 255), (0, 18), shadow)
    img.alpha_composite(face, (780, 80))
    d = ImageDraw.Draw(img)
    label = ImageFont.truetype(f"{FONTS}/PlexMono-Medium.ttf", 22)
    title = ImageFont.truetype(f"{FONTS}/Bricolage-ExtraBold.ttf", 112)
    # A single word too long for the column (it would run into the watch) gets a smaller size
    longest = max(title.getlength(w) for w in name.split())
    if longest > 620:
        title = ImageFont.truetype(f"{FONTS}/Bricolage-ExtraBold.ttf", int(112 * 620 / longest))
    body = ImageFont.truetype(f"{FONTS}/Bricolage-Regular.ttf", 34)
    x = 96
    # Title, wrapped to two lines when long
    words, lines, line = name.split(), [], ""
    for w in words:
        test = (line + " " + w).strip()
        if title.getlength(test) > 620 and line:
            lines.append(line)
            line = w
        else:
            line = test
    lines.append(line)
    # Center the block: label, title lines, tagline and byline
    top = (H - (54 + len(lines) * 112 + 24 + 92)) // 2
    # Widely tracked coral label, drawn letter by letter
    cx = x
    for ch in tag:
        d.text((cx, top), ch, font=label, fill=CORAL)
        cx += label.getlength(ch) + 6
    y = top + 54
    for ln in lines:
        d.text((x - 4, y), ln, font=title, fill=WHITE)
        y += 112
    d.text((x, y + 24), TAGLINES[key], font=body, fill=MUTED)
    d.text((x, y + 82), "Free  ·  by Wiryana", font=body, fill=WHITE)
    return img.convert("RGB")


if __name__ == "__main__":
    for key, folder in FOLDERS.items():
        out = os.path.expanduser(f"~/WatchFaces/{folder}/store")
        hero(key, folder).save(f"{out}/hero-1440x720.png", optimize=True)
        for i in (1, 2, 3):
            path = f"{out}/screenshot-{i}.png"
            shot = Image.open(path).convert("RGBA")
            if shot.getextrema()[3][0] < 255:
                flat = Image.new("RGB", shot.size, (0, 0, 0))
                flat.paste(shot, (0, 0), shot)
                flat.save(path, optimize=True)
        print(folder, os.path.getsize(f"{out}/hero-1440x720.png") // 1024, "KB")
