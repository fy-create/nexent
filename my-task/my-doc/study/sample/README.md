# Python Flask Hello World Docker 示例

这是一个简单的Python Flask应用，演示如何使用Docker进行容器化部署。

## 📋 项目结构
```
sample/
├── hello_world_app.py      # Flask应用主文件
├── requirements.txt        # Python依赖包
├── Dockerfile             # Docker镜像构建文件
├── docker compose.yml     # Docker Compose配置
├── .dockerignore          # Docker忽略文件
├── start.sh              # 启动脚本
├── stop.sh               # 停止脚本
└── README.md             # 项目文档
```

## 🚀 快速开始

### 前置要求

- Docker (版本 20.0+)
- Docker Compose (版本 2.0+)

### 方法1: 使用启动脚本（推荐）

```bash
# 给脚本执行权限
chmod +x start.sh stop.sh

# 启动服务
./start.sh

# 停止服务
./stop.sh
```

### 方法2: 使用Docker Compose

```bash
# 构建并启动服务
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

### 方法3: 使用Docker命令

```bash
# 构建镜像
docker build -t test-hello-world .

# 运行容器
docker run -d -p 8080:8080 --name test-hello-world test-hello-world

# 停止容器
docker stop test-hello-world

# 删除容器
docker rm test-hello-world
```

## 🌐 访问应用

启动成功后，可以通过以下地址访问应用：

- **主页**: http://localhost:8080
- **健康检查**: http://localhost:8080/health
- **系统信息**: http://localhost:8080/info

## 📊 API端点

### GET /
返回HTML格式的欢迎页面，包含应用信息和当前时间。

### GET /health
返回JSON格式的健康检查信息：
```json
{
  "status": "healthy",
  "message": "Hello World应用运行正常",
  "timestamp": "2024-01-01T12:00:00.000000",
  "version": "1.0.0"
}
```

### GET /info
返回JSON格式的系统信息：
```json
{
  "python_version": "3.10",
  "framework": "Flask",
  "container": "Docker",
  "environment": "production",
  "hostname": "container_id",
  "port": 8080
}
```

## 🔧 配置说明

### 环境变量

- `FLASK_ENV`: Flask运行环境 (development/production)
- `FLASK_APP`: Flask应用入口文件
- `PYTHONUNBUFFERED`: Python输出缓冲设置

### 端口配置

- 容器内端口: 8080
- 主机映射端口: 8080 (可在docker compose.yml中修改)

## 🛠️ 开发指南

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python hello_world_app.py
```

### 修改应用

1. 编辑 `hello_world_app.py` 文件
2. 重新构建镜像: `docker compose build`
3. 重启服务: `docker compose restart`

### 添加新的依赖

1. 在 `requirements.txt` 中添加新的包
2. 重新构建镜像: `docker compose build`

## 📝 日志管理

```bash
# 查看实时日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f hello-world

# 查看最近100行日志
docker compose logs --tail=100
```

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   lsof -i :8080
   
   # 修改docker compose.yml中的端口映射
   ports:
     - "8081:8080"  # 改为8081端口
   ```

2. **容器启动失败**
   ```bash
   # 查看详细日志
   docker compose logs
   
   # 检查容器状态
   docker compose ps
   ```

3. **镜像构建失败**
   ```bash
   # 清理Docker缓存
   docker system prune -f
   
   # 重新构建
   docker compose build --no-cache
   ```

### 健康检查

应用包含内置的健康检查机制：
- 每30秒检查一次
- 超时时间3秒
- 最多重试3次
- 启动后40秒开始检查

## 🔒 安全最佳实践

1. **非root用户**: 容器内使用非特权用户运行应用
2. **最小镜像**: 使用python:3.10-slim精简镜像
3. **健康检查**: 内置健康检查机制
4. **环境隔离**: 使用Docker网络隔离

## 📈 性能优化

1. **多阶段构建**: 可以进一步优化镜像大小
2. **缓存优化**: 合理安排Dockerfile层级
3. **资源限制**: 在生产环境中设置内存和CPU限制

```yaml
# 在docker compose.yml中添加资源限制
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

## 🚀 部署到生产环境

### 使用Docker Swarm

```bash
# 初始化Swarm
docker swarm init

# 部署服务
docker stack deploy -c docker compose.yml hello-world-stack
```

### 使用Kubernetes

可以将Docker Compose配置转换为Kubernetes配置：

```bash
# 安装kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose

# 转换配置
kompose convert
```

## 📚 扩展学习

- [Docker官方文档](https://docs.docker.com/)
- [Flask官方文档](https://flask.palletsprojects.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [Python Docker最佳实践](https://docs.docker.com/language/python/)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个示例项目。

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**作者**: test Team  
**版本**: 1.0.0  
**更新时间**: 2024年1月