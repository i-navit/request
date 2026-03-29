import streamlit as st
import re
import requests

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

# --- GAS設定 (デプロイした最新のURLをここに貼り付けてね) ---
GAS_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw6DRYqll_vD39m8xiP9-KAqRmY2R_3LcqO0aK7rTZge5UI797QjN2wJG1rvugsQPll/exec"

# デザインの調整
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .download-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    .dl-btn {
        text-decoration: none !important;
        background-color: #28a745;
        color: white !important;
        padding: 15px 25px;
        border-radius: 10px;
        font-weight: bold;
        display: inline-block;
        width: 100%;
        transition: 0.3s;
    }
    .dl-btn:hover {
        background-color: #218838;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 MP3 Downloader")
st.write("07＊YouTubeのURLを入力して変換ボタンを押してください。")

url_input = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("変換", use_container_width=True):
    if url_input:
        # 動画IDの抽出
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
        
        if video_id_match:
            video_id = video_id_match.group(1)
            
            with st.spinner("Googleサーバーでリンクを生成中..."):
                try:
                    # 1. GASにリクエストを送ってcobalt経由の直リンクを取得
                    res = requests.get(GAS_WEB_APP_URL, params={"url": url_input}, timeout=25)
                    data = res.json()
                    
                    if data.get("status") == "success":
                        st.success("ダウンロードの準備が完了したよ！")
                        download_url = data.get("downloadUrl")
                        
                        # 2. 直リンクをボタンとして表示
                        st.markdown(f"""
                            <div class="download-card">
                                <a href="{download_url}" target="_blank" class="dl-btn">
                                    📥 MP3をダウンロードする
                                </a>
                                <p style="font-size: 0.85em; color: #666; margin-top: 15px;">
                                    ※クリックすると別タブでダウンロードが始まるよ。
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        # GAS側でエラー（No link found等）が返ってきた場合
                        st.error(f"直接リンクの生成に失敗したよ: {data.get('message', 'Unknown Error')}")
                        st.info("以下の代わりの変換ルートを試してみて。")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.link_button("🚀 変換ルートA", f"https://y2meta.app/en/youtube/{video_id}", use_container_width=True)
                        with col2:
                            st.link_button("🚀 変換ルートB", f"https://yt5s.io/en/youtube/{video_id}", use_container_width=True)

                except Exception as e:
                    # 通信エラーやJSON解析エラーの場合
                    st.error("現在、アクセス制限により自動変換が難しいみたいだ。")
                    st.link_button("🚀 外部の変換サイトを開く", f"https://y2meta.app/en/youtube/{video_id}", use_container_width=True)
        else:
            st.warning("有効なYouTube URLを入力してね。")
    else:
        st.warning("URLを入力してね。")

st.markdown("---")
st.caption("Produced by mp3-downloader Team | Powered by Google Apps Script")