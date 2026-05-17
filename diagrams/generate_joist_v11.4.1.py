#!/usr/bin/env python3
"""Generate joist_layout_v11.4.1.png — Trex-style overhead framing with blocking shown."""

from PIL import Image, ImageDraw, ImageFont

# ── Config ──
SCALE = 26          # pixels per foot (slightly smaller to fit labels)
W_FT, D_FT = 22, 12
MARGIN = {"top": 140, "bottom": 90, "left": 110, "right": 110}

W = int(W_FT * SCALE)
H = int(D_FT * SCALE)
CW = W + MARGIN["left"] + MARGIN["right"]
CH = H + MARGIN["top"] + MARGIN["bottom"]

# Trex-style palette
BG = "#f5f2ed"
FRAME = "#2c2825"
RIM_FILL = "#c4b8a8"
RIM_LINE = "#8a7e72"
JOIST_FILL = "#a89e92"
JOIST_LINE = "#7a7268"
BLOCK_FILL = "#7a9aaa"   # Blue-ish for blocking (Trex style)
BLOCK_LINE = "#5a7a8a"
TEXT = "#2c2825"
DIM_COLOR = "#5a5548"
LABEL_BG = "#f5f2ed"

# Dimensions in inches
RIM_THICK = 3.0      # doubled 2×6
JOIST_THICK = 1.5    # 2×6 actual
JOIST_OCC = 16.0
BLOCK_THICK = 1.5    # 2×6 blocking

def px(inches): return inches / 12.0 * SCALE

img = Image.new("RGB", (CW, CH), BG)
d = ImageDraw.Draw(img)

try:
    font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
    font_md = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
    font_xl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    font_dim = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic.ttf", 12)
except:
    font_sm = font_md = font_lg = font_xl = font_dim = ImageFont.load_default()

ox = MARGIN["left"]
oy = MARGIN["top"]

# ── Draw outer frame boundary ──
d.rectangle([ox, oy, ox+W, oy+H], outline=FRAME, width=2)

# ── Draw doubled rims (thick, filled) ──
rim_px = px(RIM_THICK)
# Back rim (top)
d.rectangle([ox, oy, ox+W, oy+int(rim_px)], fill=RIM_FILL, outline=RIM_LINE, width=2)
# Front rim (bottom)
d.rectangle([ox, oy+H-int(rim_px), ox+W, oy+H], fill=RIM_FILL, outline=RIM_LINE, width=2)
# Left rim
d.rectangle([ox, oy, ox+int(rim_px), oy+H], fill=RIM_FILL, outline=RIM_LINE, width=2)
# Right rim
d.rectangle([ox+W-int(rim_px), oy, ox+W, oy+H], fill=RIM_FILL, outline=RIM_LINE, width=2)

# ── Calculate inner area ──
joist_px = max(2, int(px(JOIST_THICK)))
inner_left = ox + int(rim_px)
inner_right = ox + W - int(rim_px)
inner_top = oy + int(rim_px)
inner_bottom = oy + H - int(rim_px)
inner_width_px = inner_right - inner_left
inner_depth_px = inner_bottom - inner_top

# ── Draw joists FRONT-TO-BACK (vertical bars) ──
joist_x_positions = []
num_joists = int((W_FT * 12 - 2 * RIM_THICK) / JOIST_OCC) + 1
for i in range(num_joists):
    x_off = i * px(JOIST_OCC)
    x = inner_left + int(x_off)
    if x + joist_px > inner_right:
        break
    joist_x_positions.append(x)
    # Draw joist as filled rectangle with outline
    d.rectangle([x, inner_top, x+joist_px, inner_bottom], fill=JOIST_FILL, outline=JOIST_LINE, width=1)

# Ensure joist near right rim
if joist_x_positions and joist_x_positions[-1] + joist_px < inner_right - 5:
    x = inner_right - joist_px
    if x not in joist_x_positions:
        joist_x_positions.append(x)
        d.rectangle([x, inner_top, x+joist_px, inner_bottom], fill=JOIST_FILL, outline=JOIST_LINE, width=1)

# ── Draw BLOCKING (mid-span, horizontal, between joists) ──
# Blocking runs LEFT-TO-RIGHT (perpendicular to joists) at mid-span
block_y = inner_top + inner_depth_px // 2  # Mid-span
block_px = max(2, int(px(BLOCK_THICK)))

