# 必要的库
import base64
import hashlib
import os
import sys
import shutil
import json
from pprint import pprint
from zfn_api import Client
from pushplus import send_message

# 从环境变量中提取教务系统的URL、用户名、密码和TOKEN等信息
url = os.environ.get("URL")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
token = os.environ.get("TOKEN")
repository_name = os.environ.get("REPOSITORY_NAME")
github_sha = os.environ.get("GITHUB_SHA")
github_workflow = os.environ.get("GITHUB_WORKFLOW")
github_run_number = os.environ.get("GITHUB_RUN_NUMBER")
github_run_id = os.environ.get("GITHUB_RUN_ID")
beijing_time = os.environ.get("BEIJING_TIME")


# MD5加密
def md5_encrypt(string):
    return hashlib.md5(string.encode()).hexdigest()


# 初始化变量
cookies = {}
base_url = url
raspisanie = []
ignore_type = []
detail_category_type = []
timeout = 5

# 创建教务系统客户端对象
student_client = Client(
    cookies=cookies,
    base_url=base_url,
    raspisanie=raspisanie,
    ignore_type=ignore_type,
    detail_category_type=detail_category_type,
    timeout=timeout,
)

# 登录
if not cookies:
    login_result = student_client.login(username, password)
    if login_result["code"] == 1001:
        # 如果需要验证码,获取验证码并进行登录
        verify_data = login_result["data"]
        # 将验证码图片写入文件
        with open(os.path.abspath("kaptcha.png"), "wb") as pic:
            pic.write(base64.b64decode(verify_data.pop("kaptcha_pic")))
        # 输入验证码
        verify_data["kaptcha"] = input("输入验证码：")
        # 使用验证码进行登录
        login_result = student_client.login_with_kaptcha(**verify_data)

        if login_result["code"] != 1000:
            pprint(login_result)
            sys.exit()
        pprint(login_result)

    elif login_result["code"] != 1000:
        pprint(login_result)
        sys.exit()

# 获取个人信息
info = student_client.get_info()["data"]

# 整合个人信息
integrated_info = (
    f"个人信息：\n"
    f"学号：{info['sid']}\n"
    f"班级：{info['class_name']}\n"
    f"姓名：{info['name']}"
)

# 加密个人信息
encrypted_info = md5_encrypt(integrated_info)

# 定义info.txt文件路径
info_file_path = "info.txt"

# 初始化运行次数
run_count = 2

# 判断info.txt文件是否存在
if not os.path.exists(info_file_path):
    # 如果文件不存在,创建并写入encrypted_info的内容
    with open(info_file_path, "w") as info_file:
        info_file.write(encrypted_info)
else:
    # 如果文件存在,读取文件内容并比较
    with open(info_file_path, "r") as info_file:
        info_file_content = info_file.read()
        # 若info.txt文件中保存的个人信息与获取到的个人信息一致,则代表非第一次运行程序
        if info_file_content == encrypted_info:
            # 非第一次运行程序
            run_count = 1

# 第一次运行程序则运行两遍,否则运行一遍
for _ in range(run_count):
    # 如果grade.txt文件不存在,则创建文件
    if not os.path.exists("grade.txt"):
        open("grade.txt", "w").close()

    # 清空old_grade.txt文件内容
    with open("old_grade.txt", "w") as old_grade_file:
        old_grade_file.truncate()

    # 获取成绩信息
    grade_data = student_client.get_grade("").get("data", {})
    grade = grade_data.get("courses", [])

    # 将grade.txt文件中的内容写入old_grade.txt文件内
    with open("grade.txt", "r") as grade_file, open(
        "old_grade.txt", "w"
    ) as old_grade_file:
        old_grade_file.write(grade_file.read())

    # 成绩不为空时则对成绩信息进行处理
    if grade:
        # 清空grade.txt文件内容
        with open("grade.txt", "w") as grade_file:
            grade_file.truncate()

        # 按照提交时间降序排序
        sorted_grade = sorted(grade, key=lambda x: x["submission_time"], reverse=True)

        # 学分总和
        total_credit = sum(float(course["credit"]) for course in grade)

        # 学分绩点总和
        total_xfjd = sum(float(course["xfjd"]) for course in grade)

        # (百分制成绩*学分)的总和
        sum_of_percentage_grades_multiplied_by_credits = sum(
            float(course["percentage_grades"]) * float(course["credit"])
            for course in grade
        )

        # GPA计算 (学分*绩点)的总和/学分总和
        gpa = "{:.2f}".format(total_xfjd / total_credit)

        # 百分制GPA计算 (百分制成绩*学分)的总和/学分总和
        percentage_gpa = "{:.2f}".format(
            sum_of_percentage_grades_multiplied_by_credits / total_credit
        )

        # 初始化输出成绩信息字符串
        integrated_grade_info = "成绩信息："

        # 遍历前8条成绩信息
        for i, course in enumerate(sorted_grade[:8]):
            # 整合成绩信息
            integrated_grade_info += (
                f"\n"
                f"课程ID: {course['course_id']}\n"
                f"课程名称: {course['title']}\n"
                f"任课教师: {course['teacher']}\n"
                f"成绩: {course['grade']}\n"
                f"提交时间: {course['submission_time']}\n"
                f"提交人姓名: {course['name_of_submitter']}\n"
                f"------"
            )
    else:
        # 成绩为空时将成绩信息定义为"成绩为空"
        integrated_grade_info = "------\n成绩为空\n------"

    # 加密保存成绩
    encrypted_integrated_grade_info = md5_encrypt(integrated_grade_info)

    # 将加密后的成绩信息写入grade.txt文件
    with open("grade.txt", "w") as grade_file:
        grade_file.write(encrypted_integrated_grade_info)

