import streamlit as st
from PIL import Image
import base64
from utils import initialize_session, load_data
import io
import os

# ページ設定（最上部に置く）
st.set_page_config(layout="wide")

# セッション＆データ
initialize_session()
load_data()

# 安全なパス取得方法
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "gif_assets", "abyss_background.gif")
logo_path = os.path.join(current_dir, "images", "abysslog_logo_transparent.png")
start_banner_path = os.path.join(current_dir, "gif_assets", "start_banner.gif")

# 背景GIF表示用関数
def apply_background_gif(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("data:image/gif;base64,{encoded}") no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# 開始バナー表示用関数
def display_base64_gif(file_path, width=600):
    with open(file_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f'<div style="text-align:center;"><img src="data:image/gif;base64,{encoded}" width="{width}"/></div>',
            unsafe_allow_html=True,
        )

# ロゴ表示用関数
def display_logo(path: str, width: int = 320):
    logo = Image.open(path)
    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(
        f"""
        <style>
        .logo-container {{
            position: absolute;
            top: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="{width}">
        </div>
        """,
        unsafe_allow_html=True
    )

# 背景とロゴの表示（ここから）
apply_background_gif(background_path)
display_logo(logo_path)

# ペルソナ風CSS適用
st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap');
body {
    background-color: #0d0d0d;
    color: white;
    font-family: 'Jost', 'BIZ UDPGothic', sans-serif;
}
h1, h2, h3, h4 {
    color: #ff0033;
    text-shadow: 2px 2px black;
    font-weight: bold;
}
.block-container {
    padding: 2rem 2rem;
    background: linear-gradient(45deg, #0a0a0a, #1a1a1a);
    border-radius: 12px;
    box-shadow: 0 0 10px #ff0033;
}
.glow {
    color: deepskyblue;
    font-weight: bold;
    animation: glowPulse 1.5s infinite;
}
@keyframes glowPulse {
    0% { text-shadow: 0 0 5px #00ffff; }
    50% { text-shadow: 0 0 15px #00ffff; }
    100% { text-shadow: 0 0 5px #00ffff; }
}
div.stButton > button {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border: none;
    padding: 0.6em 1.5em;
    border-radius: 8px;
    box-shadow: 0 0 5px #ff0033;
}
div.stButton > button:hover {
    background-color: #cc0000;
    box-shadow: 0 0 10px #ff0033;
}
    </style>
""", unsafe_allow_html=True)

# 起動画面 or メイン画面
if not st.session_state.get("started"):
    display_base64_gif(start_banner_path)
    st.markdown('<div style="text-align:center;font-size:28px;color:white;text-shadow:2px 2px black;">- tap to start -</div>', unsafe_allow_html=True)
    
    if st.button("▶️ はじめる"):
        st.session_state.started = True
        st.experimental_rerun()
else:
    st.markdown("<h1>🕶 ステータス育成アプリ</h1>", unsafe_allow_html=True)
    st.markdown("## ✨ 今日も、自分を育てる1日を。")
    st.markdown("---")
    st.info("📘 サイドバーから [行動入力] へどうぞ。")
