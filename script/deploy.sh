#!/bin/bash

# 智能文档问答助手部署脚本

echo "开始部署智能文档问答助手..."

# 检查Docker是否已安装
if ! [ -x "$(command -v docker)" ]; then
  echo "错误: Docker未安装，请先安装Docker." >&2
  exit 1
fi

# 检查Docker Compose是否已安装
if ! [ -x "$(command -v docker-compose)" ]; then
  echo "警告: Docker Compose未安装，尝试使用docker compose命令."
  if ! [ -x "$(command -v docker compose)" ]; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose." >&2
    exit 1
  fi
fi

echo "构建并启动服务..."

# 使用Docker Compose构建并启动服务
if [ -x "$(command -v docker-compose)" ]; then
  docker-compose up --build -d
else
  docker compose up --build -d
fi

echo "等待服务启动..."

# 等待几秒让服务启动
sleep 10

# 检查服务状态
echo "检查服务状态..."
if [ -x "$(command -v docker-compose)" ]; then
  docker-compose ps
else
  docker compose ps
fi

echo "部署完成!"
echo "前端访问地址: http://localhost:3000"
echo "后端API地址: http://localhost:8000"
echo "数据库地址: http://localhost:5432 (内部使用)"