# Chat 应用

这是一个前后端分离的聊天应用，前端使用 Nuxt.js，后端使用 Flask 和 PostgreSQL 数据库。

## 快速开始（容器化部署）

本项目提供了完整的容器化部署方案：

1. **克隆项目后，进入项目目录**
   ```bash
   cd chatbot
   ```

2. **复制环境变量配置**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件填入你的配置
   ```

3. **启动服务**
   ```bash
   # 生产环境部署
   ./script/deploy.sh deploy
   ```

4. **访问应用**
   - 前端: http://localhost:3000
   - 后端 API: http://localhost:5001/api

## 项目结构

- `frontend/` - Nuxt.js 前端应用
- `backend/` - Flask 后端应用  
- `docker-compose.yml` - 生产环境编排文件
- `script/deploy.sh` - 一键部署脚本

更多部署信息请参见 [DEPLOYMENT.md](./DEPLOYMENT.md)。