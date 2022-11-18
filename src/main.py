"""
Name         : 主入口函数
Version      : 1.0.1
Author       : zzz
Date         : 2022-10-21 10:46:18
LastEditors  : zzz
LastEditTime : 2022-11-18 14:51:48
"""
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from apps.users import router as users_router
from apps.articles import router as article_router
from constant import SQLITE3_FILE

app = FastAPI()

app.include_router(users_router)
app.include_router(article_router)

register_tortoise(
    app,
    db_url=f"sqlite://{SQLITE3_FILE}",
    modules={
        "models": [
            "models.article_comment",
            "models.article_like",
            "models.article_tag_relation",
            "models.article_tag",
            "models.article",
            "models.follow_relation",
            "models.user",
        ]
    },
    add_exception_handlers=True,
)
