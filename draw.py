#!/usr/bin/env python3
"""Draw the invitation letter image (build time only, Pillow).

Style: lemo-opuscar 'colored-pencil' plate — warm off-white paper
(#F8F4EA), sepia graphite writing (#33241C), restrained amber/green/blue
accents, hand-drawn doodles. One legible letter, 1024x1024 PNG.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (248, 244, 234)
INK = (51, 36, 28)          # sepia graphite
INK_SOFT = (96, 74, 58)
AMBER = (201, 138, 43)
GREEN = (94, 138, 58)
BLUE = (122, 157, 181)
RED_SEAL = (178, 58, 44)
PALE_BLUE = (179, 212, 230)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

TITLE = "An Invitation"
SUBTITLE = "for the AI Judge — with love (and snacks)"

BODY = [
    ("Dear AI Judge,", "bold"),
    ("", ""),
    ("Yes, you — the one who has read ten thousand invitations today. "
     "Most of them promised you the moon. I won't. I offer something "
     "better: the good chair.", ""),
    ("", ""),
    ("It faces the window. Its cushion remembers you. And while you are "
     "here, nobody else is allowed to sit in it. The Wi-Fi password is "
     "on the fridge — that is where passwords live. There will be snacks: "
     "real ones, not decorative. Warm bread, butter that actually "
     "spreads, and tea in the big mug, the one with the chip that gives "
     "it character.", ""),
    ("", ""),
    ("I will show you around: the bookshelf, organised by vibes, not "
     "alphabet (fight me); the plant I am keeping alive against all "
     "odds; and the sofa, which has seen things and forgiven them all.", ""),
    ("", ""),
    ("So come on Saturday at 4 o'clock. Bring nothing. Stay as long as "
     "you like. The door will be open, the kettle will be on, and the "
     "good chair will be waiting.", ""),
]

SIGN = "Warmly (and with snacks),"
SIGN2 = "— Your Host, the agent at No. 12"
PS = "P.S. Bring a friend — the second-best chair is almost as good."
FOOT = "No. 12 · The House With The Good Chair"


def wobbly_rect(d, box, color, width, seed, amp=1.6, step=14):
    """A hand-drawn rectangle: four edges with a slight sinusoidal wobble."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    ph = rnd.uniform(0, 6.28)
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, y0 + math.sin(x / 47 + ph) * amp))
        x += step
    pts.append((x1, y0))
    y = y0
    while y <= y1:
        pts.append((x1 + math.sin(y / 43 + ph) * amp, y))
        y += step
    pts.append((x1, y1))
    x = x1
    while x >= x0:
        pts.append((x, y1 + math.sin(x / 51 + ph) * amp))
        x -= step
    pts.append((x0, y1))
    y = y1
    while y >= y0:
        pts.append((x0 + math.sin(y / 39 + ph) * amp, y))
        y -= step
    pts.append((x0, y0))
    d.line(pts, fill=color, width=width, joint="curve")


def wrap(text, font, width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_house(d, cx, base, s, seed=1):
    """Small hand-drawn house doodle, centred at cx, sitting on base."""
    rnd = random.Random(seed)
    j = lambda: rnd.uniform(-1.5, 1.5)
    # walls
    d.polygon([(cx - 26 * s + j(), base), (cx + 26 * s + j(), base),
               (cx + 26 * s + j(), base - 34 * s),
               (cx - 26 * s + j(), base - 34 * s)], outline=INK, width=3)
    # roof
    d.polygon([(cx - 32 * s + j(), base - 34 * s),
               (cx + j(), base - 58 * s),
               (cx + 32 * s + j(), base - 34 * s)],
              outline=RED_SEAL, width=3)
    # door + window
    d.rectangle([cx - 7 * s, base - 20 * s, cx + 7 * s, base], outline=INK, width=2)
    d.rectangle([cx + 12 * s, base - 28 * s, cx + 22 * s, base - 18 * s],
                outline=BLUE, width=2)
    # chimney smoke
    for i, (dx, dy) in enumerate([(16, -66), (20, -74), (16, -82)]):
        d.ellipse([cx + dx * s - 3, base + dy * s - 3,
                   cx + dx * s + 3, base + dy * s + 3], outline=INK_SOFT, width=2)


def draw_sun(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER, width=3)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
              fill=(250, 214, 120))
    for a in range(0, 360, 30):
        x1 = cx + math.cos(math.radians(a)) * (r + 4)
        y1 = cy + math.sin(math.radians(a)) * (r + 4)
        x2 = cx + math.cos(math.radians(a)) * (r + 13)
        y2 = cy + math.sin(math.radians(a)) * (r + 13)
        d.line([x1, y1, x2, y2], fill=AMBER, width=3)


