# MCP 医疗工具集文档

## 概述

MCP (Model Context Protocol) 医疗工具集是一个专门为医疗领域设计的智能分析工具套件，基于 FastMCP 框架构建。该工具集主要包含两大核心模块：

1. **医疗图像分析模块** - 专业的医疗影像智能分析
2. **医疗数据处理模块** - 完整的医疗数据工程流水线

## 项目结构
```
backend/tool_collection/mcp/
├── local_mcp_service.py              # MCP服务主入口
├── medical_image_analysis/           # 医疗图像分析模块
│   ├── init .py
│   ├── case_analyzer.py             # 医疗病例分析器
│   ├── image_processor.py           # 图像处理器
│   └── medical_prompts.py           # 医疗提示词模板
└── medical_data_processing/         # 医疗数据处理模块
    ├── init .py
    ├── data_cleaner.py              # 数据清洗器
    ├── demo_processor.py            # 演示处理器
    ├── knowledge_annotator.py       # 知识标注器
    ├── knowledge_base_integrator.py # 知识库集成器
    ├── pathology_processor.py       # 病理处理器
    ├── professional_annotator.py    # 专业标注器
    └── qa_generator.py              # Q&A生成器
```

## 核心工具

### 1. 乳腺组织学分析工具 (breast_histology_analyzer)

**功能描述**: 专业的乳腺组织学显微镜图像分析工具，支持乳腺病理切片的智能分析和诊断辅助。

**参数**:
- `image_path` (str): 乳腺组织学显微镜图像文件的完整路径
- `magnification` (str, 可选): 显微镜放大倍数（如：40x, 100x, 200x, 400x等），默认"未知"
- `staining_method` (str, 可选): 染色方法，默认"HE"
- `clinical_info` (str, 可选): 相关临床信息（年龄、症状、影像学发现等）
- `custom_requirements` (str, 可选): 自定义分析要求或特别关注点

**返回**: JSON格式的病理学分析结果

**分析内容**:
- 组织结构特征
- 细胞形态学特征
- 病理学诊断意见
- 分级评估（如适用）
- 临床意义和建议

### 2. 医疗数据清洗工具 (medical_data_cleaner)

**功能描述**: 专门用于清洗病理教科书等医疗专业素材，去除噪声并提取医学术语。

**参数**:
- `text_content` (str, 可选): 直接输入的医疗文本内容
- `file_path` (str, 可选): 单个文件路径
- `batch_file_paths` (str, 可选): 批量文件路径，用逗号分隔

**功能特性**:
- 医学术语识别和提取
- 噪声模式清理（图片引用、页码、参考文献等）
- 支持单文件和批量处理
- 质量评分和统计分析

### 3. 医疗专业标注工具 (medical_professional_annotator)

**功能描述**: 对清洗后的医疗数据进行病理学术语、疾病诊断、组织学特征等专业标注。

**参数**:
- `content` (str): 需要标注的医疗文本内容
- `content_type` (str, 可选): 内容类型
  - `general`: 通用医疗内容
  - `pathology`: 病理学内容
  - `diagnosis`: 诊断相关内容
  - `treatment`: 治疗相关内容

**标注类别**:
- **病理学术语**: 肿瘤分类、疾病分类、组织学特征
- **诊断相关术语**: 临床表现、辅助检查、诊断方法、治疗方案
- **严重程度分级**: 轻度、中度、重度

### 4. 医疗Q&A生成工具 (medical_qa_generator)

**功能描述**: 基于标注后的医疗数据生成高质量的病理学问答对数据集。

**参数**:
- `annotated_content` (str): 标注后的医疗内容（JSON字符串格式）
- `qa_count` (int, 可选): 生成的Q&A对数量，默认10个

**问题类型**:
- **定义类**: "什么是{term}？"
- **症状类**: "{disease}有哪些症状？"
- **诊断类**: "如何诊断{disease}？"
- **治疗类**: "{disease}如何治疗？"
- **病理类**: "{disease}的病理特征是什么？"

