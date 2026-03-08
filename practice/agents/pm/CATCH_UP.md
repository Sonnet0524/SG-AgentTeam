# PM Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-08 (v1.2.0 Released 🎉)  
**Current Phase**: v1.2 Complete - Ready for v1.3  
**Status**: 🟢 Idle - 无正在进行的任务  
**Version**: v1.2.0

---

## Current Focus

**Primary Task**: 无 - v1.2.0 已发布，等待用户指示

---

## 🎉 v1.2.0 发布完成 (2026-03-08)

### 发布链接

**GitHub Release**: https://github.com/Sonnet0524/knowledge-assistant/releases/tag/v1.2.0

### 完成的功能

| 功能 | Team | 测试 |
|------|------|------|
| 性能优化 (10x scale) | AI Team | ✅ |
| Connector Framework | Core Team | ✅ 134 tests |
| Calendar Connector | Core Team | ✅ 31 tests |
| Notes Connector | Core Team | ✅ 30 tests |
| Abstractive Summarization | Core Team | ✅ 50 tests |
| Multi-language Support | Core Team | ✅ 33 tests |
| Web UI API | Integration Team | ✅ 4 tests |
| Web UI | Integration Team | ✅ |

### 质量指标

| 指标 | 数值 | 目标 |
|------|------|------|
| 测试通过 | 269/269 (100%) | ✅ |
| 代码覆盖率 | 91% | ✅ |
| 搜索延迟 | ~85ms | ✅ |
| 内存使用 | ~350MB | ✅ |

### Issues 状态

**全部关闭**: 16/16 Issues (#37-#52)

---

## 下一步建议

### v1.3 规划方向

1. **更多连接器**: Slack, GitHub, Jira
2. **高级 NLP**: 实体提取、关系抽取
3. **知识图谱可视化**: Web UI 增强
4. **插件系统**: 可扩展架构

### 待处理

- [ ] 总结 v1.2 开发经验
- [ ] 清理 reports/ 目录
- [ ] 规划 v1.3 任务

---

## 今日工作总结 (2026-03-08)

### 完成的工作

1. ✅ v1.1.0 发布完成
   - 语义搜索、关键词提取、摘要生成
   - GitHub Release v1.1.0

2. ✅ v1.2 开发完成
   - 并行启动 3 个 Agent
   - Core Team: Connector Framework, Calendar, Notes, Abstractive Summary, Multi-language
   - AI Team: Performance Optimization
   - Integration Team: Web UI API, Web UI

3. ✅ 测试通过
   - 269/269 tests passed
   - 91% code coverage

4. ✅ v1.2.0 发布
   - RELEASE_NOTES.md 更新
   - README.md 更新
   - GitHub Release 创建
   - Tag v1.2.0 推送

5. ✅ 经验文档
   - 创建 parallel-agent-launch-20260308.md
   - 记录并行启动 Agent 的方法

---

## 📁 关键文件位置

### 状态文档
- `practice/status/agent-status.md` - Team 状态
- `practice/status/human-admin.md` - 用户总览

### 任务文件
- `tasks/` - 任务分配文件
- `reports/` - 完成报告
- `archive/v1.1/` - v1.1 归档

### 经验文档
- `practice/agents/pm/experiences/` - PM Team 经验

### 工作流程
- `practice/agents/pm/WORKFLOW.md` - Agent 管理流程
- `practice/agents/pm/ESSENTIALS.md` - 核心指南

---

## Team Status

| Team | Status | Location | Last Task |
|------|--------|----------|-----------|
| PM Team | 🟢 Idle | agents/pm/ | v1.2 发布完成 |
| Core Team | ✅ Complete | agents/core/ | Sprint 2 完成 |
| AI Team | ✅ Complete | agents/ai/ | Sprint 1 完成 |
| Integration Team | ✅ Complete | agents/integration/ | Sprint 3 完成 |
| Test Team | ✅ Complete | agents/test/ | 集成测试完成 |

---

## 多仓库操作指南

### 启动位置
```
始终在 dev 仓库启动和工作
```

### 操作 main 仓库
```bash
# 方法1: 相对路径
cd ../knowledge-assistant

# 方法2: workdir 参数
<command> --workdir=../knowledge-assistant
```

### 同步仓库
```bash
# 同步 dev 仓库
git pull origin main

# 同步 main 仓库
cd ../knowledge-assistant && git pull origin main
```

---

## Agent 启动方式

### 核心命令
```bash
opencode run --agent <name> "任务描述" > logs/<team>.log 2>&1 &
```

### 任务文件方式（推荐）
```bash
# 1. 创建任务文件
cat > tasks/<team>-task.md << 'EOF'
# 任务标题
## 任务背景
...
## 输出要求
完成后写入 reports/<team>-report.md
EOF

# 2. 启动 Agent
opencode run --agent <name> "请读取 tasks/<team>-task.md 并完成，结果写入 reports/<team>-report.md" > logs/<team>.log 2>&1 &
```

### 权限配置要求
```json
{
  "permission": {
    "edit": "allow"  // 非交互模式必须为 allow
  }
}
```

详见: `practice/agents/pm/experiences/parallel-agent-launch-20260308.md`

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `practice/agents/pm/CATCH_UP.md` (本文件) |
| 核心指南 | `practice/agents/pm/ESSENTIALS.md` |
| 工作流程 | `practice/agents/pm/WORKFLOW.md` |
| 团队状态 | `practice/status/agent-status.md` |
| 用户总览 | `practice/status/human-admin.md` |
| 经验文档 | `practice/agents/pm/experiences/` |

---

## Important Notes

### 工作模式
- ✅ **主动启动Agent** - 分配任务后立即启动
- ❌ **不轮询状态** - 不主动检查Agent进度
- ✅ **被动接收报告** - Agent完成后读取报告
- ❌ **禁止使用task工具启动Team Agent** - task只能启动general/explore

### 仓库操作
- 在 dev 仓库启动和工作
- 操作 main 仓库时使用 `../knowledge-assistant` 或 `workdir` 参数

### Research Agent
- 外部Agent，不受PM Team管控
- 保持知识分享

---

**Last Updated**: 2026-03-08 23:35  
**Next Work**: 等待用户指示 (v1.3规划 / 经验总结 / 其他)  
**Status**: 🟢 Ready for next task
- 执行时间: 8.88s

**Sprint 2验证**:
- ✅ Issue #8: extract_keywords() 已实现并通过测试
- ✅ Issue #9: generate_summary() 已实现并通过测试
- ✅ PR #17: 已合并到 main 分支
- ✅ 所有性能指标达标

**发布建议**: ✅ **建议发布 v1.1**

**报告位置**: `reports/test-report.md`

---

## Team Status

| Team | Status | Location | Current Task |
|------|--------|----------|--------------|
| PM Team | 🟢 Active | agents/pm/ | 准备v1.1发布 |
| Core Team | ✅ Complete | agents/core/ | Sprint 2完成 |
| AI Team | ✅ Complete | agents/ai/ | Sprint 1完成 |
| Integration Team | ✅ Complete | agents/integration/ | Sprint 2-3完成 |
| Test Team | ✅ Complete | agents/test/ | 集成测试完成 |
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
- [x] 读取Test Team报告 ✅
  - reports/test-report.md - 已读取
  - 测试通过率: 91.7%
  - 发布建议: ✅ 建议发布 v1.1

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

**Last Updated**: 2026-03-07 21:00  
**Next Work**: 准备v1.1发布（Issue #15）
