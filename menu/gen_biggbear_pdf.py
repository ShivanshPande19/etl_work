#!/usr/bin/env python3
"""Bigg Bear Bites menu -> lightweight vector PDF (black + orange theme)."""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/google-noto"
pdfmetrics.registerFont(TTFont("Noto", f"{FD}/NotoSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Noto-Bold", f"{FD}/NotoSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Noto-Black", f"{FD}/NotoSans-Black.ttf"))
pdfmetrics.registerFont(TTFont("Noto-XBold", f"{FD}/NotoSans-ExtraBold.ttf"))

BODY_F, BODY_B, HEAD_F, BLACK_F = "Noto", "Noto-Bold", "Noto-XBold", "Noto-Black"
RS = "\u20b9"

# palette
BG      = HexColor("#100f0d")
BG2     = HexColor("#161310")
PANEL   = HexColor("#241d15")
PANEL2  = HexColor("#191511")
ORANGE  = HexColor("#ea7d1c")
ORANGE_HI = HexColor("#f7a13a")
AMBER   = HexColor("#f4b41a")
BORDER  = HexColor("#71481d")
TEXT    = HexColor("#f2ede3")
MUTED   = HexColor("#b6ab97")
PRICE   = HexColor("#f2b430")
LEADER  = HexColor("#5c4a32")

# ---------------- data ----------------
COL1 = [
    ("Chai", [("Adraki Chai", "15"), ("Masala Chai", "20")]),
    ("Patties", [("Aloo Patties", "40"), ("Paneer Patties", "50"), ("Chicken Patties", "60")]),
    ("Toasties", [("Bread Toast", "40"), ("Italian Toast", "89"),
                  ("Peri Peri Cheese Blast Toastie", "99")]),
    ("Bun Maska", [("Butter Bun Maska", "69"), ("Chocolate Bun Maska", "89"),
                   ("Cheese Pineapple Bun Maska", "99"),
                   ("Butter Scotch Crunch Bun Maska", "99")]),
    ("Maggi", [("Butter Double Masala Maggi", "59"), ("Hot Spicy Passion Maggi", "69"),
               ("Vegetable Masala Maggi", "79"), ("Cheese Chatori Maggi", "89"),
               ("Chilly Garlic Cheese Maggi", "89"), ("Egg Maggi", "99"),
               ("Egg Cheese Maggi", "99")]),
]
COL2 = [
    ("Sweet Corns", [("Classic Butter Sweet Corn", "69"), ("Masala Sweet Corn", "79"),
                     ("Peri Peri Sweet Corn", "89"), ("Cheese Sweet Corn", "99")]),
    ("Popcorns", [("Butter Popcorn", "69"), ("Extra Butter Popcorn", "89"),
                  ("Cheese Popcorn", "89")]),
    ("Nachos", [("Nachos With Cheesy Dip", "89"), ("Cheesy Delight Nachos", "109"),
                ("Nachos & Salsa", "109")]),
    ("Spiral Potatoes", [("Spiral Potato", "69"), ("Peri Peri Spiral Potato", "79"),
                         ("Cheese Spiral Potato", "89"), ("Tandoori Spiral Potato", "89")]),
    ("Bigg Bear Sub", [("Aloo Tikki Sub", "79"), ("Spicy Barbeque Sub", "89"),
                       ("Spicy Salsa Sub", "99"), ("Mexican King Sub", "99"),
                       ("Paneer Sub", "99"), ("Paneer Tikka Sub", "99"),
                       ("Grilled Chicken Sub", "99"), ("Chicken Seekh Sub", "109")]),
]
COL3 = [
    ("Veg Salads", [("Veggie Delight Salad", "149"), ("Sprouts Chana Salad", "149"),
                    ("Corn & Peas Salad", "149"), ("Paneer Tikka Salad", "149")]),
    ("Non-Veg Salads", [("Grilled Chicken Salad", "199"), ("Peri Peri Chicken Salad", "199"),
                        ("Creamy Chicken Salad", "199")]),
    ("Mojitos", [("Surprise Mojito", "89"), ("Spicy Devil Mojito", "89"),
                 ("Strawberry Mojito", "89"), ("Korean Mojito", "89"),
                 ("Tangy Mango Mojito", "89"), ("Pineapple Punch Mojito", "89"),
                 ("Litchi Mojito", "89"), ("Mint Mojito", "89"),
                 ("Orange Cinderella Mojito", "89"), ("Blue Heaven Mojito", "89")]),
    ("Nutri Special", [("Nutri Kulcha", "99"), ("Masala Nutri Kulcha", "99"),
                       ("Cheese Masala Nutri Kulcha", "119")]),
    ("Fries", [("Salted Fries", "99"), ("Peri Peri Fries", "129")]),
]

# ---------------- geometry ----------------
W, H = 820, 640
M = 26
CX0 = M + 12
CW = W - 2 * (M + 12)
GAP = 18
COLW = (CW - 2 * GAP) / 3.0
COLX = [CX0, CX0 + COLW + GAP, CX0 + 2 * (COLW + GAP)]
LINE_H = 13.0
PILL_H = 18
SEC_GAP = 10
NAME_FS = 8.9
PRICE_FS = 8.9

