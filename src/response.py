"""
Name         : 定义基本的响应模型
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-22 09:30:44
LastEditors  : zzz
LastEditTime : 2022-10-24 11:26:39
"""
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class BaseResponseModel(GenericModel, Generic[DataType]):
    code: int
    success: bool
    message: str or None = None
    data: Optional[DataType] = None


def response(data: DataType, message=None, code=100) -> BaseResponseModel[DataType]:
    return {
        "code": code,
        "success": code == 100,
        "message": message,
        "data": data,
    }
