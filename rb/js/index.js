// ファンアートポップアップ - ❌ボタンによる手動終了
(function () {
    const btn = document.getElementById('popup_boxBtn');
    const modal = document.getElementById('popup_boxModal');
    const closeX = document.getElementById('close_popup_box');

    // 閉じる処理
    const hideModal = () => {
        modal.classList.remove('active');
    };

    // 開く処理
    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.add('active');
        });
    }

    // ❌ボタンで閉じる
    if (closeX) {
        closeX.addEventListener('click', (e) => {
            e.stopPropagation();
            hideModal();
        });
    }

    // 背景クリックで閉じる
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                hideModal();
            }
        });
    }

    // Escキーで閉じる
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            hideModal();
        }
    });
})();



// ぼっちん&るみなダンス動画
const trigger = document.getElementById('popupTrigger');
const overlay = document.getElementById('overlay');
// 動画要素を取得
const video = overlay.querySelector('video');
let timer = null;

// 閉じる処理を共通化
const closePopup = () => {
    overlay.classList.remove('active');
    if (timer) {
        clearTimeout(timer);
        timer = null;
    }
    // 動画を一時停止して最初に戻す
    if (video) {
        video.pause();
        video.currentTime = 0;
    }
};

// ポップアップを表示して3秒後に閉じる関数
trigger.addEventListener('click', () => {
    if (timer) clearTimeout(timer);

    // 表示する瞬間に動画を最初から再生
    if (video) {
        video.currentTime = 0;
        video.play();
    }

    overlay.classList.add('active');

    timer = setTimeout(() => {
        closePopup();
    }, 3000);
});

// 背景クリックでも即座に閉じられるようにしておく
overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
        closePopup();
    }
});