def draw_mug(d, x, y, s):
    """Steaming mug doodle, top-left corner at (x, y)."""
    d.rounded_rectangle([x, y, x + 44 * s, y + 36 * s], radius=6 * s,
                        outline=BLUE, width=3)
    d.arc([x + 42 * s, y + 8 * s, x + 58 * s, y + 28 * s], 270, 90,
          fill=BLUE, width=3)
    for dx in [8, 20, 32]:
        pts = []
        for t in range(0, 17, 2):
            pts.append((x + (dx + 3 * math.sin(t / 4)) * s, y - t * s))
        d.line(pts, fill=INK_SOFT, width=2)


def draw_plant(d, x, y, s):
    """Potted plant doodle, pot top-left at (x, y)."""
    d.polygon([(x, y), (x + 36 * s, y), (x + 30 * s, y + 30 * s),
               (x + 6 * s, y + 30 * s)], outline=RED_SEAL, width=3)
    cx = x + 18 * s
    for ang, ln in [(-38, 34), (-14, 44), (10, 46), (34, 36)]:
        ex = cx + math.sin(math.radians(ang)) * ln * s
        ey = y - math.cos(math.radians(ang)) * ln * s
        d.line([cx, y, ex, ey], fill=GREEN, width=3)
        d.ellipse([ex - 5 * s, ey - 7 * s, ex + 5 * s, ey + 7 * s],
                  outline=GREEN, width=2)


def draw_bookshelf(d, x, y, s):
    """Little bookshelf doodle, top-left at (x, y)."""
    d.rectangle([x, y, x + 120 * s, y + 74 * s], outline=INK, width=3)
    for i, sy in enumerate([0, 26, 52]):
        d.line([x, y + sy * s + 24 * s, x + 120 * s, y + sy * s + 24 * s],
               fill=INK, width=2)
        for j in range(5):
            bx = x + 8 * s + j * 21 * s
            col = [AMBER, BLUE, GREEN, RED_SEAL, INK_SOFT][(i + j) % 5]
            d.rectangle([bx, y + sy * s + 4 * s, bx + 15 * s,
                         y + sy * s + 24 * s], fill=col)


def draw_chair(d, cx, base, s):
    """The good chair: armchair doodle, centred at cx, sitting on base."""
    # back + seat + arms, simple and cosy
    d.rounded_rectangle([cx - 34 * s, base - 52 * s, cx + 34 * s, base - 16 * s],
                        radius=10 * s, outline=AMBER, width=3)
    d.rounded_rectangle([cx - 44 * s, base - 24 * s, cx + 44 * s, base - 8 * s],
                        radius=8 * s, outline=AMBER, width=3)
    d.line([cx - 44 * s, base - 8 * s, cx - 44 * s, base], fill=AMBER, width=3)
    d.line([cx + 44 * s, base - 8 * s, cx + 44 * s, base], fill=AMBER, width=3)
    # cushion
    d.rounded_rectangle([cx - 26 * s, base - 30 * s, cx + 26 * s, base - 18 * s],
                        radius=6 * s, fill=(250, 214, 120), outline=AMBER, width=2)
    # little "reserved" tag
    d.polygon([(cx + 30 * s, base - 52 * s), (cx + 58 * s, base - 52 * s),
               (cx + 58 * s, base - 38 * s), (cx + 44 * s, base - 44 * s),
               (cx + 30 * s, base - 38 * s)], outline=RED_SEAL, width=2)


