"""首页数据模块"""
import time

from ..base import JwxtBase


class HomepageModule:
    """首页各区域数据"""

    _AREAS = {
        "schedule": "/jwglxt/xtgl/index_cxAreaOne.html",
        "files": "/jwglxt/xtgl/index_cxAreaTwo.html",
        "messages": "/jwglxt/xtgl/index_cxAreaThree.html",
        "grades_exams": "/jwglxt/xtgl/index_cxAreaFour.html",
        "calendar": "/jwglxt/xtgl/index_cxAreaFive.html",
        "calendar_files": "/jwglxt/xtgl/index_cxAreaSix.html",
        "news": "/jwglxt/xtgl/index_cxNews.html",
    }

    def __init__(self, base: JwxtBase):
        self._base = base

    def all(self) -> dict[str, str | None]:
        """获取首页所有区域 HTML"""
        self._base.ensure_login()
        result = {}
        for name, path in self._AREAS.items():
            try:
                resp = self._base.post(f"{path}?localeKey=zh_CN&gnmkdm=index")
                result[name] = resp.text
            except Exception:
                result[name] = None
        return result

    def user_info_html(self) -> str:
        """用户信息 HTML 片段（姓名、学号、院系、照片）"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.post(
            f"/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_={ts}&gnmkdm=index"
        )
        return resp.text

    def photo_url(self, student_id: str = "") -> str:
        """学生照片 URL"""
        sid = student_id or self._base.username
        return f"/jwglxt/xtgl/photo_cxXszp4.html?xh_id={sid}&zplx=rxqzp"

    def my_apps(self) -> list:
        """我的应用列表"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.post(
            f"/jwglxt/xtgl/index_cxWdyy.html?localeKey=zh_CN&gnmkdm=index&time={ts}"
        )
        try:
            return resp.json()
        except Exception:
            return []

    def recently_used(self) -> list:
        """最近使用"""
        self._base.ensure_login()
        ts = int(time.time() * 1000)
        resp = self._base.post(
            f"/jwglxt/xtgl/index_cxZjsy.html?localeKey=zh_CN&gnmkdm=index&time={ts}"
        )
        try:
            return resp.json()
        except Exception:
            return []
