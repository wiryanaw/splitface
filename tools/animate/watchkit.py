"""Shared pieces for rendering face previews off the watch, with the same art the watch draws.

A face project's smooth fonts are read from its own generated files (source/SmoothFonts.mc for
each font's sheets and colors, resources/drawables and resources/jsonData for the images and
metrics), and drawn glyph by glyph exactly as SmoothFont.mc does: the sheet's on or off alpha
copied through each glyph's box. Shapes the watch draws in code (rings, lines, the battery
icon) are drawn here supersampled, so the previews are smooth."""
import json
import math
import os
import re
from PIL import Image, ImageDraw

HOME = os.path.expanduser("~")
N = 390


def rgb(c):
    return ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)


def blend(a, b, amount):
    """Mix color a over b by amount (0 to 1), as the faces do by hand."""
    ca, cb = rgb(a), rgb(b)
    return tuple(round(x * amount + y * (1 - amount)) for x, y in zip(ca, cb))


class Font:
    def __init__(self, sheets, palette, metrics):
        self.sheets = sheets
        self.palette = palette
        self.chars = metrics["chars"]
        self.m = metrics["m"]
        self.base = metrics["base"]
        self.height = metrics["height"]

    def width(self, text):
        return sum(self.m[self.chars.find(ch) * 7 + 6] for ch in text if self.chars.find(ch) >= 0)

    def sheet(self, color):
        return self.sheets[self.palette.index(color)] if color in self.palette else self.sheets[0]

    def draw(self, img, x, y, text, color, justify="left", vcenter=False, clip=None):
        """Same justification as Dc.drawText: y is the line box top unless vcenter."""
        sheet = self.sheet(color)
        if justify == "center":
            x -= self.width(text) // 2
        elif justify == "right":
            x -= self.width(text)
        if vcenter:
            y -= self.height // 2
        for ch in text:
            i = self.chars.find(ch)
            if i < 0:
                continue
            px, py, w, h, xoff, yoff, adv = self.m[i * 7:i * 7 + 7]
            if w > 0:
                self._blit(img, sheet, px, py, w, h, x + xoff, y + yoff, clip)
            x += adv

    def draw_along(self, img, x, y, text, color, dx, dy):
        """Text rendered at a tilt: the pen steps along (dx, dy) per pixel of advance."""
        sheet = self.sheet(color)
        for ch in text:
            i = self.chars.find(ch)
            if i < 0:
                continue
            px, py, w, h, xoff, yoff, adv = self.m[i * 7:i * 7 + 7]
            if w > 0:
                self._blit(img, sheet, px, py, w, h, round(x) + xoff, round(y) + yoff, None)
            x += adv * dx
            y += adv * dy

    @staticmethod
    def _blit(img, sheet, px, py, w, h, left, top, clip):
        glyph = sheet.crop((px, py, px + w, py + h))
        if clip:
            cx, cy, cw, ch = clip
            x0, y0 = max(left, cx), max(top, cy)
            x1, y1 = min(left + w, cx + cw), min(top + h, cy + ch)
            if x1 <= x0 or y1 <= y0:
                return
            glyph = glyph.crop((x0 - left, y0 - top, x1 - left, y1 - top))
            left, top = x0, y0
        img.paste(glyph, (left, top), glyph)


class Project:
    """One face project: its fonts and bitmaps by the ids the face code uses."""

    def __init__(self, folder):
        self.root = os.path.join(HOME, folder)
        res = os.path.join(self.root, "resources")
        self.files = {}
        for xml in ("drawables/drawables.xml", "drawables/smooth_fonts.xml"):
            path = os.path.join(res, xml)
            if os.path.exists(path):
                for ident, name in re.findall(r'<bitmap id="(\w+)" filename="([^"]+)"', open(path).read()):
                    self.files[ident] = os.path.join(res, "drawables", name)
        self.json = {}
        path = os.path.join(res, "jsonData", "jsonData.xml")
        if os.path.exists(path):
            for ident, name in re.findall(r'<jsonData id="(\w+)" filename="([^"]+)"', open(path).read()):
                self.json[ident] = os.path.join(res, "jsonData", name)
        self.fonts = {}
        source = open(os.path.join(self.root, "source", "SmoothFonts.mc")).read()
        ids = dict(re.findall(r"const (\w+) = (\d+);", source))
        for case, sheets, palette, metrics in re.findall(
                r"case (\w+):\s*return new SmoothFont\(\[([^\]]*)\], \[([^\]]*)\], Rez\.JsonData\.(\w+)\);", source):
            sheet_ids = [s.strip().replace("Rez.Drawables.", "") for s in sheets.split(",")]
            colors = [int(c.strip(), 16) for c in palette.split(",")]
            self.fonts[case] = (sheet_ids, colors, metrics)
        self._loaded = {}
        self._bitmaps = {}

    def font(self, name):
        if name not in self._loaded:
            sheet_ids, colors, metrics = self.fonts[name]
            sheets = [Image.open(self.files[s]).convert("RGBA") for s in sheet_ids]
            self._loaded[name] = Font(sheets, colors, json.load(open(self.json[metrics])))
        return self._loaded[name]

    def bitmap(self, ident):
        if ident not in self._bitmaps:
            self._bitmaps[ident] = Image.open(self.files[ident]).convert("RGBA")
        return self._bitmaps[ident]

    def blit(self, img, ident, x, y):
        b = self.bitmap(ident)
        img.paste(b, (round(x), round(y)), b)


