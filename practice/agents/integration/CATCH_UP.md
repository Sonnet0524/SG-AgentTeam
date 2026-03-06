# Integration Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06  
**Current Phase**: v1.1 Planning  
**Status**: 📋 Ready to Start  

---

## Current Focus

**Primary Task**: opencode集成和连接器开发

**Immediate Actions**:
1. ⏳ 等待 Sprint 2 开始
2. 📋 准备 Sprint 2 任务
   - TASK-INT1: 邮箱连接器
3. 📋 准备 Sprint 3 任务
   - TASK-INT2: Skill定义
   - TASK-INT3: Agent配置
4. 📚 学习opencode能力

---

## Team Status

| Team | Status | Current Task |
|------|--------|--------------|
| Integration Team | 📋 Ready | Sprint 2-3 准备 |
| AI Team | 🚀 Active | Sprint 1 (索引+搜索) |
| Core Team | 🟢 Ready | Sprint 2 准备 |

---

## 🎯 v1.1 Responsibilities

### 核心职责
- ⏳ 邮箱连接器 (Sprint 2)
- ⏳ Skill定义 (Sprint 3)
- ⏳ Agent配置 (Sprint 3)
- 📋 集成文档 (Sprint 3)

### 不负责
- ❌ 向量嵌入 (AI Team)
- ❌ 语义搜索 (AI Team)
- ❌ 数据处理 (Core Team)

---

## 🚀 启动流程

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/integration/CATCH_UP.md    # 本文件
practice/status/agent-status.md            # 团队状态
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

### 3. 检查任务
- 查看 GitHub Issues (label: `team: integration`)
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
- `agents/integration/AGENTS.md` - Integration Team配置

### Integration Docs
- `skills/knowledge-assistant/SKILL.md` - Skill定义 (待创建)
- `AGENT.md` - Agent配置 (待创建)

---

## Sprint 2 Tasks (Week 3-4)

### TASK-INT1: 邮箱连接器

**工期**: 3天  
**优先级**: P1  

**步骤**:
1. 创建目录结构
   ```
   scripts/connectors/
   ├── __init__.py
   ├── base.py
   └── email.py
   ```

2. 实现BaseConnector抽象类
   - connect() 抽象方法
   - disconnect() 抽象方法
   - search() 抽象方法

3. 实现EmailConnector
   - IMAP连接
   - 邮件搜索
   - 邮件读取
   - 结构化返回

4. 编写测试
   - 连接测试
   - 搜索测试
   - 错误处理测试

5. 编写文档
   - 使用说明
   - 配置指南
   - 示例代码

---

## Sprint 3 Tasks (Week 5-6)

### TASK-INT2: Skill定义

**工期**: 3天  
**优先级**: P0  

**步骤**:
1. 分析用户场景
   - 构建知识库
   - 搜索文档
   - 提取知识
   - 多源检索

2. 设计触发模式
   - 自然语言短语
   - 意图识别
   - 参数提取

3. 定义工具调用
   - build_semantic_index
   - semantic_search
   - extract_keywords
   - EmailConnector

4. 编写示例
   - 完整交互流程
   - 错误处理
   - 最佳实践

---

### TASK-INT3: Agent配置

**工期**: 2天  
**优先级**: P0  

**步骤**:
1. 定义Agent能力
   - 知识库管理
   - 语义搜索
   - 知识提取
   - 多源集成

2. 创建意图映射
   - 意图识别规则
   - 工具选择逻辑
   - 参数传递

3. 描述工作流
   - 初始化流程
   - 搜索流程
   - 更新流程

4. 配置说明
   - 依赖安装
   - 配置文件
   - 首次使用

---

## Skill设计要点

### 1. 触发词设计
```
用户语言 → 意图识别 → 工具调用

示例：
"find documents about Python" → search_documents → semantic_search()
"build knowledge base from ./notes" → build_kb → build_semantic_index()
"search emails for budget" → search_emails → EmailConnector.search_emails()
```

### 2. 工具调用约定
```python
# opencode调用knowledge-assistant工具
from scripts.tools.search import semantic_search

# opencode提供参数
results = semantic_search(
    query="Python async programming",
    index_path=".ka-index",
    top_k=5
)

# 返回结构化数据给opencode
return {
    "type": "search_results",
    "results": [...],
    "metadata": {...}
}
```

### 3. 错误处理
```yaml
error_handling:
  index_not_found:
    message: "Knowledge base not found. Please build index first."
    action: "Ask user to build knowledge base"
  
  email_not_configured:
    message: "Email not configured. Would you like to configure now?"
    action: "Guide user through email setup"
```

---

## opencode能力理解

### opencode自身能力
- ✅ 文件扫描和读取
- ✅ 自然语言理解
- ✅ 意图分析
- ✅ 结果展示
- ✅ 用户交互

### knowledge-assistant提供
- ✅ 语义索引算法
- ✅ 向量搜索算法
- ✅ 知识提取算法
- ✅ 外部连接器

### 集成原则
```
opencode: "我来扫描文件和读取内容"
knowledge-assistant: "我来处理向量化"
opencode: "我来展示结果"

opencode: "我理解用户想搜索Python文档"
knowledge-assistant: "我来做语义搜索"
opencode: "我来读取并展示文档"
```

---

## Status Update

**更新 `agent-status.md`**:
- 开始任务时
- 提交代码后
- 遇到阻塞时
- 完成任务后

---

## Next Steps

### 本周
1. 学习opencode能力和限制
2. 设计Skill触发模式
3. 规划Agent配置结构

### Sprint 2
1. 实现邮箱连接器
2. 测试连接器功能
3. 编写使用文档

### Sprint 3
1. 完成Skill定义
2. 完成Agent配置
3. 编写集成文档
4. v1.1发布准备

---

**Remember**: 
- 专注于opencode集成，不处理算法
- 返回结构化数据，不做展示
- 理解opencode能力边界
- 通过Issue与PM Team沟通
