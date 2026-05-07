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
