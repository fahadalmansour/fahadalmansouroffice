<?php
/**
 * 404 template — branded, reuses the hero shell.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<section class="hero">
	<img class="hero-logo" src="<?php echo esc_url( FA_OFFICE_URI . '/assets/img/logo-mono-sapphire-512.png' ); ?>" alt="" />
	<h1>404</h1>
	<span class="ar-name">صفحة غير موجودة</span>
	<p class="tagline">
		<?php esc_html_e( 'The page you were looking for has moved or no longer exists.', 'fahadalmansouroffice' ); ?>
		<span class="ar">الصفحة التي تبحث عنها غير موجودة أو تم نقلها.</span>
	</p>
	<div class="cta-row">
		<a class="btn btn-primary" href="<?php echo esc_url( home_url( '/' ) ); ?>">
			<?php fa_office_the_icon( 'menu' ); ?>
			<?php esc_html_e( 'Back to homepage', 'fahadalmansouroffice' ); ?>
		</a>
		<a class="btn btn-outline" href="<?php echo esc_url( home_url( '/#contact' ) ); ?>">
			<?php fa_office_the_icon( 'mail' ); ?>
			<?php esc_html_e( 'Contact the office', 'fahadalmansouroffice' ); ?>
		</a>
	</div>
</section>

<?php
get_footer();
