# ============================================
# Makefile - 常用命令
# ============================================

.PHONY: help dev prod stop logs test lint format clean

# 默认目标
help:
	@echo "FastAPI 实战项目 - 可用命令:"
	@echo ""
	@echo "  make dev      - 启动开发环境"
	@echo "  make prod     - 启动生产环境"
	@echo "  make stop     - 停止所有服务"
	@echo "  make logs     - 查看日志"
	@echo "  make test     - 运行测试"
	@echo "  make lint     - 代码检查"
	@echo "  make format   - 代码格式化"
	@echo "  make clean    - 清理容器和数据"
	@echo ""

# 开发环境
dev:
	docker-compose -f docker-compose.dev.yml up -d
	@echo ""
	@echo "开发环境已启动!"
	@echo "  - API: http://localhost:8000"
	@echo "  - 文档: http://localhost:8000/docs"
	@echo "  - Adminer: http://localhost:8080"
	@echo "  - Redis Commander: http://localhost:8081"

# 生产环境
prod:
	docker-compose up -d --build
	@echo ""
	@echo "生产环境已启动!"
	@echo "  - API: http://localhost/api"
	@echo "  - 文档: http://localhost/docs"

# 停止服务
stop:
	docker-compose -f docker-compose.dev.yml down
	docker-compose down

# 查看日志
logs:
	docker-compose logs -f

# 运行测试
test:
	docker-compose -f docker-compose.dev.yml exec app pytest -v

# 代码检查
lint:
	docker-compose -f docker-compose.dev.yml exec app black --check app/
	docker-compose -f docker-compose.dev.yml exec app isort --check-only app/
	docker-compose -f docker-compose.dev.yml exec app mypy app/

# 代码格式化
format:
	docker-compose -f docker-compose.dev.yml exec app black app/
	docker-compose -f docker-compose.dev.yml exec app isort app/

# 清理
clean:
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose down -v
	rm -rf logs/*.log
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
