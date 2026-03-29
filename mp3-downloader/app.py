import streamlit as st
import yt_dlp
import os
import re
import time
import requests

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

# --- GAS設定 ---
# デプロイしたウェブアプリのURL
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
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 YouTube MP3 Downloader")
st.write("02＊YouTubeのURLを貼り付けて変換ボタンを押してください。")

url_input = st.text_input("URL", placeholder="https://www.youtube.com/watch?v=...")

def download_process(url):
    """メインのダウンロード処理"""
    timestamp = int(time.time())
    output_filename = f"music_{timestamp}"
    full_path = f"{output_filename}.mp3"
    
    # YouTubeの厳格な制限を回避するための設定
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # クライアント偽装: android_testsuiteは現在比較的安定している
        'extractor_args': {
            'youtube': {
                'player_client': ['android_testsuite', 'web_embedded'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'headers': {
            'User-Agent': 'com.google.android.youtube/19.05.36 (Linux; U; Android 11; ja_JP; Pixel 5 Build/RD2A.211001.002) gzip',
            'Accept-Language': 'ja-JP',
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ダウンロード実行
        info = ydl.extract_info(url, download=True)
        title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
        return full_path, f"{title}.mp3"

if st.button("変換", use_container_width=True):
    if url_input:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # 動画IDを抽出してクリーンなURLにする
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
                clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}" if video_id_match else url_input

                with st.spinner("変換中..."):
                    # 1. GASを経由してYouTubeにアクセス（GoogleのIPで足跡をつける）
                    try:
                        requests.get(GAS_WEB_APP_URL, params={"url": clean_url}, timeout=15)
                    except:
                        pass # GASの応答が遅くても処理は続行
                    
                    # 2. ダウンロードとMP3変換の実行
                    file_path, display_name = download_process(clean_url)
                    
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 MP3を保存する",
                                data=f,
                                file_name=display_name,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                        st.success(f"変換が完了しました: {display_name}")
                        # 使用した一時ファイルを削除
                        os.remove(file_path)
                    else:
                        st.error("ファイルの生成に失敗しました。")

            except Exception as e:
                st.error("YouTubeの制限により現在このURLは変換できません。")
                st.info("時間を置いてからもう一度試してみてください。")
        else:
            st.warning("YouTubeのURLを正しく入力してください。")
    else:
        st.warning("URLを入力してください。")

st.markdown("---")
st.caption("Produced by mp3-downloader Team | Powered by Streamlit & GAS")