### 5. 医疗数据工程流水线 (medical_data_pipeline)

**功能描述**: 完整执行数据清洗→专业标注→Q&A生成的全流程处理。

**参数**:
- `input_content` (str, 可选): 输入的原始医疗文本
- `input_file_path` (str, 可选): 输入文件路径
- `qa_count` (int, 可选): 生成的Q&A对数量，默认10个
- `content_type` (str, 可选): 内容类型，默认"general"

**处理流程**:
1. **数据清洗**: 去除噪声，提取医学术语
2. **专业标注**: 标注病理术语、诊断信息等
3. **Q&A生成**: 生成高质量问答对数据集

### 6. 医疗知识库集成工具 (medical_knowledge_base_integrator)

**功能描述**: 将Q&A数据集存储到Elasticsearch知识库，支持创建索引、数据存储和搜索。

**参数**:
- `action` (str): 操作类型
  - `create_index`: 创建索引
  - `integrate_data`/`store`: 存储数据
  - `search`: 搜索知识库
  - `list_indices`: 列出索引
  - `delete_index`: 删除索引
- `index_name` (str, 可选): 索引名称
- `qa_dataset` (str, 可选): Q&A数据集（JSON字符串格式）
- `query` (str, 可选): 搜索查询
- `search_type` (str, 可选): 搜索类型（accurate, semantic, hybrid），默认"hybrid"
- `top_k` (int, 可选): 搜索结果数量，默认10

## 医疗图像分析模块详解

### MedicalCaseAnalyzer 类

**核心功能**: 医疗病例分析器，基于视觉语言模型进行医疗图像智能分析。

**主要方法**:
- `analyze_medical_image_from_stream()`: 从图像流分析医疗图像
- `_init_vlm_model()`: 初始化视觉语言模型

**技术特点**:
- 集成OpenAI视觉语言模型
- 支持多租户配置
- 实时消息观察和日志记录
- 专业医疗提示词模板

### MedicalImageProcessor 类

**功能**: 医疗图像预处理和格式转换。

### 医疗提示词模板

包含专业的医疗分析提示词，涵盖：
- 病例分析模板
- 安全免责声明
- 专业术语指导

## 医疗数据处理模块详解

### MedicalDataCleaner 类

**核心功能**: 医疗文本数据清洗和预处理。

**清洗模式**:
- **医学术语模式**: 疾病名称、解剖结构、病理术语、诊断术语、组织学特征
- **噪声清理模式**: 图片引用、表格引用、页码、参考文献、附录引用

**主要方法**:
- `clean_medical_text()`: 清洗单个医疗文本
- `batch_clean_files()`: 批量清洗文件
- `extract_medical_terms()`: 提取医学术语
- `calculate_quality_score()`: 计算文本质量分数

### MedicalProfessionalAnnotator 类

**核心功能**: 医疗专业术语标注和分类。

**标注体系**:
- **病理学术语词典**: 肿瘤分类、疾病分类、组织学特征
- **诊断相关术语**: 临床表现、辅助检查、诊断方法、治疗方案
- **严重程度分级**: 轻度、中度、重度分级标准

**主要方法**:
- `annotate_medical_content()`: 标注医疗内容
- `extract_entities()`: 提取医疗实体
- `classify_content()`: 内容分类
- `calculate_annotation_quality()`: 计算标注质量

### MedicalQAGenerator 类

**核心功能**: 基于标注内容生成高质量医疗问答对。

**问题模板系统**:
- **定义类问题**: 术语定义和概念解释
- **症状类问题**: 疾病症状和临床表现
- **诊断类问题**: 诊断方法和检查手段
- **治疗类问题**: 治疗方案和用药指导
- **病理类问题**: 病理特征和组织学表现

