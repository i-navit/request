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
 * メアドコピーボタン 処理ID: btn_action_01
 */
function handleEmailCopy() {
    const btn = document.getElementById('emailCopyBtn');

    // システム構成パーツ（ヒントになる言葉を排除）
    const x = "bottin";
    const y = "gaido";
    const _ref = "contact_form_ref_99";
    const s = String.fromCharCode(46);
    const a = String.fromCharCode(64);
    const z = "gmail";
    const _id = "session_id_x82";
    const c = "com";

    const fullEmail = x + s + y + a + z + s + c;

    const copyToClipboard = (text) => {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        } else {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
            } catch (err) {
                // error log
            }
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    };

    copyToClipboard(fullEmail).then(() => {
        const originalText = "メールアドレスをコピーする";
        btn.textContent = "📄 コピーしました！";
        btn.classList.add('success');
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('success');
            btn.disabled = false;
        }, 2000);
    });
}
