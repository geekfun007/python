"""
Python HTTP 服务器与 FastAPI 详解 (with Type Hints)
===================================================

本文件涵盖：
- http.server (标准库)
- FastAPI 基础
- FastAPI 路由与参数
- 请求和响应
- 依赖注入
- 中间件
- FastAPI 底层原理 (Starlette + Pydantic)
"""

from typing import Any, Annotated, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json
import uvicorn

# ============================================================================
# 1. http.server (标准库 - 简单服务器)
# ============================================================================

class SimpleHTTPServerDemo:
    """标准库 HTTP 服务器"""
    
    @staticmethod
    def basic_server_code() -> str:
        """基本服务器代码示例"""
        return '''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MyHandler(BaseHTTPRequestHandler):
    """自定义请求处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Hello, World!</h1>')
        
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {"message": "Hello", "timestamp": "2024-01-01"}
            self.wfile.write(json.dumps(data).encode())
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"received": json.loads(post_data)}
        self.wfile.write(json.dumps(response).encode())

# 启动服务器
# server = HTTPServer(('localhost', 8000), MyHandler)
# server.serve_forever()
'''


# ============================================================================
# 2. FastAPI 基础
# ============================================================================

# 注意: 需要安装 fastapi 和 uvicorn
# pip install fastapi uvicorn[standard]

from fastapi import (
    FastAPI, APIRouter, Depends, HTTPException, status,
    Query, Path, Body, Header, Cookie, Form, File, UploadFile,
    Request, Response, BackgroundTasks
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr, field_validator

# 创建 FastAPI 应用
app = FastAPI(
    title="Python Tutorial API",
    description="FastAPI 教程示例 API",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)


# ============================================================================
# 3. Pydantic 模型
# ============================================================================

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "john@example.com"
                }
            ]
        }
    }


class UserCreate(UserBase):
    """创建用户请求"""
    password: str = Field(..., min_length=8, description="密码")
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool = True
    created_at: datetime


