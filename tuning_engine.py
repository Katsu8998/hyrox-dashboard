from engine import run_engine
import copy

def compute_error(pred_time, actual_time):
    return actual_time - pred_time


def tune_weights(data, actual_time, base_config):

    best_config = copy.deepcopy(base_config)

    # 初期予測
    pred = run_engine(data)
    pred_time = pred["p2"]["hyrox_index"]  # 仮の時間スケール

    error = compute_error(pred_time, actual_time)

    # -------------------------
    # ① P2補正（ラン影響）
    # -------------------------
    if error > 0:  # 遅く見積もりすぎ
        best_config["RUN_WEIGHT"] += 0.5
    else:
        best_config["RUN_WEIGHT"] -= 0.5

    # -------------------------
    # ② 疲労係数補正
    # -------------------------
    fatigue = pred["p2"]["fatigue_total"]

    if fatigue > 1200:
        best_config["FATIGUE_SCALE"] += 0.1
    else:
        best_config["FATIGUE_SCALE"] -= 0.05

    # -------------------------
    # ③ 種目補正（wall ball / sled）
    # -------------------------
    if error > 0:
        best_config["FATIGUE_WEIGHT"]["wall_ball"] += 0.2
        best_config["FATIGUE_WEIGHT"]["sled_push"] += 0.1

    return best_config, error