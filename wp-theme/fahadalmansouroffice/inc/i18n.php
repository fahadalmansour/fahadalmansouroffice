<?php
/**
 * Bilingual helpers — wrappers around the .ar / .ar-h / .ar-p hooks defined
 * in assets/css/theme.css.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Inline Arabic span. Use for prose.
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar( $ar ) {
	return '<span class="ar" lang="ar" dir="rtl">' . esc_html( $ar ) . '</span>';
}

/**
 * Heading-variant Arabic block. Use as a sibling to <h1>/<h2>/<h3>.
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar_h( $ar ) {
	return '<div class="ar-h" lang="ar" dir="rtl">' . esc_html( $ar ) . '</div>';
}

/**
 * Paragraph-variant Arabic block. Use as a sibling to <p>.
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar_p( $ar ) {
	return '<p class="ar-p" lang="ar" dir="rtl">' . esc_html( $ar ) . '</p>';
}

/**
 * Hero/name-card variant. Use as a sibling to a brand <h1>.
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar_name( $ar ) {
	return '<span class="ar-name" lang="ar" dir="rtl">' . esc_html( $ar ) . '</span>';
}

/**
 * H3-equivalent Arabic title. Use in footer/banner blocks where the
 * Arabic name stands alone (no English sibling).
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar_title( $ar ) {
	return '<h3 class="ar-title" lang="ar" dir="rtl">' . esc_html( $ar ) . '</h3>';
}

/**
 * Country/region block. Use inside contact rows for an RTL place name
 * displayed under an English address line.
 *
 * @param string $ar Arabic text.
 * @return string
 */
function fa_office_ar_country( $ar ) {
	return '<span class="ar-country" lang="ar" dir="rtl">' . esc_html( $ar ) . '</span>';
}
