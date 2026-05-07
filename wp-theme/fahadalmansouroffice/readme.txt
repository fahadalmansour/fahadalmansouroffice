=== Fahad Almansour Office ===
Contributors: fahadalmansour
Tags: classic-theme, custom-colors, custom-logo, custom-menu, featured-images, threaded-comments, translation-ready, woocommerce, rtl-language-support
Requires at least: 6.4
Tested up to: 6.9
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPL-2.0-or-later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Bilingual EN/AR classic PHP theme for fahadalmansouroffice.com.

== Description ==

Custom classic-template-hierarchy theme (header.php / footer.php / front-page.php / page.php / single.php / functions.php / style.css). Designed around the office's brand kit: sapphire (#0B2A4A), champagne (#C8A45C), pearl (#FBF8F2), ink (#0F1419). Display type: Playfair Display + Amiri (Arabic). Body: Inter + Noto Naskh Arabic.

* Front page ports the original static landing (5 sections: hero / services / about / contact / footer).
* Light + dark mode via [data-theme] on <html>, persisted to localStorage 'theme'.
* Contact form posts to admin-post.php with a nonce + honeypot, delivered via wp_mail().
* WooCommerce-aware: theme support declared, archive-product.php and single-product.php wrappers shipped, custom_order_tables (HPOS) compatibility declared. Cart/checkout/my-account are intentionally NOT overridden — WC core templates are used and visual harmony is handled in assets/css/theme.css.

== Customizer ==

Settings → Office contact details: contact email, phone (display + tel:), CR number, address. Front-page output reads these via fa_office_setting().

== Changelog ==

= 1.0.0 =
Initial release. Port of the static index.html design with brand-kit palette, classic PHP template hierarchy, Woo-ready scaffolding.
