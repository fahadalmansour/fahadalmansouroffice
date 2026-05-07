# fahadalmansouroffice

Source for **fahadalmansouroffice.com** — Fahad Saad Fahad Almansour Office for Electronic Services & E-Commerce (مكتب فهد سعد فهد المنصور للخدمات الإلكترونية), CR #7053130576.

## What's in here

- **`wp-theme/fahadalmansouroffice/`** — the active WordPress classic-PHP theme deployed to `~/fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice/` on the VPS. Bilingual EN/AR, sapphire/champagne brand-kit palette, WooCommerce-ready.
- **`Brand kit/`** — logos (SVG + PNG), brand pattern, favicons, and the brand documentation page (also published at `https://fahadalmansouroffice.com/brand-kit/`).
- **`index.html`** — legacy single-file static landing page kept for archival reference.
- **`generate_brand_kit.py`** / **`generate_official.py`** — Pillow + numpy scripts that regenerate brand assets and official papers (letterhead, business cards, stamps, invoice, envelope).
- **`fahad-almansour.com/`** — older personal-site directory.
- **`CLAUDE.md`** — guidance for Claude Code sessions.

## Deploying the theme

```sh
rsync -avz -e 'ssh -p 21098' \
  wp-theme/fahadalmansouroffice/ \
  fsalmansour@162.254.39.146:fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice/

ssh -p 21098 fsalmansour@162.254.39.146 \
  'find ~/fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice -type d -exec chmod 755 {} + && \
   find ~/fahadalmansouroffice.com/wp-content/themes/fahadalmansouroffice -type f -exec chmod 644 {} + && \
   cd ~/fahadalmansouroffice.com && wp theme activate fahadalmansouroffice'
```

The VPS has a restrictive umask, so the chmod step is required after every rsync.
