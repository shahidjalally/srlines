<?php
/**
 * Plugin Name:       SRLINES wCRM Contact Form
 * Plugin URI:        https://srlines.net/
 * Description:       Adds a theme-friendly contact form that sends submissions to a configured wCRM form.
 * Version:           1.0.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            SRLINES
 * Author URI:        https://srlines.net/
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       srlines-contact-form
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'SRLINES_CONTACT_FORM_VERSION', '1.0.0' );
define( 'SRLINES_CONTACT_FORM_OPTION', 'srlines_wcrm_form_id' );

/**
 * Registers the public stylesheet only when the shortcode is rendered.
 */
function srlines_contact_form_register_assets() {
	wp_register_style(
		'srlines-contact-form',
		plugins_url( 'assets/contact-form.css', __FILE__ ),
		array(),
		SRLINES_CONTACT_FORM_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'srlines_contact_form_register_assets' );

/**
 * Limits a wCRM form ID to the characters used by wCRM identifiers.
 *
 * @param string $value Unsanitized option value.
 * @return string
 */
function srlines_contact_form_sanitize_id( $value ) {
	$value = is_string( $value ) ? trim( $value ) : '';

	return preg_replace( '/[^A-Za-z0-9_-]/', '', $value );
}

/**
 * Adds the plugin settings page.
 */
function srlines_contact_form_admin_menu() {
	add_options_page(
		__( 'wCRM Contact Form', 'srlines-contact-form' ),
		__( 'wCRM Contact Form', 'srlines-contact-form' ),
		'manage_options',
		'srlines-contact-form',
		'srlines_contact_form_settings_page'
	);
}
add_action( 'admin_menu', 'srlines_contact_form_admin_menu' );

/**
 * Registers the wCRM form ID setting.
 */
function srlines_contact_form_register_settings() {
	register_setting(
		'srlines_contact_form_settings',
		SRLINES_CONTACT_FORM_OPTION,
		array(
			'type'              => 'string',
			'sanitize_callback' => 'srlines_contact_form_sanitize_id',
			'default'           => '',
		)
	);

	add_settings_section(
		'srlines_contact_form_main',
		__( 'wCRM connection', 'srlines-contact-form' ),
		'__return_false',
		'srlines-contact-form'
	);

	add_settings_field(
		SRLINES_CONTACT_FORM_OPTION,
		__( 'External form ID', 'srlines-contact-form' ),
		'srlines_contact_form_id_field',
		'srlines-contact-form',
		'srlines_contact_form_main'
	);
}
add_action( 'admin_init', 'srlines_contact_form_register_settings' );

/**
 * Renders the form ID settings field.
 */
function srlines_contact_form_id_field() {
	$value = get_option( SRLINES_CONTACT_FORM_OPTION, '' );
	?>
	<input class="regular-text" id="<?php echo esc_attr( SRLINES_CONTACT_FORM_OPTION ); ?>" name="<?php echo esc_attr( SRLINES_CONTACT_FORM_OPTION ); ?>" type="text" value="<?php echo esc_attr( $value ); ?>" placeholder="wf_xxxxxxxxxxxxxxxxxxxxxxxx" autocomplete="off">
	<p class="description"><?php esc_html_e( 'Paste the form ID supplied by wCRM. It normally begins with “wf_”.', 'srlines-contact-form' ); ?></p>
	<?php
}

/**
 * Renders the Settings screen.
 */
function srlines_contact_form_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	?>
	<div class="wrap">
		<div style="display:flex;align-items:center;gap:14px;margin-top:18px">
			<img src="https://srlines.net/logo.png" alt="SRLINES" width="52" height="52" style="object-fit:contain">
			<h1><?php esc_html_e( 'SRLINES wCRM Contact Form', 'srlines-contact-form' ); ?></h1>
		</div>
		<p><?php esc_html_e( 'Connect this website to a wCRM external form, then place the shortcode wherever the contact form should appear.', 'srlines-contact-form' ); ?></p>
		<form action="options.php" method="post">
			<?php
			settings_fields( 'srlines_contact_form_settings' );
			do_settings_sections( 'srlines-contact-form' );
			submit_button();
			?>
		</form>
		<h2><?php esc_html_e( 'Shortcode', 'srlines-contact-form' ); ?></h2>
		<p><code>[srlines_contact_form]</code></p>
		<p><?php esc_html_e( 'Optional: change the heading and introductory copy with the title and description attributes.', 'srlines-contact-form' ); ?></p>
		<p><code>[srlines_contact_form title="Request a quote" description="Tell us about your project."]</code></p>
	</div>
	<?php
}

