import streamlit as st
import yt_dlp
import os
import re

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

st.title("🎵 YouTube MP3 Downloader")
st.write("YouTubeのURLを貼って「変換」ボタンを押してね。")

# URL入力
url_input = st.text_input("URLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

# 変換ボタン
if st.button("変換", use_container_width=True):
    if url_input:
        # YouTubeのURLかチェック
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # プレイリスト等の余計なパラメータをカット（エラー回避のため）
                clean_url = url_input.split('&')[0]
                
                with st.spinner("変換中... 数分かかる場合があるよ"):
                    # ダウンロード設定（サーバーブロック回避を強化）
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'temp_music.%(ext)s',
                        'noplaylist': True,
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'add_header': [
                            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                            'Accept-Language: ja,en-US;q=0.9,en;q=0.8',
                        ],
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # 動画情報を取得してダウンロード
                        info = ydl.extract_info(clean_url, download=True)
                        
                        # ファイル名のクリーニング
                        title = re.sub(r'[\\/*?:"<>|]', "", info['title'])
                        filename = "temp_music.mp3"
                        download_name = f"{title}.mp3"

                    # ダウンロードボタンの表示
                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📥 MP3を保存する",
                                data=f,
                                file_name=download_name,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                        
                        # 保存後にサーバー上のファイルを削除
                        os.remove(filename)
                        st.success(f"「{info['title']}」の準備ができたよ！")
                    else:
                        st.error("ファイルの作成に失敗したみたい。")

            except Exception as e:
                st.error(f"エラーが発生しました。YouTube側の制限かもしれません。\n(Error: {e})")
        else:
            st.warning("有効なYouTubeのURLを入れてね。")
    else:
        st.warning("URLを入力してからボタンを押してね。")