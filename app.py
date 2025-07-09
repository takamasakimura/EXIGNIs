import streamlit as st
from PIL import Image
import base64
import io
import os

from utils import initialize_session, load_data
# from pages.skills import show_skills_page  # 一時コメントアウト
from pages.status import show_status_page
from pages.library import show_library_page
from pages.report import show_report_page

st.set_page_config(layout="wide")

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

initialize_session()
load_data()

current_dir = os.path.dirname(os.path.abspath(__file__))
tap_path = os.path.join(current_dir, "images", "tap_to_start_clean.png")
background_path = os.path.join(current_dir, "gif_assets", "abyss_background.gif")
logo_path = os.path.join(current_dir, "images", "abysslog_logo_transparent.png")

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

apply_background_gif(background_path)

if not st.session_state.get("started"):
    with open(tap_path, "rb") as f:
        tap_encoded = base64.b64encode(f.read()).decode()

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
        st.session_state["page"] = "status"  # skills から status に変更
        st.rerun()

else:
    page = st.session_state.get("page", "status")

    if page == "status":
        show_status_page()
    elif page == "library":
        show_library_page()
    elif page == "report":
        show_report_page()
