<?php
/**
 * Front-end and editor asset enqueues.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'wp_enqueue_scripts',
	function () {
		// Brand kit fonts: Inter (body), Playfair Display (display headings),
		// Noto Naskh Arabic + Amiri (Arabic headings/body).
		wp_enqueue_style(
			'fa-office-fonts',
			'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@500;600;700;800;900&family=Noto+Naskh+Arabic:wght@400;500;600;700&family=Amiri:wght@400;700&display=swap',
			array(),
			null
		);

		wp_enqueue_style(
			'fa-office-theme',
			FA_OFFICE_URI . '/assets/css/theme.css',
			array( 'fa-office-fonts' ),
			FA_OFFICE_VERSION
		);

		wp_enqueue_script(
			'fa-office-theme',
			FA_OFFICE_URI . '/assets/js/theme.js',
			array(),
			FA_OFFICE_VERSION,
			true
		);

		// Inline boot script — applies the persisted theme + prefers-color-scheme
		// before paint to avoid a flash of light theme on dark-mode reload.
		$boot = "(function(){try{var t=localStorage.getItem('theme');"
			. "if(!t&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches){t='dark';}"
			. "if(t){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();";
		wp_add_inline_script( 'fa-office-theme', $boot, 'before' );

		if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
			wp_enqueue_script( 'comment-reply' );
		}
	}
);

/**
 * Add favicons + Apple touch icon directly so they don't depend on Customizer setup.
 */
add_action(
	'wp_head',
	function () {
		$base = FA_OFFICE_URI . '/assets/img';
		printf( '<link rel="icon" type="image/x-icon" href="%s/favicon.ico" />' . "\n", esc_url( $base ) );
		printf( '<link rel="icon" type="image/png" sizes="192x192" href="%s/favicon-192.png" />' . "\n", esc_url( $base ) );
		printf( '<link rel="icon" type="image/png" sizes="512x512" href="%s/favicon-512.png" />' . "\n", esc_url( $base ) );
		printf( '<link rel="apple-touch-icon" sizes="192x192" href="%s/favicon-192.png" />' . "\n", esc_url( $base ) );
	},
	5
);
