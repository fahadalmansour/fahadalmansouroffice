<?php
/**
 * Single product — same wrapper strategy as archive-product.php.
 *
 * @package fahadalmansouroffice
 */

defined( 'ABSPATH' ) || exit;

get_header( 'shop' );
?>

<div class="page-shell woocommerce-single">
	<div class="container">
		<?php
		/**
		 * Hook: woocommerce_before_main_content.
		 *
		 * @hooked woocommerce_output_content_wrapper - 10 (removed below)
		 * @hooked woocommerce_breadcrumb - 20
		 * @hooked WC_Structured_Data::generate_website_data() - 30
		 */
		remove_action( 'woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10 );
		remove_action( 'woocommerce_after_main_content',  'woocommerce_output_content_wrapper_end', 10 );
		do_action( 'woocommerce_before_main_content' );

		while ( have_posts() ) :
			the_post();
			wc_get_template_part( 'content', 'single-product' );
		endwhile;

		do_action( 'woocommerce_after_main_content' );
		?>
	</div>
</div>

<?php
get_footer( 'shop' );
