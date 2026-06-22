"""考试安排模块"""
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery
from ..models.data import ExamItem, ExamQueryResult


class ExamModule:
    """考试安排"""

    _ENDPOINT = "/jwglxt/kwgl/kscx_cxXsksxxIndex.html"
    _GNMKDM = "N3580"

    def __init__(self, base: JwxtBase):
        self._base = base

    def query(self, year: str = "", term: str = "", query: Optional[PageQuery] = None) -> ExamQueryResult:
        """查询考试安排

        Args:
            year: 学年起始年份，不传则查询所有
            term: 学期编码，不传则查询所有
        """
        self._base.ensure_login()
        q = query or PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"{self._ENDPOINT}?doType=query&gnmkdm={self._GNMKDM}",
            data=data, 
        )
        raw = resp.json()
        items = [ExamItem(**item) for item in raw.get("items", [])]
        return ExamQueryResult(items=items, total=raw.get("totalResult", 0))
