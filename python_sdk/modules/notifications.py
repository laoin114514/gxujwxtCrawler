"""通知公告 & 待办事项模块"""
from typing import Optional

from ..base import JwxtBase
from ..models.common import PageQuery
from ..models.data import (
    NotificationItem, NotificationQueryResult,
    TodoItem, TodoQueryResult,
)


class NotificationModule:
    """通知公告 & 待办事项"""

    def __init__(self, base: JwxtBase):
        self._base = base

    # ---- 通知公告 ----

    def list(self, query: Optional[PageQuery] = None) -> NotificationQueryResult:
        """通知公告列表"""
        self._base.ensure_login()
        q = query or PageQuery(page_size=15, sort_name=" ", sort_order="desc")
        data = q.to_form_data()
        data["time"] = 0
        resp = self._base.post(
            "/jwglxt/xtgl/xwck_cxMoreXwList.html?doType=query",
            data=data,
        )
        raw = resp.json()
        items = [NotificationItem(**item) for item in raw.get("items", [])]
        return NotificationQueryResult(items=items, total=raw.get("totalResult", 0))

    def detail(self, news_id: str) -> str:
        """通知详情 HTML"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xtgl/xwck_ckXw.html?xwbh={news_id}&doType=save"
        )
        return resp.text

    # ---- 待办事项 ----

    def todos(self, query: Optional[PageQuery] = None) -> TodoQueryResult:
        """待办事项列表"""
        self._base.ensure_login()
        q = query or PageQuery(page_size=15, sort_name="cjsj ", sort_order="desc")
        data = q.to_form_data()
        data["flag"] = "1"
        data["sfyy"] = "1"
        data["time"] = 0
        resp = self._base.post(
            "/jwglxt/xtgl/index_cxDbsy.html?doType=query",
            data=data,
        )
        raw = resp.json()
        items = [TodoItem(**item) for item in raw.get("items", [])]
        return TodoQueryResult(items=items, total=raw.get("totalResult", 0))
