document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('.js-load-more-wrapper');

    containers.forEach(wrapper => {
        // 件数設定を取得
        const displayCount = parseInt(wrapper.getAttribute('data-display-count')) || 5;
        const posts = Array.from(wrapper.querySelectorAll('.post-item'));
        const loadMoreBtn = wrapper.querySelector('.js-load-more-btn');
        const loadMoreContainer = wrapper.querySelector('.js-load-more-container');
        // 数字を書き換えるターゲットを追加
        const countDisplay = wrapper.querySelector('.js-next-count');

        let currentVisibleCount = displayCount;

        function updatePosts() {
            posts.forEach((post, index) => {
                if (index < currentVisibleCount) {
                    post.classList.remove('is-hidden');
                } else {
                    post.classList.add('is-hidden');
                }
            });

            // 残りの件数を計算
            const remaining = posts.length - currentVisibleCount;

            if (loadMoreContainer) {
                if (remaining > 0) {
                    loadMoreContainer.style.display = 'block';
                    // ★ここでボタンの中の数字を書き換えています
                    if (countDisplay) {
                        countDisplay.textContent = Math.min(displayCount, remaining);
                    }
                } else {
                    loadMoreContainer.style.display = 'none';
                }
            }
        }

        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', function (e) {
                e.preventDefault();
                currentVisibleCount += displayCount;
                updatePosts();
            });
        }

        updatePosts();
    });
});