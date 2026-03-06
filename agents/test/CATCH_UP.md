---
version: 2.0
last_update: 2026-03-06
agent: test
---

# Test Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 11:16  
**Status**: ✅ Completed  
**Current Task**: M5 测试框架已完成，覆盖率 96%  
**Progress**: 等待新模块提交测试

---

## Who You Are

**Role**: Test & Quality Assurance Engineer  
**Team**: Test Team (`agents/test/`)  
**Expertise**: 测试框架、质量保证、代码审查、文档审核

---

## Current Phase

**Phase**: Sprint 1 - Phase 4 (New Features)  
**Sprint Day**: 2/14

### Current Task
✅ PR #18 已合并，测试框架完成

**待命任务**:
- 等待 Template Team 完成 #23, #24
- 等待 Data Team 完成 #25-27
- 为新功能补充测试

---

## Module Boundaries

### ✅ You Own
```
tests/
├── conftest.py            # 测试配置和fixtures
├── test_*.py              # 测试文件
├── reports/               # 测试报告
└── fixtures/              # 测试固件

test-data/
├── examples/              # 示例文档
└── fixtures/              # 测试数据
```

### ❌ You Do NOT Own
- 所有开发代码 (`scripts/`, `templates/`)
- 只能测试和报告，不能修改开发代码

---

## Active PRs & Issues

| Item | Status | Action Needed |
|------|--------|---------------|
| PR #18 | ✅ 已合并 | 测试框架完成 |
| Issue #16 | ✅ 完成 | PR #18 已实现 |
| Issue #23 | 🔍 监控 | Template Team - 模板引擎 |
| Issue #24 | 🔍 监控 | Template Team - 配置系统 |
| Issue #25 | 🔍 监控 | Data Team - 笔记整理工具 |
| Issue #26 | 🔍 监控 | Data Team - 索引生成工具 |
| Issue #27 | 🔍 监控 | Data Team - 关键词提取工具 |

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
agents/test/CATCH_UP.md     # 本文件
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
- 查看GitHub Issues（label: `team: test`）
- 检查 `agent-status.md` 中的状态

---

## Next Actions

### 🟢 Immediate (现在)
**Rebase PR #18 到最新 main**

```bash
# 1. 在main仓库操作
cd ../knowledge-assistant

# 2. 切换到feature分支
git checkout test/integration-framework

# 3. Rebase
git fetch origin
git rebase origin/main

# 4. 推送
git push -f origin test/integration-framework

# 5. 确认PR状态
gh pr view 18

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

## Status Update

**更新 `agent-status.md`**:
```markdown
### Test Team
| Field | Value |
|-------|-------|
| Status | 🟢 Ready to Merge |
| Current Task | PR #18 rebased, waiting for merge |
| Last Activity | YYYY-MM-DD HH:MM |
```

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `agents/test/CATCH_UP.md` |
| 核心指南 | `agents/test/ESSENTIALS.md` |
| 项目状态 | `agent-status.md` |
| Main仓库 | `../knowledge-assistant/` |

---

**Remember**: 
- 在dev仓库启动和工作
- 只创建测试文件和报告
- 操作main仓库时使用 `../knowledge-assistant`
