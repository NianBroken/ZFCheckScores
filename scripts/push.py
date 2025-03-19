import requests
import json
import re
from scripts.ad import get_advertise


# 定义函数send_message，用于发送消息
def send_message(token, title, content):
    # 推送消息的url，格式化字符串以包含token
    url = f"https://push.showdoc.com.cn/server/api/push/{token}"
    # 调用get_advertise函数获取广告内容
    advertise = get_advertise()
    # 如果广告内容不为空，则将广告内容添加到消息内容前
    content = f"{advertise}{content}" if advertise else content
    # 定义正则表达式模式，用于匹配包含“教学班ID”的行
    pattern = re.compile(r"^.*教学班ID.*$\n?", re.MULTILINE)
    # 使用正则表达式替换匹配的行为空字符串，并去除前后的空白字符
    content = re.sub(pattern, "", content).strip()
    # 定义一个字典，用于存储需要替换的字符串及其对应的替换值
    replacements = {
        "------": "\n------\n",  # 替换多连字符为换行后的连字符
        "个人信息：": "<h1>个人信息</h1>\n",  # 替换“个人信息：”为HTML标题标签
        "成绩信息：": "<h1>成绩信息</h1>\n",  # 替换“成绩信息：”为HTML标题标签
        "未公布成绩的课程：": "<h1>未公布成绩的课程</h1>\n",  # 替换“未公布成绩的课程：”为HTML标题标签
        "工作流信息：": "<h1>工作流信息</h1>\n",  # 替换“工作流信息：”为HTML标题标签
        "Copyright © 2024 Klauthmos. All rights reserved.": "Copyright © 2024 <a href='https://www.klaio.top/' target='_blank'>Klauthmos</a>. All rights reserved.",  # 替换版权信息为带有超链接的HTML
    }
    # 遍历字典中的所有键值对，进行替换操作
    for old, new in replacements.items():
        content = content.replace(old, new)
    # 创建一个字典，包含标题和内容
    data = {"title": title, "content": content}
    # 将字典转换为JSON字符串，并编码为UTF-8
    body = json.dumps(data).encode(encoding="utf-8")
    # 定义HTTP请求头，设置内容类型为JSON
    headers = {"Content-Type": "application/json"}
    # 发送POST请求，携带JSON数据和请求头
    response = requests.post(url, data=body, headers=headers)
    # 解析响应的JSON数据，转换为字典
    response_dict = json.loads(response.text)

    # 返回响应字典
    return response_dict