class ItemModel(BaseModel):
    """商品模型"""
    name: str = Field(..., min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    price: float = Field(..., gt=0)
    tax: float | None = Field(default=None, ge=0)
    tags: list[str] = Field(default_factory=list)
    
    @property
    def total_price(self) -> float:
        return self.price + (self.tax or 0)


class OrderStatus(str, Enum):
    """订单状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class OrderModel(BaseModel):
    """订单模型"""
    id: int
    items: list[ItemModel]
    status: OrderStatus = OrderStatus.PENDING
    total: float | None = None
    
    def model_post_init(self, __context: Any) -> None:
        """初始化后计算总价"""
        if self.total is None:
            self.total = sum(item.total_price for item in self.items)


# ============================================================================
# 4. 路由与路径参数
# ============================================================================

# 基本路由
@app.get("/")
async def root() -> dict[str, str]:
    """根路由"""
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict[str, Any]:
    """
    路径参数会自动进行类型转换和验证
    - item_id: int 类型，自动转换
    """
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int,
    item_id: int,
    q: str | None = None
) -> dict[str, Any]:
    """多个路径参数"""
    result = {"user_id": user_id, "item_id": item_id}
    if q:
        result["q"] = q
    return result


# 路径参数验证
@app.get("/items-validated/{item_id}")
async def get_item_validated(
    item_id: Annotated[int, Path(
        title="商品 ID",
        description="要查询的商品 ID",
        ge=1,  # >= 1
        le=1000,  # <= 1000
        examples=[1, 42, 100]
    )]
) -> dict[str, int]:
    """使用 Path 进行路径参数验证"""
    return {"item_id": item_id}


# ============================================================================
# 5. 查询参数
# ============================================================================

@app.get("/search")
async def search_items(
    # 必需参数
    keyword: str,
    # 可选参数
    category: str | None = None,
    # 带默认值
    page: int = 1,
    size: int = 10,
    # 布尔参数
    in_stock: bool = True,
) -> dict[str, Any]:
    """查询参数示例"""
    return {
        "keyword": keyword,
        "category": category,
        "page": page,
        "size": size,
        "in_stock": in_stock
    }


@app.get("/search-validated")
async def search_validated(
    keyword: Annotated[str, Query(
        min_length=2,
        max_length=50,
        description="搜索关键词"
    )],
    page: Annotated[int, Query(ge=1, le=100)] = 1,
    size: Annotated[int, Query(ge=1, le=50)] = 10,
    tags: Annotated[list[str] | None, Query(description="标签列表")] = None,
) -> dict[str, Any]:
    """带验证的查询参数"""
    return {
        "keyword": keyword,
        "page": page,
        "size": size,
        "tags": tags
    }


# ============================================================================
# 6. 请求体
# ============================================================================

@app.post("/items", response_model=ItemModel, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemModel) -> ItemModel:
    """
    创建商品
    - item: 自动从 JSON 请求体解析
    - response_model: 响应模型（过滤和验证）
    """
    return item


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate) -> dict[str, Any]:
    """创建用户"""
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "is_active": True,
        "created_at": datetime.now()
    }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: ItemModel,
    importance: Annotated[int, Body(ge=1, le=5)] = 1
) -> dict[str, Any]:
    """
    混合路径参数、请求体和额外的 Body 参数
    """
    return {
        "item_id": item_id,
        "item": item.model_dump(),
        "importance": importance
    }


# ============================================================================
# 7. Headers, Cookies, Form
# ============================================================================

@app.get("/headers")
async def read_headers(
    user_agent: Annotated[str | None, Header()] = None,
    x_token: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header(alias="Accept-Language")] = None,
) -> dict[str, Any]:
    """读取请求头"""
    return {
        "user_agent": user_agent,
        "x_token": x_token,
        "accept_language": accept_language
    }


@app.get("/cookies")
async def read_cookies(
    session_id: Annotated[str | None, Cookie()] = None,
) -> dict[str, Any]:
    """读取 Cookies"""
    return {"session_id": session_id}


@app.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> dict[str, str]:
    """表单登录"""
    return {"username": username, "message": "Login successful"}


# ============================================================================
# 8. 文件上传
# ============================================================================

@app.post("/uploadfile")
async def upload_file(
    file: UploadFile,
    description: Annotated[str | None, Form()] = None
) -> dict[str, Any]:
    """单文件上传"""
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "description": description
    }


@app.post("/uploadfiles")
async def upload_files(
    files: list[UploadFile]
) -> list[dict[str, Any]]:
    """多文件上传"""
    results = []
    for file in files:
        contents = await file.read()
        results.append({
            "filename": file.filename,
            "size": len(contents)
        })
    return results


# ============================================================================
# 9. 响应处理
# ============================================================================

@app.get("/html", response_class=HTMLResponse)
async def get_html() -> str:
    """返回 HTML"""
    return """
    <html>
        <head><title>Hello</title></head>
        <body><h1>Hello, World!</h1></body>
    </html>
    """


@app.get("/custom-response")
async def custom_response() -> Response:
    """自定义响应"""
    data = {"message": "Custom response"}
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        headers={"X-Custom-Header": "custom-value"}
    )


@app.get("/set-cookie")
async def set_cookie(response: Response) -> dict[str, str]:
    """设置 Cookie"""
    response.set_cookie(
        key="session_id",
        value="abc123",
        httponly=True,
        max_age=3600
    )
    return {"message": "Cookie set"}


# ============================================================================
# 10. 依赖注入
# ============================================================================

# 简单依赖
def get_db():
    """获取数据库连接"""
    db = {"connection": "fake_db"}
    try:
        yield db
    finally:
        print("Closing DB connection")


# 带参数的依赖
def pagination(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
) -> dict[str, int]:
    """分页参数"""
    return {"page": page, "size": size, "skip": (page - 1) * size}


# 类依赖
class CommonParams:
    """通用参数类"""
    
    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit


# 认证依赖
security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict[str, str]:
    """获取当前用户"""
    token = credentials.credentials
    # 实际项目中应该验证 token
    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"username": "authenticated_user", "token": token}


@app.get("/items-with-db")
async def items_with_db(
    db: Annotated[dict, Depends(get_db)],
    pagination: Annotated[dict, Depends(pagination)]
) -> dict[str, Any]:
    """使用依赖注入"""
    return {
        "db": db,
        "pagination": pagination
    }


@app.get("/items-with-class")
async def items_with_class(
    commons: Annotated[CommonParams, Depends()]
) -> dict[str, Any]:
    """类依赖"""
    return {
        "q": commons.q,
        "skip": commons.skip,
        "limit": commons.limit
    }


@app.get("/protected")
async def protected_route(
    user: Annotated[dict, Depends(get_current_user)]
) -> dict[str, Any]:
    """受保护的路由"""
    return {"message": f"Hello, {user['username']}!"}


# ============================================================================
# 11. 后台任务
# ============================================================================

def write_log(message: str) -> None:
    """模拟写日志的后台任务"""
    print(f"[LOG] {message}")


@app.post("/send-notification")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
) -> dict[str, str]:
    """发送通知（后台处理）"""
    background_tasks.add_task(write_log, f"Sending email to {email}")
    return {"message": "Notification scheduled"}


# ============================================================================
# 12. 异常处理
# ============================================================================

class ItemNotFoundError(Exception):
    """商品未找到异常"""
    def __init__(self, item_id: int):
        self.item_id = item_id


@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(
    request: Request,
    exc: ItemNotFoundError
) -> JSONResponse:
    """自定义异常处理器"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Item not found",
            "item_id": exc.item_id
        }
    )


@app.get("/items-error/{item_id}")
async def get_item_or_error(item_id: int) -> dict[str, Any]:
    """演示异常处理"""
    if item_id == 0:
        raise ItemNotFoundError(item_id)
    if item_id < 0:
        raise HTTPException(
            status_code=400,
            detail="Item ID must be positive"
        )
    return {"item_id": item_id}


# ============================================================================
# 13. 中间件
# ============================================================================

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 自定义中间件
@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """添加处理时间头"""
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================================================
# 14. 路由器 (APIRouter)
# ============================================================================

