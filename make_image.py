#!/usr/bin/env python3
"""Draw entry.png: one picture summing up the world news of Thursday 19 November 2026.

Everything is drawn from scratch with PIL shapes and text -- no photos, no
copyrighted assets, no outlet logos. Run: python3 make_image.py
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (18, 16, 34)
PANEL = (32, 30, 58)
BORDER = (78, 72, 132)
ACCENT = (255, 196, 90)
TEXT = (243, 244, 250)
SUB = (196, 198, 224)
CYAN = (120, 205, 255)
GREEN = (130, 235, 165)
RED = (255, 120, 120)
PINK = (255, 150, 205)
VIOLET = (190, 160, 255)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def flag_us(draw, x, y, w=66, h=42):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(0, 0, 0))
    for i in range(0, 7, 2):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=(200, 40, 50))
    draw.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(40, 60, 160))


def flag_cn(draw, x, y, w=66, h=42):
    draw.rectangle([x, y, x + w, y + h], fill=(215, 40, 40), outline=(0, 0, 0))
    draw.ellipse([x + 8, y + 8, x + 23, y + 23], fill=(255, 220, 60))


def flag_ru(draw, x, y, w=66, h=42):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(50, 90, 200))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(215, 40, 40))


def leader(draw, cx, cy, suit):
    draw.ellipse([cx - 27, cy - 62, cx + 27, cy - 8], fill=(235, 200, 165))  # head
    draw.pieslice([cx - 54, cy - 6, cx + 54, cy + 84], 180, 360, fill=suit)    # shoulders
    draw.rectangle([cx - 54, cy + 32, cx + 54, cy + 68], fill=suit)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Header: the day, named big ----
    d.text((24, 20), "THURSDAY 19 NOVEMBER 2026", font=font(60), fill=TEXT)
    d.text((26, 94), "The day in one picture — world news", font=font(30, bold=False), fill=ACCENT)
    d.rectangle([24, 138, 1000, 144], fill=ACCENT)

    # ---- Main panel: first-ever US-China-Russia summit ----
    box = (24, 160, 1000, 470)
    d.rounded_rectangle(box, radius=14, fill=PANEL, outline=BORDER, width=3)
    d.text((44, 176), "SHENZHEN SUMMIT", font=font(38), fill=ACCENT)
    flag_us(d, 400, 232)
    flag_cn(d, 640, 232)
    flag_ru(d, 856, 232)
    leader(d, 432, 372, (60, 70, 90))
    leader(d, 672, 372, (90, 40, 40))
    leader(d, 888, 372, (40, 50, 80))
    d.rectangle([80, 428, 944, 456], fill=(120, 85, 50))  # table
    summit_lines = [
        "First-ever",
        "US–China–Russia",
        "summit. Peace",
        "declaration:",
        "\"Nuclear war must",
        "never be fought.\"",
    ]
    ty = 238
    for ln in summit_lines:
        d.text((44, ty), ln, font=font(27, bold=False), fill=TEXT)
        ty += 34

    # ---- Grid of six stories: 2 columns x 3 rows ----
    stories = [
        ("GTA VI LAUNCH", ["Biggest game launch ever", "~$1.8B on day one (est.)"], PINK, "pad"),
        ("ANTHROPIC IPO", ["Biggest IPO in history", "~$81B raised on day one"], GREEN, "bars"),
        ("ICJ VERDICT", ["UN court: Myanmar", "committed genocide,", "a first in 80 years"], VIOLET, "scales"),
        ("TRUMP ON IRAN", ["\"See what happens after Jan 1\"", "Strikes wait until 2027"], RED, "cal"),
        ("KERCH BRIDGE", ["Ukraine hits the Crimea bridge", "a third time in a week"], CYAN, "bridge"),
        ("GAZA", ["Israel pushes into central Gaza", "despite the ceasefire"], ACCENT, "pin"),
    ]
    gx = [24, 512]
    gy = [486, 660, 834]
    pw, ph = 488, 158
    for idx, (title, lines, color, icon) in enumerate(stories):
        x0, y0 = gx[idx % 2], gy[idx // 2]
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL, outline=BORDER, width=3)
        d.rectangle([x0, y0, x0 + 10, y1], fill=color)
        d.text((x0 + 26, y0 + 12), title, font=font(30), fill=color)
        ty = y0 + 54
        for ln in lines:
            for part in wrap(d, ln, font(24, bold=False), 300):
                d.text((x0 + 26, ty), part, font=font(24, bold=False), fill=TEXT)
                ty += 31
        ix, iy = x1 - 118, y0 + 34
        if icon == "pad":  # gamepad
            d.rounded_rectangle([ix - 6, iy + 36, ix + 96, iy + 92], radius=26, outline=TEXT, width=5)
            d.ellipse([ix + 56, iy + 50, ix + 70, iy + 64], fill=PINK)
            d.ellipse([ix + 72, iy + 64, ix + 86, iy + 78], fill=PINK)
            d.line([ix + 14, iy + 64, ix + 40, iy + 64], fill=TEXT, width=6)
            d.line([ix + 27, iy + 51, ix + 27, iy + 77], fill=TEXT, width=6)
        elif icon == "bars":  # rising bars
            for j, bh in enumerate([28, 46, 68, 92]):
                d.rectangle([ix + j * 22, iy + 100 - bh, ix + j * 22 + 15, iy + 100], fill=GREEN)
            d.line([ix - 4, iy + 82, ix + 88, iy + 4], fill=TEXT, width=5)
        elif icon == "scales":  # scales of justice
            d.line([ix + 44, iy + 8, ix + 44, iy + 84], fill=TEXT, width=6)
            d.line([ix + 4, iy + 20, ix + 84, iy + 20], fill=TEXT, width=6)
            d.line([ix + 4, iy + 20, ix + 4, iy + 48], fill=TEXT, width=4)
            d.line([ix + 84, iy + 20, ix + 84, iy + 48], fill=TEXT, width=4)
            d.arc([ix - 12, iy + 34, ix + 20, iy + 66], 0, 180, fill=VIOLET, width=6)
            d.arc([ix + 68, iy + 34, ix + 100, iy + 66], 0, 180, fill=VIOLET, width=6)
            d.line([ix + 28, iy + 96, ix + 60, iy + 96], fill=TEXT, width=6)
        elif icon == "cal":  # calendar
            d.rounded_rectangle([ix, iy + 10, ix + 88, iy + 96], radius=8, outline=TEXT, width=5)
            d.rectangle([ix, iy + 10, ix + 88, iy + 36], fill=RED)
            d.text((ix + 11, iy + 46), "2027", font=font(30), fill=TEXT)
        elif icon == "bridge":  # bridge over water
            d.line([ix - 8, iy + 58, ix + 100, iy + 58], fill=TEXT, width=7)
            d.line([ix + 16, iy + 58, ix + 16, iy + 88], fill=TEXT, width=6)
            d.line([ix + 76, iy + 58, ix + 76, iy + 88], fill=TEXT, width=6)
            d.arc([ix + 16, iy + 34, ix + 76, iy + 86], 180, 360, fill=CYAN, width=5)
            for k in range(3):
                d.line([ix - 4 + k * 36, iy + 100, ix + 20 + k * 36, iy + 100], fill=CYAN, width=5)
        else:  # map pin
            d.ellipse([ix + 22, iy + 4, ix + 74, iy + 56], fill=ACCENT)
            d.polygon([(ix + 30, iy + 44), (ix + 66, iy + 44), (ix + 48, iy + 92)], fill=ACCENT)
            d.ellipse([ix + 38, iy + 20, ix + 58, iy + 40], fill=PANEL)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
