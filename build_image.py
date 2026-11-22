#!/usr/bin/env python3
"""Build the news-image entry for Sunday 22 November 2026.

Draws a one-page newspaper-style collage of the day's world news with PIL
and writes entry.png beside this file. The shipped program (main.py) only
copies entry.png to the output directory; this script is the drawing tool
used at build time, kept in the repository for transparency.

Stories (all happened, or were first reported, on 22 November 2026):
  - COP31, the UN climate summit in Antalya, Turkiye, entered a second
    day of overtime, deadlocked over fossil fuels after a $120 billion
    adaptation target for poorer nations was dropped from the draft
    (BBC Science, The Straits Times).
  - Bahrain says an Iranian strike set a civilian industrial site on
    fire; two oil tankers were hit near the Strait of Hormuz (The Japan
    Times, UKMTO reports).
  - The Saudi-led coalition says it intercepted three Houthi ballistic
    missiles fired at Riyadh; it also struck Yemen's port of Hodeidah.
  - Ukraine's strikes on the Crimean bridge strain Russian logistics
    (The Japan Times analysis).
  - A boat carrying mourners to a funeral capsized in southern Nigeria:
    at least 24 dead, 24 rescued (Al Jazeera, UPI).
  - A candy factory fire near Jakarta, Indonesia, killed 3, with dozens
    missing; a magnitude 6.7 earthquake struck Peru; French protesters
    rallied for a sixth weekend over living costs.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W = H = 1024
MARGIN = 34
CW = W - 2 * MARGIN  # content width

PAPER = (247, 243, 234)
INK = (18, 28, 40)
GREY = (96, 104, 112)
RULE_RED = (193, 39, 45)
NAVY = (19, 44, 74)
NAVY_TEXT = (216, 226, 238)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, size, max_width, max_lines, min_size=20):
    """Wrap at the largest size (<= size) that fits max_lines."""
    s = size
    while s > min_size:
        lines = wrap(draw, text, bold(s), max_width)
        if len(lines) <= max_lines:
            return bold(s), lines
        s -= 2
    return bold(min_size), wrap(draw, text, bold(min_size), max_width)[:max_lines]


# ---------------------------------------------------------------- icons
def star_points(cx, cy, r_out, r_in, n=12, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_burst(d, cx, cy, r, color=(255, 170, 40), core=(214, 48, 49)):
    d.polygon(star_points(cx, cy, r, r * 0.45), fill=color)
    d.ellipse([cx - r * 0.34, cy - r * 0.34, cx + r * 0.34, cy + r * 0.34], fill=core)


def icon_missile(d, cx, cy, r, body=(120, 130, 145), tip=(214, 48, 49)):
    d.polygon([(cx - 6, cy + 20), (cx + 14, cy - 26), (cx + 26, cy - 14),
               (cx - 20, cy + 32)], fill=body)
    d.polygon([(cx + 14, cy - 26), (cx + 30, cy - 30), (cx + 26, cy - 14)], fill=tip)
    d.polygon([(cx - 20, cy + 32), (cx - 34, cy + 30), (cx - 26, cy + 18)], fill=tip)
    d.polygon([(cx - 6, cy + 20), (cx - 20, cy + 18), (cx - 14, cy + 32)], fill=tip)
    icon_burst(d, cx - 30, cy + 34, 13)


def icon_globe(d, cx, cy, r, line=(120, 225, 190)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=line, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=line, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=line, width=3)
    d.line([cx - r * 0.87, cy - r * 0.5, cx + r * 0.87, cy - r * 0.5], fill=line, width=3)
    d.line([cx - r * 0.87, cy + r * 0.5, cx + r * 0.87, cy + r * 0.5], fill=line, width=3)


def icon_flame(d, cx, cy, r, outer=(230, 110, 30), inner=(250, 190, 60)):
    d.polygon([(cx, cy - r), (cx + r * 0.62, cy + r * 0.25),
               (cx + r * 0.42, cy + r * 0.85), (cx - r * 0.42, cy + r * 0.85),
               (cx - r * 0.62, cy + r * 0.25)], fill=outer)
    d.polygon([(cx, cy - r * 0.25), (cx + r * 0.3, cy + r * 0.35),
               (cx + r * 0.18, cy + r * 0.8), (cx - r * 0.18, cy + r * 0.8),
               (cx - r * 0.3, cy + r * 0.35)], fill=inner)


def icon_bridge(d, cx, cy, r, line=(70, 90, 120)):
    deck_y = cy + r * 0.55
    d.line([cx - r, deck_y, cx + r, deck_y], fill=line, width=5)
    d.arc([cx - r, cy - r * 0.75, cx + r, deck_y + r * 0.55],
          start=180, end=360, fill=line, width=4)
    for fx in (-0.66, -0.33, 0.0, 0.33, 0.66):
        top = cy - r * 0.1 - r * 0.62 * (1 - fx * fx) ** 0.5
        d.line([cx + fx * r, top, cx + fx * r, deck_y], fill=line, width=3)
    d.line([cx - r * 0.8, cy + r, cx + r * 0.8, cy + r], fill=(90, 150, 200), width=4)


def icon_waves(d, cx, cy, r, hull=(120, 72, 30), wave=(40, 110, 180)):
    d.polygon([(cx - r * 0.7, cy - r * 0.1), (cx + r * 0.7, cy - r * 0.1),
               (cx + r * 0.45, cy + r * 0.3), (cx - r * 0.45, cy + r * 0.3)],
              fill=hull)
    d.polygon([(cx, cy - r * 0.95), (cx, cy - r * 0.15), (cx + r * 0.55, cy - r * 0.15)],
              fill=(200, 60, 50))
    for dy in (0.55, 0.85):
        pts = [(cx - r + i * 4, cy + r * dy + 5 * math.sin(i / 3.2))
               for i in range(int(2 * r / 4) + 1)]
        d.line(pts, fill=wave, width=4)


ICONS = {"burst": icon_burst, "missile": icon_missile, "globe": icon_globe,
         "flame": icon_flame, "bridge": icon_bridge, "waves": icon_waves}


# ---------------------------------------------------------------- layout
def chip(d, x, y, text, color):
    f = bold(19)
    w = d.textlength(text, font=f) + 22
    d.rounded_rectangle([x, y, x + w, y + 30], radius=6, fill=color)
    d.text((x + 11, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def draw_card(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(255, 255, 255),
                        outline=(205, 198, 182), width=2)
    chip(d, x + 18, y + 14, story["tag"], story["color"])
    ICONS[story["icon"]](d, x + w - 52, y + 46, 30)
    hf, hlines = fit_lines(d, story["headline"], 29, w - 130, 2, min_size=23)
    ty = y + 54
    for ln in hlines:
        d.text((x + 18, ty), ln, font=hf, fill=INK)
        ty += hf.size + 5
    sf = regular(20)
    for ln in wrap(d, story["summary"], sf, w - 36)[:2]:
        d.text((x + 18, ty + 4), ln, font=sf, fill=(52, 62, 74))
        ty += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    kicker = "THE WORLD IN ONE DAY"
    kf = bold(24)
    d.text(((W - d.textlength(kicker, font=kf)) / 2, 26), kicker, font=kf,
           fill=RULE_RED)
    date = "SUNDAY 22 NOVEMBER 2026"
    df = bold(57)
    d.text(((W - d.textlength(date, font=df)) / 2, 58), date, font=df, fill=INK)
    d.rectangle([MARGIN, 138, W - MARGIN, 143], fill=RULE_RED)
    d.rectangle([MARGIN, 148, W - MARGIN, 150], fill=INK)

    # lead story
    ly, lh = 166, 282
    d.rounded_rectangle([MARGIN, ly, W - MARGIN, ly + lh], radius=14, fill=NAVY)
    chip(d, MARGIN + 24, ly + 20, "LEAD STORY · CLIMATE", (14, 124, 102))
    icon_globe(d, W - MARGIN - 74, ly + 66, 44)
    hf, hlines = fit_lines(d, "COP31 CLIMATE TALKS DEADLOCKED IN OVERTIME",
                           47, CW - 190, 2, min_size=36)
    ty = ly + 64
    for ln in hlines:
        d.text((MARGIN + 24, ty), ln, font=hf, fill=(255, 255, 255))
        ty += hf.size + 6
    sf = regular(24)
    lead_sum = ("The UN summit in Antalya, Türkiye enters a second day of overtime, "
                "split over fossil fuels after a $120bn adaptation fund for poorer "
                "nations was dropped from the draft deal.")
    for ln in wrap(d, lead_sum, sf, CW - 48)[:3]:
        d.text((MARGIN + 24, ty + 4), ln, font=sf, fill=NAVY_TEXT)
        ty += 31

    # story grid, 2 x 2
    stories = [
        {"tag": "GULF · HORMUZ", "color": (146, 44, 40), "icon": "flame",
         "headline": "Iran hits Bahrain site; tankers struck in Hormuz",
         "summary": "Bahrain says Iran set a civilian site ablaze; two "
                    "tankers hit near the strait."},
        {"tag": "SAUDI ARABIA", "color": (30, 107, 58), "icon": "missile",
         "headline": "Houthi missiles shot down over Riyadh",
         "summary": "Three ballistic missiles intercepted over the capital; "
                    "Hodeidah port also struck."},
        {"tag": "UKRAINE · CRIMEA", "color": (49, 87, 122), "icon": "bridge",
         "headline": "Ukraine strikes Crimean bridge, squeezing Russia",
         "summary": "Kyiv's strikes on the bridge and supply lines strain "
                    "Russian forces in Crimea."},
        {"tag": "NIGERIA · DISASTER", "color": (141, 110, 0), "icon": "waves",
         "headline": "24 die as funeral boat capsizes in Nigeria",
         "summary": "Boat carrying mourners overturned in the south; 24 "
                    "rescued, driver fled."},
    ]
    gx, gy = MARGIN, 464
    gw, gh, gap = (CW - 16) // 2, 186, 16
    for i, story in enumerate(stories):
        draw_card(d, gx + (i % 2) * (gw + gap), gy + (i // 2) * (gh + gap),
                  gw, gh, story)

    # also today strip
    sy = gy + 2 * gh + gap + 14
    d.rounded_rectangle([MARGIN, sy, W - MARGIN, sy + 96], radius=12,
                        fill=(236, 230, 216))
    d.text((MARGIN + 18, sy + 10), "ALSO TODAY", font=bold(20), fill=RULE_RED)
    items = ("Indonesia candy-factory fire kills 3, dozens missing  •  "
             "Magnitude 6.7 earthquake strikes Peru  •  "
             "France rallies for a sixth weekend over living costs")
    ty = sy + 40
    for ln in wrap(d, items, regular(22), CW - 36)[:2]:
        d.text((MARGIN + 18, ty), ln, font=regular(22), fill=INK)
        ty += 27

    # footer
    foot = ("Sunday 22 November 2026 · Sources: BBC · Al Jazeera · "
            "The Japan Times · UPI · Sky News")
    ff = regular(18)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 970), foot, font=ff, fill=GREY)
    d.rectangle([MARGIN, 998, W - MARGIN, 1002], fill=RULE_RED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
