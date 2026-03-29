import streamlit as st
import yt_dlp
import os
import re
import time

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

# デザインの調整
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
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 YouTube MP3 Downloader")
st.write("1*YouTubeのURLを貼り付けて変換ボタンを押してください。")

# URL入力
url_input = st.text_input("URL", placeholder="https://www.youtube.com/watch?v=...")

def download_process(url):
    """メインのダウンロード処理"""
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
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'mweb'],
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = re.sub(r'[\\/*?:"<>|]', "", info.get('title', 'music'))
        return full_path, f"{title}.mp3"

# 変換ボタン
if st.button("変換", use_container_width=True):
    if url_input:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # URLのクリーニング
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url_input)
                clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}" if video_id_match else url_input

                with st.spinner("変換中..."):
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
                        os.remove(file_path)
                    else:
                        st.error("ファイルの生成に失敗しました。")

            except Exception as e:
                st.error("YouTubeの制限により、この環境からはダウンロードできません。")
                st.info("別の動画で試すか、時間をおいて再度実行してください。")
        else:
            st.warning("YouTubeのURLを入力してください。")
    else:
        st.warning("URLを入力してください。")

st.markdown("---")
st.caption("Produced by mp3-downloader Team")