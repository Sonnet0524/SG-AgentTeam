---
version: 2.0
last_update: 2026-03-06
agent: template
---

# Template Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 10:45  
**Status**: 🟢 Active  
**Current Task**: PR #22 已创建，等待审核  
**Progress**: ✅ 已完成干净PR创建

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
✅ PR #22 已创建（干净的模板PR）

**完成内容**:
- 创建新分支 `feature/templates-clean`
- 只包含 `templates/` 目录（5个md文件）
- 关闭旧 PR #17
- PR #22 等待 PM 审核

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
| PR #22 | 🟢 Open | 等待 PM 审核 |
| PR #17 | ✅ Closed | 已被 #22 替代 |
| Issue #14 | ✅ 完成 | 已关联到 #22 |

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/template/CATCH_UP.md  # 本文件
practice/status/agent-status.md       # 项目状态
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

### ✅ Completed
**创建新的干净PR** - 已完成

已执行的操作：
```bash
# 1. 在main仓库操作
cd ../knowledge-assistant

# 2. 创建新分支
git checkout main && git pull
git checkout -b feature/templates-clean

# 3. 只复制模板文件
git checkout origin/feature/a-document-templates -- templates/

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

### 🟡 Next (等待PM审核)
- 等待 PM 审核并合并 PR #22
- 准备下一阶段的模板引擎开发

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
| 启动文档 | `practice/agents/template/CATCH_UP.md` |
| 核心指南 | `practice/agents/template/ESSENTIALS.md` |
| 项目状态 | `practice/status/agent-status.md` |
| Main仓库 | `../knowledge-assistant/` |

---

**Remember**: 
- 在dev仓库启动和工作
- 只修改 `templates/` 目录
- 操作main仓库时使用 `../knowledge-assistant`