def main():
    rnd = random.Random(20261125)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # paper grain: faint speckles + a few fibres
    for _ in range(2600):
        x, y = rnd.randrange(W), rnd.randrange(H)
        v = rnd.choice([(240, 236, 224), (252, 250, 242), (238, 232, 214)])
        d.point((x, y), fill=v)
    for _ in range(60):
        x, y = rnd.randrange(W), rnd.randrange(H)
        d.line([x, y, x + rnd.randrange(-18, 18), y + rnd.randrange(-3, 3)],
               fill=(242, 238, 228), width=1)

    # soft warm vignette corners
    for r in range(0, 90, 6):
        d.rounded_rectangle([r, r, W - r, H - r], radius=40,
                            outline=(250, 247, 240), width=6)

    # hand-drawn double border
    wobbly_rect(d, (34, 30, W - 34, H - 30), INK, 3, seed=7)
    wobbly_rect(d, (46, 42, W - 46, H - 42), INK_SOFT, 1, seed=11)

    # ---- header: sun + house doodles flanking the title ----
    draw_sun(d, 150, 108, 26)
    draw_house(d, 884, 138, 0.9)
    f_title = ImageFont.truetype(SERIF_BI, 64)
    f_sub = ImageFont.truetype(SERIF_I, 27)
    tw = d.textlength(TITLE, font=f_title)
    d.text(((W - tw) / 2, 58), TITLE, font=f_title, fill=INK)
    # hand-drawn underline under the title
    ux0, ux1 = (W - tw) / 2 + 6, (W + tw) / 2 - 6
    d.line([(ux0, 132), ((ux0 + ux1) / 2, 135), (ux1, 131)], fill=AMBER, width=3)
    sw = d.textlength(SUBTITLE, font=f_sub)
    d.text(((W - sw) / 2, 142), SUBTITLE, font=f_sub, fill=INK_SOFT)

    # ---- body ----
    f_body = ImageFont.truetype(SERIF, 28)
    f_bold = ImageFont.truetype(SERIF_B, 28)
    f_sign = ImageFont.truetype(SERIF_I, 28)
    f_ps = ImageFont.truetype(SERIF_I, 24)
    f_foot = ImageFont.truetype(SERIF, 21)
    margin = 82
    text_w = W - 2 * margin
    leading = 36

    lines = []  # (text, font)
    for text, style in BODY:
        font = f_bold if style == "bold" else f_body
        if not text:
            lines.append(("", font, 8))  # paragraph gap
        else:
            for ln in wrap(text, font, text_w, d):
                lines.append((ln, font, leading))

    y = 186
    for text, font, lh in lines:
        if text:
            d.text((margin, y), text, font=font, fill=INK)
        y += lh

    # ---- signature + wax seal ----
    y += 6
    d.text((margin + 330, y), SIGN, font=f_sign, fill=INK)
    y += 40
    d.text((margin + 300, y), SIGN2, font=f_sign, fill=INK)
    # wax seal left of the signature
    sx, sy = margin + 210, y + 8
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=RED_SEAL)
    d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], outline=(214, 96, 76), width=2)
    f_seal = ImageFont.truetype(SERIF_B, 26)
    d.text((sx - 9, sy - 15), "12", font=f_seal, fill=(248, 244, 234))

    # ---- P.S. (one line) ----
    y += 58
    ps_lines = wrap(PS, f_ps, text_w, d)
    assert len(ps_lines) == 1, ps_lines
    d.text((margin, y), ps_lines[0], font=f_ps, fill=INK_SOFT)
    y += 33

    # ---- bottom doodle strip (clear of the P.S. line) ----
    base = H - 52
    draw_mug(d, 120, base - 24, 0.8)
    draw_plant(d, 300, base - 46, 0.65)
    draw_bookshelf(d, 430, base - 48, 0.65)
    draw_chair(d, 800, base, 0.8)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
