// --- サイトメニュー ---
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



/**
 * メールアドレスコピー機能
 */
function handleEmailCopy() {
    const btn = document.getElementById('emailCopyBtn');

    // 1. メアドをその場で組み立てる（ボット対策）
    const part1 = "bottin";
    const part2 = "gaido";
    const domain = "gmail.com";
    const fullEmail = part1 + "." + part2 + "@" + domain;

    // 2. クリップボードにコピー
    // navigator.clipboard が使えない環境への対策として従来の方法も考慮
    const copyToClipboard = (text) => {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        } else {
            // フォールバック（iFrame内などで動作を安定させるため）
            const textArea = document.createElement("textarea");
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
            } catch (err) {
                console.error('Copy failed', err);
            }
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    };

    copyToClipboard(fullEmail).then(() => {
        // 3. UIの変更
        const originalText = "メールアドレスをコピーする";
        btn.textContent = "📄 コピーしました！";
        btn.classList.add('success'); // ピンクにするクラスを追加
        btn.disabled = true; // 連打防止

        // 4. 2秒後に元の状態に戻す
        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('success');
            btn.disabled = false;
        }, 2000);
    });
}
