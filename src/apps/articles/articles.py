"""
Name         : 文章
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-24 10:55:47
LastEditors  : zzz
LastEditTime : 2022-10-24 17:04:02
"""
from dependencies import check_token
from fastapi import APIRouter, Depends, Query, status
from models.article import Article
from models.article_like import ArticleLike
from models.article_tag import ArticleTag
from models.article_tag_relation import ArticleTagRelation
from models.article_comment import ArticleComment
from models.user import User
from pydantic import BaseModel
from response import BaseResponseModel, response
from tortoise.exceptions import ValidationError, DoesNotExist
from tortoise.expressions import Q
from utils.snowflake import SnowFlake

from .tags import add_tags, get_tags, update_tags

snow_flake_worker = SnowFlake(2, 2, 1)

router = APIRouter(prefix="/articles", tags=["articles"])


class ArticleModel(BaseModel):
    title: str
    summary: str
    content: str
    article_id: str = None
    tags: list[str] = None
    like_num: str = None
    publish_time: str = None
    username: str = None
    image: str = None


@router.post("/", response_model=BaseResponseModel)
async def add_article(body: ArticleModel, user_id: str = Depends(check_token)):
    # async def add_article(body: ArtcileModel, user_id: str = "1583639399055364096"):
    user_orm = await User.get_or_none(Q(user_id=user_id))
    try:
        article_orm = await Article.create(
            article_id=snow_flake_worker.get_id(),
            user=user_orm,
            title=body.title,
            summary=body.summary,
            content=body.content,
        )
    except ValidationError as e:
        return response(None, str(e), status.HTTP_406_NOT_ACCEPTABLE)

    err = await add_tags(article_orm.article_id, body.tags)
    if err is not None:
        return response(None, err, status.HTTP_406_NOT_ACCEPTABLE)
    return response(None)


@router.get("/{article_id}", response_model=BaseResponseModel[ArticleModel])
async def get_article(article_id: str):
    article_orm = await Article.get_or_none(Q(article_id=article_id)).prefetch_related(
        "user"
    )
    if article_orm is None:
        return response(None, "Article doesn't exist", status.HTTP_404_NOT_FOUND)
    return response(
        {
            "title": article_orm.title,
            "summary": article_orm.summary,
            "content": article_orm.content,
            "tags": await get_tags(article_id),
            "like_num": str(article_orm.like_num),
            "publish_time": article_orm.create_time.strftime("%B %d, %Y"),
            "username": article_orm.user.username,
            "image": article_orm.user.image,
        }
    )


@router.get("/like", response_model=BaseResponseModel)
async def like_article(
    article_id: str = Query(default=None), user_id: str = Depends(check_token)
):
    article_like_orm = await ArticleLike.get_or_none(
        Q(Q(article_id=article_id), Q(user_id=user_id))
    )
    if article_like_orm is None:
        await ArticleLike.create(article_id=article_id, user_id=user_id)
        article_orm = await Article.get(Q(article_id=article_id))
        article_orm.like_num += 1
        article_orm.save()
        return response(None)
    return response(None, "Already like this article", status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/unlike", response_model=BaseResponseModel)
async def unlike_article(
    article_id: str = Query(default=None), user_id: str = Depends(check_token)
):
    article_like_orm = await ArticleLike.get_or_none(
        Q(Q(article_id=article_id), Q(user_id=user_id))
    )
    if article_like_orm is None:
        return response(
            None, "Already like this article", status.HTTP_406_NOT_ACCEPTABLE
        )
    article_like_orm.delete()
    article_orm = await Article.get(Q(article_id=article_id))
    article_orm.like_num -= 1
    article_orm.save()
    return response(None)


@router.put("/", response_model=BaseResponseModel, dependencies=[Depends(check_token)])
async def update_article(body: ArticleModel):
    # async def add_article(body: ArtcileModel, user_id: str = "1583639399055364096"):
    article_orm = await Article.get_or_none(Q(article_id=body.article_id))
    if article_orm is None:
        return response(None, "The article doesn't exist", status.HTTP_404_NOT_FOUND)
    try:
        article_orm.update_from_dict(
            {
                "title": body.title,
                "summary": body.summary,
                "content": body.content,
            }
        )
    except ValidationError as e:
        return response(None, str(e), status.HTTP_406_NOT_ACCEPTABLE)
    # 更新标签
    err = await update_tags(article_orm.article_id, body.tags)
    if err is not None:
        return response(None, err, status.HTTP_406_NOT_ACCEPTABLE)
    return response(None)


@router.delete(
    "/{article_id}",
    response_model=BaseResponseModel,
    dependencies=[Depends(check_token)],
)
async def delete_article(article_id: str):
    # 删文章
    try:
        await Article.filter(Q(article_id=article_id)).delete()
    except DoesNotExist as e:
        return response(None, str(e), status.HTTP_404_NOT_FOUND)

    # 删除 tag 相关的数据
    need_update_tag_ids = [
        i.tag_id for i in await ArticleTagRelation.filter(Q(article_id=article_id))
    ]
    need_update_tag_orms = await ArticleTag.filter(Q(tag_id__in=need_update_tag_ids))
    for tag in need_update_tag_orms:
        tag.article_num -= 1
        await tag.save()
    await ArticleTagRelation.filter(Q(article_id=article_id)).delete()

    # 删除 comment 相关的数据
    await ArticleComment.filter(Q(article=article_id)).update(is_delete=1)

    return response(None)
