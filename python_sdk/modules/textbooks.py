"""教材管理模块"""
import time

from ..base import JwxtBase


class TextbookModule:
    """教材管理"""

    _ENDPOINTS = {
        "booking": ("/jwglxt/jcydgl/xsjcyd_cxXsjcydIndex.html", "N253545"),
        "fee_confirm": ("/jwglxt/jcjsgl/xsjs_cxJcfyqrIndex.html", "N758066"),
        "plan_apply": ("/jwglxt/jczdgl/jhjczdsq_cxJhjczdsqIndex.html", "N757010"),
    }

    def __init__(self, base: JwxtBase):
        self._base = base

    def booking(self) -> str:
        return self._get_page("booking")

    def fee_confirm(self) -> str:
        return self._get_page("fee_confirm")

    def plan_apply(self) -> str:
        return self._get_page("plan_apply")

    def _get_page(self, key: str) -> str:
        self._base.ensure_login()
        path, gnmkdm = self._ENDPOINTS[key]
        ts = int(time.time() * 1000)
        resp = self._base.get(f"{path}?gnmkdm={gnmkdm}&time={ts}")
        return resp.text
