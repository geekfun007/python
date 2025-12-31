-- ============================================
-- Seed Data - 初始化测试数据
-- ============================================

USE fastapi_demo;

-- 插入测试用户
-- 密码都是 'password123' 的 bcrypt 哈希
INSERT INTO users (username, email, password_hash, status, role) VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4tS.IqBBAKVXKDeW', 1, 2),
('user1', 'user1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4tS.IqBBAKVXKDeW', 1, 0),
('user2', 'user2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4tS.IqBBAKVXKDeW', 1, 0),
('moderator', 'mod@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4tS.IqBBAKVXKDeW', 1, 1);

-- 插入分类
INSERT INTO categories (name, description, parent_id, sort_order) VALUES
('技术', '技术相关文章', NULL, 1),
('Python', 'Python 编程', 1, 1),
('JavaScript', 'JavaScript 编程', 1, 2),
('DevOps', '运维与部署', 1, 3),
('生活', '生活随笔', NULL, 2),
('旅行', '旅行记录', 5, 1),
('美食', '美食分享', 5, 2);

-- 插入标签
INSERT INTO tags (name, color) VALUES
('FastAPI', '#009688'),
('Python', '#3776AB'),
('Docker', '#2496ED'),
('MySQL', '#4479A1'),
('Redis', '#DC382D'),
('Nginx', '#009639'),
('Vue.js', '#4FC08D'),
('React', '#61DAFB'),
('TypeScript', '#3178C6'),
('教程', '#FF9800');

-- 插入示例文章
INSERT INTO articles (title, content, summary, author_id, category_id, status, view_count, like_count, published_at) VALUES
(
    'FastAPI 入门教程',
    '# FastAPI 入门教程\n\nFastAPI 是一个现代、快速（高性能）的 Web 框架...\n\n## 安装\n\n```bash\npip install fastapi uvicorn\n```\n\n## 快速开始\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"Hello": "World"}\n```',
    'FastAPI 是一个现代、快速的 Python Web 框架，本文介绍其基本使用方法。',
    1, 2, 1, 1500, 120, NOW()
),
(
    'Docker 容器化部署指南',
    '# Docker 容器化部署\n\n本文介绍如何使用 Docker 部署 Python 应用...\n\n## Dockerfile\n\n```dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD ["uvicorn", "main:app", "--host", "0.0.0.0"]\n```',
    'Docker 容器化部署 Python 应用的完整指南。',
    1, 4, 1, 890, 65, NOW()
),
(
    'MySQL 性能优化实战',
    '# MySQL 性能优化\n\n数据库性能优化是后端开发的重要技能...\n\n## 索引优化\n\n合理使用索引可以大幅提升查询性能...',
    'MySQL 数据库性能优化的实用技巧和最佳实践。',
    2, 2, 1, 650, 48, NOW()
);

-- 关联文章和标签
INSERT INTO article_tags (article_id, tag_id) VALUES
(1, 1), (1, 2), (1, 10),  -- FastAPI 文章
(2, 3), (2, 6), (2, 10),  -- Docker 文章
(3, 4), (3, 2);           -- MySQL 文章

-- 插入示例评论
INSERT INTO comments (article_id, user_id, content) VALUES
(1, 2, '写得很详细，感谢分享！'),
(1, 3, '请问 FastAPI 和 Flask 相比有什么优势？'),
(1, 1, '@user2 FastAPI 的主要优势是：1. 自动生成 API 文档 2. 原生异步支持 3. 类型提示和数据验证'),
(2, 2, 'Docker Compose 的配置示例能再详细点吗？');

-- 设置评论的父子关系
UPDATE comments SET parent_id = 2 WHERE id = 3;
