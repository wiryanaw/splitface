"""The still shown before a face plays: each face at a representative moment of its loop.
Usage: python3 stills.py [face ...]  (from tools/animate; no names renders every face)"""
import sys
from faces import ALL
from watchkit import round_mask

STILL = {"running-track": 0.55, "orbit": 8 / 60, "topo-map": 0.0, "liquid-battery": 0.4, "oversize-type": 0.3,
         "matchday": 0.0, "pool-lanes": 0.0, "race-bib": 0.0, "summit": 0.72, "flight-path": 0.43,
         "sticker-bomb": 0.0, "arcade-hud": 0.0, "waypoint-map": 0.0, "chess-clock": 0.0, "origami": 0.0,
         "toy-bricks": 0.0, "traffic-light": 0.0, "shot-clock": 0.0, "tennis-court": 0.0, "watermelon": 0.0,
         "jakarta": 0.0, "singapore": 0.0, "kuala-lumpur": 0.0}

if __name__ == "__main__":
    for name in sys.argv[1:] or ALL:
        cls = ALL[name]
        round_mask(cls().render(STILL[name])).save(f"../../public/faces/{name}-still.webp", quality=88, method=6)
