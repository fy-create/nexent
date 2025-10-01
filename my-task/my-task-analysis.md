# My-Task 目录分析文档

## 📋 概述

`my-task` 目录是 Nexent 项目中的个人工作空间，主要用于存放与病理知识问答智能体开发相关的任务文件、工具、文档和实验数据。该目录体现了一个完整的 AI 项目开发流程，从模型管理到数据处理，从工具开发到知识库自动化。

## 🗂️ 目录结构
```
Users/liubin/work/github_ws/nexent/my-task/
├── MCP-tool/                    # MCP工具文档
│   └── mcp.md
├── build-and-deploy.sh          # 构建部署脚本
├── dock_reset.sh               # Docker环境重置脚本
├── iciar2018_70x30_with_DA/    # ICIAR2018乳腺癌数据集
│   ├── aug_0_1012.jpg
│   ├── aug_0_1076.jpg
│   ├── aug_0_36.jpg
│   ├── aug_0_46.jpg
│   └── test/
├── knowledge_base_automation/   # 知识库自动化工具
│   ├── requirements.txt
│   ├── setup_venv.sh
│   └── venv/
├── model_management/           # 模型管理工具集
│   ├── .env-sample.txt
│   ├── .env.txt
│   ├── README.md
│   ├── models_config.json
│   ├── nexent_model_manager.py
│   ├── one_click_deploy.sh
│   ├── setupENV.sh
│   └── venv/
├── my-doc/                     # 个人文档和学习笔记
│   ├── 1.1-配置专业的病理知识提示词.md
│   ├── 1.3-自定义工具开发(可选加分项).md
│   ├── 2-关于数据.md
│   ├── study/
│   │   ├── 1-docker.md
│   │   ├── 2-docker镜像.md
│   │   ├── 3-docker容器.md
│   │   ├── Nexent 项目分析报告.md
│   │   ├── nexant_docker.md
│   │   ├── sample/
│   │   └── 提示词的作用.md
│   └── 题目要求-native.md
└── 测试数据处理.md             # 数据处理测试文档
```

## 🔧 核心功能模块

### 1. 模型管理模块 (`model_management/`)

**功能描述**: 自动化管理 Nexent 中的 AI 模型，支持批量导入、删除和验证模型连通性。

**核心文件**:
- <mcfile name="nexent_model_manager.py" path="my-task/model_management/nexent_model_manager.py"></mcfile>: 主要的 Python 管理脚本
- <mcfile name="models_config.json" path="my-task/model_management/models_config.json"></mcfile>: 模型配置文件，包含：
  - **Jina Embeddings V4**: 文本嵌入和多模态嵌入
  - **DeepSeek V3.1**: 大语言模型
  - **通义千问 2.5-32B**: 大语言模型  
  - **通义千问 2.5-VL-32B**: 视觉语言模型
- <mcfile name="one_click_deploy.sh" path="my-task/model_management/one_click_deploy.sh"></mcfile>: 一键部署脚本（删除→导入→校验）

**配置示例**:
```json
{
  "models": [
    {
      "model_name": "jina-embeddings-v4",
      "model_type": "embedding",
      "base_url": "https://api.jina.ai/v1/embeddings",
      "api_key": "${JINA_API_KEY}",
      "display_name": "Jina embedding",
      "model_factory": "OpenAI-API-Compatible"
    }
  ]
}
```

### 2. MCP 工具模块 (`MCP-tool/`)

**功能描述**: 医疗案例处理 (Medical Case Processing) 工具的完整文档。

**核心内容**:
- <mcfile name="mcp.md" path="my-task/MCP-tool/mcp.md"></mcfile>: 详细的 MCP 工具文档，包含：
  - 乳腺组织学分析器
  - 医疗数据清洗器
  - 医疗专业标注器
  - 医疗问答生成器
  - 医疗数据处理管道
  - 医疗知识库集成器

### 3. 数据集模块 (`iciar2018_70x30_with_DA/`)