**质量控制**:
- 问答对相关性评分
- 医学准确性验证
- 语言流畅度检查
- 信息完整性评估

### MedicalKnowledgeBaseIntegrator 类

**核心功能**: 医疗知识库集成和管理。

**技术架构**:
- 基于Elasticsearch的向量数据库
- 支持混合搜索（精确+语义）
- 多索引管理
- 实时数据同步

**主要功能**:
- 创建和管理医疗知识索引
- Q&A数据集批量导入
- 多模式智能搜索
- 知识库维护和优化

## 使用示例

### 1. 乳腺组织学图像分析

```python
# 分析乳腺病理切片
result = await breast_histology_analyzer(
    image_path="breast_sample.jpg",
    magnification="400x",
    staining_method="HE",
    clinical_info="45岁女性，乳腺肿块",
    custom_requirements="重点关注细胞异型性"
)
```

### 2. 医疗数据处理流水线

```python
# 完整的数据处理流程
result = await medical_data_pipeline(
    input_file_path="pathology_textbook.txt",
    qa_count=20,
    content_type="pathology"
)
```

### 3. 知识库集成

```python
# 创建医疗知识库索引
await medical_knowledge_base_integrator(
    action="create_index",
    index_name="breast_pathology_kb"
)

# 存储Q&A数据
await medical_knowledge_base_integrator(
    action="store",
    index_name="breast_pathology_kb",
    qa_dataset=json.dumps(qa_data)
)

# 搜索知识库
result = await medical_knowledge_base_integrator(
    action="search",
    index_name="breast_pathology_kb",
    query="乳腺癌的病理特征",
    search_type="hybrid",
    top_k=5
)
```

## 技术特性

### 1. 多租户支持
- 支持多租户配置管理
- 独立的模型配置和权限控制
- 租户级别的数据隔离

### 2. 高可用性
- 异常处理和错误恢复
- 详细的日志记录和监控
- 优雅的降级策略

### 3. 可扩展性
- 模块化设计，易于扩展
- 插件式工具注册
- 标准化的接口规范

### 4. 数据安全
- MinIO对象存储集成
- 数据传输加密
- 访问权限控制

## 依赖项

### 核心依赖
- `fastmcp`: MCP协议框架
- `nexent.core`: 核心模型和工具
- `nexent.vector_database`: 向量数据库支持

### 数据库依赖
- `sqlalchemy`: 数据库ORM
- `elasticsearch`: 搜索引擎

### 图像处理依赖
- `PIL/Pillow`: 图像处理
- `opencv-python`: 计算机视觉

## 配置要求

### 环境变量
```bash
# Elasticsearch配置
ELASTICSEARCH_HOST=http://localhost:9200
ELASTICSEARCH_API_KEY=your_api_key
ELASTIC_PASSWORD=your_password

# 数据库配置
DATABASE_URL=your_database_url

# MinIO配置
MINIO_ENDPOINT=your_minio_endpoint
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
```

### 模型配置
- OpenAI VLM模型配置
- 租户级别的模型权限设置
- 模型参数和性能优化

## 最佳实践

### 1. 图像分析
- 使用高质量的病理切片图像
- 提供准确的放大倍数和染色信息
- 包含相关的临床背景信息

### 2. 数据处理
- 确保输入文本的医学专业性
- 选择合适的内容类型进行标注
- 合理设置Q&A生成数量

### 3. 知识库管理
- 定期更新和维护索引
- 优化搜索参数和策略
- 监控存储和查询性能

## 故障排除

### 常见问题
1. **图像分析失败**: 检查图像格式和MinIO连接
2. **模型初始化错误**: 验证租户配置和API密钥
3. **知识库连接失败**: 确认Elasticsearch服务状态
4. **数据处理异常**: 检查输入数据格式和编码

### 调试建议
- 启用详细日志记录
- 使用测试数据验证功能
- 监控系统资源使用情况
- 定期备份重要数据

