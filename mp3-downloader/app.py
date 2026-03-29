import streamlit as st
import yt_dlp
import os
import re
import time
import requests

# Page Configuration
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
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
st.write("7*URLを貼って「変換」を押してね。フレンドのみんなも使えるよ！")

# URL Input
url_input = st.text_input("YouTubeのURLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

def download_mp3_with_fallback(url):
    timestamp = int(time.time())
    output_filename = f"music_{timestamp}"
    full_path = f"{output_filename}.mp3"
    
    # 複数のクライアント設定を試す
    clients = ['android', 'ios', 'mweb']
    
    last_error = None
    
    for client in clients:
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
                    'player_client': [client],
                    'player_skip': ['webpage', 'configs'],
                }
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
                return full_path, f"{title}.mp3"
        except Exception as e:
            last_error = e
            continue # 次のクライアントを試す
            
    raise last_error

# Action Button
if st.button("変換開始", use_container_width=True):
    if url_input:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # クエリパラメータを整理
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
                if video_id_match:
                    clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
                else:
                    clean_url = url_input

                with st.spinner("変換中... YouTubeの制限を回避しながら頑張ってるよ！"):
                    file_path, display_name = download_mp3_with_fallback(clean_url)
                    
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 MP3を保存する",
                                data=f,
                                file_name=display_name,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                        st.success(f"✅ 「{display_name}」の準備ができたよ！")
                        os.remove(file_path)
                    else:
                        st.error("ファイルがうまく作れなかったよ。")
            except Exception as e:
                st.error("YouTubeにブロックされてしまったみたい。")
                st.info("💡 対策案: Google Apps Scriptを中継役に使う設定を検討中だよ。")
                st.caption(f"Error Details: {str(e)[:150]}...")
        else:
            st.warning("YouTubeのURLを正しく入力してね。")
    else:
        st.warning("まずはURLを貼ってね！")

st.markdown("---")
st.caption("Produced by mp3-downloader Team")