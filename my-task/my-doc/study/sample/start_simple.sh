#!/bin/bash

# 简单的Docker启动脚本（不依赖Docker Compose）

set -e

echo "🐳 Python Flask Hello World Docker 示例 (简单模式)"
echo "================================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装，请先安装Docker"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 停止并删除已存在的容器（如果有）
echo "🧹 清理已存在的容器..."
docker stop test-hello-world 2>/dev/null || true
docker rm test-hello-world 2>/dev/null || true

# 构建镜像
echo "🔨 构建Docker镜像..."
docker build -t test-hello-world .

# 启动容器
echo "🚀 启动服务..."
docker run -d -p 8080:8080 --name test-hello-world test-hello-world

echo "⏳ 等待服务启动..."
sleep 5

# 检查容器状态
if docker ps | grep -q "test-hello-world"; then
    echo "✅ 服务启动成功!"
    echo ""
    echo "📍 访问地址:"
    echo "   主页: http://localhost:8080"
    echo "   健康检查: http://localhost:8080/health"
    echo "   系统信息: http://localhost:8080/info"
    echo ""
    echo "📋 管理命令:"
    echo "   查看日志: docker logs -f test-hello-world"
    echo "   停止服务: docker stop test-hello-world"
    echo "   删除容器: docker rm test-hello-world"
else
    echo "❌ 服务启动失败，请检查日志:"
    docker logs test-hello-world
    exit 1
fi