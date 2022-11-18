"""
Name         : article_comment
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-22 14:11:28
"""
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ArticleTag(models.Model):
    """
    The Tag model
    """

    id = fields.IntField(pk=True)
    tag_id = fields.CharField(max_length=64, unique=True)
    tag = fields.CharField(max_length=32)
    article_num = fields.IntField(default=0)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "article_tag"

    class PydanticMeta:
        computed = []


ArticleTag_Pydantic = pydantic_model_creator(ArticleTag, name="ArticleTag")
