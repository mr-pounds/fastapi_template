"""
Name         : 用户
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 17:10:13
LastEditors  : zzz
LastEditTime : 2022-11-18 13:49:35
"""
from dependencies import check_token, create_token
from fastapi import APIRouter, Depends, status
from models.user import User
from pydantic import BaseModel
from response import BaseResponseModel, response
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError
from tortoise.expressions import Q
from utils.snowflake import SnowFlake

router = APIRouter(prefix="/users")

snowflake_worker = SnowFlake(1, 1, 1)


class SignUpBodyModel(BaseModel):
    username: str
    email: str
    password: str


@router.post("/account", tags=["users"], response_model=BaseResponseModel[None])
async def create_account(body: SignUpBodyModel):
    user_orm = await User.get_or_none(Q(email=body.email))
    if user_orm is not None:
        return response(None, "Email has been registered")
    await User.create(
        user_id=snowflake_worker.get_id(),
        username=body.username,
        email=body.email,
        password=body.password,
        image="https://pic1.zhimg.com/v2-1b8cfcf4da2f1a7af815640f2bc87c58_r.jpg",
    )
    return response(None, None)


class LoginBodyModel(BaseModel):
    email: str
    password: str


class LoginResponseModel(BaseModel):
    token: str
    userid: str
    avatarUrl: str


@router.post(
    "/login", tags=["users"], response_model=BaseResponseModel[LoginResponseModel]
)
async def login(body: LoginBodyModel):
    user_orm = await User.get_or_none(Q(email=body.email))
    if user_orm is None:
        return response(None, "Email isn't registered.", 500)

    if user_orm.password != body.password:
        return response(None, "Password is wrong", 500)

    # 构建token
    token, _ = create_token(user_orm.user_id)
    return response(
        {"token": token, "userid": user_orm.user_id, "avatarUrl": user_orm.image}
    )


UserSettingsModel = pydantic_model_creator(
    User,
    name="UserSettings",
    exclude=["create_time", "update_time", "password"],
    optional=["intro"],
)


@router.get(
    "/users/settings",
    tags=["users"],
    response_model=BaseResponseModel[UserSettingsModel],
)
async def get_settings(user_id: str = Depends(check_token)):
    return response(
        data=await UserSettingsModel.from_queryset_single(User.get(Q(user_id=user_id)))
    )


UpdateUserSettingsModel = pydantic_model_creator(
    User,
    name="UpdateUserSetting",
    exclude=["create_time", "update_time"],
    optional=["intro"],
)


@router.post("/user/settings", tags=["users"], response_model=BaseResponseModel)
async def update_settings(
    body: UpdateUserSettingsModel, user_id: str = Depends(check_token)
):
    user_orm = await User.get_or_none(Q(Q(email=body.email), Q(user_id__not=user_id)))
    if user_orm is None:
        try:
            await User.filter(user_id=user_id).update(
                image=body.image,
                username=body.username,
                intro=body.intro,
                email=body.email,
                password=body.password,
            )
        except ValidationError as e:
            return response(data=None, message=e, code=status.HTTP_406_NOT_ACCEPTABLE)
        return response(data=None)
    return response(
        data=None,
        message="Email Address has been registered",
        code=status.HTTP_406_NOT_ACCEPTABLE,
    )
