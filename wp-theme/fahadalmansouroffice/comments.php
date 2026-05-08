<?php
/**
 * Comments template — minimal stub.
 *
 * @package fahadalmansouroffice
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( post_password_required() ) {
	return;
}
?>

<section id="comments" class="comments-area">
	<?php if ( have_comments() ) : ?>
		<h2 class="comments-title">
			<?php
			$count = get_comments_number();
			printf(
				/* translators: %s: comment count. */
				esc_html( _n( '%s comment', '%s comments', $count, 'fahadalmansouroffice' ) ),
				esc_html( number_format_i18n( $count ) )
			);
			?>
		</h2>

		<ol class="comment-list">
			<?php
			wp_list_comments(
				array(
					'style'      => 'ol',
					'short_ping' => true,
				)
			);
			?>
		</ol>

		<?php
		the_comments_pagination(
			array(
				'prev_text' => esc_html__( 'Older comments', 'fahadalmansouroffice' ),
				'next_text' => esc_html__( 'Newer comments', 'fahadalmansouroffice' ),
			)
		);
		?>
	<?php endif; ?>

	<?php if ( ! comments_open() && get_comments_number() && post_type_supports( get_post_type(), 'comments' ) ) : ?>
		<p class="no-comments"><?php esc_html_e( 'Comments are closed.', 'fahadalmansouroffice' ); ?></p>
	<?php endif; ?>

	<?php
	comment_form(
		array(
			'class_form' => 'comment-form fa-office-form',
		)
	);
	?>
</section>
