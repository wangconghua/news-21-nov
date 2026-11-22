#!/usr/bin/env python3
"""Render the 21 November 2026 world-news infographic (1024x1024 PNG).

Six verified stories from Saturday 21 November 2026, laid out as a
two-column grid of cards under a dated masthead. Every pictogram is drawn
from PIL primitives; no external images, no network, no randomness, so two
runs produce byte-identical output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (13, 27, 46)
CARD = (21, 42, 69)
CARD_EDGE = (42, 74, 107)
WHITE = (244, 246, 248)
MUTED = (199, 211, 224)
GOLD = (201, 162, 39)
FAINT = (120, 138, 158)

STORIES = [
    {
        "kicker": "WAR  ·  UKRAINE & POLAND",
        "accent": (229, 72, 77),
        "icon": "missile",
        "headline": "Russian missiles land in Poland",
        "detail": "404 drones and 111 missiles hit Ukraine overnight; debris falls in Poland.",
    },
    {
        "kicker": "WAR  ·  UKRAINE",
        "accent": (247, 107, 21),
        "icon": "city",
        "headline": "Strike hits Zelenskyy's hometown",
        "detail": "A Russian ballistic strike on Kryvyi Rih kills 2 and wounds 60 in a double-tap attack.",
    },
    {
        "kicker": "JUSTICE  ·  THE HAGUE",
        "accent": (229, 181, 69),
        "icon": "scales",
        "headline": "Myanmar guilty of genocide",
        "detail": "The World Court rules Myanmar committed genocide against the Rohingya; Myanmar rejects the verdict.",
    },
    {
        "kicker": "MARKETS",
        "accent": (42, 183, 169),
        "icon": "chart",
        "headline": "AI stocks plunge, S&P slides",
        "detail": "Chip shares lead a sharp sell-off; the S&P 500 drops 3.7% as the AI rally unwinds.",
    },
    {
        "kicker": "CLIMATE  ·  ANTALYA",
        "accent": (76, 154, 255),
        "icon": "globe",
        "headline": "COP31 talks stall in overtime",
        "detail": "Climate negotiations in Antalya grind past their deadline with no deal yet in sight.",
    },
    {
        "kicker": "CRIME  ·  MEXICO",
        "accent": (176, 124, 255),
        "icon": "cuffs",
        "headline": "Mexico captures cartel boss",
        "detail": "Troops seize 'El Chapo Isidro', one of the FBI's most wanted, with US help.",
    },
]


def load(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_missile(d, x, y, s, color):
    """A rocket climbing to the upper right: nose cone, body, fins, flame."""
    d.polygon(
        [(x + 0.58 * s, y + 0.02 * s), (x + 0.80 * s, y + 0.24 * s),
         (x + 0.66 * s, y + 0.36 * s), (x + 0.46 * s, y + 0.14 * s)],
        fill=color,
    )
    d.polygon(
        [(x + 0.46 * s, y + 0.14 * s), (x + 0.66 * s, y + 0.36 * s),
         (x + 0.34 * s, y + 0.68 * s), (x + 0.14 * s, y + 0.48 * s)],
        fill=color,
    )
    d.polygon(
        [(x + 0.14 * s, y + 0.48 * s), (x + 0.34 * s, y + 0.68 * s),
         (x + 0.30 * s, y + 0.82 * s), (x + 0.08 * s, y + 0.60 * s)],
        fill=color,
    )
    d.polygon(
        [(x + 0.66 * s, y + 0.36 * s), (x + 0.80 * s, y + 0.24 * s),
         (x + 0.88 * s, y + 0.38 * s), (x + 0.72 * s, y + 0.44 * s)],
        fill=color,
    )
    for bx, by in [(0.02, 0.86), (0.12, 0.94), (0.22, 0.90)]:
        d.ellipse([x + bx * s, y + by * s,
                   x + (bx + 0.09) * s, y + (by + 0.09) * s],
                  fill=color)


def draw_city(d, x, y, s, color):
    """Skyline of three towers with a blast star above the middle one."""
    for bx, bw, bh in [(0.02, 0.26, 0.52), (0.36, 0.30, 0.72), (0.72, 0.26, 0.44)]:
        d.rectangle([x + bx * s, y + (0.98 - bh) * s,
                     x + (bx + bw) * s, y + 0.98 * s], fill=color)
    cx, cy, r1, r2 = x + 0.51 * s, y + 0.14 * s, 0.16 * s, 0.06 * s
    pts = []
    for i in range(8):
        ang = 3.14159 * i / 4
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + r * _cos(ang), cy + r * _sin(ang)))
    d.polygon(pts, fill=color)


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def draw_scales(d, x, y, s, color):
    """Balanced scales of justice: stem, beam, two hanging pans."""
    d.rectangle([x + 0.47 * s, y + 0.06 * s, x + 0.53 * s, y + 0.92 * s],
                fill=color)
    d.rectangle([x + 0.06 * s, y + 0.16 * s, x + 0.94 * s, y + 0.22 * s],
                fill=color)
    for cx in (0.19, 0.81):
        px = x + cx * s
        d.line([px, y + 0.22 * s, px - 0.13 * s, y + 0.58 * s],
               fill=color, width=4)
        d.line([px, y + 0.22 * s, px + 0.13 * s, y + 0.58 * s],
               fill=color, width=4)
        d.arc([px - 0.13 * s, y + 0.52 * s, px + 0.13 * s, y + 0.78 * s],
              0, 180, fill=color, width=5)
    d.rectangle([x + 0.30 * s, y + 0.92 * s, x + 0.70 * s, y + 0.98 * s],
                fill=color)


def draw_chart(d, x, y, s, color):
    """Three falling bars with a descending arrow line."""
    for i, bh in enumerate((0.34, 0.58, 0.82)):
        bx = x + (0.08 + i * 0.30) * s
        d.rectangle([bx, y + (0.98 - bh) * s, bx + 0.20 * s, y + 0.98 * s],
                    fill=color)
    pts = [(x + 0.08 * s, y + 0.10 * s), (x + 0.38 * s, y + 0.34 * s),
           (x + 0.66 * s, y + 0.52 * s), (x + 0.94 * s, y + 0.80 * s)]
    d.line(pts, fill=color, width=6, joint="curve")
    d.polygon([(x + 0.94 * s, y + 0.80 * s), (x + 0.78 * s, y + 0.76 * s),
               (x + 0.92 * s, y + 0.62 * s)], fill=color)


def draw_globe(d, x, y, s, color):
    """A globe: outer circle, two meridians and an equator band."""
    d.ellipse([x + 0.04 * s, y + 0.04 * s, x + 0.96 * s, y + 0.96 * s],
              outline=color, width=5)
    d.ellipse([x + 0.30 * s, y + 0.04 * s, x + 0.70 * s, y + 0.96 * s],
              outline=color, width=4)
    d.line([x + 0.04 * s, y + 0.50 * s, x + 0.96 * s, y + 0.50 * s],
           fill=color, width=4)
    d.arc([x + 0.04 * s, y + 0.26 * s, x + 0.96 * s, y + 0.74 * s],
          200, 340, fill=color, width=4)


def draw_cuffs(d, x, y, s, color):
    """Handcuffs: two rings joined by a short chain link."""
    for cx in (0.26, 0.74):
        px = x + cx * s
        d.ellipse([px - 0.22 * s, y + 0.22 * s, px + 0.22 * s, y + 0.66 * s],
                  outline=color, width=7)
    d.rectangle([x + 0.44 * s, y + 0.40 * s, x + 0.56 * s, y + 0.48 * s],
                fill=color)
    d.ellipse([x + 0.44 * s, y + 0.30 * s, x + 0.56 * s, y + 0.42 * s],
              outline=color, width=4)


ICONS = {
    "missile": draw_missile,
    "city": draw_city,
    "scales": draw_scales,
    "chart": draw_chart,
    "globe": draw_globe,
    "cuffs": draw_cuffs,
}


def draw_card(d, story, x, y, w, h):
    accent = story["accent"]
    d.rounded_rectangle([x, y, x + w, y + h], radius=14,
                        fill=CARD, outline=CARD_EDGE, width=2)
    d.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=accent)
    kicker_f = load(19, bold=True)
    head_f = load(30, bold=True)
    body_f = load(21)
    tx = x + 28
    d.text((tx, y + 16), story["kicker"], font=kicker_f, fill=accent)
    ICONS[story["icon"]](d, x + w - 84, y + 14, 62, accent)
    text_w = w - 28 - 100
    lines = wrap(d, story["headline"], head_f, text_w)
    ly = y + 48
    for line in lines[:2]:
        d.text((tx, ly), line, font=head_f, fill=WHITE)
        ly += 37
    detail = wrap(d, story["detail"], body_f, w - 56)
    for line in detail[:3]:
        d.text((tx, ly), line, font=body_f, fill=MUTED)
        ly += 28


def render(path):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    title_f = load(62, bold=True)
    sub_f = load(25)
    tag_f = load(20, bold=True)
    foot_f = load(20)

    d.text((28, 26), "21 NOVEMBER 2026", font=title_f, fill=WHITE)
    d.text((28, 100), "SATURDAY  ·  THE WORLD IN ONE IMAGE",
           font=sub_f, fill=GOLD)
    tag = "6 STORIES"
    tw = d.textlength(tag, font=tag_f)
    tx0 = W - 28 - tw - 24
    d.rounded_rectangle([tx0, 44, W - 28, 84], radius=18,
                        outline=GOLD, width=2)
    d.text((tx0 + 12, 53), tag, font=tag_f, fill=GOLD)
    d.rectangle([28, 148, W - 28, 152], fill=GOLD)

    margin, gap = 28, 20
    cw = (W - 2 * margin - gap) // 2
    ch = 248
    tops = [168, 436, 704]
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(d, story, margin + col * (cw + gap), tops[row], cw, ch)

    foot = "Six stories that defined Saturday, 21 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 972), foot, font=foot_f, fill=FAINT)

    img.save(path, "PNG")
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print(f"wrote {out}")
