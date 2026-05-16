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

    def _json_number(self, path: str) -> int:
        """POST 获取 JSON 数字结果"""
        try:
            self._base.ensure_login()
            return self._base.post(path).json()
        except Exception:
            return 0

    def pending_textbook_apply(self) -> int:
        """教材申请未提交数量"""
        return self._json_number("/jwglxt/xtgl/index_cxJhkcjcsqWtjNum.html")

    def elective_credit_deficiency(self) -> dict:
        """公选课学分未修满"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXsGxkxfwxm.html").json()

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
        return self._base.post("/jwglxt/xtgl/index_cxFxjftsNum.html").json()

    def minor_fee_reminder_update(self) -> str:
        """更新辅修提醒状态"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxUpdateFxjftszt.html").text

    def thesis_topic_time(self) -> dict:
        """毕设选题时间"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxBsxtsj.html").json()

    def credit_confirm_time(self) -> dict:
        """学分确认时间"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxXfqrsj.html").json()

    def role_enabled(self) -> dict:
        """角色是否启用"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxJssfqy.html").json()

    def set_default_role(self) -> dict:
        """设置默认角色"""
        self._base.ensure_login()
        return self._base.post("/jwglxt/xtgl/index_cxSzmrjs.html").json()

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
        return self._base.post("/jwglxt/xtgl/index_cxXxdlztgx.html").json()

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
