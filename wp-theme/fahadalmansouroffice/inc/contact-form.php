<?php
/**
 * Contact form handler — replaces the static page's mailto: form.
 *
 * Posts to admin-post.php with action=fa_office_contact.
 *  - nonce verified
 *  - honeypot field (`fa_office_company`) must be empty
 *  - inputs sanitized
 *  - delivered via wp_mail() to the Customizer-configured contact email
 *  - redirects back to the referring page with ?contact=ok|err|spam
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function fa_office_contact_handler() {
	$referer = wp_get_referer() ? wp_get_referer() : home_url( '/' );

	if ( ! isset( $_POST['fa_office_nonce'] ) || ! wp_verify_nonce( wp_unslash( $_POST['fa_office_nonce'] ), 'fa_office_contact' ) ) {
		wp_safe_redirect( add_query_arg( 'contact', 'err', $referer ) . '#contact' );
		exit;
	}

	// Honeypot — bots fill every field they see.
	if ( ! empty( $_POST['fa_office_company'] ) ) {
		wp_safe_redirect( add_query_arg( 'contact', 'spam', $referer ) . '#contact' );
		exit;
	}

	$name    = isset( $_POST['name'] )  ? sanitize_text_field( wp_unslash( $_POST['name'] ) )  : '';
	$email   = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) )      : '';
	$message = isset( $_POST['body'] )  ? sanitize_textarea_field( wp_unslash( $_POST['body'] ) ) : '';

	if ( '' === $name || ! is_email( $email ) || '' === $message ) {
		wp_safe_redirect( add_query_arg( 'contact', 'err', $referer ) . '#contact' );
		exit;
	}

	$to        = fa_office_setting( 'fa_office_email' );
	$site_name = wp_specialchars_decode( get_bloginfo( 'name' ), ENT_QUOTES );
	$subject   = sprintf(
		/* translators: 1: visitor name. */
		__( '[%1$s] New contact form message from %2$s', 'fahadalmansouroffice' ),
		$site_name,
		$name
	);

	$body  = sprintf( "Name:    %s\n", $name );
	$body .= sprintf( "Email:   %s\n", $email );
	$body .= sprintf( "Date:    %s\n", current_time( 'mysql' ) );
	$body .= sprintf( "IP:      %s\n", isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '' );
	$body .= "\nMessage:\n";
	$body .= wp_kses_post( $message );

	$headers = array(
		'Reply-To: ' . sprintf( '%s <%s>', $name, $email ),
	);

	$sent = wp_mail( $to, $subject, $body, $headers );

	wp_safe_redirect( add_query_arg( 'contact', $sent ? 'ok' : 'err', $referer ) . '#contact' );
	exit;
}
add_action( 'admin_post_fa_office_contact',         'fa_office_contact_handler' );
add_action( 'admin_post_nopriv_fa_office_contact',  'fa_office_contact_handler' );
