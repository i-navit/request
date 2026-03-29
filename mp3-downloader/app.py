import streamlit as st
import yt_dlp
import os
import re

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

st.title("🎵 YouTube MP3 Downloader")
st.write("2*YouTubeのURLを貼って「変換」ボタンを押してね。")

# URL入力
url_input = st.text_input("URLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

# 変換ボタン
if st.button("変換", use_container_width=True):
    if url_input:
        # YouTubeのURLかチェック
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # URLの掃除（パラメータを最小限にする）
                clean_url = url_input.split('?')[0] + '?' + url_input.split('?')[1].split('&')[0] if '?' in url_input else url_input
                
                with st.spinner("変換中... YouTubeの制限を回避しながら処理しているよ"):
                    # 403 Forbidden や Bot判定を回避するための最新設定
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
                        # 最新のBot検知回避策：Android端末からのアクセスを偽装
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android'],
                                'skip': ['dash', 'hls']
                            }
                        },
                        'youtube_include_dash_manifest': False,
                        'add_header': [
                            'User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language: ja-JP,ja;q=0.9',
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
                        st.error("ファイルがうまく作成されなかったみたい。")

            except Exception as e:
                # エラーメッセージをより詳細に
                error_msg = str(e)
                if "Sign in to confirm you’re not a bot" in error_msg:
                    st.error("YouTubeに「ロボット」だと判定されてブロックされちゃった...。Web版の限界かもしれないけど、URLを変えてもう一度試してみて。")
                else:
                    st.error(f"エラーが発生しました。\n(Error: {e})")
        else:
            st.warning("有効なYouTubeのURLを入れてね。")
    else:
        st.warning("URLを入力してからボタンを押してね。")