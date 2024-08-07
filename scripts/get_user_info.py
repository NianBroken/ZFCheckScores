from .get_grade import get_grade
import traceback
import time


def get_user_info(student_client, output_type="none"):
    try:
        # 定义重试次数上限为5次
        attempts = 5
        # 初始化info为空字典
        info = {}

        # 使用while循环最多重试5次获取个人信息
        while attempts > 0:
            # 调用student_client的get_info方法获取个人信息字典
            info = student_client.get_info().get("data", {})

            # 如果info不为空，退出循环
            if info:
                break

            # 如果info为空，等待1秒后重试
            time.sleep(1)
            # 减少剩余重试次数
            attempts -= 1

        # 如果成功获取到个人信息
        if info:
            # 整合个人信息为字符串格式
            info = (
                f"个人信息：\n"
                f"学号：{info['sid']}\n"
                f"班级：{info['class_name']}\n"
                f"姓名：{info['name']}"
            )

            # 调用get_grade方法获取学生成绩信息
            grade = get_grade(student_client, output_type="grade")

            # 如果成功获取到成绩信息
            if grade:
                # 获取当前GPA
                gpa = get_grade(student_client, output_type="gpa")
                # 获取当前百分制GPA
                percentage_gpa = get_grade(student_client, output_type="percentage_gpa")
                # 整合GPA信息为字符串格式
                gpa_info = f"\n当前GPA：{gpa}\n" f"当前百分制GPA：{percentage_gpa}"
                # 将个人信息和GPA信息整合为完整字符串
                integrated_info = f"{info}{gpa_info}"

                # 根据output_type返回不同类型的信息
                if output_type == "info":
                    return info
                elif output_type == "integrated_info":
                    return integrated_info
                else:
                    # 如果output_type参数无效，返回错误提示
                    return "获取个人信息：参数缺失"
            else:
                # 如果未获取到成绩信息，返回仅包含个人信息的字符串
                return f"{info}"

    except Exception:
        # 捕获并打印所有异常的详细信息
        print(traceback.format_exc())
        # 返回错误提示信息
        return "个人信息：\n获取个人信息时出错"
