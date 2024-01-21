import requests
import json
import os


def send_message(title, content):
    token = os.environ.get("TOKEN")
    url = "http://www.pushplus.plus/send"
    data = {"token": token, "title": title, "content": content}
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=body, headers=headers)

    return response.text
