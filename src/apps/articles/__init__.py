from fastapi import APIRouter
from .articles import router as article_router
from .feeds import router as feed_router
from .tags import router as tag_router
from .comments import router as comment_router

router = APIRouter()
router.include_router(article_router)
router.include_router(feed_router)
router.include_router(tag_router)
router.include_router(comment_router)
