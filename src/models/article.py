"""
Name         : Article
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-24 15:18:59
"""
from .user import User
from tortoise import fields, models


class Article(models.Model):
    """
    The Article model
    """

    id = fields.IntField(pk=True)
    article_id = fields.CharField(max_length=64, unique=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="article", to_field="user_id"
    )
    title = fields.CharField(max_length=128)
    summary = fields.CharField(max_length=128)
    content = fields.TextField()
    like_num = fields.IntField(default=0)
    is_delete = fields.IntField(default=0)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    def author(self):
        return self.user_id.username

    def author_image(self):
        return self.user_id.image

    class Meta:
        table = "article"

    class PydanticMeta:
        computed = ["author", "author_image"]
