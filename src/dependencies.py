"""
Name         : 项目通过的依赖项
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-22 14:18:04
LastEditors  : zzz
LastEditTime : 2022-10-22 14:53:46
"""
from datetime import datetime, timedelta
import hashlib
from typing import Union
from fastapi import Cookie
from exception import TokenDoesNotExist, TokenHasExpired

token_list = {}


def create_token(user_id: str):
    """create token when user sign in.

    Args:
        user_id (str): user_id

    Returns:
        token(str): token string
        expire(str): token expired time. format: %Y-%m-%d %H:%M:%S
    """
    token = hashlib.md5(user_id.encode("utf-8")).hexdigest()
    expire = (datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
    token_list[token] = {"user_id": user_id, "expire": expire}
    return token, expire


def check_token(token: Union[str, None] = Cookie(default=None)) -> str:
    """check the status and infomation of login.

    Args:
        token (str): Defaults to Cookie(default=None).

    Raises:
        TokenHasExpired
        TokenDoesNotExist

    Returns:
        user_id(str)
    """
    if token in token_list:
        if datetime.now() > datetime.strptime(
            token_list[token]["expire"], "%Y-%m-%d %H:%M:%S"
        ):
            raise TokenHasExpired()
        return token_list[token]["user_id"]
    raise TokenDoesNotExist()
