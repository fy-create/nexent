#!/bin/bash

# Python Flask Hello World Docker 停止脚本

echo "🛑 停止Hello World服务..."

# 检查Docker Compose是否可用（支持新旧版本）
COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ 错误: Docker Compose未安装或不可用"
    exit 1
fi

# 停止并删除容器
$COMPOSE_CMD down

# 可选：删除镜像（取消注释下面的行来删除镜像）
# docker rmi $(docker images -q test-hello-world) 2>/dev/null || true

echo "✅ 服务已停止"