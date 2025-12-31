"""
Categories Router
分类相关 API 路由
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.article import CategoryCreate, CategoryResponse
from app.schemas.common import ResponseModel
from app.services.article_service import ArticleService
from app.services.auth_service import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get(
    "",
    response_model=ResponseModel[List[CategoryResponse]],
    summary="获取分类列表",
    description="获取所有文章分类"
)
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有分类
    
    - 返回树形结构（包含子分类）
    """
    article_service = ArticleService(db)
    result = await article_service.get_categories()
    return ResponseModel.success(data=result)


@router.post(
    "",
    response_model=ResponseModel[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建分类",
    description="创建新分类（需要管理员权限）"
)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建新分类
    
    - 需要管理员权限
    - **name**: 分类名称（唯一）
    - **description**: 分类描述（可选）
    - **parent_id**: 父分类ID（可选）
    - **sort_order**: 排序权重（默认0）
    """
    article_service = ArticleService(db)
    result = await article_service.create_category(category_data)
    return ResponseModel.success(data=result, message="分类创建成功")
