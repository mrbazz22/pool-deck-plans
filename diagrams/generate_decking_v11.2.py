#!/usr/bin/env python3
"""Generate decking_layout_v11.2.png — Picture-frame borders creating two visual sections."""

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
SEAM = "#e8e2db"
TEXT = "#4a4540"
RIM = "#6b6560"
ACCENT = "#c17a5c"
SAGE = "#7a8b6e"

# Dimensions
RIM_THICK = 3.0
BORDER_DEPTH = 11.0
SEAM_WIDTH = 6.0
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
seam_px = px(SEAM_WIDTH)
board_px = max(2, int(px(BOARD_W)))
gap_px = max(1, int(px(GAP)))

# ── Draw outer frame ──
d.rectangle([ox, oy, ox+W, oy+H], outline=FRAME, width=3)

# Inner bounds
inner_left = ox + int(rim_px)
inner_right = ox + W - int(rim_px)
inner_top = oy + int(rim_px)
inner_bottom = oy + H - int(rim_px)

# Center seam
seam_left = ox + (W - int(seam_px)) // 2
seam_right = seam_left + int(seam_px)

# Draw seam gap
d.rectangle([seam_left, inner_top, seam_right, inner_bottom], fill=SEAM, outline=ACCENT, width=2)

# Section bounds
secA_left = inner_left
secA_right = seam_left
secB_left = seam_right
secB_right = inner_right

# ── Helper: draw border board strips ──
def vstrip(x1, x2, y1, y2, fill=BORDER):
    d.rectangle([int(x1), int(y1), int(x2), int(y2)], fill=fill, outline=FRAME, width=1)

def hstrip(x1, x2, y1, y2, fill=BORDER):
    d.rectangle([int(x1), int(y1), int(x2), int(y2)], fill=fill, outline=FRAME, width=1)

# ── Section A borders (outer + seam sides) ──
vstrip(secA_left, secA_left+border_px, inner_top, inner_bottom)          # left outer
vstrip(secA_right-border_px, secA_right, inner_top, inner_bottom)        # right at seam
hstrip(secA_left+border_px, secA_right-border_px, inner_top, inner_top+border_px)      # back
hstrip(secA_left+border_px, secA_right-border_px, inner_bottom-border_px, inner_bottom)  # front

# ── Section B borders (seam + outer sides) ──
vstrip(secB_left, secB_left+border_px, inner_top, inner_bottom)        # left at seam
vstrip(secB_right-border_px, secB_right, inner_top, inner_bottom)      # right outer
hstrip(secB_left+border_px, secB_right-border_px, inner_top, inner_top+border_px)       # back
hstrip(secB_left+border_px, secB_right-border_px, inner_bottom-border_px, inner_bottom)  # front

# ── Section A field ──
fieldA_left = secA_left + int(border_px)
fieldA_right = secA_right - int(border_px)
fieldA_top = inner_top + int(border_px)
fieldA_bottom = inner_bottom - int(border_px)

# Draw field board rows (left→right)
y = fieldA_top
while y + board_px <= fieldA_bottom:
    d.rectangle([fieldA_left, y, fieldA_right, y+board_px], fill=FIELD, outline=FRAME, width=1)
    y += board_px + gap_px

# ── Section B field ──
fieldB_left = secB_left + int(border_px)
fieldB_right = secB_right - int(border_px)
y = inner_top + int(border_px)
while y + board_px <= inner_bottom - int(border_px):
    d.rectangle([fieldB_left, y, fieldB_right, y+board_px], fill=FIELD, outline=FRAME, width=1)
    y += board_px + gap_px

# ── Draw individual border board detail ──
def draw_vborder_boards(x_start, x_end, y_start, y_end):
    y = y_start
    while y + board_px <= y_end:
        d.rectangle([int(x_start), int(y), int(x_end), int(y+board_px)], fill=BORDER, outline=FRAME, width=1)
        y += board_px + gap_px

def draw_hborder_boards(x_start, x_end, y_start, y_end):
    x = x_start
    while x + board_px <= x_end:
        d.rectangle([int(x), int(y_start), int(x+board_px), int(y_end)], fill=BORDER, outline=FRAME, width=1)
        x += board_px + gap_px

# Section A left outer double border (boards front-to-back)
draw_vborder_boards(secA_left, secA_left+board_px, inner_top, inner_bottom)
draw_vborder_boards(secA_left+board_px+gap_px, secA_left+2*board_px+gap_px, inner_top, inner_bottom)

# Section A right border at seam (boards front-to-back)
draw_vborder_boards(secA_right-2*board_px-gap_px, secA_right-board_px-gap_px, inner_top, inner_bottom)
draw_vborder_boards(secA_right-board_px, secA_right, inner_top, inner_bottom)

