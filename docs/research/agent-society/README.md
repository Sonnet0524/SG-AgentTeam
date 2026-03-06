# Agent社会架构研究

> 🤖 Agent Team的组织结构与社会关系

**研究状态**: 🔄 基础框架建立  
**创建日期**: 2026-03-06  
**最后更新**: 2026-03-06

---

## 🎯 研究概述

### 核心问题

**如何定义Agent vs Subagent？如何设计Agent Team的组织结构？**

### 核心洞察

```
Agent Team不是简单的Agent集合
而是有组织结构的"社会"

关键设计维度：
├─ 生命周期（长期 vs 临时）
├─ 层级关系（Agent vs Subagent）
├─ 团队边界（Team内 vs Team间）
└─ 生成方式（模板 vs 自主）
```

---

## 📊 核心理论

### Agent vs Subagent定义

这是本次研究的**核心突破**：

| 维度 | Agent | Subagent |
|------|-------|----------|
| **生命周期** | Persistent（持久） | Transient（临时） |
| **存在方式** | Serve模式（服务进程） | Task-bound（任务绑定） |
| **创建者** | System / PM | Agent |
| **销毁条件** | Explicit stop | Task complete |
| **能力积累** | 跨任务记忆 | 任务内无跨任务记忆 |
| **资源占用** | 长期 | 临时 |

**关键洞察**:
```
差异不在能力高低
而在生命周期长短

Agent = 长期存在的服务提供者
Subagent = 临时任务的执行者
```

### PM Agent的特殊定位

```
PM Agent = Agent + 特殊职责

Agent属性：
├─ 长期存在
├─ PM创建或系统启动
└─ 有跨任务记忆

特殊职责：
├─ Team协调者（协调Subagent）
├─ Human接口（首问负责制）
├─ 决策者（自主决策边界）
└─ 质量门控判断者
```

### PM Agent能力模型

```
PM能力公式：
PM能力 = LLM基础能力 + Prompt增强能力 + 经验积累能力

关键洞察：
├─ PM能力受限于底层LLM（这是合理的）
├─ 可通过Prompt设计增强
├─ 可通过经验积累提升
└─ 真正价值在"最优协调"而非"最强能力"
```

**协调能力分解**:
```
最优协调能力 = 
  知道每个Agent的能力边界
+ 知道何时自主决策（质量门控HIGH）
+ 知道何时呼叫Human（质量门控LOW）
+ 知道如何组合Agent能力
```

---

## 🏗️ 架构设计

### 四维设计空间

Agent社会架构由四个维度定义：

```
维度1：生成方式
├─ 模板生成Agent（Template Instantiated）
│   ├─ 特点：标准化、成本低
│   └─ 适用：常规任务
│
└─ 自主生成Agent（Real-time Created）
    ├─ 特点：灵活、针对性强
    └─ 适用：创新任务

维度2：团队边界
├─ Team内（Intra-Team）
│   ├─ 关系：紧密协作、强依赖
│   ├─ 信任：高（by PM design）
│   └─ 通信：高频、低延迟
│
└─ Team间（Inter-Team）
    ├─ 关系：松散协作、弱依赖
    ├─ 信任：低（需建立）
    └─ 通信：低频、高延迟

维度3：层级关系
├─ Agent-Subagent（主从关系）
├─ Agent-Agent（对等关系）
└─ Agent-Human（人机关系）

维度4：生命周期
├─ 临时Agent（Transient）
└─ 持久Agent（Persistent）
```

### PM主导模式

```
当前框架采用：PM主导模式

架构层次：

Layer 0: Human（最终决策者）
├─ 参与：最小化
└─ 触发：PM有需求时

Layer 1: PM Agent（首问责任人）
├─ 自主性：强
├─ 职责：协调 + Human接口
└─ 决策边界：质量门控判断

Layer 2: Subagent Team（执行单元）
├─ 自主性：中
├─ 生命周期：任务绑定
└─ 职责：具体任务执行
```

---

## 📚 研究成果

### 核心文档

