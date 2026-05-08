<?php
/**
 * Single post template.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<div class="page-shell">
		<div class="container">
			<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
				<header class="section-head">
					<h1><?php the_title(); ?></h1>
					<div class="entry-meta">
						<time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date() ); ?></time>
					</div>
					<div class="gold-bar"></div>
				</header>

				<?php if ( has_post_thumbnail() ) : ?>
					<div class="entry-thumb"><?php the_post_thumbnail( 'large' ); ?></div>
				<?php endif; ?>

				<div class="entry-content">
					<?php the_content(); ?>
				</div>

				<footer class="entry-footer">
					<?php
					the_tags(
						'<div class="entry-tags">' . esc_html__( 'Tags:', 'fahadalmansouroffice' ) . ' ',
						', ',
						'</div>'
					);
					?>
				</footer>
			</article>

			<nav class="post-nav" aria-label="<?php esc_attr_e( 'Post navigation', 'fahadalmansouroffice' ); ?>">
				<?php
				previous_post_link(
					'%link',
					/* translators: %title is the previous post title. */
					'<span aria-hidden="true">&laquo;</span> ' . esc_html__( '%title', 'fahadalmansouroffice' )
				);
				next_post_link(
					'%link',
					/* translators: %title is the next post title. */
					esc_html__( '%title', 'fahadalmansouroffice' ) . ' <span aria-hidden="true">&raquo;</span>'
				);
				?>
			</nav>

			<?php
			if ( comments_open() || get_comments_number() ) {
				comments_template();
			}
			?>
		</div>
	</div>
	<?php
endwhile;

get_footer();
