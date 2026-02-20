/**
 * ファッション占いガチャ 設定ファイル
 */
const GACHA_CONFIG = {
    // --- システム設定 ---
    isLimitEnabled: true, // trueで1日1回制限を有効、falseで無制限
    isDebugMode: true,    // trueで開発用のリセットボタンを表示、falseで非表示

    // --- 確率設定 (合計100%) ---
    probabilities: {
        "N": 27,
        "R": 23,
        "SR": 20,
        "SSR": 15,
        "UR": 10,
        "LR": 5
    },

    // --- 各レア度に対応する画像IDリスト ---
    // 画像パス: fashion/レア度_fs_ID.jpg
    imageIds: {
        "N": ["normal"],
        "R": ["clear"],
        "SR": ["y2k"],
        "SSR": ["landmine"],
        "UR": ["christmas"],
        "LR": ["school", "maid"]
    },

};