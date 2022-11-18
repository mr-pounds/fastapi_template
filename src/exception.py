"""
Name         : 定义HTTP请求的异常
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-22 14:30:59
LastEditors  : zzz
LastEditTime : 2022-10-22 14:45:36
"""
from fastapi import HTTPException, status
from response import response


class TokenDoesNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response(data=None, message="未登录", code=status.HTTP_403_FORBIDDEN),
        )


class TokenHasExpired(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=response(
                data=None, message="登录信息已失效", code=status.HTTP_403_FORBIDDEN
            ),
        )
