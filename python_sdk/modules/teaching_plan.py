"""教学执行计划模块"""
from ..base import JwxtBase
from ..models.common import PageQuery


class TeachingPlanModule:
    """教学执行计划 (N153540)"""

    _BASE = "/jwglxt/jxzxjhgl"
    _GNMKDM = "N153540"

    def __init__(self, base: JwxtBase):
        self._base = base

    # ---- 数据查询 ----

    def index_page(self) -> str:
        """执行计划首页"""
        self._base.ensure_login()
        return self._base.get(
            f"{self._BASE}/jxzxjhck_cxJxzxjhckIndex.html"
            f"?gnmkdm={self._GNMKDM}&layout=default"
        ).text

    def query_list(self) -> dict:
        """查询执行计划列表 (JSON)"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}/jxzxjhck_cxJxzxjhckIndex.html"
            f"?doType=query&gnmkdm={self._GNMKDM}"
        )
        return resp.json()

    def course_list(self, jh_id: str) -> dict:
        """查询执行计划课程列表 (JSON, 需先加载首页)

        Args:
            jh_id: 执行计划ID (jxzxjhxx_id)
        """
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}/jxzxjhkcxx_cxJxzxjhkcxxIndex.html"
            f"?doType=query&gnmkdm={self._GNMKDM}",
            data={"jxzxjhxx_id": jh_id},
        )
        try:
            return resp.json()
        except Exception:
            return {"_html": resp.text}

    # ---- 子页面 ----

    def requirements(self, jh_id: str) -> str:
        """修读要求页面

        Args:
            jh_id: 执行计划ID
        """
        self._base.ensure_login()
        try:
            resp = self._base.get(
                f"{self._BASE}/jxzxjhck_cxJxzxjhxdyqIndex.html"
                f"?jxzxjhxx_id={jh_id}"
            )
            return resp.text
        except Exception:
            # fallback: POST with form data
            resp = self._base.post(
                f"{self._BASE}/jxzxjhck_cxJxzxjhxdyqIndex.html",
                data={"jxzxjhxx_id": jh_id},
            )
            return resp.text

    def preview(self, jh_id: str) -> str:
        """预览执行计划"""
        self._base.ensure_login()
        return self._base.get(
            f"{self._BASE}/jxzxjhxxwh_cxDyJxzxjhxx.html"
            f"?jxzxjhxx_id={jh_id}"
        ).text

    def course_hours(self) -> str:
        """课程学时信息"""
        self._base.ensure_login()
        return self._base.post(
            "/jwglxt/kkqkcx/kkqkcx_cxKcxsxxGJH.html"
        ).text

    def course_info(self, kch: str) -> str:
        """课程详细信息"""
        self._base.ensure_login()
        return self._base.get(
            f"/jwglxt/jxjhgl/common_cxKcJbxx.html?id={kch}"
        ).text

    def syllabus_content(self) -> str:
        """教学大纲内容 (富文本)"""
        self._base.ensure_login()
        return self._base.post(
            "/jwglxt/query/query_cxFckContent.html",
            data={"content": "zwjxdg"},
        ).text

    def syllabus_attachment(self, file_path: str, file_name: str) -> bytes:
        """下载教学大纲附件"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/kckgl/kcdgsq_cxFjxx.html"
            f"?fjsclj={file_path}&fjm={file_name}"
        )
        return resp.content

    def export_main(self) -> str:
        """导出执行计划 (需先加载首页)"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}/jxzxjhck_dcJxzxjhckIndex.html"
            f"?gnmkdm={self._GNMKDM}"
        )
        return resp.text

    def export_courses(self) -> str:
        """导出课程信息 (需先加载首页)"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}/jxzxjhkcxx_dcJxzxjhkcxxIndex.html"
            f"?gnmkdm={self._GNMKDM}"
        )
        return resp.text
