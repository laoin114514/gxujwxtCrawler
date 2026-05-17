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

    def export_table(self, xnm: str = "", xqm: str = "") -> str:
        """课表导出 (表格)"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=xnm, xqm=xqm)
        resp = self._base.post(
            "/jwglxt/kbcx/xskbcx_cxDcExcelXskb.html?doType=table&gnmkdm=N2151",
            data=data,
        )
        return resp.text

    def export_list(self, xnm: str = "", xqm: str = "") -> str:
        """课表导出 (列表)"""
        self._base.ensure_login()
        q = PageQuery()
        data = q.to_form_data(xnm=xnm, xqm=xqm)
        resp = self._base.post(
            "/jwglxt/kbcx/xskbcx_cxDcExcelXskblb.html?doType=list&gnmkdm=N2151",
            data=data,
        )
        return resp.text

    def simple_view(self) -> str:
        """课表简洁版"""
        self._base.ensure_login()
        return self._base.get(
            "/jwglxt/kbcx/xskbcx_cxXskbSimpleIndex.html?gnmkdm=N2151"
        ).text

    def credit_confirm_detail(self) -> str:
        """课表确认详情查询"""
        self._base.ensure_login()
        q = PageQuery()
        resp = self._base.post(
            "/jwglxt/kbcx/xskbqr_cxXskbqrIndex.html?doType=query&gnmkdm=N2158",
            data=q.to_form_data(),
        )
        return resp.text

    def credit_confirm_submit(self) -> str:
        """课表确认提交"""
        self._base.ensure_login()
        resp = self._base.post(
            "/jwglxt/kbcx/xskbqr_qrXskbqr.html?gnmkdm=N2158"
        )
        return resp.text
