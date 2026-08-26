=== SRLINES wCRM Contact Form ===
Contributors: srlines
Tags: contact form, crm, wcrm, shortcode
Requires at least: 6.4
Tested up to: 7.1
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

A lightweight, theme-friendly shortcode form connected to an external wCRM form ID.

== Description ==

SRLINES wCRM Contact Form adds a responsive contact form without bundling images, fonts, or other binary assets. The form inherits typography and WordPress global colour presets from the active theme. The plugin's settings screen displays the SRLINES logo directly from https://srlines.net/logo.png.

== Installation ==

1. Upload the `contact-form-widget` directory to `/wp-content/plugins/` or install a ZIP containing that directory.
2. Activate “SRLINES wCRM Contact Form” in Plugins.
3. Open Settings > wCRM Contact Form and enter the external form ID supplied by wCRM.
4. Add `[srlines_contact_form]` to a page, post, or shortcode-capable widget.

Optional shortcode attributes:

`[srlines_contact_form title="Request a quote" description="Tell us about your project."]`

== Frequently Asked Questions ==

= Where are submissions sent? =

The official widget loaded from `https://crm.srlines.net/form-widget.js` sends the form to the wCRM form ID saved in Settings.

= Does the plugin contain tracking code? =

No. On pages containing the shortcode, it loads the wCRM form widget required to submit the form. The settings screen loads the externally hosted SRLINES logo.

= How can I adjust the accent colour? =

The form first uses the active block theme's Primary or Accent 1 preset. A theme can explicitly set `--srlines-form-accent` on the form or an ancestor.

== Changelog ==

= 1.0.0 =

* Initial release.
