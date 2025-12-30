/* 修正後の common.js */

window.addEventListener('load', function () {
    // --- 1. メニューの制御 ---
    const btn = document.getElementById('js-menu-toggle');
    const memo = document.getElementById('js-menu-memo');

    if (btn && memo) {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            memo.classList.toggle('is-open');
        });

        document.addEventListener('click', (e) => {
            if (!memo.contains(e.target)) {
                memo.classList.remove('is-open');
            }
        });
    }

    // --- 2. トップへ戻るボタンの出現・消滅 ---
    const pageTopBtn = document.getElementById('js-pagetop');

    if (pageTopBtn) {
        window.addEventListener('scroll', function () {
            // 現在のスクロール量を取得
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

            if (currentScroll > 200) { // 200px以上スクロールしたら
                pageTopBtn.classList.add('is-show');
            } else {
                pageTopBtn.classList.remove('is-show');
            }
        });

        // --- 3. クリックでスムーズスクロール ---
        const topLink = pageTopBtn.querySelector('a');
        if (topLink) {
            topLink.addEventListener('click', (e) => {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }
    }
});