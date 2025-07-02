import streamlit as st
import pandas as pd
import altair as alt
from utils import initialize_session

def show_report_page():
    st.markdown("### 🔧 行動入力（Skills）")
    st.markdown("ここに行動入力フォームやスキル選択UIを実装します。")
    # 例: スキルの選択肢や入力欄など
    if st.button("ダミーボタン"):
        st.success("ダミー操作が実行されました！")

st.set_page_config(page_title="週報・分析", layout="wide")
initialize_session()

st.title("📅 週間レポート")

# 想定：スキル実施履歴をCSVなどから読み込む形
# 仮データ（7日分×スキル名×実施度）を生成
def load_mock_log():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
    skills = list(st.session_state.skill_levels.keys())
    data = []

    for date in dates:
        for skill in skills:
            value = st.session_state.skill_levels[skill] + (hash(f"{date}-{skill}") % 3)
            data.append({"日付": date.strftime("%Y-%m-%d"), "スキル": skill, "実施度": min(value, 5)})

    return pd.DataFrame(data)

df = load_mock_log()

# 🎯 スキル別使用傾向
st.markdown("### 📘 スキル別 実施度ヒートマップ")

heatmap = alt.Chart(df).mark_rect().encode(
    x=alt.X('日付:O', sort=None),
    y=alt.Y('スキル:O'),
    color=alt.Color('実施度:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['スキル', '日付', '実施度']
).properties(height=300)

st.altair_chart(heatmap, use_container_width=True)

# 📊 ステータスの成長グラフ
st.markdown("### 📊 ステータス成長推移（擬似）")

# 擬似データ生成（現状はsessionの現在値を元に加工）
stats_df = pd.DataFrame({
    "ステータス": list(st.session_state.status.keys()),
    "現在値": list(st.session_state.status.values())
})

bar_chart = alt.Chart(stats_df).mark_bar().encode(
    x='ステータス',
    y='現在値',
    color=alt.Color('現在値', scale=alt.Scale(scheme='redblue')),
    tooltip=['ステータス', '現在値']
).properties(height=400)

st.altair_chart(bar_chart, use_container_width=True)