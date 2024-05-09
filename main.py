# 必要的依赖库
import re
import hashlib
import os
import shutil
from user_login import login
from get_user_info import get_user_info
from get_grade import get_grade
from get_selected_courses import get_selected_courses
from pushplus import send_message
from datetime import datetime


# MD5加密
def md5_encrypt(string):
    return hashlib.md5(string.encode()).hexdigest()


# 从环境变量中提取教务系统的URL、用户名、密码和TOKEN等信息
force_push_message = os.environ.get("FORCE_PUSH_MESSAGE")
github_actions = os.environ.get("GITHUB_ACTIONS")
url = os.environ.get("URL")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
token = os.environ.get("TOKEN")
github_event_name = os.environ.get("GITHUB_EVENT_NAME")
github_triggering_actor = os.environ.get("GITHUB_TRIGGERING_ACTOR")
repository_name = os.environ.get("REPOSITORY_NAME")
github_sha = os.environ.get("GITHUB_SHA")
github_workflow = os.environ.get("GITHUB_WORKFLOW")
github_run_number = os.environ.get("GITHUB_RUN_NUMBER")
github_run_id = os.environ.get("GITHUB_RUN_ID")
beijing_time = os.environ.get("BEIJING_TIME")
github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")

# 将字符串转换为布尔值
# 是否强制推送信息
force_push_message = force_push_message == "True"

# 定义文件路径
info_file_path = "info.txt"
grade_file_path = "grade.txt"
old_grade_file_path = "old_grade.txt"

# 初始化运行次数
run_count = 2

# 初始化运行日志
run_log = ""

# 当前时间
current_time = "------\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

# 当前文件名
current_file_name = os.path.realpath(__file__)

# 登录
student_client = login(url, username, password)

# 获取个人信息
info = get_user_info(student_client, output_type="info")

# 获取完整个人信息
integrated_info = get_user_info(student_client, output_type="integrated_info")

# 加密个人信息
encrypted_info = md5_encrypt(info)

# 判断info.txt文件是否存在
if not os.path.exists(info_file_path):
    # 如果文件不存在,创建并写入加密后的个人信息
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
    if not os.path.exists(grade_file_path):
        open(grade_file_path, "w").close()

    # 清空old_grade.txt文件内容
    with open(old_grade_file_path, "w") as old_grade_file:
        old_grade_file.truncate()

    # 将grade.txt文件中的内容写入old_grade.txt文件内
    with open(grade_file_path, "r") as grade_file, open(
        old_grade_file_path, "w"
    ) as old_grade_file:
        old_grade_file.write(grade_file.read())

    # 获取成绩信息
    grade = get_grade(student_client, output_type="grade")

    # 成绩不为空时
    if grade:
        # 清空grade.txt文件内容
        with open(grade_file_path, "w") as grade_file:
            grade_file.truncate()

        # 获取整合后的成绩信息
        integrated_grade_info = get_grade(
            student_client, output_type="integrated_grade_info"
        )
        if integrated_grade_info == "获取成绩时出错":
            integrated_grade_info += "\n------"
    else:
        # 成绩为空时将成绩信息定义为"成绩为空"
        integrated_grade_info = "------\n成绩为空\n------"

    # 加密保存成绩
    encrypted_integrated_grade_info = md5_encrypt(integrated_grade_info)

    # 将加密后的成绩信息写入grade.txt文件
    with open(grade_file_path, "w") as grade_file:
        grade_file.write(encrypted_integrated_grade_info)

# 读取grade.txt和old_grade.txt文件的内容
with open(grade_file_path, "r") as grade_file, open(
    old_grade_file_path, "r"
) as old_grade_file:
    grade_content = grade_file.read()
    old_grade_content = old_grade_file.read()

# 整合MD5值
integrated_grade_info += f"\n" f"MD5：{encrypted_integrated_grade_info}"

# 获取未公布成绩的课程和异常的课程
selected_courses_filtering = get_selected_courses(student_client)

