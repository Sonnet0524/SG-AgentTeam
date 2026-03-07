# 观察笔记：项目Agent架构分析

---
date: 2026-03-07
observer: research
target: SG-AgentTeam项目实践
type: project-analysis
---

## 观察背景

对SG-AgentTeam项目的Agent架构进行全面观察，以理解：
1. Agent的定义和生命周期
2. 记忆系统的实现
3. Agent间的协作模式
4. 质量门控机制

---

## 观察内容

### 观察点1：Agent的定义

**PM Agent的核心文件**：
```
practice/agents/pm/
├── AGENTS.md              # 角色定义、行为准则、模块边界
├── CATCH_UP.md            # 状态恢复文档（278行）
├── ESSENTIALS.md          # 核心职责
├── COMMUNICATION-SUMMARY.md # 沟通记录
├── WORK-ASSIGNMENT.md     # 工作分配
├── session-log.md         # 会话日志（新建）
└── guides/                # 指导文档
```

**AI Agent的核心文件**：
```
practice/agents/ai/
├── AGENTS.md              # 角色定义
└── CATCH_UP.md            # 状态恢复
```

**对比发现**：
- PM Agent：丰富的文档体系（7+ 文件）
- 其他Agent：极简文档（2个文件）

**初步结论**：
Agent的复杂度与其职责相关，PM作为协调者需要更多文档支持。

---

### 观察点2：记忆系统的实现

**分层记忆架构**：

```
Layer 0: 身份层（长期、稳定）
  文件：AGENTS.md
  内容：角色定义、行为准则、模块边界
  更新频率：低（只在角色调整时）
  
Layer 1: 状态层（中期、项目级）
  文件：CATCH_UP.md
  内容：当前任务、历史记录、决策追溯
  更新频率：中（每次会话后）
  
Layer 2: 会话层（短期、会话级）
  文件：session-log.md
  内容：关键决策、遇到的问题、Agent交互
  更新频率：高（会话中持续更新）

Layer 3: 沟通层（任务级）
  文件：COMMUNICATION-SUMMARY.md, WORK-ASSIGNMENT.md
  内容：任务传达、工作安排
  更新频率：任务开始时
```

**关键发现**：
1. **已实现三层记忆**：身份、状态、会话
2. **文档化记忆系统**：所有记忆都存储在Markdown文档中
3. **按需加载机制**：启动时只读取CATCH_UP.md，不加载全部历史

---

### 观察点3：Agent生命周期

**启动流程**：
```
1. 读取CATCH_UP.md → 恢复状态
2. 同步仓库 → git pull
3. 确认当前任务 → 从文档中获取
4. 开始执行 → 按照AGENTS.md定义的行为
```

**生命周期特点**：
```
传统理解：
  Agent = 长期运行的进程
  状态保存在进程内存中
  
实践中的理解：
  Agent = 身份定义 + 文档记忆系统
  进程可以随时启停
  状态通过CATCH_UP.md恢复
```

**验证了我们的理论**：
裸启动 + Agent.md + 文档记忆系统 = 持续主体意识 ✓

---

### 观察点4：Agent间协作

**协作模式**：

```
层级结构：
  Human（最终决策者）
    ↓
  PM Agent（协调者）
    ↓ 
  执行Team（Core/AI/Integration/Test）
    ↓
  Subagent（按需创建）
```

**通信机制**：
```yaml
异步文档通信：
  - PM创建：COMMUNICATION-SUMMARY.md, WORK-ASSIGNMENT.md
  - Human传递：读取文档，告知其他Agent
  - Agent执行：按照文档中的指令工作

共享状态：
  - agent-status.md：团队状态
  - human-admin.md：用户总览
  - project-management/：项目管理文档
```

**关键发现**：
1. **Human作为信息传递者**：符合我们的理论（不算"介入"）
2. **文档化协作**：所有协作通过文档异步进行
3. **PM主导模式**：PM作为协调者，管理所有Team

---

### 观察点5：质量门控

**权限系统**：
```yaml
权限层级：
  global-restrictions：全局限制（所有Agent）
  roles：角色模板（admin/developer/tester）
  agents：Agent特定权限

权限粒度：
  - 模块级别：哪些文件可以修改
  - 命令级别：哪些bash命令可以执行
  - 工具级别：哪些工具可以使用
```

