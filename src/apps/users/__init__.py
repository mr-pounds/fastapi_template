from fastapi import APIRouter
from .acoount import router as account_router
from .follow import router as follow_router

# 这里处理整个模块的路由和初始化
router = APIRouter()
router.include_router(account_router)
router.include_router(follow_router)
