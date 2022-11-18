"""
Name         : 用户之间的关注
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-24 10:03:42
LastEditors  : zzz
LastEditTime : 2022-10-24 11:06:23
"""
from dependencies import check_token
from fastapi import APIRouter, Depends, status
from models.follow_relation import UserFollowRelation
from pydantic import BaseModel
from response import BaseResponseModel, response
from tortoise.exceptions import ValidationError

from tortoise.expressions import Q

router = APIRouter()


class FollowModel(BaseModel):
    user_id: str


async def get_follow_list(user_id: str):
    return await UserFollowRelation.filter(Q(follower_user_id=user_id)).values_list(
        "followed_user_id"
    )


@router.post("/follow", tags=["follow"], response_model=BaseResponseModel)
async def add_follow(body: FollowModel, user_id: str = Depends(check_token)):
    # async def add_follow(body: FollowModel, user_id: str = "1583639399055364096"):
    follow_orm = await UserFollowRelation.get_or_none(
        Q(Q(followed_user_id=body.user_id), Q(follower_user_id=user_id))
    )
    if follow_orm is not None:
        return response(None, "已经关注", status.HTTP_208_ALREADY_REPORTED)
    try:
        await UserFollowRelation.create(
            followed_user_id=body.user_id, follower_user_id=user_id
        )
    except ValidationError as e:
        return response(None, str(e), status.HTTP_406_NOT_ACCEPTABLE)
    return response(None)


@router.delete("/follow", tags=["follow"], response_model=BaseResponseModel)
async def delete_follow(body: FollowModel, user_id: str = Depends(check_token)):
    # async def delete_follow(body: FollowModel, user_id: str = "1583639399055364096"):
    try:
        await UserFollowRelation.filter(
            Q(Q(followed_user_id=body.user_id), Q(follower_user_id=user_id))
        ).delete()
    except ValidationError as e:
        return response(None, e.__str__(), status.HTTP_406_NOT_ACCEPTABLE)
    return response(None)
