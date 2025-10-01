#!/bin/bash

cd ..

# 1. 构建自定义镜像
docker build --progress=plain -t nexent/nexent -f make/main/Dockerfile .
#docker build --progress=plain -t nexent/nexent-data-process -f make/data_process/Dockerfile .
#docker build --progress=plain -t nexent/nexent-web -f make/web/Dockerfile .

# 2. 配置环境变量
cd docker
cp .env.example .env
echo "NEXENT_IMAGE=nexent/nexent:latest" >> .env
echo "NEXENT_WEB_IMAGE=nexent/nexent-web:latest" >> .env
echo "NEXENT_DATA_PROCESS_IMAGE=nexent/nexent-data-process:latest" >> .env


# 3. 部署服务 - 使用环境变量方式避免所有交互提示
 ./deploy.sh --mode 1 --version 1 --is-mainland N --enable-terminal N --root-dir "$HOME/nexent-data"
  # ./deploy.sh