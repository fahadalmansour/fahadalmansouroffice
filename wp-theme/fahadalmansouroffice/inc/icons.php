<?php
/**
 * Inline SVG icons.
 *
 * Ports the icon set used on the original static landing page. All icons share
 * a 24x24 viewBox and rely on currentColor + the .btn / .card-icon / .ci-icon
 * / .tag / .flinks styling to control fill / stroke. Glyphs that contained
 * stroked-only paths in the source (e.g. `M4 6h16M4 10h16…`) keep that visual
 * by being rendered with stroke=currentColor and fill=none — see the markup
 * builder below.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Catalogue of the 13 unique glyphs the design uses (some appear in multiple
 * spots — `phone`, `globe`, etc.).
 *
 * Each value is the inner SVG markup. Glyph type ('fill' or 'stroke') is
 * encoded so the wrapper can apply the right rendering hint.
 *
 * @return array<string, array{type:string, paths:string}>
 */
function fa_office_icon_set() {
	return array(
		'moon'      => array(
			'type'  => 'fill',
			'paths' => '<path d="M21 12.79A9 9 0 1111.21 3a7 7 0 109.79 9.79z"/>',
		),
		'sun'       => array(
			'type'  => 'stroke',
			'paths' => '<path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/><circle cx="12" cy="12" r="5"/>',
		),
		'menu'      => array(
			'type'  => 'stroke',
			'paths' => '<path d="M4 6h16M4 10h16M4 14h16M4 18h16"/>',
		),
		'phone'     => array(
			'type'  => 'fill',
			'paths' => '<path d="M22 16.92v3a2 2 0 01-2.18 2 19.8 19.8 0 01-8.63-3.07A19.5 19.5 0 013.07 9.67 19.8 19.8 0 01.08 1.05 2 2 0 012.05 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>',
		),
		'monitor'   => array(
			'type'  => 'stroke',
			'paths' => '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
		),
		'cart'      => array(
			'type'  => 'stroke',
			'paths' => '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 001.95-1.57l1.65-8.43H6"/>',
		),
		'info'      => array(
			'type'  => 'stroke',
			'paths' => '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
		),
		'doc'       => array(
			'type'  => 'stroke',
			'paths' => '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>',
		),
		'doc-lines' => array(
			'type'  => 'stroke',
			'paths' => '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
		),
		'globe'     => array(
			'type'  => 'stroke',
			'paths' => '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20"/>',
		),
		'pin'       => array(
			'type'  => 'stroke',
			'paths' => '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>',
		),
		'mail'      => array(
			'type'  => 'stroke',
			'paths' => '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
		),
		'send'      => array(
			'type'  => 'fill',
			'paths' => '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
		),
	);
}

/**
 * Render an icon by name.
 *
 * @param string $name  Glyph key — see fa_office_icon_set().
 * @param array  $args  Optional. Keys: id, class, title, hidden (bool), size.
 * @return string SVG markup, or empty string if the name isn't known.
 */
function fa_office_icon( $name, $args = array() ) {
	$set = fa_office_icon_set();
	if ( ! isset( $set[ $name ] ) ) {
		return '';
	}

	$args = wp_parse_args(
		$args,
		array(
			'id'     => '',
			'class'  => '',
			'title'  => '',
			'hidden' => true,
			'size'   => '',
		)
	);

	$icon = $set[ $name ];

	$attrs = ' viewBox="0 0 24 24"';
	if ( '' !== $args['id'] ) {
		$attrs .= ' id="' . esc_attr( $args['id'] ) . '"';
	}
	if ( '' !== $args['class'] ) {
		$attrs .= ' class="' . esc_attr( $args['class'] ) . '"';
	}
	if ( '' !== $args['size'] ) {
		$attrs .= ' width="' . esc_attr( $args['size'] ) . '" height="' . esc_attr( $args['size'] ) . '"';
	}

	if ( 'stroke' === $icon['type'] ) {
		$attrs .= ' fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';
	} else {
		$attrs .= ' fill="currentColor"';
	}

	if ( $args['hidden'] && '' === $args['title'] ) {
		$attrs .= ' aria-hidden="true" focusable="false"';
	} elseif ( '' !== $args['title'] ) {
		$attrs .= ' role="img" aria-label="' . esc_attr( $args['title'] ) . '"';
	}

	$inner = $icon['paths'];
	if ( '' !== $args['title'] && ! $args['hidden'] ) {
		$inner = '<title>' . esc_html( $args['title'] ) . '</title>' . $inner;
	}

	return '<svg' . $attrs . '>' . $inner . '</svg>';
}

/**
 * Echo helper.
 *
 * @param string $name Glyph key.
 * @param array  $args Optional render args.
 */
function fa_office_the_icon( $name, $args = array() ) {
	echo fa_office_icon( $name, $args ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped — internal builder, all attrs already escaped.
}
