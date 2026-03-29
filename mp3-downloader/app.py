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
st.write("04＊YouTubeのURLを貼り付けて変換ボタンを押してください。")

url_input = st.text_input("URL", placeholder="https://www.youtube.com/watch?v=...")

def download_process(url):
    """メインのダウンロード処理"""
    timestamp = int(time.time())
    output_filename = f"music_{timestamp}"
    full_path = f"{output_filename}.mp3"
    
    # 究極の回避策：iOSの公式アプリをエミュレート
    # Androidの偽装がバレやすいため、判定の緩いiOSクライアントを使用
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
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'ja-JP,ja;q=0.9',
            'Referer': 'https://www.youtube.com/',
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
        return full_path, f"{title}.mp3"

if st.button("変換", use_container_width=True):
    if url_input:
        # 動画IDの抽出
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
        
        if video_id_match:
            video_id = video_id_match.group(1)
            clean_url = f"https://www.youtube.com/watch?v={video_id}"

            try:
                with st.spinner("変換中... (Googleサーバーでバイパス処理中)"):
                    # 1. GASにアクセスさせて、GoogleのIPでYouTubeのセッションを「こじ開ける」
                    try:
                        requests.get(GAS_WEB_APP_URL, params={"url": clean_url}, timeout=15)
                    except:
                        pass
                    
                    # 2. 直後にStreamlitから「iPhone」になりすまして実行
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
                        st.error("エラー：ファイルが生成されませんでした。")

            except Exception as e:
                # 403ブロックなどで失敗した場合、外部の安定した変換ルートを表示
                st.error("YouTubeの制限が非常に厳しいため、直接変換できませんでした。")
                st.info("以下のリンクから、外部の安全な変換サイトを利用できます。")
                # y2mateなどの安定した外部サービスへのリンクを動的に生成
                st.link_button("🚀 外部サイトでMP3変換する", f"https://www.y2mate.com/youtube/{video_id}", use_container_width=True)
                st.caption(f"Debug Info: {str(e)[:50]}")
        else:
            st.warning("有効なYouTube URLを入力してください。")
    else:
        st.warning("URLを入力してください。")

st.markdown("---")
st.caption("Produced by mp3-downloader Team | Powered by Streamlit & GAS")