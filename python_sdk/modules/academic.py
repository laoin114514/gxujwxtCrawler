"""学业情况 & 学籍预警模块"""
import time

from ..base import JwxtBase


class AcademicModule:
    """学业情况、学籍预警"""

    def __init__(self, base: JwxtBase):
        self._base = base

    def status(self) -> str:
        """学业情况页面（已修学分、培养方案进度等）"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.get(
            f"/jwglxt/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&time={ts}"
        )
        return resp.text

    def warning(self) -> str:
        """学籍预警页面"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.get(
            f"/jwglxt/xjyj/xjyj_cxXjyjIndex.html?gnmkdm=N105505&time={ts}"
        )
        return resp.text
