#!/usr/bin/env python3
"""Generate the B2B - Bukhara to Beijing menu as a lightweight vector PDF."""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ---------- palette ----------
BG       = HexColor("#15181f")
BG2      = HexColor("#1b2027")
PANEL    = HexColor("#262b36")
PANEL2   = HexColor("#191d25")
GOLD     = HexColor("#e6c179")
GOLD_HI  = HexColor("#f6e2ab")
GOLD_DP  = HexColor("#c99a45")
ORANGE   = HexColor("#d9772e")
EMBER    = HexColor("#e85d2a")
TEXT     = HexColor("#e9e2d4")
MUTED    = HexColor("#b7ac95")
LEADER   = HexColor("#6e6650")

TITLE_F = "Times-Bold"
BODY_F  = "Helvetica"
BODY_B  = "Helvetica-Bold"
BODY_I  = "Helvetica-Oblique"

# ---------- menu data ----------
COL1 = [
    ("Beverages", [
        ("Lassi (Sweet / Salt / Mango)", "79"),
        ("Lemon Mint", "79"),
        ("Mint Masala", "79"),
        ("Classic Lemon Soda", "79"),
        ("Boondi Raita", "30"),
        ("Mix Veg", "50"),
    ]),
    ("Noodles", [
        ("Veg Hakka Noodles", "149"),
        ("Veg Chilli Garlic Noodles", "169"),
        ("Chicken Hakka Noodles", "229"),
        ("Chicken Chilli Garlic Noodles", "239"),
        ("Egg Noodles", "169"),
    ]),
    ("Rice & Biryani", [
        ("Steamed Rice", "79"),
        ("Jeera Rice", "89"),
        ("Peas Pulao", "99"),
        ("Veg Fried Rice", "139"),
        ("Egg Fried Rice", "149"),
        ("Chicken Fried Rice", "199"),
        ("Veg Biryani", "229"),
        ("Egg Biryani", "229"),
        ("Chicken Biryani", "199/299"),
    ], "Complimentary raita with rice & biryani"),
    ("Tandoori Veg", [
        ("Paneer Tikka", "279"),
        ("Paneer Masala Tikka", "279"),
        ("Paneer Malai Tikka", "279"),
        ("Soya Chaap", "249"),
        ("Malai Chaap", "249"),
        ("Dahi Kebab", "249"),
        ("Hara Bhara Kebab", "249"),
    ]),
    ("Desserts", [
        ("Gulab Jamun", "79"),
        ("Rabri Falooda", "129"),
        ("Kulfi Falooda", "129"),
        ("Kulfi Pista", "99"),
    ]),
]

COL3 = [
    ("Snacks", [
        ("Chole Bhature", "99"),
        ("Chole Kulche", "99"),
        ("Pav Bhaji", "99"),
    ]),
    ("Chinese Starters", [
        ("Chilli Potato / Honey Chilli Potato", "139/149"),
        ("Veg Spring Roll", "129"),
        ("Cheese Cigar Roll", "149"),
        ("Chilli Paneer Dry / Gravy", "249/259"),
        ("Veg Manchurian Dry / Gravy", "139/149"),
        ("Chilli Mushroom", "149"),
        ("Chilli Chicken Dry / Gravy", "249/269"),
    ]),
    ("Indian Breads", [
        ("Plain Roti", "15"), ("Rumali Roti", "15"), ("Butter Roti", "20"),
        ("Laccha Paratha", "40"), ("Pudina Paratha", "50"), ("Missi Paratha", "60"),
        ("Plain Naan", "40"), ("Butter Naan", "55"), ("Garlic Naan", "60"),
        ("Aloo Kulcha", "79"), ("Onion Kulcha", "79"), ("Paneer Kulcha", "99"),
        ("Mixed Kulcha", "99"),
    ]),
    ("Tandoori Non Veg", [
        ("Chicken Tikka", "299"),
        ("Chicken Malai Tikka", "299"),
        ("Tandoori Chicken Half", "199"),
        ("Tandoori Chicken Full", "369"),
        ("Chicken Sheekh Kebab", "299"),
        ("Tangri Kebab Half", "199"),
        ("Tangri Kebab", "349"),
    ]),
]

