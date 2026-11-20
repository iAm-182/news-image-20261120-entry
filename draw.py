#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 as a 1024x1024 PNG.

A single-page newspaper: masthead with the date, one hero lead (Trump
defers the Iran decision to 2027), three illustrated leads (Shenzhen
summit, ICJ genocide ruling, Cyclone Akvan), a world map with twelve
numbered pins, a by-the-numbers strip, and thirty-eight one-line briefs
-- fifty distinct stories in total, every one reported on 20 November
2026.

Everything is drawn with PIL primitives (rectangles, polygons, arcs,
ellipses, text). No external images, no network access, no AI generation.
The output is deterministic: two runs write byte-identical files.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- palette
PAPER = (253, 252, 246)
INK = (18, 18, 18)
RED = (172, 28, 28)
NAVY = (18, 48, 86)
GOLD = (198, 158, 38)
GREY = (96, 96, 96)
LINE = (200, 198, 190)
OCEAN = (206, 226, 240)
LAND = (236, 226, 198)
LAND_EDGE = (176, 152, 100)
PANEL = (244, 242, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns lines that fit in `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, width, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, y, x1, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def rotated_text(text, fnt, fill, angle):
    """A small transparent image holding `text` rotated by `angle`."""
    tmp = Image.new("RGBA", (400, 80), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((4, 4), text, font=fnt, fill=fill + (255,))
    box = tmp.getbbox()
    tmp = tmp.crop(box)
    return tmp.rotate(angle, expand=True, resample=Image.BICUBIC)


# ------------------------------------------------------------------- data
# Every story below was reported on Friday 20 November 2026 (events of
# the day, or first reported that day, in some time zone).

HERO = (
    "THE LEAD \u2014 WASHINGTON",
    "TRUMP DEFERS IRAN DECISION TO 2027",
    "\u201cSee what happens after Jan 1,\u201d the president says \u2014 no rush "
    "on a call as Gulf tensions simmer and allies press for diplomacy.",
)

LEADS = [
    (
        "SHENZHEN \u2014 THE SUMMIT",
        "Three leaders, one table",
        "Trump, Xi and Putin meet for the first time as a trio and call "
        "for lower nuclear risk \u2014 but agree nothing firm on Ukraine.",
        "flags",
    ),
    (
        "THE HAGUE \u2014 THE COURT",
        "Genocide, the court rules",
        "The world court finds Myanmar committed genocide against the "
        "Rohingya minority in its 2017 crackdown.",
        "scales",
    ),
    (
        "ODISHA \u2014 THE STORM",
        "Akvan bears down on the coast",
        "300,000 people evacuated and 423 rescue teams deployed as the "
        "cyclone nears landfall on India's east coast.",
        "storm",
    ),
]

# (number, lon, lat, legend line). First four repeat the hero/leads.
PINS = [
    (1, -77.0, 38.9, "WASHINGTON \u2014 Iran call put off to 2027"),
    (2, 114.1, 22.5, "SHENZHEN \u2014 Three leaders meet; no breakthrough"),
    (3, 4.3, 52.1, "THE HAGUE \u2014 Court: Myanmar committed genocide"),
    (4, 85.8, 20.3, "ODISHA \u2014 Akvan nears; 300,000 evacuated"),
    (5, 46.7, 24.6, "RIYADH \u2014 Houthi strike damages wealth-fund tower"),
    (6, 34.0, 45.0, "CRIMEA \u2014 Ukrainian strike halts rail over bridge"),
    (7, 127.0, 37.5, "SEOUL \u2014 Court clears ex-PM Han over martial law"),
    (8, 178.4, -17.7, "SUVA \u2014 Fiji declares disaster as drought bites"),
    (9, -66.9, 10.5, "CARACAS \u2014 US and Venezuela restore military ties"),
    (10, 139.7, 35.7, "TOKYO \u2014 Engine trouble ends Hayabusa2 landing"),
    (11, 174.8, -41.3, "WELLINGTON \u2014 Nicholls century; NZ 243/5, day one"),
    (12, -0.1, 51.5, "LONDON \u2014 BBC warns of deeper cuts to come"),
]

NUMBERS = [
    ("\u22122.19%", "Dow Jones, below 50,000"),
    ("\u22122.25%", "Nasdaq, worst week since April"),
    ("$1.3tn", "Anthropic's debut value"),
    ("\u2212$669bn", "Nvidia lost in six days"),
    ("$91.98", "Brent crude, a barrel"),
    ("300,000", "evacuated ahead of Akvan"),
]

# (kicker, one-line story). 38 briefs; with the hero, 3 leads and 8
# pin-only stories that is 50 distinct stories on the page.
BRIEFS = [
    ("SPACE", "Voyager 1 passes one light-day from Earth"),
    ("MARKETS", "Dow slides below 50,000; worst week since April"),
    ("TECH", "Anthropic closes debut near $97; worth ~$1.3tn"),
    ("TECH", "Nvidia sheds $669bn of value in six sessions"),
    ("TECH", "AMD falls 8% on report tying firmware to China"),
    ("TECH", "Congress finds flood of US AI chips reached China"),
    ("TECH", "Apple building autonomous AI agent for late 2027"),
    ("WASHINGTON", "White House cyber chief ousted after outages"),
    ("TECH", "California opens antitrust probe into Nvidia"),
    ("BUSINESS", "JPMorgan breach touches Reserve Program clients"),
    ("NEW YORK", "Hackers take data of 4,000+ retired city workers"),
    ("EUROPE", "Europe ready for talks with Russia on ending war"),
    ("MEDIA", "Judge lets Trump's $15bn NYT suit proceed"),
    ("INDIA", "Modi meets Prince and Princess of Wales in Delhi"),
    ("MARKETS", "Sensex up 1.21% as autos and banks lead rally"),
    ("ENERGY", "Brent holds $91.98 as Gulf risk lingers"),
    ("GAMES", "GTA VI sales pass $1.8bn, beyond The Odyssey"),
    ("GAMES", "Germany pays workers to play GTA VI; backlash grows"),
    ("SPORT", "Ravens suspend Humphrey after podcast remarks"),
    ("USA", "Fiona the hippo dies at Cincinnati Zoo"),
    ("BANGLADESH", "Fire at Muhammad Yunus ancestral home"),
    ("PAKISTAN", "74 militants killed in 10 days of border raids"),
    ("CLIMATE", "COP31 enters final two days; 21 issues unresolved"),
    ("USA", "Nikhil Gupta to be sentenced in Pannun plot"),
    ("USA", "Florida pastor convicted over 2021 Haiti killing"),
    ("TEXAS", "Governor-elect to reverse H-1B hiring freeze"),
    ("WASHINGTON", "Democrats press Lutnick over Nvidia and family"),
    ("INDIA", "Cyclone Murasu soaks Tamil Nadu; 11 flights off"),
    ("SPORT", "India beats Malaysia at Hong Kong Open"),
    ("SPORT", "Women's Asian Hockey Champions Trophy opens"),
    ("ECONOMY", "IMF's Georgieva: 4.7% inflation needs tighter policy"),
    ("WASHINGTON", "Senate set to vote on permitting-reform bill"),
    ("MARKETS", "Copper drops more than 5% from September highs"),
    ("MARKETS", "Gold under pressure as the dollar firms"),
    ("CRYPTO", "Bitcoin put premiums jump before Fed minutes"),
    ("YEMEN", "Voices from inside a besieged Yemeni city"),
    ("SCIENCE", "Fat-burning compound spares muscle, study finds"),
    ("USA\u2013CHINA", "Trump and Xi agree on need for AI safety rules"),
]

# Rough continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-105, 68),
     (-95, 69), (-85, 66), (-78, 62), (-72, 62), (-65, 60), (-60, 55),
     (-55, 47), (-60, 43), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 21), (-97, 16),
     (-102, 17), (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-124, 40),
     (-124, 48), (-130, 55), (-140, 60), (-150, 59), (-158, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 65), (-42, 70), (-50, 74),
     (-58, 76), (-65, 76), (-68, 72), (-62, 68)],
    # South America
    [(-79, 9), (-77, 4), (-80, -2), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -41), (-58, -34), (-52, -32),
     (-48, -28), (-41, -23), (-39, -15), (-35, -8), (-35, -5), (-40, -3),
     (-44, -2), (-50, 0), (-52, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
     (-76, 10)],
    # Africa
    [(-17, 15), (-16, 20), (-14, 25), (-10, 30), (-6, 35), (0, 36), (10, 37),
     (11, 34), (19, 32), (25, 32), (30, 31), (32, 31), (35, 28), (37, 22),
     (39, 18), (41, 15), (44, 11), (48, 11), (51, 11), (51, 10), (46, 5),
     (42, 0), (40, -5), (39, -10), (36, -15), (33, -20), (32, -26), (28, -33),
     (25, -34), (20, -35), (18, -33), (16, -29), (14, -22), (12, -18),
     (13, -12), (12, -6), (9, -1), (9, 4), (4, 6), (-2, 5), (-8, 5),
     (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-1, 49), (2, 51),
     (4, 53), (7, 54), (8, 57), (10, 57), (12, 55), (18, 56), (21, 55),
     (21, 58), (24, 58), (28, 59), (30, 60), (30, 63), (28, 66), (32, 68),
     (40, 68), (48, 68), (55, 69), (62, 70), (70, 72), (78, 72), (85, 73),
     (95, 76), (105, 76), (115, 73), (125, 73), (135, 72), (145, 72),
     (155, 70), (165, 69), (170, 66), (178, 65), (178, 62), (170, 60),
     (162, 58), (158, 53), (156, 51), (150, 47), (142, 46), (140, 40),
     (138, 36), (135, 34), (130, 33), (127, 35), (127, 39), (124, 40),
     (120, 35), (120, 30), (115, 23), (110, 20), (108, 15), (105, 9),
     (103, 7), (100, 8), (98, 12), (95, 15), (92, 20), (90, 22), (87, 22),
     (84, 19), (80, 15), (77, 8), (75, 12), (73, 18), (70, 21), (66, 25),
     (62, 25), (58, 25), (56, 27), (52, 28), (50, 29), (48, 30), (44, 33),
     (42, 36), (39, 36), (36, 36), (33, 36), (30, 36), (27, 37), (24, 39),
     (22, 40), (19, 42), (16, 44), (13, 44), (10, 44), (7, 44), (4, 43),
     (0, 40), (-2, 37), (-6, 36)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (118, -35), (122, -33), (126, -32),
     (130, -32), (134, -33), (137, -35), (140, -38), (144, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (143, -15),
     (142, -11), (139, -14), (136, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (123, -17), (120, -20), (116, -21)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 57), (1, 52), (-1, 51)],
    # Japan
    [(130, 31), (131, 33), (133, 34), (136, 35), (138, 35), (140, 37),
     (141, 39), (142, 42), (143, 43), (145, 44), (143, 42), (141, 40),
     (140, 38), (139, 36), (137, 35), (134, 34), (132, 33)],
    # New Zealand
    [(167, -45), (169, -43), (172, -41), (174, -39), (176, -38), (178, -38),
     (176, -40), (174, -42), (172, -44), (169, -46)],
    # Indonesia (schematic blobs)
    [(95, 5), (98, 3), (102, -1), (106, -3), (110, -6), (114, -7),
     (118, -8), (120, -9), (116, -9), (112, -8), (108, -7), (104, -5),
     (100, -1), (97, 2)],
    [(119, -1), (122, -1), (125, 0), (127, 1), (124, 2), (121, 1)],
    [(131, -1), (134, -2), (136, -3), (133, -4), (131, -3)],
]


# ------------------------------------------------------------- illustrations
def draw_calendar(d, img, x, y, w, h):
    """A desk calendar page marked 2027, stamped DEFERRED."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 22], fill=RED)
    d.text((x + 10, y + 3), "2027", font=font(SANS_B, 13), fill=(255, 255, 255))
    d.text((x + w - 62, y + 3), "JAN", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    # little month grid
    gx, gy = x + 12, y + 34
    cell = 13
    for r in range(3):
        for c in range(7):
            d.rectangle([gx + c * (cell + 4), gy + r * (cell + 4),
                         gx + c * (cell + 4) + cell, gy + r * (cell + 4) + cell],
                        outline=LINE, width=1)
    d.text((x + 14, y + 86), "2027", font=font(SERIF_B, 40), fill=RED)
    stamp = rotated_text("DEFERRED", font(SANS_B, 17), RED, -14)
    img.paste(stamp, (x + w - stamp.width - 8, y + h - stamp.height - 34),
              stamp)


def draw_flags(d, x, y, w, h):
    """Three small flags (US, China, Russia) over a skyline."""
    # skyline
    base = y + h - 16
    for i, bh in enumerate([26, 40, 18, 48, 30, 22, 36]):
        bx = x + 6 + i * 30
        d.rectangle([bx, base - bh, bx + 24, base], fill=(178, 180, 175))
    d.rectangle([x, base, x + w, base + 2], fill=INK)
    # flag poles and flags
    specs = [
        (x + 30, "us"), (x + w // 2 - 20, "cn"), (x + w - 70, "ru"),
    ]
    for fx, kind in specs:
        d.line([(fx, y + 8), (fx, y + 58)], fill=INK, width=2)
        fw, fh = 44, 28
        if kind == "us":
            for s in range(7):
                d.rectangle([fx, y + 8 + s * 4, fx + fw, y + 8 + s * 4 + 4],
                            fill=RED if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, y + 8, fx + 18, y + 8 + 16], fill=NAVY)
            for sy in range(3):
                for sx in range(3):
                    d.ellipse([fx + 3 + sx * 5, y + 11 + sy * 5,
                               fx + 5 + sx * 5, y + 13 + sy * 5],
                              fill=(255, 255, 255))
        elif kind == "cn":
            d.rectangle([fx, y + 8, fx + fw, y + 8 + fh], fill=RED)
            d.ellipse([fx + 5, y + 12, fx + 11, y + 18], fill=GOLD)
            for sx, sy in [(20, 10), (26, 14), (28, 20), (22, 24)]:
                d.ellipse([fx + sx, y + sy, fx + sx + 3, y + sy + 3],
                          fill=GOLD)
        else:
            d.rectangle([fx, y + 8, fx + fw, y + 8 + 9], fill=(255, 255, 255),
                        outline=INK)
            d.rectangle([fx, y + 17, fx + fw, y + 17 + 10], fill=(0, 57, 166))
            d.rectangle([fx, y + 27, fx + fw, y + 8 + fh], fill=(213, 0, 50))


def draw_scales(d, x, y, w, h):
    """Scales of justice."""
    cx = x + w // 2
    top = y + 6
    d.line([(cx, top), (cx, y + h - 26)], fill=INK, width=3)
    d.line([(cx - 52, top + 8), (cx + 52, top + 8)], fill=INK, width=3)
    d.ellipse([cx - 4, top - 2, cx + 4, top + 6], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * 52
        d.line([(px, top + 8), (px - 16, top + 34)], fill=INK, width=1)
        d.line([(px, top + 8), (px + 16, top + 34)], fill=INK, width=1)
        d.line([(px, top + 8), (px, top + 34)], fill=INK, width=1)
        d.arc([px - 20, top + 30, px + 20, top + 56], 0, 180, fill=NAVY,
              width=3)
        d.line([(px - 20, top + 43), (px + 20, top + 43)], fill=NAVY, width=3)
    d.line([(cx - 26, y + h - 24), (cx + 26, y + h - 24)], fill=INK, width=3)
    d.line([(cx - 14, y + h - 12), (cx + 14, y + h - 12)], fill=INK, width=3)


def draw_storm(d, x, y, w, h):
    """A cyclone spiral over a coastline."""
    cx, cy = x + w // 2 - 20, y + h // 2 - 4
    for r in range(8, 46, 7):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200 + r * 4,
              end=200 + r * 4 + 250, fill=NAVY, width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # rain slashes
    for i in range(6):
        rx = x + w - 46 + i * 7
        d.line([(rx, y + 14), (rx - 4, y + 30)], fill=NAVY, width=2)
    # coastline
    d.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)], fill=INK, width=2)
    d.arc([x + w - 60, y + h - 34, x + w + 10, y + h + 6], 180, 300,
          fill=LAND_EDGE, width=2)


def draw_map(d, x, y, w, h):
    """Schematic world map (equirectangular, lat 75..-55) with pins."""
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 75.0, -55.0

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for n, lon, lat, _label in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 10)
        tw = d.textlength(str(n), font=f)
        d.text((px - tw / 2, py - 7), str(n), font=f, fill=(255, 255, 255))
    return proj


# ------------------------------------------------------------------ layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([7, 7, W - 8, H - 8], outline=INK, width=2)
    d.rectangle([11, 11, W - 12, H - 12], outline=LINE, width=1)
    mx, mx1 = 24, W - 24  # content margins

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 52)
    d.text(((W - d.textlength(title, font=tf)) / 2, 12), title, font=tf,
           fill=INK)
    date = "FRIDAY, 20 NOVEMBER 2026"
    df = font(SANS_B, 23)
    d.text(((W - d.textlength(date, font=df)) / 2, 70), date, font=df,
           fill=RED)
    sf = font(SANS_B, 13)
    d.text((mx, 76), "50 STORIES", font=sf, fill=INK)
    right = "ONE DAY \u2022 EVERY REGION"
    d.text((mx1 - d.textlength(right, font=sf), 76), right, font=sf, fill=INK)
    rule(d, mx, 100, mx1, 3)
    rule(d, mx, 104, mx1, 1)

    # ---- hero lead
    hy = 110
    kicker, headline, deck = HERO
    d.text((mx, hy), kicker, font=font(SANS_B, 14), fill=RED)
    y = text_block(d, mx, hy + 20, headline, font(SERIF_B, 34), INK, 636,
                   leading=40)
    y = text_block(d, mx, y + 6, deck, font(SERIF, 16), INK, 636, leading=21)
    # calendar panel on the right
    px, pw = 684, 316
    d.rectangle([px, hy, px + pw, hy + 146], fill=PANEL, outline=LINE, width=1)
    draw_calendar(d, img, px + 14, hy + 8, pw - 28, 130)
    rule(d, mx, 264, mx1, 1)

    # ---- three illustrated leads
    ly = 272
    col_w = 317
    cols = [mx, mx + col_w + 11, mx + 2 * (col_w + 11)]
    for (kick, head, dek, kind), cx in zip(LEADS, cols):
        d.rectangle([cx, ly, cx + col_w, ly + 64], fill=PANEL, outline=LINE,
                    width=1)
        if kind == "flags":
            draw_flags(d, cx + 6, ly + 2, col_w - 12, 60)
        elif kind == "scales":
            draw_scales(d, cx + 6, ly + 2, col_w - 12, 60)
        else:
            draw_storm(d, cx + 6, ly + 2, col_w - 12, 60)
        d.text((cx, ly + 72), kick, font=font(SANS_B, 12), fill=RED)
        y = text_block(d, cx, ly + 90, head, font(SERIF_B, 19), INK, col_w,
                       leading=22)
        text_block(d, cx, y + 2, dek, font(SANS, 11), GREY, col_w, leading=14)
    rule(d, mx, 456, mx1, 1)

    # ---- world map + pin legend
    d.text((mx, 464), "THE DAY ON THE MAP \u2014 TWELVE PLACES THAT MADE "
           "THE NEWS", font=font(SANS_B, 14), fill=INK)
    map_x, map_y, map_w, map_h = mx, 482, 616, 132
    draw_map(d, map_x, map_y, map_w, map_h)
    lx = 656
    lf = font(SANS, 12)
    ly2 = map_y
    for n, _lon, _lat, label in PINS:
        d.text((lx, ly2), label, font=lf, fill=INK)
        ly2 += 11.5
    rule(d, mx, 626, mx1, 1)

    # ---- by the numbers
    d.text((mx, 634), "BY THE NUMBERS", font=font(SANS_B, 12), fill=RED)
    cell_w = 137
    for i, (val, lab) in enumerate(NUMBERS):
        cx = 180 + i * cell_w
        d.text((cx, 632), val, font=font(SERIF_B, 19), fill=NAVY)
        d.text((cx, 654), lab, font=font(SANS, 10), fill=GREY)
    rule(d, mx, 672, mx1, 1)

    # ---- briefs
    d.text((mx, 680), "THE REST OF THE DAY \u2014 38 MORE STORIES",
           font=font(SANS_B, 14), fill=INK)
    bf = font(SANS, 12)
    kf = font(SANS_B, 12)
    col2_x = mx + 488
    by = 698
    for i, (kick, text) in enumerate(BRIEFS):
        col = 0 if i < 19 else 1
        row = i if i < 19 else i - 19
        bx = mx if col == 0 else col2_x
        yy = by + row * 15
        d.text((bx, yy), kick, font=kf, fill=RED)
        kw = d.textlength(kick, font=kf)
        d.text((bx + kw + 6, yy), "\u2014 " + text, font=bf, fill=INK)

    # ---- footer
    rule(d, mx, 988, mx1, 1)
    foot = ("Every story on this page was reported on Friday 20 November "
            "2026. Sources: Reuters, BBC, AP, The Hindu, MarketWatch.")
    d.text((mx, 992), foot, font=font(SANS, 9), fill=GREY)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
