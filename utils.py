import streamlit as st
import pandas as pd
import os

SKILL_DICT = {
    "睡眠統制": {
        "base": 2,
        "attribute": ["体調管理", "持久力"],
        "status": ["CON", "POW"],
        "desc": "夢界との境界を強固に保つ。SAN減少回復+5%。"
    },
    "朝行動術": {
        "base": 3,
        "attribute": ["自律", "瞬発力"],
        "status": ["DEX", "POW"],
        "desc": "日の出前に目覚める術。先制判定+10%。"
    },
    "体幹維持力": {
        "base": 4,
        "attribute": ["肉体強化"],
        "status": ["STR", "CON"],
        "desc": "見えざる力に対抗する軸。転倒・拘束耐性強化。"
    },
    "内息制御": {
        "base": 3,
        "attribute": ["精神集中", "呼吸法"],
        "status": ["POW", "CON"],
        "desc": "恐怖と同調せず整える息。MP消費-1。"
    },
    "学習集中術": {
        "base": 5,
        "attribute": ["集中力", "知力"],
        "status": ["INT", "EDU"],
        "desc": "アーカム大学式学習術。読解・記憶判定+5%。"
    },
    "発声制御": {
        "base": 2,
        "attribute": ["表現力", "コミュ力"],
        "status": ["APP", "EDU"],
        "desc": "異界語すら響かせる声。言語判定+10%。"
    },
    "受容姿勢": {
        "base": 2,
        "attribute": ["共感力", "集中"],
        "status": ["APP", "POW"],
        "desc": "相手の言葉に沈み込む。説得・交渉技能+5%。"
    },
    "身体整律": {
        "base": 3,
        "attribute": ["自律神経", "筋制御"],
        "status": ["CON", "DEX"],
        "desc": "身体の軸を取り戻す。気絶耐性+1段階。"
    },
    "鉄の意志": {
        "base": 4,
        "attribute": ["自制力", "精神耐性"],
        "status": ["POW", "EDU"],
        "desc": "エロスを振り払いし者。魅了効果を1ターン無効化。"
    },
    "拳闘技法": {
        "base": 3,
        "attribute": ["武術", "爆発力"],
        "status": ["STR", "DEX"],
        "desc": "拳に宿す念の流れ。近接攻撃命中+5%。"
    },
    "脚技制動": {
        "base": 3,
        "attribute": ["肉体制御", "柔軟性"],
        "status": ["STR", "DEX"],
        "desc": "足元の冥府を蹴り払う。回避判定+10%。"
    },
    "心身調整術": {
        "base": 3,
        "attribute": ["体調管理", "精神安定"],
        "status": ["POW", "CON"],
        "desc": "脱落寸前に戻る術。HP/MP回復+1D3。"
    },
    "推論構築": {
        "base": 5,
        "attribute": ["思考力", "知識応用"],
        "status": ["INT", "EDU"],
        "desc": "断片から真実を紡ぐ。アイデア成功率+10%。"
    },
    "認知防御術": {
        "base": 5,
        "attribute": ["観察", "懐疑性"],
        "status": ["INT", "POW"],
        "desc": "誘導を跳ね返す術。心理判定耐性+5%。"
    },
    "頭脳加算術": {
        "base": 2,
        "attribute": ["計算処理", "集中力"],
        "status": ["INT", "DEX"],
        "desc": "即興の思考演算。技術判定成功+5%。"
    },
    "珠算集中法": {
        "base": 3,
        "attribute": ["微細制御", "学習力"],
        "status": ["DEX", "EDU"],
        "desc": "魔法陣を描く手の技。判定時間-10%。"
    },
    "洞察観察術": {
        "base": 4,
        "attribute": ["観察力", "分析"],
        "status": ["INT", "APP"],
        "desc": "視線に宿す鋭さ。隠された物品の発見+10%。"
    },
    "心理読み": {
        "base": 4,
        "attribute": ["感受性", "読解"],
        "status": ["EDU", "POW"],
        "desc": "言葉の裏に潜む本心を見抜く。心理学判定+15%。"
    },
    "信仰解釈": {
        "base": 5,
        "attribute": ["思弁力", "教養"],
        "status": ["EDU", "POW"],
        "desc": "神々との距離を測る。神秘学・オカルト+10%。"
    },
    "任務完遂術": {
        "base": 3,
        "attribute": ["自律", "遂行力"],
        "status": ["EDU", "DEX"],
        "desc": "任を最後まで遂行する意志。成功率上昇+5%。"
    },
    "慎重分析": {
        "base": 4,
        "attribute": ["判断力", "計画性"],
        "status": ["EDU", "INT"],
        "desc": "罠を踏まず進む術。初見判定にボーナスダイス1。"
    },
    "禁欲精神": {
        "base": 5,
        "attribute": ["精神防衛", "意志力"],
        "status": ["POW", "APP"],
        "desc": "ナメクジ女神の誘惑にも屈せず。魅了判定無効化。"
    }
}