# Column 2 built separately (has the two-price main-course tables)
MC_VEG = [
    ("Paneer Makhani", "150", "249"),
    ("Paneer Lababdar", "150", "249"),
    ("Kadai Paneer", "150", "249"),
    ("Paneer Kolhapuri", "150", "249"),
    ("Matar Paneer", "150", "249"),
    ("Special Dal Makhani", "150", "229"),
    ("Yellow Dal Tadka", None, "199"),
    ("Assorted Veg", None, "229"),
    ("Aloo Gobhi Adraki", None, "149"),
    ("Chana Masala", None, "199"),
]
MC_NONVEG = [
    ("Home Style Chicken Curry", "299"),
    ("Chicken Lababdar", "299"),
    ("Kadai Chicken", "299"),
    ("Butter Chicken", "349"),
]
PARATHA = [
    ("Aloo Paratha", "79"), ("Onion Paratha", "79"), ("Paneer Paratha", "99"),
    ("Mixed Paratha", "89"), ("Egg Paratha", "89"), ("Keema Paratha", "119"),
]
ROLLS = [
    ("Soya Roll", "129"), ("Soya Malai Roll", "149"), ("Soya Masala Roll", "149"),
    ("Paneer Roll", "149"), ("Paneer Malai Roll", "149"), ("Paneer Peri Peri Roll", "149"),
    ("Egg Roll", "119"), ("Egg Masala Roll", "129"), ("Egg Malai Roll", "139"),
    ("Chicken Sheekh Roll", "199"), ("Chicken Malai Roll", "199"),
    ("Double Egg Roll", "199"), ("Double Chicken Roll", "199"),
]
COMBOS = [
    ("Chinese Veg Combo (Spring Roll, Hakka Noodles, Chilli Paneer)", "349"),
    ("Chinese Veg Combo (Spring Roll, Fr. Rice, Veg Manchurian)", "329"),
    ("Chinese Non Veg Combo (Spring Roll, Chicken Fried Rice, Chicken Manchurian)", "399"),
    ("Chinese Nonveg Combo (Spring Roll, Chicken Noodles, Chilli Chicken Gravy)", "399"),
    ("Indian Veg Combo (Paneer Tikka, Dal Makhani, Sahi Paneer, Steam Rice, Roti)", "449"),
    ("Indian Non Veg Combo (Chicken Tikka, Butter Chicken, Lababdar, Jeera Rice, Butter Naan)", "499"),
]

# ---------- geometry ----------
W, H = 792, 1040
M = 30
CX0 = M + 8
CW = W - 2 * (M + 8)
GAP = 16
COLW = (CW - 2 * GAP) / 3.0
COLX = [CX0, CX0 + COLW + GAP, CX0 + 2 * (COLW + GAP)]

LINE_H = 12.6
PILL_H = 17
SEC_GAP = 9
ITEM_FS = 8.6
NAME_FS = 8.6

c = canvas.Canvas("menu/B2B_Menu.pdf", pagesize=(W, H))
c.setTitle("B2B - Bukhara to Beijing | Menu")


def diamond(cx, cy, r, color=GOLD):
    p = c.beginPath()
    p.moveTo(cx, cy + r); p.lineTo(cx + r, cy); p.lineTo(cx, cy - r); p.lineTo(cx - r, cy)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)


def dotted(x1, x2, y):
    if x2 - x1 < 4:
        return
    c.setStrokeColor(LEADER)
    c.setLineWidth(0.6)
    c.setDash([0.6, 2.2])
    c.line(x1, y, x2, y)
    c.setDash([])


def sec_header(x, y, w, title):
    """Draw a section pill; y = top. Returns new top y."""
    c.setFillColor(PANEL); c.setStrokeColor(GOLD_DP); c.setLineWidth(0.9)
    c.roundRect(x, y - PILL_H, w, PILL_H, 3.5, fill=1, stroke=1)
    t = title.upper()
    c.setFont(TITLE_F, 9.6)
    tw = c.stringWidth(t, TITLE_F, 9.6)
    cx = x + w / 2.0
    baseline = y - PILL_H + 5.4
    c.setFillColor(GOLD)
    c.drawString(cx - tw / 2.0 + 6, baseline, t)
    diamond(cx - tw / 2.0 - 5, y - PILL_H / 2.0, 3.0, GOLD)
    return y - PILL_H - 7


def item_row(x, y, w, name, price):
    c.setFont(BODY_F, NAME_FS); c.setFillColor(TEXT)
    c.drawString(x, y, name)
    nw = c.stringWidth(name, BODY_F, NAME_FS)
    c.setFont(BODY_B, ITEM_FS); c.setFillColor(GOLD)
    pw = c.stringWidth(price, BODY_B, ITEM_FS)
    c.drawRightString(x + w, y, price)
    dotted(x + nw + 3, x + w - pw - 3, y + 1.6)


