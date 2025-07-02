import streamlit as st
from utils import SKILL_DICT, initialize_session, apply_exp, level_up_status, get_skill_description

st.set_page_config(page_title="スキル入力", layout="centered")
initialize_session()

st.title("📘 今日の行動入力")

# 行動一覧（辞書から取得）
skills = list(SKILL_DICT.keys())

st.markdown("### 🎯 各スキルの実施度を記録（0〜5）")

with st.form("skill_form"):
    effort_levels = {}
    for skill in skills:
        col1, col2 = st.columns([2, 3])
        with col1:
            level = st.slider(f"{skill}", 0, 5, 0, key=f"effort_{skill}")
            effort_levels[skill] = level
        with col2:
            st.caption(get_skill_description(skill))

    submitted = st.form_submit_button("記録して経験値に反映")

from utils import save_data
...
if submitted:
    ...
    save_data()

if submitted:
    # 各スキルに対して経験値を加算
    for skill, level in effort_levels.items():
        if level > 0:
            apply_exp(skill, level)
            st.success(f"✅ {skill} の実施 → 経験値を反映しました")

    # レベルアップの自動チェック
    level_up_status()

    # ログ表示
    if st.session_state.log:
        st.markdown("---")
        st.markdown("### 🔔 レベルアップ演出！")
        for msg in st.session_state.log:
            st.markdown(f"<span style='color:deepskyblue;font-weight:bold;'>{msg}</span>", unsafe_allow_html=True)
        st.session_state.log.clear()