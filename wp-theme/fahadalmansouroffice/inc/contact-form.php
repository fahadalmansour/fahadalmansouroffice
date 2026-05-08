<?php
/**
 * Contact form handler — replaces the static page's mailto: form.
 *
 * Posts to admin-post.php with action=fa_office_contact.
 *  - nonce verified (sanitize_key + wp_verify_nonce)
 *  - referer host validated against home_url()
 *  - per-IP rate limit (max 3 sends / 10 min)
 *  - honeypot field (`fa_office_company`) must be empty
 *  - inputs sanitized; CR/LF stripped from header-bound name
 *  - delivered via wp_mail() to the Customizer-configured contact email
 *  - redirects back to the referring page with ?contact=ok|err|spam
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Resolve the visitor IP, preferring Cloudflare's connecting-IP header
 * when present, falling back to REMOTE_ADDR.
 *
 * @since 1.1.0
 * @return string Validated IP address, or '0.0.0.0' on failure.
 */
function fa_office_client_ip() {
	$candidates = array( 'HTTP_CF_CONNECTING_IP', 'HTTP_X_REAL_IP', 'REMOTE_ADDR' );
	foreach ( $candidates as $key ) {
		if ( empty( $_SERVER[ $key ] ) ) {
			continue;
		}
		$ip = sanitize_text_field( wp_unslash( $_SERVER[ $key ] ) );
		if ( filter_var( $ip, FILTER_VALIDATE_IP ) ) {
			return $ip;
		}
	}
	return '0.0.0.0';
}

/**
 * Handle the contact-form POST.
 *
 * @since 1.0.0
 * @return void
 */
function fa_office_contact_handler() {
	// Validate referer host before using it as a redirect target.
	$home_host   = wp_parse_url( home_url(), PHP_URL_HOST );
	$referer_raw = wp_get_referer();
	$ref_host    = $referer_raw ? wp_parse_url( $referer_raw, PHP_URL_HOST ) : '';
	$referer     = ( $referer_raw && $ref_host === $home_host ) ? $referer_raw : home_url( '/' );

	// Nonce: sanitize as key, then verify.
	$nonce = isset( $_POST['fa_office_nonce'] ) ? sanitize_key( wp_unslash( $_POST['fa_office_nonce'] ) ) : '';
	if ( ! wp_verify_nonce( $nonce, 'fa_office_contact' ) ) {
		wp_safe_redirect( add_query_arg( 'contact', 'err', $referer ) . '#contact' );
		exit;
	}

	// Per-IP throttle: 3 submissions per 10 minutes.
	$ip            = fa_office_client_ip();
	$throttle_key  = 'fa_office_contact_' . md5( $ip );
	$throttle_hits = (int) get_transient( $throttle_key );
	if ( $throttle_hits >= 3 ) {
		wp_safe_redirect( add_query_arg( 'contact', 'spam', $referer ) . '#contact' );
		exit;
	}
	set_transient( $throttle_key, $throttle_hits + 1, 10 * MINUTE_IN_SECONDS );

	// Honeypot — bots fill every field they see.
	if ( ! empty( $_POST['fa_office_company'] ) ) {
		wp_safe_redirect( add_query_arg( 'contact', 'spam', $referer ) . '#contact' );
		exit;
	}

	$name    = isset( $_POST['name'] )  ? sanitize_text_field( wp_unslash( $_POST['name'] ) )      : '';
	$email   = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) )          : '';
	$message = isset( $_POST['body'] )  ? sanitize_textarea_field( wp_unslash( $_POST['body'] ) )  : '';

	if ( '' === $name || ! is_email( $email ) || '' === $message ) {
		wp_safe_redirect( add_query_arg( 'contact', 'err', $referer ) . '#contact' );
		exit;
	}

	$to        = fa_office_setting( 'fa_office_email' );
	$site_name = wp_specialchars_decode( get_bloginfo( 'name' ), ENT_QUOTES );
	$subject   = sprintf(
		/* translators: 1: site name, 2: visitor name. */
		__( '[%1$s] New contact form message from %2$s', 'fahadalmansouroffice' ),
		$site_name,
		$name
	);

	$body  = sprintf( "Name:    %s\n", $name );
	$body .= sprintf( "Email:   %s\n", $email );
	$body .= sprintf( "Date:    %s\n", current_time( 'mysql' ) );
	$body .= sprintf( "IP:      %s\n", $ip );
	$body .= "\nMessage:\n";
	$body .= $message;

	// Strip CR/LF from name before injecting into Reply-To, and quote-escape
	// the display name. Pin From: to the on-domain mailbox so SPF/DKIM remain
	// aligned and the visitor address is only ever the Reply-To.
	$safe_name = trim( preg_replace( '/[\r\n\t]+/', ' ', $name ) );
	$headers   = array(
		sprintf( 'From: %s <%s>',       $site_name, $to ),
		sprintf( 'Reply-To: "%s" <%s>', addcslashes( $safe_name, '"\\' ), $email ),
	);

	$sent = wp_mail( $to, $subject, $body, $headers );

	wp_safe_redirect( add_query_arg( 'contact', $sent ? 'ok' : 'err', $referer ) . '#contact' );
	exit;
}
add_action( 'admin_post_fa_office_contact',        'fa_office_contact_handler' );
add_action( 'admin_post_nopriv_fa_office_contact', 'fa_office_contact_handler' );
