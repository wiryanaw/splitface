"""The looping previews that play on hover: 60 frames at 15 fps per face.
Usage: python3 animate.py [face ...]  (from tools/animate; no names renders every face)"""
import sys
from faces import ALL
from watchkit import save_loop

for name in sys.argv[1:] or ALL:
    face = ALL[name]()
    save_loop([face.render(k / 60) for k in range(60)], f"../../public/faces/{name}.webp", fps=15)
