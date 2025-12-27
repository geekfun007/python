"""安全相关功能：密码哈希、JWT Token"""
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
import bcrypt

from ..config import settings
from ..schemas.token import TokenData


def get_password_hash(password: str) -> str:
    """对密码进行哈希处理
    
    Args:
        password: 明文密码
        
    Returns:
        哈希后的密码
    """
    # 确保密码是 bytes 类型
    password_bytes = password.encode('utf-8')
    # 生成 salt 并哈希
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
        
    Returns:
        密码是否匹配
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        JWT token 字符串
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建刷新令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        JWT token 字符串
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expire_days
        )
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """解码 JWT Token
    
    Args:
        token: JWT token 字符串
        
    Returns:
        解码后的 TokenData，如果无效则返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        sub = payload.get("sub")
        username: str = payload.get("username")
        scopes: list = payload.get("scopes", [])
        
        if sub is None:
            return None
        
        # sub 是字符串，需要转换为 int
        user_id = int(sub)
        
        return TokenData(
            user_id=user_id,
            username=username,
            scopes=scopes
        )
    except (JWTError, ValueError):
        return None
