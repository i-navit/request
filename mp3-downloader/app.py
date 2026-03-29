import streamlit as st
import yt_dlp
import os
import re

# ページの設定
st.set_page_config(page_title="MP3 Downloader", page_icon="🎵")

st.title("🎵 YouTube MP3 Downloader")
st.write("3*YouTubeのURLを貼って「変換」ボタンを押してね。")

# URL入力
url_input = st.text_input("URLを貼り付けてね", placeholder="https://www.youtube.com/watch?v=...")

# 変換ボタン
if st.button("変換", use_container_width=True):
    if url_input:
        # YouTubeのURLかチェック
        if "youtube.com" in url_input or "youtu.be" in url_input:
            try:
                # URLをクレンジング（不要なパラメータを完全に削除）
                # 共有用やプレイリスト用の長いURLでも動画単体として扱う
                video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url_input)
                if video_id_match:
                    clean_url = f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
                else:
                    clean_url = url_input
                
                with st.spinner("変換中... サーバーブロックを回避しながら処理しているよ"):
                    # 403 Forbidden 回避のための高度な設定
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
                        # チャンクサイズを小さくして、少しずつデータを読み込む（ブロック対策）
                        'http_chunk_size': 1048576, 
                        # 複数のクライアントタイプを試行させる
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'web', 'mweb', 'ios'],
                                'player_skip': ['webpage', 'configs'],
                            }
                        },
                        'add_header': [
                            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                            'Accept-Language: ja,en-US;q=0.9,en;q=0.8',
                            'Origin: https://www.youtube.com',
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
                        st.error("ファイルが生成されませんでした。")

            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg:
                    st.error("YouTube側がこのサーバーからのアクセスを強く制限しているみたい（403エラー）。少し時間を置いてから、別の動画のURLで試してみてね。")
                elif "Sign in" in error_msg:
                    st.error("YouTubeにロボットだと判定されてしまったよ。Web版ではこれ以上の回避が難しいかもしれないんだ。")
                else:
                    st.error(f"エラーが発生しました。\n(Error: {e})")
        else:
            st.warning("有効なYouTubeのURLを入れてね。")
    else:
        st.warning("URLを入力してからボタンを押してね。")