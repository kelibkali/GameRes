import requests

# 获取指定用户的游戏
# KEY = "94B1007200FF112BB750F4BE9664CAC0"
# 平台用户需要与Steam绑定
# STEAM_ID = "76561198850065894"
# url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={STEAM_ID}&format=json"
# r = requests.get(url)
# with open("t.json", "w") as f:
#     f.write(r.text)
# print(r.text)

# 获取游戏的商店页面

GAME_ID = 0
for GAME_ID in range(10,1000,10):
    u2 = f"https://store.steampowered.com/api/appdetails?appids={GAME_ID}&l=schinese"
    r = requests.get(u2)
    with open(f"./game/{GAME_ID}_data.json", "w",encoding="utf-8") as f:
        f.write(r.text)
    print(r.text)