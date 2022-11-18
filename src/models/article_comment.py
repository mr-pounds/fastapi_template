"""
Name         : article_comment
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-25 09:25:18
"""
from .article import Article
from .user import User
from tortoise import fields, models


class ArticleComment(models.Model):
    """
    The ArticleComment model
    """

    id = fields.IntField(pk=True)
    comment_id = fields.CharField(max_length=64, unique=True)
    article: fields.ForeignKeyRelation[Article] = fields.ForeignKeyField(
        "models.Article", related_name="comment_article", to_field="article_id"
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="comment_user", to_field="user_id"
    )
    comment = fields.CharField(max_length=256)
    is_delete = fields.BooleanField(default=False)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    def author(self):
        return self.user.username

    def author_image(self):
        return self.user.image

    class Meta:
        table = "article_comment"

    class PydanticMeta:
        computed = ["author", "author_image"]