class Shapes:
    """A 4x supersampled layer for shapes the watch draws in code, composited when done."""

    S = 4

    def __init__(self):
        self.layer = Image.new("RGBA", (N * self.S, N * self.S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.layer)

    def _p(self, v):
        return v * self.S

    def line(self, pts, width, color):
        s = self.S
        self.d.line([(x * s, y * s) for x, y in pts], fill=color + (255,), width=round(width * s), joint="curve")
        r = width * s / 2
        for x, y in (pts[0], pts[-1]):
            self.d.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=color + (255,))

    def arc(self, cx, cy, r, start, end, width, color):
        """Clockwise from start to end in degrees, 0 at 3 o'clock (PIL's convention)."""
        s = self.S
        h = width * s / 2
        self.d.arc([(cx - r) * s - h, (cy - r) * s - h, (cx + r) * s + h, (cy + r) * s + h], start, end, fill=color + (255,), width=round(width * s))

    def circle(self, cx, cy, r, color):
        s = self.S
        self.d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=color + (255,))

    def ring(self, cx, cy, r, width, color):
        self.arc(cx, cy, r, 0, 360, width, color)

    def rect(self, x, y, w, h, color):
        s = self.S
        self.d.rectangle([x * s, y * s, (x + w) * s - 1, (y + h) * s - 1], fill=color + (255,))

    def rounded(self, x, y, w, h, r, width, color):
        """An outlined rounded rectangle, like Dc.drawRoundedRectangle."""
        s = self.S
        hw = width * s / 2
        x0, y0, x1, y1 = x * s + hw, y * s + hw, (x + w) * s - hw, (y + h) * s - hw
        rr = r * s
        col = color + (255,)
        ws = round(width * s)
        self.d.line([(x0 + rr, y0), (x1 - rr, y0)], fill=col, width=ws)
        self.d.line([(x0 + rr, y1), (x1 - rr, y1)], fill=col, width=ws)
        self.d.line([(x0, y0 + rr), (x0, y1 - rr)], fill=col, width=ws)
        self.d.line([(x1, y0 + rr), (x1, y1 - rr)], fill=col, width=ws)
        for cx, cy, a in ((x0 + rr, y0 + rr, 180), (x1 - rr, y0 + rr, 270), (x1 - rr, y1 - rr, 0), (x0 + rr, y1 - rr, 90)):
            self.d.arc([cx - rr - ws / 2, cy - rr - ws / 2, cx + rr + ws / 2, cy + rr + ws / 2], a, a + 90, fill=col, width=ws)

    def filled_rounded(self, x, y, w, h, r, color):
        s = self.S
        x0, y0, x1, y1, rr = x * s, y * s, (x + w) * s, (y + h) * s, r * s
        col = color + (255,)
        self.d.rectangle([x0 + rr, y0, x1 - rr, y1], fill=col)
        self.d.rectangle([x0, y0 + rr, x1, y1 - rr], fill=col)
        for cx, cy in ((x0 + rr, y0 + rr), (x1 - rr, y0 + rr), (x0 + rr, y1 - rr), (x1 - rr, y1 - rr)):
            self.d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)

    def onto(self, img):
        small = self.layer.resize((N, N), Image.LANCZOS)
        img.alpha_composite(small)


def battery(shapes, x, y, level, color, w=21, h=12, inner=15, fill_h=6, inset=3):
    """The battery icon the faces draw: an outline and a fill that follows the charge."""
    shapes.rounded(x, y, w, h, 2, 2, color)
    filled = int(inner * level / 100)
    if filled > 0:
        shapes.rect(x + inset, y + inset, filled, fill_h, color)


def thousands(v):
    return f"{v:,}"


def clock(minutes):
    return f"{(minutes // 60) % 24:02d}:{minutes % 60:02d}"


def ease(t):
    """Smooth in and out, for values that glide between holds."""
    return t * t * (3 - 2 * t)


def keyframes(t, frames):
    """Value at loop time t (0 to 1) along [(time, value), ...], easing between keys."""
    for (t0, v0), (t1, v1) in zip(frames, frames[1:]):
        if t0 <= t <= t1:
            k = 0 if t1 == t0 else ease((t - t0) / (t1 - t0))
            return v0 + (v1 - v0) * k
    return frames[-1][1]


def round_mask(img):
    mask = Image.new("L", (N * 4, N * 4), 0)
    ImageDraw.Draw(mask).ellipse([2, 2, N * 4 - 3, N * 4 - 3], fill=255)
    out = img.copy()
    out.putalpha(mask.resize((N, N), Image.LANCZOS))
    return out


def save_loop(frames, path, fps=15):
    frames = [round_mask(f) for f in frames]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=round(1000 / fps), loop=0, quality=82, method=4)
