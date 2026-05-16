"""课表查询模块"""
import time
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery


class ScheduleModule:
    """课表查询"""

    _GNMKDM = "N2151"

    def __init__(self, base: JwxtBase):
        self._base = base

    def page(self) -> str:
        """获取课表页面 HTML（含本学期课表数据）"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.get(
            f"/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm={self._GNMKDM}&layout=default&time={ts}"
        )
        return resp.text

    def personal(self, year: str, term: str) -> dict:
        """个人课表数据"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.json()

    def classroom(self, year: str, term: str, room: str = "") -> str:
        """教室课表"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term, jsmc=room)
        resp = self._base.post(
            f"/jwglxt/kbcx/jskbcx_cxJskb.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.text

    def teacher(self, year: str, term: str, name: str = "") -> dict:
        """教师课表"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term, jsmc=name)
        resp = self._base.post(
            f"/jwglxt/kbcx/jskbcx_cxJsKb.html?gnmkdm={self._GNMKDM}",
            data=data,
        )
        return resp.json()

    def class_group(self, year: str, term: str) -> str:
        """班级课表"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=year, xqm=term)
        resp = self._base.post(
            f"/jwglxt/kbcx/xskbcx_cxBjKb.html?gnmkdm=N253501",
            data=data,
        )
        return resp.text

    def credit_confirm(self) -> str:
        """课表/学分确认页面"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.get(
            f"/jwglxt/kbcx/xskbqr_cxXskbqrIndex.html?gnmkdm=N2158&time={ts}"
        )
        return resp.text