# 创建路由器
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@user_router.get("/")
async def list_users() -> list[dict[str, Any]]:
    """获取用户列表"""
    return [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"}
    ]


@user_router.get("/{user_id}")
async def get_user(user_id: int) -> dict[str, Any]:
    """获取单个用户"""
    return {"id": user_id, "username": f"user_{user_id}"}


# 注册路由器
app.include_router(user_router)


# ============================================================================
# 15. FastAPI 底层原理
# ============================================================================

class FastAPIInternalsDemo:
    """FastAPI 底层原理"""
    
    @staticmethod
    def explain_architecture() -> str:
        """架构说明"""
        return """
FastAPI 底层架构：

1. Starlette (ASGI 框架)
   ├── 处理 HTTP 请求/响应
   ├── 路由系统
   ├── 中间件支持
   ├── WebSocket 支持
   └── 后台任务

2. Pydantic (数据验证)
   ├── 类型验证
   ├── 数据转换
   ├── JSON Schema 生成
   └── 序列化/反序列化

3. Python 类型提示
   ├── 参数解析
   ├── 编辑器支持
   └── 文档生成

请求处理流程：
1. ASGI Server (uvicorn) 接收请求
2. Starlette 路由到对应处理函数
3. FastAPI 使用 Pydantic 验证/转换参数
4. 执行处理函数
5. Pydantic 序列化响应
6. 返回响应
"""
    
    @staticmethod
    def starlette_example() -> str:
        """纯 Starlette 示例"""
        return '''
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"hello": "world"})

async def user(request):
    user_id = request.path_params["user_id"]
    return JSONResponse({"user_id": user_id})

app = Starlette(routes=[
    Route("/", homepage),
    Route("/users/{user_id:int}", user),
])
'''
    
    @staticmethod
    def asgi_interface() -> str:
        """ASGI 接口说明"""
        return '''
# ASGI (Asynchronous Server Gateway Interface)
# 是 WSGI 的异步版本

async def app(scope, receive, send):
    """
    ASGI 应用接口
    
    scope: 请求信息（类型、路径、头等）
    receive: 接收请求体的协程
    send: 发送响应的协程
    """
    assert scope["type"] == "http"
    
    # 读取请求体
    body = b""
    while True:
        message = await receive()
        body += message.get("body", b"")
        if not message.get("more_body"):
            break
    
    # 发送响应
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [[b"content-type", b"application/json"]],
    })
    await send({
        "type": "http.response.body",
        "body": b\'{"hello": "world"}\',
    })
'''


# ============================================================================
# 16. 完整 CRUD 示例
# ============================================================================

# 模拟数据库
fake_db: dict[int, dict[str, Any]] = {}
item_counter = 0


class ItemCRUD(BaseModel):
    """商品 CRUD 模型"""
    name: str
    price: float
    description: str | None = None


class ItemInDB(ItemCRUD):
    """数据库中的商品"""
    id: int
    created_at: datetime


crud_router = APIRouter(prefix="/crud/items", tags=["CRUD"])


@crud_router.post("/", response_model=ItemInDB, status_code=201)
async def crud_create_item(item: ItemCRUD) -> dict[str, Any]:
    """创建商品"""
    global item_counter
    item_counter += 1
    
    db_item = {
        "id": item_counter,
        **item.model_dump(),
        "created_at": datetime.now()
    }
    fake_db[item_counter] = db_item
    return db_item


@crud_router.get("/", response_model=list[ItemInDB])
async def crud_list_items(
    skip: int = 0,
    limit: int = 10
) -> list[dict[str, Any]]:
    """获取商品列表"""
    items = list(fake_db.values())
    return items[skip:skip + limit]


@crud_router.get("/{item_id}", response_model=ItemInDB)
async def crud_get_item(item_id: int) -> dict[str, Any]:
    """获取单个商品"""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@crud_router.put("/{item_id}", response_model=ItemInDB)
async def crud_update_item(item_id: int, item: ItemCRUD) -> dict[str, Any]:
    """更新商品"""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item = fake_db[item_id]
    db_item.update(item.model_dump())
    return db_item


@crud_router.delete("/{item_id}", status_code=204)
async def crud_delete_item(item_id: int) -> None:
    """删除商品"""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]


app.include_router(crud_router)


# ============================================================================
# 启动服务器
# ============================================================================

def run_server() -> None:
    """运行服务器"""
    uvicorn.run(
        "11_fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式热重载
        log_level="info"
    )


if __name__ == "__main__":
    print("FastAPI Server")
    print("=" * 60)
    print("\n启动服务器:")
    print("  python 11_fastapi_server.py")
    print("\n或使用 uvicorn:")
    print("  uvicorn 11_fastapi_server:app --reload")
    print("\n访问文档:")
    print("  Swagger UI: http://localhost:8000/docs")
    print("  ReDoc: http://localhost:8000/redoc")
    print("\n" + "=" * 60)
    
    # 打印架构说明
    print(FastAPIInternalsDemo.explain_architecture())
    
    # 如果取消注释下面的行，将启动服务器
    # run_server()
