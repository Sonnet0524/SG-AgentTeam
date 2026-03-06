# Core Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06  
**Current Phase**: v1.1 Planning  
**Status**: 🟢 Ready to Start  

---

## Current Focus

**Primary Task**: 知识提取工具开发

**Immediate Actions**:
1. ⏳ 等待 Sprint 1 完成（AI Team的索引和搜索）
2. 📋 准备 Sprint 2 任务
   - TASK-C1: 知识提取工具
   - extract_keywords() 实现
   - generate_summary() 实现
3. 📝 编写单元测试

---

## Team Status

| Team | Status | Current Task |
|------|--------|--------------|
| Core Team | 🟢 Ready | Sprint 2 准备 |
| AI Team | 🔄 Active | Sprint 1 (索引+搜索) |
| Integration Team | 📋 Planned | Sprint 3 (集成) |

---

## 🎯 v1.1 Responsibilities

### 核心职责
- ✅ 类型系统 (已完成)
- ✅ 元数据解析 (已完成)
- ✅ 工具函数 (已完成)
- ✅ organize_notes (已完成)
- ✅ generate_index (已完成)
- ⏳ extract_keywords (Sprint 2)
- ⏳ generate_summary (Sprint 2)

### 不负责
- ❌ 向量嵌入 (AI Team)
- ❌ 语义搜索 (AI Team)
- ❌ 外部连接器 (Integration Team)

---

## 🚀 启动流程

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/core/CATCH_UP.md    # 本文件
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

### 3. 检查任务
- 查看 GitHub Issues (label: `team: core`)
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
- `agents/core/AGENTS.md` - Core Team配置

### Technical Docs
- `../knowledge-assistant/docs/api-reference.md` - API文档
- `../knowledge-assistant/docs/user-guide.md` - 用户指南

---

## Next Actions

### Sprint 2 (Week 3-4)
1. 实现 `extract_keywords()` 函数
   - TF-IDF 方法
   - TextRank 方法
   - 多语言支持

2. 实现 `generate_summary()` 函数
   - 抽取式摘要
   - 可配置长度

3. 编写单元测试
   - 覆盖率 > 85%
   - 测试多语言

---

## Status Update

**更新 `agent-status.md`**:
- 开始任务时
- 提交代码后
- 遇到阻塞时
- 完成任务后

---

**Remember**: 
- 只修改自己负责的模块
- 不涉及AI/ML算法
- 专注于数据处理和文本分析
- 通过Issue与PM Team沟通
