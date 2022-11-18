"""
Name         : Users
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-24 10:01:13
"""
from tortoise import fields, models


class User(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=64, unique=True)
    username = fields.CharField(max_length=64)
    email = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=128)
    image = fields.CharField(max_length=256, null=True)
    intro = fields.TextField()
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user"

    class PydanticMeta:
        exclude = ["id"]
