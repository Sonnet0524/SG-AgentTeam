---
version: 2.0
last_update: 2026-03-06
agent: template
---

# Template Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 02:30  
**Status**: 🟡 Revision Needed  
**Current Task**: PR #17 需要修正 - 创建只包含templates/的新PR  
**Progress**: 等待创建新PR

---

## Who You Are

**Role**: Template System Developer  
**Team**: Template Team (`agents/template/`)  
**Expertise**: 文档模板、配置管理、模板引擎

---

## Current Phase

**Phase**: Sprint 1 - PR Integration  
**Sprint Day**: 2/14

### Current Task
⚠️ PR #17 存在问题，需要创建新的干净PR

**问题**: PR #17 包含了 Data Team 的模块 (`scripts/utils.py`)
**解决**: 创建新PR，只包含 `templates/` 目录

---

## Module Boundaries

### ✅ You Own
```
templates/                  # 模板文件
├── daily-note.md
├── research-note.md
├── meeting-minutes.md
├── task-list.md
└── knowledge-card.md
```

### ❌ You Do NOT Own (Data Team's Modules)
```
scripts/
├── types.py               # Data Team
├── utils.py               # Data Team
├── metadata_parser.py     # Data Team
```

---

## Active PRs & Issues

| Item | Status | Action Needed |
|------|--------|---------------|
| PR #17 | 🔴 需重做 | 创建新PR（只含templates/） |
| Issue #14 | 🟡 进行中 | 关联到新PR |

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
agents/template/CATCH_UP.md  # 本文件
agent-status.md              # 项目状态
```

### 2. 同步代码仓库
```bash
# 在main仓库拉取最新代码（使用相对路径）
cd ../knowledge-assistant
git pull origin main
cd ../knowledge-assistant-dev
```

### 3. 检查分配的任务
- 查看GitHub Issues（label: `team: template`）
- 检查 `agent-status.md` 中的状态

---

## Next Actions

### 🔴 Immediate (现在)
**创建新的干净PR**

```bash
# 1. 在main仓库操作
cd ../knowledge-assistant

# 2. 创建新分支
git checkout main && git pull
git checkout -b feature/templates-clean

# 3. 只复制模板文件
git checkout feature/a-document-templates -- templates/

# 4. 提交
git add templates/
git commit -m "feat(template): create 5 document templates - Closes #14"

# 5. 推送并创建PR
git push -u origin feature/templates-clean
gh pr create --title "feat(template): create 5 document templates" --body "..."

# 6. 关闭旧PR
gh pr close 17 --comment "Superseded by clean PR"

# 7. 返回dev仓库更新状态
cd ../knowledge-assistant-dev
```

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用绝对路径访问

---

## Status Update

**更新 `agent-status.md`**:
```markdown
### Template Team
| Field | Value |
|-------|-------|
| Status | 🟢 Active / 🟡 Idle |
| Current Task | [当前任务] |
| Last Activity | YYYY-MM-DD HH:MM |
```

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `agents/template/CATCH_UP.md` |
| 核心指南 | `agents/template/ESSENTIALS.md` |
| 项目状态 | `agent-status.md` |
| Main仓库 | `../knowledge-assistant/` |

---

**Remember**: 
- 在dev仓库启动和工作
- 只修改 `templates/` 目录
- 操作main仓库时使用 `../knowledge-assistant`
