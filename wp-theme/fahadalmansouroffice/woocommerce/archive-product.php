<?php
/**
 * Product archive — wraps WooCommerce's archive content in this theme's
 * container/typography. The shop loop, breadcrumbs, sorting, etc. continue
 * to come from the WooCommerce templates and hooks.
 *
 * @package fahadalmansouroffice
 */

defined( 'ABSPATH' ) || exit;

get_header( 'shop' );
?>

<div class="page-shell woocommerce-archive">
	<div class="container">
		<header class="section-head">
			<h1><?php woocommerce_page_title(); ?></h1>
			<div class="gold-bar"></div>
		</header>

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
		?>

		<?php if ( woocommerce_product_loop() ) : ?>
			<?php
			do_action( 'woocommerce_before_shop_loop' );
			woocommerce_product_loop_start();

			if ( wc_get_loop_prop( 'total' ) ) {
				while ( have_posts() ) {
					the_post();
					do_action( 'woocommerce_shop_loop' );
					wc_get_template_part( 'content', 'product' );
				}
			}

			woocommerce_product_loop_end();
			do_action( 'woocommerce_after_shop_loop' );
			?>
		<?php else : ?>
			<?php do_action( 'woocommerce_no_products_found' ); ?>
		<?php endif; ?>

		<?php do_action( 'woocommerce_after_main_content' ); ?>
	</div>
</div>

<?php
get_footer( 'shop' );
