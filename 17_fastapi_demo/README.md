# FastAPI 实战示例

完整的 RESTful API 服务器实现。

## 功能特性

- ✅ RESTful API 设计
- ✅ 数据验证（Pydantic）
- ✅ 自动生成 API 文档
- ✅ 依赖注入
- ✅ 异常处理
- ✅ CORS 支持
- ✅ 查询参数
- ✅ 路径参数
- ✅ 请求体验证
- ✅ 响应模型

## 安装

```bash
pip install fastapi uvicorn pydantic
```

## 运行

```bash
# 开发模式（自动重载）
uvicorn main:app --reload

# 或者直接运行
python main.py

# 指定端口
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API 文档

启动服务器后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 用户管理

- `POST /api/users` - 创建用户
- `GET /api/users` - 获取用户列表
- `GET /api/users/{user_id}` - 获取单个用户
- `PUT /api/users/{user_id}` - 更新用户
- `DELETE /api/users/{user_id}` - 删除用户

### 商品管理

- `POST /api/items` - 创建商品
- `GET /api/items` - 获取商品列表
- `GET /api/items/{item_id}` - 获取单个商品

## 示例请求

### 创建用户

```bash
curl -X POST http://localhost:8000/api/users \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Bob",
       "email": "bob@example.com",
       "age": 30,
       "password": "password123"
     }'
```

### 获取用户列表

```bash
# 基本请求
curl http://localhost:8000/api/users

# 带分页
curl "http://localhost:8000/api/users?skip=0&limit=10"

# 按名称过滤
curl "http://localhost:8000/api/users?name=Alice"
```

### 更新用户

```bash
curl -X PUT http://localhost:8000/api/users/1 \
     -H "Content-Type: application/json" \
     -d '{"age": 26}'
```

### 创建商品

```bash
curl -X POST http://localhost:8000/api/items \
     -H "Content-Type: application/json" \
     -d '{
       "name": "iPhone 15",
       "description": "最新款iPhone",
       "price": 5999.0,
       "tax": 10.5,
       "tags": ["电子产品", "手机"]
     }'
```

### 获取商品（带过滤）

```bash
# 价格范围
curl "http://localhost:8000/api/items?min_price=1000&max_price=10000"

# 标签过滤
curl "http://localhost:8000/api/items?tags=电子产品&tags=手机"
```

## 项目结构

```
17_fastapi_demo/
├── main.py          # 主应用文件
└── README.md        # 说明文档
```

## 核心概念

### Pydantic 模型

数据验证和序列化：

```python
class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    age: Optional[int] = Field(None, ge=0, le=150)
```

### 路径参数

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    ...
```

### 查询参数

```python
@app.get("/items")
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    ...
```

### 请求体

```python
@app.post("/users")
async def create_user(user: UserCreate):
    ...
```

### 依赖注入

```python
def get_user(user_id: int):
    ...

@app.get("/users/{user_id}")
async def read_user(user: dict = Depends(get_user)):
    ...
```

## 扩展建议

1. **数据库集成**
   - SQLAlchemy
   - Tortoise ORM
   - MongoDB

2. **认证授权**
   - JWT tokens
   - OAuth2
   - API keys

3. **测试**
   - pytest
   - httpx (测试客户端)

4. **部署**
   - Docker
   - Kubernetes
   - Cloud platforms

5. **监控**
   - Prometheus
   - Grafana
   - Logging

## 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Uvicorn 文档](https://www.uvicorn.org/)