/**
 * Renders a contact form and connects it to the wCRM widget.
 *
 * @param array $attributes Shortcode attributes.
 * @return string
 */
function srlines_contact_form_shortcode( $attributes = array() ) {
	$form_id = get_option( SRLINES_CONTACT_FORM_OPTION, '' );

	if ( '' === $form_id ) {
		if ( current_user_can( 'manage_options' ) ) {
			return '<p class="srlines-contact-form__notice">' . wp_kses_post( sprintf( __( 'Set the wCRM form ID in <a href="%s">Settings → wCRM Contact Form</a>.', 'srlines-contact-form' ), esc_url( admin_url( 'options-general.php?page=srlines-contact-form' ) ) ) ) . '</p>';
		}

		return '';
	}

	$attributes = shortcode_atts(
		array(
			'title'       => __( 'Contact us', 'srlines-contact-form' ),
			'description' => __( 'Tell us how we can help and our team will get back to you.', 'srlines-contact-form' ),
		),
		$attributes,
		'srlines_contact_form'
	);

	wp_enqueue_style( 'srlines-contact-form' );

	$instance = wp_unique_id( 'srlines-contact-form-' );
	$heading  = $instance . '-heading';

	ob_start();
	?>
	<section class="srlines-contact-form" aria-labelledby="<?php echo esc_attr( $heading ); ?>">
		<div class="srlines-contact-form__inner">
			<h2 id="<?php echo esc_attr( $heading ); ?>"><?php echo esc_html( $attributes['title'] ); ?></h2>
			<p class="srlines-contact-form__intro"><?php echo esc_html( $attributes['description'] ); ?></p>
			<form id="<?php echo esc_attr( $instance ); ?>">
				<label><?php esc_html_e( 'Name', 'srlines-contact-form' ); ?><input name="name" type="text" autocomplete="name" required></label>
				<label><?php esc_html_e( 'Email', 'srlines-contact-form' ); ?><input name="email" type="email" autocomplete="email" required></label>
				<label><?php esc_html_e( 'Phone', 'srlines-contact-form' ); ?><input name="phone" type="tel" autocomplete="tel" required></label>
				<label><?php esc_html_e( 'Company', 'srlines-contact-form' ); ?><input name="company" type="text" autocomplete="organization"></label>
				<label class="srlines-contact-form__full"><?php esc_html_e( 'How can we help?', 'srlines-contact-form' ); ?><textarea name="message" rows="5" required></textarea></label>
				<label class="srlines-contact-form__honeypot" aria-hidden="true"><?php esc_html_e( 'Website', 'srlines-contact-form' ); ?><input name="website" type="text" tabindex="-1" autocomplete="off"></label>
				<button class="srlines-contact-form__submit" type="submit"><?php esc_html_e( 'Send message', 'srlines-contact-form' ); ?></button>
				<p class="srlines-contact-form__result" data-wcrm-result aria-live="polite"></p>
			</form>
		</div>
	</section>
	<script src="https://crm.srlines.net/form-widget.js" data-form-id="<?php echo esc_attr( $form_id ); ?>" data-form-selector="#<?php echo esc_attr( $instance ); ?>" async></script>
	<?php

	return ob_get_clean();
}
add_shortcode( 'srlines_contact_form', 'srlines_contact_form_shortcode' );

