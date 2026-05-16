"""选课管理模块"""
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery


class CourseModule:
    """选课管理"""

    _GNMKDM = "N253512"

    def __init__(self, base: JwxtBase):
        self._base = base

    def available(self, year: str, term: str, keyword: str = "", query: Optional[PageQuery] = None) -> str:
        """可选课程列表"""
        self._base.ensure_login()
        q = query or PageQuery()
        data = q.to_form_data(xnm=year, xqm=term, kcmc=keyword)
        resp = self._base.post(
            f"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def selected(self, year: str = "", term: str = "") -> str:
        """已选课程"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"/jwglxt/xsxk/zzxkyzb_cxZzxkYzb.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text
