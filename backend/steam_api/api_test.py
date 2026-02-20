import json

from datetime import datetime
import requests

from steam_api.games_response import GamesResponse

# 获取指定用户的游戏
KEY = "94B1007200FF112BB750F4BE9664CAC0"
# 平台用户需要与Steam绑定
STEAM_ID = "76561198850065894"
url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={STEAM_ID}&format=json&include_appinfo=true"
r = requests.get(url)
gr = GamesResponse(r,int(datetime.now().timestamp()))

for game in gr.games:
    achievement = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={KEY}&steamid={STEAM_ID}&appid={game.app_id}"
    data = requests.get(achievement).json()
    print(data)
    if "achievements" in data["playerstats"]:
        game.achievement = data["playerstats"]["achievements"]
        break
print(gr.to_dict())

# 获取游戏的商店页面

# GAME_ID = 105600
# # for GAME_ID in range(10,1000,10):
# u2 = f"https://store.steampowered.com/api/appdetails?appids={GAME_ID}&l=schinese&cc=CN"
# r = requests.get(u2)
# with open(f"../data/steam/game_data/{GAME_ID}_data.json", "w",encoding="utf-8") as f:
#     f.write(r.text)
# print(r.text)