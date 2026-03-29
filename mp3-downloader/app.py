import streamlit as st
import yt_dlp
import os
import re
import time

# Page Configuration
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

# Custom CSS for better look
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
st.write("5*URLを貼って「変換」を押してね。フレンドのみんなも使えるよ！")

# URL Input
url_input = st.text_input("YouTubeのURLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

# Download Function
def download_mp3(url):
    # Unique filename to avoid conflicts
    timestamp = int(time.time())
    output_filename = f"music_{timestamp}"
    full_path = f"{output_filename}.mp3"
    
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
        # Try to use different clients to bypass blocks
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'android', 'ios'],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to check if available
            info = ydl.extract_info(url, download=True)
            title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
            return full_path, f"{title}.mp3"
    except Exception as e:
        raise e

# Action Button
if st.button("変換開始", use_container_width=True):
    if url_input:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # Clean URL (remove playlist params)
                clean_url = url_input.split('&')[0]
                
                with st.spinner("変換中... 30秒〜1分くらい待ってね！"):
                    file_path, display_name = download_mp3(clean_url)
                    
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 MP3を保存する",
                                data=f,
                                file_name=display_name,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                        # Success message and cleanup
                        st.success(f"✅ 「{display_name}」の準備ができたよ！")
                        os.remove(file_path)
                    else:
                        st.error("ごめん、ファイルがうまく作れなかったよ。")
            except Exception as e:
                st.error("YouTubeの制限で今は変換できないみたい...。別の動画で試すか、少し時間を置いてみてね。")
                st.info(f"技術的なエラー: {str(e)[:100]}...")
        else:
            st.warning("YouTubeのURLを正しく入力してね。")
    else:
        st.warning("まずはURLを貼ってね！")

st.markdown("---")
st.caption("Produced by mp3-downloader Team")