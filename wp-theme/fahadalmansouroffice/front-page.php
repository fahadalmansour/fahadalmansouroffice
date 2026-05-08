<?php
/**
 * Front page — the office landing.
 *
 * Ports the original static index.html body (lines 361–565) into PHP-rendered
 * sections, with the brand kit assets and Customizer-driven contact fields.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$fa_email      = fa_office_setting( 'fa_office_email' );
$fa_phone      = fa_office_setting( 'fa_office_phone' );
$fa_phone_e164 = fa_office_setting( 'fa_office_phone_e164' );
$fa_cr         = fa_office_setting( 'fa_office_cr' );
$fa_address    = fa_office_setting( 'fa_office_address' );

// Read contact-form status (set by inc/contact-form.php).
$contact_status = isset( $_GET['contact'] ) ? sanitize_key( wp_unslash( $_GET['contact'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended
?>

<!-- Hero -->
<section id="home" class="hero">
	<img class="hero-logo" src="<?php echo esc_url( FA_OFFICE_URI . '/assets/img/logo-primary.svg' ); ?>" alt="<?php esc_attr_e( 'Fahad Almansour Office logo', 'fahadalmansouroffice' ); ?>" />
	<h1>Fahad Saad Fahad Almansour</h1>
	<?php echo fa_office_ar_name( 'مكتب فهد سعد فهد المنصور' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
	<p class="tagline">
		<?php esc_html_e( 'Office For Electronic Services & E-Commerce', 'fahadalmansouroffice' ); ?>
		<?php echo fa_office_ar( 'للخدمات الإلكترونية والتجارة الإلكترونية' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
	</p>
	<div class="cta-row">
		<a class="btn btn-primary" href="#services">
			<?php fa_office_the_icon( 'menu' ); ?>
			<?php esc_html_e( 'Our Services', 'fahadalmansouroffice' ); ?>
		</a>
		<a class="btn btn-outline" href="#contact">
			<?php fa_office_the_icon( 'phone' ); ?>
			<?php esc_html_e( 'Contact Us', 'fahadalmansouroffice' ); ?>
		</a>
	</div>
</section>

<!-- Services -->
<section id="services" class="alt">
	<div class="container">
		<div class="section-head">
			<h2><?php esc_html_e( 'What We Offer', 'fahadalmansouroffice' ); ?></h2>
			<?php echo fa_office_ar( 'ماذا نقدم' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
			<div class="gold-bar"></div>
		</div>
		<div class="cards">
			<article class="card">
				<div class="card-icon"><?php fa_office_the_icon( 'monitor' ); ?></div>
				<h3><?php esc_html_e( 'Electronic Services', 'fahadalmansouroffice' ); ?></h3>
				<?php echo fa_office_ar_h( 'الخدمات الإلكترونية' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
				<p><?php esc_html_e( 'Digital solutions including system setup, e-government services, and IT consultancy for individuals and businesses.', 'fahadalmansouroffice' ); ?></p>
			</article>
			<article class="card">
				<div class="card-icon"><?php fa_office_the_icon( 'cart' ); ?></div>
				<h3><?php esc_html_e( 'E-Commerce Solutions', 'fahadalmansouroffice' ); ?></h3>
				<?php echo fa_office_ar_h( 'حلول التجارة الإلكترونية' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
				<p><?php esc_html_e( 'Online store setup, product management, payment integration, and full e-commerce lifecycle support.', 'fahadalmansouroffice' ); ?></p>
			</article>
			<article class="card">
				<div class="card-icon"><?php fa_office_the_icon( 'info' ); ?></div>
				<h3><?php esc_html_e( 'Digital Consulting', 'fahadalmansouroffice' ); ?></h3>
				<?php echo fa_office_ar_h( 'الاستشارات الرقمية' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
				<p><?php esc_html_e( 'Strategic guidance for digital transformation, online presence, and business automation for the Saudi market.', 'fahadalmansouroffice' ); ?></p>
			</article>
		</div>
	</div>
</section>

<!-- About -->
<section id="about">
	<div class="container">
		<div class="about-grid">
			<div class="about-logo-wrap">
				<img class="about-logo" src="<?php echo esc_url( FA_OFFICE_URI . '/assets/img/logo-primary-512.png' ); ?>" alt="<?php esc_attr_e( 'Office logo badge', 'fahadalmansouroffice' ); ?>" />
				<div class="est"><?php esc_html_e( 'Established · Saudi Arabia', 'fahadalmansouroffice' ); ?></div>
			</div>
			<div class="about-text">
				<h2><?php esc_html_e( 'About the Office', 'fahadalmansouroffice' ); ?></h2>
				<?php echo fa_office_ar_h( 'عن المكتب' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
				<p><?php esc_html_e( 'Fahad Saad Fahad Almansour Office for Electronic Services is a Saudi establishment specialising in digital and electronic services, e-commerce, and technology consultancy.', 'fahadalmansouroffice' ); ?></p>
				<?php echo fa_office_ar_p( 'مكتب فهد سعد فهد المنصور للخدمات الإلكترونية مؤسسة سعودية متخصصة في الخدمات الرقمية والإلكترونية والتجارة الإلكترونية والاستشارات التقنية.' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
				<div class="tags">
					<span class="tag">
						<?php fa_office_the_icon( 'doc' ); ?>
						<?php
						printf(
							/* translators: %s: CR number. */
							esc_html__( 'CR #%s', 'fahadalmansouroffice' ),
							'<strong>' . esc_html( $fa_cr ) . '</strong>' // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
						);
						?>
					</span>
					<span class="tag">
						<?php fa_office_the_icon( 'globe' ); ?>
						<?php echo esc_html( wp_parse_url( home_url(), PHP_URL_HOST ) ); ?>
					</span>
					<span class="tag">
						<?php fa_office_the_icon( 'pin' ); ?>
						<?php echo esc_html( $fa_address ); ?>
					</span>
					<span class="tag">
						<?php fa_office_the_icon( 'phone' ); ?>
						<?php echo esc_html( $fa_phone ); ?>
					</span>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- Contact -->
