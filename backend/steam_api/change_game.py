import os
import json
import time

import requests

# 配置目录路径
data_dir = "../data/steam/game_data"


def process_and_update_file(file_path,v=1):
    try:
        # 1. 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 获取内部的游戏详情字典 (假设结构为 { "appid": { ... } })
        if not raw_data:
            return False

        app_id = list(raw_data.keys())[0]
        data = raw_data[app_id]
        # print(f"正在处理: {app_id}")
        if v == 1:
            if "supported_languages" in data:
                supported_languages = data["supported_languages"]
                if "中文" in supported_languages:
                    has_chinese = "true"
                else:
                    has_chinese = "false"
            else:
                supported_languages = ""
                has_chinese = "false"

            if "app_reviews" not in data:
                print(f"✅ 正在更新: {app_id}")
                url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&language=schinese"
                response = requests.get(url)
                response_data = response.json()
                try:
                    app_reviews = {
                        "review_score_desc": response_data["query_summary"]["review_score_desc"],
                        "total_positive": response_data["query_summary"]["total_positive"],
                        "total_negative": response_data["query_summary"]["total_negative"],
                        "total_reviews": response_data["query_summary"]["total_reviews"],
                    }
                except:
                    app_reviews = {
                        "review_score_desc": "",
                        "total_positive": 0,
                        "total_negative": 0,
                        "total_reviews": 0
                    }
                data["app_reviews"] = app_reviews
            else:
                print(f"{app_id}:{data["app_reviews"]["review_score_desc"]}")

            # 3. 添加/更新字段到数据对象中
            # 这里我们将 supported_languages 和 has_chinese 都写回去
            # 如果原本就有 supported_languages，这会更新它（值不变）；如果没有，则添加
            data["supported_languages"] = supported_languages
            data["has_chinese"] = has_chinese
        elif v == 2:
            if "type" not in data:
                print(f"✅ 正在更新: {app_id}")
                url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=schinese&cc=CN"
                response = requests.get(url)
                response_data = response.json()
                try:
                    type =  response_data[f"{app_id}"]["data"]["type"]
                except:
                    type = "none"
                data["type"] = type
            else:
                print(f"{app_id}:{data["type"]}")

        # 4. 写回文件 (覆盖原文件)
        with open(file_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False 保证中文正常显示，indent=2 保持格式美观
            json.dump(raw_data, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时出错: {e}")
        return False


def main():
    if not os.path.exists(data_dir):
        print(f"❌ 错误：目录 {data_dir} 不存在。")
        print("请检查路径是否正确，或者尝试使用绝对路径。")
        return

    success_count = 0
    fail_count = 0

    print(f"开始处理目录：{os.path.abspath(data_dir)} ...")

    # 遍历目录下所有文件
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(data_dir, filename)
            if process_and_update_file(file_path,2):
                success_count += 1
                # 可选：打印成功信息，如果文件太多可以注释掉下面这行
                # print(f"✅ 已更新: {filename}")
            else:
                fail_count += 1
            if (success_count + fail_count) % 200 == 0:
                time.sleep(5*60)

    print("-" * 30)
    print(f"🎉 处理完成！")
    print(f"✅ 成功更新: {success_count} 个文件")
    print(f"❌ 失败: {fail_count} 个文件")
    print(f"新字段 'has_chinese' 已添加到成功的文件中。")


if __name__ == "__main__":
    main()