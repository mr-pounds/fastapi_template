"""
Name         : 文章评论
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-25 09:17:31
LastEditors  : zzz
LastEditTime : 2022-10-25 09:57:06
"""
from fastapi import APIRouter, Depends, status, Query
from models.article_comment import ArticleComment
from response import response, BaseResponseModel
from dependencies import check_token
from pydantic import BaseModel
from utils.snowflake import SnowFlake
from tortoise.exceptions import ValidationError, DoesNotExist
from tortoise.expressions import Q

snow_flake_worker = SnowFlake(2, 2, 3)

router = APIRouter(prefix="/article", tags=["comments"])


class CommentModel(BaseModel):
    article_id: str
    comment: str
    comment_id: str = None
    user_id: str = None
    create_time: str = None
    image: str = None
    username: str = None


@router.post("/comment", response_model=BaseResponseModel)
async def add_comment(body: CommentModel, user_id: str = Depends(check_token)):
    try:
        await ArticleComment.create(
            comment_id=snow_flake_worker.get_id(),
            article=body.article_id,
            user=user_id,
            comment=body.comment,
        )
    except ValidationError as e:
        return response(None, str(e), status.HTTP_406_NOT_ACCEPTABLE)
    return response(None)


@router.delete(
    "/comment/{comment_id}",
    response_model=BaseResponseModel,
    dependencies=[Depends(check_token)],
)
async def delete_comment(comment_id: str):
    try:
        await ArticleComment.filter(Q(comment_id=comment_id)).update(is_delete=1)
    except DoesNotExist as e:
        return response(None, str(e), status.HTTP_404_NOT_FOUND)
    return response(None)


class CommentsListModel(BaseModel):
    comments: list[CommentModel]
    total: int


@router.get("/comment", response_model=BaseResponseModel[CommentsListModel])
async def get_comments(
    article_id: str = Query(default=None),
    limit: str = Query(default=10),
    offset: str = Query(default=1),
):
    querys = [Q(id_delete=0), Q(article_id=article_id)]
    commnet_orms = (
        await ArticleComment.filter(Q(*querys))
        .prefetch_related("user")
        .order_by("-create_time")
        .limit(limit)
        .offset(limit * (offset - 1))
    )
    return response(
        data={
            "comments": [
                {
                    "comment_id": comment.comment_id,
                    "comment": comment.comment,
                    "create_time": comment.create_time,
                    "username": comment.user.username,
                    "image": comment.user.image,
                }
                for comment in commnet_orms
            ],
            "total": await ArticleComment.filter(Q(*querys)).count(),
        }
    )
