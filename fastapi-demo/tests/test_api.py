"""
API Tests
API 接口测试
"""

import pytest
from httpx import AsyncClient


class TestHealthCheck:
    """健康检查测试"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """测试健康检查端点"""
        response = await client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAuth:
    """认证测试"""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """测试用户注册成功"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["email"] == user_data["email"]
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """测试重复邮箱注册"""
        user_data = {
            "username": "another",
            "email": test_user["user"]["email"],
            "password": "password123",
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """测试登录成功"""
        login_data = {
            "email": test_user["user"]["email"],
            "password": "testpassword123",
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: AsyncClient, test_user: dict):
        """测试错误密码登录"""
        login_data = {
            "email": test_user["user"]["email"],
            "password": "wrongpassword",
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient, test_user: dict):
        """测试获取当前用户"""
        response = await client.get(
            "/api/v1/auth/me",
            headers=test_user["headers"]
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["data"]["email"] == test_user["user"]["email"]
    
    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """测试未授权访问"""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestUsers:
    """用户管理测试"""
    
    @pytest.mark.asyncio
    async def test_get_user(self, client: AsyncClient, test_user: dict):
        """测试获取用户信息"""
        user_id = test_user["user"]["id"]
        response = await client.get(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == user_id
    
    @pytest.mark.asyncio
    async def test_update_user(self, client: AsyncClient, test_user: dict):
        """测试更新用户信息"""
        user_id = test_user["user"]["id"]
        update_data = {"username": "updateduser"}
        
        response = await client.put(
            f"/api/v1/users/{user_id}",
            json=update_data,
            headers=test_user["headers"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["username"] == "updateduser"
    
    @pytest.mark.asyncio
    async def test_change_password(self, client: AsyncClient, test_user: dict):
        """测试修改密码"""
        password_data = {
            "old_password": "testpassword123",
            "new_password": "newpassword456",
        }
        
        response = await client.post(
            "/api/v1/users/change-password",
            json=password_data,
            headers=test_user["headers"]
        )
        
        assert response.status_code == 200


class TestArticles:
    """文章管理测试"""
    
    @pytest.mark.asyncio
    async def test_create_article(self, client: AsyncClient, test_user: dict):
        """测试创建文章"""
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content.",
            "summary": "Test summary",
        }
        
        response = await client.post(
            "/api/v1/articles",
            json=article_data,
            headers=test_user["headers"]
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["title"] == article_data["title"]
    
    @pytest.mark.asyncio
    async def test_get_articles(self, client: AsyncClient):
        """测试获取文章列表"""
        response = await client.get("/api/v1/articles")
        
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data["data"]
        assert "total" in data["data"]
    
    @pytest.mark.asyncio
    async def test_create_article_unauthorized(self, client: AsyncClient):
        """测试未授权创建文章"""
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content.",
        }
        
        response = await client.post("/api/v1/articles", json=article_data)
        assert response.status_code == 401
