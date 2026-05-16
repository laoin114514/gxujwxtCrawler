"""
广西大学教务管理系统 Python SDK
教务管理信息服务平台 (正方教务系统 v5 - ZFTAL UI)
"""
import json
import time
import base64
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class JwxtClient:
    """教务系统客户端

    用法:
        client = JwxtClient("学号", "密码")
        client.login()
        grades = client.get_grades("2025", "3")
        exams = client.get_exam_arrangement("2025", "12")
    """

    BASE_URL = "https://jwxt2018.gxu.edu.cn"
    LOGIN_PATH = "/jwglxt/xtgl/login_slogin.html"
    PUBLIC_KEY_PATH = "/jwglxt/xtgl/login_getPublicKey.html"
    INIT_MENU_PATH = "/jwglxt/xtgl/index_initMenu.html"

    def __init__(self, username: str, password: str, base_url: str = None):
        self.username = username
        self.password = password
        if base_url:
            self.BASE_URL = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self._logged_in = False
        self._csrftoken = None

    # ========== 内部方法 ==========

    def _get(self, path: str, **kwargs) -> requests.Response:
        url = urljoin(self.BASE_URL, path)
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("Referer", self.BASE_URL + "/jwglxt/xtgl/index_initMenu.html")
        resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    def _post(self, path: str, data=None, **kwargs) -> requests.Response:
        url = urljoin(self.BASE_URL, path)
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("Referer", self.BASE_URL + "/jwglxt/xtgl/index_initMenu.html")
        kwargs["headers"].setdefault("Content-Type", "application/x-www-form-urlencoded")
        kwargs.setdefault("allow_redirects", True)
        resp = self.session.post(url, data=data, **kwargs)
        resp.raise_for_status()
        return resp

    def _encrypt_password(self) -> str:
        """RSA 加密密码，返回 base64 密文"""
        ts = int(time.time() * 1000)
        resp = self._get(f"{self.PUBLIC_KEY_PATH}?time={ts}")
        key_data = resp.json()
        modulus_int = int.from_bytes(base64.b64decode(key_data["modulus"]), 'big')
        exponent_int = int.from_bytes(base64.b64decode(key_data["exponent"]), 'big')
        public_key = rsa.RSAPublicNumbers(exponent_int, modulus_int).public_key(default_backend())
        encrypted = public_key.encrypt(self.password.encode('utf-8'), padding.PKCS1v15())
        return base64.b64encode(encrypted).decode()

    def _make_query_data(self, **extra) -> dict:
        """构造标准分页查询参数"""
        ts = int(time.time() * 1000)
        return {
            "_search": "false",
            "nd": ts,
            "queryModel.showCount": 100,
            "queryModel.currentPage": 1,
            "queryModel.sortName": "",
            "queryModel.sortOrder": "asc",
            "time": ts,
            **extra,
        }

    def _query_endpoint(self, path: str, data: dict = None, method: str = "POST") -> requests.Response:
        """通用端点查询"""
        if method.upper() == "GET":
            return self._get(path)
        else:
            return self._post(path, data=data or self._make_query_data())

    # ========== 认证 ==========

    def login(self) -> bool:
        """登录教务系统

        Returns:
            True 登录成功, False 登录失败
        """
        if self._logged_in:
            return True

        # 1. 获取登录页面和 csrftoken
        resp = self._get(self.LOGIN_PATH)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrftoken'})
        self._csrftoken = csrf_input.get('value', '') if csrf_input else ''

        # 2. RSA 加密密码
        encrypted_mm = self._encrypt_password()

        # 3. 提交登录表单
        ts = int(time.time() * 1000)
        resp = self._post(
            f"{self.LOGIN_PATH}?time={ts}",
            data={
                "csrftoken": self._csrftoken,
                "language": "zh_CN",
                "yhm": self.username,
                "mm": encrypted_mm,
                "ydType": "",
            },
            allow_redirects=True,
        )
        resp_url = resp.url.lower()
        self._logged_in = "login" not in resp_url or "index" in resp_url

        # 4. 初始化首页会话
        if self._logged_in:
            ts = int(time.time() * 1000)
            self._get(f"{self.INIT_MENU_PATH}?jsdm=xs&_t={ts}&echarts=1")

        return self._logged_in

    def logout(self):
        """退出登录"""
        self._get("/jwglxt/xtgl/login_logoutAccount.html")
        self._logged_in = False

    @property
    def is_logged_in(self) -> bool:
        return self._logged_in

    # ========== 用户信息 ==========

    def get_user_info_html(self) -> str:
        """获取用户信息 HTML 片段（含姓名、学号、院系、照片URL）"""
        ts = int(time.time() * 1000)
        resp = self._post(
            f"/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_={ts}&gnmkdm=index"
        )
        return resp.text

    def get_photo_url(self) -> str:
        """获取学生照片 URL"""
        return f"/jwglxt/xtgl/photo_cxXszp4.html?xh_id={self.username}&zplx=rxqzp"

    # ========== 成绩查询 ==========

    def get_grades(self, xnm: str, xqm: str) -> dict:
        """查询学期成绩

        Args:
            xnm: 学年 (起始年份)，如 '2025'=2025-2026学年
            xqm: 学期，'3'=第一学期, '12'=第二学期

        Returns:
            {"items": [{cj, kcmc, xf, jd, ...}], "totalResult": N}
        """
        data = self._make_query_data(xnm=xnm, xqm=xqm)
        resp = self._post(
            "/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005",
            data=data,
        )
        return resp.json()

    def get_grade_detail(self, jxb_id: str) -> dict:
        """查询某课程分项成绩

        Args:
            jxb_id: 教学班ID (从 get_grades 结果中获取)
        """
        data = self._make_query_data(jxb_id=jxb_id, xh=self.username)
        resp = self._post(
            "/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=details&gnmkdm=N305005",
            data=data,
        )
        try:
            return resp.json()
        except json.JSONDecodeError:
            return {"_html": resp.text}

    def get_grade_statistics(self) -> dict:
        """获取成绩统计（总学分、平均绩点等）"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=statistics&gnmkdm=N305005&time={ts}"
        )
        return resp.json()

    # ========== 课表查询 ==========

    def get_schedule_page(self) -> str:
        """获取课表页面 HTML"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&time={ts}"
        )
        return resp.text

    def get_schedule_data(self, xnm: str, xqm: str) -> dict:
        """获取课表数据 (个人课表)

        Args:
            xnm: 学年 (起始年份)，如 '2025'
            xqm: 学期，'3'=第一学期, '12'=第二学期
        """
        data = self._make_query_data(xnm=xnm, xqm=xqm)
        resp = self._post(
            "/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151",
            data=data,
        )
        return resp.json()

    def get_classroom_schedule(self, xnm: str, xqm: str, jsmc: str = "") -> dict:
        """查询教室课表"""
        data = self._make_query_data(xnm=xnm, xqm=xqm, jsmc=jsmc)
        resp = self._post(
            "/jwglxt/kbcx/jskbcx_cxJskb.html?gnmkdm=N2151",
            data=data,
        )
        return resp.json()

    def get_teacher_schedule(self, xnm: str, xqm: str, jsmc: str = "") -> dict:
        """查询教师课表"""
        data = self._make_query_data(xnm=xnm, xqm=xqm, jsmc=jsmc)
        resp = self._post(
            "/jwglxt/kbcx/jskbcx_cxJsKb.html?gnmkdm=N2151",
            data=data,
        )
        return resp.json()

    def get_schedule_credit_confirm(self) -> str:
        """课表/学分确认页面"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/kbcx/xskbqr_cxXskbqrIndex.html?gnmkdm=N2158&time={ts}"
        )
        return resp.text

    # ========== 考试安排 ==========

    def get_exam_arrangement(self, xnm: str = "", xqm: str = "") -> dict:
        """获取考试安排

        Args:
            xnm: 学年，不传则查询所有
            xqm: 学期，不传则查询所有
        """
        data = self._make_query_data(xnm=xnm, xqm=xqm)
        resp = self._post(
            "/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N3580",
            data=data,
        )
        return resp.json()

    def get_exam_monitor_info(self) -> dict:
        """获取考试监考信息"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/jkap/ksjkxxcx_cxKsjkxxcxIndex.html?gnmkdm=N353088&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    # ========== 选课 ==========

    def get_available_courses(self, xnm: str, xqm: str, kcmc: str = "") -> dict:
        """查询可选课程列表

        Args:
            xnm: 学年
            xqm: 学期
            kcmc: 课程名称（模糊搜索）
        """
        data = self._make_query_data(xnm=xnm, xqm=xqm, kcmc=kcmc)
        resp = self._post(
            "/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?doType=query&gnmkdm=N253512",
            data=data,
        )
        return resp.json()

    def get_selected_courses(self, xnm: str = "", xqm: str = "") -> dict:
        """获取已选课程"""
        data = self._make_query_data(xnm=xnm, xqm=xqm)
        resp = self._post(
            "/jwglxt/xsxk/zzxkyzb_cxZzxkYzb.html?gnmkdm=N253512",
            data=data,
        )
        return resp.json()

    # ========== 学业情况 ==========

    def get_academic_status(self) -> dict:
        """获取学业情况（已修学分、绩点、学业进度等）"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    # ========== 学籍预警 ==========

    def get_academic_warning(self) -> dict:
        """获取学籍预警信息"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/xjyj/xjyj_cxXjyjIndex.html?gnmkdm=N105505&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    # ========== 培养方案 ==========

    def get_training_plan_page(self) -> str:
        """获取培养方案页面"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/pyfa/pyfagl_cxXsPyfaIndex.html?gnmkdm=N2580&time={ts}"
        )
        return resp.text

    # ========== 学生评价 ==========

    def get_evaluation_list(self) -> dict:
        """获取学生评价列表"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/xspjgl/xspj_cxXspjIndex.html?gnmkdm=N401605&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    # ========== 教材管理 ==========

    def get_textbook_booking(self) -> dict:
        """获取教材预订信息"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/jcydgl/xsjcyd_cxXsjcydIndex.html?gnmkdm=N253545&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    def get_textbook_fee_confirm(self) -> dict:
        """教材费用确认"""
        ts = int(time.time() * 1000)
        resp = self._get(
            f"/jwglxt/jcjsgl/xsjs_cxJcfyqrIndex.html?gnmkdm=N758066&time={ts}"
        )
        try:
            return resp.json()
        except:
            return {"_html": resp.text}

    # ========== 通知公告 ==========

    def get_notifications(self, page: int = 1, size: int = 15) -> dict:
        """获取通知公告列表"""
        data = {
            "_search": "false",
            "nd": int(time.time() * 1000),
            "queryModel.showCount": size,
            "queryModel.currentPage": page,
            "queryModel.sortName": " ",
            "queryModel.sortOrder": "desc",
            "time": 0,
        }
        resp = self._post("/jwglxt/xtgl/xwck_cxMoreXwList.html?doType=query", data=data)
        return resp.json()

    def get_notification_detail(self, xwbh: str) -> str:
        """获取通知详情页面 HTML

        Args:
            xwbh: 新闻编号 (从 get_notifications 的 items[].xwbh 获取)
        """
        resp = self._get(f"/jwglxt/xtgl/xwck_ckXw.html?xwbh={xwbh}&doType=save")
        return resp.text

    # ========== 待办事项 ==========

    def get_todo_list(self, page: int = 1, size: int = 15) -> dict:
        """获取待办事项列表（调课提醒、补课提醒等）"""
        data = {
            "flag": "1",
            "sfyy": "1",
            "_search": "false",
            "nd": int(time.time() * 1000),
            "queryModel.showCount": size,
            "queryModel.currentPage": page,
            "queryModel.sortName": "cjsj ",
            "queryModel.sortOrder": "desc",
            "time": 0,
        }
        resp = self._post("/jwglxt/xtgl/index_cxDbsy.html?doType=query", data=data)
        return resp.json()

    # ========== 首页各区域 ==========

    def get_homepage_data(self) -> dict:
        """获取首页所有区域数据（课表、成绩、通知、消息、文件等）"""
        areas = {}
        endpoints = {
            "schedule": "/jwglxt/xtgl/index_cxAreaOne.html",
            "files": "/jwglxt/xtgl/index_cxAreaTwo.html",
            "messages": "/jwglxt/xtgl/index_cxAreaThree.html",
            "grades_exams": "/jwglxt/xtgl/index_cxAreaFour.html",
            "calendar": "/jwglxt/xtgl/index_cxAreaFive.html",
            "calendar_files": "/jwglxt/xtgl/index_cxAreaSix.html",
            "news": "/jwglxt/xtgl/index_cxNews.html",
        }
        for name, path in endpoints.items():
            try:
                ts = int(time.time() * 1000)
                resp = self._post(f"{path}?localeKey=zh_CN&gnmkdm=index")
                areas[name] = resp.text
            except:
                areas[name] = None
        return areas

    def get_my_apps(self) -> list:
        """获取"我的应用"列表"""
        ts = int(time.time() * 1000)
        resp = self._post(
            f"/jwglxt/xtgl/index_cxWdyy.html?localeKey=zh_CN&gnmkdm=index&time={ts}"
        )
        try:
            return resp.json()
        except:
            return []

    def get_recently_used(self) -> list:
        """获取最近使用的功能列表"""
        ts = int(time.time() * 1000)
        resp = self._post(
            f"/jwglxt/xtgl/index_cxZjsy.html?localeKey=zh_CN&gnmkdm=index&time={ts}"
        )
        try:
            return resp.json()
        except:
            return []

    # ========== 系统信息 ==========

    def get_system_tips(self) -> dict:
        """获取系统提示信息（学分未修满等）"""
        try:
            resp = self._post("/jwglxt/xtgl/index_cxXttsxx.html?bj=2")
            return resp.json()
        except:
            return {}

    def get_absentee_warning(self) -> dict:
        """获取旷课预警信息"""
        try:
            resp = self._post("/jwglxt/xtgl/index_cxKkyjxx.html")
            return resp.json()
        except:
            return {}

    # ========== 通用查询 ==========

    def query(self, path: str, data: dict = None, method: str = "POST") -> dict:
        """通用查询 — 调用任意教务 API

        Args:
            path: 接口完整路径，如 '/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
            data: POST 数据字典
            method: 'GET' 或 'POST'

        Returns:
            JSON 响应 (dict) 或包含 _html 字段的 dict

        Examples:
            # 查询成绩
            client.query('/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005',
                         {'xnm': '2025', 'xqm': '3'})

            # 查询课表
            client.query('/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151')
        """
        resp = self._query_endpoint(path, data, method)
        try:
            return resp.json()
        except json.JSONDecodeError:
            return {"_html": resp.text}

    def query_page(self, path: str) -> str:
        """获取页面 HTML"""
        resp = self._get(path)
        return resp.text

    # ========== 辅助 ==========

    def get_academic_year_semester(self) -> tuple:
        """根据当前日期推断学年学期

        Returns:
            (学年, 学期): 如 ('2025-2026', '12')

        学年格式: 'YYYY-YYYY+1'，学期: '3'=第一学期(9月-次年1月), '12'=第二学期(2月-7月)
        """
        import datetime
        now = datetime.datetime.now()
        y = now.year
        m = now.month
        if m >= 9:
            return f"{y}-{y+1}", "3"
        elif m >= 2:
            return f"{y-1}-{y}", "12"
        else:
            return f"{y-1}-{y}", "3"

    def __repr__(self):
        return f"<JwxtClient username={self.username} logged_in={self._logged_in}>"


# ========== CLI 使用示例 ==========
if __name__ == "__main__":
    import sys

    client = JwxtClient("laoin", "NB666")

    if not client.login():
        print("登录失败！")
        sys.exit(1)

    print("=== 登录成功 ===\n")

    # 成绩查询
    print("--- 2025-2026 第一学期成绩 ---")
    grades = client.get_grades("2025", "3")
    for item in grades.get("items", []):
        print(f"  {item.get('kcmc','')}: {item.get('cj','')} (绩点: {item.get('jd','')}, 学分: {item.get('xf','')})")
    print(f"  共 {grades.get('totalResult', 0)} 门\n")

    # 考试安排
    print("--- 考试安排 ---")
    exams = client.get_exam_arrangement("2025", "12")
    for item in exams.get("items", []):
        print(f"  {item.get('kcmc','')}: {item.get('kssj','')} @ {item.get('cdmc','')}")

    # 通知公告
    print("\n--- 最新通知 ---")
    notifs = client.get_notifications(size=3)
    for item in notifs.get("items", []):
        print(f"  [{item.get('fbsj','')}] {item.get('xwbtqc','')}")

    # 待办事项
    print("\n--- 待办事项 ---")
    todos = client.get_todo_list(size=3)
    for item in todos.get("items", []):
        print(f"  [{item.get('cjsj','')}] {item.get('xxbtjc','')}")
