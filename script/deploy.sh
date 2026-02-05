#!/bin/bash

# 部署脚本 - 用于构建和启动容器化应用

set -e  # 遇到错误时退出

echo "🚀 开始部署 Chat 应用..."

# 检查是否安装了 Docker 和 Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose 未安装，尝试使用 docker compose (Docker v20.10.0+)"
    if ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
fi

# 设置默认环境变量
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-chat-app}"

# 根据参数决定执行的操作
case "${1:-deploy}" in
    "deploy")
        echo "🏗️  构建并启动所有服务..."
        docker-compose up --build -d
        
        echo "⏳ 等待服务启动..."
        sleep 10
        
        echo "✅ 部署完成！"
        echo "🌐 前端访问地址: http://localhost:3000"
        echo "🔗 后端API地址: http://localhost:5001/api"
        echo "💾 数据库地址: localhost:5432 (数据库: chat_db, 用户: chat_user)"
        ;;
    
    "dev")
        echo "🏗️  构建并启动开发环境..."
        docker-compose -f docker-compose.dev.yml up --build -d
        
        echo "⏳ 等待开发服务启动..."
        sleep 10
        
        echo "✅ 开发环境启动完成！"
        echo "🌐 前端开发服务器: http://localhost:3000"
        echo "🔗 后端API开发服务器: http://localhost:5001/api"
        ;;
    
    "stop")
        echo "🛑 停止所有服务..."
        docker-compose down
        echo "✅ 服务已停止"
        ;;
        
    "stop-dev")
        echo "🛑 停止开发环境..."
        docker-compose -f docker-compose.dev.yml down
        echo "✅ 开发环境已停止"
        ;;
        
    "logs")
        echo "📋 查看服务日志..."
        docker-compose logs -f
        ;;
        
    "logs-dev")
        echo "📋 查看开发环境日志..."
        docker-compose -f docker-compose.dev.yml logs -f
        ;;
        
    "clean")
        echo "🧹 清理所有容器、网络和未使用的镜像..."
        docker-compose down -v
        docker system prune -f
        echo "✅ 清理完成"
        ;;
        
    "rebuild")
        echo "🔄 重新构建并启动服务..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo "✅ 重建完成"
        ;;
        
    *)
        echo "📖 使用说明:"
        echo "  $0 deploy     - 构建并启动生产环境 (默认)"
        echo "  $0 dev        - 构建并启动开发环境"
        echo "  $0 stop       - 停止生产环境"
        echo "  $0 stop-dev   - 停止开发环境"
        echo "  $0 logs       - 查看生产环境日志"
        echo "  $0 logs-dev   - 查看开发环境日志"
        echo "  $0 clean      - 清理所有资源"
        echo "  $0 rebuild    - 重新构建镜像并启动"
        exit 1
        ;;
esac

echo "🎉 部署脚本执行完成"