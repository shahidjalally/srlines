<?php
/**
 * Removes plugin data when the plugin is deleted in WordPress.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

delete_option( 'srlines_wcrm_form_id' );

