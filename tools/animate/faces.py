"""One renderer per face: render(t) draws the face at loop time t (0 to 1) from the face's own
art and layout code (each mirrors that project's source/FaceView.mc), with the value that
drives the face (steps, battery, time) moving through the loop."""
import json
import math
import os
from PIL import Image, ImageDraw
from watchkit import N, Project, Shapes, battery, blend, clock, keyframes, rgb, thousands

DATE = "TUE 03 NOV"


def heart_rate(t, base=62):
    """A resting pulse that drifts a little over the loop."""
    return base + round(4 * math.sin(t * math.tau * 2))


# ---------------------------------------------------------------- Running Track (FR165Face)
class RunningTrack:
    """Steps fill the lap from the start line to the step goal."""

    TRACK, RUNNER = 0xC2452D, 0xFFD23F
    GROUND, INFIELD, LABEL, WHITE = 0x10140F, 0x1F7A4D, 0xA9B3A6, 0xFAFAFA

    def __init__(self):
        self.p = Project("FR165Face")
        shapes = Shapes()
        shapes.filled_rounded(34, 98, 322, 194, 97, rgb(self.TRACK))
        for i in range(3):
            inset = 12 * (i + 1)
            shapes.rounded(34 + inset, 98 + inset, 322 - inset * 2, 194 - inset * 2, 97 - inset, 1, blend(0xFFFFFF, self.TRACK, 0.7))
        shapes.filled_rounded(82, 146, 226, 98, 49, rgb(self.INFIELD))
        shapes.line([(195, 98), (195, 146)], 3, (255, 255, 255))
        self.base = Image.new("RGBA", (N, N), rgb(self.GROUND) + (255,))
        shapes.onto(self.base)

    def lap(self, shapes, amount):
        bend = math.pi * 91
        lengths = [64, bend, 128, bend, 64]
        remaining = sum(lengths) * amount
        color = rgb(self.RUNNER)
        x, y = 195.0, 104.0
        for i, length in enumerate(lengths):
            if remaining <= 0:
                break
            run = min(remaining, length)
            remaining -= run
            if i in (0, 4):
                x0 = 195 if i == 0 else 131
                shapes.line([(x0, 104), (x0 + run, 104)], 7, color)
                x, y = x0 + run, 104.0
            elif i == 2:
                shapes.line([(259, 286), (259 - run, 286)], 7, color)
                x, y = 259 - run, 286.0
            else:
                cx = 259 if i == 1 else 131
                start = 270 if i == 1 else 90
                deg = math.degrees(run / 91)
                shapes.arc(cx, 195, 91, start, start + deg, 7, color)
                a = math.radians(start + deg)
                x, y = cx + 91 * math.cos(a), 195 + 91 * math.sin(a)
                shapes.circle(x, y, 3.5, color)
        shapes.circle(x, y, 10, color)
        shapes.circle(x, y, 6, (255, 255, 255))

    def render(self, t):
        goal = 10000
        steps = round(keyframes(t, [(0, 0), (0.85, goal), (1, goal)]))
        img = self.base.copy()
        shapes = Shapes()
        self.lap(shapes, steps / goal)
        top = self.p.font("TRACK_TOP")
        bat = 78
        label = f"{bat}%"
        left = 195 - (top.width(DATE) + 16 + 21 + 5 + top.width(label)) // 2
        icon = left + top.width(DATE) + 16
        battery(shapes, icon, 53, bat, rgb(self.WHITE))
        shapes.onto(img)
        top.draw(img, left, 48, DATE, self.WHITE)
        top.draw(img, icon + 26, 48, label, self.WHITE)
        self.p.font("TRACK_TIME").draw(img, 195, 150, "10:08", self.WHITE, "center")
        sf, lf = self.p.font("TRACK_STEPS"), self.p.font("TRACK_LABEL")
        text = thousands(steps)
        sl = 195 - (sf.width(text) + 6 + lf.width("STEPS")) // 2
        sf.draw(img, sl, 300, text, self.RUNNER)
        lf.draw(img, sl + sf.width(text) + 6, 312, "STEPS", self.LABEL)
        hf = self.p.font("TRACK_HEART")
        hr = str(heart_rate(t, 72))
        hl = 195 - (18 + 6 + hf.width(hr)) // 2
        self.p.blit(img, "IconTrackHeart", hl, 338)
        hf.draw(img, hl + 24, 332, hr, self.WHITE)
        return img


