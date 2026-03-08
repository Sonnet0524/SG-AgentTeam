# Migration Agent 使用指南

## 📋 任务概述

Migration Agent将帮你完成多仓库架构调整，建立清晰的四层协作体系。

## 🎯 目标架构

```
Layer 0: SEARCH-R（方法论框架）
    └─ Research Agent实例：研究方法论本身

Layer 1: agent-team-research（课题仓库）【新建】
    └─ Research Agent实例：研究Agent Team课题

Layer 2: AgentTeam-Template（模板仓库）
    └─ PM Agent：维护可复用模板

Layer 3: knowledge-assistant-dev, WPS（实践仓库）
    └─ 具体Team：执行实际项目
```

## 🚀 启动Migration Agent

### 方法1：使用启动脚本（推荐）

```bash
cd /Users/sonnet/opencode/knowledge-assistant-dev
./start-migration.sh
```

### 方法2：直接使用opencode

```bash
cd /Users/sonnet/opencode/knowledge-assistant-dev
opencode run --agent migration
```

## 📝 Migration Agent工作方式

### 执行模式

Migration Agent将：
1. **逐步执行**：按照Phase 1到Phase 10的顺序执行
2. **汇报进度**：每完成一个Phase向你汇报
3. **等待确认**：关键操作会等待你的确认
4. **记录日志**：所有操作记录到日志文件

### 交互方式

```
Migration Agent: "Phase 1准备阶段完成，发现以下情况..."
Migration Agent: "是否继续Phase 2创建L1仓库？"
User: "继续"
Migration Agent: "开始Phase 2..."
```

## ⚠️ 重要提醒

### 执行前

1. **检查Git状态**：
   ```bash
   cd /Users/sonnet/opencode/knowledge-assistant-dev
   git status
   ```
   确保工作目录干净或了解未提交的内容

2. **了解任务**：
   - 阅读agents/migration/AGENTS.md了解详细任务
   - 了解将要创建和修改的内容

3. **准备时间**：
   - 预计需要1-2小时
   - 确保有足够时间完成或中途可以暂停

### 执行中

1. **关键操作确认**：
   - Migration Agent会在关键操作前询问
   - 可以选择继续、跳过或取消

2. **随时暂停**：
   - 可以随时要求暂停
   - Migration Agent会记录进度，下次继续

3. **观察日志**：
   - 所有操作记录到migration-log.md
   - 可以查看当前进度

### 执行后

1. **验证结果**：
   - Migration Agent会生成完成报告
   - 检查各仓库是否按预期调整

2. **推送到远程**：
   - 确认无误后推送到GitHub
   - 特别是新建的agent-team-research仓库

3. **清理临时文件**：
   - Migration Agent会自动清理
   - 如有遗漏，手动清理/tmp目录

## 📊 预期成果

### 新建的仓库

**agent-team-research/**
```
├── framework/
│   ├── methodology/ (Submodule: SEARCH-R)
│   ├── dependencies.yaml
│   ├── sync-status.yaml
│   └── skills/sync/
├── agents/research/
│   ├── AGENTS.md
│   ├── CATCH_UP.md
│   └── session-log.md
├── theory/
├── practice-feedback/
├── notifications/
└── opencode.json
```

### 调整的仓库

**SEARCH-R/**
- 添加research-instances/目录
- 调整AGENTS.md（明确L0职责）

**AgentTeam-Template/**
- 添加framework/notifications/
- 添加framework/skills/sync/
- 添加theory-references/
- 添加dependencies.yaml和sync-status.yaml

**knowledge-assistant-dev/**
- 添加framework/dependencies.yaml和sync-status.yaml
- 添加archive/feedback/
- 删除docs/research/（迁移到L1）
- 删除agents/research/（迁移到L1）
- 更新opencode.json

## 🔄 后续任务

Migration Agent完成后：

1. **启动L1 Research Agent**：
   ```bash
   cd /Users/sonnet/opencode/agent-team-research
   opencode run --agent research
   ```

2. **推送新仓库到GitHub**：
   ```bash
   cd /Users/sonnet/opencode/agent-team-research
   git remote add origin git@github.com:Sonnet0524/agent-team-research.git
   git push -u origin main
   ```

3. **更新其他项目**：
   - 将WPS项目也添加到依赖配置
   - 配置实践项目的反馈机制

## 🆘 故障排除

### 问题1：Git状态不干净

**解决**：
```bash
# 提交或暂存变更
git add .
git commit -m "WIP"

# 或暂存
git stash
```

### 问题2：Submodule添加失败

**解决**：
```bash
# 检查SSH密钥
ssh -T git@github.com

# 检查Git版本（需要2.13+）
git --version
```

### 问题3：Migration Agent中断

**解决**：
- Migration Agent会记录进度到CATCH_UP.md
- 重新启动会询问从哪里继续

### 问题4：需要回滚

**解决**：
- Migration Agent会生成rollback-guide.md
- 按照指南逐步回滚

## 📞 联系

如有问题，可以：
1. 查看Migration Agent的日志
2. 查看AGENTS.md中的详细说明
3. 暂停执行，向Migration Agent询问

---

**准备好开始了吗？运行 `./start-migration.sh` 启动Migration Agent！**
