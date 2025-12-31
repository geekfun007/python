"""
健康检查 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.base import BaseResponse

router = APIRouter()


@router.get(
    "",
    response_model=BaseResponse[dict],
    summary="健康检查",
    description="检查服务是否正常运行",
)
async def health_check():
    """健康检查接口"""
    return BaseResponse.success(
        data={"status": "healthy", "service": "fastapi-demo"},
        message="服务运行正常",
    )


@router.get(
    "/db",
    response_model=BaseResponse[dict],
    summary="数据库健康检查",
    description="检查数据库连接是否正常",
)
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """数据库健康检查接口"""
    try:
        await db.execute(text("SELECT 1"))
        return BaseResponse.success(
            data={"status": "healthy", "database": "connected"},
            message="数据库连接正常",
        )
    except Exception as e:
        return BaseResponse.error(
            message=f"数据库连接失败: {str(e)}",
            code=503,
        )
