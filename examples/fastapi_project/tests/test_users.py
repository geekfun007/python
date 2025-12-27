"""用户测试"""
import pytest


class TestCurrentUser:
    """当前用户测试"""
    
    def test_get_current_user(self, client, auth_headers):
        """测试获取当前用户"""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_unauthorized(self, client):
        """测试未认证访问"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    def test_update_current_user(self, client, auth_headers):
        """测试更新当前用户"""
        response = client.put(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"full_name": "Updated Name"}
        )
        assert response.status_code == 200
        assert response.json()["full_name"] == "Updated Name"


class TestUserAdmin:
    """用户管理测试（管理员）"""
    
    def test_list_users_as_admin(self, client, admin_headers, test_user):
        """测试管理员获取用户列表"""
        response = client.get("/api/v1/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # 至少有管理员和测试用户
    
    def test_list_users_as_normal_user(self, client, auth_headers):
        """测试普通用户获取用户列表（应该被拒绝）"""
        response = client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == 403
    
    def test_get_user_as_admin(self, client, admin_headers, test_user):
        """测试管理员获取指定用户"""
        response = client.get(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
    
    def test_get_nonexistent_user(self, client, admin_headers):
        """测试获取不存在的用户"""
        response = client.get("/api/v1/users/9999", headers=admin_headers)
        assert response.status_code == 404
    
    def test_update_user_as_admin(self, client, admin_headers, test_user):
        """测试管理员更新用户"""
        response = client.put(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers,
            json={"full_name": "Admin Updated"}
        )
        assert response.status_code == 200
        assert response.json()["full_name"] == "Admin Updated"
    
    def test_delete_user_as_admin(self, client, admin_headers, test_user):
        """测试管理员删除用户"""
        response = client.delete(
            f"/api/v1/users/{test_user.id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        assert "已删除" in response.json()["message"]
    
    def test_delete_self(self, client, admin_headers, admin_user):
        """测试删除自己（应该被拒绝）"""
        response = client.delete(
            f"/api/v1/users/{admin_user.id}",
            headers=admin_headers
        )
        assert response.status_code == 403
        assert "不能删除自己" in response.json()["detail"]
