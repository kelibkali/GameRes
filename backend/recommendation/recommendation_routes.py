import json
import pickle
from typing import Optional

import numpy as np
from datetime import datetime

from scipy.sparse import csr_matrix

game_vectors:Optional[csr_matrix] = None
voca:dict = {}
app_id_to_index:dict = {}
has_chinese_list:list = []
wilson_scores_list: list[float] = []

# 加载预计算矩阵
def load_precomputed():
    global game_vectors,vocab,app_id_to_index,has_chinese_list,wilson_scores_list
    try:
        with open("../data/recommendation/game_vectors.pkl","rb") as f:
            game_vectors ,vocab, app_id_to_index,has_chinese_list,wilson_scores_list = pickle.load(f)
        return True
    except:
        return False

# 构建用户兴趣向量
def build_user_vector(user_games,current_time,vocab):
    user_vector = np.zeros(len(vocab))
    total_weight = 0.0

    for game in user_games:
        play_time = game["playtime_forever"]
        last_played = game["rtime_last_played"]

        if play_time <= 0 or last_played is None:
            continue

        time_diff = current_time - last_played
        weight = play_time / (time_diff+1)
        total_weight += weight

        app_id = game['app_id']
        # TODO:使用别的方式取数据
        try:
            with open(f"../data/steam/game_data/{app_id}.json","r",encoding="utf-8") as f:
                game_data = json.load(f)[str(app_id)]
            for genre in game_data["genres"]:
                EARLY_ACCESS_FACTOR = 1
                if genre["id"] in vocab:
                    if genre["id"] == "70":
                        # TODO:可调节
                        EARLY_ACCESS_FACTOR = 0.001
                    user_vector[vocab[genre["id"]]] += weight * EARLY_ACCESS_FACTOR
        except:
            continue
    # 归一化
    if total_weight > 0:
        user_vector /= total_weight
    return user_vector

def get_recommendations(user_games,current_time,top_n=10,alpha=0.2,chinese_bonus=0.5):
    # 1. 构建用户向量
    user_vector = build_user_vector(user_games,current_time,vocab)

    # 2. 计算余弦相似度
    user_vector_dense = user_vector.astype(np.float32)

    similarities = game_vectors.dot(user_vector_dense)

    wilson_scores = np.array(wilson_scores_list,dtype=np.float32)

    final_scores = (alpha * similarities) + (1 - alpha) * wilson_scores

    if has_chinese_list:
        chinese_indices = np.array(has_chinese_list,dtype=np.int32)
        valid_mask = chinese_indices < len(final_scores)
        final_scores[chinese_indices[valid_mask]] += chinese_bonus

    user_app_ids = {game["app_id"] for game in user_games}
    all_app_ids = list(app_id_to_index.keys())
    mask = np.ones(len(all_app_ids), dtype=bool)

    for app_id in user_app_ids:
        if app_id in app_id_to_index:
            idx = app_id_to_index[app_id]
            mask[idx] = False  # 排除已玩游戏

    scores = final_scores.copy()

    scores[~mask] = -np.inf

    sorted_indices = np.argsort(scores)[::-1]  # 从大到小

    recommended_app_ids = []
    count = 0

    for idx in sorted_indices:
        if scores[idx] == -np.inf:
            break

        app_id = all_app_ids[idx]

        if int(app_id) not in user_app_ids and app_id not in recommended_app_ids:
            recommended_app_ids.append(app_id)
            count += 1

        if count >= top_n:
            break

    return recommended_app_ids

load_precomputed()
steam_id = 76561198850065894

with open(f"../data/steam/user/{steam_id}.json","r",encoding="utf-8") as f:
    user_data = json.load(f)
user_games = user_data["games"]
recommendation_apps = get_recommendations(user_games,datetime.now().timestamp(),top_n=100)
print(recommendation_apps)

for app_id in recommendation_apps:
    try:
        with open(f"../data/steam/game_data/{app_id}.json","r",encoding="utf-8") as f:
            game_data = json.load(f)
            print(game_data[app_id])
    except:
        continue