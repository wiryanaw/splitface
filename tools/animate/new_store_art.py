"""Connect IQ Store art for the faces added after the first ten, in the same look as
store_art.py: the hero, a 500 x 500 cover (the face on the dark ground with a coral glow) and
three screenshots, one per color option, flattened onto black.
Usage: python3 new_store_art.py [face keys]  (from tools/animate)"""
import os
from PIL import Image
from faces import (ArcadeHUD, ChessClock, Origami, ShotClock, StickerBomb, TennisCourt, ToyBricks, TrafficLight, WaypointMap,
                   Watermelon, Jakarta, Singapore, KualaLumpur)
import sys
from store_art import glow, hero
from watchkit import round_mask

LABEL = "GARMIN  ·  WATCH FACE"
# key, store folder, face class, the three color options shown, and the values on screen
NEW = [
    ("sticker-bomb", "Sticker Bomb", StickerBomb, [0, 1, 2]),
    ("arcade-hud", "Arcade HUD", ArcadeHUD, [0, 3, 1]),
    ("waypoint-map", "Waypoint Map", WaypointMap, [0, 1, 2]),
    ("chess-clock", "Chess Clock", ChessClock, [0, 1, 2]),
    ("origami", "Origami", Origami, [0, 1, 2]),
    ("toy-bricks", "Toy Bricks", ToyBricks, [0, 1, 3]),
    ("traffic-light", "Traffic Light", TrafficLight, [0, 1, 2]),
    ("shot-clock", "Shot Clock", ShotClock, [0, 1, 2]),
    ("tennis-court", "Tennis Court", TennisCourt, [0, 1, 2]),
    ("watermelon", "Watermelon", Watermelon, [0, 1, 2]),
    ("jakarta", "Jakarta", Jakarta, [0, 1, 2]),
    ("singapore", "Singapore", Singapore, [0, 1, 2]),
    ("kuala-lumpur", "Kuala Lumpur", KualaLumpur, [0, 1, 2]),
]
SHOTS = [dict(steps=8412, hr=58, battery_level=72, minutes=608), dict(steps=12650, hr=64, battery_level=88, minutes=754),
         dict(steps=4213, hr=71, battery_level=45, minutes=1172)]


def flat(img):
    out = Image.new("RGB", img.size, (0, 0, 0))
    face = round_mask(img)
    out.paste(face, (0, 0), face)
    return out


def cover(face):
    import numpy as np
    size = 500
    y, x = np.mgrid[0:size, 0:size]
    t = np.clip(1 - np.hypot(x - 250, y - 250) / 360, 0, 1) ** 2
    ground = np.array((0x12, 0x12, 0x12))
    img = ground * (1 - 0.24 * t[..., None]) + np.array((0xFF, 0x5A, 0x36)) * 0.24 * t[..., None]
    img = Image.fromarray(img.astype(np.uint8), "RGB").convert("RGBA")
    img.alpha_composite(round_mask(face).resize((438, 438), Image.LANCZOS), (31, 31))
    return img.convert("RGB")


if __name__ == "__main__":
    # Optional face keys on the command line: only those faces
    for key, folder, cls, options in [n for n in NEW if len(sys.argv) < 2 or n[0] in sys.argv[1:]]:
        out = os.path.expanduser(f"~/WatchFaces/{folder}/store")
        os.makedirs(out, exist_ok=True)
        first = cls(options[0]).render(0, **SHOTS[0])
        hero(key, folder, first, LABEL).save(f"{out}/hero-1440x720.png", optimize=True)
        cover(first).save(f"{out}/cover-500x500.png", optimize=True)
        for i, (option, values) in enumerate(zip(options, SHOTS), 1):
            flat(cls(option).render(0, **values)).save(f"{out}/screenshot-{i}.png", optimize=True)
        print(folder, {f: os.path.getsize(f"{out}/{f}") // 1024 for f in os.listdir(out) if f.endswith(".png")})