# ---------------------------------------------------------------- Liquid Battery (LiquidFace)
class LiquidBattery:
    """The liquid follows the battery: full, then 72%, then 35%, then charging back up."""

    DARK, LIGHT, TOP, LABEL = 0x07080F, 0xE6E9F5, 0x4FF0C8, 0x9AA0B8

    def __init__(self):
        self.p = Project("LiquidFace")
        src = open(f"{self.p.root}/source/LiquidSurface.mc").read()
        self.strip = int(src.split("STRIP = ")[1].split(";")[0])
        self.surface = [int(v) for v in src.split("Y = [")[1].split("]")[0].split(",")]

    @staticmethod
    def offset(b):
        return int((72 - b) * 290 / 72) if b <= 72 else -int((b - 72) * 8 / 28)

    def two_tone(self, img, dark_id, light_id, top, text, offset):
        dark, light = self.p.font(dark_id), self.p.font(light_id)
        width = dark.width(text)
        left = 195 - width // 2
        bottom = top + dark.height
        x = left - left % self.strip
        while x < left + width:
            i = x // self.strip
            water = (self.surface[i] if 0 <= i < len(self.surface) else 390) + offset
            if water > top:
                light.draw(img, left, top, text, self.LIGHT, clip=(x, top, self.strip, water - top))
            if water < bottom:
                start = max(water, top)
                dark.draw(img, left, top, text, self.DARK, clip=(x, start, self.strip, bottom - start))
            x += self.strip

    def render(self, t):
        b = round(keyframes(t, [(0, 100), (0.12, 100), (0.32, 72), (0.48, 72), (0.68, 35), (0.8, 35), (1, 100)]))
        img = Image.new("RGBA", (N, N), rgb(self.DARK) + (255,))
        off = self.offset(b)
        if 84 + off < 390:
            self.p.blit(img, "Liquid", 0, 84 + off)
        pct, label = self.p.font("LIQ_PCT"), self.p.font("LIQ_LABEL")
        text = f"{b}%"
        left = 195 - (pct.width(text) + 6 + label.width("BATTERY")) // 2
        pct.draw(img, left, 44, text, self.TOP)
        label.draw(img, left + pct.width(text) + 6, 62, "BATTERY", self.LABEL)
        self.two_tone(img, "LIQ_DATE_DARK", "LIQ_DATE_LIGHT", 138, DATE, off)
        self.two_tone(img, "LIQ_TIME_DARK", "LIQ_TIME_LIGHT", 143, "10:08", off)
        self.two_tone(img, "LIQ_STEPS_DARK", "LIQ_STEPS_LIGHT", 272, f"8,412 steps · ♥ {heart_rate(t, 58)}", off)
        return img


def orbit_point(radius, angle):
    a = math.radians(angle)
    return round(195 + radius * math.sin(a)), round(195 - radius * math.cos(a))


