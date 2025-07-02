import streamlit as st
from utils import initialize_session

st.set_page_config(page_title="ステータス画面", layout="centered")
initialize_session()

st.title("📊 現在のステータス")

# 表示前の前回ステータス（前回比較用に一時保存しておく）
if "prev_status" not in st.session_state:
    st.session_state.prev_status = st.session_state.status.copy()

# CSSアニメーション：青く発光する文字
st.markdown("""
    <style>
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
    </style>
""", unsafe_allow_html=True)

# 表示用の並び順
status_keys = ["STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU"]

# 2列表示
cols = st.columns(2)

for i, stat in enumerate(status_keys):
    col = cols[i % 2]
    with col:
        current = st.session_state.status[stat]
        prev = st.session_state.prev_status.get(stat, current)

        if current > prev:
            # 上昇したステータスは光らせて表示
            st.markdown(f"<h3>{stat}：<span class='glow'>{current}</span> 🔼</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3>{stat}：{current}</h3>", unsafe_allow_html=True)

# 保存（表示終了時に現在値をprev_statusに記録）
st.session_state.prev_status = st.session_state.status.copy()