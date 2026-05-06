# 钢城博客

一个基于 FastAPI + Vue 3 的全栈博客平台，支持文章发布、评论互动、收藏和浏览历史等功能。

## 技术栈

### 后端
- **框架**: FastAPI + Uvicorn
- **ORM**: SQLAlchemy 2.0（异步）
- **数据库**: MySQL 8
- **缓存**: Redis（文章列表缓存 + 浏览量批量同步）
- **认证**: JWT + bcrypt
- **数据校验**: Pydantic v2
- **数据库迁移**: Alembic

### 前端
- **框架**: Vue 3（组合式 API + TypeScript）
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **UI 组件库**: Element Plus
- **样式**: Tailwind CSS

## 功能特性

- 用户注册/登录（JWT 认证）
- 文章的创建、编辑、删除和列表展示
- 文章搜索（按标题、作者）
- 评论的发布与删除
- 文章收藏与取消收藏
- 浏览历史记录
- Redis 缓存文章列表，提升读取性能
- 浏览量通过 Redis 计数器批量写入数据库，减少数据库压力
- 基于滑动窗口的接口限流
- 统一的 JSON 响应格式

## 项目结构

```
├── app/                    # 后端应用
│   ├── main.py             # FastAPI 入口
│   ├── database.py         # 数据库连接配置
│   ├── models/             # SQLAlchemy ORM 模型
│   ├── schemas/            # Pydantic 数据校验模型
│   ├── crud/               # 数据库访问层
│   ├── routers/            # API 路由
│   ├── core/               # 配置、安全、依赖注入、日志
│   ├── cache/              # Redis 缓存策略
│   └── scripts/            # 后台同步脚本
├── blog-frontend/          # Vue 3 前端
│   └── src/
│       ├── views/          # 页面组件
│       ├── components/     # 公共组件
│       ├── api/            # API 请求封装
│       ├── stores/         # Pinia 状态管理
│       ├── router/         # 路由配置
│       └── utils/          # 工具函数
├── alembic/                # 数据库迁移
├── run.py                  # 后端启动脚本
├── requirements.txt        # Python 依赖
└── .env                    # 环境变量配置
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis

### 后端启动

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 .env 文件中的数据库和 Redis 连接信息

# 执行数据库迁移
alembic upgrade head

# 启动后端服务
python run.py
```

服务默认运行在 `http://127.0.0.1:8080`，API 文档访问 `/docs`。

### 前端启动

```bash
cd blog-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 后台浏览量同步

```bash
python -m app.scripts.sync_worker
```

该进程会定期将 Redis 中的浏览量增量写入 MySQL。

## API 概览

| 路由前缀 | 说明 |
|---------|------|
| `/api/users` | 用户注册、登录、信息管理 |
| `/api/articles` | 文章 CRUD、列表查询 |
| `/api/comment` | 评论发布与管理 |
| `/api/favorite` | 收藏管理 |
| `/api/history` | 浏览历史管理 |

所有接口返回统一格式：`{ "code": 200, "message": "...", "data": ... }`