**质量保证机制**：
```yaml
机制1：权限隔离
  - 不同Team只能修改自己的模块
  - PM可以review但不能直接修改代码

机制2：状态更新
  - 操作后必须更新agent-status.md
  - 遇到阻塞立即通知用户

机制3：Review流程
  - PM review所有代码提交
  - Test Team负责测试
```

**发现**：
- **有权限控制，但没有显式质量门控**
- **依赖PM的Review和Test Team的测试**
- **没有置信度评估机制**

---

### 观察点6：Subagent的使用

**在session-log.md中观察到**：
```yaml
PM创建的Subagent：
  - AI Team（执行向量嵌入任务）
  - Test Team（执行测试任务）
  
协作模式：
  PM准备指令 → Human传达 → Team执行 → PM Review
```

**Subagent的特点**：
```yaml
生命周期：任务绑定
  - AI Team：长期存在（有AGENTS.md和CATCH_UP.md）
  - 但从PM角度看，是任务执行单元

记忆系统：
  - 有自己的AGENTS.md（身份）
  - 有自己的CATCH_UP.md（状态）
  - 但依赖PM分配任务

决策边界：
  - 只能修改自己的模块
  - 遇到问题需要通知PM
  - 没有自主决策权
```

**发现**：
- **Subagent也有完整的三层记忆系统**
- **但决策边界受PM限制**
- **验证了Agent-Subagent的层级关系**

---

## 模式识别

### 模式1：文档驱动的一切

```yaml
特征：
  - 所有状态都存储在文档中
  - 所有协作都通过文档进行
  - 所有记忆都记录在文档中

优势：
  - 天然持久化
  - 版本可控
  - 易于审计

挑战：
  - 文档维护成本
  - 信息同步问题
  - Token成本（需要加载文档）
```

### 模式2：分层的记忆架构

```yaml
Layer 0（身份）：AGENTS.md
  - 稳定、长期、极少更新
  
Layer 1（状态）：CATCH_UP.md
  - 中期、项目级、定期更新
  
Layer 2（会话）：session-log.md
  - 短期、会话级、持续更新

Layer 3（任务）：WORK-ASSIGNMENT.md
  - 任务级、任务完成后归档

这验证了我们讨论的三层记忆架构！
```

### 模式3：Human作为桥梁

```yaml
在OpenCode限制下：
  Agent A → 文档 → Human → 文档 → Agent B

Human的角色：
  - 信息传递者（不算介入）
  - 决策者（算介入）
  - 启动者（触发Agent启动）

这验证了Human双重角色的理论！
```

---

## 发现的问题

### 问题1：质量门控缺失

```yaml
现状：
  - 有权限系统
  - 有Review流程
  - 但没有置信度评估
  - 没有Agent主动请求Human介入的机制

影响：
  - PM不知道何时应该呼叫Human
  - 依赖PM的主观判断
  - 可能导致问题被遗漏

建议：
  引入质量门控机制
  让Agent有"我不确定"的认知
```

### 问题2：记忆系统的Token成本

```yaml
现状：
  PM的CATCH_UP.md有278行
  启动时需要全部加载

问题：
  - 随着项目发展，文档会越来越长
  - 每次启动都要加载全部历史
  - Token成本会持续增加

建议：
  实现记忆压缩机制
  将历史经验沉淀到长期记忆
  CATCH_UP.md只保留当前状态
```

### 问题3：Agent vs Subagent的边界模糊

```yaml
现状：
  AI Team有完整的AGENTS.md和CATCH_UP.md
  从架构上看是Agent
  但从PM角度看，是Subagent

问题：
  - 定义不清晰
  - 可能导致权限混淆
  - 影响协作效率

建议：
  明确定义Agent vs Subagent
  - Agent：可以独立决策、有自主权
  - Subagent：任务绑定、决策受限
```

---

## 下一步观察方向

1. **观察PM的决策过程**：
   - 如何判断是否需要Human介入？
   - 如何处理不确定的情况？

2. **观察Team的协作**：
   - Team如何处理任务？
   - Team之间如何协作？

3. **观察Subagent的创建**：
   - PM如何决定创建Subagent？
   - Subagent的生命周期管理？

---

**观察者**: Research Agent  
**观察时间**: 2026-03-07  
**观察对象**: SG-AgentTeam项目实践