c = canvas.Canvas("menu/BiggBear_Menu.pdf", pagesize=(W, H))
c.setTitle("Bigg Bear Bites | Menu")


def diamond(cx, cy, r, color):
    p = c.beginPath()
    p.moveTo(cx, cy + r); p.lineTo(cx + r, cy); p.lineTo(cx, cy - r); p.lineTo(cx - r, cy)
    p.close(); c.setFillColor(color); c.drawPath(p, fill=1, stroke=0)


def dotted(x1, x2, y):
    if x2 - x1 < 4:
        return
    c.setStrokeColor(LEADER); c.setLineWidth(0.6); c.setDash([0.6, 2.3])
    c.line(x1, y, x2, y); c.setDash([])


def sec_header(x, y, w, title):
    c.setFillColor(PANEL); c.setStrokeColor(BORDER); c.setLineWidth(1.0)
    c.roundRect(x, y - PILL_H, w, PILL_H, 4, fill=1, stroke=1)
    # small orange accent bar on the left inside the pill
    c.setFillColor(ORANGE); c.rect(x + 6, y - PILL_H + 4, 3, PILL_H - 8, fill=1, stroke=0)
    t = title.upper()
    c.setFont(HEAD_F, 10.2); c.setFillColor(ORANGE_HI)
    c.drawString(x + 14, y - PILL_H + 5.2, t)
    return y - PILL_H - 7


def item_row(x, y, w, name, price):
    c.setFont(BODY_F, NAME_FS); c.setFillColor(TEXT)
    c.drawString(x, y, name)
    nw = c.stringWidth(name, BODY_F, NAME_FS)
    ptxt = RS + price
    c.setFont(BODY_B, PRICE_FS); c.setFillColor(PRICE)
    pw = c.stringWidth(ptxt, BODY_B, PRICE_FS)
    c.drawRightString(x + w, y, ptxt)
    dotted(x + nw + 3, x + w - pw - 3, y + 1.6)


def draw_section(x, y, w, sec):
    title, items = sec
    y = sec_header(x, y, w, title)
    for name, price in items:
        y -= 9
        item_row(x, y, w, name, price)
        y -= (LINE_H - 9)
    return y - SEC_GAP


# ---------------- background ----------------
c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(BG2); c.rect(M - 6, M - 6, W - 2 * (M - 6), H - 2 * (M - 6), fill=1, stroke=0)
c.setStrokeColor(BORDER); c.setLineWidth(2.0)
c.rect(M, M, W - 2 * M, H - 2 * M, fill=0, stroke=1)
c.setStrokeColor(HexColor("#3a2a16")); c.setLineWidth(0.8)
c.rect(M + 4, M + 4, W - 2 * (M + 4), H - 2 * (M + 4), fill=0, stroke=1)

# ---------------- header ----------------
def star(cx, cy, r, color):
    import math
    p = c.beginPath()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        px, py = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        (p.moveTo if i == 0 else p.lineTo)(px, py)
    p.close(); c.setFillColor(color); c.drawPath(p, fill=1, stroke=0)

cxm = W / 2.0
c.setFont(BLACK_F, 40)
big = "BIGG BEAR "; bites = "BITES"
wb = c.stringWidth(big, BLACK_F, 40); wt = c.stringWidth(bites, BLACK_F, 40)
startx = cxm - (wb + wt) / 2.0
ytitle = H - M - 46
c.setFillColor(AMBER); c.drawString(startx, ytitle, "BIGG ")
w1 = c.stringWidth("BIGG ", BLACK_F, 40)
c.setFillColor(ORANGE); c.drawString(startx + w1, ytitle, "BEAR ")
w2 = c.stringWidth("BEAR ", BLACK_F, 40)
c.setFillColor(TEXT); c.drawString(startx + w1 + w2, ytitle, bites)
star(startx - 22, ytitle + 12, 11, ORANGE)
star(startx + wb + wt + 22, ytitle + 12, 11, ORANGE)

# tagline
c.setFont(HEAD_F, 11); 
tag_parts = [("MADE FRESH", ORANGE_HI), ("  \u2022  ", MUTED), ("MADE BIGG", AMBER),
             ("  \u2022  ", MUTED), ("MADE FOR YOU", ORANGE_HI)]
tot = sum(c.stringWidth(t, HEAD_F, 11) for t, _ in tag_parts)
tx = cxm - tot / 2.0; tyy = H - M - 64
for t, col in tag_parts:
    c.setFillColor(col); c.drawString(tx, tyy, t); tx += c.stringWidth(t, HEAD_F, 11)
# divider
c.setStrokeColor(BORDER); c.setLineWidth(0.8)
c.line(cxm - 170, H - M - 74, cxm + 170, H - M - 74)
diamond(cxm, H - M - 74, 2.6, ORANGE)

# ---------------- columns ----------------
y_top = H - M - 90
for col, x in zip([COL1, COL2, COL3], COLX):
    y = y_top
    for sec in col:
        y = draw_section(x, y, COLW, sec)

# ---------------- footer ----------------
c.setFillColor(MUTED); c.setFont(BODY_F, 7.6)
c.drawCentredString(cxm, M + 12, "Bigg Bear Bites  \u2022  Prices in " + RS + " (INR), inclusive of taxes")

c.showPage(); c.save()
print("PDF written: menu/BiggBear_Menu.pdf")
