"""选课管理模块"""
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery


class CourseModule:
    """选课管理

    注意: 选课数据查询受选课时间窗口限制，非选课期仅能获取页面框架。
    """

    _GNMKDM = "N253512"
    _BASE = "/jwglxt/xsxk/zzxkyzb"

    def __init__(self, base: JwxtBase):
        self._base = base

    # ---- 页面 ----

    def index_page(self) -> str:
        """选课首页（含可选课程列表框架）"""
        self._base.ensure_login()
        resp = self._base.get(
            f"{self._BASE}_cxZzxkYzbIndex.html?gnmkdm={self._GNMKDM}&layout=default"
        )
        return resp.text

    # ---- 可选课程 ----

    def available_list(self, year: str, term: str, keyword: str = "",
                       query: Optional[PageQuery] = None) -> str:
        """可选课程列表（需在选课期间，返回 HTML 含课程数据）"""
        self._base.ensure_login()
        q = query or PageQuery()
        data = q.to_form_data(xnm=year, xqm=term, kcmc=keyword)
        resp = self._base.post(
            f"{self._BASE}_cxZzxkYzbIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    # ---- 已选课程 ----

    def selected_page(self) -> str:
        """已选课程页面"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data()
        resp = self._base.post(
            f"{self._BASE}_cxZzxkYzb.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    # ---- 其他选课类型 ----

    def public_elective(self, year: str, term: str) -> str:
        """公选课列表"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._BASE}_cxGxkjxqkIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def all_school_elective(self, year: str, term: str) -> str:
        """全校选修课"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._BASE}_cxQxkcxkIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def pe_elective(self, year: str, term: str) -> str:
        """体育选课"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._BASE}_cxTykcxxkIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def retake_courses(self, year: str, term: str) -> str:
        """重修选课"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._BASE}_cxCxkccxIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def result_query(self) -> str:
        """选课结果查询"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data()
        resp = self._base.post(
            f"{self._BASE}_cxXskccjcx.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text
