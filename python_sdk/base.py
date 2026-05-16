"""核心层：HTTP 客户端、RSA 加密、认证"""
import json
import time
import base64
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

from .exceptions import LoginError, NotLoggedInError


class JwxtBase:
    """教务系统核心客户端

    提供 HTTP 请求、RSA 加密、登录认证等底层能力。
    业务模块通过组合方式持有本实例。
    """

    BASE_URL = "https://jwxt2018.gxu.edu.cn"
    _LOGIN_PATH = "/jwglxt/xtgl/login_slogin.html"
    _PUBLIC_KEY_PATH = "/jwglxt/xtgl/login_getPublicKey.html"
    _INIT_MENU_PATH = "/jwglxt/xtgl/index_initMenu.html"

    def __init__(self, username: str, password: str, base_url: Optional[str] = None):
        self.username = username
        self._password = password
        if base_url:
            self.BASE_URL = base_url
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self._logged_in = False
        self._csrftoken: Optional[str] = None

    # ========== HTTP ==========

    def get(self, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("Referer", self._referer())
        r = self._session.get(self._url(path), **kwargs)
        r.raise_for_status()
        return r

    def post(self, path: str, data=None, **kwargs) -> requests.Response:
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault("Referer", self._referer())
        kwargs["headers"].setdefault("Content-Type", "application/x-www-form-urlencoded")
        kwargs.setdefault("allow_redirects", True)
        r = self._session.post(self._url(path), data=data, **kwargs)
        r.raise_for_status()
        return r

    def _url(self, path: str) -> str:
        return urljoin(self.BASE_URL, path)

    def _referer(self) -> str:
        return self.BASE_URL + "/jwglxt/xtgl/index_initMenu.html"

    # ========== 加密 ==========

    def encrypt_password(self, password: str) -> str:
        """RSA 公钥加密密码"""
        ts = int(time.time() * 1000)
        resp = self.get(f"{self._PUBLIC_KEY_PATH}?time={ts}")
        key = resp.json()
        n = int.from_bytes(base64.b64decode(key["modulus"]), 'big')
        e = int.from_bytes(base64.b64decode(key["exponent"]), 'big')
        pub = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
        ct = pub.encrypt(password.encode('utf-8'), padding.PKCS1v15())
        return base64.b64encode(ct).decode()

    # ========== 认证 ==========

    def login(self) -> None:
        """登录教务系统

        Raises:
            LoginError: 登录失败时抛出
        """
        if self._logged_in:
            return

        # 1. 获取 csrftoken
        resp = self.get(self._LOGIN_PATH)
        soup = BeautifulSoup(resp.text, 'html.parser')
        inp = soup.find('input', {'name': 'csrftoken'})
        self._csrftoken = inp.get('value', '') if inp else ''

        # 2. 加密并提交
        ts = int(time.time() * 1000)
        resp = self.post(
            f"{self._LOGIN_PATH}?time={ts}",
            data={
                "csrftoken": self._csrftoken,
                "language": "zh_CN",
                "yhm": self.username,
                "mm": self.encrypt_password(self._password),
                "ydType": "",
            },
        )

        if not self._check_login_success(resp):
            self._raise_login_error(resp)

        # 3. 初始化会话
        self._logged_in = True
        ts = int(time.time() * 1000)
        self.get(f"{self._INIT_MENU_PATH}?jsdm=xs&_t={ts}&echarts=1")

    def ensure_login(self) -> None:
        """确保已登录，否则抛出 NotLoggedInError"""
        if not self._logged_in:
            raise NotLoggedInError("请先调用 login() 登录")

    def logout(self) -> None:
        self.get("/jwglxt/xtgl/login_logoutAccount.html")
        self._logged_in = False

    @property
    def is_logged_in(self) -> bool:
        return self._logged_in

    @property
    def session(self) -> requests.Session:
        return self._session

    # ========== 内部 ==========

    @staticmethod
    def _check_login_success(resp: requests.Response) -> bool:
        url = resp.url.lower()
        return "login" not in url or "index" in url

    @staticmethod
    def _raise_login_error(resp: requests.Response) -> None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        for selector, label in [
            ('#tips', '页面提示'),
            ('#errorMsg', '错误信息'),
            ('.error', '错误信息'),
            ('.alert-danger', '错误信息'),
            ('.form-msg', '表单消息'),
        ]:
            el = soup.select_one(selector)
            if el and el.get_text(strip=True):
                raise LoginError(f"{label}: {el.get_text(strip=True)}")

        if "login_slogin" in resp.url.lower():
            title = soup.find('title')
            if title and ("错误" in (title.get_text(strip=True) or "") or "失败" in (title.get_text(strip=True) or "")):
                raise LoginError(title.get_text(strip=True))
            raise LoginError("用户名或密码错误，或账号已被锁定")

        raise LoginError(f"登录失败，响应URL: {resp.url}")

    def __repr__(self):
        return f"<JwxtBase username={self.username} logged_in={self._logged_in}>"
