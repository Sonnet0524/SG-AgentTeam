---
version: 2.0
last_update: 2026-03-06
agent: data
---

# Data Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 02:30  
**Status**: 🟢 Ready to Merge  
**Current Task**: PR #19 已批准，需要 rebase 到最新 main  
**Progress**: 等待 rebase 后合并

---

## Who You Are

**Role**: Data System Developer  
**Team**: Data Team (`agents/data/`)  
**Expertise**: 元数据解析、数据验证、工具函数、算法实现

---

## Current Phase

**Phase**: Sprint 1 - PR Integration  
**Sprint Day**: 2/14

### Current Task
✅ PR #19 已通过审查，准备合并

**需要操作**: Rebase 到最新 main 分支

---

## Module Boundaries

### ✅ You Own
```
scripts/
├── types.py               # 类型定义
├── metadata_parser.py     # 元数据解析器
├── utils.py               # 工具函数
└── tools/                 # 工具脚本
    ├── organize_notes.py
    ├── generate_index.py
    └── extract_keywords.py
```

### ❌ You Do NOT Own (Template Team's Modules)
```
templates/                 # Template Team
scripts/
├── template_engine.py     # Template Team (未来)
├── config.py              # Template Team (未来)
```

---

## Active PRs & Issues

| Item | Status | Action Needed |
|------|--------|---------------|
| PR #19 | 🟢 待合并 | Rebase到最新main后可合并 |
| Issue #15 | ✅ 完成 | PR #19 已实现 |

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
agents/data/CATCH_UP.md     # 本文件
agent-status.md             # 项目状态
```

### 2. 同步代码仓库
```bash
# 在main仓库拉取最新代码（使用相对路径）
cd ../knowledge-assistant
git pull origin main
cd ../knowledge-assistant-dev
```

### 3. 检查分配的任务
- 查看GitHub Issues（label: `team: data`）
- 检查 `agent-status.md` 中的状态

---

## Next Actions

### 🟢 Immediate (现在)
**Rebase PR #19 到最新 main**

```bash
# 1. 在main仓库操作
cd ../knowledge-assistant

# 2. 切换到feature分支
git checkout feature/b-utils-c

# 3. Rebase
git fetch origin
git rebase origin/main

# 4. 推送
git push -f origin feature/b-utils-c

# 5. 确认PR状态
gh pr view 19

# 6. 返回dev仓库更新状态
cd ../knowledge-assistant-dev
```

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用绝对路径访问

---

## Public APIs You Provide

```python
# 其他Team可以导入使用
from scripts.types import DocumentMetadata, Document
from scripts.metadata_parser import MetadataParser
from scripts.utils import read_file, write_file, ensure_directory
```

---

## Status Update

**更新 `agent-status.md`**:
```markdown
### Data Team
| Field | Value |
|-------|-------|
| Status | 🟢 Ready to Merge |
| Current Task | PR #19 rebased, waiting for merge |
| Last Activity | YYYY-MM-DD HH:MM |
```

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `agents/data/CATCH_UP.md` |
| 核心指南 | `agents/data/ESSENTIALS.md` |
| 项目状态 | `agent-status.md` |
| Main仓库 | `../knowledge-assistant/` |

---

**Remember**: 
- 在dev仓库启动和工作
- 只修改 `scripts/types.py`, `scripts/utils.py`, `scripts/metadata_parser.py`
- 操作main仓库时使用 `../knowledge-assistant`
