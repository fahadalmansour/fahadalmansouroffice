<?php
/**
 * Site footer.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$fa_email      = fa_office_setting( 'fa_office_email' );
$fa_phone      = fa_office_setting( 'fa_office_phone' );
$fa_phone_e164 = fa_office_setting( 'fa_office_phone_e164' );
$fa_cr         = fa_office_setting( 'fa_office_cr' );
$fa_address    = fa_office_setting( 'fa_office_address' );
$current_year  = date_i18n( 'Y' );
?>
</main><!-- #site-content -->

<footer role="contentinfo">
	<img class="footer-logo" src="<?php echo esc_url( FA_OFFICE_URI . '/assets/img/logo-mono-sapphire-512.png' ); ?>" alt="" />
	<h3>مكتب فهد سعد فهد المنصور للخدمات الإلكترونية</h3>
	<div class="fen"><?php esc_html_e( 'Fahad Saad Fahad Almansour — Office For Electronic Services', 'fahadalmansouroffice' ); ?></div>

	<div class="flinks">
		<a href="<?php echo esc_url( home_url( '/' ) ); ?>">
			<?php fa_office_the_icon( 'globe' ); ?>
			<?php echo esc_html( wp_parse_url( home_url(), PHP_URL_HOST ) ); ?>
		</a>
		<a href="mailto:<?php echo esc_attr( $fa_email ); ?>">
			<?php fa_office_the_icon( 'mail' ); ?>
			<?php echo esc_html( $fa_email ); ?>
		</a>
		<a href="tel:<?php echo esc_attr( $fa_phone_e164 ); ?>">
			<?php fa_office_the_icon( 'phone' ); ?>
			<?php echo esc_html( $fa_phone ); ?>
		</a>
	</div>

	<div class="fbar"></div>

	<div class="copy">
		<?php
		printf(
			/* translators: 1: CR number, 2: address, 3: current year. */
			esc_html__( 'CR #%1$s · %2$s · © %3$s Fahad Saad Fahad Almansour', 'fahadalmansouroffice' ),
			esc_html( $fa_cr ),
			esc_html( $fa_address ),
			esc_html( $current_year )
		);
		?>
		<br />
		<?php
		printf(
			/* translators: %s: current year. */
			esc_html__( 'جميع الحقوق محفوظة © %s — مكتب فهد سعد فهد المنصور للخدمات الإلكترونية', 'fahadalmansouroffice' ),
			esc_html( $current_year )
		);
		?>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