**功能描述**: ICIAR2018 乳腺癌病理数据集，用于病理知识问答智能体的训练和测试。

**数据特征**:
- **图像类型**: H&E 染色的乳腺组织病理图像
- **分辨率**: 2048x1536 像素，像素尺度 0.42 µm x 0.42 µm
- **分类标准**: 正常、良性、原位癌、浸润性癌
- **专业标注**: 由两名医学专家标注

**应用价值**:
- 作为高质量训练数据源
- 生成专业 Q&A 对数据集
- 支持多模态病理分析

### 4. 知识库自动化模块 (`knowledge_base_automation/`)

**功能描述**: 自动化知识库管理和维护工具。

**核心文件**:
- <mcfile name="requirements.txt" path="my-task/knowledge_base_automation/requirements.txt"></mcfile>: 依赖管理
- <mcfile name="setup_venv.sh" path="my-task/knowledge_base_automation/setup_venv.sh"></mcfile>: 环境设置脚本

### 5. 文档管理模块 (`my-doc/`)

**功能描述**: 项目相关的文档、学习笔记和任务要求。

**主要文档**:
- <mcfile name="1.1-配置专业的病理知识提示词.md" path="my-task/my-doc/1.1-配置专业的病理知识提示词.md"></mcfile>: 提示词配置指南
- <mcfile name="2-关于数据.md" path="my-task/my-doc/2-关于数据.md"></mcfile>: 数据集应用分析
- <mcfolder name="study" path="my-task/my-doc/study"></mcfolder>: 深度学习笔记，包含 Docker、项目分析等内容

## 🚀 部署和运维脚本

### 构建部署脚本 (`build-and-deploy.sh`)

**功能**: 自动化构建和部署 Nexent 服务
**主要步骤**:
1. 构建自定义 Docker 镜像
2. 配置环境变量
3. 部署服务（避免交互提示）

```bash
# 构建镜像
docker build --progress=plain -t nexent/nexent -f make/main/Dockerfile .

# 配置环境
cp .env.example .env
echo "NEXENT_IMAGE=nexent/nexent:latest" >> .env

# 部署服务
./deploy.sh --mode 1 --version 1 --is-mainland N --enable-terminal N --root-dir "$HOME/nexent-data"
```

### Docker 重置脚本 (`dock_reset.sh`)

**功能**: 清理和重置 Nexent Docker 环境
**清理范围**:
- 停止所有 Nexent 相关容器
- 删除容器和数据目录
- 强制清理残留资源

## 📊 项目任务分析

基于文档内容，该项目主要围绕两个核心任务：

### 任务一：智能体开发（基础任务）
1. **基础问答能力**: 模型接入、提示词配置、流畅问答
2. **知识库扩展**: 文档上传、知识外挂、专业资料集成
3. **自定义工具开发**: MCP 工具开发、病例图片分析等

### 任务二：数据工程与模型训练（进阶任务）
1. **数据处理与标注**: 使用 ModelEngine 数据工程平台
2. **模型推理**: 基于 ModelEngine 模型工程平台
3. **推理加速优化**: 性能优化和部署优化

## 🔗 技术栈和依赖

**核心技术**:
- **容器化**: Docker + Docker Compose
- **后端**: Python + FastAPI
- **数据库**: Elasticsearch + PostgreSQL + Redis + MinIO
- **AI 模型**: OpenAI-Compatible API
- **嵌入模型**: Jina Embeddings V4
- **大语言模型**: DeepSeek V3.1, 通义千问系列

**开发环境**:
- Python 虚拟环境管理
- 自动化脚本部署
- 配置文件管理

## 📈 项目特色

1. **完整的 AI 开发流程**: 从数据处理到模型部署的全链路覆盖
2. **专业医疗领域应用**: 专注于病理知识问答的垂直领域
3. **自动化工具集**: 模型管理、知识库维护、环境部署的自动化
4. **多模态支持**: 文本、图像、视觉语言模型的综合应用
5. **标准化配置**: 通过 JSON 配置文件管理复杂的模型参数