# Section B left border at seam
draw_vborder_boards(secB_left, secB_left+board_px, inner_top, inner_bottom)
draw_vborder_boards(secB_left+board_px+gap_px, secB_left+2*board_px+gap_px, inner_top, inner_bottom)

# Section B right outer border
draw_vborder_boards(secB_right-2*board_px-gap_px, secB_right-board_px-gap_px, inner_top, inner_bottom)
draw_vborder_boards(secB_right-board_px, secB_right, inner_top, inner_bottom)

# Back borders (boards left-to-right)
draw_hborder_boards(secA_left+border_px, secA_right-border_px, inner_top, inner_top+board_px)
draw_hborder_boards(secA_left+border_px, secA_right-border_px, inner_top+board_px+gap_px, inner_top+2*board_px+gap_px)
draw_hborder_boards(secB_left+border_px, secB_right-border_px, inner_top, inner_top+board_px)
draw_hborder_boards(secB_left+border_px, secB_right-border_px, inner_top+board_px+gap_px, inner_top+2*board_px+gap_px)

# Front borders
front_y1 = inner_bottom - 2*board_px - gap_px
front_y2 = inner_bottom - board_px - gap_px
front_y3 = inner_bottom - board_px
front_y4 = inner_bottom
draw_hborder_boards(secA_left+border_px, secA_right-border_px, front_y1, front_y2)
draw_hborder_boards(secA_left+border_px, secA_right-border_px, front_y3, front_y4)
draw_hborder_boards(secB_left+border_px, secB_right-border_px, front_y1, front_y2)
draw_hborder_boards(secB_left+border_px, secB_right-border_px, front_y3, front_y4)

# ── Center seam boards (perpendicular, front-to-back) ──
seam_y = inner_top
while seam_y + board_px <= inner_bottom:
    d.rectangle([seam_left, seam_y, seam_right, seam_y+board_px], fill=BORDER, outline=ACCENT, width=1)
    seam_y += board_px + gap_px

# ── Title ──
title = "Decking Layout — v11.2"
sub = "Picture-Frame Double Borders  ·  Two Visual Sections  ·  6\" Center Seam  ·  Field Boards Left→Right"
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

# Seam width
draw_dim_line(seam_left, oy+H+15, seam_right, oy+H+15, '6" seam', offset=(0, 12), font=font_sm)

# Border depth
draw_dim_line(ox-15, inner_top, ox-15, inner_top+int(border_px), '11" border', offset=(-40, 0), font=font_sm)

# ── Section labels ──
d.text(((secA_left+secA_right)//2, (inner_top+inner_bottom)//2 - 15), "Section A", fill="#9a9590", font=font_lg, anchor="mm")
d.text(((secA_left+secA_right)//2, (inner_top+inner_bottom)//2 + 15), "(Visual)", fill="#b0a8a0", font=font_md, anchor="mm")
d.text(((secB_left+secB_right)//2, (inner_top+inner_bottom)//2 - 15), "Section B", fill="#9a9590", font=font_lg, anchor="mm")
d.text(((secB_left+secB_right)//2, (inner_top+inner_bottom)//2 + 15), "(Visual)", fill="#b0a8a0", font=font_md, anchor="mm")

# ── Inner field callout ──
d.text((CW//2, CH - 50), "Inner field per section: ~9\u20322\" × ~10\u20326\"", fill=ACCENT, font=font_md, anchor="mm")

# ── Legend ──
legend_y = CH - 28
legend_items = [
    (FIELD, "Field Boards (left→right)"),
    (BORDER, "Border Boards (perpendicular)"),
    (SEAM, "6\" Center Seam"),
]
legend_x = ox + 20
for color, label in legend_items:
    d.rectangle([legend_x, legend_y, legend_x+16, legend_y+10], fill=color, outline=FRAME, width=1)
    d.text((legend_x+22, legend_y), label, fill=TEXT, font=font_sm)
    bbox = d.textbbox((0,0), label, font=font_sm)
    legend_x += 22 + (bbox[2]-bbox[0]) + 25

# ── Direction arrow ──
arrow_y = fieldA_top + 25
arrow_x_start = fieldA_left + 20
arrow_x_end = fieldA_left + 75
d.line([(arrow_x_start, arrow_y), (arrow_x_end, arrow_y)], fill=SAGE, width=2)
d.polygon([(arrow_x_end, arrow_y-4), (arrow_x_end, arrow_y+4), (arrow_x_end+8, arrow_y)], fill=SAGE)
d.text((arrow_x_start+25, arrow_y-12), "Field →", fill=SAGE, font=font_sm)

img.save("decking_layout_v11.2.png", "PNG")
print("Saved decking_layout_v11.2.png  ({}×{})".format(CW, CH))
