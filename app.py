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

<img src="data:image/png;base64,{base64}" style="background-color: transparent;" />

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

# ロゴ表示
def display_logo(path: str, width: int = 320):
    logo = Image.open(path)
    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    logo_base64 = base64.b64encode(buffered.getvalue()).decode()
st.markdown("""
    <style>
    .tap-to-start {{
        position: absolute;
        bottom: 5%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        opacity: 0.9;
    }}
    </style>
    <div class="tap-to-start">
        <a href="?start=true">
            <img src="data:image/png;base64,{}" width="220">
        </a>
    </div>
""".format(base64.b64encode(open("images/tap_to_start_clean.png", "rb").read()).decode()), unsafe_allow_html=True)

# ペルソナ風CSS
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

# 背景とロゴの表示
apply_background_gif(background_path)
display_logo(logo_path)

# tap_to_start_clean.png 用エンコード
tap_path = os.path.join(current_dir, "images", "tap_to_start_clean.png")
with open(tap_path, "rb") as f:
    tap_encoded = base64.b64encode(f.read()).decode()

# 起動画面
if not st.session_state.get("started"):
    st.markdown(f"""
        <style>
        .logo-top-left {{
            position: absolute;
            top: 0x;
            left: 0px;
            z-index: 9999;
	    padding;10px;
        }}
        .tap-to-start {{
            position: absolute;
            bottom: 5%;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }}
        .transparent-button {{
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50%;
            z-index: 10000;
        }}
        </style>
        <div class="logo-top-left">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" width="180">
        </div>
        <div class="tap-to-start">
            <a href="?start=true">
                <img src="data:image/png;base64,{tap_encoded}" width="200">
            </a>
        </div>
        <div class="transparent-button">
            <a href="?start=true">
                <img src="data:image/png;base64,{}" width="100%" height="100%" style="opacity:0;" />
            </a>
        </div>
""".format(base64.b64encode(open("images/transparent_click_area.png", "rb").read()).decode()), 
    """, unsafe_allow_html=True)

    # 遷移トリガー
    if st.query_params.get("start") == ["true"]:
        st.session_state.started = True
        st.experimental_rerun()

else:
    # 本編（skillsページ）へ
    show_skills_page()

    if tab == "SKILLS":
        show_skills_page()
    elif tab == "STATUS":
        show_status_page()
    elif tab == "LIBRARY":
        show_library_page()
    elif tab == "REPORT":
        show_report_page()