# Draw blocking as horizontal pieces between each pair of joists
for i in range(len(joist_x_positions) - 1):
    x1 = joist_x_positions[i] + joist_px
    x2 = joist_x_positions[i + 1]
    if x2 > x1 + 2:
        # Draw blocking piece
        d.rectangle([x1, block_y - block_px//2, x2, block_y + block_px//2], 
                    fill=BLOCK_FILL, outline=BLOCK_LINE, width=1)

# ── Dimension lines ──
def draw_dim_line(x1, y1, x2, y2, text, offset=(0, -15), font=font_md, color=DIM_COLOR):
    d.line([(x1, y1), (x2, y2)], fill=color, width=1)
    tick = 5
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
    d.rectangle([tx-tw//2-4, ty-th//2-2, tx+tw//2+4, ty+th//2+2], fill=LABEL_BG, outline=None)
    d.text((tx-tw//2, ty-th//2), text, fill=color, font=font)

# Overall width at top
draw_dim_line(ox, oy-35, ox+W, oy-35, "22' 0\" overall width", offset=(0, -18), font=font_md)
# Overall depth on right
draw_dim_line(ox+W+35, oy, ox+W+35, oy+H, "12' 0\" overall depth", offset=(10, 0), font=font_md)

# Rim thickness
draw_dim_line(ox-30, oy, ox-30, oy+int(rim_px), '3"', offset=(-35, 0), font=font_sm)

# Joist span (front-to-back) on left
draw_dim_line(ox-45, inner_top, ox-45, inner_bottom, "11' 6\" joist span", offset=(-65, 0), font=font_md)

# Blocking position label
bbox = d.textbbox((0,0), "Mid-span blocking", font=font_md)
tw = bbox[2]-bbox[0]
d.text((inner_left + inner_width_px//2 - tw//2, block_y - 25), "Mid-span blocking", fill=BLOCK_LINE, font=font_md)

# Joist spacing indicator
if len(joist_x_positions) >= 2:
    x1 = joist_x_positions[0] + joist_px//2
    x2 = joist_x_positions[1] + joist_px//2
    draw_dim_line(x1, inner_bottom+15, x2, inner_bottom+15, '16" O.C.', offset=(-10, 12), font=font_sm)

# ── BACK / FRONT labels ──
d.text((CW//2, oy-70), "BACK (house side)", fill=TEXT, font=font_lg, anchor="mm")
d.text((CW//2, oy+H+50), "FRONT (pool side)", fill=TEXT, font=font_lg, anchor="mm")
d.text((ox-80, oy+H//2), "LEFT", fill=TEXT, font=font_md, anchor="mm")
d.text((ox+W+80, oy+H//2), "RIGHT", fill=TEXT, font=font_md, anchor="mm")

# ── Title ──
title = "Framing Plan — v11.4.1"
sub = "22' × 12'  ·  Joists front-to-back  ·  Mid-span blocking at 5' 9\""
d.text((CW//2, 30), title, fill=TEXT, font=font_xl, anchor="mm")
d.text((CW//2, 58), sub, fill=DIM_COLOR, font=font_md, anchor="mm")

# ── Legend (Trex style, bottom) ──
legend_y = CH - 70
items = [
    (RIM_FILL, "Rim Joist (doubled 2×6, 3\" thick)"),
    (JOIST_FILL, "Field Joist (2×6, 11'6\", front-to-back)"),
    (BLOCK_FILL, "Blocking (2×6, mid-span, left-to-right)"),
]
legend_x = ox
for color, label in items:
    d.rectangle([legend_x, legend_y, legend_x+22, legend_y+14], fill=color, outline=FRAME, width=1)
    d.text((legend_x+28, legend_y), label, fill=TEXT, font=font_sm)
    bbox = d.textbbox((0,0), label, font=font_sm)
    legend_x += 28 + (bbox[2]-bbox[0]) + 35

# ── Callout ──
callout = "~{} joists at 16\" O.C.  ·  One row mid-span blocking  ·  Zero joist cuts".format(len(joist_x_positions))
bbox = d.textbbox((0,0), callout, font=font_md)
tw = bbox[2]-bbox[0]
d.text((CW//2, CH-35), callout, fill=DIM_COLOR, font=font_md, anchor="mm")

# ── Joist count inside frame ──
count_text = f"{len(joist_x_positions)} joists"
bbox = d.textbbox((0,0), count_text, font=font_lg)
tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
cy = inner_top + inner_depth_px//2
d.text((inner_left + inner_width_px//2 - tw//2, cy - 40), count_text, fill="#9a8e82", font=font_lg)
d.text((inner_left + inner_width_px//2 - 35, cy - 15), "@ 16\" O.C.", fill="#9a8e82", font=font_md)

img.save("joist_layout_v11.4.1.png", "PNG")
print(f"Saved joist_layout_v11.4.1.png — {len(joist_x_positions)} joists, {len(joist_x_positions)-1} blocking pieces")
