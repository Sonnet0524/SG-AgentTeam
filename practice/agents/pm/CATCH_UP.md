# PM Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-07 20:30  
**Current Phase**: v1.1 Sprint 2 Complete  
**Status**: 🟢 Active - Test Team运行集成测试中  

---

## Current Focus

**Primary Task**: 完成v1.1集成测试和发布

**Completed Actions**:
1. ✅ Sprint 1完成（AI Team + Test Team）
2. ✅ Sprint 2完成（Core Team + Integration Team）
   - Core Team: 关键词提取 + 摘要生成
   - Integration Team: 邮件连接器 + Skill/Agent配置
3. ✅ 发现并解决Core Team Sprint 2代码缺失问题
4. ✅ PM Team工作模式更新
   - 主动启动Agent + 不轮询 + 被动接收
   - 创建WORKFLOW.md文档

**Next Actions**:
1. 🔄 Test Team集成测试运行中（后台）
   - 任务文件: tasks/test-team-task.md
   - 报告文件: reports/test-report.md (待生成)
2. ⏳ 等待Test Team报告
3. ⏳ 准备v1.1发布（Issue #15）

---

## 今日工作总结 (2026-03-07)

### 主要成果

#### 1. Sprint 1 & 2 完成 ✅
- **Sprint 1**: AI Team语义索引和搜索 ✅
- **Sprint 2**: Core Team知识提取 + Integration Team集成 ✅

#### 2. 发现并解决问题 ✅
- Test Team集成测试发现Core Team代码缺失
- PM Team调查确认问题
- Core Team重新开发并完成
- PR #17已合并

#### 3. PM Team工作模式更新 ✅
**新工作模式**:
- ✅ 主动启动Agent
- ❌ 不轮询状态
- ✅ 被动接收报告

**新增文档**:
- WORKFLOW.md - Agent管理完整指南
- tasks/ - 任务文件目录
- reports/ - 报告文件目录
- logs/ - 日志文件目录

**Agent启动方法**:
```bash
opencode run --agent <name> "message" > logs/<team>.log 2>&1 &
```

#### 4. Test Team启动 ✅
- 任务文件: tasks/test-team-task.md
- 后台运行中
- 等待报告: reports/test-report.md

---

## Team Status

| Team | Status | Location | Current Task |
|------|--------|----------|--------------|
| PM Team | 🟢 Active | agents/pm/ | 等待Test Team报告 |
| Core Team | ✅ Complete | agents/core/ | Sprint 2完成 |
| AI Team | ✅ Complete | agents/ai/ | Sprint 1完成 |
| Integration Team | ✅ Complete | agents/integration/ | Sprint 2-3完成 |
| Test Team | 🔄 Running | agents/test/ | 集成测试运行中 |
| Research | 🔒 External | agents/research/ | 外部Agent，不受管控 |

---

## Project Context

### Repositories
- **Dev Repo**: `D:\opencode\knowledge-assistant-dev` (当前工作目录)
- **Main Repo**: `../knowledge-assistant` (代码仓库)

### v1.1 Architecture
```
opencode (Master Agent)
  ├── 文件操作 (own capability)
  ├── NLU & 理解 (own capability)
  └── 调用 knowledge-assistant tools
      ↓
knowledge-assistant (Tool Library)
  ├── AI Team: 语义索引+搜索
  ├── Core Team: 知识提取
  └── Integration Team: 连接器+集成
```

### v1.1 Sprint Plan
- **Sprint 1** (Week 1-2): AI Team - 索引+搜索 ✅ 完成
- **Sprint 2** (Week 3-4): Core Team + Integration Team - 提取+连接器 ✅ 完成
- **Sprint 3** (Week 5-6): Integration Team - 集成+发布 ✅ 开发完成，测试中

---

## 🚀 启动流程

**在dev仓库启动，操作main仓库时使用路径**

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/pm/CATCH_UP.md    # 本文件
practice/status/agent-status.md   # 团队状态
practice/status/human-admin.md    # 用户总览
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
- 检查 `status/task-assignments/v1.1-task-assignments.md`

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用工具的 `workdir` 参数

---

## Key Files to Reference

### Planning Documents
- `status/task-assignments/v1.1-task-assignments.md` - v1.1任务分配
- `../knowledge-assistant/docs/PRD.md` - 产品需求文档

### Team Status
- `status/agent-status.md` - All teams status tracking

### Team Configs
- `agents/pm/AGENTS.md` - PM Team config
- `agents/core/AGENTS.md` - Core Team config
- `agents/ai/AGENTS.md` - AI Team config
- `agents/integration/AGENTS.md` - Integration Team config
- `agents/test/AGENTS.md` - Test Team config

### Startup Scripts
- `start-pm.bat/sh` - PM Team启动
- `start-core.bat/sh` - Core Team启动
- `start-ai.bat/sh` - AI Team启动
- `start-integration.bat/sh` - Integration Team启动
- `start-test.bat/sh` - Test Team启动

---

## Pending Tasks

### High Priority
- [ ] 读取Test Team报告（等待生成）
  - reports/test-report.md

- [ ] 完成v1.1发布准备（Issue #15）
  - 准备Release Notes
  - 更新版本号
  - 创建发布文档

### Medium Priority
- [ ] 总结v1.1开发经验
- [ ] 更新项目文档

---

## Status Update

**更新 `agent-status.md`**:
- 用户询问后更新
- Agent报告问题后记录
- 任务分配后跟踪
- Review完成后记录

**工作模式**:
- ✅ **主动启动Agent** - 分配任务后立即启动
- ❌ **不轮询状态** - 不主动检查Agent进度
- ✅ **被动接收报告** - 等待Agent报告

**Agent启动方法**:
详见 `practice/agents/pm/WORKFLOW.md`

```bash
opencode run --agent <name> "message" > logs/<team>.log 2>&1 &
```

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `practice/agents/pm/CATCH_UP.md` |
| 核心指南 | `practice/agents/pm/ESSENTIALS.md` |
| **工作流程** | `practice/agents/pm/WORKFLOW.md` ⭐ |
| 团队状态 | `practice/status/agent-status.md` |
| 用户总览 | `practice/status/human-admin.md` |

---

## Important Notes

### Research Agent
- **状态**: 外部Agent，不受PM Team管控
- **权限**: PM Team不能修改Research Agent的任何内容
- **协作**: 向Research Team分享知识和经验

### Team结构变更流程
当Team结构变化时，必须同步更新：
1. opencode.json
2. practice/agents/{team}/AGENTS.md
3. practice/agents/{team}/CATCH_UP.md
4. start-{team}.bat 和 start-{team}.sh
5. agent-status.md 和 human-admin.md

---

**Remember**: 
- ✅ **主动启动Agent** - 分配任务后立即启动（opencode run）
- ❌ **不轮询状态** - 不主动检查Agent进度
- ✅ **被动接收报告** - Agent完成后读取报告
- ❌ **禁止使用task工具启动Team Agent** - task只能启动general/explore
- 在dev仓库启动和工作
- 操作main仓库时使用 `../knowledge-assistant` 或 `workdir` 参数
- 你是协调者，保持所有人同步
- v1.1核心：opencode集成，不重复opencode能力
- Research Agent是外部Agent，保持知识分享

---

**Last Updated**: 2026-03-07 20:30  
**Next Work**: 等待Test Team报告或用户指示