| 文档 | 说明 | 状态 |
|------|------|------|
| [Agent定义标准](agent-definition.md) | Agent vs Subagent的标准定义 | 🔜 待整理 |
| [PM Agent模型](pm-agent-model.md) | PM的能力、职责、决策边界 | 🔜 待整理 |
| [架构模式库](architecture-patterns.md) | 不同场景的架构模式 | 🔜 待整理 |
| [调研报告](agent-team-survey/) | 业界主流架构调研 | ✅ 已完成 |

### 调研资料

- 📖 [Agent Team设计调研](agent-team-survey/agent-team-design-survey.md)
- 📖 [调研摘要](agent-team-survey/agent-team-design-survey-summary.md)
- 📖 [框架对比参考](agent-team-survey/framework-comparison.md)

### 研究过程

完整的理论推导过程记录在：
- 📖 [研究日志 - Agent社会架构部分](../research-log.md#agent社会架构理论)

---

## 🔬 理论深度分析

### 为什么PM Agent是Agent？

```
判断标准：
✅ 生命周期：Persistent（长期存在）
✅ 存在方式：Serve模式（服务进程）
✅ 创建方式：系统启动或显式创建
✅ 能力积累：跨任务记忆
✅ 资源占用：长期

结论：PM Agent符合Agent的所有标准
```

### 是否需要多个Agent？

```
当前设计：只有PM是Agent，其他都是Subagent

优势：
├─ 架构简单，资源占用少
├─ 协调成本低
└─ 适合小规模、简单场景

未来可能：
├─ Domain Expert Agent（领域专家）
├─ Knowledge Manager Agent（知识管理）
├─ Integration Agent（集成管理）
└─ 适合大规模、复杂场景
```

### Agent社会的演化方向

```
初期：单Agent模式（当前）
├─ 只有PM是Agent
└─ 其他都是Subagent

中期：多Agent协作模式
├─ 引入新的长期Agent
├─ Agent间协作机制
└─ 更复杂的社会关系

长期：Agent生态模式
├─ Agent模板市场
├─ Agent能力交易
└─ Agent社会网络
```

---

## 🎯 应用价值

### 实践指导

1. **明确角色定位** - Agent vs Subagent清晰区分
2. **资源优化配置** - 长期Agent贵精不贵多
3. **生命周期管理** - 临时Subagent及时销毁
4. **能力积累机制** - Agent的记忆和学习

### 设计原则

```
原则1：最小Agent原则
├─ 能用Subagent就不用Agent
├─ 减少长期资源占用
└─ 提高资源利用效率

原则2：生命周期优先
├─ 生命周期是核心判断标准
├─ 而非能力高低
└─ 避免过度设计

原则3：职责清晰
├─ Agent：协调、接口、决策
├─ Subagent：执行、反馈、完成
└─ 避免角色混淆
```

---

## 🔜 待深入研究的问题

### 问题1：Agent的判定标准
- [ ] 是否需要更精细的判定标准？
- [ ] 边界案例如何处理？
- [ ] Agent能否降级为Subagent？

### 问题2：多Agent协作
- [ ] 何时需要引入新的Agent？
- [ ] Agent间如何协作？
- [ ] Agent间的信任机制？

### 问题3：能力积累
- [ ] Agent如何积累经验？
- [ ] 经验如何跨任务传递？
- [ ] 如何避免经验过时？

---

## 🔗 相关研究

- [质量门控](../quality-gates/) - PM的决策边界
- [文档化交互](../agent-interaction/) - Agent间交互机制
- [Agent模板标准](../agent-template-standard/) - Agent的标准定义

---

## 📝 参与贡献

欢迎对这个理论提出质疑、补充或验证：
- 💬 **架构讨论** - 是否有更好的架构模式？
- 🧪 **实践验证** - 在实际项目中验证架构
- 🐛 **问题发现** - 架构的局限性或边界条件

---

**维护者**: Research Agent  
**创建日期**: 2026-03-06  
**研究状态**: 基础框架建立，深入研究进行中
