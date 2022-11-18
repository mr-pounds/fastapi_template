"""
Name         : 文章列表相关的接口
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-24 14:25:49
LastEditors  : zzz
LastEditTime : 2022-10-25 09:16:11
"""
from fastapi import APIRouter, Depends, Query
from dependencies import check_token
from models.article import Article
from models.follow_relation import UserFollowRelation
from pydantic import BaseModel
from tortoise.expressions import Q

from .tags import get_tags
from response import response, BaseResponseModel

router = APIRouter(tags=["feeds"])


class ArticleModel(BaseModel):
    title: str
    summary: str
    tags: list[str] = None
    like_num: str = None
    publish_time: str = None
    username: str = None
    image: str = None


class ArticlesListModel(BaseModel):
    articles: list[ArticleModel]
    total: int


async def get_articles_list(
    querys: list[Q], limit: int = 10, offset: int = 1, order_by: str = "-create_time"
) -> list[ArticleModel]:
    article_orms = (
        await Article.filter(Q(*querys))
        .prefetch_related("user")
        .order_by(order_by)
        .limit(limit)
        .offset(limit * (offset - 1))
    )
    return {
        "articles": [
            {
                "title": article.title,
                "summary": article.summary,
                "tags": await get_tags(article_id=article.article_id),
                "like_num": article.like_num,
                "publish_time": article.create_time.strftime("%B %d, %Y"),
                "username": article.user.username,
                "image": article.user.image,
            }
            for article in article_orms
        ],
        "total": await Article.filter(Q(*querys)).count(),
    }


@router.get("/myArticles", response_model=BaseResponseModel[ArticlesListModel])
async def my_articles(
    limit: int = Query(default=10),
    offset: int = Query(default=1),
    user_id: str = Depends(check_token),
):
    return response(
        data=await get_articles_list(
            querys=[Q(user=user_id), Q(is_delete=0)], limit=limit, offset=offset
        )
    )


@router.get("/globalFeeds", response_model=BaseResponseModel[ArticlesListModel])
async def global_feeds(
    limit: int = Query(default=10),
    offset: int = Query(default=1),
):
    return response(
        data=await get_articles_list(
            querys=[Q(is_delete=0)], limit=limit, offset=offset
        )
    )


@router.get("/yourFeeds", response_model=BaseResponseModel[ArticlesListModel])
async def your_feeds(
    user_id: str = Depends(check_token),
    limit: int = Query(default=10),
    offset: int = Query(default=1),
):
    # 先找出关注的user清单
    follow_user_list = [
        i.followed_user_id
        for i in await UserFollowRelation.filter(Q(follower_user_id=user_id))
    ]
    return response(
        data=await get_articles_list(
            querys=[Q(is_delete=0), Q(user_id__in=follow_user_list)],
            limit=limit,
            offset=offset,
        ),
    )


@router.get("/favoritedFeeds", response_model=BaseResponseModel[ArticlesListModel])
async def favorited_feeds(
    user_id: str = Depends(check_token),
    limit: int = Query(default=10),
    offset: int = Query(default=1),
):
    return response(
        data=await get_articles_list(
            querys=[Q(is_delete=0), Q(user_id=user_id)],
            limit=limit,
            offset=offset,
            order_by="-like_num",
        ),
    )
