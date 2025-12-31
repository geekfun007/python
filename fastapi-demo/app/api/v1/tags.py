"""
Tags Router
标签相关 API 路由
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.article import TagCreate, TagResponse
from app.schemas.common import ResponseModel
from app.services.article_service import ArticleService
from app.services.auth_service import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get(
    "",
    response_model=ResponseModel[List[TagResponse]],
    summary="获取标签列表",
    description="获取所有标签（按使用次数排序）"
)
async def get_tags(
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有标签
    
    - 按使用次数降序排列
    """
    article_service = ArticleService(db)
    result = await article_service.get_tags()
    return ResponseModel.success(data=result)


@router.post(
    "",
    response_model=ResponseModel[TagResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建标签",
    description="创建新标签（需要管理员权限）"
)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建新标签
    
    - 需要管理员权限
    - **name**: 标签名称（唯一）
    - **color**: 标签颜色（可选，如 #FF5733）
    """
    article_service = ArticleService(db)
    result = await article_service.create_tag(tag_data)
    return ResponseModel.success(data=result, message="标签创建成功")
