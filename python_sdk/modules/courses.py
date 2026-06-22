"""选课管理模块

所有接口从 zzxkYzb.js 逆向提取，含完整参数格式。
选课操作受时间窗口限制，非选课期仅返回空列表或页面框架。
"""
import re
from typing import Optional

from bs4 import BeautifulSoup

from ..base import JwxtBase
from ..models.common import PageQuery
from ..models.data import CourseItem, CourseClassDetail, CourseQueryResult, CourseClassResult


class CourseModule:
    """选课管理"""

    _GNMKDM = "N253512"
    _BASE = "/jwglxt/xsxk/zzxkyzb"

    def __init__(self, base: JwxtBase):
        self._base = base
        self._context: Optional[dict] = None

    # ================================================================
    # 数据查询接口 (JSON)
    # ================================================================

    def display(self,
                xkkz_id: str, kklxdm: str,
                njdm_id: str = "", zyh_id: str = "",
                xszxzt: str = "", kspage: int = 0, jspage: int = 0) -> CourseQueryResult:
        """查询选课课程列表（主查询，对应页签切换）

        Args:
            xkkz_id: 选课控制ID
            kklxdm: 选课类型代码
            njdm_id: 年级代码
            zyh_id: 专业代码
            xszxzt: 学生在线状态
            kspage: 起始页
            jspage: 结束页
        """
        self._base.ensure_login()
        data = {
            "xkkz_id": xkkz_id, "kklxdm": kklxdm,
            "xszxzt": xszxzt, "njdm_id": njdm_id, "zyh_id": zyh_id,
            "kspage": kspage, "jspage": jspage,
        }
        resp = self._base.post(f"{self._BASE}_cxZzxkYzbDisplay.html", data=data)
        try:
            resp.raise_for_status()
            raw = resp.json()
            items = [CourseItem(**item) for item in raw.get("tmpList", [])]
        except Exception:
            items = []
        return CourseQueryResult(items=items)

    def search(self, xkkz_id: str, kklxdm: str,
               xkxnm: str, xkxqm: str,
               njdm_id: str = "", zyh_id: str = "",
               kspage: int = 0, jspage: int = 20, **filters) -> CourseQueryResult:
        """分页搜索课程（高级查询，searchBox 触发）

        Args:
            xkkz_id: 选课控制ID
            kklxdm: 选课类型代码
            xkxnm: 选课学年
            xkxqm: 选课学期
            njdm_id: 年级代码
            zyh_id: 专业代码
            kspage: 起始页码
            jspage: 结束页码
            **filters: 筛选条件 (key 对应页面上的 hidden input id)
        """
        self._base.ensure_login()
        data = {
            "xkkz_id": xkkz_id, "kklxdm": kklxdm,
            "xkxnm": xkxnm, "xkxqm": xkxqm,
            "njdm_id": njdm_id, "zyh_id": zyh_id,
            "kspage": kspage + 1, "jspage": jspage,
            "xklc": filters.get("xklc", ""),
            "xkly": filters.get("xkly", ""),
            "bklx_id": filters.get("bklx_id", ""),
            "sfkkjyxdxnxq": filters.get("sfkkjyxdxnxq", ""),
            "xqh_id": filters.get("xqh_id", ""),
            "jg_id": filters.get("jg_id", ""),
            "zyfx_id": filters.get("zyfx_id", ""),
            "bh_id": filters.get("bh_id", ""),
            "xbm": filters.get("xbm", ""),
            "xslbdm": filters.get("xslbdm", ""),
            "mzm": filters.get("mzm", ""),
            "xz": filters.get("xz", ""),
            "ccdm": filters.get("ccdm", ""),
            "xsbj": filters.get("xsbj", ""),
            "sfkknj": filters.get("sfkknj", ""),
            "sfkkzy": filters.get("sfkkzy", ""),
            "kzybkxy": filters.get("kzybkxy", ""),
            "sfznkx": filters.get("sfznkx", ""),
            "zdkxms": filters.get("zdkxms", ""),
            "sfkxq": filters.get("sfkxq", ""),
            "bhbcyxkjxb": filters.get("bhbcyxkjxb", ""),
            "sfkcfx": filters.get("sfkcfx", ""),
            "kkbk": filters.get("kkbk", ""),
            "kkbkdj": filters.get("kkbkdj", ""),
            "bklbkcj": filters.get("bklbkcj", ""),
            "sfkgbcx": filters.get("sfkgbcx", ""),
            "sfrxtgkcxd": filters.get("sfrxtgkcxd", ""),
            "tykczgxdcs": filters.get("tykczgxdcs", ""),
            "gnjkxdnj": filters.get("gnjkxdnj", ""),
            "bjgkczxbbjwcx": filters.get("bjgkczxbbjwcx", ""),
            "bbhzxjxb": filters.get("bbhzxjxb", ""),
            "kzkcgs": filters.get("kzkcgs", ""),
            "rwlx": filters.get("rwlx", ""),
            "rlkz": filters.get("rlkz", ""),
            "xkzgbj": filters.get("xkzgbj", ""),
        }
        resp = self._base.post(f"{self._BASE}_cxZzxkYzbPartDisplay.html", data=data)
        try:
            resp.raise_for_status()
            raw = resp.json()
            items = [CourseItem(**item) for item in raw.get("tmpList", [])]
        except Exception:
            items = []
        return CourseQueryResult(items=items)

    def selected(self) -> list[dict]:
        """已选课程列表"""
        self._base.ensure_login()
        try:
            resp = self._base.post(f"{self._BASE}_cxZzxkYzbChoosed.html", data={})
            resp.raise_for_status()
        except Exception:
            return []
        try:
            data = resp.json()
            return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        except Exception:
            return []

    def class_detail(self, kch_id: str, jxb_id: str, xkkz_id: str, kklxdm: str,
                     xkxnm: str, xkxqm: str, **fields) -> CourseClassResult:
        """教学班详情（点击课程展开）

        Args:
            kch_id: 课程ID
            jxb_id: 教学班ID (可选，用于定位具体教学班)
            xkkz_id: 选课控制ID
            kklxdm: 选课类型代码
            xkxnm: 学年
            xkxqm: 学期
        """
        self._base.ensure_login()
        data = {
            "kch_id": kch_id, "jxb_id": jxb_id,
            "xkkz_id": xkkz_id, "kklxdm": kklxdm,
            "xkxnm": xkxnm, "xkxqm": xkxqm,
            "rwlx": fields.get("rwlx", ""),
            "xkly": fields.get("xkly", ""),
            "bklx_id": fields.get("bklx_id", ""),
            "sfkkjyxdxnxq": fields.get("sfkkjyxdxnxq", ""),
            "kzkcgs": fields.get("kzkcgs", ""),
            "xqh_id": fields.get("xqh_id", ""),
            "jg_id": fields.get("jg_id", ""),
            "zyfx_id": fields.get("zyfx_id", ""),
            "njdm_id": fields.get("njdm_id", ""),
            "zyh_id": fields.get("zyh_id", ""),
            "bh_id": fields.get("bh_id", ""),
            "xbm": fields.get("xbm", ""),
            "xslbdm": fields.get("xslbdm", ""),
            "mzm": fields.get("mzm", ""),
            "xz": fields.get("xz", ""),
            "ccdm": fields.get("ccdm", ""),
            "xsbj": fields.get("xsbj", ""),
            "sfkknj": fields.get("sfkknj", ""),
            "sfkkzy": fields.get("sfkkzy", ""),
            "kzybkxy": fields.get("kzybkxy", ""),
            "sfznkx": fields.get("sfznkx", ""),
            "zdkxms": fields.get("zdkxms", ""),
            "sfkxq": fields.get("sfkxq", ""),
            "bhbcyxkjxb": fields.get("bhbcyxkjxb", ""),
            "sfkcfx": fields.get("sfkcfx", ""),
            "bbhzxjxb": fields.get("bbhzxjxb", ""),
            "kkbk": fields.get("kkbk", ""),
            "kkbkdj": fields.get("kkbkdj", ""),
            "bklbkcj": fields.get("bklbkcj", ""),
            "rlkz": fields.get("rlkz", ""),
            "gnjkxdnj": fields.get("gnjkxdnj", ""),
            "txbsfrl": fields.get("txbsfrl", ""),
            "cdrlkz": fields.get("cdrlkz", ""),
            "rlzlkz": fields.get("rlzlkz", ""),
            "xklc": fields.get("xklc", ""),
            "cxbj": fields.get("cxbj", ""),
            "fxbj": fields.get("fxbj", ""),
            "xkxskcgskg": fields.get("xkxskcgskg", ""),
            "jxbzcxskg": fields.get("jxbzcxskg", ""),
        }
        resp = self._base.post(
            f"/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html", data=data
        )
        try:
            resp.raise_for_status()
            raw = resp.json()
            items = [CourseClassDetail(**item) for item in raw] if isinstance(raw, list) else []
        except Exception:
            items = []
        return CourseClassResult(items=items)

    # ================================================================
    # 选课操作
    # ================================================================

    def quick_select(self, xkkz_id: str) -> dict:
        """一键选课"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}_xkZzxkyzbQuickly.html",
            data={"xkkz_id": xkkz_id},
        )
        try:
            return resp.json()
        except Exception:
            return {"flag": "0", "msg": "选课未开放或请求失败"}

    def check_credit(self, xnm: str, xqm: str, njdm_id: str,
                     zyh_id: str, kklxdm: str) -> dict:
        """学分检查"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}_cxCheckZzxkyzbXfmcBynjzy.html",
            data={"xnm": xnm, "xqm": xqm, "njdm_id": njdm_id,
                  "zyh_id": zyh_id, "kklxdm": kklxdm},
        )
        return {"result": resp.text}

    def credit_validation(self, kklxdm: str) -> dict:
        """学年学分验证"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}_cxZzxkyzbLnyhxf.html",
            data={"kklxdm": kklxdm},
        )
        return {"credit": resp.text}

    # ================================================================
    # 信息查看 (页面)
    # ================================================================

    def credit_requirement(self, kklxdm: str) -> str:
        """学分要求查看"""
        self._base.ensure_login()
        resp = self._base.post(
            f"{self._BASE}_cxYinxyixxfView.html",
            data={"kklxdm": kklxdm},
        )
        return resp.text

    def course_rules(self, xkkz_id: str, kklxdm: str) -> str:
        """选课规则"""
        self._base.ensure_login()
        resp = self._base.post(
            "/jwglxt/xkgzsz/jbxkgzsz_cxJbxkgzsz.html",
            data={"xkkz_id": xkkz_id, "kklxdm": kklxdm},
        )
        return resp.text

    def teacher_info(self, jgh_id: str, kch_id: str) -> str:
        """教师简介弹窗"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_cxJsxxModel.html?jgh_id={jgh_id}&kch_id={kch_id}"
        )
        return resp.text

    def course_info(self, kch_id: str) -> str:
        """课程简介弹窗"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_cxKcxxModel.html?kch_id={kch_id}"
        )
        return resp.text

    def class_enrollment_detail(self, kch_id: str, jxb_id: str,
                                xnm: str, xqm: str) -> str:
        """教学班人数明细"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_cxJxbrsmxIndex.html"
            f"?kch_id={kch_id}&jxb_id={jxb_id}&xnm={xnm}&xqm={xqm}"
        )
        return resp.text

    def textbook_info(self, jxb_id: str) -> str:
        """教材信息弹窗"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xsxk/tjxkyzb_cxJcxxList.html?jxb_id={jxb_id}"
        )
        return resp.text

    def course_remark(self, jxb_id: str) -> str:
        """选课备注"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xsxk/tjxkyzb_cxXkbzMsg.html?jxb_id={jxb_id}"
        )
        return resp.text

    def schedule_preview(self, xnm: str, xqm: str) -> str:
        """课表预览（选课页内弹窗）"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/kbcx/xskbcx_cxXskbPopupIndex.html?xnm={xnm}&xqm={xqm}"
        )
        return resp.text

    # ================================================================
    # 下拉条件查询 (供高级搜索使用)
    # ================================================================

    def filter_colleges(self, locale_key: str = "zh_CN") -> list[dict]:
        """开课学院列表"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_queryKkbmPaged.html?localeKey={locale_key}"
        )
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_grades(self, njdm_id: str = "") -> list[dict]:
        """年级列表"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_queryNjPaged.html?njdm_id={njdm_id}"
        )
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_majors(self, locale_key: str = "zh_CN", jg_id: str = "",
                      zyh_id: str = "") -> list[dict]:
        """专业列表"""
        self._base.ensure_login()
        resp = self._base.get(
            f"/jwglxt/xkgl/common_queryZyPaged.html"
            f"?localeKey={locale_key}&jg_id={jg_id}&zyh_id={zyh_id}"
        )
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_campus(self) -> list[dict]:
        """校区列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_queryXquListPaged.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_course_types(self) -> list[dict]:
        """课程类别列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_queryKclbListPaged.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_course_natures(self) -> list[dict]:
        """课程性质列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_queryKcxzPaged.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_course_groups(self) -> list[dict]:
        """课程归属列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_queryKcgsPaged.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_course_clusters(self) -> list[dict]:
        """课程组列表"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_queryKczPaged.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_teach_modes(self) -> list[dict]:
        """教学模式"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xtgl/comm_cxJcsjList.html?lxdm=0032")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_weekdays(self) -> list[dict]:
        """上课星期"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xtgl/comm_cxJcsjList.html?lxdm=0036")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    def filter_periods(self) -> list[dict]:
        """上课节次"""
        self._base.ensure_login()
        resp = self._base.get("/jwglxt/xkgl/common_querySkjcList.html")
        data = resp.json()
        return data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    # ================================================================
    # 页面加载 (HTML)
    # ================================================================

    def index_page(self) -> str:
        """选课首页"""
        self._base.ensure_login()
        resp = self._base.get(
            f"{self._BASE}_cxZzxkYzbIndex.html?gnmkdm={self._GNMKDM}&layout=default"
        )
        return resp.text

    # ================================================================
    # 上下文解析
    # ================================================================

    def get_context(self, force_refresh: bool = False) -> dict:
        """解析选课首页，提取 xkkz_id、kklxdm 等必要参数

        返回 dict:
            in_period:   是否在选课期
            xkkz_id:     选课控制ID
            kklxdm_list: 可选课程类型列表 [{code, name, idx}]
            njdm_id:     年级代码
            zyh_id:      专业代码
            xkkz_xh:     选课序号
            xklc:        选课轮次
            xkxnm:       选课学年
            xkxqm:       选课学期
        """
        if self._context and not force_refresh:
            return self._context

        html = self.index_page()
        soup = BeautifulSoup(html, 'html.parser')
        ctx = {
            "in_period": False,
            "xkkz_id": "",
            "kklxdm_list": [],
            "njdm_id": "",
            "zyh_id": "",
            "xkkz_xh": "",
            "xklc": "",
            "xkxnm": "",
            "xkxqm": "",
        }

        # 检查是否在选课期
        nodata = soup.select_one('.nodata span')
        if nodata and '不属' in (nodata.get_text(strip=True) or ''):
            ctx["in_period"] = False
            self._context = ctx
            return ctx

        ctx["in_period"] = True

        # 提取 hidden inputs
        for inp in soup.find_all('input', type='hidden'):
            name = inp.get('name', '')
            val = inp.get('value', '')
            if name in ctx and val:
                ctx[name] = val

        # 从 script 中提取 kklxdm 选项卡定义
        # 模式: queryCourse(a_element, kklxdm, xkkz_id, ...)
        for script in soup.find_all('script'):
            if not script.string:
                continue
            for m in re.finditer(
                r"queryCourse\s*\(\s*[^,]+,\s*['\"](\d+)['\"]",
                script.string
            ):
                code = m.group(1)
                if code not in [k['code'] for k in ctx['kklxdm_list']]:
                    ctx['kklxdm_list'].append({
                        "code": code,
                        "name": "",
                        "idx": len(ctx['kklxdm_list']),
                    })

        # 提取 kklxdm 的 display name (从 i18n 或 tab title)
        for script in soup.find_all('script'):
            if not script.string:
                continue
            for m in re.finditer(
                r"['\"]msg_(\w+)['\"]\s*:\s*['\"]([^'\"]+)['\"]",
                script.string
            ):
                key, name = m.group(1), m.group(2)
                if key.startswith('kklxdm'):
                    code = key[6:] if len(key) > 6 else ''
                    for item in ctx['kklxdm_list']:
                        if item['code'] == code:
                            item['name'] = name

        # 默认 kklxdm 为第一个
        if not ctx['kklxdm_list']:
            # 从学期数据推测常见值
            from ..jwxt_client import JwxtClient
            try:
                sem = JwxtClient.current_semester()
            except Exception:
                sem = None
            ctx['xkxnm'] = sem.year if sem else ""
            ctx['xkxqm'] = sem.term if sem else ""

        self._context = ctx
        return ctx

    # ================================================================
    # 选课操作
    # ================================================================

    def select_course(self, jxb_id: str, do_jxb_id: str = "",
                      kch_id: str = "", jxbzls: str = "",
                      xkkz_id: str = "", kklxdm: str = "",
                      **extra) -> dict:
        """选课 — 提交单个教学班

        Args:
            jxb_id:    教学班ID
            do_jxb_id: 目标教学班ID (换班时使用)
            kch_id:    课程ID
            jxbzls:    教学班总容量标记
            xkkz_id:   选课控制ID (不传自动从页面提取)
            kklxdm:    选课类型代码 (不传自动从页面提取)
        """
        self._base.ensure_login()
        if not xkkz_id or not kklxdm:
            ctx = self.get_context()
            xkkz_id = xkkz_id or ctx.get("xkkz_id", "")
            kklxdm = kklxdm or (ctx["kklxdm_list"][0]["code"] if ctx.get("kklxdm_list") else "")

        data = {
            "jxb_id": jxb_id,
            "do_jxb_id": do_jxb_id,
            "kch_id": kch_id,
            "jxbzls": jxbzls,
            "xkkz_id": xkkz_id,
            "kklxdm": kklxdm,
            **extra,
        }
        resp = self._base.post(f"{self._BASE}_xkBcZyZzxkYzb.html", data=data)
        try:
            return resp.json()
        except Exception:
            return {"flag": "0", "msg": resp.text}

    def drop_course(self, jxb_id: str, do_jxb_id: str = "",
                    kch_id: str = "", xkkz_id: str = "",
                    kklxdm: str = "", **extra) -> dict:
        """退课 — 退选单个教学班

        Args:
            jxb_id:    教学班ID
            do_jxb_id: 目标教学班ID (换班时使用)
            kch_id:    课程ID
            xkkz_id:   选课控制ID (不传自动从页面提取)
            kklxdm:    选课类型代码 (不传自动从页面提取)
        """
        self._base.ensure_login()
        if not xkkz_id or not kklxdm:
            ctx = self.get_context()
            xkkz_id = xkkz_id or ctx.get("xkkz_id", "")
            kklxdm = kklxdm or (ctx["kklxdm_list"][0]["code"] if ctx.get("kklxdm_list") else "")

        data = {
            "jxb_id": jxb_id,
            "do_jxb_id": do_jxb_id,
            "kch_id": kch_id,
            "xkkz_id": xkkz_id,
            "kklxdm": kklxdm,
            **extra,
        }
        resp = self._base.post(f"{self._BASE}_tuikBcZzxkYzb.html", data=data)
        try:
            return resp.json()
        except Exception:
            return {"flag": "0", "msg": resp.text}

    def list_all_courses(self, xkkz_id: str = "",
                         kklxdm: str = "") -> list[dict]:
        """遍历所有课程类型的可选课程，返回汇总列表"""
        self._base.ensure_login()
        ctx = self.get_context()
        if not ctx["in_period"]:
            return []

        xkkz_id = xkkz_id or ctx["xkkz_id"]
        if not ctx["kklxdm_list"]:
            return []

        # 如果指定了 kklxdm，只查询该类型
        targets = [k for k in ctx["kklxdm_list"] if not kklxdm or k["code"] == kklxdm]
        if kklxdm and not targets:
            targets = [{"code": kklxdm, "name": "", "idx": 0}]

        all_courses = []
        for kk in targets:
            result = self.display(
                xkkz_id=xkkz_id,
                kklxdm=kk["code"],
                njdm_id=ctx.get("njdm_id", ""),
                zyh_id=ctx.get("zyh_id", ""),
            )
            for item in result.items:
                all_courses.append({
                    "kklxdm": kk["code"],
                    "kklxdm_name": kk.get("name", ""),
                    "course_code": item.course_code,
                    "course_name": item.course_name,
                    "credit": item.credit,
                    "class_id": item.class_id,
                    "class_name": item.class_name,
                    "capacity": item.capacity,
                    "selected_count": item.selected_count,
                    "is_recommended": item.is_recommended,
                    "kc_row": item.kc_row,
                })
        return all_courses
