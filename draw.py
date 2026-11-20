#!/usr/bin/env python3
"""news-image-20261120 v2 — draw the front page for Friday 20 November 2026.

Original artwork drawn with PIL primitives only. No photos, no downloaded
images, no external assets. Run: python3 draw.py  ->  writes entry.png
(1024x1024) next to this file. Deterministic: two runs write identical bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (158, 28, 34)
REDBRIGHT = (176, 32, 38)
BROWN = (122, 74, 52)
NAVY = (22, 40, 63)
NAVY2 = (16, 32, 52)
TAN = (217, 201, 163)
TAN2 = (226, 212, 178)
GREY = (90, 88, 82)
LINE = (60, 58, 52)
WHITE = (250, 248, 242)
CREAM = (238, 231, 214)
GOLD = (184, 134, 42)
GREEN = (46, 110, 72)
TEAL = (18, 110, 106)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(draw, text, f):
    """Text width in pixels."""
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, text, f, max_w):
    """Shorten with an ellipsis until the single line fits."""
    if draw.textlength(text, font=f) <= max_w:
        return text
    while len(text) > 4 and draw.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1]
    return text + "\u2026"


def para(draw, x, y, text, f, max_w, leading, fill=INK, max_lines=None):
    """Draw a wrapped paragraph; returns y after the last line."""
    lines = wrap(draw, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, wdt=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


# ---------------------------------------------------------------- stories
# Every story below happened, or was first reported, on Friday 20 Nov 2026
# in at least one time zone, verified against live reporting on 20 Nov 2026.
# Thursday stories (Shenzhen summit itself, Anthropic IPO debut, ICJ Myanmar
# verdict, GTA VI midnight launch, Bukele registration, Senegal boat,
# Fiona's death, Indonesia asset law, Denmark Greenland bill) are NOT listed
# as Friday news; they are named in the DATE CHECK footer instead.

FEATURES = [
    dict(
        n=1, place="ODISHA, INDIA", tag="CYCLONE", art="akvan",
        head="Cyclone Akvan makes landfall in eastern India",
        body=("Severe storm crosses near Gopalpur; 300,000+ evacuated, winds "
              "70\u201380 gusting 90 km/h, 423 rescue teams deployed, schools shut."),
        src="(IMD, The Hindu)",
        strip="LANDFALL \u00b7 GUSTS 90 KM/H",
    ),
    dict(
        n=2, place="KYIV, UKRAINE", tag="WAR", art="kyiv",
        head="Russia fires wave of ~30 ballistic missiles at Kyiv",
        body=("Seven overnight waves hit energy and transport sites; fires burn "
              "in three districts, power and water cut, hospitals hit in Kharkiv."),
        src="(Kyiv Post, Reuters)",
        strip="01:25 LOCAL \u00b7 7 WAVES",
    ),
    dict(
        n=3, place="ANTALYA, T\u00dcRK\u0130YE", tag="CLIMATE", art="cop31",
        head="COP31 reaches its final day deadlocked",
        body=("Closing draft omits fossil-fuel phase-out while $120bn adaptation "
              "finance stays unresolved; hosts push \u201c35 by 35\u201d clean-power goal."),
        src="(UN News, Reuters)",
        strip="FINAL DAY \u00b7 DEADLOCK",
    ),
]

MEDIUMS = [
    dict(
        n=4, place="SEOUL / TOKYO", tag="MARKETS", art="selloff",
        head="AI sell-off sinks Asia to worst week since 2020",
        body="Nikkei \u22124.5%, KOSPI \u22124.7%, SoftBank \u221216%; worst week since 2020.",
        src="(Reuters)",
    ),
    dict(
        n=5, place="MERCURY", tag="SPACE", art="mercury",
        head="BepiColombo reaches Mercury after 8 years",
        body="ESA/JAXA probe ends 6bn-mile trip; orbit insertion set for Saturday.",
        src="(ESA, BBC)",
    ),
    dict(
        n=6, place="BRUSSELS", tag="EUROPE", art="flags",
        head="Burnham holds first EU\u2013UK reset summit",
        body="Costa & von der Leyen host UK PM; youth & carbon deals eyed.",
        src="(EU Council)",
    ),
    dict(
        n=7, place="TOKYO", tag="ECONOMY", art="cpi",
        head="Japan inflation hits 2.3%; BoJ hike eyed",
        body="Oct headline CPI rises from 2.1%; core 2.2%, above 2% for a second month.",
        src="(Reuters)",
    ),
    dict(
        n=8, place="BEIJING", tag="RATES", art="rates",
        head="China holds lending rates for 18th month",
        body="1-year LPR at 3.0%, 5-year at 3.5% as expected.",
        src="(PBOC, Reuters)",
    ),
    dict(
        n=9, place="WELLINGTON", tag="CRICKET", art="cricket",
        head="Phillips makes history with 118 vs India",
        body="First NZ batter with centuries in all 3 formats vs India in a year.",
        src="(ICC, AP)",
    ),
    dict(
        n=10, place="BARCELONA", tag="HEALTH", art="pill",
        head="Pancreatic cancer pill shrinks tumours 60.7%",
        body="Daraxonrasib + chemo beats chemo alone; 1 in 12 tumours vanish.",
        src="(Reuters)",
    ),
    dict(
        n=11, place="HORMUZ", tag="ENERGY", art="tanker",
        head="Hormuz stays tense; Brent holds near $92.50",
        body="Oil edges up Friday as tanker attacks disrupt shipping.",
        src="(Reuters)",
    ),
    dict(
        n=12, place="ROME", tag="LABOUR", art="strike",
        head="Italy\u2019s CGIL holds 24-hr general strike",
        body="Unions rally across ~100 squares against 2027 budget; transport hit.",
        src="(CGIL, AFP)",
    ),
    dict(
        n=13, place="SEOUL", tag="JUSTICE", art="gavel",
        head="Korea\u2019s ruling party moves to impeach top judge",
        body="Targets Chief Justice Cho Hee-dae; opposition calls it \u201cmadness\u201d.",
        src="(SBS)",
    ),
]

BRIEFS = [
    ("LONDON", "UK & Norway fund \u00a3100m+ for naval vessels", "BBC"),
    ("LOS ANGELES", "Thomas Markle ruled fit to stand trial", "BBC"),
    ("TURIN", "ATP Finals groups close: Alcaraz, Medvedev win", "ATP"),
    ("WELLINGTON", "Henry Nicholls scores 175* in 216-run stand", "ICC"),
    ("GAZA", "Aid groups score the peace plan 4 out of 26", "UN News"),
    ("NEW DELHI", "Pakistan minister leads SCO delegation", "The Hindu"),
    ("TONGA", "Drought emergency declared as El Ni\u00f1o bites", "RNZ"),
    ("HONG KONG", "Hang Seng about 20% off January peak", "AP"),
    ("SYDNEY", "Retailer General Pants enters administration", "ABC"),
    ("ODISHA", "209mm of rain at Patrapur as Akvan crosses", "PTI"),
    ("CANBERRA", "Australia sanctions West Bank settlers", "Reuters"),
    ("PARIS", "France edge South Africa 21\u201319", "AP"),
    ("SHENZHEN", "Trump heads home after summit with Xi, Putin", "CNN"),
    ("LVIV", "Air defences fire at Russian drone over city", "Governor"),
    ("DAR ES SALAAM", "Tanzania in Africa\u2019s top 5 gold holders", "Reuters"),
    ("SEOUL", "Appeal court upholds Kakao founder\u2019s acquittal", "SBS"),
    ("US CINEMAS", "\u201cHunger Games\u201d prequel opens", "Lionsgate"),
    ("WORLD", "GTA VI\u2019s first full day: 1.7m copies counted", "Sensor Tower"),
    ("BRUSSELS", "UK: carbon link may be worth \u00a33.8bn", "UK factsheet"),
    ("MEXICO CITY", "Nation marks 116th Revolution Day", "AP"),
    ("S\u00c3O PAULO", "Markets shut for Black Consciousness Day", "B3"),
    ("WORLD", "UN marks World Children\u2019s Day", "UN News"),
    ("BEIT SHEMESH", "Haredi protesters clash with Israeli police", "AP"),
]

STATS = [
    ("300,000+", "evacuated ahead of Akvan"),
    ("~30", "ballistic missiles at Kyiv"),
    ("\u22127%", "worst week since 2020"),
    ("2.3%", "Japan Oct CPI; BoJ eyed"),
    ("118", "historic century vs India"),
    ("8 yrs", "reaches Mercury"),
]

CHIPS = [
    ("EUROPE 9", (31, 90, 158)),
    ("AMERICAS 4", (46, 110, 72)),
    ("ASIA-PACIFIC 10", (158, 28, 34)),
    ("MIDEAST 3", (150, 110, 30)),
    ("AFRICA 1", (104, 74, 150)),
    ("OCEANIA 5", (18, 110, 106)),
    ("WORLD 4", (90, 88, 82)),
]

DATE_CHECK = (
    "First reported Thursday 19 Nov, so NOT shown here as Friday\u2019s news: the Trump\u2013Xi\u2013Putin "
    "Shenzhen summit itself \u00b7 Anthropic\u2019s $83 IPO pricing & Nasdaq debut \u00b7 the ICJ\u2019s Myanmar "
    "Rohingya genocide verdict \u00b7 GTA VI\u2019s midnight launch \u00b7 Bukele\u2019s third-term registration \u00b7 "
    "the Senegal boat capsizing \u00b7 Fiona the hippo\u2019s death \u00b7 Indonesia\u2019s asset-forfeiture law \u00b7 "
    "Denmark\u2019s Greenland defence bill \u00b7 the $190.4m Van Gogh sale \u00b7 Voyager 1\u2019s one-light-day "
    "milestone."
)

FOOTER = (
    "Every story here happened, or was first reported, on Friday 20 November 2026 in at least one time zone. "
    "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, ICC, EU Council, PBOC. Original vector drawings."
)


# ---------------------------------------------------------------- illustrations
# All drawn from scratch with PIL primitives. Each takes (draw, x, y, w, h)
# and paints inside that box.

def ill_akvan(d, x, y, w, h):
    # Bay of Bengal (right, blue) vs Odisha coast (left, tan); spiral cyclone.
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(38, 84, 122))
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h * 0.55),
               (x + w * 0.38, y + h), (x, y + h)], fill=TAN)
    d.polygon([(x + w * 0.42, y), (x + w * 0.55, y + h * 0.28),
               (x + w * 0.38, y + h * 0.55), (x + w * 0.30, y + h * 0.55)],
              fill=(200, 182, 140))
    cx, cy = x + w * 0.66, y + h * 0.52
    for r, wd in ((52, 5), (40, 4), (28, 4), (17, 3)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=WHITE, width=wd)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=NAVY, width=2)
    # Gopalpur marker on the coast, label on a land-coloured tag
    gx, gy = x + w * 0.40, y + h * 0.42
    lab = "Gopalpur"
    lf = font(F_SANS_BOLD, 12)
    lw = d.textlength(lab, font=lf)
    d.rectangle([gx + 8, gy - 8, gx + 12 + lw, gy + 8], fill=TAN)
    d.text((gx + 10, gy - 6), lab, font=lf, fill=(60, 50, 38))
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED, outline=WHITE, width=2)
    d.text((x + 8, y + 6), "ODISHA", font=font(F_SANS_BOLD, 12), fill=(60, 50, 38))
    d.text((x + 8, y + 22), "INDIA", font=font(F_SANS, 11), fill=(60, 50, 38))
    d.text((x + w - 108, y + h - 20), "BAY OF BENGAL",
           font=font(F_SANS_BOLD, 11), fill=(200, 220, 235))


def ill_kyiv(d, x, y, w, h):
    # Night sky, skyline silhouette, missile trails and fires.
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY2)
    for sx, sy in ((18, 14), (70, 26), (150, 10), (230, 22), (290, 12)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 210, 225))
    # skyline
    base = y + h - 26
    for bx, bw, bh in ((0, 34, 34), (36, 26, 52), (64, 40, 30), (106, 24, 58),
                       (132, 30, 40), (164, 34, 62), (200, 28, 44), (230, 36, 56),
                       (268, 30, 38), (300, 24, 48)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base + 26], fill=(8, 14, 26))
    # dome
    d.pieslice([x + 168, base - 78, x + 196, base - 50], 180, 360, fill=(8, 14, 26))
    d.rectangle([x + 180, base - 86, x + 184, base - 76], fill=(8, 14, 26))
    # missile trails: bright arcs from top-right to the city
    for (x0, y0, x1, y1, col) in (
            (300, 4, 210, 62, (255, 170, 60)), (262, 2, 150, 74, (255, 140, 60)),
            (210, 6, 96, 84, (255, 190, 90))):
        d.line([(x + x0, y + y0), (x + x1, y + y1)], fill=col, width=3)
        d.ellipse([x + x1 - 4, y + y1 - 4, x + x1 + 4, y + y1 + 4], fill=(255, 220, 120))
    # fires on rooftops
    for fx, fy in ((52, base - 52), (150, base - 58), (250, base - 44)):
        d.polygon([(x + fx, y + fy - 12), (x + fx - 7, y + fy + 2), (x + fx + 7, y + fy + 2)],
                  fill=(255, 120, 20))
        d.polygon([(x + fx, y + fy - 6), (x + fx - 4, y + fy + 2), (x + fx + 4, y + fy + 2)],
                  fill=(255, 210, 90))


def ill_cop31(d, x, y, w, h):
    # Globe, rising thermometer, COP31 badge.
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    cx, cy, r = x + w * 0.30, y + h * 0.52, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 168))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.ellipse([cx - 34, cy - 30, cx - 6, cy - 2], fill=GREEN)
    d.ellipse([cx + 2, cy + 6, cx + 34, cy + 34], fill=GREEN)
    d.ellipse([cx + 8, cy - 34, cx + 30, cy - 12], fill=GREEN)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=WHITE, width=2)
    # thermometer, right side below the badge, clear of the bottom strip
    tx = x + w - 34
    d.rounded_rectangle([tx, y + 68, tx + 16, y + 100], radius=8,
                        fill=WHITE, outline=RED, width=3)
    d.ellipse([tx - 7, y + 94, tx + 23, y + 110], fill=RED, outline=RED)
    d.rounded_rectangle([tx + 4, y + 86, tx + 12, y + 98], radius=4, fill=RED)
    for i, t in enumerate(("2.0", "1.5")):
        yy = y + 74 + i * 14
        d.line([(tx - 8, yy), (tx - 2, yy)], fill=INK, width=2)
        d.text((tx - 34, yy - 6), t, font=font(F_SANS, 10), fill=INK)
    # badge
    bx = x + w - 128
    d.rounded_rectangle([bx, y + 10, x + w - 10, y + 62], radius=4,
                        fill=WHITE, outline=RED, width=2)
    d.text((bx + 8, y + 13), "ANTALYA \u00b7 NOV 20", font=font(F_SANS_BOLD, 11), fill=RED)
    d.text((bx + 8, y + 30), "COP31", font=font(F_SERIF_BLACK, 24), fill=INK)


def ill_selloff(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY2)
    d.text((x + 8, y + 4), "ASIA  \u22127% WK", font=font(F_SANS_BOLD, 12),
           fill=(255, 120, 120))
    # falling candlesticks, kept inside the box
    pts = [22, 28, 24, 32, 30, 38, 36, 42]
    for i, py in enumerate(pts):
        px = x + 10 + i * 22
        top = y + py
        d.rectangle([px, top, px + 11, top + 10],
                    fill=(220, 60, 60) if i % 2 == 0 else (200, 40, 40))
        d.line([(px + 5, top - 4), (px + 5, top + 14)], fill=(220, 60, 60), width=2)


def ill_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(12, 16, 30))
    for sx, sy in ((14, 8), (60, 16), (120, 6), (170, 14), (40, 44), (150, 46)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 225, 235))
    mx, my, mr = x + w * 0.68, y + h * 0.55, 23
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(178, 172, 158))
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(120, 114, 100), width=2)
    for cx, cy, cr in ((-9, -5, 5), (7, 4, 6), (-1, 11, 3), (11, -9, 3)):
        d.ellipse([mx + cx - cr, my + cy - cr, mx + cx + cr, my + cy + cr],
                  fill=(140, 134, 120))
    # probe with panels, dotted approach path (left, clear of the label)
    px, py = x + 12, y + h * 0.62
    for i in range(5):
        d.ellipse([px + i * 8, py + 8 - i * 2, px + i * 8 + 3, py + 11 - i * 2],
                  fill=(255, 210, 90))
    d.rectangle([px + 44, py - 2, px + 56, py + 6], fill=(200, 205, 215))
    d.rectangle([px + 32, py, px + 44, py + 4], fill=(40, 90, 160))
    d.rectangle([px + 56, py, px + 68, py + 4], fill=(40, 90, 160))
    d.text((x + 8, y + 4), "6BN MILES", font=font(F_SANS_BOLD, 11), fill=(255, 210, 90))


def ill_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    # EU flag: blue field, circle of stars
    fx, fy, fw, fh = x + 8, y + 6, 84, 42
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(28, 60, 140))
    import math
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx = fx + fw / 2 + 30 * math.cos(a)
        sy = fy + fh / 2 + 14 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 0))
    # Union Jack, simplified: blue field, white + red crosses
    jx, jy, jw, jh = x + w - 92, y + 6, 84, 42
    d.rectangle([jx, jy, jx + jw, jy + jh], fill=(28, 60, 140))
    d.polygon([(jx, jy), (jx + 14, jy), (jx + jw, jy + jh - 14), (jx + jw, jy + jh),
               (jx + jw - 14, jy + jh), (jx, jy + 14)], fill=WHITE)
    d.polygon([(jx + jw, jy), (jx + jw - 14, jy), (jx, jy + jh - 14), (jx, jy + jh),
               (jx + 14, jy + jh), (jx + jw, jy + 14)], fill=WHITE)
    d.rectangle([jx, jy + jh / 2 - 8, jx + jw, jy + jh / 2 + 8], fill=WHITE)
    d.rectangle([jx + jw / 2 - 8, jy, jx + jw / 2 + 8, jy + jh], fill=WHITE)
    d.rectangle([jx, jy + jh / 2 - 5, jx + jw, jy + jh / 2 + 5], fill=RED)
    d.rectangle([jx + jw / 2 - 5, jy, jx + jw / 2 + 5, jy + jh], fill=RED)


def ill_cpi(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    d.text((x + 8, y + 3), "2% TARGET", font=font(F_SANS_BOLD, 10), fill=GREY)
    d.line([(x + 8, y + 26), (x + w - 8, y + 26)], fill=RED, width=2)
    vals = [1.9, 2.1, 2.1, 2.3]
    bw, gap = 26, 14
    for i, v in enumerate(vals):
        bh = int((v - 1.6) * 40)
        bx = x + 12 + i * (bw + gap)
        by = y + h - 4 - bh
        col = RED if i == 3 else (110, 110, 104)
        d.rectangle([bx, by, bx + bw, y + h - 4], fill=col)
        d.text((bx + 2, by - 12), f"{v}%", font=font(F_SANS_BOLD, 10), fill=INK)


def ill_rates(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    d.text((x + 8, y + 4), "5-YR  3.50%", font=font(F_SANS_BOLD, 13), fill=INK)
    d.line([(x + 8, y + 22), (x + w - 8, y + 22)], fill=RED, width=4)
    d.text((x + 8, y + 28), "1-YR  3.00%", font=font(F_SANS_BOLD, 13), fill=INK)
    d.line([(x + 8, y + 46), (x + w - 8, y + 46)], fill=(90, 88, 82), width=4)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(64, 128, 66))
    d.rectangle([x + 30, y + 4, x + w - 30, y + h - 4], fill=(196, 172, 120))
    d.line([(x + w / 2, y + 4), (x + w / 2, y + h - 4)], fill=WHITE, width=2)
    # bat
    d.polygon([(x + 78, y + 8), (x + 92, y + 8), (x + 100, y + 30),
               (x + 88, y + 46), (x + 76, y + 26)], fill=(222, 190, 140),
              outline=(120, 90, 50))
    d.rectangle([x + 84, y + 2, x + 90, y + 10], fill=(90, 60, 30))
    # ball
    d.ellipse([x + 138, y + 34, x + 152, y + 48], fill=RED, outline=WHITE, width=2)
    d.text((x + 8, y + 2), "118", font=font(F_SERIF_BLACK, 22), fill=WHITE)


def ill_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    # capsule, tilted
    d.rounded_rectangle([x + 40, y + 8, x + 150, y + 28], radius=10, fill=WHITE,
                        outline=RED, width=3)
    d.rectangle([x + 92, y + 8, x + 150, y + 28], fill=RED)
    d.rounded_rectangle([x + 40, y + 8, x + 150, y + 28], radius=10, outline=RED, width=3)
    # shrinking cells
    for cx, cy, r, col in ((30, 44, 8, (200, 60, 60)), (70, 47, 6, (220, 90, 90)),
                           (110, 43, 5, (235, 130, 130)), (150, 47, 4, (245, 180, 180))):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=col)


def ill_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 70, 100))
    # sea
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(18, 50, 78))
    for i in range(5):
        d.arc([x + i * 38 - 10, y + h - 30, x + i * 38 + 22, y + h - 8],
              200, 340, fill=(140, 180, 210), width=2)
    # tanker hull + bridge
    d.polygon([(x + 14, y + 30), (x + w - 14, y + 30), (x + w - 26, y + 52),
               (x + 26, y + 52)], fill=(40, 40, 44))
    d.rectangle([x + w - 52, y + 12, x + w - 22, y + 30], fill=(220, 220, 215))
    d.rectangle([x + 30, y + 18, x + 60, y + 30], fill=(200, 60, 40))
    d.rectangle([x + 66, y + 18, x + 96, y + 30], fill=(200, 60, 40))
    d.text((x + 8, y + 4), "$92.50", font=font(F_SANS_BOLD, 13), fill=(255, 210, 90))


def ill_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 231, 214))
    d.rectangle([x, y + 4, x + w, y + 24], fill=RED)
    d.text((x + 10, y + 7), "SCIOPERO", font=font(F_SANS_BOLD, 14), fill=WHITE)
    # placards
    for px, py, col in ((20, 30, (31, 90, 158)), (70, 27, (46, 110, 72)),
                        (120, 31, (158, 28, 34)), (160, 28, (150, 110, 30))):
        d.rectangle([x + px, y + py, x + px + 22, y + py + 12], fill=col)
        d.line([(x + px + 11, y + py + 12), (x + px + 11, y + py + 22)],
               fill=INK, width=2)


def ill_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 226, 208))
    # scales of justice, kept inside the box
    cx = x + w / 2
    d.line([(cx, y + 4), (cx, y + 44)], fill=INK, width=3)
    d.line([(cx - 32, y + 10), (cx + 32, y + 10)], fill=INK, width=3)
    for sx in (cx - 32, cx + 32):
        d.line([(sx, y + 10), (sx, y + 28)], fill=INK, width=2)
        d.pieslice([sx - 11, y + 26, sx + 11, y + 40], 0, 180, fill=GOLD)
    d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=INK)
    d.rectangle([cx - 15, y + 44, cx + 15, y + 50], fill=INK)


ART = {
    "akvan": ill_akvan, "kyiv": ill_kyiv, "cop31": ill_cop31,
    "selloff": ill_selloff, "mercury": ill_mercury, "flags": ill_flags,
    "cpi": ill_cpi, "rates": ill_rates, "cricket": ill_cricket,
    "pill": ill_pill, "tanker": ill_tanker, "strike": ill_strike,
    "gavel": ill_gavel,
}


# ---------------------------------------------------------------- world map
# Simplified continent outlines (lon, lat), drawn as flat shapes.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 73), (-95, 80),
     (-85, 76), (-75, 72), (-65, 62), (-55, 52), (-60, 47), (-65, 44),
     (-70, 42), (-76, 36), (-80, 32), (-81, 26), (-84, 30), (-90, 21),
     (-97, 26), (-97, 16), (-92, 15), (-86, 13), (-83, 9), (-80, 8),
     (-85, 11), (-90, 14), (-95, 16), (-100, 18), (-105, 20), (-110, 23),
     (-115, 28), (-120, 34), (-124, 40), (-124, 48), (-130, 55), (-140, 60),
     (-150, 61), (-158, 58), (-165, 60)],
    [(-79, 9), (-72, 11), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -27), (-52, -33), (-58, -38),
     (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50), (-73, -42),
     (-72, -30), (-70, -20), (-77, -12), (-80, -5), (-81, 0), (-80, 5)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (3, 43), (7, 44), (10, 44),
     (12, 42), (16, 40), (19, 42), (23, 36), (26, 38), (28, 41), (30, 46),
     (28, 45), (24, 45), (20, 44), (15, 44), (13, 45), (8, 47), (5, 50),
     (2, 51), (-2, 50), (-5, 48), (-10, 44)],
    [(-17, 15), (-16, 20), (-10, 29), (-6, 33), (0, 36), (10, 37), (11, 34),
     (20, 32), (25, 32), (32, 31), (35, 28), (39, 21), (43, 12), (48, 11),
     (51, 12), (48, 2), (44, -2), (40, -10), (36, -18), (33, -26), (28, -33),
     (20, -35), (16, -29), (12, -18), (13, -12), (9, -1), (9, 4), (4, 6),
     (-8, 5), (-13, 8), (-17, 12)],
    [(28, 36), (30, 36), (36, 36), (36, 42), (42, 42), (44, 39), (48, 38),
     (50, 37), (54, 26), (57, 26), (61, 25), (66, 25), (70, 23), (72, 20),
     (76, 10), (77, 8), (80, 13), (85, 19), (88, 22), (91, 22), (94, 17),
     (97, 16), (100, 8), (101, 3), (103, 1), (104, 2), (105, 9), (107, 11),
     (109, 13), (108, 18), (106, 20), (110, 21), (113, 22), (117, 23),
     (120, 27), (122, 31), (124, 35), (127, 38), (129, 35), (132, 38),
     (135, 43), (138, 46), (141, 50), (142, 52), (140, 57), (137, 60),
     (133, 65), (128, 70), (120, 73), (113, 74), (105, 76), (98, 76),
     (90, 75), (82, 73), (75, 72), (68, 70), (60, 69), (55, 65), (52, 60),
     (50, 55), (47, 52), (44, 48), (41, 45), (38, 42), (35, 41), (32, 38),
     (30, 36)],
    [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -27), (150, -23), (146, -19), (143, -15), (142, -11), (137, -12),
     (132, -12), (127, -14), (124, -17), (120, -20), (116, -21)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (141, 45), (139, 41), (137, 38), (134, 35),
     (131, 33)],
    [(167, -45), (170, -42), (173, -41), (175, -38), (177, -38), (174, -41),
     (171, -44), (168, -46)],
    [(109, -1), (113, -3), (117, -1), (119, 1), (117, 5), (114, 4), (110, 1)],
    [(131, -1), (136, -3), (141, -3), (146, -6), (147, -9), (143, -9),
     (138, -8), (133, -4)],
]

# story number -> (lon, lat) for the map pins; 5 is Mercury (space), no pin.
PINS = {
    1: (85.0, 19.5), 2: (33.0, 53.0), 3: (31.0, 34.0), 4: (134.0, 39.0),
    6: (2.0, 53.0), 7: (141.0, 34.0), 8: (116.4, 39.9), 9: (174.8, -41.3),
    10: (-1.0, 41.0), 11: (56.5, 26.5), 12: (16.0, 39.0), 13: (126.0, 36.0),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)

    def proj(lon, lat):
        px = x + (lon + 168.0) / 360.0 * w
        py = y + (84.0 - lat) / 142.0 * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN)
    # graticule
    for lon in (-120, -60, 0, 60, 120):
        px = x + (lon + 168.0) / 360.0 * w
        d.line([(px, y), (px, y + h)], fill=(44, 66, 96), width=1)
    for lat in (60, 30, 0, -30):
        py = y + (84.0 - lat) / 142.0 * h
        d.line([(x, py), (x + w, py)], fill=(44, 66, 96), width=1)
    # pins
    for n, (lon, lat) in sorted(PINS.items()):
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE, width=2)
        f = font(F_SANS_BOLD, 9 if n < 10 else 8)
        twd = d.textlength(str(n), font=f)
        d.text((px - twd / 2, py - 5), str(n), font=f, fill=WHITE)
    # space tag for story 5
    d.ellipse([x + 10, y + h - 22, x + 24, y + h - 8], fill=RED, outline=WHITE, width=2)
    d.text((x + 17, y + h - 21), "5", font=font(F_SANS_BOLD, 9), fill=WHITE)
    d.text((x + 28, y + h - 22), "SPACE \u00b7 Mercury", font=font(F_SANS_BOLD, 10),
           fill=WHITE)


# ---------------------------------------------------------------- page build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    RX = W - M
    CW = W - 2 * M

    # outer border
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- top bar
    y = 12
    d.text((M, y), "THE WORLD IN ONE DAY", font=font(F_SANS_BOLD, 13), fill=RED)
    right = "FRIDAY\u2019S NEWS \u00b7 ONE PAGE \u00b7 36 STORIES \u00b7 6 CONTINENTS"
    d.text((RX - tw(d, right, font(F_SANS_BOLD, 11)), y + 1), right,
           font=font(F_SANS_BOLD, 11), fill=INK)

    # ---- masthead
    y = 30
    title = "Friday 20 November 2026"
    tf = font(F_SERIF_BLACK, 60)
    d.text(((W - tw(d, title, tf)) / 2, y), title, font=tf, fill=INK)
    y = 96
    sub = ("Cyclone Akvan strikes India \u00b7 Ballistic missiles hit Kyiv \u00b7 "
           "COP31 deadlocked on final day \u00b7 Asian AI sell-off")
    sf = font(F_SERIF_IT, 17)
    d.text(((W - tw(d, sub, sf)) / 2, y), sub, font=sf, fill=BROWN)
    y = 120
    hrule(d, M, RX, y, 3)
    hrule(d, M, RX, y + 5, 1)

    # ---- stats strip
    y = 128
    cell = CW // 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cell
        nf = font(F_SERIF_BOLD, 26)
        d.text((cx + 4, y), num, font=nf, fill=RED)
        para(d, cx + 4, y + 30, cap, font(F_SANS, 10), cell - 10, 12, fill=GREY,
             max_lines=1)
        if i:
            d.line([(cx, y + 2), (cx, y + 44)], fill=(200, 192, 172), width=1)
    y = 176
    hrule(d, M, RX, y, 1)

    # ---- region chips
    y = 182
    cx = M
    for label, col in CHIPS:
        f = font(F_SANS_BOLD, 10)
        wch = tw(d, label, f) + 12
        d.rounded_rectangle([cx, y, cx + wch, y + 19], radius=3, fill=col)
        d.text((cx + 6, y + 4), label, font=f, fill=WHITE)
        cx += wch + 6
    note = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
    d.text((RX - tw(d, note, font(F_SANS, 10)), y + 4), note,
           font=font(F_SANS, 10), fill=GREY)

    # ---- three feature cards
    y = 207
    fw = (CW - 2 * 12) // 3
    fh = 244
    for i, s in enumerate(FEATURES):
        fx = M + i * (fw + 12)
        d.rectangle([fx, y, fx + fw - 1, y + fh - 1], outline=INK, width=1)
        ART[s["art"]](d, fx + 1, y + 1, fw - 2, 132)
        # strip over the bottom of the illustration
        d.rectangle([fx + 1, y + 112, fx + fw - 2, y + 133], fill=(0, 0, 0))
        stf = font(F_SANS_BOLD, 11)
        d.text((fx + 8, y + 117), s["strip"], font=stf, fill=(255, 210, 90))
        ty = y + 138
        kick = f"{s['n']:02d} \u00b7 {s['place']} \u00b7 {s['tag']}"
        d.text((fx + 6, ty), kick, font=font(F_SANS_BOLD, 11), fill=RED)
        ty += 16
        ty = para(d, fx + 6, ty, s["head"], font(F_SERIF_BOLD, 20), fw - 12, 22,
                  max_lines=3)
        ty += 3
        ty = para(d, fx + 6, ty, s["body"], font(F_SERIF, 12), fw - 12, 15,
                  max_lines=3)
        d.text((fx + 6, y + fh - 16), s["src"], font=font(F_SERIF_IT, 10), fill=GREY)
    y += fh + 8

    # ---- ten medium cards, two rows of five
    mw = (CW - 4 * 10) // 5
    mh = 144
    for row in range(2):
        for col in range(5):
            s = MEDIUMS[row * 5 + col]
            mx = M + col * (mw + 10)
            my = y + row * (mh + 8)
            d.rectangle([mx, my, mx + mw - 1, my + mh - 1], outline=INK, width=1)
            ART[s["art"]](d, mx + 1, my + 1, mw - 2, 56)
            ty = my + 61
            kick = f"{s['n']:02d} \u00b7 {s['place']} \u00b7 {s['tag']}"
            d.text((mx + 5, ty), fit_one(d, kick, font(F_SANS_BOLD, 9), mw - 10),
                   font=font(F_SANS_BOLD, 9), fill=RED)
            ty += 13
            ty = para(d, mx + 5, ty, s["head"], font(F_SERIF_BOLD, 13), mw - 10, 15,
                      max_lines=2)
            ty += 1
            ty = para(d, mx + 5, ty, s["body"], font(F_SERIF, 11), mw - 10, 13,
                      max_lines=2)
            d.text((mx + 5, my + mh - 13), s["src"], font=font(F_SERIF_IT, 9),
                   fill=GREY)
    y += 2 * mh + 8 + 8

    # ---- bottom: map + briefs
    by = y
    bh = 158
    map_w = 300
    d.text((M, by), "WHERE IT HAPPENED", font=font(F_SANS_BOLD, 12), fill=RED)
    draw_map(d, M, by + 17, map_w, bh - 17)
    bx = M + map_w + 12
    bw = RX - bx
    d.text((bx, by), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES",
           font=font(F_SANS_BOLD, 12), fill=RED)
    d.text((RX - tw(d, "BRIEFS 14\u201336", font(F_SANS, 10)), by + 1),
           "BRIEFS 14\u201336", font=font(F_SANS, 10), fill=GREY)
    col_w = (bw - 10) // 2
    bf = font(F_SANS, 10)
    bf_b = font(F_SANS_BOLD, 10)
    ly = by + 17
    for i, (city, text, src) in enumerate(BRIEFS):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        lx = bx + col * (col_w + 10)
        yy = ly + row * 12
        num = 14 + i
        label = f"{num} {city} \u2014 "
        d.text((lx, yy), label, font=bf_b, fill=INK)
        rest = fit_one(d, f"{text} ({src})", bf, col_w - tw(d, label, bf_b))
        d.text((lx + tw(d, label, bf_b), yy), rest, font=bf, fill=INK)
    y = by + bh + 8

    # ---- date check
    d.rectangle([M, y, RX, y + 54], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=font(F_SANS_BOLD, 11), fill=RED)
    para(d, M + 8, y + 19, DATE_CHECK, font(F_SANS, 10), CW - 16, 12, fill=INK,
         max_lines=3)
    y += 60

    # ---- footer
    para(d, M, y, FOOTER, font(F_SANS, 9), CW, 11, fill=GREY, max_lines=1)

    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
