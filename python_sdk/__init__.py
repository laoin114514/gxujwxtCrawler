"""广西大学教务管理系统 Python SDK"""
from .jwxt_client import JwxtClient
from .exceptions import LoginError, NotLoggedInError, RequestError, JwxtError
from .models.common import PageQuery, Semester
