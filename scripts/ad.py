import os
import requests

# 定义常量URL，广告内容的URL
AD_URL = "https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/data/advertise.txt"
# 定义常量URL，免广告用户列表的URL
NO_AD_USERS_LIST_URL = "https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/data/no_ad_users_list.txt"

# 定义本地数据存储的文件夹路径
FOLDER_PATH = "data"
# 定义本地信息文件的路径
INFO_FILE_PATH = os.path.join(FOLDER_PATH, "info.txt")

# 从文件中读取当前用户
try:
    with open(INFO_FILE_PATH, "r") as info_file:  # 尝试打开本地信息文件并读取内容
        CURRENT_USER = info_file.read().strip()  # 读取文件内容并去除首尾空格，赋值给CURRENT_USER
except Exception:  # 如果读取文件发生异常
    CURRENT_USER = "None"  # 将CURRENT_USER设为"None"


# 发送HTTP GET请求获取指定URL的内容
def fetch_content(url):  # 定义函数fetch_content，参数为url
    try:
        response = requests.get(url)  # 发送HTTP GET请求
        return response.text if response.status_code == 200 else None  # 如果响应状态码是200，返回响应内容，否则返回None
    except Exception:  # 如果请求过程中发生异常
        return None  # 返回None


# 获取免广告用户列表
def get_no_ad_users_list():  # 定义函数get_no_ad_users_list
    try:
        return fetch_content(NO_AD_USERS_LIST_URL) or []  # 尝试获取免广告用户列表内容，如果失败返回空列表
    except Exception:  # 如果过程中发生异常
        return []  # 返回空列表


# 获取广告内容
def get_advertise():  # 定义函数get_advertise
    try:
        no_ad_users_list = get_no_ad_users_list()  # 获取免广告用户列表

        if CURRENT_USER not in no_ad_users_list:  # 如果当前用户不在免广告用户列表中
            ad_content = fetch_content(AD_URL)  # 获取广告内容
            return ad_content  # 返回广告内容
        else:  # 当前用户在免广告用户列表中
            return None  # 不推送广告，返回None
    except Exception:  # 如果过程中发生异常
        return None  # 返回None
