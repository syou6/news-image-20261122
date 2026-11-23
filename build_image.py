#!/usr/bin/env python3
"""Build the news-image entry for Sunday 22 November 2026.

Draws a dense one-page newspaper front page with PIL and writes
entry.png beside this file. The shipped program (main.py) only copies
entry.png to the output directory; this script is the drawing tool used
at build time, kept in the repository for transparency.

Every story drawn here happened, or was first reported, on Sunday
22 November 2026 (in some time zone). The page carries 53 stories:
1 lead, 4 secondary cards, 40 one-line briefs in six regional groups
and 8 sport results, under nine sections in all.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width = 968

PAPER = (250, 247, 240)
INK = (20, 22, 26)
GREY = (96, 100, 104)
RED = (178, 30, 35)
NAVY = (16, 38, 66)
NAVY_TX = (216, 226, 238)
TEAL = (14, 110, 96)
GOLD = (168, 124, 32)
CARD = (255, 254, 249)
RULE = (52, 56, 62)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return font("DejaVuSans.ttf", size)


def serif_bold(size):
    return font("DejaVuSerif-Bold.ttf", size)


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def text_block(draw, x, y, text, fnt, fill, max_width, leading=None):
    """Draw wrapped text; return the y just below it."""
    lines = wrap(draw, text, fnt, max_width)
    step = leading or int(fnt.size * 1.3)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def hline(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def centred(draw, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


# ---------------------------------------------------------------- masthead
def draw_masthead(draw):
    y = 12
    draw.text((MARGIN, y), "THE WORLD IN ONE PAGE", font=serif_bold(20),
              fill=NAVY)
    tag = "53 stories \u00b7 9 regions \u00b7 one day"
    tf = regular(14)
    tw = draw.textlength(tag, font=tf)
    draw.text((W - MARGIN - tw, y + 4), tag, font=tf, fill=GREY)
    y += 28
    hline(draw, MARGIN, W - MARGIN, y, fill=INK, width=3)
    y += 7
    # the date is the largest text on the page; shrink only if needed
    date = "SUNDAY 22 NOVEMBER 2026"
    size = 62
    while size > 30 and draw.textlength(date, font=serif_bold(size)) > CW:
        size -= 2
    y = centred(draw, y, date, serif_bold(size), INK)
    sub = ("COP31 deadlocked in Antalya \u2014 missiles over Riyadh \u2014 "
           "tankers hit in Hormuz \u2014 Nigeria boat disaster")
    y = centred(draw, y - 2, sub, regular(15), RED)
    hline(draw, MARGIN, W - MARGIN, y, fill=RED, width=3)
    return y + 8


# ---------------------------------------------------------------- lead
def draw_lead_visual(draw, x, y, w, h):
    """A cracked globe over a heat bar: talks stuck, planet warming."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx, cy, r = x + w // 2 - 18, y + h // 2 - 10, 62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(62, 110, 164))
    draw.ellipse([cx - 44, cy - 36, cx - 6, cy - 4], fill=(94, 152, 94))
    draw.ellipse([cx - 24, cy + 4, cx + 4, cy + 38], fill=(94, 152, 94))
    draw.ellipse([cx + 10, cy - 32, cx + 48, cy - 2], fill=(94, 152, 94))
    draw.ellipse([cx + 22, cy + 8, cx + 44, cy + 30], fill=(94, 152, 94))
    crack = [(cx - 4, cy - r), (cx + 8, cy - 32), (cx - 8, cy - 4),
             (cx + 10, cy + 24), (cx - 2, cy + r)]
    draw.line(crack, fill=(250, 240, 200), width=4)
    # heat bar at the right edge
    bx = x + w - 30
    draw.rectangle([bx, y + 18, bx + 9, y + h - 34], fill=(228, 232, 236))
    draw.rectangle([bx, y + 34, bx + 9, y + h - 34], fill=RED)
    draw.ellipse([bx - 6, y + h - 46, bx + 15, y + h - 25], fill=RED)
    cap = "ANTALYA, T\u00dcRKIYE \u2014 NO DEAL YET"
    cf = bold(12)
    tw = draw.textlength(cap, font=cf)
    draw.text((x + (w - tw) / 2, y + h - 20), cap, font=cf, fill=NAVY_TX)


