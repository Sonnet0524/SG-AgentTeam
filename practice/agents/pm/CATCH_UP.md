# PM Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-06 17:00  
**Current Phase**: v1.1 Ready to Start  
**Status**: 🟢 Completed Planning  

---

## Current Focus

**Primary Task**: v1.1规划完成，准备启动开发

**Completed Actions**:
1. ✅ 完成v1.1整体规划
2. ✅ 更新PRD（反映opencode集成架构）
3. ✅ 完成团队结构调整
   - 新建：Core Team, AI Team, Integration Team
   - 更新：PM Team, Test Team
   - 归档：Data Team, Template Team
4. ✅ 创建所有配置文档
   - opencode.json
   - 所有Team的AGENTS.md和CATCH_UP.md
5. ✅ 创建启动脚本
   - start-core.bat/sh
   - start-ai.bat/sh
   - start-integration.bat/sh
6. ✅ 更新PM Team规则

**Next Actions**:
1. ⏳ 创建GitHub Issues（下个工作日）
2. ⏳ 启动Sprint 1（AI Team开始索引+搜索）
3. ⏳ 监控进度和处理问题

---

## 今日工作总结 (2026-03-06)

### 主要成果

#### 1. v1.1规划完成
- **PRD更新**: 明确了opencode主控 + knowledge-assistant工具库的架构
- **用户场景**: 分析了三个核心场景（构建知识库、语义检索、多源搜索）
- **任务分配**: 创建了详细的v1.1-task-assignments.md

#### 2. 团队结构调整
**调整原因**:
- Data Team职责过重（数据处理+AI算法）
- Template Team职责不匹配集成工作
- 需要专门的AI Team支持v1.1的语义搜索功能

**调整结果**:
```
v1.0:
- Data Team (已归档)
- Template Team (已归档)

v1.1:
- Core Team (数据处理)
- AI Team (向量嵌入+搜索) ← NEW
- Integration Team (opencode集成)
```

#### 3. 配置文档完善
- ✅ 所有Team的AGENTS.md（6个Team）
- ✅ 所有Team的CATCH_UP.md（6个Team）
- ✅ opencode.json更新
- ✅ 状态文档更新

#### 4. 启动脚本创建
- ✅ start-core.bat/sh
- ✅ start-ai.bat/sh
- ✅ start-integration.bat/sh
- ✅ 删除旧的start-data和start-template

#### 5. 规则完善
- ✅ PM Team规则更新
  - 增加启动脚本管理要求
  - 记录Team结构变更流程
  - 明确Research Agent为外部Agent

---

## Team Status

| Team | Status | Location | Current Task |
|------|--------|----------|--------------|
| PM Team | 🟢 Complete | agents/pm/ | 规划完成，准备启动 |
| Core Team | 🟢 Ready | agents/core/ | Sprint 2准备 |
| AI Team | 🟢 Ready | agents/ai/ | Sprint 1准备 |
| Integration Team | 📋 Planned | agents/integration/ | Sprint 2-3准备 |
| Test Team | 🟢 Ready | agents/test/ | 支持所有Sprint |
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
- **Sprint 1** (Week 1-2): AI Team - 索引+搜索
- **Sprint 2** (Week 3-4): Core Team + Integration Team - 提取+连接器
- **Sprint 3** (Week 5-6): Integration Team - 集成+发布

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

## Pending Tasks (Next Workday)

### High Priority
- [ ] 创建GitHub Issues
  - TASK-AI1: 语义索引构建
  - TASK-AI2: 语义搜索工具
  - TASK-TE1, TE2: 测试
  - 设置labels和milestone

- [ ] 通知AI Team开始Sprint 1
  - 确认依赖安装
  - 启动开发

- [ ] 监控Sprint 1进度
  - 每周更新agent-status.md
  - 处理阻塞问题

### Medium Priority
- [ ] 完善开发文档
- [ ] 设置里程碑追踪

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
| 启动文档 | `practice/agents/pm/CATCH_UP.md` |
| 核心指南 | `practice/agents/pm/ESSENTIALS.md` |
| 团队状态 | `practice/status/agent-status.md` |
| 用户总览 | `practice/status/human-admin.md` |
| 任务分配 | `practice/status/task-assignments/v1.1-task-assignments.md` |
| Main仓库 | `../knowledge-assistant/` |

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
- 在dev仓库启动和工作
- 操作main仓库时使用 `../knowledge-assistant` 或 `workdir` 参数
- 你是协调者，保持所有人同步
- v1.1核心：opencode集成，不重复opencode能力
- Research Agent是外部Agent，保持知识分享

---

**下班时间**: 2026-03-06 17:00  
**下次工作**: 创建GitHub Issues，启动v1.1 Sprint 1
