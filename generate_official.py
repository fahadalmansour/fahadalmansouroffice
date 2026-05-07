"""
Generate official brand papers and stamp for Fahad Almansour brand.
Outputs to brand_kit/official/
"""

import os, math
from PIL import Image, ImageDraw, ImageFont

# ── Output directory ────────────────────────────────────────────────
OUT = "/Users/fahadalmansour/fahad/brand_kit/official"
os.makedirs(OUT, exist_ok=True)

BADGE_PATH  = "/Users/fahadalmansour/fahad/brand_kit/favicon/favicon-512x512.png"
BADGE_BIG   = "/Users/fahadalmansour/fahad/badge_logo.png"

# ── Colors (Gold Premium) ───────────────────────────────────────────
DARK_BG   = (13, 8, 0)
GOLD      = (232, 200, 96)
PALE_GOLD = (255, 240, 160)
ACCENT    = (200, 160, 48)
CREAM     = (250, 248, 244)
BODY_TEXT = (26, 26, 26)
MID_GOLD  = (180, 140, 30)

# ── Fonts ────────────────────────────────────────────────────────────
FONT_DIR = "/Users/fahadalmansour/Library/Fonts"
SYS_FONT = "/System/Library/Fonts/Supplemental"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

NASKH_BOLD   = os.path.join(FONT_DIR, "NotoNaskhArabic-VariableFont_wght.ttf")
NASKH_REG    = NASKH_BOLD
SANS_BOLD    = os.path.join(SYS_FONT, "Arial Bold.ttf")
SANS_REG     = os.path.join(SYS_FONT, "Arial.ttf")
SERIF_BOLD   = os.path.join(SYS_FONT, "Times New Roman Bold.ttf")
SERIF_REG    = os.path.join(SYS_FONT, "Times New Roman.ttf")

def paste_badge(canvas: Image.Image, badge_path: str, size: int, x: int, y: int, cx=False):
    """Paste badge (RGBA) resized to size×size at top-left (x,y). cx=True centers x."""
    b = Image.open(badge_path).convert("RGBA").resize((size, size), Image.LANCZOS)
    if cx:
        x = x - size // 2
    canvas.paste(b, (x, y), b)

def draw_hline(draw, x0, x1, y, color, width=4):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)

def draw_vline(draw, x, y0, y1, color, width=4):
    draw.line([(x, y0), (x, y1)], fill=color, width=width)

