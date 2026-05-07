<?php
/**
 * Site header.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?><!doctype html>
<html <?php language_attributes(); ?> data-theme="light">
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<meta name="description" content="<?php echo esc_attr__( 'Fahad Saad Fahad Almansour Office for Electronic Services & E-Commerce. Saudi establishment, Commercial Registration #7053130576.', 'fahadalmansouroffice' ); ?>" />
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="skip-link screen-reader-text" href="#site-content"><?php esc_html_e( 'Skip to content', 'fahadalmansouroffice' ); ?></a>

<nav role="navigation" aria-label="<?php esc_attr_e( 'Primary', 'fahadalmansouroffice' ); ?>">
	<div class="nav-inner">
		<a class="nav-brand" href="<?php echo esc_url( home_url( '/' ) ); ?>">
			<img src="<?php echo esc_url( FA_OFFICE_URI . '/assets/img/logo-primary.svg' ); ?>" alt="<?php esc_attr_e( 'Fahad Almansour Office logo', 'fahadalmansouroffice' ); ?>" />
			<span>
				<?php echo esc_html( get_bloginfo( 'name' ) ); ?>
				<span class="sub"><?php esc_html_e( 'Electronic Services & E-Commerce', 'fahadalmansouroffice' ); ?></span>
			</span>
		</a>

		<?php
		if ( has_nav_menu( 'primary' ) ) {
			wp_nav_menu(
				array(
					'theme_location'  => 'primary',
					'container'       => false,
					'menu_class'      => 'nav-links',
					'menu_id'         => 'navLinks',
					'fallback_cb'     => 'fa_office_primary_nav_fallback',
					'items_wrap'      => '<ul id="%1$s" class="%2$s">%3$s</ul>',
				)
			);
		} else {
			fa_office_primary_nav_fallback();
		}
		?>

		<div style="display:flex;align-items:center;gap:10px;">
			<button class="theme-btn" id="themeBtn" type="button" aria-label="<?php esc_attr_e( 'Toggle dark mode', 'fahadalmansouroffice' ); ?>">
				<?php fa_office_the_icon( 'moon', array( 'id' => 'themeIco' ) ); ?>
				<span id="themeTxt"><?php esc_html_e( 'Dark', 'fahadalmansouroffice' ); ?></span>
			</button>
			<button class="hamburger" id="hamburger" type="button" aria-label="<?php esc_attr_e( 'Menu', 'fahadalmansouroffice' ); ?>" aria-expanded="false" aria-controls="navLinks">
				<span></span><span></span><span></span>
			</button>
		</div>
	</div>
</nav>

<main id="site-content">
