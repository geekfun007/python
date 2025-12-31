"""
Pytest Configuration
测试配置和 fixtures
"""

import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


# 测试数据库 URL（使用 SQLite 内存数据库）
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建测试引擎
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

# 创建测试会话工厂
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    创建测试数据库会话
    
    每个测试函数使用独立的数据库会话
    测试结束后回滚所有更改
    """
    # 创建表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    # 清理表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    创建测试客户端
    
    使用测试数据库会话替换实际的数据库会话
    """
    # 覆盖数据库依赖
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    # 清理依赖覆盖
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(client: AsyncClient) -> dict:
    """
    创建测试用户
    
    Returns:
        包含用户信息和令牌的字典
    """
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    
    # 注册用户
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    # 登录获取令牌
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"],
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    login_response = response.json()
    
    return {
        "user": login_response["user"],
        "access_token": login_response["access_token"],
        "headers": {"Authorization": f"Bearer {login_response['access_token']}"},
    }


@pytest_asyncio.fixture
async def test_admin(client: AsyncClient, db_session: AsyncSession) -> dict:
    """
    创建测试管理员用户
    """
    from app.models.user import User, UserStatus, UserRole
    from app.core.security import get_password_hash
    
    # 直接在数据库中创建管理员
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("adminpassword123"),
        status=UserStatus.ACTIVE,
        role=UserRole.SUPER_ADMIN,
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    # 登录获取令牌
    login_data = {
        "email": "admin@example.com",
        "password": "adminpassword123",
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    login_response = response.json()
    
    return {
        "user": login_response["user"],
        "access_token": login_response["access_token"],
        "headers": {"Authorization": f"Bearer {login_response['access_token']}"},
    }
