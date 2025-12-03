"""
API 测试脚本
API Test Script

简单的测试脚本，用于验证 API 功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(response):
    """打印响应"""
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print("-" * 60)


def test_root():
    """测试根路径"""
    print("\n1. 测试根路径 GET /")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)


def test_health():
    """测试健康检查"""
    print("\n2. 测试健康检查 GET /health")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)


def test_create_user():
    """测试创建用户"""
    print("\n3. 测试创建用户 POST /api/v1/users/")
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test123456",
        "full_name": "测试用户",
        "age": 25
    }
    response = requests.post(f"{BASE_URL}/api/v1/users/", json=data)
    print_response(response)
    return response.json().get("data", {}).get("id")


def test_get_users():
    """测试获取用户列表"""
    print("\n4. 测试获取用户列表 GET /api/v1/users/")
    response = requests.get(f"{BASE_URL}/api/v1/users/?skip=0&limit=10")
    print_response(response)


def test_get_user(user_id):
    """测试获取用户详情"""
    print(f"\n5. 测试获取用户详情 GET /api/v1/users/{user_id}")
    response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}")
    print_response(response)


def test_update_user(user_id):
    """测试更新用户"""
    print(f"\n6. 测试更新用户 PUT /api/v1/users/{user_id}")
    data = {
        "full_name": "测试用户（已更新）",
        "age": 26
    }
    response = requests.put(f"{BASE_URL}/api/v1/users/{user_id}", json=data)
    print_response(response)


def test_search_users():
    """测试搜索用户"""
    print("\n7. 测试搜索用户 GET /api/v1/users/search/by-name")
    response = requests.get(f"{BASE_URL}/api/v1/users/search/by-name?search_term=测试")
    print_response(response)


def test_create_product():
    """测试创建产品"""
    print("\n8. 测试创建产品 POST /api/v1/products/")
    data = {
        "name": "测试产品",
        "description": "这是一个测试产品",
        "price": 99.99,
        "stock": 100,
        "category": "测试分类"
    }
    response = requests.post(f"{BASE_URL}/api/v1/products/", json=data)
    print_response(response)
    return response.json().get("data", {}).get("id")


def test_get_products():
    """测试获取产品列表"""
    print("\n9. 测试获取产品列表 GET /api/v1/products/")
    response = requests.get(f"{BASE_URL}/api/v1/products/?skip=0&limit=10")
    print_response(response)


def test_get_product(product_id):
    """测试获取产品详情"""
    print(f"\n10. 测试获取产品详情 GET /api/v1/products/{product_id}")
    response = requests.get(f"{BASE_URL}/api/v1/products/{product_id}")
    print_response(response)


def test_update_product_stock(product_id):
    """测试更新产品库存"""
    print(f"\n11. 测试更新产品库存 PATCH /api/v1/products/{product_id}/stock")
    data = {"quantity": -10}
    response = requests.patch(f"{BASE_URL}/api/v1/products/{product_id}/stock", json=data)
    print_response(response)


def test_price_range_query():
    """测试价格区间查询"""
    print("\n12. 测试价格区间查询 GET /api/v1/products/price-range/query")
    response = requests.get(f"{BASE_URL}/api/v1/products/price-range/query?min_price=50&max_price=200")
    print_response(response)


def test_statistics():
    """测试分类统计"""
    print("\n13. 测试分类统计 GET /api/v1/products/statistics/by-category")
    response = requests.get(f"{BASE_URL}/api/v1/products/statistics/by-category")
    print_response(response)


def test_delete_user(user_id):
    """测试删除用户"""
    print(f"\n14. 测试删除用户 DELETE /api/v1/users/{user_id}")
    response = requests.delete(f"{BASE_URL}/api/v1/users/{user_id}")
    print_response(response)


def test_delete_product(product_id):
    """测试删除产品"""
    print(f"\n15. 测试删除产品 DELETE /api/v1/products/{product_id}")
    response = requests.delete(f"{BASE_URL}/api/v1/products/{product_id}")
    print_response(response)


def main():
    """主函数"""
    print("=" * 60)
    print("FastAPI API 测试")
    print("=" * 60)
    print(f"基础URL: {BASE_URL}")
    print("\n请确保应用正在运行: python main.py")
    print("=" * 60)
    
    try:
        # 基础测试
        test_root()
        test_health()
        
        # 用户相关测试
        user_id = test_create_user()
        test_get_users()
        if user_id:
            test_get_user(user_id)
            test_update_user(user_id)
        test_search_users()
        
        # 产品相关测试
        product_id = test_create_product()
        test_get_products()
        if product_id:
            test_get_product(product_id)
            test_update_product_stock(product_id)
        test_price_range_query()
        test_statistics()
        
        # 删除测试（可选）
        # if user_id:
        #     test_delete_user(user_id)
        # if product_id:
        #     test_delete_product(product_id)
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保应用正在运行: python main.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")


if __name__ == "__main__":
    main()
