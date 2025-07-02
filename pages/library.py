import streamlit as st
from utils import SKILL_DICT, initialize_session

st.set_page_config(page_title="スキル辞典と称号", layout="wide")
initialize_session()

st.title("📚 スキル辞典")

# レイアウト整形
cols = st.columns(2)

for i, (skill, data) in enumerate(SKILL_DICT.items()):
    col = cols[i % 2]
    with col:
        st.markdown(f"### 🎓 {skill}")
        st.markdown(f"- **属性**：{' ／ '.join(data['attribute'])}")
        st.markdown(f"- **ステータス**：{'・'.join(data['status'])}")
        st.markdown(f"- **説明**：{data['desc']}")
        st.markdown("---")

# 称号一覧セクション
st.markdown("## 🏅 称号コレクション")

# 仮の称号リスト（今後はスキル経験値などから自動解禁）
ALL_TITLES = [
    "睡眠を制す者", "目覚めの勇者", "身体は資本", "呼吸を知る者",
    "知を灯す者", "声に魂を宿す者"
]

# ユーザーが獲得済の称号（セッション状態から）
unlocked = st.session_state.unlocked_titles

for title in ALL_TITLES:
    if title in unlocked:
        st.markdown(f"- ✅ **{title}**")
    else:
        st.markdown(f"- ❌ ~~{title}~~")  # 未取得は打ち消し表示