# 工作流信息
workflow_info = (
    f"------\n"
    f"工作流信息：\n"
    f"Force Push Message：{force_push_message}\n"
    f"Triggered By：{github_event_name}\n"
    f"Run By：{github_triggering_actor}\n"
    f"Repository Name：{repository_name}\n"
    f"Commit SHA：{github_sha}\n"
    f"Workflow Name：{github_workflow}\n"
    f"Workflow Number：{github_run_number}\n"
    f"Workflow ID：{github_run_id}\n"
    f"Beijing Time：{beijing_time}"
)

# 第一次运行时的提示文本
first_run_text = (
    "你的程序运行成功\n"
    "从现在开始,程序将会每隔 30 分钟自动检测一次成绩是否有更新\n"
    "若有更新,将通过微信推送及时通知你\n"
    "------"
)

# 整合所有信息
# 注意此处integrated_send_info保存的是未加密的信息,仅用于信息推送
# 若是在 Github Actions 等平台运行,请不要使用print(integrated_send_info)
integrated_send_info = (
    f"{integrated_info}\n"
    f"{integrated_grade_info}\n"
    f"{selected_courses_filtering}\n"
    f"{workflow_info if github_actions else current_time}"
)

# 整合首次运行时需要使用到的所有信息
first_time_run_integrated_send_info = f"{first_run_text}\n" f"{integrated_send_info}"

# 整合成绩已更新时需要使用到的所有信息
grades_updated_push_integrated_send_info = (
    f"{'强制推送信息成功' if force_push_message else '教务管理系统成绩已更新'}\n"
    f"------\n"
    f"{integrated_send_info}"
)

# 如果是第一次运行,则提示程序运行成功
if run_count == 2:
    run_log += f"{first_run_text}\n"

    # 推送信息
    first_run_text_response_text = send_message(
        token,
        "正方教务管理系统成绩推送",
        first_time_run_integrated_send_info,
    )

    # 输出响应内容
    run_log += f"{first_run_text_response_text}\n"
else:
    # 如果非第一次运行,则输出成绩信息
    if grade:
        run_log += f"新成绩：{encrypted_integrated_grade_info}\n"
        run_log += f"旧成绩：{old_grade_content}\n"
    else:
        run_log += "成绩为空\n"
    run_log += "------\n"

    # 对grade.txt和old_grade.txt两个文件的内容进行比对,输出成绩是否更新
    if grade_content != old_grade_content or force_push_message:
        # 判断是否选中了强制推送信息
        run_log += f"{'强制推送信息' if force_push_message else '成绩已更新'}\n"

        # 推送信息
        response_text = send_message(
            token,
            "正方教务管理系统成绩推送",
            grades_updated_push_integrated_send_info,
        )
        # 输出响应内容
        run_log += f"{response_text}\n"
    else:
        run_log += "成绩未更新"

# 更新info.txt
with open(info_file_path, "r") as info_file:
    info_file_content = info_file.read()
    if info_file_content != encrypted_info:
        with open("info.txt", "w") as info_file:
            info_file.write(encrypted_info)

# 输出运行日志
if run_log:
    print(run_log)

    # 整合JobSummary信息
    github_step_summary_run_log = (
        f"# 正方教务管理系统成绩推送\n{run_log}\n{workflow_info}"
    )
    # 将任意个数的换行替换为两个换行
    github_step_summary_run_log = re.sub("\n+", "\n\n", github_step_summary_run_log)

    if github_actions:
        # 将 github_step_summary_run_log 写入到 GitHub Actions 的环境文件中
        with open(github_step_summary, "w", encoding="utf-8") as file:
            file.write(github_step_summary_run_log)

# 删除 __pycache__ 缓存目录及其内容
current_directory = os.getcwd()
cache_folder = os.path.join(current_directory, "__pycache__")
# 检查目录是否存在
if os.path.exists(cache_folder):
    # 删除目录及其内容
    shutil.rmtree(cache_folder)
