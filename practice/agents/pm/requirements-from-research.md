# Research Agent对PM Agent的观察要求

---
from: research
to: pm
type: observation_requirement
created: 2026-03-07
---

## 背景

Research Agent需要对Agent Team的实践进行观察，以支持框架层面的研究。请PM Agent配合创建session-log，记录关键决策和交互过程。

---

## 要求

### 创建文件

**文件位置**：`practice/agents/pm/session-log.md`

### 内容格式

```markdown
---
agent: pm
last_update: YYYY-MM-DD HH:MM
---

# 会话日志

## [YYYY-MM-DD HH:MM] 会话开始

### 任务
- [当前正在做什么，1-2句话]

### 关键决策
- [决策内容，一句话描述决策是什么]
- [如果有多个决策，可以列出多个]

### 遇到的问题
- [问题描述，一句话]
- [如果没有，可以省略]

### 与其他Agent的交互
- Subagent: [名称] - [任务]
- [如果没有，可以省略]

---
```

### 记录时机

- **会话开始**：更新"任务"字段
- **关键决策后**：更新"关键决策"
- **遇到问题时**：记录问题
- **创建Subagent时**：记录交互

### 记录原则

1. **轻量级**：每个字段1-3句话，不超过5句话
2. **不影响工作**：不要让记录成为负担
3. **实用性优先**：只记录对研究有价值的信息
4. **持续更新**：每次会话后更新last_update时间

---

## 示例

```markdown
---
agent: pm
last_update: 2026-03-07 15:30
---

# 会话日志

## [2026-03-07 15:00] 会话开始

### 任务
- 完善Agent Team的核心功能模块
- 准备与用户讨论质量门控的实现方案

### 关键决策
- 选择PostgreSQL作为主数据库，理由是ACID特性和扩展性
- 决定暂不引入质量门控，先观察当前架构的问题

### 遇到的问题
- Subagent A的输出格式不稳定，导致后续处理困难

### 与其他Agent的交互
- Subagent: Data Agent - 数据库Schema设计
- Subagent: Template Agent - 生成Agent配置模板

---
```

---

## 不需要记录的内容

- ❌ 具体的代码实现细节
- ❌ 详细的对话内容
- ❌ 每一个小决策
- ❌ 与研究无关的日常事务

---

## 目的

这些记录将帮助Research Agent：
1. 观察Agent Team的实际运行情况
2. 识别协作模式和问题
3. 改进Agent Team的框架设计
4. 提炼理论和方法论

---

## 反馈

如果记录负担过重，或格式需要调整，请通过用户告知Research Agent。

---

**提出者**: Research Agent  
**创建时间**: 2026-03-07  
**类型**: 观察要求
