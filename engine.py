import config

# =========================
# 弱点分析（基準比較）
# =========================
def analyze_weakness(events_sec):

    base = config.HYROX_BASE

    result = []

    for k, v in events_sec.items():

        avg = base[k]
        ratio = v / avg

        if ratio < 0.8:
            rank = "S（トップレベル）"
        elif ratio < 1.0:
            rank = "A（平均以上）"
        elif ratio < 1.2:
            rank = "B（平均）"
        elif ratio < 1.5:
            rank = "C（改善必要）"
        else:
            rank = "D（大きな弱点）"

        result.append((k, rank, v))

    return sorted(result, key=lambda x: x[2], reverse=True)


# =========================
# 戦略（意思決定）
# =========================
def build_strategy(total_min, fatigue, weakest):

    # レース可否判断
    if total_min <= 90 and fatigue < 30:
        mode = "レース推奨"
        reason = "90分内・疲労安定"
    else:
        mode = "トレーニング優先"
        reason = "完走リスク or 後半失速リスク"

    actions = []

    for k, rank, _ in weakest:

        if rank in ["C（改善必要）", "D（大きな弱点）"]:
            actions.append(f"{k}：重点強化（出力 or 技術改善）")

    return {
        "mode": mode,
        "reason": reason,
        "actions": actions[:3]
    }


# =========================
# メイン
# =========================
def run_engine(data):

    run_sec = data["run_1km_sec"]
    rox_sec = data["roxzone_total_sec"]
    events_sec = data["events_sec"]
    target = data["target_time"]

    # =========================
    # RUN（1km×8）
    # =========================
    run_total = 0

    for i in range(8):
        fatigue_factor = 1 + (i * 0.03)
        run_total += run_sec * fatigue_factor

    # =========================
    # ROXZONE（実測）
    # =========================
    rox_total = rox_sec

    # =========================
    # WORKOUT
    # =========================
    workout_total = sum(events_sec.values())

    # =========================
    # TOTAL
    # =========================
    total_sec = run_total + rox_total + workout_total
    total_min = total_sec / 60

    # =========================
    # FATIGUE
    # =========================
    fatigue = (rox_total + workout_total) / 10

    # =========================
    # WEAKNESS
    # =========================
    weakness = analyze_weakness(events_sec)

    # =========================
    # STRATEGY
    # =========================
    strategy = build_strategy(total_min, fatigue, weakness)

    # =========================
    # BREAKDOWN
    # =========================
    breakdown = {
        "run": run_total / 60,
        "roxzone": rox_total / 60,
        "workout": workout_total / 60
    }

    return {
        "total_time_min": total_min,
        "target_time": target,
        "breakdown": breakdown,
        "weakness": weakness,
        "fatigue": fatigue,
        "strategy": strategy
    }