def text_w(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def text_h(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def centered_text(draw, y, text, font, color, canvas_w, anchor_x=None):
    w = text_w(draw, text, font)
    x = (canvas_w - w) // 2 if anchor_x is None else anchor_x - w // 2
    draw.text((x, y), text, font=font, fill=color)
    return w

def curved_text(img: Image.Image, text: str, font, color,
                cx: int, cy: int, radius: int,
                start_angle_deg: float, clockwise: bool = True,
                letter_spacing: float = 1.0):
    """Draw text curved along a circle arc."""
    draw_tmp = ImageDraw.Draw(img)
    chars = list(text)
    n = len(chars)
    if n == 0:
        return

    # Measure each character width to space them along the arc
    widths = []
    for c in chars:
        bb = draw_tmp.textbbox((0, 0), c, font=font)
        widths.append((bb[2] - bb[0]) * letter_spacing)

    total_arc_px = sum(widths)
    total_angle_rad = total_arc_px / radius  # arc length = r * theta

    # Start angle so text is centered around start_angle_deg
    angle = math.radians(start_angle_deg) - total_angle_rad / 2

    for i, c in enumerate(chars):
        char_w = widths[i]
        mid_angle = angle + (char_w / 2) / radius

        x = cx + radius * math.cos(mid_angle)
        y = cy + radius * math.sin(mid_angle)

        # Rotate: tangent direction
        rot_deg = math.degrees(mid_angle) + (90 if clockwise else -90)

        # Render character on transparent tile
        tile_size = max(char_w + 20, text_h(draw_tmp, c, font) + 20)
        tile = Image.new("RGBA", (int(tile_size), int(tile_size)), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(tile)
        tdraw.text((tile_size // 2, tile_size // 2), c, font=font, fill=color,
                   anchor="mm")
        tile = tile.rotate(-rot_deg, expand=True, resample=Image.BICUBIC)
        tw, th = tile.size
        paste_x = int(x - tw / 2)
        paste_y = int(y - th / 2)
        img.paste(tile, (paste_x, paste_y), tile)

        angle += char_w / radius

# ═══════════════════════════════════════════════════════════════════
#  1. OFFICIAL ROUND STAMP / SEAL
# ═══════════════════════════════════════════════════════════════════

def make_stamp(ink_color_rgb, suffix, bg_transparent=True):
    SIZE   = 900
    CX, CY = SIZE // 2, SIZE // 2

    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ink = ink_color_rgb
    ink_a = ink + (255,)

    # Outer ring (double)
    R_OUTER = 420
    R_INNER = 375
    R_LOGO  = 200
    draw.ellipse([CX-R_OUTER, CY-R_OUTER, CX+R_OUTER, CY+R_OUTER],
                 outline=ink_a, width=14)
    draw.ellipse([CX-R_INNER, CY-R_INNER, CX+R_INNER, CY+R_INNER],
                 outline=ink_a, width=6)

    # 24 small dots on outer ring at 15° intervals
    for i in range(24):
        a = math.radians(i * 15)
        dx = (R_OUTER - 22) * math.cos(a)
        dy = (R_OUTER - 22) * math.sin(a)
        draw.ellipse([CX+dx-4, CY+dy-4, CX+dx+4, CY+dy+4], fill=ink_a)

    # Arabic company name curved on top half
    # "مكتب فهد سعد المنصور"  — reversed for display
    ar_text = "مكتب فهد سعد المنصور"
    f_ar = load_font(NASKH_BOLD, 48)
    curved_text(img, ar_text, f_ar, ink_a, CX, CY,
                radius=400, start_angle_deg=-90, clockwise=True,
                letter_spacing=1.1)

    # English text curved on bottom half
    en_text = "FAHAD ALMANSOUR · ELECTRONIC SERVICES"
    f_en = load_font(SANS_BOLD, 32)
    curved_text(img, en_text, f_en, ink_a, CX, CY,
                radius=400, start_angle_deg=90, clockwise=False,
                letter_spacing=1.0)

    # Badge in center — clipped to circle so no square bg shows
    badge_sz = R_LOGO * 2
    badge_src = Image.open(BADGE_PATH).convert("RGBA").resize((badge_sz, badge_sz), Image.LANCZOS)
    # Create circular mask
    mask = Image.new("L", (badge_sz, badge_sz), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, badge_sz - 1, badge_sz - 1], fill=255)
    badge_circ = Image.new("RGBA", (badge_sz, badge_sz), (0, 0, 0, 0))
    badge_circ.paste(badge_src, (0, 0), mask)
    img.paste(badge_circ, (CX - R_LOGO, CY - R_LOGO), badge_circ)

    # CR number at very bottom inside inner ring
    f_cr = load_font(SANS_BOLD, 34)
    cr_text = "S.C.R. No. 7053130576"
    cr_w = text_w(draw, cr_text, f_cr)
    draw.text((CX - cr_w // 2, CY + R_INNER - 70), cr_text, font=f_cr, fill=ink_a)

    # Horizontal divider lines inside stamp
    draw.line([(CX - R_INNER + 30, CY + R_INNER - 80),
               (CX + R_INNER - 30, CY + R_INNER - 80)],
              fill=ink_a, width=2)

    # If we want a solid white background version for preview
    if not bg_transparent:
        bg = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 255))
        bg.paste(img, (0, 0), img)
        img = bg

    out_path = os.path.join(OUT, f"stamp-{suffix}.png")
    img.save(out_path, "PNG")
    print(f"  saved: stamp-{suffix}.png  ({SIZE}x{SIZE})")
    return out_path

print("Generating stamps...")
make_stamp((160, 0, 0), "red-ink")
make_stamp((0, 51, 128), "blue-ink")
make_stamp((200, 160, 48), "gold-preview", bg_transparent=False)

# ═══════════════════════════════════════════════════════════════════
#  2. OFFICIAL LETTERHEAD  (A4 @ 150 DPI = 1240 × 1754 px)
# ═══════════════════════════════════════════════════════════════════

def make_letterhead():
    W, H  = 1240, 1754
    MARG  = 80
    img   = Image.new("RGB", (W, H), CREAM)
    draw  = ImageDraw.Draw(img)

    # ── Header band ──────────────────────────────────────────────────
    HDR_H = 300
    draw.rectangle([0, 0, W, HDR_H], fill=DARK_BG)

    # Badge left in header
    badge_size = 220
    paste_badge(img, BADGE_PATH, badge_size, MARG, (HDR_H - badge_size) // 2)

    # Company names right side of badge
    x_text = MARG + badge_size + 30
    # Arabic company name
    f_ar_lg  = load_font(NASKH_BOLD, 52)
    f_ar_sm  = load_font(NASKH_BOLD, 30)
    f_en_lg  = load_font(SERIF_BOLD, 42)
    f_en_sm  = load_font(SANS_REG, 26)

    ar_name = "مكتب فهد سعد فهد المنصور"
    ar_sub  = "للخدمات الإلكترونية"
    en_name = "Fahad Saad Fahad Almansour"
    en_sub  = "Office For Electronic Services"
    en_web  = "fahadalmansouroffice.com  ·  CR #7053130576"

    draw.text((x_text, 38),  ar_name, font=f_ar_lg, fill=PALE_GOLD)
    draw.text((x_text, 100), ar_sub,  font=f_ar_sm, fill=GOLD)
    draw.text((x_text, 148), en_name, font=f_en_lg, fill=PALE_GOLD)
    draw.text((x_text, 202), en_sub,  font=f_en_sm, fill=GOLD)
    draw.text((x_text, 240), en_web,  font=f_en_sm, fill=ACCENT)

    # Gold divider under header
    draw.rectangle([0, HDR_H, W, HDR_H + 5], fill=ACCENT)
    draw.rectangle([0, HDR_H + 5, W, HDR_H + 9], fill=GOLD)

    # ── Left margin gold stripe ──────────────────────────────────────
    draw.rectangle([0, HDR_H + 9, 6, H - 180], fill=ACCENT)

    # ── Content area guides (placeholder lines) ──────────────────────
    f_label  = load_font(NASKH_BOLD, 32)
    f_label2 = load_font(SANS_REG, 22)
    f_dots   = load_font(SANS_REG, 24)

    y = HDR_H + 60
    # Date / reference row
    draw.text((MARG + 20, y),
              "Date: _______________   Ref No.: ______________",
              font=f_label2, fill=(140, 120, 80))
    y += 60

    # Gold thin divider
    draw.rectangle([MARG, y, W - MARG, y + 2], fill=ACCENT)
    y += 30

    # Subject row
    draw.text((MARG + 20, y),
              "Subject / الموضوع:  _____________________________________",
              font=f_label2, fill=(140, 120, 80))
    y += 60

    # Body area — faint dotted lines
    line_h = 46
    for i in range(20):
        yy = y + i * line_h
        if yy > H - 220:
            break
        draw.line([(MARG + 20, yy), (W - MARG - 20, yy)],
                  fill=(200, 185, 140, 60), width=1)

    # ── Watermark badge (faint) ──────────────────────────────────────
    badge_wm = Image.open(BADGE_PATH).convert("RGBA").resize((400, 400), Image.LANCZOS)
    # Lower opacity
    r, g, b, a = badge_wm.split()
    a = a.point(lambda x: int(x * 0.08))
    badge_wm = Image.merge("RGBA", (r, g, b, a))
    wm_x = (W - 400) // 2
    wm_y = HDR_H + (H - HDR_H - 400) // 2
    img.paste(badge_wm, (wm_x, wm_y), badge_wm)

    # ── Footer band ──────────────────────────────────────────────────
    FTR_Y = H - 175
    draw.rectangle([0, FTR_Y, W, H], fill=DARK_BG)
    draw.rectangle([0, FTR_Y, W, FTR_Y + 4], fill=ACCENT)
    draw.rectangle([0, FTR_Y + 4, W, FTR_Y + 7], fill=GOLD)

    f_ftr = load_font(SANS_REG, 22)
    f_ftr_sm = load_font(SANS_REG, 18)
    ftr_items = [
        ("مملكة العربية السعودية", PALE_GOLD),
        ("Kingdom of Saudi Arabia", GOLD),
        ("fahadalmansouroffice.com", ACCENT),
        ("CR #7053130576", ACCENT),
    ]
    col_w = (W - 2 * MARG) // len(ftr_items)
    for i, (txt, col) in enumerate(ftr_items):
        x_f = MARG + i * col_w
        draw.text((x_f, FTR_Y + 20), txt, font=f_ftr, fill=col)

    draw.text((MARG, FTR_Y + 70),
              "© 2026 مكتب فهد سعد فهد المنصور للخدمات الإلكترونية  ·  All rights reserved",
              font=f_ftr_sm, fill=(120, 100, 50))

    out_path = os.path.join(OUT, "letterhead-a4.png")
    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"  saved: letterhead-a4.png  ({W}x{H})")

print("\nGenerating letterhead...")
make_letterhead()

# ═══════════════════════════════════════════════════════════════════
#  3. BUSINESS CARD — FRONT  (1050 × 600 px @ 300 DPI = 3.5"×2")
# ═══════════════════════════════════════════════════════════════════

def make_business_card():
    W, H = 1050, 600

    # ── FRONT (dark Gold Premium) ────────────────────────────────────
    front = Image.new("RGB", (W, H), DARK_BG)
    draw  = ImageDraw.Draw(front)

    # Left half: badge + subtle geometric diamond pattern
    BADGE_SZ = 260
    paste_badge(front, BADGE_PATH, BADGE_SZ, 60, (H - BADGE_SZ) // 2)

    # Vertical gold divider
    draw.rectangle([370, 60, 374, H - 60], fill=ACCENT)
    draw.rectangle([375, 80, 378, H - 80], fill=GOLD)

    # Right half: text
    x_r = 410
    f_name_en = load_font(SERIF_BOLD, 52)
    f_sub_en  = load_font(SERIF_REG, 28)
    f_name_ar = load_font(NASKH_BOLD, 48)
    f_detail  = load_font(SANS_REG, 24)

    draw.text((x_r, 70),  "Fahad Saad Almansour",         font=f_name_en, fill=PALE_GOLD)
    draw.text((x_r, 132), "Office For Electronic Services", font=f_sub_en,  fill=GOLD)

    draw.text((x_r, 188),
              "فهد سعد المنصور",
              font=f_name_ar, fill=PALE_GOLD)
    draw.text((x_r, 248),
              "مكتب للخدمات الإلكترونية",
              font=f_detail, fill=GOLD)

    # Gold thin divider
    draw.rectangle([x_r, 312, W - 60, 315], fill=ACCENT)

    # Contact details
    f_contact = load_font(SANS_REG, 26)
    contacts = [
        ("fahadalmansouroffice.com",    360),
        ("+966 57 013 1122",        405),
        ("CR #7053130576",          450),
        ("Kingdom of Saudi Arabia", 495),
    ]
    for txt, y_c in contacts:
        draw.text((x_r, y_c), txt, font=f_contact, fill=ACCENT)

    # Bottom thin gold lines
    draw.rectangle([0, H - 12, W, H - 8],  fill=ACCENT)
    draw.rectangle([0, H - 7,  W, H - 3],  fill=GOLD)

    front.save(os.path.join(OUT, "business-card-front.png"), "PNG", dpi=(300, 300))
    print("  saved: business-card-front.png  (1050x600)")

    # ── BACK (geometric gold pattern) ────────────────────────────────
    back = Image.new("RGB", (W, H), DARK_BG)
    draw2 = ImageDraw.Draw(back)

    # Diamond grid pattern
    STEP = 80
    for row in range(-2, H // STEP + 3):
        for col in range(-2, W // STEP + 3):
            x_c = col * STEP + (row % 2) * (STEP // 2)
            y_c = row * STEP
            pts = [(x_c, y_c - 16), (x_c + 12, y_c),
                   (x_c, y_c + 16), (x_c - 12, y_c)]
            draw2.polygon(pts, outline=(200, 160, 48, 35), fill=None)

    # Large badge centered, low opacity
    badge_back = Image.open(BADGE_PATH).convert("RGBA").resize((340, 340), Image.LANCZOS)
    r, g, b, a = badge_back.split()
    a = a.point(lambda x: int(x * 0.18))
    badge_back = Image.merge("RGBA", (r, g, b, a))
    back.paste(badge_back, ((W - 340) // 2, (H - 340) // 2), badge_back)

    # Centered domain name
    f_domain = load_font(SERIF_BOLD, 46)
    f_dom_sub = load_font(SANS_REG, 28)
    dw = text_w(draw2, "fahadalmansouroffice.com", f_domain)
    draw2.text(((W - dw) // 2, H // 2 - 36), "fahadalmansouroffice.com",
               font=f_domain, fill=PALE_GOLD)
    sub_txt = "مكتب فهد سعد فهد المنصور للخدمات الإلكترونية"
    sw = text_w(draw2, sub_txt, f_dom_sub)
    draw2.text(((W - sw) // 2, H // 2 + 28), sub_txt, font=f_dom_sub, fill=GOLD)

    # Border lines
    draw2.rectangle([0, 0, W - 1, H - 1], outline=ACCENT, width=8)
    draw2.rectangle([12, 12, W - 13, H - 13], outline=MID_GOLD, width=3)

    back.save(os.path.join(OUT, "business-card-back.png"), "PNG", dpi=(300, 300))
    print("  saved: business-card-back.png   (1050x600)")

print("\nGenerating business card...")
make_business_card()

# ═══════════════════════════════════════════════════════════════════
#  4. INVOICE / QUOTATION HEADER  (A4 width @ 150 DPI)
# ═══════════════════════════════════════════════════════════════════

def make_invoice_header():
    W = 1240
    # Full A4-width invoice template (just header + table shell)
    H = 1754
    img  = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header band
    HDR_H = 260
    draw.rectangle([0, 0, W, HDR_H], fill=DARK_BG)

    # Badge
    paste_badge(img, BADGE_PATH, 200, 50, 30)

    # Company info
    f_ar = load_font(NASKH_BOLD, 46)
    f_sm = load_font(NASKH_BOLD, 28)
    f_en = load_font(SERIF_BOLD, 38)
    f_ws = load_font(SANS_REG, 22)

    x_t = 290
    draw.text((x_t, 22),
              "مكتب فهد سعد فهد المنصور",
              font=f_ar, fill=PALE_GOLD)
    draw.text((x_t, 78),
              "للخدمات الإلكترونية",
              font=f_sm, fill=GOLD)
    draw.text((x_t, 120), "Fahad Saad Fahad Almansour",       font=f_en, fill=PALE_GOLD)
    draw.text((x_t, 168), "Office For Electronic Services",    font=f_ws, fill=GOLD)
    draw.text((x_t, 200), "fahadalmansouroffice.com  |  CR #7053130576", font=f_ws, fill=ACCENT)
    draw.text((x_t, 228), "Kingdom of Saudi Arabia", font=f_ws, fill=(140, 120, 60))

    # Document type banner (right side)
    doc_w = 300
    draw.rectangle([W - doc_w - 20, 20, W - 20, 120], fill=ACCENT)
    f_doc = load_font(SERIF_BOLD, 44)
    f_doc2 = load_font(NASKH_BOLD, 38)
    draw.text((W - doc_w, 26), "INVOICE", font=f_doc, fill=DARK_BG)
    draw.text((W - doc_w, 72),
              "فاتورة",
              font=f_doc2, fill=DARK_BG)

    # Invoice number box
    draw.rectangle([W - doc_w - 20, 125, W - 20, 240], outline=ACCENT, width=3)
    f_lbl = load_font(SANS_REG, 20)
    f_num = load_font(SANS_BOLD, 28)
    draw.text((W - doc_w - 10, 130), "Invoice No. / رقم الفاتورة:", font=f_lbl, fill=GOLD)
    draw.text((W - doc_w - 10, 158), "INV-2026-____",  font=f_num, fill=PALE_GOLD)
    draw.text((W - doc_w - 10, 195), "Date / التاريخ:   _____________", font=f_lbl, fill=GOLD)

    # Gold divider
    draw.rectangle([0, HDR_H, W, HDR_H + 5], fill=ACCENT)
    draw.rectangle([0, HDR_H + 5, W, HDR_H + 8], fill=GOLD)

    MARG = 60
    y = HDR_H + 40

    # ── Bill To / From boxes ─────────────────────────────────────────
    f_box  = load_font(SANS_BOLD, 22)
    f_box2 = load_font(SANS_REG, 20)
    bw = (W - 3 * MARG) // 2

    # Bill To
    draw.rectangle([MARG, y, MARG + bw, y + 180], outline=ACCENT, width=2)
    draw.rectangle([MARG, y, MARG + bw, y + 34], fill=ACCENT)
    draw.text((MARG + 10, y + 6),
              "Bill To / فاتورة إلى:", font=f_box, fill=DARK_BG)
    placeholder_lines = ["Client Name / اسم العميل:", "Address / العنوان:", "Phone / الهاتف:", "Email:"]
    for i, pl in enumerate(placeholder_lines):
        draw.text((MARG + 10, y + 44 + i * 34), pl, font=f_box2, fill=(150, 130, 80))

    # Payment info
    x2 = MARG + bw + MARG
    draw.rectangle([x2, y, x2 + bw, y + 180], outline=ACCENT, width=2)
    draw.rectangle([x2, y, x2 + bw, y + 34], fill=ACCENT)
    draw.text((x2 + 10, y + 6),
              "Payment Info / معلومات الدفع:", font=f_box, fill=DARK_BG)
    pay_lines = ["Bank: ____________________________",
                 "IBAN: SA______________________",
                 "Beneficiary: Fahad Almansour",
                 "Currency: SAR"]
    for i, pl in enumerate(pay_lines):
        draw.text((x2 + 10, y + 44 + i * 34), pl, font=f_box2, fill=(150, 130, 80))

    y += 210

    # ── Line items table ─────────────────────────────────────────────
    cols = ["#", "Description / الوصف", "Qty", "Unit Price", "Total"]
    col_widths = [60, 580, 100, 180, 180]
    col_x = [MARG]
    for cw in col_widths[:-1]:
        col_x.append(col_x[-1] + cw)

    # Header row
    draw.rectangle([MARG, y, W - MARG, y + 44], fill=DARK_BG)
    for i, (cx_t, header) in enumerate(zip(col_x, cols)):
        draw.text((cx_t + 8, y + 10), header, font=f_box, fill=PALE_GOLD)

    y += 44
    # 8 empty rows
    ROW_H = 50
    for row in range(8):
        yy = y + row * ROW_H
        bg = CREAM if row % 2 == 0 else (240, 236, 224)
        draw.rectangle([MARG, yy, W - MARG, yy + ROW_H], fill=bg)
        draw.text((col_x[0] + 8, yy + 14), str(row + 1), font=f_box2, fill=(180, 160, 100))
        # Vertical col dividers
        for cx_t in col_x[1:]:
            draw.line([(cx_t, yy), (cx_t, yy + ROW_H)], fill=ACCENT, width=1)

    y += 8 * ROW_H

    # Totals block
    tot_x = col_x[-2]
    draw.rectangle([MARG, y, W - MARG, y + 2], fill=ACCENT)
    y += 10
    totals = [("Subtotal / المجموع الفرعي:", "SAR ___________"),
              ("VAT 15% / ضريبة القيمة المضافة:", "SAR ___________"),
              ("TOTAL / المجموع الكلي:", "SAR ___________")]
    f_tot = load_font(SANS_BOLD, 24)
    f_tot2 = load_font(SANS_REG, 22)
    for i, (label, val) in enumerate(totals):
        yy = y + i * 50
        bg = DARK_BG if i == 2 else CREAM
        fc = PALE_GOLD if i == 2 else BODY_TEXT
        draw.rectangle([tot_x, yy, W - MARG, yy + 46], fill=bg)
        draw.text((tot_x + 10, yy + 11), label, font=f_tot if i==2 else f_tot2, fill=fc)
        vw = text_w(draw, val, f_tot)
        draw.text((W - MARG - vw - 10, yy + 11), val, font=f_tot, fill=fc)

    y += 3 * 50 + 30

    # Notes box
    draw.rectangle([MARG, y, W // 2 - 20, y + 160], outline=ACCENT, width=2)
    draw.rectangle([MARG, y, W // 2 - 20, y + 34], fill=ACCENT)
    draw.text((MARG + 10, y + 6), "Notes / ملاحظات:", font=f_box, fill=DARK_BG)
    note_txt = "Thank you for your business.\nشكراً لثقتكم بنا."
    draw.multiline_text((MARG + 10, y + 46), note_txt, font=f_box2, fill=(130, 110, 60))

    # Signature box
    x_sig = W // 2 + 20
    draw.rectangle([x_sig, y, W - MARG, y + 160], outline=ACCENT, width=2)
    draw.rectangle([x_sig, y, W - MARG, y + 34], fill=ACCENT)
    draw.text((x_sig + 10, y + 6),
              "Authorized Signature / التوقيع:", font=f_box, fill=DARK_BG)
    draw.line([(x_sig + 30, y + 140), (W - MARG - 30, y + 140)],
              fill=ACCENT, width=2)
    draw.text((x_sig + 10, y + 100), "Fahad Saad Fahad Almansour", font=f_box2, fill=(150, 130, 80))

    # ── Footer ───────────────────────────────────────────────────────
    FTR_Y = H - 90
    draw.rectangle([0, FTR_Y, W, H], fill=DARK_BG)
    draw.rectangle([0, FTR_Y, W, FTR_Y + 4], fill=ACCENT)
    f_ftr = load_font(SANS_REG, 20)
    draw.text((MARG, FTR_Y + 20),
              "fahadalmansouroffice.com  |  CR #7053130576  |  Kingdom of Saudi Arabia",
              font=f_ftr, fill=GOLD)
    ftr_ar = "مملكة العربية السعودية  |سجل تجاري 7053130576"
    draw.text((MARG, FTR_Y + 52), ftr_ar, font=f_ftr, fill=ACCENT)

    out_path = os.path.join(OUT, "invoice-template.png")
    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"  saved: invoice-template.png  ({W}x{H})")

print("\nGenerating invoice template...")
make_invoice_header()

# ═══════════════════════════════════════════════════════════════════
#  5. ENVELOPE FRONT  (DL envelope: 2598 × 1299 px @ 300 DPI)
# ═══════════════════════════════════════════════════════════════════

def make_envelope():
    W, H = 2598, 1299
    img  = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Left stripe
    draw.rectangle([0, 0, 320, H], fill=DARK_BG)

    # Badge in stripe
    paste_badge(img, BADGE_PATH, 220, 50, (H - 220) // 2)

    # Gold divider line
    draw.rectangle([320, 0, 326, H], fill=ACCENT)

    # Sender (top-left inside)
    f_en = load_font(SERIF_BOLD, 36)
    f_sm = load_font(SANS_REG, 24)
    f_ar = load_font(NASKH_BOLD, 38)
    draw.text((360, 60),  "Fahad Saad Fahad Almansour", font=f_en, fill=DARK_BG)
    draw.text((360, 106), "Office For Electronic Services", font=f_sm, fill=(80, 60, 20))
    draw.text((360, 140),
              "مكتب فهد سعد فهد المنصور",
              font=f_ar, fill=DARK_BG)
    draw.text((360, 188), "Kingdom of Saudi Arabia  |  fahadalmansouroffice.com", font=f_sm, fill=(100, 80, 30))

    # "TO" address area (center)
    draw.rectangle([700, 380, 1700, 780], outline=ACCENT, width=3)
    f_to = load_font(SANS_BOLD, 28)
    f_to2 = load_font(SANS_REG, 26)
    draw.text((720, 390), "To / إلى:", font=f_to, fill=DARK_BG)
    for i, line in enumerate(["Name:", "Address:", "City, Country:"]):
        draw.text((720, 440 + i * 80), line, font=f_to2, fill=(160, 140, 90))
        draw.line([(830 if i == 0 else 920, 470 + i * 80),
                   (1680, 470 + i * 80)], fill=ACCENT, width=1)

    # Postage area
    draw.rectangle([W - 400, 40, W - 40, 300], outline=ACCENT, width=3)
    draw.text((W - 390, 55), "POSTAGE", font=f_to2, fill=(160, 140, 90))

    # Bottom gold line
    draw.rectangle([0, H - 18, W, H], fill=DARK_BG)
    draw.rectangle([320, H - 18, W, H - 12], fill=ACCENT)
    draw.rectangle([320, H - 12, W, H - 6], fill=GOLD)

    out_path = os.path.join(OUT, "envelope-dl.png")
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"  saved: envelope-dl.png  ({W}x{H})")

print("\nGenerating envelope...")
make_envelope()

# ═══════════════════════════════════════════════════════════════════
#  6. LIGHT-THEME BUSINESS CARD  (for light / white backgrounds)
# ═══════════════════════════════════════════════════════════════════

def make_business_card_light():
    W, H = 1050, 600

    # ── FRONT (cream/white with navy accents) ────────────────────────
    LIGHT_BG   = (252, 250, 246)
    DARK_TEXT  = (13, 8, 0)
    NAVY       = (14, 59, 114)
    GOLD_LT    = (160, 110, 10)
    ACCENT_LT  = (140, 95, 10)

    front = Image.new("RGB", (W, H), LIGHT_BG)
    draw  = ImageDraw.Draw(front)

    # Left accent stripe (navy)
    draw.rectangle([0, 0, 14, H], fill=NAVY)
    draw.rectangle([14, 0, 18, H], fill=(200, 160, 48))

    # Badge
    paste_badge(front, BADGE_PATH, 240, 38, (H - 240) // 2)

    # Vertical divider
    draw.rectangle([310, 50, 313, H - 50], fill=(200, 160, 48))
    draw.rectangle([314, 70, 316, H - 70], fill=NAVY)

    # Right half text
    x_r = 336
    f_name_en = load_font(SERIF_BOLD, 52)
    f_sub_en  = load_font(SERIF_REG, 28)
    f_name_ar = load_font(NASKH_BOLD, 46)
    f_detail  = load_font(SANS_REG, 24)
    f_contact = load_font(SANS_REG, 24)

    draw.text((x_r, 70),  "Fahad Saad Almansour",          font=f_name_en, fill=DARK_TEXT)
    draw.text((x_r, 132), "Office For Electronic Services",  font=f_sub_en,  fill=NAVY)
    draw.text((x_r, 182),
              "فهد سعد المنصور",
              font=f_name_ar, fill=DARK_TEXT)
    draw.text((x_r, 240),
              "مكتب للخدمات الإلكترونية",
              font=f_detail, fill=NAVY)

    draw.rectangle([x_r, 296, W - 50, 299], fill=(200, 160, 48))

    contacts = [
        ("fahadalmansouroffice.com",    322),
        ("+966 57 013 1122",        358),
        ("CR #7053130576",          394),
        ("Kingdom of Saudi Arabia", 430),
    ]
    for txt, y_c in contacts:
        draw.text((x_r, y_c), txt, font=f_contact, fill=GOLD_LT)

    # Top/bottom accent lines
    draw.rectangle([0, 0,    W, 6],  fill=NAVY)
    draw.rectangle([0, 6,    W, 10], fill=(200, 160, 48))
    draw.rectangle([0, H-10, W, H-6], fill=(200, 160, 48))
    draw.rectangle([0, H-6,  W, H],   fill=NAVY)

    front.save(os.path.join(OUT, "business-card-front-light.png"), "PNG", dpi=(300, 300))
    print("  saved: business-card-front-light.png")

    # ── BACK (light, geometric pattern) ─────────────────────────────
    back = Image.new("RGB", (W, H), LIGHT_BG)
    draw2 = ImageDraw.Draw(back)

    # Diamond grid (faint)
    STEP = 80
    for row in range(-2, H // STEP + 3):
        for col in range(-2, W // STEP + 3):
            x_c = col * STEP + (row % 2) * (STEP // 2)
            y_c = row * STEP
            pts = [(x_c, y_c - 16), (x_c + 12, y_c),
                   (x_c, y_c + 16), (x_c - 12, y_c)]
            draw2.polygon(pts, outline=(180, 140, 30, 40), fill=None)

    # Faint badge watermark
    badge_back = Image.open(BADGE_PATH).convert("RGBA").resize((320, 320), Image.LANCZOS)
    r, g, b, a = badge_back.split()
    a = a.point(lambda x: int(x * 0.12))
    badge_back = Image.merge("RGBA", (r, g, b, a))
    back.paste(badge_back, ((W - 320) // 2, (H - 320) // 2), badge_back)

    f_domain  = load_font(SERIF_BOLD, 44)
    f_dom_sub = load_font(SANS_REG, 26)
    dw = text_w(draw2, "fahadalmansouroffice.com", f_domain)
    draw2.text(((W - dw) // 2, H // 2 - 32), "fahadalmansouroffice.com",
               font=f_domain, fill=DARK_TEXT)
    sub_txt = "مكتب فهد سعد فهد المنصور للخدمات الإلكترونية"
    sw = text_w(draw2, sub_txt, f_dom_sub)
    draw2.text(((W - sw) // 2, H // 2 + 26), sub_txt, font=f_dom_sub, fill=NAVY)

    draw2.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=8)
    draw2.rectangle([12, 12, W - 13, H - 13], outline=(200, 160, 48), width=3)

    back.save(os.path.join(OUT, "business-card-back-light.png"), "PNG", dpi=(300, 300))
    print("  saved: business-card-back-light.png")

print("\nGenerating light-theme business card...")
make_business_card_light()

# ═══════════════════════════════════════════════════════════════════
#  7. LIGHT-THEME LETTERHEAD  (for printing on white paper)
# ═══════════════════════════════════════════════════════════════════

def make_letterhead_light():
    W, H  = 1240, 1754
    MARG  = 80
    NAVY       = (14, 59, 114)
    NAVY_DK    = (8, 35, 75)
    GOLD_LT    = (160, 110, 10)
    ACCENT_LT  = (200, 160, 48)
    LIGHT_BG   = (252, 250, 246)

    img  = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # ── Header (navy) ────────────────────────────────────────────────
    HDR_H = 300
    draw.rectangle([0, 0, W, HDR_H], fill=NAVY)

    # Badge left
    paste_badge(img, BADGE_PATH, 220, MARG, (HDR_H - 220) // 2)

    x_text = MARG + 220 + 30
    f_ar_lg = load_font(NASKH_BOLD, 52)
    f_ar_sm = load_font(NASKH_BOLD, 30)
    f_en_lg = load_font(SERIF_BOLD, 42)
    f_en_sm = load_font(SANS_REG, 26)

    draw.text((x_text, 38),  "مكتب فهد سعد فهد المنصور",   font=f_ar_lg, fill=(255, 240, 160))
    draw.text((x_text, 100), "للخدمات الإلكترونية",          font=f_ar_sm, fill=(232, 200, 96))
    draw.text((x_text, 148), "Fahad Saad Fahad Almansour",    font=f_en_lg, fill=(255, 240, 160))
    draw.text((x_text, 202), "Office For Electronic Services", font=f_en_sm, fill=(200, 168, 72))
    draw.text((x_text, 240),
              "fahadalmansouroffice.com  ·  CR #7053130576  ·  +966 57 013 1122",
              font=f_en_sm, fill=(180, 150, 50))

    # Gold divider lines
    draw.rectangle([0, HDR_H, W, HDR_H + 5], fill=ACCENT_LT)
    draw.rectangle([0, HDR_H + 5, W, HDR_H + 8], fill=GOLD_LT)

    # Left navy stripe
    draw.rectangle([0, HDR_H + 8, 6, H - 180], fill=NAVY)

    # Content area
    f_label2 = load_font(SANS_REG, 22)
    y = HDR_H + 60
    draw.text((MARG + 20, y),
              "Date: _______________   Ref No.: ______________",
              font=f_label2, fill=(100, 80, 30))
    y += 60
    draw.rectangle([MARG, y, W - MARG, y + 2], fill=ACCENT_LT)
    y += 30
    draw.text((MARG + 20, y),
              "Subject / الموضوع:  _____________________________________",
              font=f_label2, fill=(100, 80, 30))
    y += 60

    line_h = 46
    for i in range(20):
        yy = y + i * line_h
        if yy > H - 220:
            break
        draw.line([(MARG + 20, yy), (W - MARG - 20, yy)],
                  fill=(180, 160, 100, 60), width=1)

    # Faint badge watermark
    badge_wm = Image.open(BADGE_PATH).convert("RGBA").resize((380, 380), Image.LANCZOS)
    r, g, b, a = badge_wm.split()
    a = a.point(lambda x: int(x * 0.06))
    badge_wm = Image.merge("RGBA", (r, g, b, a))
    img.paste(badge_wm, ((W - 380) // 2, HDR_H + (H - HDR_H - 380) // 2), badge_wm)

    # ── Footer (navy) ─────────────────────────────────────────────────
    FTR_Y = H - 175
    draw.rectangle([0, FTR_Y, W, H], fill=NAVY)
    draw.rectangle([0, FTR_Y, W, FTR_Y + 4], fill=ACCENT_LT)
    draw.rectangle([0, FTR_Y + 4, W, FTR_Y + 7], fill=GOLD_LT)

    f_ftr    = load_font(SANS_REG, 22)
    f_ftr_sm = load_font(SANS_REG, 18)
    ftr_items = [
        ("مملكة العربية السعودية", (255, 240, 160)),
        ("Kingdom of Saudi Arabia", (200, 168, 72)),
        ("fahadalmansouroffice.com",     (200, 160, 48)),
        ("+966 57 013 1122",         (200, 160, 48)),
    ]
    col_w = (W - 2 * MARG) // len(ftr_items)
    for i, (txt, col) in enumerate(ftr_items):
        draw.text((MARG + i * col_w, FTR_Y + 20), txt, font=f_ftr, fill=col)

    draw.text((MARG, FTR_Y + 70),
              "© 2026 مكتب فهد سعد فهد المنصور  ·  All rights reserved  ·  CR #7053130576",
              font=f_ftr_sm, fill=(150, 130, 60))

    out_path = os.path.join(OUT, "letterhead-a4-light.png")
    img.save(out_path, "PNG", dpi=(150, 150))
    print(f"  saved: letterhead-a4-light.png  ({W}x{H})")

print("\nGenerating light-theme letterhead...")
make_letterhead_light()

print("\nAll official papers generated in brand_kit/official/")
print("Files:")
for f in sorted(os.listdir(OUT)):
    fpath = os.path.join(OUT, f)
    size_kb = os.path.getsize(fpath) // 1024
    print(f"  {f}  ({size_kb} KB)")
