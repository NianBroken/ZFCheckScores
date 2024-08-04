from .get_grade import get_grade
import traceback


def get_user_info(student_client, output_type="none"):
    try:
        # 获取个人信息
        info = student_client.get_info()["data"]

        # 整合个人信息
        info = f"个人信息：\n" f"学号：{info['sid']}\n" f"班级：{info['class_name']}\n" f"姓名：{info['name']}"

        grade = get_grade(student_client, output_type="grade")

        if grade:
            gpa = get_grade(student_client, output_type="gpa")
            percentage_gpa = get_grade(student_client, output_type="percentage_gpa")
            # 整合个人信息
            gpa_info = f"\n当前GPA：{gpa}\n" f"当前百分制GPA：{percentage_gpa}\n" f"------"
            integrated_info = f"{info}{gpa_info}"

            if output_type == "info":
                return info
            elif output_type == "integrated_info":
                return integrated_info
            else:
                return "获取个人信息：参数缺失"
        else:
            return f"{info}\n------"

    except Exception:
        print(traceback.format_exc())
        return "获取个人信息时出错\n------"