# 成绩信息不为空时整合GPA信息
if grade:
    # 整合个人信息
    integrated_info += (
        f"\n当前GPA：{gpa}\n" f"当前百分制GPA：{percentage_gpa}\n" f"------"
    )

# 读取grade.txt和old_grade.txt文件的内容
with open("grade.txt", "r") as grade_file, open("old_grade.txt", "r") as old_grade_file:
    grade_content = grade_file.read()
    old_grade_content = old_grade_file.read()

# 第一次运行时的提示文本
first_run_text = (
    "你的程序运行成功\n"
    "从现在开始,程序将会每隔 30 分钟自动检测成绩是否有更新\n"
    "若有更新,将通过微信推送及时通知你\n"
    "------"
)

# 整合MD5值
integrated_grade_info += f"\n" f"MD5：{encrypted_integrated_grade_info}"

# 工作流信息
workflow_info = (
    f"------\n"
    f"工作流信息：\n"
    f"Repository Name：{repository_name}\n"
    f"Commit SHA：{github_sha}\n"
    f"Current Workflow：{github_workflow}\n"
    f"Workflow Number：{github_run_number}\n"
    f"Workflow ID：{github_run_id}\n"
    f"Beijing Time：{beijing_time}"
)

# 整合首次运行时需要使用到的所有信息
first_time_run_integrated_send_info = (
    f"{first_run_text}\n"
    f"{integrated_info}\n"
    f"{integrated_grade_info}\n"
    f"{workflow_info}"
)

# 如果是第一次运行,则提示程序运行成功
if run_count == 2:
    print(first_run_text)

    # 推送信息
    first_run_text_response_text = send_message(
        token, "正方教务管理系统成绩推送", first_time_run_integrated_send_info
    )

    # 解析 JSON 数据
    first_run_text_response_dict = json.loads(first_run_text_response_text)

    # 删除 "data" 字段
    if "data" in first_run_text_response_dict:
        first_run_text_response_dict.pop("data")

    # 输出响应内容
    print(first_run_text_response_dict)
else:
    # 如果非第一次运行,则输出成绩信息
    if grade:
        print(f"新成绩：{encrypted_integrated_grade_info}")
        print(f"旧成绩：{old_grade_content}")
    else:
        print("成绩为空")
    print("------")

    # 整合所有信息
    # 注意此处integrated_send_info保存的是未加密的信息,仅用于信息推送
    # 若是在 Github Actions 等平台运行,请不要使用print(integrated_send_info)
    integrated_send_info = (
        f"{integrated_info}\n{integrated_grade_info}\n{workflow_info}"
    )

    grades_updated_push_integrated_send_info = (
        f"教务管理系统成绩已更新\n" f"------\n" f"{integrated_send_info}"
    )

    # 对grade.txt和old_grade.txt两个文件的内容进行比对,输出成绩是否更新
    if grade_content == old_grade_content:
        print("成绩未更新")
    else:
        print("成绩已更新")

        # 推送信息
        response_text = send_message(
            token, "正方教务管理系统成绩推送", grades_updated_push_integrated_send_info
        )

        # 解析 JSON 数据
        response_dict = json.loads(response_text)

        # 删除 "data" 字段
        if "data" in response_dict:
            response_dict.pop("data")

        # 输出响应内容
        print(response_dict)

# 更新info.txt
with open(info_file_path, "r") as info_file:
    info_file_content = info_file.read()
    if info_file_content != encrypted_info:
        with open("info.txt", "w") as info_file:
            info_file.write(encrypted_info)

# 删除 __pycache__ 缓存目录及其内容
current_directory = os.getcwd()
cache_folder = os.path.join(current_directory, "__pycache__")
# 检查目录是否存在
if os.path.exists(cache_folder):
    # 删除目录及其内容
    shutil.rmtree(cache_folder)
