#!/usr/bin/env python3
"""Generate decking_layout_v11.3.png — Single-row picture-frame border, no center seam, 45° mitered corners."""

from PIL import Image, ImageDraw, ImageFont

# ── Config ──
SCALE = 28
W_FT, D_FT = 22, 12
MARGIN = {"top": 125, "bottom": 80, "left": 75, "right": 75}

W = int(W_FT * SCALE)
H = int(D_FT * SCALE)
CW = W + MARGIN["left"] + MARGIN["right"]
CH = H + MARGIN["top"] + MARGIN["bottom"]

# Colors
BG = "#faf8f6"
FRAME = "#4a4540"
FIELD = "#b8a89a"
BORDER = "#8b7d70"
TEXT = "#4a4540"
RIM = "#6b6560"
ACCENT = "#c17a5c"
SAGE = "#7a8b6e"

# Dimensions
RIM_THICK = 3.0
BORDER_DEPTH = 5.5    # single row = one 5/4×6 board
BOARD_W = 5.5
GAP = 0.125

def px(inches): return inches / 12.0 * SCALE

img = Image.new("RGB", (CW, CH), BG)
d = ImageDraw.Draw(img)

try:
    font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
    font_md = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    font_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    font_xl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
except:
    font_sm = font_md = font_lg = font_xl = ImageFont.load_default()

ox = MARGIN["left"]
oy = MARGIN["top"]

rim_px = px(RIM_THICK)
border_px = px(BORDER_DEPTH)
board_px = max(2, int(px(BOARD_W)))
gap_px = max(1, int(px(GAP)))

# ── Draw outer frame ──
d.rectangle([ox, oy, ox+W, oy+H], outline=FRAME, width=3)

# Inner bounds
inner_left = ox + int(rim_px)
inner_right = ox + W - int(rim_px)
inner_top = oy + int(rim_px)
inner_bottom = oy + H - int(rim_px)

# ── Draw field boards (left→right, continuous across full width) ──
field_left = inner_left
field_right = inner_right
field_top = inner_top + int(border_px)
field_bottom = inner_bottom - int(border_px)

y = field_top
while y + board_px <= field_bottom:
    d.rectangle([field_left, y, field_right, y+board_px], fill=FIELD, outline=FRAME, width=1)
    y += board_px + gap_px

# ── Draw border boards (perpendicular to the edge they border) ──
# Back border (runs front-to-back, perpendicular to back edge which runs left→right)
def draw_vborder(x1, x2, y1, y2):
    x = x1
    while x + board_px <= x2:
        d.rectangle([x, int(y1), x+board_px, int(y2)], fill=BORDER, outline=FRAME, width=1)
        x += board_px + gap_px

# Side borders (run left→right, perpendicular to side edge which runs front-to-back)
def draw_hborder(x1, x2, y1, y2):
    y = y1
    while y + board_px <= y2:
        d.rectangle([int(x1), y, int(x2), y+board_px], fill=BORDER, outline=FRAME, width=1)
        y += board_px + gap_px

# Back border (front-to-back, perpendicular to back edge)
draw_vborder(field_left, field_right, inner_top, inner_top + border_px)
# Front border (front-to-back, perpendicular to front edge)
draw_vborder(field_left, field_right, inner_bottom - border_px, inner_bottom)
# Left border (left→right, perpendicular to left edge)
draw_hborder(inner_left, inner_left + border_px, field_top, field_bottom)
# Right border (left→right, perpendicular to right edge)
draw_hborder(inner_right - border_px, inner_right, field_top, field_bottom)

# ── Draw 45° mitered corners (diagonal fill at each corner) ──
def draw_miter(cx, cy, direction, size=8):
    """Draw a small diagonal line showing 45° miter at corner.
    direction: 'tl', 'tr', 'bl', 'br' (which corner of the frame)"""
    s = size
    if direction == 'tl':  # top-left
        d.line([(cx, cy+s), (cx+s, cy)], fill=ACCENT, width=2)
        d.line([(cx+1, cy+s), (cx+s, cy+1)], fill=ACCENT, width=1)
    elif direction == 'tr':  # top-right
        d.line([(cx-s, cy), (cx, cy+s)], fill=ACCENT, width=2)
        d.line([(cx-s, cy+1), (cx-1, cy+s)], fill=ACCENT, width=1)
    elif direction == 'bl':  # bottom-left
        d.line([(cx, cy-s), (cx+s, cy)], fill=ACCENT, width=2)
        d.line([(cx+1, cy-s), (cx+s, cy-1)], fill=ACCENT, width=1)
    elif direction == 'br':  # bottom-right
        d.line([(cx-s, cy), (cx, cy-s)], fill=ACCENT, width=2)
        d.line([(cx-s, cy-1), (cx-1, cy-s)], fill=ACCENT, width=1)

