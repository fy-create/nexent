# 使用官方Python 3.10精简版镜像作为基础镜像
FROM python:3.10-slim

# 设置维护者信息
LABEL maintainer="test-team"
LABEL description="Python Flask Hello World Docker示例"
LABEL version="1.0.0"

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=hello_world_app.py
ENV FLASK_ENV=production

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖包
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY hello_world_app.py .

# 创建非root用户（安全最佳实践）
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露应用端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动应用
CMD ["python", "hello_world_app.py"]