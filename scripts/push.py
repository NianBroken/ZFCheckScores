import requests
import json
import re
from scripts.ad import advertise


def send_message(token, title, content):
    url = f"https://push.showdoc.com.cn/server/api/push/{token}"
    content = advertise() + content
    pattern = re.compile(r"^.*教学班ID.*$\n?", re.MULTILINE)
    content = re.sub(pattern, "", content).strip()
    replacements = {
        "------": "\n------\n",
        "个人信息：": "<h1>个人信息</h1>\n",
        "成绩信息：": "<h1>成绩信息</h1>\n",
        "未公布成绩的课程：": "<h1>未公布成绩的课程</h1>\n",
        "异常的课程：": "<h1>异常的课程</h1>\n",
        "工作流信息：": "<h1>工作流信息</h1>\n",
        "Copyright © 2024 NianBroken. All rights reserved.": "Copyright © 2024 <a href='https://www.nianbroken.top/' target='_blank'>NianBroken</a>. All rights reserved.",
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    data = {"title": title, "content": content}
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=body, headers=headers)
    # 解析 JSON 数据
    response_dict = json.loads(response.text)

    return response_dict
