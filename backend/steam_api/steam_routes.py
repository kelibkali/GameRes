import json
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
import os

import requests
from flask import Blueprint

from config.settings import (steam_key)
from models.Message import Message, MsgType
from steam_api.games_response import GamesResponse

steam_api_bp = Blueprint('steam_api', __name__,url_prefix='/api/steam')

KEY = steam_key

USER_PATH = "./data/steam/user"

GAME_PATH = "./data/steam/game_data"

ONE_DAY_SECONDS = 24*60*60

def get_games(STEAM_ID:str) -> GamesResponse:
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={STEAM_ID}&format=json"
    r = requests.get(url)
    gr = GamesResponse(r, int(datetime.now().timestamp()))

    def fetch_achievement(game,index):
        achievement_url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={KEY}&steamid={STEAM_ID}&appid={game.app_id}"
        try:
            data = requests.get(achievement_url).json()
            print(data)
            if data and "playerstats" in data and "achievements" in data["playerstats"]:
                return index,data["playerstats"]["achievements"]
        except Exception as e:
            print(f"failed to get achievements for {game.app_id}: {e}")
        return index,None

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_index = {
            executor.submit(fetch_achievement,game,i): i for i, game in enumerate(gr.games)
        }

        results = {}
        for future in as_completed(future_to_index):
            index,achievements = future.result()
            if achievements:
                results[index] = achievements

    for index,achievements in results.items():
        gr.games[index].set_achievements(achievements)

    return gr

def gen_games(steam_id):
    data = {}
    # 如果不存在用户的记录 -> 获取记录和记录的时间戳
    if not os.path.exists(f"{USER_PATH}/{steam_id}.json"):
        data = get_games(steam_id).to_dict()
        with open(f"{USER_PATH}/{steam_id}.json", "w") as f:
            f.write(json.dumps(data))
    else:
        with open(f"{USER_PATH}/{steam_id}.json","r") as f:
            data = json.load(f)

    # 如果存在 -> 直接使用 如果记录时间戳大于一天 更新记录
    last_update = data["update_timestamp"]
    if int(datetime.now().timestamp()) - last_update > ONE_DAY_SECONDS:
        data = get_games(steam_id).to_dict()
        with open(f"{USER_PATH}/{steam_id}.json", "w") as f:
            f.write(json.dumps(data))

@steam_api_bp.route('/game_list/<steam_id>')
def game_list(steam_id):
    gen_games(steam_id)
    data = {
        "games": []
    }

    # 读取文件
    user_file_path = f"{USER_PATH}/{steam_id}.json"
    user_data = json.load(open(user_file_path,encoding="utf-8"))

    data["game_count"] = user_data["game_count"]
    for game in user_data["games"]:
        g = game
        game_data_file_path = f"{GAME_PATH}/{game["app_id"]}.json"
        if not os.path.exists(game_data_file_path):
            continue
        g_data = json.load(open(game_data_file_path,encoding="utf-8"))[f"{game["app_id"]}"]
        g["name"] = g_data["name"]
        g["steam_appid"] = g_data["steam_appid"]
        g["header_image"] = g_data["header_image"]
        if "total" in g_data["achievements"]:
            g["achievements_total"] = g_data["achievements"]["total"]
        else:
            g["achievements_total"] = 0
        data["games"].append(g)

    return Message(msg_type=MsgType.SUCCESS,message="success",data=data).to_dict()