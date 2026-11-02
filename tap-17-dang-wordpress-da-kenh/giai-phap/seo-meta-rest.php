<?php
/**
 * Plugin Name: SEO meta qua REST API (video Tự động hóa với Claude)
 * Description: Cho phép REST API ghi tiêu đề SEO, mô tả và từ khóa chính của Yoast SEO. Đặt file vào wp-content/mu-plugins/.
 *
 * Mặc định các meta bắt đầu bằng dấu gạch dưới (như _yoast_wpseo_metadesc) bị ẩn khỏi REST API.
 * Đoạn này đăng ký chúng với show_in_rest và chỉ cho người có quyền sửa bài được ghi.
 * Dùng RankMath thì thay bằng: rank_math_title, rank_math_description, rank_math_focus_keyword.
 */
add_action('init', function () {
    foreach (['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw'] as $khoa) {
        register_post_meta('post', $khoa, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () { return current_user_can('edit_posts'); },
        ]);
    }
});
