import os
import requests

# 定义常量URL
AD_URL = "https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/data/advertise.txt"
NO_AD_USERS_LIST_URL = "https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/data/no_ad_users_list.txt"

# 定义本地数据存储路径
FOLDER_PATH = "data"
INFO_FILE_PATH = os.path.join(FOLDER_PATH, "info.txt")

# 从文件中读取当前用户
try:
    with open(INFO_FILE_PATH, "r") as info_file:
        CURRENT_USER = info_file.read().strip()
except Exception:
    CURRENT_USER = "None"


# 发送HTTP GET请求获取指定URL的内容
def fetch_content(url):
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else None
    except Exception:
        return None


# 获取免广告用户列表
def get_no_ad_users_list():
    try:
        return fetch_content(NO_AD_USERS_LIST_URL) or []
    except Exception:
        return []


# 获取广告内容
def get_advertise():
    try:
        # 获取免广告用户列表
        no_ad_users_list = get_no_ad_users_list()

        # 如果当前用户不在免广告用户列表中，获取广告内容
        if CURRENT_USER not in no_ad_users_list:
            ad_content = fetch_content(AD_URL)
            return ad_content
        # 当前用户在免广告用户列表中，不推送广告
        else:
            return None
    except Exception:
        return None
