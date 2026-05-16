"""系统信息模块"""
from ..base import JwxtBase


class SystemModule:
    """系统提示、预警等"""

    def __init__(self, base: JwxtBase):
        self._base = base

    def tips(self) -> str:
        """系统提示（学分未修满等）"""
        self._base.ensure_login()
        resp = self._base.post("/jwglxt/xtgl/index_cxXttsxx.html?bj=2")
        return resp.text

    def absentee_warning(self) -> str:
        """旷课预警"""
        self._base.ensure_login()
        resp = self._base.post("/jwglxt/xtgl/index_cxKkyjxx.html")
        return resp.text

    def labor_warning(self) -> str:
        """劳育预警"""
        self._base.ensure_login()
        resp = self._base.post("/jwglxt/xtgl/index_cxLyyjxx.html")
        return resp.text

    def academic_warning_list(self) -> str:
        """学业预警列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xtgl/index_cxXsxyyjtxIndex.html")
        return resp.text
