"""
CORS Configuration
跨域资源共享配置

CORS原理：
浏览器出于安全考虑，限制跨域HTTP请求
CORS中间件允许指定哪些域可以访问API
"""
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    """
    配置CORS
    
    参数说明：
    - allow_origins: 允许的源列表
    - allow_credentials: 是否允许携带凭证（cookies）
    - allow_methods: 允许的HTTP方法
    - allow_headers: 允许的HTTP头
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应该指定具体域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有HTTP头
    )
