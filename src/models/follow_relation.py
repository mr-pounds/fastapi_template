"""
Name         : follow_relation
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 13:10:28
LastEditors  : zzz
LastEditTime : 2022-10-25 09:05:49
"""
from tortoise import fields, models


class UserFollowRelation(models.Model):
    """
    The UserFollowRelation model
    """

    id = fields.IntField(pk=True)
    followed_user_id = fields.CharField(max_length=64)
    follower_user_id = fields.CharField(max_length=64)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "follow_relation"
