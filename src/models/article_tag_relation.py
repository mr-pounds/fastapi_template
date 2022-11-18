"""
Name         : article_comment
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-24 11:13:22
"""
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ArticleTagRelation(models.Model):
    """
    The ArticleTagRelation model
    """

    id = fields.IntField(pk=True)
    article_id = fields.CharField(max_length=64)
    tag_id = fields.CharField(max_length=64)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "article_tag_relation"


ArticleTagRelation_Pydantic = pydantic_model_creator(
    ArticleTagRelation, name="ArticleTagRelation"
)