def draw_lead(draw, y):
    h = 196
    draw.rectangle([MARGIN, y, W - MARGIN, y + h], fill=CARD,
                   outline=RULE, width=2)
    tx = MARGIN + 16
    draw.text((tx, y + 10), "LEAD STORY \u2014 ANTALYA, T\u00dcRKIYE \u2014 CLIMATE",
              font=bold(13), fill=RED)
    y2 = text_block(draw, tx, y + 32,
                    "COP31 TALKS DEADLOCKED INTO A SECOND DAY OF OVERTIME",
                    serif_bold(28), INK, 592, leading=35)
    text_block(draw, tx, y2 + 6,
               "The UN climate summit in Antalya is split over fossil fuels "
               "after a $120bn adaptation fund for poorer nations was "
               "dropped from the draft text, with talks running into a "
               "second day of overtime. (BBC)",
               regular(14), INK, 592, leading=18)
    draw_lead_visual(draw, MARGIN + 624, y + 12, 332, 172)
    return y + h + 10


# ---------------------------------------------------------------- secondary
SECONDARY = [
    ("MIDDLE EAST \u2014 THE GULF", RED,
     "Iran hits Bahrain site; two tankers struck near Hormuz",
     "An Iranian strike set a Bahrain industrial site ablaze, and two "
     "oil tankers were struck near the Strait of Hormuz. (Reuters / "
     "Japan Times)"),
    ("SAUDI ARABIA \u2014 RIYADH", TEAL,
     "Three Houthi missiles intercepted over Riyadh",
     "Air defences downed three ballistic missiles over the capital; "
     "the coalition also struck Yemen's Hodeidah port. (Saudi Gazette "
     "/ Arab News)"),
    ("EUROPE \u2014 UKRAINE WAR", NAVY,
     "Ukraine strikes the Crimean bridge, squeezing Russia",
     "Kyiv's strike on the bridge strains Russian logistics into "
     "occupied Crimea and the southern front. (Japan Times)"),
    ("AFRICA \u2014 NIGERIA", GOLD,
     "Funeral boat capsizes in Nigeria: 24 dead, 24 rescued",
     "A boat carrying mourners overturned in the south; 24 people "
     "died, 24 were rescued and the driver fled. (Al Jazeera / UPI)"),
]


def draw_secondary(draw, y):
    gap = 12
    cw = (CW - 3 * gap) // 4
    ch = 158
    for i, (kicker, colour, head, body) in enumerate(SECONDARY):
        x = MARGIN + i * (cw + gap)
        draw.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=RULE,
                       width=2)
        draw.rectangle([x, y, x + cw, y + 7], fill=colour)
        draw.text((x + 10, y + 13), kicker, font=bold(10), fill=colour)
        y2 = text_block(draw, x + 10, y + 31, head, bold(15), INK,
                        cw - 20, leading=19)
        text_block(draw, x + 10, y2 + 3, body, regular(11), INK,
                   cw - 20, leading=14)
    return y + ch + 10


