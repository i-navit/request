document.addEventListener('DOMContentLoaded', function () {
    const displayCount = 5;
    const posts = Array.from(document.querySelectorAll('.post-item'));
    const loadMoreBtn = document.getElementById('js-load-more-btn');
    const loadMoreContainer = document.getElementById('js-load-more-container');

    let currentVisibleCount = displayCount;

    function updatePosts() {
        posts.forEach((post, index) => {
            if (index < currentVisibleCount) {
                post.classList.remove('is-hidden');
            } else {
                post.classList.add('is-hidden');
            }
        });

        if (currentVisibleCount < posts.length) {
            loadMoreContainer.style.display = 'block';
        } else {
            loadMoreContainer.style.display = 'none';
        }
    }

    loadMoreBtn.addEventListener('click', function () {
        currentVisibleCount += displayCount;
        updatePosts();
    });

    updatePosts();
});