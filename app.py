import streamlit as st
from engine import run_engine

st.title("HYROX RACE ANALYZER (DECISION VERSION)")

st.caption("基準：HYROX 大阪 平均タイムとの比較")

# =========================
# RUN
# =========================
st.subheader("RUN（1km）")

run_min = st.number_input("分", value=4, key="run_min")
run_sec = st.number_input("秒", value=0, min_value=0, max_value=59, key="run_sec")

run_1km_sec = run_min * 60 + run_sec

# =========================
# ROXZONE
# =========================
st.subheader("ROXZONE（合計）")

rox_min = st.number_input("分", value=7, key="rox_min")
rox_sec = st.number_input("秒", value=0, min_value=0, max_value=59, key="rox_sec")

roxzone_total_sec = rox_min * 60 + rox_sec

# =========================
# WORKOUT
# =========================
st.subheader("WORKOUT")

def mmss(label, m, s, key):
    m_v = st.number_input(f"{label} 分", value=m, key=f"{key}_m")
    s_v = st.number_input(f"{label} 秒", value=s, min_value=0, max_value=59, key=f"{key}_s")
    return m_v * 60 + s_v

events = {
    "ski_erg": mmss("Ski Erg", 3, 0, "ski"),
    "sled_push": mmss("Sled Push", 3, 0, "push"),
    "sled_pull": mmss("Sled Pull", 5, 0, "pull"),
    "burpee_broad_jump": mmss("Burpee", 4, 0, "burpee"),
    "row": mmss("Row", 3, 0, "row"),
    "farmer_carry": mmss("Carry", 2, 0, "carry"),
    "sandbag_lunges": mmss("Lunges", 3, 0, "lunges"),
    "wall_ball": mmss("Wall Ball", 6, 0, "wall"),
}

target_time = st.number_input("目標タイム（分）", value=90.0, key="target")

data = {
    "run_1km_sec": run_1km_sec,
    "roxzone_total_sec": roxzone_total_sec,
    "events_sec": events,
    "target_time": target_time
}

if st.button("分析"):

    result = run_engine(data)

    # =========================
    # RESULT
    # =========================
    st.subheader("RESULT")

    st.success(f"予測タイム：{result['total_time_min']:.1f} 分")

    gap = result["total_time_min"] - result["target_time"]

    if gap > 0:
        st.warning(f"目標未達：+{gap:.1f} 分")
    else:
        st.success(f"目標達成：-{abs(gap):.1f} 分")

    st.info(f"到達率：{(result['target_time']/result['total_time_min'])*100:.1f}%")

    # =========================
    # BREAKDOWN
    # =========================
    st.subheader("BREAKDOWN")

    st.write(f"RUN：{result['breakdown']['run']:.1f} 分")
    st.write(f"ROXZONE：{result['breakdown']['roxzone']:.1f} 分")
    st.write(f"WORKOUT：{result['breakdown']['workout']:.1f} 分")

    # =========================
    # WEAKNESS
    # =========================
    st.subheader("WEAKNESS（HYROX 大阪平均との差）")

    for i, (k, rank, sec) in enumerate(result["weakness"]):
        st.write(f"{i+1}. {k}：{rank}（{sec//60}:{sec%60:02d}）")

    # =========================
    # STRATEGY
    # =========================
    st.subheader("NEXT ACTION")

    for a in result["strategy"]["actions"]:
        st.write("・", a)