# Mark 45° mitered corners
miter_size = 10
draw_miter(inner_left + int(border_px)//2, inner_top + int(border_px)//2, 'tl', miter_size)
draw_miter(inner_right - int(border_px)//2, inner_top + int(border_px)//2, 'tr', miter_size)
draw_miter(inner_left + int(border_px)//2, inner_bottom - int(border_px)//2, 'bl', miter_size)
draw_miter(inner_right - int(border_px)//2, inner_bottom - int(border_px)//2, 'br', miter_size)

# Corner labels
d.text((inner_left + 5, inner_top + 5), "45°", fill=ACCENT, font=font_sm)
d.text((inner_right - 25, inner_top + 5), "45°", fill=ACCENT, font=font_sm)
d.text((inner_left + 5, inner_bottom - 18), "45°", fill=ACCENT, font=font_sm)
d.text((inner_right - 25, inner_bottom - 18), "45°", fill=ACCENT, font=font_sm)

# ── Title ──
title = "Decking Layout — v11.3"
sub = "Picture-Frame Single Border  ·  45° Mitered Corners  ·  No Center Seam  ·  Field Boards Left→Right"
d.text((CW//2, 25), title, fill=TEXT, font=font_xl, anchor="mm")
d.text((CW//2, 52), sub, fill=RIM, font=font_md, anchor="mm")

# ── Dimension lines ──
def draw_dim_line(x1, y1, x2, y2, text, offset=(0, -18), font=font_md, color=TEXT):
    d.line([(x1, y1), (x2, y2)], fill=color, width=1)
    tick = 4
    if abs(y1-y2) < 2:
        d.line([(x1, y1-tick), (x1, y1+tick)], fill=color, width=1)
        d.line([(x2, y2-tick), (x2, y2+tick)], fill=color, width=1)
    else:
        d.line([(x1-tick, y1), (x1+tick, y1)], fill=color, width=1)
        d.line([(x2-tick, y2), (x2+tick, y2)], fill=color, width=1)
    tx = (x1+x2)//2 + offset[0]
    ty = (y1+y2)//2 + offset[1]
    bbox = d.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    d.rectangle([tx-tw//2-3, ty-th//2-1, tx+tw//2+3, ty+th//2+1], fill=BG, outline=None)
    d.text((tx-tw//2, ty-th//2), text, fill=color, font=font)

# Overall
draw_dim_line(ox, oy-25, ox+W, oy-25, '~22\' overall', offset=(0, -22), font=font_md)
draw_dim_line(ox+W+25, oy, ox+W+25, oy+H, '~12\' overall', offset=(8, 0), font=font_md)

# Border depth
draw_dim_line(ox-15, inner_top, ox-15, inner_top+int(border_px), '5.5" border', offset=(-40, 0), font=font_sm)

# ── Inner field callout ──
d.text((CW//2, CH - 50), "Inner field: ~20'10\" × ~10'6\"", fill=ACCENT, font=font_md, anchor="mm")

# ── Legend ──
legend_y = CH - 28
legend_items = [
    (FIELD, "Field Boards (left→right)"),
    (BORDER, "Border Boards (perpendicular)"),
    (ACCENT, "45° Mitered Corner"),
]
legend_x = ox + 20
for color, label in legend_items:
    d.rectangle([legend_x, legend_y, legend_x+16, legend_y+10], fill=color, outline=FRAME, width=1)
    d.text((legend_x+22, legend_y), label, fill=TEXT, font=font_sm)
    bbox = d.textbbox((0,0), label, font=font_sm)
    legend_x += 22 + (bbox[2]-bbox[0]) + 25

# ── Direction arrow ──
arrow_y = field_top + 25
arrow_x_start = field_left + 20
arrow_x_end = field_left + 75
d.line([(arrow_x_start, arrow_y), (arrow_x_end, arrow_y)], fill=SAGE, width=2)
d.polygon([(arrow_x_end, arrow_y-4), (arrow_x_end, arrow_y+4), (arrow_x_end+8, arrow_y)], fill=SAGE)
d.text((arrow_x_start+25, arrow_y-12), "Field →", fill=SAGE, font=font_sm)

img.save("decking_layout_v11.3.png", "PNG")
print("Saved decking_layout_v11.3.png  ({}×{})".format(CW, CH))
