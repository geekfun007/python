"""认证测试"""
import pytest


class TestRegister:
    """注册测试"""
    
    def test_register_success(self, client):
        """测试成功注册"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "NewPass123",
                "full_name": "New User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "password" not in data
        assert "hashed_password" not in data
    
    def test_register_duplicate_email(self, client, test_user):
        """测试重复邮箱"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",  # 已存在
                "username": "anotheruser",
                "password": "NewPass123"
            }
        )
        assert response.status_code == 400
        assert "已被注册" in response.json()["detail"]
    
    def test_register_duplicate_username(self, client, test_user):
        """测试重复用户名"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "another@example.com",
                "username": "testuser",  # 已存在
                "password": "NewPass123"
            }
        )
        assert response.status_code == 400
        assert "已被使用" in response.json()["detail"]
    
    def test_register_weak_password(self, client):
        """测试弱密码"""
        # 没有大写字母
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@example.com",
                "username": "weakuser",
                "password": "weakpass123"
            }
        )
        assert response.status_code == 422
    
    def test_register_invalid_email(self, client):
        """测试无效邮箱"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "invaliduser",
                "password": "ValidPass123"
            }
        )
        assert response.status_code == 422


class TestLogin:
    """登录测试"""
    
    def test_login_success(self, client, test_user):
        """测试成功登录"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """测试错误密码"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "WrongPass123"
            }
        )
        assert response.status_code == 401
        assert "用户名或密码错误" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """测试不存在的用户"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent",
                "password": "SomePass123"
            }
        )
        assert response.status_code == 401


class TestRefreshToken:
    """刷新令牌测试"""
    
    def test_refresh_token_success(self, client, test_user):
        """测试成功刷新令牌"""
        # 先登录
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "TestPass123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # 刷新令牌
        response = client.post(
            f"/api/v1/auth/refresh?refresh_token={refresh_token}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_invalid_token(self, client):
        """测试无效刷新令牌"""
        response = client.post(
            "/api/v1/auth/refresh?refresh_token=invalid_token"
        )
        assert response.status_code == 401
