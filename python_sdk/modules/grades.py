"""成绩查询模块"""
import json
import time
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery
from ..models.data import GradeItem, GradeQueryResult


class GradeModule:
    """成绩查询"""

    _ENDPOINT = "/jwglxt/cjcx/cjcx_cxDgXscj.html"
    _GNMKDM = "N305005"

    def __init__(self, base: JwxtBase):
        self._base = base

    def query(self, year: str, term: str, query: Optional[PageQuery] = None) -> GradeQueryResult:
        """查询学期成绩

        Args:
            year: 学年起始年份，如 '2025'
            term: 学期编码，'3'=第一学期, '12'=第二学期
        """
        self._base.ensure_login()
        q = query or PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._ENDPOINT}?doType=query&gnmkdm={self._GNMKDM}",
            data=data,
        )
        raw = resp.json()
        items = [GradeItem(**item) for item in raw.get("items", [])]
        return GradeQueryResult(items=items, total=raw.get("totalResult", 0))

    def detail(self, class_id: str) -> str:
        """获取课程分项成绩页面"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(jxb_id=class_id, xh=self._base.username)
        resp = self._base.post(
            f"{self._ENDPOINT}?doType=details&gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def statistics(self) -> str:
        """获取成绩统计页面"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.get(
            f"{self._ENDPOINT}?doType=statistics&gnmkdm={self._GNMKDM}&time={ts}"
        )
        return resp.text