def initialize_session():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "status" not in st.session_state:
        st.session_state.status = {k: 5 for k in ["STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU"]}
    if "exp" not in st.session_state:
        st.session_state.exp = {k: 0 for k in st.session_state.status}
    if "skill_levels" not in st.session_state:
        st.session_state.skill_levels = {skill: 0 for skill in SKILL_DICT}
    if "unlocked_titles" not in st.session_state:
        st.session_state.unlocked_titles = []
    if "log" not in st.session_state:
        st.session_state.log = []
    if "prev_status" not in st.session_state:
        st.session_state.prev_status = st.session_state.status.copy()

# スキル名ごとの称号と獲得条件（Lv）
TITLE_DICT = {
    "睡眠統制": {
        "title": "夢を断つ者",
        "requirement": 5,
        "desc": "眠りの淵に飲まれることなく、己の意志で夢から目覚める者。"
    },
    "朝行動術": {
        "title": "暁に目覚めし者",
        "requirement": 5,
        "desc": "夜を切り裂いて目覚めるその姿は、闇の街に差す陽光のようだ。"
    },
    "体幹維持力": {
        "title": "重力に抗う柱",
        "requirement": 5,
        "desc": "己の軸を失わぬ者は、万象に押されてもなお倒れぬ。"
    },
    "内息制御": {
        "title": "淵より静かなる者",
        "requirement": 5,
        "desc": "吐息ひとつで死線を越える術を知る者。"
    },
    "学習集中術": {
        "title": "知識を焦がす者",
        "requirement": 5,
        "desc": "書物に指を這わせ、言葉を火種に知を燃やす。"
    },
    "発声制御": {
        "title": "異界に響かせる声",
        "requirement": 5,
        "desc": "響きは理を越え、知らぬ言語すら共鳴させる。"
    },
    "受容姿勢": {
        "title": "言葉を飲む聴者",
        "requirement": 5,
        "desc": "語られぬ苦悩を沈黙で包み込む耳を持つ者。"
    },
    "身体整律": {
        "title": "軸を得た者",
        "requirement": 5,
        "desc": "すべての行いが背骨を通り、軌道に乗る。"
    },
    "鉄の意志": {
        "title": "欲望を斬る刃",
        "requirement": 5,
        "desc": "全身の欲動を一点で制する術を得た者。"
    },
    "拳闘技法": {
        "title": "拳に信を宿す者",
        "requirement": 5,
        "desc": "拳の一撃に思想が宿るとき、それは武ではなく祈りとなる。"
    },
    "脚技制動": {
        "title": "空を裂く脚",
        "requirement": 5,
        "desc": "その蹴撃は風すら斬り裂き、影の届かぬところへ至る。"
    },
    "心身調整術": {
        "title": "調和を取り戻す者",
        "requirement": 5,
        "desc": "精神と肉体を一つの流れとし、均衡を保ち続ける者。"
    },
    "推論構築": {
        "title": "紐解きの智者",
        "requirement": 5,
        "desc": "すべての断片は真理への糸口であることを知る者。"
    },
    "認知防御術": {
        "title": "偽りを退ける盾",
        "requirement": 5,
        "desc": "誤謬の海に落ちず、己を保ち続ける理性の番人。"
    },
    "頭脳加算術": {
        "title": "数式の剣",
        "requirement": 5,
        "desc": "一秒の思考で刃を振るう、演算の剣士。"
    },
    "珠算集中法": {
        "title": "螺旋の指先",
        "requirement": 5,
        "desc": "すべての細部に神が宿ることを、掌で知る者。"
    },
    "洞察観察術": {
        "title": "観る者",
        "requirement": 5,
        "desc": "現象の裏に潜む意図と狂気を、その目が捉える。"
    },
    "心理読み": {
        "title": "心奥を穿つ者",
        "requirement": 5,
        "desc": "言葉の底に沈んだ本心をも拾い上げる読解者。"
    },
    "信仰解釈": {
        "title": "異神を解す者",
        "requirement": 5,
        "desc": "人智を越えた神性に理を持ち込む叡智の徒。"
    },
    "任務完遂術": {
        "title": "果てまで届ける者",
        "requirement": 5,
        "desc": "なすべきをなし終える者、信義の実践者。"
    },
    "慎重分析": {
        "title": "一歩先を読む者",
        "requirement": 5,
        "desc": "踏み出す前にすでに勝敗を計る眼を持つ者。"
    },
    "禁欲精神": {
        "title": "欲望の門を封じる者",
        "requirement": 5,
        "desc": "甘き誘惑をもってしても、その門は決して開かれぬ。"
    }
}

