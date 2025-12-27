"""商品测试"""
import pytest


class TestItemPublic:
    """商品公开接口测试"""
    
    def test_list_items_empty(self, client):
        """测试空商品列表"""
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_nonexistent_item(self, client):
        """测试获取不存在的商品"""
        response = client.get("/api/v1/items/9999")
        assert response.status_code == 404


class TestItemCRUD:
    """商品 CRUD 测试"""
    
    def test_create_item(self, client, auth_headers):
        """测试创建商品"""
        response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={
                "name": "Test Item",
                "description": "A test item",
                "price": 99.99,
                "stock": 10
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["price"] == 99.99
        assert data["stock"] == 10
    
    def test_create_item_unauthorized(self, client):
        """测试未认证创建商品"""
        response = client.post(
            "/api/v1/items",
            json={
                "name": "Test Item",
                "price": 99.99
            }
        )
        assert response.status_code == 401
    
    def test_create_item_invalid_price(self, client, auth_headers):
        """测试无效价格"""
        response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={
                "name": "Test Item",
                "price": -10  # 负价格
            }
        )
        assert response.status_code == 422
    
    def test_get_item(self, client, auth_headers):
        """测试获取商品"""
        # 先创建
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99}
        )
        item_id = create_response.json()["id"]
        
        # 再获取
        response = client.get(f"/api/v1/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Item"
    
    def test_update_item(self, client, auth_headers):
        """测试更新商品"""
        # 先创建
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99}
        )
        item_id = create_response.json()["id"]
        
        # 再更新
        response = client.put(
            f"/api/v1/items/{item_id}",
            headers=auth_headers,
            json={"name": "Updated Item", "price": 149.99}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Item"
        assert response.json()["price"] == 149.99
    
    def test_delete_item(self, client, auth_headers):
        """测试删除商品"""
        # 先创建
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99}
        )
        item_id = create_response.json()["id"]
        
        # 再删除
        response = client.delete(
            f"/api/v1/items/{item_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # 验证已删除
        get_response = client.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_list_my_items(self, client, auth_headers):
        """测试获取我的商品"""
        # 创建商品
        client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "My Item 1", "price": 10}
        )
        client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "My Item 2", "price": 20}
        )
        
        # 获取我的商品
        response = client.get("/api/v1/items/my", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestItemStock:
    """库存测试"""
    
    def test_update_stock_increase(self, client, auth_headers):
        """测试增加库存"""
        # 创建商品
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99, "stock": 10}
        )
        item_id = create_response.json()["id"]
        
        # 增加库存
        response = client.post(
            f"/api/v1/items/{item_id}/stock",
            headers=auth_headers,
            params={"quantity": 5}
        )
        assert response.status_code == 200
        assert response.json()["stock"] == 15
    
    def test_update_stock_decrease(self, client, auth_headers):
        """测试减少库存"""
        # 创建商品
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99, "stock": 10}
        )
        item_id = create_response.json()["id"]
        
        # 减少库存
        response = client.post(
            f"/api/v1/items/{item_id}/stock",
            headers=auth_headers,
            params={"quantity": -3}
        )
        assert response.status_code == 200
        assert response.json()["stock"] == 7
    
    def test_update_stock_insufficient(self, client, auth_headers):
        """测试库存不足"""
        # 创建商品
        create_response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "Test Item", "price": 99.99, "stock": 5}
        )
        item_id = create_response.json()["id"]
        
        # 尝试减少过多库存
        response = client.post(
            f"/api/v1/items/{item_id}/stock",
            headers=auth_headers,
            params={"quantity": -10}
        )
        assert response.status_code == 400
        assert "库存不足" in response.json()["detail"]


class TestItemSearch:
    """商品搜索测试"""
    
    def test_search_items(self, client, auth_headers):
        """测试搜索商品"""
        # 创建商品
        client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "iPhone 15", "price": 7999}
        )
        client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "MacBook Pro", "price": 14999}
        )
        client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={"name": "iPad Air", "price": 4599}
        )
        
        # 搜索 iPhone
        response = client.get("/api/v1/items", params={"keyword": "iPhone"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "iPhone 15"
        
        # 搜索空结果
        response = client.get("/api/v1/items", params={"keyword": "Samsung"})
        assert response.status_code == 200
        assert len(response.json()) == 0


class TestTags:
    """标签测试"""
    
    def test_create_tag(self, client, auth_headers):
        """测试创建标签"""
        response = client.post(
            "/api/v1/items/tags",
            headers=auth_headers,
            json={"name": "Electronics"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Electronics"
    
    def test_list_tags(self, client, auth_headers):
        """测试获取标签列表"""
        # 创建标签
        client.post(
            "/api/v1/items/tags",
            headers=auth_headers,
            json={"name": "Tag1"}
        )
        client.post(
            "/api/v1/items/tags",
            headers=auth_headers,
            json={"name": "Tag2"}
        )
        
        # 获取列表
        response = client.get("/api/v1/items/tags")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_create_item_with_tags(self, client, auth_headers):
        """测试创建带标签的商品"""
        # 创建标签
        tag1 = client.post(
            "/api/v1/items/tags",
            headers=auth_headers,
            json={"name": "Electronics"}
        ).json()
        tag2 = client.post(
            "/api/v1/items/tags",
            headers=auth_headers,
            json={"name": "Phone"}
        ).json()
        
        # 创建商品
        response = client.post(
            "/api/v1/items",
            headers=auth_headers,
            json={
                "name": "iPhone 15",
                "price": 7999,
                "tag_ids": [tag1["id"], tag2["id"]]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["tags"]) == 2
