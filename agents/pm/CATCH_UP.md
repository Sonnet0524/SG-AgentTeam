# PM Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 02:30  
**Current Phase**: Sprint 1 - PR Integration  
**Status**: 🟢 Active  

---

## Current Focus

**Primary Task**: PR Review & Integration Management

**Immediate Actions**:
1. ✅ Fixed lint configuration issues (PR #21 merged)
2. ✅ Reviewed all 3 PRs (#17, #18, #19)
3. ⏳ **Handle PR integration** ⭐ Current Focus
   - PR #17: Template Team - needs revision (contains Data Team's files)
   - PR #18: Test Team - approved, needs rebase
   - PR #19: Data Team - approved, needs rebase
4. Guide PR integration and merge sequence
5. Update project documentation

---

## Team Status

| Team | Status | Current Task | PR Status |
|------|--------|--------------|-----------|
| Template Team | 🟡 Revision Needed | PR #17 needs clean version | Contains wrong files |
| Data Team | 🟢 Approved | PR #19 ready after rebase | Utils implementation ✅ |
| Test Team | 🟢 Approved | PR #18 ready after rebase | Test framework ✅ |

**Action Needed**: Guide PR integration and resolve conflicts

---

## Project Context

### Repositories
- **Dev Repo**: `D:\opencode\knowledge-assistant-dev` (当前工作目录)
- **Main Repo**: `../knowledge-assistant` (代码仓库)

### Current Sprint
- **Sprint**: Sprint 1 (Mar 5-20, 2026)
- **Goal**: Metadata + Template systems foundation
- **Day**: 2/14

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
agents/pm/CATCH_UP.md       # 本文件
agent-status.md             # 团队状态
HUMAN_ADMIN.md              # 用户总览
```

### 2. 同步代码仓库
```bash
# 同步dev仓库
git pull origin main

# 同步main仓库（使用相对路径）
cd ../knowledge-assistant
git pull origin main
cd ../knowledge-assistant-dev
```

### 3. 确认当前任务
- 检查本文件中的"Current Focus"
- 检查 `agent-status.md` 中各Team状态
- 检查PR状态

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用工具的 `workdir` 参数

---

## Key Files to Reference

### Planning Documents
- `project-management/sprint-1.md` - Current sprint plan
- `project-management/roadmap.md` - Overall timeline
- `project-management/milestones.md` - Milestone definitions

### Team Status
- `agent-status.md` - All teams status tracking

### Team Configs
- `agents/pm/AGENTS.md` - PM Team config
- `agents/template/AGENTS.md` - Template Team config
- `agents/data/AGENTS.md` - Data Team config
- `agents/test/AGENTS.md` - Test Team config

---

## Pending Tasks

### High Priority
- [ ] Guide PR integration and merge sequence ⏳ In progress
- [ ] Handle PR #17 revision issue ⚠️ Critical
- [ ] Merge PR #18 and #19 after teams complete rebase

### Medium Priority
- [ ] Create development standards docs
- [ ] Setup review checklists

---

## Next Steps

1. **通知各Team执行任务** ✅ task-assignments 已创建
2. **监控Team进度** ⏳ 当前任务
   - Data Team: rebase PR #19
   - Test Team: rebase PR #18
   - Template Team: 创建新PR
3. **Review新PR** 当Template Team提交
4. **Merge PRs** 按顺序合并

---

## Status Update

**更新 `agent-status.md`**:
- 每次操作后更新
- 记录重要决策
- 跟踪Team状态

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `agents/pm/CATCH_UP.md` |
| 核心指南 | `agents/pm/ESSENTIALS.md` |
| 团队状态 | `agent-status.md` |
| 用户总览 | `HUMAN_ADMIN.md` |
| Main仓库 | `../knowledge-assistant/` |

---

**Remember**: 
- 在dev仓库启动和工作
- 操作main仓库时使用 `../knowledge-assistant` 或 `workdir` 参数
- 你是协调者，保持所有人同步
