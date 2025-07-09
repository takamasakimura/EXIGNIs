import streamlit as st
from PIL import Image
import base64
import io
import os

from utils import initialize_session, load_data
from pages.skills import show_skills_page
from pages.status import show_status_page
from pages.library import show_library_page
from pages.report import show_report_page

# ページ設定（最上部）
st.set_page_config(layout="wide")

# サイドバー完全非表示
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    div[data-testid="stSidebarContent"] {
        display: none !important;
    }
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# セッション＆データ
initialize_session()
load_data()

# パス構成
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "gif_assets", "abyss_background.gif")
logo_path = os.path.join(current_dir, "images", "abysslog_logo_transparent.png")

# 背景GIF適用
def apply_background_gif(file_path):
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
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

# 背景GIFを一度だけ適用（重複削除）
apply_background_gif(background_path)

# 起動画面（Tap to Start）
if not st.session_state.get("started"):
    with open(tap_path, "rb") as f:
        tap_encoded = base64.b64encode(f.read()).decode()

    # ロゴも表示しない（ここでは）
    st.markdown(
        f"""
        <style>
        .center-image {{
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            height: 100vh;
        }}
        .center-image img {{
            width: 200px;
            max-width: 80vw;
            animation: blink 1.5s infinite;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        <div class="center-image">
            <img src="data:image/png;base64,{tap_encoded}" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
        div.stButton > button {
            background: transparent;
            color: transparent;
            border: none;
            box-shadow: none;
            width: 200px;
            height: 80px;
            position: absolute;
            bottom: 20%;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10000;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

# ペルソナ風CSS
st.markdown("""
    <style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap');

.main, .block-container {
    background-color: rgba(0, 0, 0, 0) !important;
    box-shadow: none !important;
    padding: 2rem 2rem;
    border-radius: 12px;
}

header, footer {
    visibility: hidden;
}

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

# --- パス構成と背景・ロゴ表示 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "gif_assets", "abyss_background.gif")
logo_path = os.path.join(current_dir, "images", "abysslog_logo_transparent.png")

apply_background_gif(background_path)
# ロゴは条件付きで表示
if st.session_state.get("started") and st.session_state.get("page") != "skills":
    display_logo(logo_path)

# 背景とロゴの表示
apply_background_gif(background_path)
display_logo(logo_path)

# tap_to_start_clean.png 用エンコード
tap_path = os.path.join(current_dir, "images", "tap_to_start_clean.png")
with open(tap_path, "rb") as f:
    tap_encoded = base64.b64encode(f.read()).decode()

# 起動画面（起動前）
if not st.session_state.get("started"):
    # ボタン画像の読み込み（表示用）
    tap_path = os.path.join(current_dir, "images", "tap_to_start_clean.png")
    with open(tap_path, "rb") as f:
        tap_encoded = base64.b64encode(f.read()).decode()

    # 背景中央にボタン画像＋透明ボタン
    st.markdown(
        f"""
        <style>
        .center-image {{
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            height: 100vh;
        }}
        .center-image img {{
            width: 200px;
            max-width: 80vw;
            animation: blink 1.5s infinite;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        <div class="center-image">
            <img src="data:image/png;base64,{tap_encoded}" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
        div.stButton > button {
            background: transparent;
            color: transparent;
            border: none;
            box-shadow: none;
            width: 200px;
            height: 80px;
            position: absolute;
            bottom: 20%;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10000;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Tap to Start", key="start_button"):
        st.session_state.started = True
        st.rerun()

else:
    # 起動後で page が skills 以外のときだけロゴを表示
    if st.session_state.get("page") != "skills":
        display_logo(logo_path)

    # ページ分岐（今回は skills 固定）
    show_skills_page()