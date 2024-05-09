import traceback


def get_grade(student_client, output_type="none"):
    try:
        # 获取成绩信息
        grade_data = student_client.get_grade().get("data", {})
        grade = grade_data.get("courses", [])

        # 成绩不为空时
        if grade:
            # 遍历 grade 中的每个字典，将 title 中的中文括号替换为英文括号
            for course_data_grade in grade:
                course_data_grade["title"] = (
                    course_data_grade["title"].replace("（", "(").replace("）", ")")
                )

            # 按照提交时间降序排序
            # 对于没有提交时间参数的成绩，则将提交时间设置为1970-01-01 00:00:00，否则将无法排序
            sorted_grade = sorted(
                grade,
                key=lambda x: (
                    x["submission_time"]
                    if x["submission_time"]
                    else "1970-01-01 00:00:00"
                ),
                reverse=True,
            )

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
            for _, course in enumerate(sorted_grade[:8]):
                # 整合成绩信息
                integrated_grade_info += (
                    f"\n"
                    f"教学班ID：{course['class_id']}\n"
                    f"课程名称：{course['title']}\n"
                    f"任课教师：{course['teacher']}\n"
                    f"成绩：{course['grade']}\n"
                    f"提交时间：{course['submission_time']}\n"
                    f"提交人姓名：{course['name_of_submitter']}\n"
                    f"------"
                )

            if output_type == "grade":
                return grade
            elif output_type == "gpa":
                return gpa
            elif output_type == "percentage_gpa":
                return percentage_gpa
            elif output_type == "integrated_grade_info":
                return integrated_grade_info
            else:
                return "获取成绩：参数缺失"

    except Exception:
        print(traceback.format_exc())
        return "获取成绩时出错"
