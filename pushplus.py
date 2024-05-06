import requests
import json


def send_message(token, title, content):
    url = "http://www.pushplus.plus/send"
    data = {"token": token, "title": title, "content": content}
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=body, headers=headers)
    # 解析 JSON 数据
    response_dict = json.loads(response.text)
    # 删除 "data" 字段
    if "data" in response_dict:
        response_dict.pop("data")

    return response_dict
