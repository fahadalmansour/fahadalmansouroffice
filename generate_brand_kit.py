#!/usr/bin/env python3
"""
Brand kit generator for Fahad Almansour.
Generates favicons, profile pictures, headers, and watermarks
using Pillow from the source PNG assets.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw

# Paths
BASE_DIR = "/Users/fahadalmansour/fahad"
BRAND_KIT_DIR = os.path.join(BASE_DIR, "brand_kit")

SOURCE_BADGE = os.path.join(BASE_DIR, "badge_logo.png")
SOURCE_FULL = os.path.join(BASE_DIR, "logo_full.png")
SOURCE_TEXT = os.path.join(BASE_DIR, "logo_text.png")
BADGE_TRANSPARENT = "/tmp/badge_transparent.png"
FULL_TRANSPARENT = "/tmp/full_transparent.png"
TEXT_TRANSPARENT = "/tmp/text_transparent.png"

# Gold Premium colour scheme
COLOR_DARK_BG = (13, 8, 0)         # #0D0800
COLOR_GOLD = (232, 200, 96)         # #E8C860
COLOR_PALE_GOLD = (255, 240, 160)   # #FFF0A0
COLOR_CARD_BORDER = (90, 58, 0)     # #5A3A00

# ──────────────────────────────────────────────────────────────────────────────
# Helper: make directories
# ──────────────────────────────────────────────────────────────────────────────
def makedirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# Step 0 — Remove white background from a PNG
# ──────────────────────────────────────────────────────────────────────────────
def remove_white_bg(img: Image.Image, threshold: int = 230) -> Image.Image:
    """Make pixels where R>threshold & G>threshold & B>threshold transparent."""
    img = img.convert("RGBA")
    data = np.array(img)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    mask = (r > threshold) & (g > threshold) & (b > threshold)
    data[:, :, 3] = np.where(mask, 0, a)
    return Image.fromarray(data, "RGBA")


def prepare_transparent_assets():
    """Load all source PNGs, remove white bg, save to /tmp."""
    print("Step 0 — Preparing transparent base assets …")

    badge = Image.open(SOURCE_BADGE).convert("RGBA")
    badge_t = remove_white_bg(badge, threshold=230)
    badge_t.save(BADGE_TRANSPARENT)
    print(f"  Saved {BADGE_TRANSPARENT}")

    full = Image.open(SOURCE_FULL).convert("RGBA")
    full_t = remove_white_bg(full, threshold=235)
    full_t.save(FULL_TRANSPARENT)
    print(f"  Saved {FULL_TRANSPARENT}")

    text = Image.open(SOURCE_TEXT).convert("RGBA")
    text_t = remove_white_bg(text, threshold=230)
    text_t.save(TEXT_TRANSPARENT)
    print(f"  Saved {TEXT_TRANSPARENT}")

    return badge_t, full_t, text_t


# ──────────────────────────────────────────────────────────────────────────────
# Helper: create square with badge centered + padding
# ──────────────────────────────────────────────────────────────────────────────
def make_square_with_badge(badge_img: Image.Image, size: int, padding_frac: float = 0.10) -> Image.Image:
    """Create a square canvas (dark bg) with badge centered and padded."""
    canvas = Image.new("RGBA", (size, size), (*COLOR_DARK_BG, 255))
    # Available space after padding
    avail = int(size * (1 - 2 * padding_frac))
    bw, bh = badge_img.size
    # Scale badge to fit in avail×avail preserving aspect ratio
    scale = min(avail / bw, avail / bh)
    new_w = int(bw * scale)
    new_h = int(bh * scale)
    resized = badge_img.resize((new_w, new_h), Image.LANCZOS)
    x = (size - new_w) // 2
    y = (size - new_h) // 2
    canvas.paste(resized, (x, y), resized)
    return canvas


# ──────────────────────────────────────────────────────────────────────────────
# Step 1 — Favicons
# ──────────────────────────────────────────────────────────────────────────────
def generate_favicons(badge_img: Image.Image):
    print("\nStep 1 — Generating favicons …")
    favicon_dir = os.path.join(BRAND_KIT_DIR, "favicon")
    makedirs(favicon_dir)

    sizes = [16, 32, 48, 64, 128, 180, 192, 512]
    size_names = {
        16: "favicon-16x16.png",
        32: "favicon-32x32.png",
        48: "favicon-48x48.png",
        64: "favicon-64x64.png",
        128: "favicon-128x128.png",
        180: "favicon-180x180.png",
        192: "favicon-192x192.png",
        512: "favicon-512x512.png",
    }

    favicon_images = {}
    for s in sizes:
        img = make_square_with_badge(badge_img, s, padding_frac=0.10)
        fname = size_names[s]
        out_path = os.path.join(favicon_dir, fname)
        img.convert("RGBA").save(out_path, "PNG")
        favicon_images[s] = img
        print(f"  Saved {fname}")

    # favicon.ico — multi-size ICO containing 16, 32, 48
    ico_path = os.path.join(favicon_dir, "favicon.ico")
    # PIL needs RGB or P mode for ICO; use RGBA which PIL handles
    ico_images = [favicon_images[s].convert("RGBA") for s in [16, 32, 48]]
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=ico_images[1:],
    )
    print(f"  Saved favicon.ico (16/32/48)")


# ──────────────────────────────────────────────────────────────────────────────
# Step 2 — Social media profile pictures
# ──────────────────────────────────────────────────────────────────────────────
def generate_profiles(badge_img: Image.Image):
    print("\nStep 2 — Generating social media profile pictures …")
    profile_dir = os.path.join(BRAND_KIT_DIR, "profile")
    makedirs(profile_dir)

    profiles = [
        ("profile-twitter-400x400.png", 400),
        ("profile-instagram-320x320.png", 320),
        ("profile-facebook-170x170.png", 170),
        ("profile-linkedin-400x400.png", 400),
        ("profile-youtube-800x800.png", 800),
        ("profile-whatsapp-640x640.png", 640),
        ("profile-snapchat-320x320.png", 320),
        ("profile-tiktok-200x200.png", 200),
    ]

    for fname, size in profiles:
        img = make_square_with_badge(badge_img, size, padding_frac=0.08)
        out_path = os.path.join(profile_dir, fname)
        img.convert("RGBA").save(out_path, "PNG")
        print(f"  Saved {fname}")


# ──────────────────────────────────────────────────────────────────────────────
# Helper: add radial glow to a canvas
# ──────────────────────────────────────────────────────────────────────────────
def add_radial_glow(canvas: Image.Image) -> Image.Image:
    """Draw a subtle warm glow in the centre of the canvas."""
    w, h = canvas.size
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    cx, cy = w // 2, h // 2
    # Number of concentric ellipses from large to small
    steps = 30
    for i in range(steps):
        frac = 1.0 - i / steps  # 1.0 at outermost, 0 at innermost
        rx = int(cx * 0.9 * frac)
        ry = int(cy * 0.9 * frac)
        # Alpha increases towards centre
        alpha = int(20 * (1 - frac))  # max 20 at centre
        col = (26, 15, 0, alpha)  # #1A0F00 with low alpha
        bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
        draw.ellipse(bbox, fill=col)
    return Image.alpha_composite(canvas.convert("RGBA"), glow_layer)


def add_gold_lines(canvas: Image.Image) -> Image.Image:
    """Add thin decorative gold horizontal lines near top and bottom."""
    w, h = canvas.size
    draw = ImageDraw.Draw(canvas)
    y_top = max(1, int(h * 0.04))
    y_bot = min(h - 2, int(h * 0.96))
    gold_col = (*COLOR_GOLD, 180)
    draw.line([(0, y_top), (w, y_top)], fill=gold_col, width=1)
    draw.line([(0, y_bot), (w, y_bot)], fill=gold_col, width=1)
    return canvas


def make_header(full_logo: Image.Image, width: int, height: int,
                logo_height_frac: float = 0.80,
                safe_zone: tuple = None) -> Image.Image:
    """
    Create a header image.
    full_logo: transparent full logo PNG.
    safe_zone: (sw, sh) if we need to constrain logo to a centre safe area.
    """
    canvas = Image.new("RGBA", (width, height), (*COLOR_DARK_BG, 255))
    canvas = add_radial_glow(canvas)

    lw, lh = full_logo.size

    if safe_zone:
        # Constrain to safe zone dimensions
        max_w, max_h = safe_zone
    else:
        max_w = int(width * 0.90)
        max_h = int(height * logo_height_frac)

    # Scale logo preserving aspect ratio
    scale = min(max_w / lw, max_h / lh)
    new_w = int(lw * scale)
    new_h = int(lh * scale)
    resized = full_logo.resize((new_w, new_h), Image.LANCZOS)

    # Centre on canvas
    x = (width - new_w) // 2
    y = (height - new_h) // 2
    canvas.paste(resized, (x, y), resized)

    canvas = add_gold_lines(canvas)
    return canvas


# ──────────────────────────────────────────────────────────────────────────────
# Step 3 — Social media headers / covers
# ──────────────────────────────────────────────────────────────────────────────
def generate_headers(full_logo: Image.Image):
    print("\nStep 3 — Generating social media headers …")
    headers_dir = os.path.join(BRAND_KIT_DIR, "headers")
    makedirs(headers_dir)

    headers = [
        ("header-twitter-1500x500.png", 1500, 500, None),
        ("header-facebook-820x312.png", 820, 312, None),
        ("header-linkedin-1584x396.png", 1584, 396, None),
        # YouTube: safe zone is 1546×423 centred in 2560×1440
        ("header-youtube-2560x1440.png", 2560, 1440, (1546, 423)),
        ("header-linkedin-company-1128x191.png", 1128, 191, None),
    ]

    for fname, w, h, safe_zone in headers:
        img = make_header(full_logo, w, h, logo_height_frac=0.80, safe_zone=safe_zone)
        out_path = os.path.join(headers_dir, fname)
        img.convert("RGBA").save(out_path, "PNG")
        print(f"  Saved {fname}")


# ──────────────────────────────────────────────────────────────────────────────
# Helper: apply opacity to an RGBA image
# ──────────────────────────────────────────────────────────────────────────────
def apply_opacity(img: Image.Image, opacity: float) -> Image.Image:
    """Multiply alpha channel by opacity fraction (0..1)."""
    img = img.convert("RGBA")
    data = np.array(img, dtype=np.float32)
    data[:, :, 3] = data[:, :, 3] * opacity
    data = np.clip(data, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGBA")


def resize_to_width(img: Image.Image, target_width: int) -> Image.Image:
    """Resize image proportionally to target width."""
    w, h = img.size
    scale = target_width / w
    return img.resize((target_width, int(h * scale)), Image.LANCZOS)


# ──────────────────────────────────────────────────────────────────────────────
# Step 4 — Watermarks
# ──────────────────────────────────────────────────────────────────────────────
def generate_watermarks(badge_img: Image.Image, full_img: Image.Image, text_img: Image.Image):
    print("\nStep 4 — Generating watermarks …")
    wm_dir = os.path.join(BRAND_KIT_DIR, "watermarks")
    makedirs(wm_dir)

    # ── watermark-badge-dark-30.png ──
    # Badge on transparent bg at 30% opacity (for overlay on light content)
    wm = apply_opacity(badge_img.copy(), 0.30)
    wm.save(os.path.join(wm_dir, "watermark-badge-dark-30.png"), "PNG")
    print("  Saved watermark-badge-dark-30.png")

    # ── watermark-badge-light-30.png ──
    # Badge with white fill, transparent bg, 30% opacity (for dark content)
    badge_light = badge_img.convert("RGBA").copy()
    data = np.array(badge_light)
    # Where alpha > 0 (visible pixels), recolour to white
    mask = data[:, :, 3] > 10
    data[mask, 0] = 255
    data[mask, 1] = 255
    data[mask, 2] = 255
    badge_light = Image.fromarray(data, "RGBA")
    wm_light = apply_opacity(badge_light, 0.30)
    wm_light.save(os.path.join(wm_dir, "watermark-badge-light-30.png"), "PNG")
    print("  Saved watermark-badge-light-30.png")

    # ── watermark-badge-gold-50.png ──
    # Badge gold on transparent bg at 50% opacity
    badge_gold = badge_img.convert("RGBA").copy()
    data = np.array(badge_gold)
    mask = data[:, :, 3] > 10
    data[mask, 0] = COLOR_GOLD[0]
    data[mask, 1] = COLOR_GOLD[1]
    data[mask, 2] = COLOR_GOLD[2]
    badge_gold = Image.fromarray(data, "RGBA")
    wm_gold = apply_opacity(badge_gold, 0.50)
    wm_gold.save(os.path.join(wm_dir, "watermark-badge-gold-50.png"), "PNG")
    print("  Saved watermark-badge-gold-50.png")

    # ── watermark-text-dark-25.png ──
    # Text-only logo 800px wide at 25% opacity
    text_800 = resize_to_width(text_img.copy(), 800)
    wm_text = apply_opacity(text_800, 0.25)
    wm_text.save(os.path.join(wm_dir, "watermark-text-dark-25.png"), "PNG")
    print("  Saved watermark-text-dark-25.png")

    # ── watermark-full-30.png ──
    # Full logo 600px wide at 30% opacity
    full_600 = resize_to_width(full_img.copy(), 600)
    wm_full = apply_opacity(full_600, 0.30)
    wm_full.save(os.path.join(wm_dir, "watermark-full-30.png"), "PNG")
    print("  Saved watermark-full-30.png")


# ──────────────────────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────────────────────
def print_summary():
    print("\n" + "=" * 60)
    print("Brand kit generation complete!")
    print("=" * 60)

    total_files = 0
    total_bytes = 0

    for root, dirs, files in os.walk(BRAND_KIT_DIR):
        dirs.sort()
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            size = os.path.getsize(fpath)
            rel = os.path.relpath(fpath, BASE_DIR)
            print(f"  {rel}  ({size:,} bytes)")
            total_files += 1
            total_bytes += size

    print(f"\nTotal: {total_files} files, {total_bytes:,} bytes ({total_bytes / 1024 / 1024:.1f} MB)")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print("Fahad Almansour Brand Kit Generator")
    print("=" * 60)

    # Create output directories
    makedirs(
        os.path.join(BRAND_KIT_DIR, "favicon"),
        os.path.join(BRAND_KIT_DIR, "profile"),
        os.path.join(BRAND_KIT_DIR, "headers"),
        os.path.join(BRAND_KIT_DIR, "watermarks"),
    )

    # Step 0 — Prepare transparent base assets
    badge_t, full_t, text_t = prepare_transparent_assets()

    # Step 1 — Favicons
    generate_favicons(badge_t)

    # Step 2 — Profile pictures
    generate_profiles(badge_t)

    # Step 3 — Headers
    generate_headers(full_t)

    # Step 4 — Watermarks
    generate_watermarks(badge_t, full_t, text_t)

    # Summary
    print_summary()


if __name__ == "__main__":
    main()
