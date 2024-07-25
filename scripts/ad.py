import requests


def advertise():
    ad_content = ""
    try:
        ad_url = "https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/data/advertise.txt"
        # 发送HTTP GET请求获取内容
        response = requests.get(ad_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 输出内容
            ad_content = f"{response.text}\n------"
        return ad_content
    except Exception:
        return ad_content
