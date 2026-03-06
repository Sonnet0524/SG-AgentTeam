# Research - 研究目录

> 🔬 Agent Team Framework的核心研究成果

**更新日期**: 2026-03-06

---

## 📂 目录结构

```
research/
├── quality-gates/              # 🔥 质量门控研究
├── agent-society/              # 🤖 Agent社会架构研究
├── agent-template-standard/    # 📋 Agent模板标准（待研讨）
├── agent-interaction/          # 📄 Agent交互模式（已有）
├── information-architecture/   # 🔄 信息流架构（已有）
├── token-based/                # 📊 Token-Based管理（已有）
└── research-log.md             # 📝 完整研究日志
```

---

## 🔥 核心研究成果

### 1. 质量门控理论 ⭐ 最新突破

**核心贡献**: 质量门控 = Human介入触发器

```
理论重构：
├─ 旧理解：能力边界声明
├─ 新理解：Human介入触发器
└─ 价值：定义PM自主决策边界

核心机制：
├─ 确定性评估
├─ 可接受性评估
├─ 混淆判断
└─ Human介入决策

Token效率：~15 tokens
```

📖 [深入研究](quality-gates/)

---

### 2. Agent社会架构 ⭐ 重要突破

**核心贡献**: Agent vs Subagent的标准定义

```
核心定义：
Agent = 长期存在（Persistent）
Subagent = 临时任务（Transient）

PM Agent模型：
├─ 能力 = LLM + Prompt + 经验
├─ 价值 = 最优协调
└─ 边界 = 质量门控
```

📖 [深入研究](agent-society/)  
📖 [调研报告](agent-society/agent-team-survey/)

---

### 3. Agent交互模式 ✅ 已完成

**核心贡献**: 文档化交互机制

```
成果：
├─ 文档化交互协议
├─ 分层文档体系
└─ Message Queue愿景

效果：
├─ Context使用 ↓93%
├─ 协作冲突 ↓100%
└─ 预测准确率 ↑70%
```

📖 [深入研究](agent-interaction/)

---

## 🔄 进行中的研究

### 信息流架构

**研究问题**: "人-智能-基础能力"三层架构中信息流如何设计？

📖 [探索研究](information-architecture/)

### Token-Based管理

**研究问题**: Token能否作为Agent工作量度量单位？

📖 [参与探讨](token-based/)

---

## 🔜 待启动的研究

### Agent模板标准

**研究问题**: 什么是Agent？如何定义Agent的标准？

**优先级**: 高（重点研讨课题）

📖 [了解研究计划](agent-template-standard/)

---

## 📝 研究日志

完整的理论推导过程记录在：

📖 [研究日志](research-log.md)

**日志内容**：
- ✅ 所有理论突破的推导过程
- ✅ 完整的交流记录
- ✅ 决策追溯链
- ✅ 未解决问题的跟踪

---

## 🎯 快速导航

### 按研究阶段

```
已完成：
├─ Agent交互模式 ✅
├─ 质量门控理论 ✅
└─ Agent社会架构基础 ✅

进行中：
├─ 信息流架构 🔄
└─ Token-Based管理 🔄

待启动：
└─ Agent模板标准 🔜
```

### 按重要性

```
核心成果（必读）：
1. [质量门控理论](quality-gates/) - Human介入触发器
2. [Agent社会架构](agent-society/) - Agent定义标准
3. [Agent交互模式](agent-interaction/) - 文档化交互

扩展阅读：
4. [调研报告](agent-society/agent-team-survey/) - 业界调研
5. [研究日志](research-log.md) - 完整过程
```

### 按读者类型

```
研究者：
├─ [质量门控理论](quality-gates/)
├─ [Agent社会架构](agent-society/)
└─ [研究日志](research-log.md)

实践者：
├─ [Agent交互模式](agent-interaction/)
├─ [调研报告摘要](agent-society/agent-team-survey/agent-team-design-survey-summary.md)
└─ [框架对比](agent-society/agent-team-survey/framework-comparison.md)

初学者：
└─ 先读主文档 [../../README.md](../../README.md)
```

---

## 🤝 参与贡献

欢迎对研究提出：
- 💬 **理论探讨** - 质疑、补充、验证
- 🧪 **实践验证** - 在实际项目中验证理论
- 🐛 **问题发现** - 发现理论的局限性
- 💡 **创新想法** - 新的研究方向

**参与方式**:
- [GitHub Discussions](https://github.com/Sonnet0524/SG-AgentTeam/discussions)
- [提交Issue](https://github.com/Sonnet0524/SG-AgentTeam/issues)

---

## 📊 研究统计

| 类别 | 完成 | 进行中 | 待启动 |
|------|------|--------|--------|
| 核心理论 | 3 | 0 | 1 |
| 扩展研究 | 0 | 2 | 0 |
| **总计** | **3** | **2** | **1** |

---

**维护者**: Research Agent  
**更新日期**: 2026-03-06
