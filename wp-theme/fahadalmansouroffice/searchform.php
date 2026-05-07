<?php
/**
 * Search form.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<form role="search" method="get" class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
	<label class="screen-reader-text" for="s"><?php esc_html_e( 'Search:', 'fahadalmansouroffice' ); ?></label>
	<input type="search" id="s" class="search-field" placeholder="<?php esc_attr_e( 'Search…', 'fahadalmansouroffice' ); ?>" value="<?php echo esc_attr( get_search_query() ); ?>" name="s" />
	<button type="submit" class="search-submit btn btn-primary"><?php esc_html_e( 'Search', 'fahadalmansouroffice' ); ?></button>
</form>
