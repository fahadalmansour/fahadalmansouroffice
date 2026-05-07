# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Brand identity system and website for **Fahad Saad Fahad Almansour — Office For Electronic Services**
(مكتب فهد سعد فهد المنصور للخدمات الإلكترونية), a Saudi establishment (CR #7053130576).

GitHub: https://github.com/fahadalmansour/fahadalmansourconsulting

## Key facts

| Field | Value |
|-------|-------|
| Domain | `fahadalmansouroffice.com` |
| Email | `info@fahadalmansouroffice.com` |
| Phone | `+966 57 013 1122` |
| CR | `#7053130576` |
| Primary theme | **Gold Premium** — bg `#0D0800`, gold `#E8C860`, pale gold `#FFF0A0`, accent `#C8A030` |
| Light theme | bg `#F9F7F3`, navy `#0E3B72`, gold `#B89030` |

## Regenerating assets

All asset generation requires **Pillow** and **numpy** (already installed system-wide):

```bash
# Regenerate ALL brand kit assets (favicons, profile pics, headers, watermarks)
python3 generate_brand_kit.py

# Regenerate official papers (letterhead, business cards, stamp, invoice, envelope)
python3 generate_official.py
```

Both scripts use **absolute paths** hardcoded to `/Users/fahadalmansour/fahad/` — run them from any directory.

Source images they read from:
- `badge_logo.png` — 568×624 RGBA, the primary badge source
- `logo_full.png` — full logo on white bg
- `logo_text.png` — text bands only
- `brand_kit/favicon/favicon-512x512.png` — used as badge input by `generate_official.py`

## Architecture

### Badge geometry (important for any SVG/image work)
- Source: `badge_logo.png` 568×624
- Circle center: `(288, 361)`, radius `244 px`
- Scale factor to 200px SVG radius: `SCALE_B = 200/244 ≈ 0.8197`
- Potrace coordinate transform: outer `translate(badge_tx, badge_ty) scale(SCALE_B)` + inner `translate(0, BH) scale(0.1, -0.1)`

### Transparent badge variants
- `brand_kit/badge_transparent.png` — full 568×624, dark bg removed via numpy threshold
- `brand_kit/badge_circle_transparent.png` — 400×400, cropped to circle, no bg

Dark background removal logic (in both scripts):
```python
brightness = r.astype(int) + g.astype(int) + b.astype(int)
dark_bg = (brightness < 120) & (r > g) & (r > b + 5)  # warm dark = bg
data[dark_bg, 3] = 0
```

### Website (`fahad-almansour.com/index.html`)
Single self-contained HTML file (~1.8 MB) — no build step, no dependencies.

- **Light mode is the hard default** — the JS never reads `localStorage` on load; it only writes when the user toggles. Remove the `localStorage.setItem` call too if persistence is unwanted entirely.
- Dark mode toggle: `data-theme="dark"` on `<html>`, toggled by `#themeBtn`.
- Badge is embedded as a `data:image/png;base64,...` URI (from `badge_circle_transparent.png`) — no external image URLs.
- All layout via CSS custom properties (`--navy`, `--gold`, `--bg`, etc.) that swap between themes.
- To update the badge in the website, re-run the Python base64 embed — do not manually edit the ~360 KB data URI string.

### `generate_official.py` — what each function produces
| Function | Output file | Size |
|----------|-------------|------|
| `make_stamp(ink, suffix)` | `stamp-{suffix}.png` | 900×900 transparent PNG |
| `make_letterhead()` | `letterhead-a4-dark.png` | 1240×1754 @ 150 DPI |
| `make_letterhead_light()` | `letterhead-a4.png` | 1240×1754 @ 150 DPI (primary) |
| `make_business_card()` | `business-card-{front,back}-dark.png` | 1050×600 @ 300 DPI |
| `make_business_card_light()` | `business-card-{front,back}.png` | 1050×600 @ 300 DPI (primary) |
| `make_invoice_header()` | `invoice-template.png` | 1240×1754 @ 150 DPI |
| `make_envelope()` | `envelope-dl.png` | 2598×1299 @ 300 DPI |

Light variants are the **primary** files (no suffix). Dark variants have `-dark` suffix.

### Fonts used (macOS system paths)
```
~/Library/Fonts/NotoNaskhArabic-VariableFont_wght.ttf   ← Arabic body
/System/Library/Fonts/Supplemental/Arial Bold.ttf
/System/Library/Fonts/Supplemental/Arial.ttf
/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf
```

## Updating domain / contact info

Domain and contact details appear in five places — update all together:
1. `generate_official.py` — string literals in layout functions
2. `generate_brand_kit.py` — if referenced
3. `brand_kit/email/email_template.html` — use `sed -i '' 's/old/new/g'`
4. `brand_kit/email/email_signature.html` — same
5. `fahad-almansour.com/index.html` — Python script rebuilds the whole file with new values
6. `README.md` — Business Information table

After editing `generate_official.py`, run it to regenerate all PNG assets.

### `wp-theme/fahadalmansouroffice/` — live WordPress theme

Active theme deployed to `~/fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice/` on the VPS (`fsalmansour@162.254.39.146:21098`). It serves the live homepage at `https://fahadalmansouroffice.com/`. Classic PHP template hierarchy — no FSE, no `theme.json`-driven templates.

```
wp-theme/fahadalmansouroffice/
├── style.css                # theme header (NOT the stylesheet)
├── functions.php            # require_once each inc/* file
├── header.php / footer.php  # bilingual EN+AR shell
├── front-page.php           # 5-section landing port (hero/services/about/contact)
├── page.php / single.php / index.php / 404.php / searchform.php / comments.php
├── inc/
│   ├── theme-supports.php   # title-tag, post-thumbnails, custom-logo, woocommerce, HPOS-compat
│   ├── enqueue.php          # theme.css, theme.js, Google Fonts, favicons, early-paint theme boot
│   ├── menus.php            # primary + footer nav locations + fallback
│   ├── customizer.php       # phone / email / CR / address fields → fa_office_setting()
│   ├── contact-form.php     # admin-post.php handler with nonce + honeypot, wp_mail() to info@…
│   ├── icons.php            # fa_office_icon() / fa_office_the_icon() — 13 unique SVGs
│   └── i18n.php             # fa_office_ar() / fa_office_ar_h() / fa_office_ar_p() Arabic wrappers
├── assets/{css,js,img}/     # theme.css, theme.js, brand kit logos+favicons (copied from ../Brand kit/)
└── woocommerce/             # archive-product.php + single-product.php wrappers (cart/checkout/my-account use WC core templates; CSS-harmonized only)
```

Palette tokens in `assets/css/theme.css` come from the brand kit: `#0B2A4A` sapphire, `#0E3658` sapphire-2, `#C8A45C` champagne, `#F0DFB0` champagne-pale, `#8C6E2D` antique, `#FBF8F2` pearl, `#F5EFDF` pearl-warm, `#0F1419` ink. Fonts: Inter + Playfair Display + Noto Naskh Arabic + Amiri.

Deploying changes: `rsync -avz -e 'ssh -p 21098' wp-theme/fahadalmansouroffice/ fsalmansour@162.254.39.146:fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice/`. Then `chmod 755` for new directories, `644` for new files (the VPS umask is restrictive). Activate with `wp theme activate fahadalmansouroffice` from the docroot.

## Conventions

- **Never reply in Arabic in the CLI** — RTL breaks the terminal. Arabic content goes inside files only.
- `brand_kit/official/` light = primary name, dark = `-dark` suffix. Do not invert this.
- The interactive SVG files (`fahad_almansour_logo_gold.html`, `fahad_logo_variants.html`) are self-contained — no server needed, open directly in a browser.
- `fahad-almansour.com/` is a git submodule (has its own `.git`). Commit website changes inside that directory separately, then update the submodule pointer in the parent repo.
