import streamlit as st
import yt_dlp
import os
import re

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

st.title("🎵 YouTube MP3 Downloader")
st.write("YouTube MusicのURLを貼るだけで、楽曲をMP3に変換するよ。")

# URL入力
url = st.text_input("YouTubeのURLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

if url:
    # 簡易的なURLチェック
    if "youtube.com" in url or "youtu.be" in url:
        try:
            with st.spinner("変換中... 少し待ってね"):
                # ダウンロード設定（公開動画のみ、Cookie不要）
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'temp_music.%(ext)s',
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # ファイル名のクリーニング（変な記号を消す）
                    title = re.sub(r'[\\/*?:"<>|]', "", info['title'])
                    filename = "temp_music.mp3"
                    download_name = f"{title}.mp3"

                # ダウンロードボタン
                with open(filename, "rb") as f:
                    st.download_button(
                        label="📥 MP3を保存する",
                        data=f,
                        file_name=download_name,
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                
                # サーバーの掃除
                if os.path.exists(filename):
                    os.remove(filename)
                st.success("準備ができたよ！上のボタンを押して保存してね。")

        except Exception as e:
            st.error(f"エラーが起きちゃった。公開動画かどうか確認してみてね。\n(Error: {e})")
    else:
        st.warning("有効なYouTubeのURLを入れてね。")