# ---------------------------------------------------------------- briefs
# One line each, compressed to fit a column; facts and figures kept.
BRIEF_COLS = [
    [("EUROPE", RED, [
        "Russian strikes flatten block in Dymer, Kyiv region",
        "Cargo ship fire in the Gulf of Finland",
        "Tusk: missiles in Poland a Russian 'provocation'",
        "France rallies a 6th weekend over living costs",
        "Gen Z protests in 25+ countries: schools, not war",
        "UK-EU clinch food and youth-mobility deals",
        "Merz in Doha; Qatar pledges \u20ac15bn investment",
        "French police jailed for racist violence",
    ]), ("AFRICA", (34, 110, 66), [
        "Russian corvette destroyed at Benghazi, Libya",
        "Sudan files UN/AU complaints over Ethiopia drones",
        "Khartoum airport drones intercepted by defences",
        "WHO chief condemns attacks on Ethiopian civilians",
        "Kenya papers weigh 'third force' vs Ruto for 2027",
    ])],
    [("MIDDLE EAST", GOLD, [
        "Hartha power-station fire, Basra: 4 dead, 35 hurt",
        "Gulf states demand Iran pay for attacks",
        "Iran to ration power as strikes batter the grid",
        "Trump delays Iran strike call until after Jan 1",
        "Pentagon: Iran war cost $48.3bn since February",
        "British swimmer crosses the Strait of Hormuz",
    ]), ("ASIA-PACIFIC", NAVY, [
        "Indonesia candy-factory fire: 3 dead, dozens missing",
        "Toxic alcohol in Manipur: 11 dead, 180+ in hospital",
        "Pakistan bus hits gas tanker: 10 dead, 27 hurt",
        "S. Korea education minister quits in AI-cheat scandal",
        "Shuri Castle hall restored, 7 years after the fire",
        "China-Russia nuclear declaration at Shenzhen summit",
        "Nepal's prime minister visits Delhi for talks",
        "Zelda tops Japan's game charts",
    ])],
    [("AMERICAS", (110, 52, 130), [
        "St. Johns River floods break 73-year record, Florida",
        "Mexico captures FBI-wanted 'El Chapo Isidro'",
        "'Horrific' Seattle airport arrests fuel ICE anger",
        "FBI database breach under investigation",
    ]), ("ECONOMY + SCIENCE + CULTURE", (150, 84, 20), [
        "Amazon signs a $7.5bn AI deal with Decart",
        "GTA 6 sets a $3.79bn launch record",
        "US panel alleges Chinese support for Pakistan",
        "Pernod Ricard weighs an India IPO",
        "Tiny asteroid becomes Earth's new mini-moon",
        "ESA's BepiColombo enters Mercury orbit",
        "Lattice cryptography finds a hidden Fermi pulsar",
        "Hunger Games premiere goes viral",
        "US recall pulls toothpaste and mouthwash from shelves",
    ])],
]


def draw_brief_line(draw, x, y, text, max_width):
    """One brief on one line; drop a point size if it would overflow."""
    f = regular(10)
    if draw.textlength(text, font=f) > max_width:
        f = regular(9)
    draw.text((x, y), text, font=f, fill=INK)


def draw_briefs(draw, y):
    draw.text((MARGIN, y), "AROUND THE WORLD IN BRIEF \u2014 SUNDAY 22 NOVEMBER",
              font=bold(15), fill=NAVY)
    y += 24
    gap = 14
    cw = (CW - 2 * gap) // 3
    bottom = y
    for i, sections in enumerate(BRIEF_COLS):
        x = MARGIN + i * (cw + gap)
        cy = y
        for name, colour, items in sections:
            draw.rectangle([x, cy, x + cw, cy + 16], fill=colour)
            draw.text((x + 6, cy + 2), name, font=bold(11),
                      fill=(255, 255, 255))
            cy += 20
            for item in items:
                draw_brief_line(draw, x + 2, cy, item, cw - 4)
                cy += 14
            cy += 5
        bottom = max(bottom, cy)
    return bottom + 2


# ---------------------------------------------------------------- sport
SPORT_LINE = ("SPORT: Liverpool thrash Manchester United 4-0 \u2022 Verstappen "
              "wins the Las Vegas Grand Prix \u2022 Wembanyama scores 50 as "
              "the Spurs win \u2022 Kansas City Current win a first NWSL title "
              "\u2022 NFL: Lions 31-21 Buccaneers, Bills 26-9 Dolphins, "
              "Cowboys 51-30 Titans \u2022 Bayern striker sidelined with an "
              "ankle injury")


def draw_sport(draw, y):
    hline(draw, MARGIN, W - MARGIN, y, fill=RULE, width=2)
    y += 6
    y = text_block(draw, MARGIN, y, SPORT_LINE, regular(11), INK, CW,
                   leading=14)
    hline(draw, MARGIN, W - MARGIN, y + 1, fill=RULE, width=2)
    return y + 7


