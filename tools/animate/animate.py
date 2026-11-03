"""The looping previews that play on hover: 60 frames at 15 fps per face.
Usage: python3 animate.py  (from tools/animate)"""
from faces import ALL
from watchkit import save_loop

for name, cls in ALL.items():
    face = cls()
    save_loop([face.render(k / 60) for k in range(60)], f"../../public/faces/{name}.webp", fps=15)
