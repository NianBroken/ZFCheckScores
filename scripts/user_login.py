import os
import re
import sys
import time
from pprint import pprint
from .zfn_api import Client

# 从环境变量中提取教务系统的URL、用户名、密码和TOKEN等信息
force_push_message = os.environ.get("FORCE_PUSH_MESSAGE")
github_actions = os.environ.get("GITHUB_ACTIONS")
github_ref_name = os.environ.get("GITHUB_REF_NAME")
github_event_name = os.environ.get("GITHUB_EVENT_NAME")
github_actor = os.environ.get("GITHUB_ACTOR")
github_actor_id = os.environ.get("GITHUB_ACTOR_ID")
github_triggering_actor = os.environ.get("GITHUB_TRIGGERING_ACTOR")
repository_name = os.environ.get("REPOSITORY_NAME")
github_sha = os.environ.get("GITHUB_SHA")
github_workflow = os.environ.get("GITHUB_WORKFLOW")
github_run_number = os.environ.get("GITHUB_RUN_NUMBER")
github_run_id = os.environ.get("GITHUB_RUN_ID")
beijing_time = os.environ.get("BEIJING_TIME")
github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")

# 工作流信息
workflow_info = (
    f"------\n"
    f"工作流信息：\n"
    f"Force Push Message：{force_push_message}\n"
    f"Branch Name：{github_ref_name}\n"
    f"Triggered By：{github_event_name}\n"
    f"Initial Run By：{github_actor}\n"
    f"Initial Run By ID：{github_actor_id}\n"
    f"Initiated Run By：{github_triggering_actor}\n"
    f"Repository Name：{repository_name}\n"
    f"Commit SHA：{github_sha}\n"
    f"Workflow Name：{github_workflow}\n"
    f"Workflow Number：{github_run_number}\n"
    f"Workflow ID：{github_run_id}\n"
    f"Beijing Time：{beijing_time}"
)

copyright_text = "Copyright © 2024 NianBroken. All rights reserved."


def write_github_summary(run_log, lgn_code):
    # 检查 run_log 是否为空，若为空则赋值为“未知错误”
    if not run_log:
        run_log = "未知错误"

    # 检查 lgn_code 是否为空，若为空则赋值为“未知代码”
    if not lgn_code:
        lgn_code = "未知代码"

    summary_log = (
        f"# 正方教务管理系统成绩推送\n"
        f"你因 **{run_log}** 原因而登录失败，错误代码为 **{lgn_code}**。\n"
        f"若你不明白或不理解为什么登录失败，请到上游仓库的 "
        f"[Issue](https://github.com/NianBroken/ZFCheckScores/issues/new 'Issue') 中寻求帮助。\n"
        f"{workflow_info}\n"
        f"{copyright_text}"
    )

    # 将任意个数的换行替换为两个换行
    summary_log = re.sub("\n+", "\n\n", summary_log)

    # 将登录需要验证码写入到 GitHub Actions 的环境文件中
    with open(github_step_summary, "w", encoding="utf-8") as file:
        file.write(summary_log)


def login(url, username=None, password=None, session=None, cookies=None):
    """
    封装登录逻辑，兼容三种场景：
    1. 直接复用已登录的 requests.Session
    2. 使用现成 cookies
    3. 账号密码登录
    """
    # 统一 cookies 为 dict，方便后续判断
    if cookies is None:
        cookies = {}

    base_url = url
    raspisanie = []
    ignore_type = []
    detail_category_type = []
    timeout = 10

    # 若已提供 session，则直接复用
    if session is not None:
        cookies = session.cookies.get_dict()
        student_client = Client(
            cookies=cookies,
            base_url=base_url,
            raspisanie=raspisanie,
            ignore_type=ignore_type,
            detail_category_type=detail_category_type,
            timeout=timeout,
        )
        # 复用会话，保持连接池、代理等设置
        student_client.sess = session
        return student_client

    # 若提供了 cookies，直接使用
    if cookies:
        student_client = Client(
            cookies=cookies,
            base_url=base_url,
            raspisanie=raspisanie,
            ignore_type=ignore_type,
            detail_category_type=detail_category_type,
            timeout=timeout,
        )
        return student_client

    # 走到这里说明只能账号密码登录，缺失则直接退出
    if username is None or password is None:
        sys.exit("未提供有效登录方式（session/cookies/账号密码均为空），无法登录。")

    # 账号密码登录
    student_client = Client(
        cookies={},
        base_url=base_url,
        raspisanie=raspisanie,
        ignore_type=ignore_type,
        detail_category_type=detail_category_type,
        timeout=timeout,
    )

    attempts = 5  # 最大重试次数
    while attempts > 0:
        lgn = student_client.login(username, password)

        if lgn["code"] == 1001:
            run_log = "登录需要验证码"

            # 如果是 GitHub Actions 运行，则将运行日志写入到 GitHub Actions 的日志文件中
            if github_actions:
                write_github_summary(run_log, lgn["code"])

            sys.exit(f"你因{run_log}原因而登录失败，错误代码为{lgn['code']}。")
            """
            verify_data = lgn["data"]
            with open(os.path.abspath("kaptcha.png"), "wb") as pic:
                pic.write(base64.b64decode(verify_data.pop("kaptcha_pic")))
            verify_data["kaptcha"] = input("输入验证码：")
            ret = student_client.login_with_kaptcha(**verify_data)
            if ret["code"] != 1000:
                pprint(ret)
                sys.exit()
            pprint(ret)
            """
        elif lgn["code"] != 1000:
            # 登录失败但非验证码
            if attempts == 1:
                pprint(lgn)
                run_log = lgn["msg"]
                if github_actions:
                    write_github_summary(run_log, lgn["code"])

            # 重试
            time.sleep(1)
            attempts -= 1
            continue

        # 登录成功，跳出循环
        break

    if attempts == 0:
        # 尝试次数耗尽依旧失败
        sys.exit(0)

    return student_client
