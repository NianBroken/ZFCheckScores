# 必要的依赖库
import requests  # 导入requests库，用于发送HTTP请求
from datetime import datetime, timedelta, timezone  # 导入datetime模块中的datetime, timedelta, timezone类，用于处理日期和时间
import os  # 导入os模块，用于处理环境变量


class GitHubActionsManager:
    def __init__(self, repo_url, token, run_id, hour_count):
        self.repo_url = repo_url  # GitHub仓库的URL
        self.token = token  # GitHub个人访问令牌
        self.run_id = run_id  # 当前工作流运行记录的ID
        self.hour_count = hour_count  # 要删除的记录时间间隔，以小时为单位
        self.runs_url = f"{self.repo_url}/actions/runs"  # 用于获取工作流运行记录的URL
        self.current_time = datetime.now(timezone.utc)  # 获取当前UTC时间
        self.deleted_count = 0  # 初始化删除计数器，记录成功删除的运行记录数量

    def get_workflow_runs(self, url):
        # 发送GET请求以获取工作流运行记录
        response = requests.get(url, headers={"Authorization": f"token {self.token}"})  # 设置请求头以进行身份验证
        if response.status_code == 200:  # 如果响应状态码为200（成功）
            return response.json()["workflow_runs"]  # 返回响应中的工作流运行记录列表
        else:  # 如果响应状态码不是200（失败）
            self.log(f"Failed to fetch runs from {url}. Status code: {response.status_code}")  # 打印失败日志
            return []  # 返回空列表

    def delete_run(self, run_id):
        delete_url = f"{self.runs_url}/{run_id}"  # 构建删除指定运行记录的URL
        # 发送DELETE请求以删除指定ID的工作流运行记录
        response = requests.delete(delete_url, headers={"Authorization": f"token {self.token}"})  # 设置请求头以进行身份验证
        if response.status_code == 204:  # 如果响应状态码为204（成功删除）
            self.log(f"Deleted run with ID {run_id}")  # 打印删除成功日志
            self.deleted_count += 1  # 成功删除计数器加1
        else:  # 如果响应状态码不是204（删除失败）
            self.log(f"Failed to delete run with ID {run_id}. Status code: {response.status_code}")  # 打印删除失败日志

    def delete_old_runs(self):
        while True:  # 无限循环，直到没有符合条件的运行记录
            next_page = self.runs_url  # 初始化下一页的URL为第一页
            any_deleted = False  # 标记是否有记录被删除

            while next_page:  # 循环直到没有下一页
                # 发送GET请求以获取一页工作流运行记录
                response = requests.get(next_page, headers={"Authorization": f"token {self.token}"})  # 设置请求头以进行身份验证
                if response.status_code == 200:  # 如果响应状态码为200（成功）
                    data = response.json()  # 将响应数据解析为JSON格式
                    runs = data["workflow_runs"]  # 获取工作流运行记录列表
                    next_page = response.links.get("next", {}).get("url")  # 获取下一页的URL，如果没有下一页则为None

                    for run in runs:  # 遍历每一条运行记录
                        if self.hour_count == 0:  # 如果设置的时间间隔为0小时
                            if run["id"] != self.run_id:  # 如果运行记录ID不等于当前运行记录ID
                                self.delete_run(run["id"])  # 删除该运行记录
                                any_deleted = True  # 标记有记录被删除
                        else:  # 如果设置的时间间隔大于0小时
                            # 将运行记录的创建时间字符串转换为datetime对象，并设置为UTC时间
                            run_time = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                            # 计算当前时间与运行记录创建时间的时间差
                            time_difference = self.current_time - run_time
                            if time_difference > timedelta(hours=self.hour_count):  # 如果时间差大于设定的小时数
                                self.delete_run(run["id"])  # 删除该运行记录
                                any_deleted = True  # 标记有记录被删除
                else:  # 如果响应状态码不是200（失败）
                    self.log(f"Failed to fetch runs. Status code: {response.status_code}")  # 打印获取运行记录失败日志
                    break  # 退出循环

            if not any_deleted:  # 如果没有任何记录被删除
                break  # 退出循环

        self.log(f"Total number of deleted runs: {self.deleted_count}")  # 输出总共成功删除的运行记录数量

    def log(self, message):
        # 获取当前时间的北京时间（UTC+8）
        beijing_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
        # 将当前时间格式化为字符串，精确到三位毫秒
        current_time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
        print(f"{current_time_str} {message}")  # 打印日志消息


if __name__ == "__main__":
    repository_name = os.environ.get("REPOSITORY_NAME")  # 从环境变量获取GitHub仓库名称
    github_token = os.environ.get("GITHUB_TOKEN")  # 从环境变量获取GitHub个人访问令牌
    github_run_id = int(os.environ.get("GITHUB_RUN_ID"))  # 从环境变量获取当前工作流运行记录的ID，并转换为整数
    hour_count = int(os.environ.get("HOUR_COUNT"))  # 从环境变量获取要删除的记录时间间隔（小时），并转换为整数
    repo_url = f"https://api.github.com/repos/{repository_name}"  # 构建GitHub仓库的API URL
    token = f"{github_token}"  # GitHub个人访问令牌

    # 创建GitHubActionsManager实例
    manager = GitHubActionsManager(repo_url, token, github_run_id, hour_count)
    manager.delete_old_runs()  # 删除指定时间间隔（小时）之前的运行记录
