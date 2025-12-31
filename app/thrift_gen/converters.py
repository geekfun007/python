"""
Thrift 类型与 Pydantic/ORM 模型转换器
Converters between Thrift types and Pydantic/ORM models
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCategory as PydanticItemCategory
from app.schemas.item import ItemResponse, ItemStatus as PydanticItemStatus
from app.schemas.user import Token, UserResponse
from app.thrift_gen import (
    BaseResponse,
    ErrorCode,
    ItemCategory,
    ItemInfo,
    ItemStatus,
    PaginationInfo,
    PriceInfo,
    StockInfo,
    TokenInfo,
    UserInfo,
    UserRole,
    UserStatus,
)


def datetime_to_timestamp(dt: Optional[datetime]) -> int:
    """将 datetime 转换为毫秒时间戳"""
    if dt is None:
        return 0
    return int(dt.timestamp() * 1000)


def timestamp_to_datetime(ts: int) -> Optional[datetime]:
    """将毫秒时间戳转换为 datetime"""
    if ts == 0:
        return None
    return datetime.fromtimestamp(ts / 1000)


# ============================================
# 响应构建器
# ============================================

def build_base_response(
    code: int = 0,
    message: str = "success",
    request_id: Optional[str] = None,
) -> BaseResponse:
    """构建基础响应"""
    return BaseResponse(
        code=code,
        message=message,
        request_id=request_id,
    )


def build_success_response(
    message: str = "操作成功",
    request_id: Optional[str] = None,
) -> BaseResponse:
    """构建成功响应"""
    return build_base_response(
        code=ErrorCode.SUCCESS,
        message=message,
        request_id=request_id,
    )


def build_error_response(
    code: int,
    message: str,
    request_id: Optional[str] = None,
) -> BaseResponse:
    """构建错误响应"""
    return build_base_response(
        code=code,
        message=message,
        request_id=request_id,
    )


def build_pagination_info(
    page: int,
    page_size: int,
    total: int,
) -> PaginationInfo:
    """构建分页信息"""
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return PaginationInfo(
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    )


# ============================================
# User 转换器
# ============================================

class UserConverter:
    """用户类型转换器"""
    
    @staticmethod
    def orm_to_thrift(user: User) -> UserInfo:
        """ORM User -> Thrift UserInfo"""
        return UserInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            status=UserStatus.ACTIVE if user.is_active else UserStatus.INACTIVE,
            role=UserRole.SUPERADMIN if user.is_superuser else UserRole.USER,
            created_at=datetime_to_timestamp(user.created_at),
            updated_at=datetime_to_timestamp(user.updated_at),
        )
    
    @staticmethod
    def pydantic_to_thrift(user: UserResponse) -> UserInfo:
        """Pydantic UserResponse -> Thrift UserInfo"""
        return UserInfo(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            status=UserStatus.ACTIVE if user.is_active else UserStatus.INACTIVE,
            role=UserRole.SUPERADMIN if user.is_superuser else UserRole.USER,
            created_at=datetime_to_timestamp(user.created_at),
            updated_at=datetime_to_timestamp(user.updated_at),
        )
    
    @staticmethod
    def thrift_to_dict(user_info: UserInfo) -> Dict[str, Any]:
        """Thrift UserInfo -> Dict"""
        return {
            "id": user_info.id,
            "email": user_info.email,
            "username": user_info.username,
            "full_name": user_info.full_name,
            "is_active": user_info.status == UserStatus.ACTIVE,
            "is_superuser": user_info.role in (UserRole.ADMIN, UserRole.SUPERADMIN),
            "created_at": timestamp_to_datetime(user_info.created_at),
            "updated_at": timestamp_to_datetime(user_info.updated_at),
        }


class TokenConverter:
    """令牌类型转换器"""
    
    @staticmethod
    def pydantic_to_thrift(token: Token) -> TokenInfo:
        """Pydantic Token -> Thrift TokenInfo"""
        return TokenInfo(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            token_type=token.token_type,
            expires_in=token.expires_in,
        )
    
    @staticmethod
    def thrift_to_dict(token_info: TokenInfo) -> Dict[str, Any]:
        """Thrift TokenInfo -> Dict"""
        return {
            "access_token": token_info.access_token,
            "refresh_token": token_info.refresh_token,
            "token_type": token_info.token_type,
            "expires_in": token_info.expires_in,
        }


# ============================================
# Item 转换器
# ============================================

# 状态映射
ITEM_STATUS_MAP = {
    PydanticItemStatus.DRAFT: ItemStatus.DRAFT,
    PydanticItemStatus.ACTIVE: ItemStatus.ACTIVE,
    PydanticItemStatus.INACTIVE: ItemStatus.INACTIVE,
    PydanticItemStatus.DELETED: ItemStatus.DELETED,
}

ITEM_STATUS_REVERSE_MAP = {v: k for k, v in ITEM_STATUS_MAP.items()}

# 分类映射
ITEM_CATEGORY_MAP = {
    PydanticItemCategory.ELECTRONICS: ItemCategory.ELECTRONICS,
    PydanticItemCategory.CLOTHING: ItemCategory.CLOTHING,
    PydanticItemCategory.FOOD: ItemCategory.FOOD,
    PydanticItemCategory.BOOKS: ItemCategory.BOOKS,
    PydanticItemCategory.OTHER: ItemCategory.OTHER,
}

ITEM_CATEGORY_REVERSE_MAP = {v: k for k, v in ITEM_CATEGORY_MAP.items()}


class ItemConverter:
    """物品类型转换器"""
    
    @staticmethod
    def orm_to_thrift(item: Item) -> ItemInfo:
        """ORM Item -> Thrift ItemInfo"""
        # 获取状态
        try:
            status = ITEM_STATUS_MAP.get(
                PydanticItemStatus(item.status),
                ItemStatus.DRAFT,
            )
        except ValueError:
            status = ItemStatus.DRAFT
        
        # 获取分类
        try:
            category = ITEM_CATEGORY_MAP.get(
                PydanticItemCategory(item.category),
                ItemCategory.OTHER,
            )
        except ValueError:
            category = ItemCategory.OTHER
        
        return ItemInfo(
            id=item.id,
            title=item.title,
            description=item.description,
            price_info=PriceInfo(
                price=float(item.price),
                original_price=None,
                discount=None,
                currency="CNY",
            ),
            category=category,
            status=status,
            stock_info=StockInfo(
                stock=item.stock,
                sold_count=0,
                reserved_count=0,
            ),
            owner_id=item.owner_id,
            owner_name=item.owner.username if item.owner else None,
            images=None,
            tags=None,
            created_at=datetime_to_timestamp(item.created_at),
            updated_at=datetime_to_timestamp(item.updated_at),
        )
    
    @staticmethod
    def pydantic_to_thrift(item: ItemResponse) -> ItemInfo:
        """Pydantic ItemResponse -> Thrift ItemInfo"""
        # 获取状态
        status = ITEM_STATUS_MAP.get(item.status, ItemStatus.DRAFT)
        
        # 获取分类
        category = ITEM_CATEGORY_MAP.get(item.category, ItemCategory.OTHER)
        
        return ItemInfo(
            id=item.id,
            title=item.title,
            description=item.description,
            price_info=PriceInfo(
                price=float(item.price),
                original_price=None,
                discount=None,
                currency="CNY",
            ),
            category=category,
            status=status,
            stock_info=StockInfo(
                stock=item.stock,
                sold_count=0,
                reserved_count=0,
            ),
            owner_id=item.owner_id,
            owner_name=None,
            images=None,
            tags=None,
            created_at=datetime_to_timestamp(item.created_at),
            updated_at=datetime_to_timestamp(item.updated_at),
        )
    
    @staticmethod
    def thrift_to_dict(item_info: ItemInfo) -> Dict[str, Any]:
        """Thrift ItemInfo -> Dict"""
        # 获取状态
        status = ITEM_STATUS_REVERSE_MAP.get(
            item_info.status,
            PydanticItemStatus.DRAFT,
        )
        
        # 获取分类
        category = ITEM_CATEGORY_REVERSE_MAP.get(
            item_info.category,
            PydanticItemCategory.OTHER,
        )
        
        return {
            "id": item_info.id,
            "title": item_info.title,
            "description": item_info.description,
            "price": Decimal(str(item_info.price_info.price)),
            "category": category,
            "status": status,
            "stock": item_info.stock_info.stock,
            "owner_id": item_info.owner_id,
            "created_at": timestamp_to_datetime(item_info.created_at),
            "updated_at": timestamp_to_datetime(item_info.updated_at),
        }
    
    @staticmethod
    def list_orm_to_thrift(items: List[Item]) -> List[ItemInfo]:
        """ORM Item 列表 -> Thrift ItemInfo 列表"""
        return [ItemConverter.orm_to_thrift(item) for item in items]
    
    @staticmethod
    def list_pydantic_to_thrift(items: List[ItemResponse]) -> List[ItemInfo]:
        """Pydantic ItemResponse 列表 -> Thrift ItemInfo 列表"""
        return [ItemConverter.pydantic_to_thrift(item) for item in items]
