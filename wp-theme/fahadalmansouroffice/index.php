<?php
/**
 * Fallback template / blog index.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<div class="page-shell">
	<div class="container">
		<?php if ( have_posts() ) : ?>
			<header class="section-head">
				<h1><?php is_home() ? single_post_title() : the_archive_title(); ?></h1>
				<?php
				$desc = get_the_archive_description();
				if ( ! empty( $desc ) ) {
					echo '<p>' . wp_kses_post( $desc ) . '</p>';
				}
				?>
				<div class="gold-bar"></div>
			</header>

			<?php
			while ( have_posts() ) :
				the_post();
				?>
				<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
					<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
					<div class="entry-meta"><?php echo esc_html( get_the_date() ); ?></div>
					<div class="entry-summary"><?php the_excerpt(); ?></div>
				</article>
			<?php endwhile; ?>

			<?php
			the_posts_pagination(
				array(
					'prev_text' => esc_html__( 'Previous', 'fahadalmansouroffice' ),
					'next_text' => esc_html__( 'Next',     'fahadalmansouroffice' ),
				)
			);
			?>

		<?php else : ?>
			<h1><?php esc_html_e( 'Nothing found', 'fahadalmansouroffice' ); ?></h1>
			<p><?php esc_html_e( 'Sorry, nothing matched. Try the homepage or search.', 'fahadalmansouroffice' ); ?></p>
			<?php get_search_form(); ?>
		<?php endif; ?>
	</div>
</div>

<?php
get_footer();
