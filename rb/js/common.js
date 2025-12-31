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


function copyEmail() {
    // アドレスをその場で組み立てる（ボット対策）
    const u = "bottin.gaido";
    const d = "gmail.com";
    const fullEmail = u + "@" + d;

    // クリップボードへコピー
    const tempInput = document.createElement("input");
    tempInput.value = fullEmail;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    // UIのフィードバック
    const btnText = document.getElementById('btn-text');
    const copyMsg = document.getElementById('copy-msg');

    const originalText = btnText.innerText;
    btnText.innerText = "完了!";
    copyMsg.classList.remove('hidden');

    setTimeout(() => {
        btnText.innerText = originalText;
        copyMsg.classList.add('hidden');
    }, 2000);
}




let copyTimeout;

function copyEmail() {
    const u = "bottin.gaido";
    const d = "gmail.com";
    const fullEmail = u + "@" + d;

    // navigator.clipboard が使える場合はそれを使用し、失敗した場合は execCommand にフォールバックする
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(fullEmail).then(() => {
            updateButtonUI();
        }).catch(() => {
            fallbackCopy(fullEmail);
        });
    } else {
        fallbackCopy(fullEmail);
    }
}

function fallbackCopy(text) {
    const tempInput = document.createElement("input");
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    try {
        document.execCommand("copy");
        updateButtonUI();
    } catch (err) {
        console.error("Copy failed", err);
    }
    document.body.removeChild(tempInput);
}

function updateButtonUI() {
    const btnText = document.getElementById('btn-text');
    const btn = document.getElementById('copy-btn');

    if (copyTimeout) clearTimeout(copyTimeout);

    const originalText = "コピー";
    btnText.innerText = "完了";

    btn.classList.replace('bg-white', 'bg-yellow-400');
    btn.classList.replace('hover:bg-slate-50', 'hover:bg-yellow-500');
    btn.classList.replace('border-slate-300', 'border-yellow-500');

    copyTimeout = setTimeout(() => {
        btnText.innerText = originalText;
        btn.classList.replace('bg-yellow-400', 'bg-white');
        btn.classList.replace('hover:bg-yellow-500', 'hover:bg-slate-50');
        btn.classList.replace('border-yellow-500', 'border-slate-300');
    }, 5000);
}