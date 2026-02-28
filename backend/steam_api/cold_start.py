# 抓取游戏数据
# 需要保存的信息：type,name,steam_appid,is_free,about_the_game,supported_languages
# header_image,developers,publishers,price_overview,categories,genres
import json
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor

import datetime
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

        if "type" in data:
            self.type = data["type"]
        else:
            self.type = "none"

        if "supported_languages" in data:
            self.supported_languages = data["supported_languages"]
            if "中文" in self.supported_languages:
                self.has_chinese = "true"
            else:
                self.has_chinese = "false"
        else:
            self.supported_languages = ""
            self.has_chinese = "false"

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

        if "achievements" in data:
            self.achievements = data["achievements"]
        else:
            self.achievements = "none"

        url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&language=schinese"
        response = requests.get(url)
        data = response.json()
        try:
            app_reviews = {
                "review_score_desc":data["query_summary"]["review_score_desc"],
                "total_positive":data["query_summary"]["total_positive"],
                "total_negative":data["query_summary"]["total_negative"],
                "total_reviews":data["query_summary"]["total_reviews"],
            }
        except:
            app_reviews = {
                "review_score_desc":"",
                "total_positive":0,
                "total_negative":0,
                "total_reviews":0
            }
        self.app_reviews = app_reviews
        with open(f"../data/steam/game_data/{app_id}.json","w",encoding="utf-8") as file:
            json.dump(
                self.to_dict(),
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.close()

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
            "achievements": self.achievements,
            "has_chinese":self.has_chinese,
            "app_reviews":self.app_reviews,
            "type":self.type,
        }}

# with open("../data/steam/user/76561198850065894.json","r") as file:
#     user_data = json.load(file)
#
# for game in user_data["games"]:
#     print(game)
#     # if not os.path.exists(f"../data/steam/game_data/{game['app_id']}.json"):
#     GameData(game["app_id"])

total = 470000

batch_size = 195

interval = 5.5 * 60
start_index = 166584
# start_index = 430000

def GameDataFun(app_id):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {app_id}")
    try:
        GameData(app_id)
    except Exception as e:
        print(e)

def execute_batch(start_i,batch_num):
    end_i = min(start_i + batch_size, total+1)
    print(f"\n=== {batch_num} 个开始: app_id={start_i}~{end_i - 1}, 时间: {datetime.datetime.now().strftime('%H:%M:%S')} ===")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(start_i,end_i):
            if not os.path.exists(f"../data/steam/game_data/{i*10}.json"):
                futures.append(executor.submit(GameDataFun, i * 10))

        for future in futures:
            future.result()
    print(f"=== {batch_num} 个完成，已处理 {end_i - 1}/{total} 条 ===\n")
    return end_i

def scheduled_runner():
    batch_num = 1
    current_index = start_index
    while current_index < total:
        current_index = execute_batch(current_index,batch_size)
        batch_num += 1

        if current_index <= total:
            print(f"Wait {interval} seconds...")
            time.sleep(interval)
    print("finish!")

if __name__ == "__main__":
    try:
        scheduled_runner()
        # GameData(10)
    except KeyboardInterrupt:
        print("\n程序已停止")