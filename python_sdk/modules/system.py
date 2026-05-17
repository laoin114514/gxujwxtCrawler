"""系统信息模块"""
import time
from ..base import JwxtBase


class SystemModule:
    """系统提示、预警、统计计数等"""

    def __init__(self, base: JwxtBase):
        self._base = base

    # ---- 预警 / 提示 ----

    def tips(self) -> str:
        """系统提示（学分未修满等）"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXttsxx.html?bj=2").text

    def absentee_warning(self) -> str:
        """旷课预警"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxKkyjxx.html").text

    def labor_warning(self) -> str:
        """劳育预警"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxLyyjxx.html").text

    def academic_warning_list(self) -> str:
        """学业预警列表"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/index_cxXsxyyjtxIndex.html").text

    def academic_warning_detail(self) -> str:
        """学业预警详情"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXsxyyjtxView.html").text

    def academic_warning_confirm_status(self) -> str:
        """学籍预警确认状态"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXjyjqrzt.html").text

    # ---- 未提交计数 ----

    def _json_number(self, path: str) -> int | dict:
        """POST 获取 JSON 结果 (数字或对象)"""
        try:
            self._base.ensure_login()
            result = self._base.post(path).json()
            return result if isinstance(result, (int, dict)) else int(result)
        except Exception:
            return 0

    def _safe_json_post(self, path: str) -> dict:
        """POST 获取 JSON，失败返回空 dict"""
        try:
            self._base.ensure_login()
            return self._base.post(path).json()
        except Exception:
            return {}

    def _safe_json_get(self, path: str) -> dict | list:
        """GET 获取 JSON，失败返回空 list"""
        try:
            self._base.ensure_login()
            return self._base.get(path).json()
        except Exception:
            return []

    def pending_textbook_apply(self) -> int:
        """教材申请未提交数量"""
        return self._json_number("/jwglxt/xtgl/index_cxJhkcjcsqWtjNum.html")

    def elective_credit_deficiency(self) -> dict:
        """公选课学分未修满"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxXsGxkxfwxm.html")

    def pending_student_evaluation(self) -> int:
        """学生评价未提交数"""
        return self._json_number("/jwglxt/xtgl/index_cxXspjWtjNum.html")

    def pending_peer_evaluation(self) -> int:
        """同行评价未提交数"""
        return self._json_number("/jwglxt/xtgl/index_cxThpjWtjNum.html")

    def pending_supervisor_evaluation(self) -> int:
        """督导评价未提交数"""
        return self._json_number("/jwglxt/xtgl/index_cxDdpjWtjNum.html")

    def pending_leader_evaluation(self) -> int:
        """领导评价未提交数"""
        return self._json_number("/jwglxt/xtgl/index_cxLdpjWtjNum.html")

    # ---- 时间 / 状态 ----

    def minor_fee_reminder(self) -> dict:
        """辅修缴费提醒"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxFxjftsNum.html")

    def minor_fee_reminder_update(self) -> str:
        """更新辅修提醒状态"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxUpdateFxjftszt.html").text

    def thesis_topic_time(self) -> dict:
        """毕设选题时间"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxBsxtsj.html")

    def credit_confirm_time(self) -> dict:
        """学分确认时间"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxXfqrsj.html")

    def role_enabled(self) -> dict:
        """角色是否启用"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxJssfqy.html")

    def set_default_role(self) -> dict:
        """设置默认角色"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxSzmrjs.html")

    # ---- 监考 ----

    def exam_monitor_list(self) -> str:
        """教师监考列表"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxJsjkxxList.html").text

    def exam_monitor_view(self) -> str:
        """监考信息视图"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxJsjkxxView.html").text

    def exam_monitor_student_list(self) -> str:
        """考试监考列表（学生视角）"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxKsjkxxList.html").text

    # ---- 其他 ----

    def mark_read(self) -> dict:
        """信息已读状态更新"""
        self._base.ensure_login()
        return self._safe_json_post("/jwglxt/xtgl/index_cxXxdlztgx.html")

    def switch_account(self) -> str:
        """用户切换（返回原账号）"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_yhqhAccount.html").text

    def available_services(self) -> str:
        """可选业务页面"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/index_cxKczywIndex.html").text

    def feature_search(self) -> str:
        """功能检索页面"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/index_cxGnjsView.html").text

    def manage_my_apps(self) -> str:
        """管理我的应用页面"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/index_cxGlwdyyView.html").text

    def captcha(self) -> bytes:
        """获取图片验证码"""
        ts = int(time.time() * 1000)
        resp = self._base.get(f"/jwglxt/xtgl/login_getYzm.html?time={ts}")
        return resp.content

    def kaptcha(self) -> bytes:
        """获取图形验证码 (新版)"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/kaptcha")
        return resp.content

    def menu_json(self) -> dict:
        """获取菜单结构 (JSON)

        返回完整的菜单树，含所有模块的 gnmkdm、路径、名称。
        """
        self._base.ensure_login()
        return self._safe_json_get("/jwglxt/xtgl/index_cxMenuList.html")

    def browser_check(self) -> str:
        """浏览器检测"""
        return self._base.get("/jwglxt/xtgl/init_cxBrowser.html").text

    def change_language(self) -> str:
        """切换语言"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/init_changeLocal.html").text

    def change_password_page(self) -> str:
        """修改密码页面"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/mmgl_xgMm.html").text

    def change_role(self) -> str:
        """切换角色页面"""
        self._base.ensure_login()
        return self._base.get("/jwglxt/xtgl/index_changeRole.html").text

    def report_params(self) -> str:
        """获取报表参数"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/report_cxReportParams.html").text

    def academic_warning_tx(self) -> str:
        """学业预警提醒"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXsxyyjtx.html").text

    def absentee_warning_update(self) -> str:
        """旷课预警状态更新"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxKkyjxxUpdate.html").text

    def add_recent_function(self) -> str:
        """添加最近使用功能"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxBczjsygnmk.html").text

    def download_file(self) -> bytes:
        """下载文件"""
        return self._base.get("/jwglxt/xtgl/file_cxDownFile.html").content

    def view_file(self) -> bytes:
        """查看文件"""
        return self._base.get("/jwglxt/xtgl/file_cxViewFile.html").content

    def logout_page(self) -> str:
        """完全退出登录页面"""
        return self._base.get("/jwglxt/xtgl/dl_logout.html").text
