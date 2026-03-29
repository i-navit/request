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
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 YouTube MP3 Downloader")
st.write("03＊YouTubeのURLを貼り付けて変換ボタンを押してください。")

url_input = st.text_input("URL", placeholder="https://www.youtube.com/watch?v=...")

def download_process(url):
    """メインのダウンロード処理"""
    timestamp = int(time.time())
    output_filename = f"music_{timestamp}"
    full_path = f"{output_filename}.mp3"
    
    # YouTubeのガードを潜り抜けるための最新オプション
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
        # 埋め込みプレイヤーとAndroidアプリの挙動をミックス
        'extractor_args': {
            'youtube': {
                'player_client': ['web_embedded', 'android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        # Google検索や公式サイトからの流入を装う
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'ja-JP,ja;q=0.9',
            'Referer': 'https://www.google.com/',
            'Origin': 'https://www.youtube.com',
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 実際にダウンロードを実行
        info = ydl.extract_info(url, download=True)
        title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
        return full_path, f"{title}.mp3"

if st.button("変換", use_container_width=True):
    if url_input:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # URLを動画ID単体のクリーンな形に整形
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
                clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}" if video_id_match else url_input

                with st.spinner("変換中... (Googleサーバーを中継しています)"):
                    # 1. GASに「GoogleのIP」で動画をフェッチさせる
                    # これにより、YouTube側にGoogle経由の正常なアクセスだと記録させる
                    try:
                        requests.get(GAS_WEB_APP_URL, params={"url": clean_url}, timeout=15)
                    except:
                        pass # GASの応答待ちは15秒で切り上げる
                    
                    # 2. その直後にStreamlitからダウンロードを開始
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
                        st.success(f"変換完了: {display_name}")
                        os.remove(file_path)
                    else:
                        st.error("エラー：ファイルが見つかりませんでした。")

            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg:
                    st.error("YouTubeのガードが非常に固いため、このサーバーからの保存が制限されています。")
                    st.info("時間を置いてから別の動画でお試しください。")
                else:
                    st.error("変換に失敗しました。URLを確認してください。")
        else:
            st.warning("有効なYouTube URLを入力してください。")
    else:
        st.warning("URLを入力してください。")

st.markdown("---")
st.caption("Produced by mp3-downloader Team | Powered by Streamlit & GAS")