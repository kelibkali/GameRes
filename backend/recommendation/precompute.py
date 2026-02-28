import json
import math
import os

import scipy.sparse as sp
import pickle

def wilson_score(positive,total,confidence = 1.96):
    if total == 0:
        return 0
    p = positive / total
    score = (p + (confidence**2)/(2*total) - confidence * math.sqrt((p*(1-p) + (confidence**2)/(4*total))/total)) / (1 + (confidence**2)/total)
    return score

def games_genres():
    games = []
    # TODO:Redis缓存
    file_path = "../data/steam/game_data"
    json_list = os.listdir(file_path)
    for path in json_list:
        json_path = os.path.join(file_path, path)
        with open(json_path, "r",encoding="utf-8") as f:
            data = json.load(f)
            app_id = list(data.keys())[0]
            score = wilson_score(data[app_id]["app_reviews"]["total_positive"],data[app_id]["app_reviews"]["total_reviews"])
            games.append({
                "app_id":app_id,
                "genres":data[app_id]["genres"],
                "has_chinese": data[app_id]["has_chinese"],
                "wilson_score": score,
            })
    return games

def build_sparse_game_vectors(games):
    # 1. 构建 genre 词汇表
    genre_ids = set()

    for game in games:
        if game["type"] == "game":
            for genre in game["genres"]:
                genre_ids.add(genre["id"])
    print(genre_ids)
    vocab = { genre_id : idx for idx, genre_id in  enumerate(sorted(genre_ids)) }
    num_genres = len(genre_ids)

    # 2. 准备CSR矩阵的数据
    rows,cols,data = [],[],[]
    app_id_to_index = {}
    has_chinese_list = []
    wilson_scores_list = []
    for idx, game in enumerate(games):
        app_id = game["app_id"]
        app_id_to_index[app_id] = idx
        if game["has_chinese"] == "true":
            has_chinese_list.append(idx)
        wilson_scores_list.append(game["wilson_score"])

        for genre in game["genres"]:
            if genre["id"] in vocab:
                rows.append(idx)
                cols.append(vocab[genre["id"]])
                data.append(1) # 表示包含

    # 3. 构建 游戏-类型 二分图
    game_vectors = sp.csr_matrix((data, (rows, cols)), shape=(len(games), num_genres))

    print(f"CSR matrix shape: {game_vectors.shape}")
    print(f"Memory usage: {game_vectors.data.nbytes/1e6:.2f} MB")
    return game_vectors, vocab, app_id_to_index, has_chinese_list,wilson_scores_list

games = games_genres()
game_vectors, vocab, app_id_to_index,has_chinese_list,wilson_scores_list = build_sparse_game_vectors(games)
with open("../data/recommendation/game_vectors.pkl", "wb") as f:
    pickle.dump((game_vectors,vocab,app_id_to_index,has_chinese_list,wilson_scores_list), f)