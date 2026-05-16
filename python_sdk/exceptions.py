"""教务系统 SDK 异常"""


class JwxtError(Exception):
    """SDK 基础异常"""
    pass


class LoginError(JwxtError):
    """登录失败"""
    pass


class NotLoggedInError(JwxtError):
    """未登录时调用需认证的接口"""
    pass


class RequestError(JwxtError):
    """请求异常"""
    pass
