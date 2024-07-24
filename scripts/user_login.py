import sys
from pprint import pprint
from .zfn_api import Client


def login(url, username, password):
    cookies = {}
    base_url = url
    raspisanie = []
    ignore_type = []
    detail_category_type = []
    timeout = 5

    student_client = Client(
        cookies=cookies,
        base_url=base_url,
        raspisanie=raspisanie,
        ignore_type=ignore_type,
        detail_category_type=detail_category_type,
        timeout=timeout,
    )

    if cookies == {}:
        lgn = student_client.login(username, password)
        if lgn["code"] == 1001:
            sys.exit("你的教务系统登录时需要验证码，因此你无法使用此项目。")
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
            pprint(lgn)
            sys.exit()

    return student_client
