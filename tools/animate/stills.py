"""The still shown before a face plays: each face at a representative moment of its loop.
Usage: python3 stills.py  (from tools/animate)"""
from faces import ALL
from watchkit import round_mask

STILL = {"running-track": 0.55, "orbit": 8 / 60, "topo-map": 0.0, "liquid-battery": 0.4, "oversize-type": 0.3,
         "matchday": 0.0, "pool-lanes": 0.0, "race-bib": 0.0, "summit": 0.72, "flight-path": 0.43}

for name, cls in ALL.items():
    round_mask(cls().render(STILL[name])).save(f"../../public/faces/{name}-still.webp", quality=88, method=6)