# ---------------------------------------------------------------- Orbit (OrbitFace)
class Orbit:
    """An hour passes: the planet laps its orbit, the sun creeps on, steps fill the ring."""

    WHITE, DATE, INFO, STEPS = 0xFFFFFF, 0x9EA3D6, 0xD5D8F5, 0xB7F36B
    HOUR, MINUTE, GROUND, TRACK = 0xFF8A3D, 0x6EC8FF, 0x0F1026, 0x1E2040

    def __init__(self):
        self.p = Project("OrbitFace")

    def render(self, t):
        minutes = 10 * 60 + int(t * 60) % 60
        steps = round(keyframes(t, [(0, 3200), (1, 9600)]))
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "Background", 0, 0)
        minute_angle = (minutes % 60) * 6.0
        hour_angle = ((minutes // 60) % 12 + (minutes % 60) / 60) * 30
        s = Shapes()
        sweep = 360 * steps / 10000
        s.arc(195, 195, 178, 270, 270 + sweep, 6, blend(self.STEPS, self.TRACK, 0.45))
        s.arc(195, 195, 178, 270, 270 + sweep, 4, rgb(self.STEPS))
        s.circle(195, 17, 2, rgb(self.STEPS))
        s.circle(*orbit_point(178, sweep), 2, rgb(self.STEPS))
        if minute_angle >= 1:
            s.arc(195, 195, 140, 270, 270 + minute_angle, 2, blend(self.MINUTE, self.GROUND, 0.5))
        s.arc(195, 195, 80, 270, 270 + hour_angle, 2, blend(self.HOUR, self.GROUND, 0.4))
        info = self.p.font("ORBIT_INFO")
        hr, st, bat = str(heart_rate(t, 58)), thousands(steps) + " steps", "72%"
        hw, sw = 16 + info.width(hr), info.width(st)
        x = 195 - (hw + 18 + sw + 18 + 26 + info.width(bat)) // 2
        battery(s, x + hw + 18 + sw + 18, 287, 72, rgb(self.INFO))
        s.onto(img)
        hx, hy = orbit_point(80, hour_angle)
        self.p.blit(img, "PlanetHour", hx - 22, hy - 22)
        mx, my = orbit_point(140, minute_angle)
        self.p.blit(img, "PlanetMinute", mx - 16, my - 16)
        self.p.font("ORBIT_TIME").draw(img, 195, 150, clock(minutes), self.WHITE, "center")
        self.p.font("ORBIT_DATE").draw(img, 195, 212, DATE, self.DATE, "center")
        self.p.blit(img, "IconHeart", x, 287)
        info.draw(img, x + 16, 284, hr, self.INFO)
        info.draw(img, x + hw + 18, 284, st, self.STEPS)
        info.draw(img, x + hw + 18 + sw + 18 + 26, 284, bat, self.INFO)
        return img


# ---------------------------------------------------------------- Topo Map (TopoFace)
class TopoMap:
    """Minutes tick by and steps add up toward the goal marked on the map."""

    WHITE, GROUND, DATE, INFO, ROUTE = 0xFFFFFF, 0x0A1A14, 0x9FC7B2, 0xD9EFE3, 0xFF7A3D

    def __init__(self):
        self.p = Project("TopoFace")

    def render(self, t):
        minutes = 10 * 60 + 8 + int(t * 12)
        steps = round(keyframes(t, [(0, 6800), (1, 9200)]))
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgTopo00", 0, 0)
        self.p.font("TOPO_GOAL").draw(img, 260, 104, "▲ GOAL 10K", self.ROUTE)
        self.p.font("TOPO_DATE").draw(img, 52, 150, "TUE · 03 NOV", self.DATE)
        time = self.p.font("TOPO_TIME")
        time.draw(img, 52, 154, clock(minutes), self.GROUND)
        time.draw(img, 52, 154, clock(minutes), self.WHITE)
        info = self.p.font("TOPO_INFO")
        heart, st, bat = f"♥ {heart_rate(t, 58)}", thousands(steps) + " STEPS", "72%"
        x = 195 - (info.width(heart) + 18 + info.width(st) + 18 + 26 + info.width(bat)) // 2
        info.draw(img, x, 296, heart, self.INFO)
        x += info.width(heart) + 18
        info.draw(img, x, 296, st, self.INFO)
        x += info.width(st) + 18
        s = Shapes()
        battery(s, x, 299, 72, rgb(self.INFO))
        s.onto(img)
        info.draw(img, x + 26, 296, bat, self.INFO)
        return img


# ---------------------------------------------------------------- Matchday (MatchdayFace)
class Matchday:
    """The match clock runs on the scoreboard while steps add up."""

    WHITE, BOARD, INK = 0xFFFFFF, 0x0D0F14, 0x111111

    def __init__(self):
        self.p = Project("MatchdayFace")

    def render(self, t):
        minutes = 10 * 60 + 8 + int(t * 12)
        steps = round(keyframes(t, [(0, 7400), (1, 9300)]))
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgPitch00", 0, 0)
        info = self.p.font("MD_INFO_0")
        st = thousands(steps)
        left = 195 - (info.width(st) + 6 + info.width("STEPS")) // 2
        info.draw(img, left, 58, st, self.WHITE)
        info.draw(img, left + info.width(st) + 6, 58, "STEPS", info.palette[1])
        day = self.p.font("MD_DAY_0")
        day.draw(img, 58 + 49 // 2, 175, "TUE", self.INK, "center")
        day.draw(img, 58 + 49 // 2, 190, "03", self.INK, "center")
        self.p.font("MD_TIME").draw(img, 58 + 49 + 183 // 2, 156, clock(minutes), self.WHITE, "center")
        heart = self.p.font("MD_HEART")
        hc = 58 + 49 + 183 + 42 // 2
        heart.draw(img, hc, 175, "♥", self.BOARD, "center")
        heart.draw(img, hc, 190, str(heart_rate(t, 58)), self.BOARD, "center")
        bat = "72%"
        bl = 195 - (26 + info.width(bat)) // 2
        s = Shapes()
        battery(s, bl, 323, 72, rgb(self.WHITE))
        s.onto(img)
        info.draw(img, bl + 26, 320, bat, self.WHITE)
        return img


# ---------------------------------------------------------------- Pool Lanes (PoolFace)
class PoolLanes:
    """Lengths add up in the swim pill while the clock runs."""

    WHITE, FILL = 0xFFFFFF, 0x104678

    def __init__(self):
        self.p = Project("PoolFace")

    def pill(self, img, x, y, width, text, font):
        self.p.blit(img, "PillLeft0", x, y)
        self.p.blit(img, "PillRight0", x + width - 13, y)
        ImageDraw.Draw(img).rectangle([x + 13, y, x + width - 14, y + 24], fill=rgb(self.FILL) + (255,))
        font.draw(img, x + width // 2, y + 4, text, self.WHITE, "center")

    def render(self, t):
        minutes = 10 * 60 + 8 + int(t * 12)
        swim = round(keyframes(t, [(0, 900), (1, 1500)]) / 50) * 50
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgPool00", 0, 0)
        self.p.font("POOL_DATE_0").draw(img, 195, 92, DATE, self.WHITE, "center")
        self.p.font("POOL_TIME_0").draw(img, 195, 77, clock(minutes), self.WHITE, "center")
        pill = self.p.font("POOL_PILL_0")
        a, b = f"{thousands(swim)} m swim", "8,412 steps"
        wa, wb = pill.width(a) + 20, pill.width(b) + 20
        x = 195 - (wa + 10 + wb) // 2
        self.pill(img, x, 246, wa, a, pill)
        self.pill(img, x + wa + 10, 246, wb, b, pill)
        info = self.p.font("POOL_INFO_0")
        heart, bat = f"♥ {heart_rate(t, 58)}", "72%"
        x = 195 - (info.width(heart) + 14 + 26 + info.width(bat)) // 2
        info.draw(img, x, 281, heart, self.WHITE)
        x += info.width(heart) + 14
        s = Shapes()
        battery(s, x, 284, 72, rgb(self.WHITE))
        s.onto(img)
        info.draw(img, x + 26, 281, bat, self.WHITE)
        return img


# ---------------------------------------------------------------- Race Bib (BibFace)
class RaceBib:
    """Race time ticks on the tilted bib as the steps climb."""

    WHITE, INK = 0xFFFFFF, 0x111111
    COS, SIN = 0.99619, -0.08716

    def __init__(self):
        self.p = Project("BibFace")

    def at(self, img, font, x, y, text, color):
        dx, dy = x - 140, y - 103
        font.draw_along(img, 195 + dx * self.COS - dy * self.SIN, 195 + dx * self.SIN + dy * self.COS, text, color, self.COS, self.SIN)

    def row(self, img, font, parts, gap, top, color):
        width = gap * (len(parts) - 1) + sum(font.width(p) for p in parts)
        x = (280 - width) // 2
        for part in parts:
            self.at(img, font, x, top, part, color)
            x += font.width(part) + gap

    def render(self, t):
        minutes = 10 * 60 + 8 + int(t * 12)
        steps = round(keyframes(t, [(0, 7600), (1, 9400)]))
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgBib00", 0, 0)
        self.row(img, self.p.font("BIB_HEAD_0"), [DATE, "·", f"♥ {heart_rate(t, 58)}"], 10, 8, self.WHITE)
        time = self.p.font("BIB_TIME")
        c = clock(minutes)
        self.at(img, time, (280 - time.width(c)) // 2, 22, c, self.INK)
        self.row(img, self.p.font("BIB_FOOT"), [thousands(steps) + " STEPS", "h72%"], 18, 179, self.INK)
        return img


# ---------------------------------------------------------------- Summit (SummitFace)
class Summit:
    """The hiker climbs the trail with the day's steps and reaches the flag at the goal."""

    WHITE, STAT, META, TRAIL, RIDGE = 0xFFFFFF, 0xE6DDF5, 0xB8AEDA, 0xFFB13D, 0x5E4A8C
    PATH = [(30, 238), (80, 205), (140, 235), (200, 172)]

    def __init__(self):
        self.p = Project("SummitFace")

    def render(self, t):
        goal = 10000
        steps = round(keyframes(t, [(0, 0), (0.85, goal), (1, goal)]))
        floors = round(steps / goal * 16)
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgSummit0", 0, 0)
        lengths = [math.dist(a, b) for a, b in zip(self.PATH, self.PATH[1:])]
        remaining = sum(lengths) * steps / goal
        pts = [self.PATH[0]]
        for (a, b), length in zip(zip(self.PATH, self.PATH[1:]), lengths):
            if remaining <= 0:
                break
            f = min(1.0, remaining / length)
            pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
            remaining -= length
        s = Shapes()
        if len(pts) > 1:
            s.line(pts, 2.5, rgb(self.TRAIL))
        s.onto(img)
        end = pts[-1]
        self.p.blit(img, "Hiker0", end[0] - 8, end[1] - 8)
        self.p.font("SUMMIT_TIME").draw(img, 195, 34, "10:08", self.WHITE, "center")
        stat = self.p.font("SUMMIT_STAT")
        a, b = thousands(steps) + " STEPS", f"▲ {floors} FLOORS"
        x = 195 - (stat.width(a) + 14 + stat.width(b)) // 2
        stat.draw(img, x, 302, a, self.STAT)
        stat.draw(img, x + stat.width(a) + 14, 302, b, self.STAT)
        heart, bat = f"♥ {heart_rate(t, 58)}", "72%"
        x = 195 - (stat.width(DATE) + 14 + stat.width(heart) + 14 + 24 + stat.width(bat)) // 2
        stat.draw(img, x, 326, DATE, self.META)
        x += stat.width(DATE) + 14
        stat.draw(img, x, 326, heart, self.META)
        x += stat.width(heart) + 14
        s = Shapes()
        battery(s, x, 329, 72, rgb(self.META), w=19, h=11, inner=13, fill_h=5)
        s.onto(img)
        stat.draw(img, x + 24, 326, bat, self.META)
        return img


# ---------------------------------------------------------------- Flight Path (FlightFace)
class FlightPath:
    """The plane flies from CGK to LHR as the steps reach the goal."""

    WHITE, MUTED, INFO, ROUTE = 0xFFFFFF, 0x8FA3D1, 0xD6DEF2, 0xFFB13D
    START, CONTROL, END = (80, 250), (195, 140), (310, 230)

    def __init__(self):
        self.p = Project("FlightFace")

    def point(self, t):
        mt = 1 - t
        return (mt * mt * self.START[0] + 2 * mt * t * self.CONTROL[0] + t * t * self.END[0],
                mt * mt * self.START[1] + 2 * mt * t * self.CONTROL[1] + t * t * self.END[1])

    def render(self, t):
        goal = 10000
        steps = round(keyframes(t, [(0, 0), (0.85, goal), (1, goal)]))
        amount = steps / goal
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, "BgFlight0", 0, 0)
        s = Shapes()
        n = max(2, int(amount * 48) + 1)
        s.line([self.point(amount * k / (n - 1)) for k in range(n)], 3, rgb(self.ROUTE))
        s.onto(img)
        dx = 2 * (1 - amount) * (self.CONTROL[0] - self.START[0]) + 2 * amount * (self.END[0] - self.CONTROL[0])
        dy = 2 * (1 - amount) * (self.CONTROL[1] - self.START[1]) + 2 * amount * (self.END[1] - self.CONTROL[1])
        index = min(21, max(0, round((math.degrees(math.atan2(dy, dx)) + 44) / 4)))
        x, y = self.point(amount)
        self.p.blit(img, f"Plane{index}", x - 32, y - 32)
        self.p.font("FL_TOP").draw(img, 195, 56, "JAKARTA · " + DATE, self.MUTED, "center")
        self.p.font("FL_TIME").draw(img, 195, 61, "10:08", self.WHITE, "center")
        code, small = self.p.font("FL_CODE"), self.p.font("FL_SMALL")
        code.draw(img, 56, 262, "CGK", self.ROUTE)
        small.draw(img, 56, 282, "10:08", self.MUTED)
        code.draw(img, 338, 242, "LHR", self.WHITE, "right")
        small.draw(img, 338, 262, "03:08", self.MUTED, "right")
        info = self.p.font("FL_INFO")
        heart, st, bat = f"♥ {heart_rate(t, 58)}", thousands(steps) + " steps", "72%"
        x = 195 - (info.width(heart) + 16 + info.width(st) + 16 + 26 + info.width(bat)) // 2
        info.draw(img, x, 312, heart, self.INFO)
        x += info.width(heart) + 16
        info.draw(img, x, 312, st, self.INFO)
        x += info.width(st) + 16
        s = Shapes()
        battery(s, x, 315, 72, rgb(self.INFO))
        s.onto(img)
        info.draw(img, x + 26, 312, bat, self.INFO)
        return img


# ---------------------------------------------------------------- Sticker Bomb (StickerFace)
def turn(x, y, cx, cy, degrees):
    """A point of a CSS box turned rotate(degrees) about its center: the pen for tilted text."""
    a = math.radians(degrees)
    dx, dy = x - cx, y - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


class StickerBomb:
    """Stickers slapped on a dotted ground; the steps sticker grows with the count."""

    WHITE, INK, YELLOW, HALO = 0xFFFFFF, 0x111111, 0xFFE03D, 0x000000
    STEPS_MIN, BATT_MIN, STEP, STEPS_COUNT, BATT_COUNT = 48, 18, 4, 15, 6

    def __init__(self, ground=0):
        self.p = Project("StickerFace")
        self.g = ground
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))

    def along(self, img, font, x, y, cx, cy, degrees, text, color):
        px, py = turn(x, y, cx, cy, degrees)
        a = math.radians(degrees)
        font.draw_along(img, px, py, text, color, math.cos(a), math.sin(a))

    def bucket(self, width, low, count):
        return max(0, min(count - 1, math.ceil((width - low) / self.STEP)))

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgSticker{self.g}", 0, 0)
        date = self.p.font("ST_DATE")
        self.along(img, date, 123.7 - (date.width(DATE) - 3) / 2, 76, 123.7, 85, -10, DATE, self.INK)
        icon, rate = self.p.font("ST_HICON"), self.p.font("ST_HR")
        self.along(img, icon, 287 - icon.width("♥") / 2, 88 - icon.height / 2, 287, 101, 12, "♥", self.WHITE)
        text = str(hr)
        self.along(img, rate, 287 - rate.width(text) / 2, 108 - rate.height / 2, 287, 101, 12, text, self.WHITE)
        time, c = self.p.font(f"ST_TIME_{self.g}"), clock(minutes)
        for color in (self.HALO, self.WHITE, self.YELLOW):
            self.along(img, time, 195.05 - time.width(c) / 2, 98, 195.05, 187, -6, c, color)
        foot = self.p.font("ST_STEPS")
        text = thousands(steps) + " steps"
        i = self.bucket(foot.width(text), self.STEPS_MIN, self.STEPS_COUNT)
        x, y = self.layout["steps"][i]
        self.p.blit(img, f"Steps{self.g}_{i}", x, y)
        w = self.STEPS_MIN + i * self.STEP + 36
        self.along(img, foot, 88 + (w - 36 - foot.width(text)) / 2, 290, 70 + w / 2, 299.75, -8, text, self.INK)
        batt = self.p.font("ST_BATT")
        pct = f"{battery_level}%"
        i = self.bucket(batt.width(pct), self.BATT_MIN, self.BATT_COUNT)
        x, y = self.layout["batt"][i]
        self.p.blit(img, f"Batt{self.g}_{i}", x, y)
        w = 27 + self.BATT_MIN + i * self.STEP + 36
        level = "abcdefghijk"[(battery_level + 5) // 10]
        self.along(img, batt, 242 + (w - 63 - batt.width(pct)) / 2, 296, 224 + w / 2, 305.75, 9, level + pct, self.WHITE)
        return img


# ---------------------------------------------------------------- Arcade HUD (ArcadeFace)
class ArcadeHUD:
    """A pixel platformer HUD: steps count up like a score."""

    YELLOW, WHITE, RED, GREEN = 0xFFD23F, 0xFFFFFF, 0xFF6B6B, 0x3BD16F

    def __init__(self, coin=0):
        self.p = Project("ArcadeFace")
        self.coin = coin

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgArcade{self.coin}", 0, 0)
        label, value = self.p.font("AR_LABEL"), self.p.font("AR_VALUE")
        label.draw(img, 64, 73, "STEPS", self.YELLOW)
        value.draw(img, 64, 89, f"{min(steps, 99999):05d}", self.WHITE)
        label.draw(img, 326, 73, DATE[:3], self.YELLOW, "right")
        value.draw(img, 326, 89, "03-11", self.WHITE, "right")
        self.p.font("AR_TIME").draw(img, 195, 122, clock(minutes), self.WHITE, "center")
        foot = self.p.font("AR_FOOT")
        heart, pct = f"♥×{hr}", f"{battery_level}%"
        x = 195 - (foot.width(heart) + 22 + 38 + foot.width(pct)) / 2
        foot.draw(img, round(x), 296, heart, self.RED)
        frame = round(x + foot.width(heart) + 22)
        d = ImageDraw.Draw(img)
        d.rectangle([frame, 296, frame + 33, 311], fill=rgb(self.WHITE))
        d.rectangle([frame + 2, 298, frame + 31, 309], fill=(0xA0, 0x52, 0x2D))
        for k in range(min(4, (battery_level + 12) // 25)):
            d.rectangle([frame + 4 + 7 * k, 300, frame + 8 + 7 * k, 307], fill=rgb(self.GREEN))
        foot.draw(img, frame + 38, 298, pct, self.WHITE)
        return img


# ---------------------------------------------------------------- Waypoint Map (WaypointFace)
class WaypointMap:
    """A trail map with the day's route; the distance counts up with the steps."""

    INK, MUTED = 0x1F2A24, 0x5E7266
    HEARTS = [0xFF3D7F, 0x3D63FF, 0xFF3DB4, 0xFF5A1F]
    PILLS = [(102, 56), (166, 60), (234, 54)]

    def __init__(self, route=0):
        self.p = Project("WaypointFace")
        self.route = route

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgWaypoint{self.route}", 0, 0)
        date, time, pill = self.p.font("WP_DATE"), self.p.font("WP_TIME"), self.p.font("WP_PILL")
        line = f"TUE 3 NOV · {steps * 0.74 / 1000:.1f} KM"
        date.draw(img, round(195 - date.width(line) / 2), 70, line, self.MUTED)
        c = clock(minutes)
        time.draw(img, round(195 - time.width(c) / 2), 76, c, self.INK)
        beats = f" {hr}"
        (x, w) = self.PILLS[0]
        left = round(x + (w - pill.width("♥") - pill.width(beats)) / 2)
        pill.draw(img, left, 334, "♥", self.HEARTS[self.route])
        pill.draw(img, left + pill.width("♥"), 334, beats, self.INK)
        for (x, w), text in zip(self.PILLS[1:], [thousands(steps), f"{battery_level}%"]):
            pill.draw(img, round(x + (w - pill.width(text)) / 2), 334, text, self.INK)
        return img


# ---------------------------------------------------------------- Chess Clock (ChessFace)
class ChessClock:
    """A blitz clock on a chess board: your move, with the time on your side."""

    CREAM, INK = 0xF5EBDD, 0x1E1A16
    PILL_MIN, STEP, PILL_COUNT = 132, 4, 8

    def __init__(self, board=0):
        self.p = Project("ChessFace")
        self.board = board
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgChess{self.board}", 0, 0)
        font = self.p.font("CH_DATE")
        line = date + " · BLITZ"
        w = font.width(line)
        i = max(0, min(self.PILL_COUNT - 1, math.ceil((w - self.PILL_MIN) / self.STEP)))
        self.p.blit(img, f"Pill{self.board}_{i}", *self.layout["pill"][i])
        font.draw(img, round(195 - w / 2), 64, line, self.CREAM)
        time, c = self.p.font("CH_TIME"), clock(minutes)
        time.draw(img, round(132.1 - time.width(c) / 2), 164, c, self.INK)
        value = self.p.font("CH_VALUE")
        value.draw(img, 240, 156, str(hr), self.CREAM)
        value.draw(img, 258, 177, thousands(steps), self.CREAM)
        value.draw(img, 252, 199, f"{battery_level}%", self.CREAM)
        return img


# ---------------------------------------------------------------- Origami (OrigamiFace)
class Origami:
    """Folded low poly paper and a paper crane; the chips grow with their numbers."""

    WHITE = 0xFFFFFF
    SHADOW = [0xA02814]
    STEP = 4
    PIECES = {"tag": (112, 10), "heart": (24, 5), "steps": (52, 12), "batt": (60, 6)}
    SLOTS = [59.5, 120.5, 181.5, 208.5, 269.5]

    def __init__(self, way=0):
        self.p = Project("OrigamiFace")
        self.way = way
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))
        self.tag_colors = self.p.fonts["OG_TAG"][1]
        self.shadow = self.p.fonts[f"OG_TIME_{way}_0"][1][0]

    def piece(self, img, kind, width):
        low, count = self.PIECES[kind]
        i = max(0, min(count - 1, math.ceil((width - low) / self.STEP)))
        self.p.blit(img, f"{kind.capitalize()}{self.way}_{i}", *self.layout[kind][i])

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgOrigami{self.way}", 0, 0)
        tag, line = self.p.font("OG_TAG"), "FOLD · " + date
        self.piece(img, "tag", tag.width(line))
        tag.draw(img, round(195 - tag.width(line) / 2), 62, line, self.tag_colors[self.way])
        c = clock(minutes)
        for color in (self.shadow, self.WHITE):
            for k, ch in enumerate(c):
                self.p.font(f"OG_TIME_{self.way}_{k}").draw(img, math.floor(self.SLOTS[k] + 0.5), 78, ch, color)
        chip = self.p.font(f"OG_CHIP_{self.way}")
        ink = chip.palette[0]
        for kind, text, top in (("heart", f"♥ {hr}", 228), ("steps", thousands(steps) + " STEPS", 259.5), ("batt", f"BATT {battery_level}%", 289)):
            self.piece(img, kind, chip.width(text))
            chip.draw(img, 70, math.floor(top + 0.5), text, ink)
        return img


# ---------------------------------------------------------------- Toy Bricks (BricksFace)
class ToyBricks:
    """The time built from toy bricks on a studded baseplate."""

    INK = 0x222222
    DIGIT_X = [84, 156, 234, 306]
    STAT_X = [103, 200, 292]
    TAG_MIN, STEP, TAG_COUNT = 116, 4, 8

    def __init__(self, base=0):
        self.p = Project("BricksFace")
        self.base = base
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgBricks{self.base}", 0, 0)
        tag, line = self.p.font("BR_DATE"), "BUILD · " + date
        w = tag.width(line)
        i = max(0, min(self.TAG_COUNT - 1, math.ceil((w - self.TAG_MIN) / self.STEP)))
        self.p.blit(img, f"Tag{self.base}_{i}", *self.layout["tag"][i])
        tag.draw(img, round(195 - w / 2), 58, line, self.INK)
        for k, ch in enumerate(clock(minutes).replace(":", "")):
            font = self.p.font(f"BR_DIGIT_{k}")
            font.draw(img, round(self.DIGIT_X[k] - font.width(ch) / 2), 105, ch, font.palette[0])
        for k, text in enumerate([f"♥ {hr}", thousands(steps), f"{battery_level}%"]):
            font = self.p.font(f"BR_STAT_{k}")
            font.draw(img, round(self.STAT_X[k] - font.width(text) / 2), 245, text, font.palette[0])
        return img


# ---------------------------------------------------------------- Traffic Light (TrafficFace)
class TrafficLight:
    """A city signal at sunset, with heart rate, steps and battery in the lamps."""

    PEACH, WHITE, INK = 0xFFE1C8, 0xFFFFFF, 0x1A1A1A
    LAMPS = [103, 195, 287]

    def __init__(self, sky=0):
        self.p = Project("TrafficFace")
        self.sky = sky

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgTraffic{self.sky}", 0, 0)
        self.p.font(f"TL_DATE_{self.sky}").draw(img, 195, 60, "GO TIME · " + date, self.PEACH, "center")
        self.p.font(f"TL_TIME_{self.sky}").draw(img, 195, 68, clock(minutes), self.WHITE, "center")
        for k, text in enumerate([f"♥ {hr}", thousands(steps), f"{battery_level}%"]):
            self.p.font(f"TL_LAMP_{k}").draw(img, self.LAMPS[k], 247, text, self.INK, "center")
        return img


# ---------------------------------------------------------------- Shot Clock (ShotFace)
class ShotClock:
    """A basketball scoreboard over the court, the time in glowing red LEDs."""

    YELLOW = 0xFFD23F
    CELLS = [113.65, 195, 276.35]

    def __init__(self, paint=0):
        self.p = Project("ShotFace")
        self.paint = paint
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgShot{self.paint}", 0, 0)
        self.p.blit(img, f"Hour{(minutes // 60) % 24:02d}", *self.layout["hour"])
        self.p.blit(img, f"Minute{minutes % 60:02d}", *self.layout["minute"])
        self.p.font("SH_DATE").draw(img, 195, 64, "SHOT CLOCK · " + date, self.YELLOW, "center")
        value = self.p.font("SH_VALUE")
        for x, text in zip(self.CELLS, [str(hr), thousands(steps), f"{battery_level}%"]):
            value.draw(img, round(x), 191, text, self.YELLOW, "center")
        return img


# ---------------------------------------------------------------- Tennis Court (TennisFace)
class TennisCourt:
    """A court from above: the time over the baseline, the score panel at the net."""

    WHITE, SHADOW = 0xFFFFFF, 0x000000
    SLOTS = [86.6, 135.4, 184.2, 205.8, 254.6]
    CELLS = [126.3, 195, 263.7]

    def __init__(self, surface=0):
        self.p = Project("TennisFace")
        self.surface = surface

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgTennis{self.surface}", 0, 0)
        self.p.font(f"TC_DATE_{self.surface}").draw(img, 195, 60, date + " · SET 2", self.WHITE, "center")
        c = clock(minutes)
        for color in (self.SHADOW, self.WHITE):
            for k, ch in enumerate(c):
                self.p.font(f"TC_TIME_{self.surface}_{k}").draw(img, math.floor(self.SLOTS[k] + 0.5), 96, ch, color)
        value = self.p.font("TC_VALUE")
        for x, text in zip(self.CELLS, [str(hr), thousands(steps), f"{battery_level}%"]):
            value.draw(img, round(x), 237, text, self.WHITE, "center")
        return img


# ---------------------------------------------------------------- Watermelon (MelonFace)
class Watermelon:
    """A watermelon slice: a juicy time and three cream pills that hug their numbers."""

    WHITE, SHADOW, RIND = 0xFFFFFF, 0x780A1E, 0x2F8F3A
    SLOTS = [59.5, 120.5, 181.5, 208.5, 269.5]
    PILL_MIN, STEP, PILL_COUNT = 8, 2, 25

    def __init__(self, flesh=0):
        self.p = Project("MelonFace")
        self.flesh = flesh
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgMelon{self.flesh}", 0, 0)
        self.p.font(f"WM_DATE_{self.flesh}").draw(img, 195, 84, "JUICY · " + date, self.WHITE, "center")
        c = clock(minutes)
        for color in (self.SHADOW, self.WHITE):
            for k, ch in enumerate(c):
                self.p.font(f"WM_TIME_{self.flesh}_{k}").draw(img, math.floor(self.SLOTS[k] + 0.5), 90, ch, color)
        pill = self.p.font("WM_PILL")
        texts = [f"♥ {hr}", thousands(steps), f"{battery_level}%"]
        steps_ = [max(0, min(self.PILL_COUNT - 1, math.ceil((pill.width(t) - self.PILL_MIN) / self.STEP))) for t in texts]
        widths = [self.PILL_MIN + i * self.STEP + 24 for i in steps_]
        x = 195 - (sum(widths) + 16) / 2
        for text, i, w in zip(texts, steps_, widths):
            dx, y = self.layout["pill"][i]
            self.p.blit(img, f"Pill{self.flesh}_{i}", math.floor(x + 0.5) + dx, y)
            pill.draw(img, math.floor(x + w / 2 + 0.5) - pill.width(text) // 2, 227, text, self.RIND)
            x += w + 8
        return img


# ---------------------------------------------------------------- City faces (JakartaFace, SingaporeFace, KualaLumpurFace)
class CityFace:
    """A city skyline at a sky color: the time as Chrome drew it, the date and the stats pill."""

    WHITE, SHADOW = 0xFFFFFF, 0x000000
    DAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    PROJECT = None

    def __init__(self, sky=0):
        import re
        self.p = Project(self.PROJECT)
        self.sky = sky
        self.layout = json.load(open(os.path.join(self.p.root, "resources", "jsonData", "layout.json")))
        art = open(os.path.join(self.p.root, "source", "CityArt.mc")).read()
        self.c = {k: float(v) for k, v in re.findall(r"const (\w+) = ([-\d.]+);", art)}
        self.stacked = "const STACKED = true" in art
        rest = re.search(r"const REST = \[([^\]]*)\]", art).group(1)
        self.rest = [float(v) for v in rest.split(",")] if rest.strip() else []

    def render(self, t, steps=None, hr=None, battery_level=72, minutes=None, date="TUE 3 NOV"):
        minutes = 10 * 60 + 8 + int(t * 12) if minutes is None else minutes
        steps = round(keyframes(t, [(0, 7600), (1, 9400)])) if steps is None else steps
        hr = heart_rate(t, 58) if hr is None else hr
        px = lambda v: math.floor(v + 0.5)
        s = self.sky
        img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
        self.p.blit(img, f"BgCity{s}", 0, 0)
        self.p.blit(img, f"Hour{s}_{(minutes // 60) % 24:02d}", *self.layout["hour"])
        self.p.blit(img, f"Minute{s}_{minutes % 60:02d}", *self.layout["minute"])
        day, rest = date.split(" ", 1)
        font = self.p.font(f"CITY_DATE_{s}")
        y = px(self.c["DATE_BASE"]) - font.base
        if self.stacked:
            d = self.DAYS.index(day)
            self.p.blit(img, f"Day{s}_{d}", *self.layout["day"])
            for color in (self.SHADOW, self.WHITE):
                font.draw(img, px(self.rest[d]), y, " " + rest, color)
        else:
            for color in (self.SHADOW, self.WHITE):
                font.draw(img, px(self.c["DATE_CENTER"]), y, date, color, "center")
        pill = self.p.font(f"CITY_PILL_{s}")
        text = f"{hr} · {thousands(steps)} · {battery_level}%"
        text = " " + text if self.stacked else "♥ " + text
        step = math.ceil((self.c["PILL_LEAD"] + pill.width(text) - self.c["PILL_MIN"]) / self.c["STEP"])
        step = max(0, min(int(self.c["PILL_COUNT"]) - 1, step))
        self.p.blit(img, f"Pill{s}_{step}", *self.layout["pill"][step])
        pill.draw(img, px(self.c["PILL_TEXT"]), px(self.c["PILL_BASE"]) - pill.base, text, self.WHITE,
                  "left" if self.stacked else "center")
        return img


class Jakarta(CityFace):
    PROJECT = "JakartaFace"


class Singapore(CityFace):
    PROJECT = "SingaporeFace"


class KualaLumpur(CityFace):
    PROJECT = "KualaLumpurFace"


# ---------------------------------------------------------------- Oversize Type (OversizeFace)
class OversizeType:
    """Minutes roll over, so the giant minute digits change shape over the hour."""

    WHITE, GROUND = 0xFFFFFF, 0x2B2BE8

    def __init__(self):
        self.p = Project("OversizeFace")
        src = open(f"{self.p.root}/source/OversizeGlyphs.mc").read()

        def array(name):
            return [int(v) for v in src.split(f"const {name} = [")[1].split("]")[0].split(",")]

        self.xoff, self.yoff = array("XOFF"), array("YOFF")
        self.width, self.height, self.advance = array("WIDTH"), array("HEIGHT"), array("ADVANCE")
        body = src.split("const RECTS = [")[1].split("    ];")[0]
        self.rects = [[int(v) for v in row.split("]")[0].split(",") if v.strip()] for row in body.split("[")[1:]]

    def render(self, t):
        minutes = 10 * 60 + 5 + int(t * 10)
        hours, mins = f"{(minutes // 60) % 24:02d}", f"{minutes % 60:02d}"
        img = Image.new("RGBA", (N, N), rgb(self.GROUND) + (255,))
        placed = []
        x = 28
        for ch in hours:
            d = int(ch)
            hx, hy = x + self.xoff[d], -120 + self.yoff[d]
            self.p.blit(img, f"DigitH00{d}", hx, hy)
            placed.append((d, hx, hy))
            x += self.advance[d] - 6
        x = 150
        for ch in mins:
            d = int(ch)
            left, top = x + self.xoff[d], 46 + self.yoff[d]
            right, bottom = left + self.width[d], top + self.height[d]
            self.p.blit(img, f"DigitM0{d}", left, top)
            over = self.p.bitmap(f"DigitMh0{d}")
            for hd, hx, hy in placed:
                r = self.rects[hd]
                for k in range(0, len(r), 4):
                    cl, ct = max(left, hx + r[k]), max(top, hy + r[k + 1])
                    cr, cb = min(right, hx + r[k] + r[k + 2]), min(bottom, hy + r[k + 1] + r[k + 3])
                    if cr > cl and cb > ct:
                        piece = over.crop((cl - left, ct - top, cr - left, cb - top))
                        img.paste(piece, (cl, ct), piece)
            x += self.advance[d] - 6
        date = self.p.font("OV_DATE_0")
        date.draw(img, 354, 92, "TUE", self.WHITE, "right")
        date.draw(img, 354, 111, "03 NOV", self.WHITE, "right")
        stat = self.p.font("OV_STAT_0")
        stat.draw(img, 44, 262, thousands(8412 + round(t * 300)) + " steps", self.WHITE)
        s = Shapes()
        battery(s, 44, 289, 72, rgb(self.WHITE))
        s.onto(img)
        stat.draw(img, 70, 285, "72%", self.WHITE)
        stat.draw(img, 44, 308, f"♥ {heart_rate(t, 58)}", self.WHITE)
        return img


ALL = {
    "running-track": RunningTrack, "orbit": Orbit, "topo-map": TopoMap, "liquid-battery": LiquidBattery,
    "oversize-type": OversizeType, "matchday": Matchday, "pool-lanes": PoolLanes, "race-bib": RaceBib,
    "summit": Summit, "flight-path": FlightPath, "sticker-bomb": StickerBomb, "arcade-hud": ArcadeHUD, "waypoint-map": WaypointMap, "chess-clock": ChessClock, "origami": Origami, "toy-bricks": ToyBricks, "traffic-light": TrafficLight, "shot-clock": ShotClock, "tennis-court": TennisCourt, "watermelon": Watermelon,
    "jakarta": Jakarta, "singapore": Singapore, "kuala-lumpur": KualaLumpur,
}
