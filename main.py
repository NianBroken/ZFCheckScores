import base64
import hashlib
import os
import sys
from pprint import pprint
from zfn_api import Client
from pushplus import send_message

# 从环境变量获取教务系统的URL、用户名和密码
url = os.environ.get("URL")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


# 定义一个md5加密的封装函数
def md5_encrypt(string):
    byte_string = string.encode()
    md5_object = hashlib.md5(byte_string)
    return md5_object.hexdigest()


# 初始化相关变量
cookies = {}
base_url = url
raspisanie = []
ignore_type = []
detail_category_type = []
timeout = 5

# 创建教务系统客户端对象
stu = Client(
    cookies=cookies,
    base_url=base_url,
    raspisanie=raspisanie,
    ignore_type=ignore_type,
    detail_category_type=detail_category_type,
    timeout=timeout,
)

# 如果cookies为空字典，则进行登录
if not cookies:
    login_result = stu.login(username, password)

    if login_result["code"] == 1001:
        # 如果需要验证码，获取验证码并进行登录
        verify_data = login_result["data"]
        with open(os.path.abspath("kaptcha.png"), "wb") as pic:
            pic.write(base64.b64decode(verify_data.pop("kaptcha_pic")))
        verify_data["kaptcha"] = input("输入验证码：")
        login_result = stu.login_with_kaptcha(**verify_data)

        if login_result["code"] != 1000:
            pprint(login_result)
            sys.exit()
        pprint(login_result)

    elif login_result["code"] != 1000:
        pprint(login_result)
        sys.exit()

# 获取个人信息
info = stu.get_info()["data"]

# 整合个人信息
integrate_info = (
    f"个人信息：\n" f"学号：{info['sid']}\n" f"班级：{info['class_name']}\n" f"姓名：{info['name']}"
)

# 定义firstrun.txt文件变量
firstrun_file_path = "firstrun.txt"

# 如果firstrun.txt文件不存在，创建并写入true
if not os.path.exists(firstrun_file_path):
    with open(firstrun_file_path, "w") as firstrun_file:
        firstrun_file.write("true")

# 第一次运行则运行两遍，否则运行一遍
run_count = 2 if open(firstrun_file_path).read() == "true" else 1

for _ in range(run_count):
    # 如果grade.txt文件不存在，创建文件
    if not os.path.exists("grade.txt"):
        open("grade.txt", "w").close()

    # 清空old_grade.txt文件内容
    with open("old_grade.txt", "w") as old_grade_file:
        old_grade_file.truncate()

    # 将grade.txt文件中的内容写入到old_grade.txt文件内。
    with open("grade.txt", "r") as grade_file, open(
        "old_grade.txt", "w"
    ) as old_grade_file:
        old_grade_file.write(grade_file.read())

    # 清空grade.txt文件内容
    with open("grade.txt", "w") as grade_file:
        grade_file.truncate()

    # 获取成绩信息
    grade = stu.get_grade("")["data"]["courses"]

    # 按照提交时间降序排序
    sorted_grade = sorted(grade, key=lambda x: x["submission_time"], reverse=True)

    # 初始化输出成绩信息字符串
    integrated_grade_info = "成绩信息："

    # 遍历前8条按时间降序排序后的成绩列表
    for i, course in enumerate(sorted_grade[:8]):
        # 整合成绩信息
        integrated_grade_info += (
            f"\n课程ID: {course['course_id']}\n"
            f"课程名称: {course['title']}\n"
            f"任课教师: {course['teacher']}\n"
            f"成绩: {course['grade']}\n"
            f"提交时间: {course['submission_time']}\n"
            f"提交人姓名: {course['name_of_submitter']}\n"
            f"------"
        )

    # 加密保存成绩
    encrypt_integrated_grade_info = md5_encrypt(integrated_grade_info)

    # 将加密后的成绩信息写入grade.txt文件
    with open("grade.txt", "w") as grade_file:
        grade_file.write(encrypt_integrated_grade_info)

# 对grade.txt和old_grade.txt两个文件的内容进行比对
with open("grade.txt", "r") as grade_file, open("old_grade.txt", "r") as old_grade_file:
    # 读取grade.txt和old_grade.txt文件的内容
    grade_content = grade_file.read()
    old_grade_content = old_grade_file.read()

# 输出成绩信息
print(f"新成绩：{encrypt_integrated_grade_info}")
print(f"旧成绩：{old_grade_content}")
print("------")

# 整合所有信息
integrate_send_info = f"{integrate_info}\n------\n{integrated_grade_info}"

# 输出成绩是否更新
if grade_content == old_grade_content:
    print("成绩未更新")
else:
    print("成绩已更新")
    response_text = send_message("教务成绩已更新", integrate_send_info)
    print(response_text)

# 更新firstrun.txt文件内容为false
if open(firstrun_file_path).read() == "true":
    with open(firstrun_file_path, "w") as firstrun_file:
        # 将firstrun.txt文件内容更新为false
        firstrun_file.write("false")
