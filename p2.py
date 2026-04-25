# p2.py

def p2_analysis(data):

    run = data["run_5000m"]
    events = data["events"]

    # -----------------------
    # RUN能力（有酸素ベース）
    # -----------------------
    run_score = max(0, 100 - (run - 20.0) * 8)

    # -----------------------
    # 種目別スコア
    # -----------------------
    station_scores = {}

    baseline = 200

    for k, v in events.items():

        score = max(0, 100 - (v - baseline) * 0.25)
        station_scores[k] = score

    # -----------------------
    # 筋持久力
    # -----------------------
    strength_score = sum(station_scores.values()) / len(station_scores)

    # -----------------------
    # 疲労耐性（後半重要領域）
    # -----------------------
    fatigue_score = (
        station_scores.get("sled_push", 50) * 0.3 +
        station_scores.get("burpee_broad_jump", 50) * 0.4 +
        station_scores.get("wall_ball", 50) * 0.3
    )

    # -----------------------
    # 弱点ランキング
    # -----------------------
    weakness = sorted(station_scores.items(), key=lambda x: x[1])

    # -----------------------
    # 総合能力（P2スコア）
    # -----------------------
    hyrox_index = (
        run_score * 0.45 +
        strength_score * 0.35 +
        fatigue_score * 0.20
    )

    return {
        "run_score": run_score,
        "strength_score": strength_score,
        "fatigue_score": fatigue_score,
        "station_scores": station_scores,
        "weakness": weakness,
        "hyrox_index": hyrox_index
    }