def draw_simple_section(x, y, w, sec):
    title, items = sec[0], sec[1]
    note = sec[2] if len(sec) > 2 else None
    y = sec_header(x, y, w, title)
    if note:
        c.setFont(BODY_I, 7.4); c.setFillColor(MUTED)
        c.drawString(x, y - 8, note)
        y -= 11
    for name, price in items:
        y -= 9  # move to baseline of this line
        item_row(x, y, w, name, price)
        y -= (LINE_H - 9)
    return y - SEC_GAP


# ================= background =================
c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(BG2); c.rect(0, H * 0.62, W, H * 0.38, fill=1, stroke=0)
c.setFillColor(BG); c.rect(0, 0, W, H * 0.62, fill=1, stroke=0)
# outer gold frame
c.setStrokeColor(GOLD_DP); c.setLineWidth(1.6)
c.roundRect(M - 8, M - 8, W - 2 * (M - 8), H - 2 * (M - 8), 8, fill=0, stroke=1)
c.setStrokeColor(HexColor("#3a3428")); c.setLineWidth(0.8)
c.roundRect(M - 3, M - 3, W - 2 * (M - 3), H - 2 * (M - 3), 6, fill=0, stroke=1)

# corner ticks
def corner(cx, cy, dx, dy):
    c.setStrokeColor(GOLD_DP); c.setLineWidth(1.6)
    c.line(cx, cy, cx + dx, cy); c.line(cx, cy, cx, cy + dy)
corner(M + 2, H - M - 2, 22, -22)
corner(W - M - 2, H - M - 2, -22, -22)
corner(M + 2, M + 2, 22, 22)
corner(W - M - 2, M + 2, -22, 22)

