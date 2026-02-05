# Chat 应用 - 容器化部署指南

这是一个前后端分离的聊天应用，前端使用 Nuxt.js，后端使用 Flask 和 PostgreSQL 数据库。本项目提供了完整的容器化部署方案。

## 架构

- **前端**: Nuxt.js 应用，运行在端口 3000
- **后端**: Flask 应用，运行在端口 5001
- **数据库**: PostgreSQL，运行在端口 5432
- **存储**: 文件上传目录映射到宿主机

## 快速开始

### 先决条件

- Docker (版本 20.10.0 或更高)
- Docker Compose (版本 2.0.0 或更高)

### 部署生产环境

1. 复制环境变量模板并填入您的配置：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入 API 密钥等配置
   ```

2. 使用部署脚本启动服务：
   ```bash
   ./script/deploy.sh deploy
   ```

3. 访问应用：
   - 前端: [http://localhost:3000](http://localhost:3000)
   - 后端 API: [http://localhost:5001/api](http://localhost:5001/api)
   - 健康检查: [http://localhost:5001/api/health](http://localhost:5001/api/health)

### 部署开发环境

```bash
./script/deploy.sh dev
```

## 部署脚本使用方法

本项目提供了一个便捷的部署脚本 `script/deploy.sh`，支持以下命令：

- `./script/deploy.sh deploy` - 构建并启动生产环境（默认）
- `./script/deploy.sh dev` - 构建并启动开发环境
- `./script/deploy.sh stop` - 停止生产环境
- `./script/deploy.sh stop-dev` - 停止开发环境
- `./script/deploy.sh logs` - 查看生产环境日志
- `./script/deploy.sh logs-dev` - 查看开发环境日志
- `./script/deploy.sh clean` - 清理所有容器、网络和未使用的镜像
- `./script/deploy.sh rebuild` - 重新构建镜像并启动

## 目录结构

```
.
├── backend/              # Flask 后端应用
│   ├── app.py            # 主应用文件
│   ├── requirements.txt  # Python 依赖
│   ├── Dockerfile        # 生产环境 Dockerfile
│   └── Dockerfile.dev    # 开发环境 Dockerfile
├── frontend/             # Nuxt.js 前端应用
│   ├── nuxt.config.ts    # Nuxt 配置
│   ├── package.json      # Node.js 依赖
│   ├── Dockerfile        # 生产环境 Dockerfile
│   └── Dockerfile.dev    # 开发环境 Dockerfile
├── init.sql              # PostgreSQL 初始化脚本
├── docker-compose.yml    # 生产环境编排文件
├── docker-compose.dev.yml # 开发环境编排文件
├── .env.example          # 环境变量示例
└── script/
    └── deploy.sh         # 部署脚本
```

## 环境变量配置

在 `.env` 文件中配置以下环境变量：

- `OPENAI_API_KEY`: OpenAI API 密钥
- `ANTHROPIC_API_KEY`: Anthropic API 密钥
- `POSTGRES_DB`: PostgreSQL 数据库名
- `POSTGRES_USER`: PostgreSQL 用户名
- `POSTGRES_PASSWORD`: PostgreSQL 密码

## 数据持久化

- PostgreSQL 数据持久化存储在 Docker 卷 `postgres_data` 中
- 上传的文件存储在 `backend/uploads` 目录并映射到宿主机

## 健康检查

后端服务提供健康检查端点：`/api/health`

## 自定义配置

如需自定义配置，您可以：

1. 修改 `docker-compose.yml` 或 `docker-compose.dev.yml` 文件
2. 更新 `init.sql` 中的数据库初始化脚本
3. 调整各服务的环境变量配置