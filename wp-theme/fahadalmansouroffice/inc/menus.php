<?php
/**
 * Nav menu locations.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'after_setup_theme',
	function () {
		register_nav_menus(
			array(
				'primary' => __( 'Primary navigation', 'fahadalmansouroffice' ),
				'footer'  => __( 'Footer links',       'fahadalmansouroffice' ),
			)
		);
	}
);

/**
 * Default primary-nav fallback that mirrors the static landing page when the
 * site editor hasn't built a menu yet.
 */
function fa_office_primary_nav_fallback() {
	?>
	<ul class="nav-links" id="navLinks">
		<li><a href="#home"><?php esc_html_e( 'Home',     'fahadalmansouroffice' ); ?></a></li>
		<li><a href="#services"><?php esc_html_e( 'Services', 'fahadalmansouroffice' ); ?></a></li>
		<li><a href="#about"><?php esc_html_e( 'About',    'fahadalmansouroffice' ); ?></a></li>
		<li><a href="#contact"><?php esc_html_e( 'Contact',  'fahadalmansouroffice' ); ?></a></li>
	</ul>
	<?php
}
