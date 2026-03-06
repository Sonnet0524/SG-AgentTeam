# AI Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06  
**Current Phase**: v1.1 Sprint 1  
**Status**: 🟢 Active  

---

## Current Focus

**Primary Task**: 语义索引和搜索工具开发

**Immediate Actions**:
1. 🚀 **Sprint 1 任务** (Week 1-2)
   - TASK-AI1: 语义索引构建 (build_semantic_index)
   - TASK-AI2: 语义搜索工具 (semantic_search)
2. 📦 安装依赖
   - sentence-transformers
   - faiss-cpu
   - numpy
3. 🧪 编写测试

---

## Team Status

| Team | Status | Current Task |
|------|--------|--------------|
| AI Team | 🚀 Active | Sprint 1 (索引+搜索) |
| Core Team | 🟢 Ready | Sprint 2 准备 |
| Integration Team | 📋 Planned | Sprint 3 (集成) |

---

## 🎯 v1.1 Responsibilities

### 核心职责
- ⏳ 文本向量嵌入 (Sprint 1)
- ⏳ 向量索引构建 (Sprint 1)
- ⏳ 语义搜索实现 (Sprint 1)
- 📋 增量更新支持 (未来)

### 不负责
- ❌ 传统数据处理 (Core Team)
- ❌ 文件扫描和读取 (opencode负责)
- ❌ 外部连接器 (Integration Team)

---

## 🚀 启动流程

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/ai/CATCH_UP.md      # 本文件
practice/status/agent-status.md     # 团队状态
```

### 2. 同步代码仓库
```bash
# 同步dev仓库
git pull origin main

# 同步main仓库
cd ../knowledge-assistant
git pull origin main
cd ../knowledge-assistant-dev
```

### 3. 安装依赖
```bash
cd ../knowledge-assistant
pip install sentence-transformers faiss-cpu
```

### 4. 检查任务
- 查看 GitHub Issues (label: `team: ai`)
- 查看 `status/task-assignments/v1.1-task-assignments.md`

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用工具的 `workdir` 参数

---

## Key Files to Reference

### Planning Documents
- `status/task-assignments/v1.1-task-assignments.md` - 任务分配
- `../knowledge-assistant/docs/PRD.md` - 产品需求

### Team Configs
- `agents/ai/AGENTS.md` - AI Team配置

### Technical Docs
- `../knowledge-assistant/docs/PRD.md` - API设计参考

---

## Sprint 1 Tasks

### TASK-AI1: 语义索引构建

**工期**: 5天  
**优先级**: P0  

**步骤**:
1. 创建目录结构
   ```
   scripts/
   ├── embeddings/
   │   ├── __init__.py
   │   ├── encoder.py
   │   └── models.py
   ├── index/
   │   ├── __init__.py
   │   ├── vector_store.py
   │   └── manager.py
   └── tools/
       └── indexing.py
   ```

2. 实现 EmbeddingEncoder
   - 加载 sentence-transformers 模型
   - 文本分块 (chunk_size=512)
   - 批量编码

3. 实现 VectorStore
   - FAISS 索引构建
   - 索引保存和加载
   - 向量搜索

4. 实现 build_semantic_index
   - 整合编码器和存储
   - 返回统计信息

5. 编写测试
   - 单元测试
   - 集成测试
   - 性能测试

---

### TASK-AI2: 语义搜索

**工期**: 3天  
**优先级**: P0  
**依赖**: TASK-AI1

**步骤**:
1. 实现 semantic_search
   - 加载索引
   - 查询编码
   - 相似度搜索
   - 结果排序

2. 添加过滤功能
   - 元数据过滤
   - 相似度阈值
   - Top-K限制

3. 编写测试
   - 搜索准确性测试
   - 性能测试
   - 边界情况测试

---

## 技术决策

### 模型选择
**当前**: `paraphrase-multilingual-MiniLM-L12-v2`
- 多语言支持
- 模型大小适中
- 嵌入维度: 384

**配置方式**:
```yaml
# config.yaml
embeddings:
  model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  cache_dir: .models
  max_seq_length: 512
```

### 向量库选择
**当前**: FAISS (CPU版本)
- 开源免费
- 性能优秀
- 易于部署

**索引类型**:
- IndexFlatIP (内积，精确搜索)
- IndexIVFFlat (倒排索引，近似搜索)

---

## 性能指标

| 指标 | 目标 | 测量方法 |
|------|------|---------|
| 索引构建 | 1000文档 < 30s | 时间测试 |
| 搜索延迟 | < 100ms | 延迟测试 |
| 内存使用 | < 500MB | 内存监控 |
| 准确率 | > 85% | 人工评估 |

---

## Status Update

**更新 `agent-status.md`**:
- 开始任务时
- 提交代码后
- 遇到阻塞时
- 完成任务后

---

## Troubleshooting

### 问题1: 模型下载慢
**解决**: 使用镜像或预下载模型
```bash
# 预下载模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('...')"
```

### 问题2: FAISS 安装失败
**解决**: 
```bash
# 使用conda
conda install -c conda-forge faiss-cpu

# 或使用pip
pip install faiss-cpu
```

### 问题3: 内存不足
**解决**:
- 减小batch_size
- 使用更小的模型
- 增量处理文档

---

**Remember**: 
- 专注于AI算法，不处理文件IO
- opencode提供文档数据，我们处理向量化
- 返回结构化结果，不做展示
- 通过Issue与PM Team沟通
