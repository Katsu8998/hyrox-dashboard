# strategy.py

def strategy(data, p2, fatigue):

    run = data["run_5000m"]
    f = fatigue["final_fatigue"]

    base_pace = run / 5

    # -----------------------
    # ペース設計
    # -----------------------
    start_pace = base_pace * (1 - f * 0.05)
    mid_pace = base_pace
    end_pace = base_pace * (1 + f * 0.20)

    # -----------------------
    # 弱点特定
    # -----------------------
    weakest = p2["weakness"][0][0]

    # -----------------------
    # リスクゾーン判定
    # -----------------------
    if weakest in ["wall_ball", "burpee_broad_jump"]:
        risk_zone = "後半崩壊リスク（高）"
    else:
        risk_zone = "安定"

    # -----------------------
    # 戦略タイプ
    # -----------------------
    if f > 1.5:
        strategy_type = "守備型（前半抑制）"
    elif f > 1.0:
        strategy_type = "バランス型"
    else:
        strategy_type = "攻撃型（押し切り）"

    # -----------------------
    # 改善アクション
    # -----------------------
    advice = []

    mapping = {
        "sled_push": "スレッド強化",
        "sled_pull": "引き系強化",
        "wall_ball": "心拍耐性強化",
        "burpee_broad_jump": "無酸素持久改善",
        "row": "有酸素維持強化"
    }

    if weakest in mapping:
        advice.append(mapping[weakest])

    return {
        "start_pace": start_pace,
        "mid_pace": mid_pace,
        "end_pace": end_pace,
        "risk_zone": risk_zone,
        "strategy_type": strategy_type,
        "advice": advice
    }