<?php
/**
 * Customizer settings — minimal, just the editable contact fields.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'customize_register',
	function ( $wp_customize ) {
		$wp_customize->add_section(
			'fa_office_contact',
			array(
				'title'    => __( 'Office contact details', 'fahadalmansouroffice' ),
				'priority' => 35,
			)
		);

		$fields = array(
			'fa_office_email'    => array(
				'label'     => __( 'Contact email', 'fahadalmansouroffice' ),
				'default'   => 'info@fahadalmansouroffice.com',
				'sanitize'  => 'sanitize_email',
				'type'      => 'email',
			),
			'fa_office_phone'    => array(
				'label'     => __( 'Phone (international format)', 'fahadalmansouroffice' ),
				'default'   => '+966 57 013 1122',
				'sanitize'  => 'sanitize_text_field',
				'type'      => 'text',
			),
			'fa_office_phone_e164' => array(
				'label'     => __( 'Phone for tel: link (digits only, with +)', 'fahadalmansouroffice' ),
				'default'   => '+966570131122',
				'sanitize'  => 'sanitize_text_field',
				'type'      => 'text',
			),
			'fa_office_cr'       => array(
				'label'     => __( 'Commercial Registration #', 'fahadalmansouroffice' ),
				'default'   => '7053130576',
				'sanitize'  => 'sanitize_text_field',
				'type'      => 'text',
			),
			'fa_office_address'  => array(
				'label'     => __( 'Location label', 'fahadalmansouroffice' ),
				'default'   => 'Kingdom of Saudi Arabia',
				'sanitize'  => 'sanitize_text_field',
				'type'      => 'text',
			),
		);

		foreach ( $fields as $id => $cfg ) {
			$wp_customize->add_setting(
				$id,
				array(
					'default'           => $cfg['default'],
					'sanitize_callback' => $cfg['sanitize'],
					'transport'         => 'refresh',
				)
			);
			$wp_customize->add_control(
				$id,
				array(
					'label'   => $cfg['label'],
					'section' => 'fa_office_contact',
					'type'    => $cfg['type'],
				)
			);
		}
	}
);

/**
 * Quick accessor — returns the Customizer value or its default.
 */
function fa_office_setting( $key ) {
	$defaults = array(
		'fa_office_email'      => 'info@fahadalmansouroffice.com',
		'fa_office_phone'      => '+966 57 013 1122',
		'fa_office_phone_e164' => '+966570131122',
		'fa_office_cr'         => '7053130576',
		'fa_office_address'    => 'Kingdom of Saudi Arabia',
	);
	$default = isset( $defaults[ $key ] ) ? $defaults[ $key ] : '';
	return get_theme_mod( $key, $default );
}
