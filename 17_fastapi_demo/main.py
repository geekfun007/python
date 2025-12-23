"""
FastAPI 实战示例
完整的 RESTful API 服务器
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


# ============================================
# Pydantic 模型
# ============================================

class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('无效的邮箱格式')
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Alice",
                "email": "alice@example.com",
                "age": 25
            }
        }


class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., min_length=8, description="密码")


class User(UserBase):
    """用户模型（包含ID）"""
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """更新用户模型"""
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class Item(BaseModel):
    """商品模型"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="价格必须大于0")
    tax: Optional[float] = None
    tags: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "name": "iPhone 15",
                "description": "最新款iPhone",
                "price": 5999.0,
                "tax": 10.5,
                "tags": ["电子产品", "手机"]
            }
        }


# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(
    title="Python 教程 API",
    description="FastAPI 实战示例",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# 模拟数据库
# ============================================

users_db = {}
user_id_counter = 1

items_db = {}
item_id_counter = 1


# ============================================
# 依赖注入
# ============================================

def get_user(user_id: int = Path(..., description="用户ID")):
    """获取用户依赖"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 {user_id} 不存在"
        )
    return users_db[user_id]


# ============================================
# 路由 - 基础
# ============================================

@app.get("/", tags=["基础"])
async def root():
    """根路径"""
    return {
        "message": "欢迎使用 FastAPI",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["基础"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# ============================================
# 路由 - 用户管理 (CRUD)
# ============================================

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["用户"])
async def create_user(user: UserCreate):
    """创建用户"""
    global user_id_counter
    
    # 检查邮箱是否已存在
    for existing_user in users_db.values():
        if existing_user['email'] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
    
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now()
    }
    
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return new_user


@app.get("/api/users", response_model=List[User], tags=["用户"])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    name: Optional[str] = Query(None, description="按名称过滤")
):
    """获取用户列表"""
    users = list(users_db.values())
    
    # 过滤
    if name:
        users = [u for u in users if name.lower() in u['name'].lower()]
    
    # 分页
    users = users[skip:skip + limit]
    
    return users


@app.get("/api/users/{user_id}", response_model=User, tags=["用户"])
async def get_user_by_id(user: dict = Depends(get_user)):
    """获取单个用户"""
    return user


@app.put("/api/users/{user_id}", response_model=User, tags=["用户"])
async def update_user(
    user_update: UserUpdate,
    user_id: int = Path(..., description="用户ID")
):
    """更新用户"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 {user_id} 不存在"
        )
    
    user = users_db[user_id]
    
    # 更新字段
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        user[field] = value
    
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["用户"])
async def delete_user(user_id: int = Path(..., description="用户ID")):
    """删除用户"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 {user_id} 不存在"
        )
    
    del users_db[user_id]
    return None


# ============================================
# 路由 - 商品管理
# ============================================

@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["商品"])
async def create_item(item: Item):
    """创建商品"""
    global item_id_counter
    
    item_dict = item.dict()
    item_dict['id'] = item_id_counter
    items_db[item_id_counter] = item_dict
    item_id_counter += 1
    
    return item_dict


@app.get("/api/items", response_model=List[Item], tags=["商品"])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: Optional[float] = Query(None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(None, ge=0, description="最高价格"),
    tags: Optional[List[str]] = Query(None, description="标签过滤")
):
    """获取商品列表"""
    items = list(items_db.values())
    
    # 价格过滤
    if min_price is not None:
        items = [item for item in items if item['price'] >= min_price]
    if max_price is not None:
        items = [item for item in items if item['price'] <= max_price]
    
    # 标签过滤
    if tags:
        items = [item for item in items 
                 if any(tag in item.get('tags', []) for tag in tags)]
    
    # 分页
    items = items[skip:skip + limit]
    
    return items


@app.get("/api/items/{item_id}", response_model=Item, tags=["商品"])
async def get_item(item_id: int = Path(..., description="商品ID")):
    """获取单个商品"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品 {item_id} 不存在"
        )
    return items_db[item_id]


# ============================================
# 异常处理
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# ============================================
# 启动事件
# ============================================

@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    print("FastAPI 服务器启动")
    print("API 文档: http://localhost:8000/docs")
    
    # 初始化一些测试数据
    global user_id_counter, item_id_counter
    
    users_db[1] = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25,
        "created_at": datetime.now()
    }
    user_id_counter = 2
    
    items_db[1] = {
        "id": 1,
        "name": "iPhone 15",
        "description": "最新款iPhone",
        "price": 5999.0,
        "tax": 10.5,
        "tags": ["电子产品", "手机"]
    }
    item_id_counter = 2


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理"""
    print("FastAPI 服务器关闭")


# ============================================
# 运行说明
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ==========================================
    FastAPI 实战示例
    ==========================================
    
    运行服务器:
    uvicorn main:app --reload
    
    或者:
    python main.py
    
    API 文档:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    
    示例请求:
    
    # 获取所有用户
    curl http://localhost:8000/api/users
    
    # 创建用户
    curl -X POST http://localhost:8000/api/users \\
         -H "Content-Type: application/json" \\
         -d '{"name": "Bob", "email": "bob@example.com", "age": 30, "password": "password123"}'
    
    # 获取用户
    curl http://localhost:8000/api/users/1
    
    # 更新用户
    curl -X PUT http://localhost:8000/api/users/1 \\
         -H "Content-Type: application/json" \\
         -d '{"age": 26}'
    
    # 删除用户
    curl -X DELETE http://localhost:8000/api/users/1
    
    # 获取商品（带过滤）
    curl "http://localhost:8000/api/items?min_price=1000&max_price=10000"
    
    ==========================================
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
