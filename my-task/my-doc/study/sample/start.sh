#!/bin/bash

# Python Flask Hello World Docker 启动脚本
# 作者: test Team
# 版本: 1.0.0

set -e

echo "🐳 Python Flask Hello World Docker 示例"
echo "========================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否可用（支持新旧版本）
COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ 错误: Docker Compose未安装或不可用"
    echo "💡 提示: 请确保Docker Desktop已安装并正在运行"
    echo "   或者安装独立的docker-compose工具"
    exit 1
fi

echo "✅ Docker环境检查通过 (使用: $COMPOSE_CMD)"

# 构建并启动服务
echo "🔨 构建Docker镜像..."
$COMPOSE_CMD build

echo "🚀 启动服务..."
$COMPOSE_CMD up -d

echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if $COMPOSE_CMD ps | grep -q "Up"; then
    echo "✅ 服务启动成功!"
    echo ""
    echo "📍 访问地址:"
    echo "   主页: http://localhost:8080"
    echo "   健康检查: http://localhost:8080/health"
    echo "   系统信息: http://localhost:8080/info"
    echo ""
    echo "📋 管理命令:"
    echo "   查看日志: $COMPOSE_CMD logs -f"
    echo "   停止服务: $COMPOSE_CMD down"
    echo "   重启服务: $COMPOSE_CMD restart"
else
    echo "❌ 服务启动失败，请检查日志:"
    $COMPOSE_CMD logs
    exit 1
fi