# セッション初期化
def initialize_session():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "status" not in st.session_state:
        st.session_state.status = {k: 1 for k in ["STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU"]}
    if "status_exp" not in st.session_state:
        st.session_state.status_exp = {k: 0 for k in st.session_state.status}
    if "exp" not in st.session_state:
        st.session_state.exp = {k: 0 for k in st.session_state.status}  # 旧形式
    if "skill_levels" not in st.session_state:
        st.session_state.skill_levels = {skill: 0 for skill in SKILL_DICT}
    if "unlocked_titles" not in st.session_state:
        st.session_state.unlocked_titles = []
    if "log" not in st.session_state:
        st.session_state.log = []
    if "prev_status" not in st.session_state:
        st.session_state.prev_status = st.session_state.status.copy()

# 経験値倍率（0～5スケールに対応）
def calculate_exp(base: int, level: int) -> float:
    multipliers = [0.0, 0.4, 0.7, 1.0, 1.25, 1.5]
    return round(base * multipliers[level], 2)

# ステータスのレベルアップに必要な指数成長EXP
def get_status_exp_threshold(level: int) -> int:
    return int(10 * (1.5 ** (level - 1)))

# スキル実行による経験値加算（スキル＆対応ステータス）
def apply_exp(skill_name: str, level: int):
    skill = SKILL_DICT[skill_name]
    gained_exp = calculate_exp(skill["base"], level)
    st.session_state.skill_levels[skill_name] += gained_exp
    for stat in skill["status"]:
        st.session_state.status_exp[stat] += gained_exp

# ステータス自動レベルアップ（非公開）
def level_up_status():
    for stat, current_exp in st.session_state.status_exp.items():
        current_level = st.session_state.status[stat]
        threshold = get_status_exp_threshold(current_level)
        while current_exp >= threshold:
            st.session_state.status[stat] += 1
            st.session_state.status_exp[stat] -= threshold
            current_level += 1
            threshold = get_status_exp_threshold(current_level)
            st.session_state.log.append(f"🌟 {stat} に変化が生まれた気がする……")

# 称号解放チェック（スキルレベルに応じて）
def check_title_unlock():
    for skill, (title, req_level) in TITLE_DICT.items():
        if st.session_state.skill_levels[skill] >= req_level:
            if title not in st.session_state.unlocked_titles:
                st.session_state.unlocked_titles.append(title)
                st.session_state.log.append(f"🏅 称号「{title}」を獲得しました！")

# スキル説明取得
def get_skill_description(skill_name: str) -> str:
    return SKILL_DICT[skill_name]["desc"]

# データ保存（すべてマスクデータも含む）
def save_data():
    os.makedirs("data", exist_ok=True)
    pd.DataFrame([st.session_state.status]).to_csv("data/status.csv", index=False)
    pd.DataFrame([st.session_state.status_exp]).to_csv("data/status_exp.csv", index=False)
    pd.DataFrame([st.session_state.skill_levels]).to_csv("data/skills.csv", index=False)
    pd.DataFrame({"称号": st.session_state.unlocked_titles}).to_csv("data/titles.csv", index=False)

# データ読込
def load_data():
    try:
        st.session_state.status = pd.read_csv("data/status.csv").iloc[0].to_dict()
        st.session_state.status_exp = pd.read_csv("data/status_exp.csv").iloc[0].to_dict()
        st.session_state.skill_levels = pd.read_csv("data/skills.csv").iloc[0].to_dict()
        st.session_state.unlocked_titles = pd.read_csv("data/titles.csv")["称号"].tolist()
    except:
        pass