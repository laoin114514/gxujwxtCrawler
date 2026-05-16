"""
广西大学教务管理系统 Python SDK
教务管理信息服务平台 (正方教务系统 v5 - ZFTAL UI)
"""
import datetime
from typing import Optional

from .base import JwxtBase
from .models.common import Semester
from .modules import (
    GradeModule,
    ScheduleModule,
    ExamModule,
    NotificationModule,
    CourseModule,
    AcademicModule,
    HomepageModule,
    EvaluationModule,
    TextbookModule,
    SystemModule,
)


class JwxtClient:
    """教务系统客户端

    用法:
        from python_sdk import JwxtClient, LoginError

        client = JwxtClient("学号", "密码")
        try:
            client.login()
        except LoginError as e:
            print(f"登录失败: {e}")

        # 成绩查询
        grades = client.grades.query("2025", "3")
        for item in grades.items:
            print(f"{item.course_name}: {item.score}")

        # 考试安排
        exams = client.exams.query("2025", "12")

        # 通知公告
        notifs = client.notifications.list()
    """

    def __init__(self, username: str, password: str, base_url: Optional[str] = None):
        self._base = JwxtBase(username, password, base_url)

        # 业务模块
        self.grades = GradeModule(self._base)
        self.schedule = ScheduleModule(self._base)
        self.exams = ExamModule(self._base)
        self.notifications = NotificationModule(self._base)
        self.courses = CourseModule(self._base)
        self.academic = AcademicModule(self._base)
        self.homepage = HomepageModule(self._base)
        self.evaluation = EvaluationModule(self._base)
        self.textbooks = TextbookModule(self._base)
        self.system = SystemModule(self._base)

    # ========== 认证 ==========

    def login(self) -> None:
        self._base.login()

    def logout(self) -> None:
        self._base.logout()

    @property
    def is_logged_in(self) -> bool:
        return self._base.is_logged_in

    # ========== 通用查询 ==========

    def query(self, path: str, data: Optional[dict] = None, method: str = "POST") -> dict:
        """通用查询 — 调用任意教务 API"""
        import json
        if method.upper() == "GET":
            resp = self._base.get(path)
        else:
            resp = self._base.post(path, data=data or {})
        try:
            return resp.json()
        except json.JSONDecodeError:
            return {"_html": resp.text}

    def query_page(self, path: str) -> str:
        """获取页面 HTML"""
        resp = self._base.get(path)
        return resp.text

    # ========== 辅助 ==========

    @staticmethod
    def current_semester() -> Semester:
        """根据当前日期推断学年学期"""
        now = datetime.datetime.now()
        y = now.year
        m = now.month
        if m >= 9:
            return Semester(year=str(y), term="3")
        elif m >= 2:
            return Semester(year=str(y - 1), term="12")
        else:
            return Semester(year=str(y - 1), term="3")

    @property
    def username(self) -> str:
        return self._base.username

    def __repr__(self):
        return f"<JwxtClient username={self.username} logged_in={self.is_logged_in}>"
