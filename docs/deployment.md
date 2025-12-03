# Flask 部署指南 (Deployment Guide)

这份指南介绍如何将 Flask 应用部署到生产环境。

## 目录

1. [生产环境准备](#生产环境准备)
2. [使用 Gunicorn](#使用-gunicorn)
3. [使用 Nginx](#使用-nginx)
4. [使用 Docker](#使用-docker)
5. [云平台部署](#云平台部署)
6. [持续集成/部署](#持续集成部署)

---

## 生产环境准备

### 1. 环境变量配置

创建 `.env` 文件（不要提交到版本控制）：

```bash
# .env
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=your-very-long-and-random-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

### 2. 安装生产依赖

```bash
pip install gunicorn gevent
pip install psycopg2-binary  # PostgreSQL
pip install redis  # Redis
```

### 3. 数据库迁移

```bash
# 初始化数据库
flask db init

# 创建迁移
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

---

## 使用 Gunicorn

### 基本配置

```bash
# 启动 Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"

# 参数说明
# -w 4: 4 个工作进程
# -b 0.0.0.0:8000: 绑定到所有接口的 8000 端口
```

### Gunicorn 配置文件

创建 `gunicorn_config.py`:

```python
# gunicorn_config.py
import multiprocessing

# 服务器套接字
bind = "0.0.0.0:8000"
backlog = 2048

# 工作进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 1000
timeout = 30
keepalive = 2

# 安全
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 日志
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'
loglevel = 'info'

# 进程命名
proc_name = 'flask_app'

# 服务器钩子
def on_starting(server):
    print("Gunicorn server is starting")

def on_reload(server):
    print("Gunicorn server is reloading")

def when_ready(server):
    print("Gunicorn server is ready")

def on_exit(server):
    print("Gunicorn server is exiting")
```

使用配置文件启动：

```bash
gunicorn -c gunicorn_config.py "app:create_app()"
```

### Supervisor 进程管理

安装 Supervisor:

```bash
sudo apt-get install supervisor
```

创建配置文件 `/etc/supervisor/conf.d/flask_app.conf`:

```ini
[program:flask_app]
command=/path/to/venv/bin/gunicorn -c gunicorn_config.py "app:create_app()"
directory=/path/to/your/app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flask_app/err.log
stdout_logfile=/var/log/flask_app/out.log
```

管理应用：

```bash
# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动应用
sudo supervisorctl start flask_app

# 停止应用
sudo supervisorctl stop flask_app

# 重启应用
sudo supervisorctl restart flask_app

# 查看状态
sudo supervisorctl status flask_app
```

---

## 使用 Nginx

### 安装 Nginx

```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS/RHEL
sudo yum install nginx
```

### Nginx 配置

创建配置文件 `/etc/nginx/sites-available/flask_app`:

```nginx
# HTTP 配置
server {
    listen 80;
    server_name example.com www.example.com;
    
    # 强制跳转到 HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS 配置
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # 日志
    access_log /var/log/nginx/flask_app_access.log;
    error_log /var/log/nginx/flask_app_error.log;
    
    # 客户端最大上传大小
    client_max_body_size 10M;
    
    # 静态文件
    location /static {
        alias /path/to/your/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media {
        alias /path/to/your/app/media;
        expires 30d;
    }
    
    # 代理到 Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;
}
```

启用配置：

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重新加载 Nginx
sudo systemctl reload nginx
```

### SSL 证书（Let's Encrypt）

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d example.com -d www.example.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 使用 Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:create_app()"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: always
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
  
  redis:
    image: redis:7-alpine
    restart: always
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/app/static:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
```

### 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 数据库迁移
docker-compose exec web flask db upgrade
```

---

## 云平台部署

### Heroku

1. 创建 `Procfile`:

```
web: gunicorn "app:create_app()"
```

2. 创建 `runtime.txt`:

```
python-3.11.0
```

3. 部署：

```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 添加 PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 推送代码
git push heroku main

# 运行迁移
heroku run flask db upgrade

# 查看日志
heroku logs --tail
```

### AWS (Elastic Beanstalk)

1. 安装 EB CLI:

```bash
pip install awsebcli
```

2. 初始化：

```bash
eb init -p python-3.11 flask-app
```

3. 创建环境：

```bash
eb create flask-env
```

4. 部署：

```bash
eb deploy
```

### Google Cloud Platform (App Engine)

1. 创建 `app.yaml`:

```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT "app:create_app()"

env_variables:
  FLASK_ENV: "production"

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

2. 部署：

```bash
gcloud app deploy
```

### Digital Ocean

使用 App Platform：

1. 连接 GitHub 仓库
2. 选择 Python 环境
3. 配置构建命令和启动命令
4. 添加环境变量
5. 部署

---

## 持续集成/部署

### GitHub Actions

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=app tests/
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/app
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          flask db upgrade
          sudo supervisorctl restart flask_app
```

---

## 性能优化

### 1. 使用 CDN

配置静态文件使用 CDN：

```python
# config.py
class ProductionConfig(Config):
    CDN_DOMAIN = 'https://cdn.example.com'
    
    @staticmethod
    def init_app(app):
        # 配置静态文件 URL
        app.config['STATIC_URL'] = app.config.get('CDN_DOMAIN', '') + '/static'
```

### 2. 缓存配置

```python
# Redis 缓存
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': 300
})
```

### 3. 数据库优化

```python
# config.py
class ProductionConfig(Config):
    # 连接池配置
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 10
    
    # 启用查询优化
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ECHO = False
```

---

## 监控和日志

### 1. 应用监控

使用 Sentry 进行错误跟踪：

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 2. 日志聚合

使用 ELK Stack (Elasticsearch, Logstash, Kibana) 或 Graylog。

### 3. 性能监控

使用 New Relic、Datadog 或 Prometheus + Grafana。

---

## 安全检查清单

- [ ] 设置强密码的 SECRET_KEY
- [ ] 使用 HTTPS
- [ ] 启用 CSRF 保护
- [ ] 配置 CORS
- [ ] 实施速率限制
- [ ] 启用 SQL 注入防护
- [ ] 配置安全的 Cookie 设置
- [ ] 定期更新依赖包
- [ ] 配置防火墙
- [ ] 定期备份数据库
- [ ] 启用日志记录
- [ ] 配置错误页面（不泄露敏感信息）

---

## 备份策略

### 数据库备份

```bash
#!/bin/bash
# backup.sh

# 配置
DB_NAME="your_database"
DB_USER="your_user"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# 保留最近 7 天的备份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

定时任务：

```bash
# crontab -e
0 2 * * * /path/to/backup.sh
```

---

## 总结

部署 Flask 应用的关键步骤：

1. ✅ 准备生产环境配置
2. ✅ 使用 Gunicorn 作为 WSGI 服务器
3. ✅ 配置 Nginx 作为反向代理
4. ✅ 启用 HTTPS
5. ✅ 配置进程管理（Supervisor）
6. ✅ 实施监控和日志
7. ✅ 定期备份
8. ✅ 持续集成/部署

记住：**安全性、性能和可维护性同等重要！**
