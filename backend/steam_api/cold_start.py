# 抓取游戏数据
# 需要保存的信息：type,name,steam_appid,is_free,about_the_game,supported_languages
# header_image,developers,publishers,price_overview,categories,genres
import json
import os

import requests

class GameData:
    def __init__(self,app_id):
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=schinese&cc=CN"
        response = requests.get(url)
        print(response.json())
        if "data" not in response.json()[f"{app_id}"]:
            return
        data = response.json()[f"{app_id}"]["data"]

        self.app_id = app_id
        self.name = data["name"]
        self.steam_appid = data["steam_appid"]
        self.required_age = data["required_age"]
        self.is_free = data["is_free"]
        self.description = data["about_the_game"]

        if "supported_languages" in data:
            self.supported_languages = data["supported_languages"]
        else:
            self.supported_languages = ""

        self.header_image = data["header_image"]
        self.header_image = data["header_image"]

        if "developers" in data:
            self.developers = data["developers"]
        else:
            self.developers = []

        if "publishers" in data:
            self.publishers = data["publishers"]
        else:
            self.publishers = []

        if "price_overview" in data:
            self.price_overview = data["price_overview"]
        else:
            self.price_overview = {}
        self.release_date = data["release_date"]
        if "categories" in data:
            self.categories = data["categories"]
        else:
            self.categories = []
        if "genres" in data:
            self.genres = data["genres"]
        else:
            self.genres = []

        with open(f"../data/steam/game_data/{app_id}.json","w",encoding="utf-8") as file:
            json.dump(
                self.to_dict(),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def to_dict(self):
        return {self.app_id: {
            "name": self.name,
            "steam_appid": self.steam_appid,
            "required_age": self.required_age,
            "is_free": self.is_free,
            "description": self.description,
            "supported_languages": self.supported_languages,
            "header_image": self.header_image,
            "developers": self.developers,
            "publishers": self.publishers,
            "price_overview": self.price_overview,
            "release_date": self.release_date,
            "categories": self.categories,
            "genres": self.genres,
        }}

# with open("../data/steam/user/76561198850065894.json","r") as file:
#     user_data = json.load(file)
#
# for game in user_data["games"]:
#     print(game)
#     if not os.path.exists(f"../data/steam/game_data/{game['app_id']}.json"):
#         GameData(game["app_id"])
