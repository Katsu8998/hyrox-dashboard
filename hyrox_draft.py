import streamlit as st
import pandas as pd
from datetime import timedelta

# --------------------------
# ユーティリティ関数
# --------------------------
def parse_time_input(input_str: str) -> float:
    """1m30s形式 → 分(float)"""
    if not input_str:
        return None
    input_str = str(input_str).strip().lower()
    try:
        minutes, seconds = 0, 0
        if "m" in input_str:
            minutes = int(input_str.split("m")[0])
            input_str = input_str.split("m")[1]
        if "s" in input_str:
            seconds = int(input_str.replace("s",""))
        elif input_str:
            seconds = int(input_str)
        return minutes + seconds / 60
    except:
        return None

def hhmmss_to_minutes(time_str):
    """HH:MM:SS または MM:SS 形式 → 分(float)"""
    if pd.isna(time_str) or time_str == "":
        return None
    try:
        parts = time_str.split(":")
        if len(parts) == 3:
            h, m, s = parts
        elif len(parts) == 2:
            h, m, s = 0, parts[0], parts[1]
        else:
            return None
        return int(h)*60 + int(m) + int(s)/60
    except:
        return None

def minutes_to_hhmmss(minutes) -> str:
    """分(float) → hh:mm:ss 文字列"""
    if minutes is None:
        return ""
    try:
        total_seconds = int(float(minutes) * 60)
        return str(timedelta(seconds=total_seconds))
    except:
        return ""

def calculate_achievement(record, target):
    try:
        if record is None or target is None:
            return None
        return min(100, 100 * target / record)
    except:
        return None

def calculate_improvement(current, previous):
    try:
        if current is None or previous is None:
            return None
        return 100 * (previous - current) / previous
    except:
        return None

# --------------------------
# 種目一覧
# --------------------------
event_columns = [
    "Ski 1000m", "Row 1000m", "Farmer Carry 200m",
    "Sled Push 50m", "Sled Pull 50m", "Burpee Broad Jump 80m",
    "Sandbag Lunges 100m", "Wall Balls", "Run 1000m"
]

# --------------------------
# Streamlit 設定
# --------------------------
st.set_page_config(page_title="Hyrox トレーニング管理", layout="wide")
st.title("🏋️‍♂️ Hyrox トレーニング管理アプリ")

# --------------------------
# 過去TSVアップロード
# --------------------------
st.header("📁 過去のトレーニングTSVをアップロード")
uploaded_file = st.file_uploader("TSVを選択", type="tsv")
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, sep="\t")
        df['日付'] = pd.to_datetime(df['日付'], errors='coerce')
        # TSVの時間を float に統一
        for col in event_columns:
            df[col] = df[col].apply(lambda x: hhmmss_to_minutes(str(x)))
    except Exception as e:
        st.error(f"TSV読み込みエラー: {e}")
        df = pd.DataFrame(columns=["日付"] + event_columns)
else:
    df = pd.DataFrame(columns=["日付"] + event_columns)

# --------------------------
# 今日のトレーニング入力
# --------------------------
st.header("📝 今日のトレーニング記録")
date = st.date_input("日付")
inputs = {}
cols = st.columns(2)
for i, col_name in enumerate(event_columns):
    col = cols[i % 2]
    inputs[col_name] = col.text_input(f"{col_name} 実測タイム (例:1m30s)")

if st.button("記録追加"):
    new_record = {"日付": pd.to_datetime(date)}
    for col_name in event_columns:
        new_record[col_name] = parse_time_input(inputs[col_name])  # float
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    st.success("✅ 今日の記録を追加しました！")

# --------------------------
# 目標タイム入力
# --------------------------
st.header("🎯 各種目の目標タイム設定")
target_times = {}
cols = st.columns(2)
for i, col_name in enumerate(event_columns):
    col = cols[i % 2]
    target_input = col.text_input(f"{col_name} 目標タイム (例:1m30s)")
    target_times[col_name] = parse_time_input(target_input) if target_input else None

# --------------------------
# 過去記録表示＆計算
# --------------------------
if not df.empty:
    # 日付順にソート
    df = df.sort_values('日付').reset_index(drop=True)

    # 計算用 float データ
    calc_df = df.copy()

    # 達成率
    for col in event_columns:
        if target_times[col] is not None:
            calc_df[f"{col} 達成率 (%)"] = calc_df[col].apply(lambda x: calculate_achievement(x, target_times[col]))

    # 改善率
    for col in event_columns:
        improvement = [None]
        for i in range(1, len(calc_df)):
            improvement.append(calculate_improvement(calc_df[col].iloc[i], calc_df[col].iloc[i-1]))
        calc_df[f"{col} 改善率 (%)"] = improvement

    # 表示用 HH:MM:SS に変換
    display_df = calc_df.copy()
    for col in event_columns:
        display_df[col] = display_df[col].apply(minutes_to_hhmmss)

    st.header("📊 過去の記録と達成率・改善率")
    st.dataframe(display_df.round(1))

    # TSV保存
    st.header("💾 TSV保存")
    tsv_data = display_df.to_csv(index=False, sep="\t", encoding="utf-8-sig", lineterminator="\r\n")
    st.download_button(
        label="TSVをダウンロード",
        data=tsv_data,
        file_name="hyrox_records.tsv",
        mime="text/tab-separated-values"
    )

# --------------------------
# 入力例表示
# --------------------------
st.markdown("""
**入力例**
- Ski 1000m: 4m20s
- Row 1000m: 3m50s
- Farmer Carry 200m: 1m30s
- Sled Push 50m: 0m50s
- Sled Pull 50m: 0m55s
- Burpee Broad Jump 80m: 3m0s
- Sandbag Lunges 100m: 2m0s
- Wall Balls: 2m30s
- Run 1000m: 4m0s

※秒単位は `s`、分単位は `m` で入力（例: 1m30s → 自動的に 1.5 分に変換）
""")
