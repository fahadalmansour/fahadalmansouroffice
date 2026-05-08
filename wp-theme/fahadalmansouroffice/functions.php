<?php
/**
 * Fahad Almansour Office theme bootstrap.
 *
 * Loads each concern from inc/ to keep this file readable.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( 'FA_OFFICE_VERSION' ) ) {
	define( 'FA_OFFICE_VERSION', '1.0.0' );
}
if ( ! defined( 'FA_OFFICE_DIR' ) ) {
	define( 'FA_OFFICE_DIR', get_template_directory() );
}
if ( ! defined( 'FA_OFFICE_URI' ) ) {
	define( 'FA_OFFICE_URI', get_template_directory_uri() );
}

require_once FA_OFFICE_DIR . '/inc/theme-supports.php';
require_once FA_OFFICE_DIR . '/inc/enqueue.php';
require_once FA_OFFICE_DIR . '/inc/menus.php';
require_once FA_OFFICE_DIR . '/inc/customizer.php';
require_once FA_OFFICE_DIR . '/inc/contact-form.php';
require_once FA_OFFICE_DIR . '/inc/icons.php';
require_once FA_OFFICE_DIR . '/inc/i18n.php';
