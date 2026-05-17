#!/usr/bin/env python3
"""Generate joist_layout_v11.3.png — One simple continuous 22'×12' frame."""

from PIL import Image, ImageDraw, ImageFont

# ── Config ──
SCALE = 28          # pixels per foot
W_FT, D_FT = 22, 12 # frame dimensions
MARGIN = {"top": 110, "bottom": 75, "left": 75, "right": 75}

W = int(W_FT * SCALE)
H = int(D_FT * SCALE)
CW = W + MARGIN["left"] + MARGIN["right"]
CH = H + MARGIN["top"] + MARGIN["bottom"]

# Colors
BG = "#faf8f6"
FRAME = "#4a4540"
RIM = "#6b6560"
JOIST = "#8b7d70"
TEXT = "#4a4540"
SAGE = "#7a8b6e"

# Dimensions in inches
RIM_THICK = 3.0      # doubled 2×6 = 2×1.5"
JOIST_THICK = 1.5    # 2×6 actual
JOIST_OCC = 16.0

# Convert inches to pixels
def px(inches): return inches / 12.0 * SCALE

img = Image.new("RGB", (CW, CH), BG)
d = ImageDraw.Draw(img)

# Try to load a font
try:
    font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    font_md = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    font_xl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
except:
    font_sm = font_md = font_lg = font_xl = ImageFont.load_default()

ox = MARGIN["left"]
oy = MARGIN["top"]

# ── Draw outer frame ──
d.rectangle([ox, oy, ox+W, oy+H], outline=FRAME, width=3)

# ── Draw doubled rims ──
rim_px = px(RIM_THICK)
# Back rim (top)
d.rectangle([ox, oy, ox+W, oy+int(rim_px)], fill=RIM, outline=FRAME, width=1)
# Front rim (bottom)
d.rectangle([ox, oy+H-int(rim_px), ox+W, oy+H], fill=RIM, outline=FRAME, width=1)
# Left rim
d.rectangle([ox, oy, ox+int(rim_px), oy+H], fill=RIM, outline=FRAME, width=1)
# Right rim
d.rectangle([ox+W-int(rim_px), oy, ox+W, oy+H], fill=RIM, outline=FRAME, width=1)

# ── Draw joists (FRONT-TO-BACK, i.e. vertical bars in plan view) ──
joist_px = max(2, int(px(JOIST_THICK)))
inner_left = ox + int(rim_px)
inner_right = ox + W - int(rim_px)
inner_top = oy + int(rim_px)
inner_bottom = oy + H - int(rim_px)

joist_x_positions = []
num_joists = int((W_FT * 12 - 2 * RIM_THICK) / JOIST_OCC) + 1
for i in range(num_joists):
    x_off = i * px(JOIST_OCC)
    x = inner_left + int(x_off)
    if x + joist_px > inner_right:
        break
    joist_x_positions.append(x)
    d.rectangle([x, inner_top, x+joist_px, inner_bottom], fill=JOIST, outline=FRAME, width=1)

# Make sure there's a joist right before the right rim
if joist_x_positions and joist_x_positions[-1] + joist_px < inner_right - 5:
    x = inner_right - joist_px
    if x not in joist_x_positions:
        joist_x_positions.append(x)
        d.rectangle([x, inner_top, x+joist_px, inner_bottom], fill=JOIST, outline=FRAME, width=1)

# ── Dimension lines ──
def draw_dim_line(x1, y1, x2, y2, text, offset=(0, -18), font=font_md, color=TEXT):
    d.line([(x1, y1), (x2, y2)], fill=color, width=1)
    tick = 4
    if abs(y1 - y2) < 2:  # horizontal
        d.line([(x1, y1-tick), (x1, y1+tick)], fill=color, width=1)
        d.line([(x2, y2-tick), (x2, y2+tick)], fill=color, width=1)
    else:  # vertical
        d.line([(x1-tick, y1), (x1+tick, y1)], fill=color, width=1)
        d.line([(x2-tick, y2), (x2+tick, y2)], fill=color, width=1)
    tx = (x1+x2)//2 + offset[0]
    ty = (y1+y2)//2 + offset[1]
    bbox = d.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    d.rectangle([tx-tw//2-3, ty-th//2-1, tx+tw//2+3, ty+th//2+1], fill=BG, outline=None)
    d.text((tx-tw//2, ty-th//2), text, fill=color, font=font)

# Overall width at top
draw_dim_line(ox, oy-25, ox+W, oy-25, '~22\' overall', offset=(0, -22), font=font_md)
# Overall depth on right
draw_dim_line(ox+W+25, oy, ox+W+25, oy+H, '~12\' overall', offset=(8, 0), font=font_md)

# Rim thickness on left
draw_dim_line(ox-20, oy, ox-20, oy+int(rim_px), '3"', offset=(-30, 0), font=font_sm)

# Joist span (front-to-back) on left side — vertical dimension
draw_dim_line(ox-35, inner_top, ox-35, inner_bottom, '11\'6" joists', offset=(-55, 0), font=font_md)

# Joist spacing indicator (horizontal, showing across the 22' width)
if len(joist_x_positions) >= 2:
    x1 = joist_x_positions[0] + joist_px//2
    x2 = joist_x_positions[1] + joist_px//2
    draw_dim_line(x1, inner_bottom+10, x2, inner_bottom+10, '16" O.C.', offset=(-12, 10), font=font_sm)

# ── Title ──
title = "Joist Layout — v11.3"
sub = "One Simple Frame 22' × 12'  ·  Joists run Front-to-Back  ·  Doubled 2×6 Rims All Around"
d.text((CW//2, 25), title, fill=TEXT, font=font_xl, anchor="mm")
d.text((CW//2, 52), sub, fill=RIM, font=font_md, anchor="mm")

# ── Legend ──
legend_y = CH - 55
legend_items = [
    (RIM, "Doubled 2×6 Rim (3\" thick)"),
    (JOIST, "2×6 Field Joist (1.5\" × 11'6\")"),
]
legend_x = ox
for color, label in legend_items:
    d.rectangle([legend_x, legend_y, legend_x+18, legend_y+12], fill=color, outline=FRAME, width=1)
    d.text((legend_x+24, legend_y), label, fill=TEXT, font=font_sm)
    bbox = d.textbbox((0,0), label, font=font_sm)
    legend_x += 24 + (bbox[2]-bbox[0]) + 30

# ── Callout box ──
callout = "~{} joists at 16\" O.C. across 22' width  ·  No joist cuts needed".format(len(joist_x_positions))
d.text((CW//2, CH-28), callout, fill=SAGE, font=font_md, anchor="mm")

# ── Joist count label inside frame ──
count_text = f"{len(joist_x_positions)} joists"
bbox = d.textbbox((0,0), count_text, font=font_lg)
tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
d.text((CW//2, (inner_top+inner_bottom)//2 - 15), count_text, fill="#9a9590", font=font_lg, anchor="mm")
d.text((CW//2, (inner_top+inner_bottom)//2 + 12), "@ 16\" O.C.", fill="#9a9590", font=font_md, anchor="mm")

img.save("joist_layout_v11.3.png", "PNG")
print("Saved joist_layout_v11.3.png  ({}×{})".format(CW, CH))
