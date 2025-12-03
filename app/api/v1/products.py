"""
Product API Endpoints
产品相关的API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.dal.product_dal import ProductDAL
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductList,
    ProductStockUpdate
)
from app.schemas.common import ResponseModel

# 创建路由器
router = APIRouter()


@router.post(
    "/",
    response_model=ResponseModel[ProductResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建产品",
    description="创建一个新产品"
)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db)
):
    """创建产品"""
    product_dal = ProductDAL(db)
    
    # 检查产品名称是否已存在
    existing_product = product_dal.get_by_name(product_in.name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="产品名称已存在"
        )
    
    product_data = product_in.model_dump()
    product = product_dal.create(product_data)
    
    return ResponseModel(
        code=201,
        message="产品创建成功",
        data=ProductResponse.model_validate(product)
    )


@router.get(
    "/",
    response_model=ResponseModel[ProductList],
    summary="获取产品列表",
    description="获取产品列表（分页）"
)
def get_products(
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回的最大记录数"),
    category: Optional[str] = Query(default=None, description="按分类筛选"),
    in_stock_only: bool = Query(default=False, description="只显示有库存的产品"),
    db: Session = Depends(get_db)
):
    """获取产品列表"""
    product_dal = ProductDAL(db)
    
    if category:
        products = product_dal.get_by_category(category, skip=skip, limit=limit)
        total = product_dal.count(filters={"category": category})
    elif in_stock_only:
        products = product_dal.get_in_stock(skip=skip, limit=limit)
        total = len(products)  # 近似值
    else:
        products = product_dal.get_multi(skip=skip, limit=limit)
        total = product_dal.count()
    
    return ResponseModel(
        data=ProductList(
            total=total,
            items=[ProductResponse.model_validate(product) for product in products]
        )
    )


@router.get(
    "/{product_id}",
    response_model=ResponseModel[ProductResponse],
    summary="获取产品详情",
    description="根据ID获取产品详情"
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """获取产品详情"""
    product_dal = ProductDAL(db)
    product = product_dal.get_by_id(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"产品 ID {product_id} 不存在"
        )
    
    return ResponseModel(
        data=ProductResponse.model_validate(product)
    )


@router.put(
    "/{product_id}",
    response_model=ResponseModel[ProductResponse],
    summary="更新产品",
    description="更新产品信息"
)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新产品"""
    product_dal = ProductDAL(db)
    
    if not product_dal.exists(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"产品 ID {product_id} 不存在"
        )
    
    update_data = product_in.model_dump(exclude_unset=True)
    product = product_dal.update(product_id, update_data)
    
    return ResponseModel(
        message="产品更新成功",
        data=ProductResponse.model_validate(product)
    )


@router.delete(
    "/{product_id}",
    response_model=ResponseModel[None],
    summary="删除产品",
    description="删除指定产品"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """删除产品"""
    product_dal = ProductDAL(db)
    
    if not product_dal.exists(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"产品 ID {product_id} 不存在"
        )
    
    success = product_dal.delete(product_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除产品失败"
        )
    
    return ResponseModel(
        message="产品删除成功"
    )


@router.get(
    "/search/by-name",
    response_model=ResponseModel[ProductList],
    summary="搜索产品",
    description="根据名称搜索产品"
)
def search_products(
    search_term: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回的最大记录数"),
    db: Session = Depends(get_db)
):
    """搜索产品"""
    product_dal = ProductDAL(db)
    products = product_dal.search_by_name(search_term, skip=skip, limit=limit)
    
    return ResponseModel(
        data=ProductList(
            total=len(products),
            items=[ProductResponse.model_validate(product) for product in products]
        )
    )


@router.get(
    "/price-range/query",
    response_model=ResponseModel[ProductList],
    summary="价格区间查询",
    description="根据价格区间查询产品"
)
def get_products_by_price_range(
    min_price: float = Query(..., ge=0, description="最低价格"),
    max_price: float = Query(..., ge=0, description="最高价格"),
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),
    limit: int = Query(default=100, ge=1, le=100, description="返回的最大记录数"),
    db: Session = Depends(get_db)
):
    """价格区间查询"""
    if min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="最低价格不能大于最高价格"
        )
    
    product_dal = ProductDAL(db)
    products = product_dal.get_by_price_range(min_price, max_price, skip=skip, limit=limit)
    
    return ResponseModel(
        data=ProductList(
            total=len(products),
            items=[ProductResponse.model_validate(product) for product in products]
        )
    )


@router.patch(
    "/{product_id}/stock",
    response_model=ResponseModel[ProductResponse],
    summary="更新库存",
    description="更新产品库存（增加或减少）"
)
def update_product_stock(
    product_id: int,
    stock_update: ProductStockUpdate,
    db: Session = Depends(get_db)
):
    """
    更新库存
    
    演示：
    - PATCH方法用于部分更新
    - 业务逻辑封装在DAL层
    """
    product_dal = ProductDAL(db)
    
    if not product_dal.exists(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"产品 ID {product_id} 不存在"
        )
    
    product = product_dal.update_stock(product_id, stock_update.quantity)
    
    return ResponseModel(
        message="库存更新成功",
        data=ProductResponse.model_validate(product)
    )


@router.get(
    "/statistics/by-category",
    response_model=ResponseModel[List[dict]],
    summary="分类统计",
    description="按分类统计产品信息"
)
def get_statistics_by_category(
    db: Session = Depends(get_db)
):
    """
    分类统计
    
    演示：
    - 聚合查询
    - 统计分析
    """
    product_dal = ProductDAL(db)
    statistics = product_dal.get_statistics_by_category()
    
    return ResponseModel(
        data=statistics
    )