<section id="contact" class="alt">
	<div class="container">
		<div class="section-head">
			<h2><?php esc_html_e( 'Get In Touch', 'fahadalmansouroffice' ); ?></h2>
			<?php echo fa_office_ar( 'تواصل معنا' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
			<div class="gold-bar"></div>
		</div>
		<div class="contact-grid">
			<div class="contact-info">
				<h3><?php esc_html_e( 'Contact Details', 'fahadalmansouroffice' ); ?></h3>

				<div class="ci">
					<div class="ci-icon"><?php fa_office_the_icon( 'globe' ); ?></div>
					<div>
						<div class="ci-label"><?php esc_html_e( 'Website', 'fahadalmansouroffice' ); ?></div>
						<div class="ci-val"><a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php echo esc_html( wp_parse_url( home_url(), PHP_URL_HOST ) ); ?></a></div>
					</div>
				</div>

				<div class="ci">
					<div class="ci-icon"><?php fa_office_the_icon( 'mail' ); ?></div>
					<div>
						<div class="ci-label"><?php esc_html_e( 'Email', 'fahadalmansouroffice' ); ?></div>
						<div class="ci-val"><a href="mailto:<?php echo esc_attr( $fa_email ); ?>"><?php echo esc_html( $fa_email ); ?></a></div>
					</div>
				</div>

				<div class="ci">
					<div class="ci-icon"><?php fa_office_the_icon( 'phone' ); ?></div>
					<div>
						<div class="ci-label"><?php esc_html_e( 'Phone & WhatsApp', 'fahadalmansouroffice' ); ?></div>
						<div class="ci-val"><a href="tel:<?php echo esc_attr( $fa_phone_e164 ); ?>"><?php echo esc_html( $fa_phone ); ?></a></div>
					</div>
				</div>

				<div class="ci">
					<div class="ci-icon"><?php fa_office_the_icon( 'pin' ); ?></div>
					<div>
						<div class="ci-label"><?php esc_html_e( 'Location', 'fahadalmansouroffice' ); ?></div>
						<div class="ci-val">
							<?php echo esc_html( $fa_address ); ?>
							<br />
							<?php echo fa_office_ar_country( 'المملكة العربية السعودية' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- helper escapes. ?>
						</div>
					</div>
				</div>

				<div class="ci">
					<div class="ci-icon"><?php fa_office_the_icon( 'doc-lines' ); ?></div>
					<div>
						<div class="ci-label"><?php esc_html_e( 'Commercial Registration', 'fahadalmansouroffice' ); ?></div>
						<div class="ci-val">CR #<?php echo esc_html( $fa_cr ); ?></div>
					</div>
				</div>
			</div>

			<div class="contact-form">
				<h3><?php esc_html_e( 'Send a Message', 'fahadalmansouroffice' ); ?></h3>

				<?php if ( 'ok' === $contact_status ) : ?>
					<div class="contact-status ok" role="status"><?php esc_html_e( 'Thanks — your message has been sent. We\'ll be in touch shortly.', 'fahadalmansouroffice' ); ?></div>
				<?php elseif ( 'err' === $contact_status ) : ?>
					<div class="contact-status err" role="alert"><?php esc_html_e( 'Sorry, the message could not be sent. Please check the fields and try again, or email us directly.', 'fahadalmansouroffice' ); ?></div>
				<?php endif; ?>

				<form action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" method="post" novalidate>
					<input type="hidden" name="action" value="fa_office_contact" />
					<?php wp_nonce_field( 'fa_office_contact', 'fa_office_nonce' ); ?>

					<div class="honeypot" aria-hidden="true">
						<label for="fa_office_company"><?php esc_html_e( 'Company (leave blank)', 'fahadalmansouroffice' ); ?></label>
						<input type="text" id="fa_office_company" name="fa_office_company" tabindex="-1" autocomplete="off" />
					</div>

					<div class="fg">
						<label for="cname"><?php esc_html_e( 'Name', 'fahadalmansouroffice' ); ?></label>
						<input type="text" id="cname" name="name" placeholder="<?php esc_attr_e( 'Your full name', 'fahadalmansouroffice' ); ?>" required />
					</div>
					<div class="fg">
						<label for="cemail"><?php esc_html_e( 'Email', 'fahadalmansouroffice' ); ?></label>
						<input type="email" id="cemail" name="email" placeholder="<?php echo esc_attr( $fa_email ); ?>" required />
					</div>
					<div class="fg">
						<label for="cmsg"><?php esc_html_e( 'Message', 'fahadalmansouroffice' ); ?></label>
						<textarea id="cmsg" name="body" placeholder="<?php esc_attr_e( 'How can we help you?', 'fahadalmansouroffice' ); ?>" required></textarea>
					</div>
					<button type="submit" class="submit">
						<?php fa_office_the_icon( 'send' ); ?>
						<?php esc_html_e( 'Send Message', 'fahadalmansouroffice' ); ?>
					</button>
				</form>
			</div>
		</div>
	</div>
</section>

<?php
get_footer();
