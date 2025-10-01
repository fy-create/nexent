# Nexent 模型自动化管理工具

这个工具集帮助您自动化管理 Nexent 中的 AI 模型，无需通过 UI 界面手动添加。支持批量导入、删除和验证模型连通性。

## 📁 文件结构
```
my-task/model_management/
├── nexent_model_manager.py    # 主要的Python管理脚本
├── models_config.json         # 模型配置文件
├── .env                      # 环境变量配置
├── one_click_deploy.sh       # 一键部署脚本（删除->导入->校验）
├── setupENV.sh              # 虚拟环境设置脚本
├── venv/                    # Python虚拟环境
└── README.md                # 使用说明
```


## 🚀 快速开始

### 1. 环境准备

```bash
# 进入脚本目录
cd my-task/model_management

# 设置Python虚拟环境（首次使用）
./setupENV.sh

# 激活虚拟环境
source venv/bin/activate

# 编辑环境变量，填入您的API密钥
vim .env
```

### 2. 配置模型

编辑 `models_config.json` 文件，添加您要管理的模型。当前配置包含：

- **Jina Embeddings V4**: 文本嵌入和多模态嵌入
- **DeepSeek V3.1**: 大语言模型
- **通义千问 2.5-32B**: 大语言模型
- **通义千问 2.5-VL-32B**: 视觉语言模型

```json
{
  "models": [
    {
      "model_name": "jina-embeddings-v4",
      "model_type": "embedding",
      "base_url": "https://api.jina.ai/v1/embeddings",
      "api_key": "${JINA_API_KEY}",
      "max_tokens": 0,
      "display_name": "Jina embedding",
      "model_factory": "OpenAI-API-Compatible"
    }
  ]
}
```

### 3. 一键部署

```bash
# 使用一键部署脚本（推荐）
./one_click_deploy.sh

# 该脚本会自动执行：
# 1. 删除现有所有模型
# 2. 从配置文件导入新模型
# 3. 验证所有模型连通性
```

## 📖 详细使用方法

### 命令行参数

```bash
# 激活虚拟环境
source venv/bin/activate

# 查看帮助
python nexent_model_manager.py --help

# 从配置文件批量添加模型
python nexent_model_manager.py --config models_config.json

# 删除所有模型
python nexent_model_manager.py --delete-all

# 验证特定模型连通性
python nexent_model_manager.py --verify "Jina embedding"

# 验证所有模型连通性
python nexent_model_manager.py --verify-all

# 指定自定义API地址和Token
python nexent_model_manager.py --config models_config.json \
    --base-url "http://your-nexent-server:5010" \
    --token "your-auth-token"
```

### 支持的模型类型

- `llm`: 大语言模型
- `embedding`: 向量化模型
- `vlm`: 视觉语言模型
- `multi_embedding`: 多模态嵌入
- `rerank`: 重排序模型
- `stt`: 语音转文字
- `tts`: 文字转语音

### 环境变量配置

在 `.env` 文件中配置以下变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `JINA_API_KEY` | Jina AI API 密钥 | `jina_xxx` |
| `SILICONFLOW_API_KEY` | 硅基流动 API 密钥 | `sk-xxx` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-xxx` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxx` |

## 🔧 高级用法

### 自定义脚本集成

您可以在自己的脚本中导入和使用这个管理器：

```python
from nexent_model_manager import NexentModelManager, ModelConfig

# 创建管理器
manager = NexentModelManager(
    base_url="http://localhost:5010",
    token="your-token"
)

# 添加单个模型
model = ModelConfig(
    model_name="custom-model",
    model_type="llm",
    base_url="https://api.example.com/v1",
    api_key="your-key",
    display_name="自定义模型"
)

manager.add_model(model)

# 批量操作
models = manager.load_config_from_file("custom_config.json")
manager.batch_add_models(models)

# 验证连通性
manager.verify_all_models()
```

### CI/CD 集成

在您的 CI/CD 流水线中使用：

```yaml
# GitHub Actions 示例
- name: Setup Python Environment
  run: |
    cd my-task/model_management
    ./setupENV.sh

- name: Deploy Models to Nexent
  run: |
    cd my-task/model_management
    source venv/bin/activate
    ./one_click_deploy.sh
  env:
    JINA_API_KEY: ${{ secrets.JINA_API_KEY }}
    SILICONFLOW_API_KEY: ${{ secrets.SILICONFLOW_API_KEY }}
```

## 🛠️ 脚本说明

### setupENV.sh
- 自动创建和配置Python虚拟环境
- 安装必要的依赖包（requests）
- 首次使用时运行

### one_click_deploy.sh
- 一键完成模型部署流程
- 自动加载环境变量
- 执行删除->导入->验证的完整流程
- 提供详细的执行日志

### nexent_model_manager.py
- 核心管理脚本
- 支持批量操作和单个操作
- 提供完整的错误处理和日志输出
- 支持环境变量替换

## 🐛 故障排查

### 常见问题

1. **连接失败**: 
   - 检查 Nexent 服务是否运行在 `http://localhost:5010`
   - 确认防火墙设置

2. **认证失败**: 
   - 确认 API 密钥是否正确配置在 `.env` 文件中
   - 检查环境变量是否正确加载

3. **模型添加失败**: 
   - 检查模型名称是否重复
   - 验证 API 端点是否可访问
   - 确认模型类型是否正确

4. **虚拟环境问题**:
   - 重新运行 `./setupENV.sh`
   - 确保使用 `source venv/bin/activate` 激活环境

### 调试模式

查看详细执行日志：

```bash
# 使用一键部署脚本会自动显示详细日志
./one_click_deploy.sh

# 或者直接运行Python脚本查看详细输出
python nexent_model_manager.py --config models_config.json
```

### 验证部署结果

```bash
# 验证所有模型是否正常工作
python nexent_model_manager.py --verify-all

# 检查特定模型
python nexent_model_manager.py --verify "模型显示名称"
```

## 📝 配置文件格式

`models_config.json` 支持环境变量替换，使用 `${VARIABLE_NAME}` 格式：

```json
{
  "models": [
    {
      "model_name": "模型名称",
      "model_type": "模型类型",
      "base_url": "API基础URL",
      "api_key": "${API_KEY_ENV_VAR}",
      "max_tokens": 最大令牌数,
      "display_name": "显示名称",
      "model_factory": "OpenAI-API-Compatible"
    }
  ]
}
```

## 🔄 更新和维护

定期更新模型配置：

1. 编辑 `models_config.json` 添加新模型
2. 更新 `.env` 文件中的API密钥
3. 运行 `./one_click_deploy.sh` 重新部署
4. 使用 `--verify-all` 验证所有模型状态

这个工具让您能够高效地管理 Nexent 平台中的 AI 模型，支持自动化部署和维护工作流程。