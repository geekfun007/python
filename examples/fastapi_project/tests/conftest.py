"""测试配置和 fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.crud.user import user_crud
from app.schemas.user import UserCreate


# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 覆盖依赖
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """每个测试前创建表，测试后清理"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


@pytest.fixture
def db():
    """测试数据库会话"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db):
    """创建测试用户"""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="TestPass123",
        full_name="Test User"
    )
    return user_crud.create(db, obj_in=user_data)


@pytest.fixture
def auth_headers(client, test_user):
    """获取认证头"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "TestPass123"
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
def admin_user(db):
    """创建管理员用户"""
    user_data = UserCreate(
        email="admin@example.com",
        username="adminuser",
        password="AdminPass123",
        full_name="Admin User"
    )
    user = user_crud.create(db, obj_in=user_data)
    # 设置为超级管理员
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_headers(client, admin_user):
    """获取管理员认证头"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "adminuser",
            "password": "AdminPass123"
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
