import streamlit as st
import os
import base64
import streamlit as st
from utils import (
    SKILL_DICT,
    initialize_session,
    apply_exp,
    level_up_status,
    get_skill_description,
    check_title_unlock,
    save_data
)

# --- ② 背景適用用の関数定義（関数定義ブロックの外で）---
def apply_background(file_path):
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


def show_skills_page():
    st.set_page_config(page_title="スキル入力", layout="centered")
    initialize_session()

    # --- 背景画像を適用するパス指定ここ！ ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, "..", "gif_assets", "abyss_background2.gif")  # ←ここで画像名を指定
    apply_background(bg_path)

    st.title("📘 今日の行動入力")

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

    if submitted:
        # 各スキルに対して経験値を加算
        for skill, level in effort_levels.items():
            if level > 0:
                apply_exp(skill, level)
                st.success(f"✅ {skill} の実施 → 経験値を反映しました")

        # レベルアップ演出
        level_up_status()

        # 称号獲得チェック
        check_title_unlock()

        # ログ表示（ステータスや称号）
        if st.session_state.log:
            st.markdown("---")
            st.markdown("### 🔔 成長ログ")
            for msg in st.session_state.log:
                st.markdown(f"<span style='color:deepskyblue;font-weight:bold;'>{msg}</span>", unsafe_allow_html=True)
            st.session_state.log.clear()

        # 保存ボタン表示
        st.markdown("---")
        if st.button("💾 データを保存する"):
            save_data()
            st.success("✅ 成長記録を保存しました")