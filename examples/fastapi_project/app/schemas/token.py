"""Token 相关的 Pydantic 模式"""
from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    """Token 响应模式"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据模式（解码后的 payload）"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    scopes: List[str] = []
