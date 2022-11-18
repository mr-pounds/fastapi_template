"""
Name         : 文章标签管理
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-24 11:13:44
LastEditors  : zzz
LastEditTime : 2022-10-24 17:35:47
"""
from models.article_tag_relation import ArticleTagRelation
from tortoise.exceptions import ValidationError
from tortoise.expressions import Q
from utils.snowflake import SnowFlake
from fastapi import APIRouter, Query
from pydantic import BaseModel
from models.article_tag import ArticleTag
from response import response, BaseResponseModel

router = APIRouter(tags=["tags"])

snow_flake_worker = SnowFlake(2, 2, 2)


async def add_tags(article_id: str, tags: list[str]) -> str or None:
    """根据 tags 列表生成标签数据

    Args:
        article_id (str)
        tags (list[str])

    Returns:
        str or None: return error message when fail
    """
    tags = set(tags)
    for tag in tags:
        tag_orm = await ArticleTag.get_or_none(Q(tag=tag))
        if tag_orm is None:
            tag_id = snow_flake_worker.get_id()
            try:
                await ArticleTag.create(tag_id=tag_id, tag=tag, article_num=1)
            except ValidationError as e:
                return str(e)
            await ArticleTagRelation.create(article_id=article_id, tag_id=tag_id)
        else:
            await ArticleTagRelation.create(
                article_id=article_id, tag_id=tag_orm.tag_id
            )
            tag_orm.article_num += 1
            await tag_orm.save()

        return None


async def get_tags(article_id: str) -> list[str]:
    # 先获取相关的tag_id
    tag_ids_list = await ArticleTagRelation.filter(
        Q(article_id=article_id)
    ).values_list("tag_id")
    tag_ids_list = [i[0] for i in tag_ids_list]
    if not tag_ids_list:
        return []
    tags_list = await ArticleTag.filter(Q(tag_id__in=tag_ids_list)).values_list("tag")
    return [i[0] for i in tags_list]


async def update_tags(article_id: str, tags: list[str]) -> str:
    tags = set(tags)
    # 找到这篇文章所有的tag 跟tags对比，删除掉不需要的
    created_tag_ids_list = await ArticleTagRelation.filter(
        Q(article_id=article_id)
    ).values_list("tag_id")
    created_tag_ids_list = [i[0] for i in created_tag_ids_list]

    need_update_tag_orm = await ArticleTag.filter(
        Q(Q(tag_id__in=created_tag_ids_list), Q(tag__not_in=tags))
    )
    need_delete_tag_ids_list = [i.tag_id for i in need_update_tag_orm]
    await ArticleTagRelation.filter(Q(tag_id__in=need_delete_tag_ids_list)).delete()
    for tag_orm in need_update_tag_orm:
        tag_orm.article_num -= 1
        await tag_orm.save()

    # 根据新的tag列表进行创建
    for tag in tags:
        tag_orm = await ArticleTag.get_or_none(Q(tag=tag))
        if tag_orm is None:
            tag_id = snow_flake_worker.get_id()
            try:
                await ArticleTag.create(tag_id=tag_id, tag=tag, article_num=1)
            except ValidationError as e:
                return str(e)
            await ArticleTagRelation.create(article_id=article_id, tag_id=tag_id)
        else:
            await ArticleTagRelation.create(
                article_id=article_id, tag_id=tag_orm.tag_id
            )
            tag_orm.article_num += 1
            await tag_orm.save()
        return None


class TagsListModel(BaseModel):
    tags: list[str] = None


@router.get("/popularTags", response_model=BaseResponseModel[TagsListModel])
async def get_popular_tags(limit: int = Query(default=10)):
    popular_tags = (
        await ArticleTag.all()
        .order_by("-article_num")
        .limit(limit=limit)
        .values_list("tag")
    )
    return response(data={"tags": [i[0] for i in popular_tags]})
