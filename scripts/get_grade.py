import time
import traceback


def get_grade(student_client, output_type="none"):
    try:
        # 定义重试次数上限为5次
        attempts = 5
        # 初始化grade为空列表
        grade = []

        # 定义安全的float转换函数，避免None/空字符串导致异常
        def safe_float(value, default=0.0):
            try:
                return float(value)
            except (TypeError, ValueError):
                return default

        # 使用while循环最多重试5次获取成绩信息
        while attempts > 0:

            # 调用student_client的get_grade方法获取成绩信息
            grade_data = student_client.get_grade().get("data", {})
            grade = grade_data.get("courses", [])

            # 如果grade不为空，跳出循环
            if grade:
                break

            # 如果grade为空，等待1秒后重试
            time.sleep(1)
            # 减少剩余重试次数
            attempts -= 1

        # 成绩不为空时
        if grade:
            # 过滤出成绩大于等于60分的课程
            filtered_grade = list(
                filter(lambda x: safe_float(x.get("percentage_grades")) >= 60, grade)
            )

            # 遍历 grade 中的每个字典，将 title 中的中文括号替换为英文括号
            for course_data_grade in grade:
                if course_data_grade.get("title"):
                    course_data_grade["title"] = (
                        course_data_grade["title"].replace("（", "(").replace("）", ")")
                    )

            # 按照提交时间降序排序
            # 对于没有提交时间参数的成绩，则将提交时间设置为1970-01-01 00:00:00，否则将无法排序
            sorted_grade = sorted(
                grade,
                key=lambda x: (
                    x.get("submission_time")
                    if x.get("submission_time")
                    else "1970-01-01 00:00:00"
                ),
                reverse=True,
            )

            # 大于等于60分的课程不为空时
            if filtered_grade:
                # 学分总和
                total_credit = sum(safe_float(course.get("credit")) for course in filtered_grade)

                # 学分绩点总和
                total_xfjd = sum(safe_float(course.get("xfjd")) for course in filtered_grade)

                # (百分制成绩*学分)的总和
                sum_of_percentage_grades_multiplied_by_credits = sum(
                    safe_float(course.get("percentage_grades")) * safe_float(course.get("credit"))
                    for course in filtered_grade
                )

                # GPA计算 (学分*绩点)的总和/学分总和
                if total_credit > 0:
                    gpa = "{:.2f}".format(total_xfjd / total_credit)

                    # 百分制GPA计算 (百分制成绩*学分)的总和/学分总和
                    percentage_gpa = "{:.2f}".format(
                        sum_of_percentage_grades_multiplied_by_credits / total_credit
                    )
                else:
                    total_credit = total_xfjd = sum_of_percentage_grades_multiplied_by_credits = 0
                    gpa = percentage_gpa = 0
            else:
                total_credit = total_xfjd = sum_of_percentage_grades_multiplied_by_credits = gpa = (
                    percentage_gpa
                ) = 0

            # 初始化输出成绩信息字符串
            integrated_grade_info = "------\n成绩信息："

            # 遍历前8条成绩信息
            for _, course in enumerate(sorted_grade[:8]):

                # 如果成绩非数字，如及格、良好、中等、优秀等，则显示百分制成绩
                try:
                    float(course.get("grade"))  # 检查成绩是否为数字
                    score_grades = course.get("grade")
                except (TypeError, ValueError):
                    score_grades = f"{course.get('grade')} ({course.get('percentage_grades')})"

                # 整合成绩信息
                integrated_grade_info += (
                    f"\n"
                    f"教学班ID：{course.get('class_id')}\n"
                    f"课程名称：{course.get('title')}\n"
                    f"任课教师：{course.get('teacher')}\n"
                    f"成绩：{score_grades}\n"
                    f"提交时间：{course.get('submission_time')}\n"
                    f"提交人姓名：{course.get('name_of_submitter')}\n"
                    f"------"
                )

            last_submission_time = sorted_grade[0].get("submission_time") if sorted_grade else ""

            if output_type == "grade":
                return grade
            elif output_type == "gpa":
                return gpa
            elif output_type == "percentage_gpa":
                return percentage_gpa
            elif output_type == "integrated_grade_info":
                return integrated_grade_info
            elif output_type == "last_submission_time":
                return last_submission_time
            else:
                return "获取成绩：参数缺失"

    except Exception:
        print(traceback.format_exc())
        if output_type == "grade":
            return []
        return "获取成绩时出错"
