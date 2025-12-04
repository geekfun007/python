# Makefile for FastAPI project
# 项目管理命令

.PHONY: help install dev init-db run test clean lint format

help:  ## 显示帮助信息
	@echo "FastAPI 项目管理命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装生产依赖
	pip install -r requirements.txt

dev:  ## 安装开发依赖
	pip install -r requirements.txt -r requirements-dev.txt

init-db:  ## 初始化数据库
	python init_db.py

run:  ## 运行应用
	python main.py

test:  ## 运行测试
	pytest tests/ -v --cov=app

test-api:  ## 测试 API
	python test_api.py

clean:  ## 清理缓存文件
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build

lint:  ## 代码检查
	flake8 app/ --max-line-length=100
	mypy app/ --ignore-missing-imports
	pylint app/ --max-line-length=100

format:  ## 代码格式化
	black app/ main.py config.py
	isort app/ main.py config.py

migrate-create:  ## 创建数据库迁移
	alembic revision --autogenerate -m "$(msg)"

migrate-up:  ## 执行数据库迁移
	alembic upgrade head

migrate-down:  ## 回滚数据库迁移
	alembic downgrade -1

docker-build:  ## 构建 Docker 镜像
	docker build -t fastapi-demo .

docker-run:  ## 运行 Docker 容器
	docker-compose up -d

docker-stop:  ## 停止 Docker 容器
	docker-compose down

logs:  ## 查看日志
	tail -f logs/*.log
