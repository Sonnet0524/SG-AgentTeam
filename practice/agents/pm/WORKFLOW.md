# PM Team - Agent管理工作流程

> 📖 **核心文档** - PM Team如何启动和管理其他Agent

---

## 🎯 核心理念

**主动启动 + 不轮询 + 被动接收**

### 三大原则

1. ✅ **主动启动Agent** - 分配任务后立即启动
2. ❌ **不轮询状态** - 不主动检查Agent进度
3. ✅ **被动接收报告** - Agent完成后自动报告

---

## 📋 工作流程

### 完整流程图

```
用户询问/指示
     ↓
PM Team分析任务
     ↓
创建任务文件 (tasks/<team>-task.md)
     ↓
启动Agent (opencode run --agent <name>)
     ↓
Agent后台执行（不等待）
     ↓
PM Team继续其他工作
     ↓
Agent完成后写入报告 (reports/<team>-report.md)
     ↓
PM Team读取报告（被动触发）
     ↓
处理结果，继续下一步
```

---

## 🚀 Agent启动方法

### 方法1：直接启动（简单任务）

```bash
opencode run --agent <name> "任务描述" > logs/<team>.log 2>&1 &
```

**适用场景**: 简单、一次性任务

### 方法2：文件传递任务（推荐）

```bash
# 1. 创建任务文件
mkdir -p tasks reports logs

cat > tasks/test-task.md << 'EOF'
# 任务标题

## 任务背景
...

## 具体要求
...

## 输出要求
完成后在 reports/test-report.md 写入报告
EOF

# 2. 启动Agent
opencode run --agent test "请读取 tasks/test-task.md 中的任务并完成，结果写入 reports/test-report.md" > logs/test.log 2>&1 &
```

**适用场景**: 复杂、多步骤任务

---

## 📂 目录结构

```
SG-AgentTeam/
├── tasks/              # 任务文件
│   ├── core-task.md
│   ├── test-task.md
│   └── ai-task.md
├── reports/            # 报告文件
│   ├── core-report.md
│   ├── test-report.md
│   └── ai-report.md
├── logs/               # 日志文件
│   ├── core.log
│   ├── test.log
│   └── ai.log
└── practice/
    └── agents/
        └── pm/
            └── WORKFLOW.md  # 本文件
```

---

## 📝 任务文件模板

### 模板结构

```markdown
# <Team>任务：<任务标题>

## 📋 任务背景
为什么需要这个任务？

## 🎯 具体任务
1. 步骤1
2. 步骤2
3. 步骤3

## 📁 相关文件
- 文件路径1
- 文件路径2

## ⚠️ 注意事项
- 重要提醒1
- 重要提醒2

## 📤 输出要求
完成后在 `reports/<team>-report.md` 写入报告，包含：
1. 结果1
2. 结果2
3. 遇到的问题

---
**创建者**: PM Team
**创建时间**: YYYY-MM-DD HH:MM
**优先级**: P0/P1/P2
```

---

## 📊 报告文件格式

### 标准报告结构

```markdown
# <Team>报告：<任务标题>

## ✅ 完成情况
- 任务1：✅ 完成
- 任务2：✅ 完成

## 📊 详细结果
...

## ⚠️ 遇到的问题
...

## 💡 建议
...

---
**完成时间**: YYYY-MM-DD HH:MM
**执行者**: <Team> Agent
```

---

## 🔄 多Agent管理

### 并行启动多个Agent

```bash
# 启动Core Team
opencode run --agent core "任务..." > logs/core.log 2>&1 &

# 启动AI Team
opencode run --agent ai "任务..." > logs/ai.log 2>&1 &

# 启动Test Team
opencode run --agent test "任务..." > logs/test.log 2>&1 &
```

### 依赖管理

如果Agent B依赖Agent A的结果：

```bash
# 1. 先启动Agent A
opencode run --agent core "任务A..." > logs/core.log 2>&1 &

# 2. 等待Agent A完成（读取报告）
# 不需要主动等待，Agent A完成后会生成报告

# 3. PM Team读取报告后，再启动Agent B
opencode run --agent test "任务B..." > logs/test.log 2>&1 &
```

---

## ⚠️ 重要注意事项

### ✅ 必须做

1. ✅ 启动前创建任务文件
2. ✅ 使用后台运行（`&`）
3. ✅ 重定向日志（`> logs/xxx.log 2>&1`）
4. ✅ 在message中明确指出报告文件位置
5. ✅ 等待Agent报告（不主动检查）

### ❌ 禁止做

1. ❌ 使用task工具启动Team Agent
   - task只能启动general/explore临时代理
   - Team Agent必须用opencode run启动

2. ❌ 轮询Agent状态
   - 不要定期检查日志
   - 不要定期检查进程
   - 等待Agent主动报告

3. ❌ 使用交互式启动
   - 不要用 `opencode --agent <name>`（交互式）
   - 必须用 `opencode run --agent <name>`（非交互式）

4. ❌ 忘记创建报告目录
   - 启动前确保 `reports/` 目录存在

---

## 🎓 示例：完整工作流

### 场景：Test Team运行集成测试

#### 1. 创建任务文件

```bash
mkdir -p tasks reports logs

cat > tasks/test-team-task.md << 'EOF'
# Test Team任务：运行集成测试

## 任务背景
Core Team已完成Sprint 2开发，需要重新运行集成测试。

## 具体任务
1. git pull origin main
2. pytest tests/integration/ -v
3. 检查之前跳过的测试是否通过

## 输出要求
在 reports/test-report.md 写入：
- 测试结果统计
- 通过/失败/跳过数量
- 发现的问题

---
**优先级**: P0
EOF
```

#### 2. 启动Test Team

```bash
opencode run --agent test "请读取 tasks/test-team-task.md 中的任务并完成，结果写入 reports/test-report.md" > logs/test.log 2>&1 &
```

#### 3. PM Team继续其他工作

PM Team不需要等待，可以：
- 处理其他任务
- 回应用户询问
- 准备下一个任务

#### 4. Test Team完成，生成报告

Test Team自动完成工作并写入 `reports/test-report.md`

#### 5. PM Team读取报告（被动触发）

用户询问或PM Team需要时，读取报告：

```bash
cat reports/test-report.md
```

---

## 📚 参考资料

### OpenCode命令

- `opencode run --agent <name>` - 非交互式启动agent
- `opencode --agent <name>` - 交互式启动（不推荐）
- `opencode run --help` - 查看帮助

### Team Agent列表

- `core` - Core Team - 数据处理和工具开发
- `ai` - AI Team - 向量嵌入和语义搜索
- `test` - Test Team - 测试框架和质量保证
- `integration` - Integration Team - opencode集成和连接器
- `pm` - PM Team - 项目管理和协调（你自己）

### 不支持task工具

- `task` 工具只能启动 `general` 或 `explore` 临时代理
- 不能用task启动项目中的Team Agent

---

## 🔧 故障排查

### Agent没有启动

检查：
```bash
# 查看进程
ps aux | grep opencode

# 查看日志
tail -20 logs/<team>.log
```

### Agent没有生成报告

可能原因：
1. 任务文件路径错误
2. reports目录不存在
3. Agent执行失败

解决：
```bash
# 检查日志
cat logs/<team>.log

# 手动创建目录
mkdir -p reports
```

### 需要查看Agent进度

虽然不应该主动轮询，但如果需要：

```bash
# 查看日志尾部
tail -f logs/<team>.log
```

---

**版本**: v1.0  
**更新日期**: 2026-03-07  
**维护者**: PM Team