# ------------------------------------------------------- timeline and map
TIMELINE = [
    "ANTALYA: COP31 talks run into a second overtime day",
    "RIYADH: three Houthi missiles intercepted",
    "HORMUZ: two oil tankers struck near the strait",
    "KYIV REGION: strikes hit Dymer and the Crimean bridge",
    "BASRA: power-station fire kills four",
    "LAS VEGAS: Verstappen wins the night race",
    "LIVERPOOL: Reds thrash United 4-0",
]

SOURCES = ("Sources: BBC \u00b7 Reuters \u00b7 Japan Times \u00b7 Al Jazeera \u00b7 "
           "UPI \u00b7 Saudi Gazette \u00b7 Arab News \u00b7 SCMP \u00b7 RFE/RL")

# Coarse dot-grid world map, one character per dot cell ('#' is land).
WORLD_MAP = [
    "                                                                ",
    "        #########                                               ",
    "      ##############        ####  ###############               ",
    "     ################      #############################        ",
    "      #############  ##   ###############################       ",
    "       ##########         ################  ############        ",
    "        ########           ##############    #########          ",
    "         ######             ############      #######           ",
    "          #####              ##########        #####            ",
    "          ####                ########         ####             ",
    "          ###                  ######           ##   ##         ",
    "          ##                   #####                 ###        ",
    "                              ####                   ####       ",
    "                              ###                     ##        ",
    "                              ##                                        ",
    "                                                                ",
]

# (name, grid col, grid row, label dx, label dy) - approximate positions,
# each checked to sit on (or, for the Hormuz strait, just beside) land dots
MAP_PINS = [
    ("Kyiv", 35, 4, 6, -3),
    ("Antalya", 36, 6, 8, 1),
    ("Riyadh", 36, 9, -36, 2),
    ("Hormuz", 40, 8, 7, 2),
    ("Lagos", 33, 11, 6, 0),
]


def draw_map(draw, x, y, w):
    draw.rectangle([x, y, x + w, y + 176], fill=(238, 240, 244),
                   outline=RULE, width=2)
    draw.text((x + 10, y + 7), "THE DAY ON THE MAP", font=bold(11),
              fill=NAVY)
    # 60 columns max across the box; rows stretched vertically to fill it
    ox, oy, step_x, step_y = x + 13, y + 30, 5, 8
    land = (140, 152, 168)
    for r, row in enumerate(WORLD_MAP):
        for c, ch in enumerate(row[:60]):
            if ch == "#":
                px, py = ox + c * step_x, oy + r * step_y
                draw.ellipse([px, py, px + 2, py + 3], fill=land)
    lf = bold(8)
    for name, c, r, dx, dy in MAP_PINS:
        px, py = ox + c * step_x, oy + r * step_y
        draw.ellipse([px - 3, py - 3, px + 4, py + 4], fill=RED,
                     outline=(255, 255, 255), width=1)
        lx, ly = px + dx, py + dy - 3
        lw = draw.textlength(name, font=lf)
        draw.rectangle([lx - 1, ly - 1, lx + lw + 1, ly + 10],
                       fill=(238, 240, 244))
        draw.text((lx, ly), name, font=lf, fill=RED)


def draw_bottom(draw, y):
    h = H - 16 - y
    tw = 630
    draw.rectangle([MARGIN, y, MARGIN + tw, y + h], fill=NAVY)
    draw.text((MARGIN + 12, y + 7), "THE DAY AROUND THE CLOCK (UTC)",
              font=bold(13), fill=(232, 190, 90))
    ty = y + 30
    for event in TIMELINE:
        draw.ellipse([MARGIN + 12, ty + 4, MARGIN + 21, ty + 13],
                     fill=(232, 190, 90))
        draw.text((MARGIN + 27, ty), event, font=regular(12), fill=NAVY_TX)
        ty += 19
    draw.text((MARGIN + 12, y + h - 18), SOURCES, font=regular(9),
              fill=(150, 165, 185))
    draw_map(draw, MARGIN + tw + 12, y, CW - tw - 12)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_secondary(draw, y)
    y = draw_briefs(draw, y)
    y = draw_sport(draw, y)
    draw_bottom(draw, y)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