# ================= header =================
def lantern(cx, top):
    c.setStrokeColor(GOLD_DP); c.setLineWidth(1)
    c.line(cx, top, cx, top - 8)
    c.setFillColor(GOLD_DP); c.circle(cx, top - 10, 3, fill=1, stroke=0)
    c.setFillColor(EMBER); c.setStrokeColor(HexColor("#7a1f10")); c.setLineWidth(1)
    c.ellipse(cx - 11, top - 34, cx + 11, top - 12, fill=1, stroke=1)
    c.setStrokeColor(HexColor("#b83f18")); c.setLineWidth(0.7)
    c.line(cx - 6, top - 13, cx - 6, top - 33)
    c.line(cx + 6, top - 13, cx + 6, top - 33)
    c.setFillColor(GOLD_DP); c.circle(cx, top - 35, 3, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(cx, top - 38, cx, top - 46)
    c.setFillColor(GOLD); c.rect(cx - 2, top - 52, 4, 6, fill=1, stroke=0)

top = H - M - 18
lantern(M + 60, top + 6)
lantern(W - M - 60, top + 6)

c.setFillColor(GOLD_HI); c.setFont(TITLE_F, 50)
c.drawCentredString(W / 2.0, H - M - 60, "B2B")
c.setFillColor(GOLD); c.setFont(TITLE_F, 21)
c.drawCentredString(W / 2.0, H - M - 84, "B U K H A R A   T O   B E I J I N G")
c.setFillColor(MUTED); c.setFont(BODY_F, 8.6)
c.drawCentredString(W / 2.0, H - M - 98, "M U L T I - C U I S I N E   R E S T A U R A N T")
c.setFillColor(GOLD_DP); c.setFont(BODY_F, 8.2)
c.drawCentredString(W / 2.0, H - M - 111, "Contact:  +91 98765 43210")
# divider
c.setStrokeColor(GOLD_DP); c.setLineWidth(0.8)
c.line(W / 2.0 - 150, H - M - 120, W / 2.0 + 150, H - M - 120)
diamond(W / 2.0, H - M - 120, 2.6, GOLD)

# ================= columns =================
y_top = H - M - 138
ends = []

# Column 1
y = y_top
for sec in COL1:
    y = draw_simple_section(COLX[0], y, COLW, sec)
ends.append(y)

# Column 3
y = y_top
for sec in COL3:
    y = draw_simple_section(COLX[2], y, COLW, sec)
ends.append(y)

# Column 2 (with main-course tables)
x = COLX[1]; y = y_top
y = draw_simple_section(x, y, COLW, ("Paratha", PARATHA))
y = draw_simple_section(x, y, COLW, ("Rolls", ROLLS))

# --- Indian Main Course (Veg) two-price table ---
y = sec_header(x, y, COLW, "Indian Main Course (Veg)")
p1c = x + COLW - 58   # 300 ml column center
p2c = x + COLW - 18   # 500 ml column center
c.setFont(BODY_F, 6.8); c.setFillColor(GOLD_DP)
c.drawCentredString(p1c, y - 7, "300 ML"); c.drawCentredString(p2c, y - 7, "500 ML")
y -= 12
for name, a, b in MC_VEG:
    y -= 9
    c.setFont(BODY_F, NAME_FS); c.setFillColor(TEXT)
    c.drawString(x, y, name)
    c.setFont(BODY_B, ITEM_FS)
    if a:
        c.setFillColor(GOLD); c.drawCentredString(p1c, y, a)
    else:
        c.setFillColor(MUTED); c.setFont(BODY_F, ITEM_FS); c.drawCentredString(p1c, y, "\u2014")
    c.setFont(BODY_B, ITEM_FS); c.setFillColor(GOLD); c.drawCentredString(p2c, y, b)
    y -= (LINE_H - 9)
y -= SEC_GAP

# --- Indian Main Course (Non Veg) ---
y = sec_header(x, y, COLW, "Indian Main Course (Non Veg)")
for name, price in MC_NONVEG:
    y -= 9
    item_row(x, y, COLW, name, price)
    y -= (LINE_H - 9)
y -= SEC_GAP
ends.append(y)

# ================= combos box =================
combos_top = min(ends) - 6
bx, bw = CX0, CW
rows_h = len(COMBOS) * 13.4
box_h = PILL_H + 10 + rows_h + 12
c.setFillColor(PANEL2); c.setStrokeColor(GOLD_DP); c.setLineWidth(1.1)
c.roundRect(bx, combos_top - box_h, bw, box_h, 6, fill=1, stroke=1)
# header pill (centered, narrow)
pill_w = 150
sec_header(bx + (bw - pill_w) / 2.0, combos_top - 6, pill_w, "Combos")
c.setFont(BODY_F, 7.6); c.setFillColor(GOLD_DP)
c.drawRightString(bx + bw - 12, combos_top - 6 - 12, "Serves 2 / 3")
yy = combos_top - 6 - PILL_H - 12
for name, price in COMBOS:
    c.setFont(BODY_F, 8.7); c.setFillColor(TEXT)
    c.drawString(bx + 16, yy, name)
    nw = c.stringWidth(name, BODY_F, 8.7)
    c.setFont(BODY_B, 8.7); c.setFillColor(GOLD)
    pw = c.stringWidth(price, BODY_B, 8.7)
    c.drawRightString(bx + bw - 16, yy, price)
    dotted(bx + 16 + nw + 4, bx + bw - 16 - pw - 4, yy + 1.6)
    yy -= 13.4

# ================= footer skyline =================
sky_y = M + 40
c.setStrokeColor(ORANGE); c.setLineWidth(1.2)
# Taj (left)
tx = W * 0.24
c.arc(tx - 22, sky_y + 8, tx + 22, sky_y + 52, 0, 180)
c.line(tx - 22, sky_y, tx - 22, sky_y + 30)
c.line(tx + 22, sky_y, tx + 22, sky_y + 30)
c.line(tx, sky_y + 52, tx, sky_y + 60)
for mx in (tx - 40, tx + 40):
    c.line(mx, sky_y, mx, sky_y + 34)
    c.arc(mx - 4, sky_y + 34, mx + 4, sky_y + 42, 0, 180)
# Pagoda (right)
px = W * 0.76
for i, (halfw, yb) in enumerate([(30, sky_y), (24, sky_y + 16), (17, sky_y + 30)]):
    c.line(px - halfw, yb, px + halfw, yb)
    c.line(px - halfw, yb, px - halfw + 6, yb + 10)
    c.line(px + halfw, yb, px + halfw - 6, yb + 10)
c.line(px, sky_y + 40, px, sky_y + 48)
c.line(px - 26, sky_y, px - 26, sky_y + 30)
c.line(px + 26, sky_y, px + 26, sky_y + 30)
# base line
c.setStrokeColor(GOLD_DP); c.setLineWidth(0.7)
c.line(M + 20, sky_y, W - M - 20, sky_y)

c.setFillColor(GOLD); c.setFont(TITLE_F, 12)
c.drawCentredString(W / 2.0, M + 20, "BUKHARA 2 BEIJING")
c.setFillColor(MUTED); c.setFont(BODY_F, 7.6)
c.drawCentredString(W / 2.0, M + 8, "NORTH INDIAN SOUL  \u2022  CHINESE SPIRIT")

c.showPage()
c.save()
print("PDF written: menu/B2B_Menu.pdf")
