"""学生评价模块"""
import time

from ..base import JwxtBase


class EvaluationModule:
    """学生评价"""

    _ENDPOINTS = {
        "student": ("/jwglxt/xspjgl/xspj_cxXspjIndex.html", "N401605"),
        "supervisor": ("/jwglxt/jxbpjgl/ddpjkc_cxDdpjkcIndex.html", "N401637"),
        "leader": ("/jwglxt/jxbpjgl/ldpjkc_cxLdpjkcIndex.html", "N401642"),
    }

    def __init__(self, base: JwxtBase):
        self._base = base

    def student(self) -> str:
        return self._get_page("student")

    def supervisor(self) -> str:
        return self._get_page("supervisor")

    def leader(self) -> str:
        return self._get_page("leader")

    def _get_page(self, key: str) -> str:
        self._base.ensure_login()
        path, gnmkdm = self._ENDPOINTS[key]
        ts = int(time.time() * 1000)
        resp = self._base.get(f"{path}?gnmkdm={gnmkdm}&time={ts}")
        return resp.text
