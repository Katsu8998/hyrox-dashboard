# fatigue_model.py

def fatigue_curve(data):

    events = data["events"]

    fatigue = 0
    curve = []

    # -----------------------
    # 種目別疲労係数（競技構造ベース）
    # -----------------------
    weight = {
        "ski_erg": 0.7,
        "sled_push": 1.8,
        "sled_pull": 1.6,
        "burpee_broad_jump": 2.0,
        "row": 0.8,
        "farmer_carry": 1.0,
        "sandbag_lunges": 1.7,
        "wall_ball": 2.3
    }

    # -----------------------
    # 疲労蓄積（累積モデル）
    # -----------------------
    for k, v in events.items():

        impact = v * weight[k]

        # 後半加速（SSAC構造）
        fatigue += impact * 0.015

        curve.append({
            "station": k,
            "impact": impact,
            "fatigue": fatigue
        })

    return {
        "curve": curve,
        "final_fatigue": fatigue
    }