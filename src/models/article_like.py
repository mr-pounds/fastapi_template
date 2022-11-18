"""
Name         : article_comment
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-24 15:21:55
"""
from tortoise import fields, models


class ArticleLike(models.Model):
    """
    The ArticleLike model
    """

    id = fields.IntField(pk=True)
    article_id = fields.CharField(max_length=64)
    user_id = fields.CharField(max_length=64)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "article_like"
