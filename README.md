# Agent Team Framework

> 🤝 基于文档的AI Agent协作框架

**版本**: v1.1 | **状态**: 实践验证中 | **更新**: 2026-03-07

---

## 💡 核心理念

让多个AI Agent像人类团队一样**高效、可靠地协作**——通过**文档化交互**实现异步、可追溯、可自动化的协作模式。

## 📚 研究框架

本项目使用 **[SEARCH-R Framework](https://github.com/Sonnet0524/SEARCH-R)** 进行系统性研究。

SEARCH-R是一个通用的研究型Agent框架，提供：
- 🔍 **SEARCH-R方法论** - 完整的研究循环
- 🤖 **Research Agent模板** - 可复用的研究Agent
- 📄 **标准文档模板** - 研究文档的标准格式
- 🛠️ **Skills库** - 可复用的研究能力

**框架仓库**: [https://github.com/Sonnet0524/SEARCH-R](https://github.com/Sonnet0524/SEARCH-R)

---

## 📖 内容导航

本仓库包含两部分内容：

| 部分 | 内容 | 适合读者 |
|------|------|---------|
| **[框架篇](#-框架篇)** | 理论、方法论、设计思想 | 想了解Agent协作模式的研究者 |
| **[实践篇](#-实践篇)** | 本项目的Agent Team实现 | 想参考具体实现的实践者 |

### 🔬 研究文档

完整的研究成果位于 [docs/research/](docs/research/)

| 研究课题 | 核心成果 | 状态 |
|---------|---------|------|
| [SEARCH-R方法论](agents/research/CATCH_UP.md) | 研究型Agent工作循环 | ✅ 方法论确立 |
| [Agent四层架构](agents/research/CATCH_UP.md) | 身份+能力+记忆+访问系统 | ✅ 理论突破 |
| [质量门控分层](agents/research/CATCH_UP.md) | 元认知+规则+工具三层 | ✅ 理论突破 |
| [质量门控理论](docs/research/quality-gates/) | Human介入触发器 | ✅ 理论突破 |
| [Agent社会架构](docs/research/agent-society/) | Agent定义标准 | ✅ 基础完成 |
| [Agent交互模式](docs/research/agent-interaction/) | 文档化交互 | ✅ 核心成果 |
| [Agent模板标准](docs/research/agent-template-standard/) | Agent行为规范 | 🔜 待研讨 |

📄 **完整研究过程**: [研究日志](docs/research/research-log.md)

---

# 🎓 框架篇

> 通用理论，可复用于任何Agent协作场景

## 🎯 核心研究

### SEARCH-R方法论 ⭐ 最新突破

**方法论确立**: 研究型Agent的标准工作循环

```
SEARCH-R方法论

S - Survey（观察调研）
E - Explore（探索检索）
A - Analyze（分析思考）
R - Review（评审探讨）
C - Confirm（确认验证）
H - Harvest（收获产出）
R - Reflect（反思迭代）

循环：S → E → A → R → C → H → R → (回到S)
```

**命名由来**: Search（搜索）+ Reflect（反思）= 持续探索真理

**核心价值**:
- 🔍 **观察调研** - 从实践中发现问题
- 📚 **探索检索** - 检索相关知识
- 💭 **分析思考** - 深度理论构建
- 🤝 **评审探讨** - Human参与探讨
- ✅ **确认验证** - 实践中验证
- 📦 **收获产出** - 沉淀研究成果
- 🔄 **反思迭代** - 持续优化方法

📖 [完整方法论](agents/research/CATCH_UP.md)

---

### Agent交互模式 ⭐ 核心成果

**研究问题**: Agent之间如何高效、可靠地交互？

**解决方案**: 基于文档的上下文交换机制

```
传统方式：Agent ←→ Agent（直接对话）
           ↓ 问题：同步阻塞、不可追溯、难以自动化

本研究：Agent ←→ 文档 ←→ Agent（文档中介）
           ↓ 优势：异步协作、可追溯、可自动化
```

**核心成果**:
- 📄 **文档化交互协议** - 标准化的交互格式和状态流转
- 📁 **分层文档体系** - Level 0/1/2按需加载
- 🚀 **Message Queue愿景** - 未来可实现全自动协作

**效果数据**:

| 指标 | 传统方式 | 本框架 | 改进 |
|------|---------|--------|------|
| Context使用 | 600行 | 40行 | ↓93% |
| 协作冲突 | 每周3次 | 0次 | ↓100% |
| 预测准确率 | 50% | 85% | ↑70% |

📖 [深入研究](docs/research/agent-interaction/)

---

## 🔥 最新理论突破

### Agent系统四层架构

**研究突破**: Agent系统的完整架构定义

```
Agent系统 = 身份层 + 能力系统 + 记忆系统 + 访问系统

┌─────────────────────────────────────────┐
│ 身份层（AGENTS.md）                      │
│ - 角色定义                              │
│ - 核心能力（不可分离）                   │
│ - 元认知意识                            │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 能力系统                                │
│ - 核心能力：定义在AGENTS.md中           │
│ - 通用能力：Skills，可复用、按需加载     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 记忆系统                                │
│ - 身份记忆：AGENTS.md                   │
│ - 状态记忆：CATCH_UP.md                 │
│ - 经验记忆：experiences/                │
│ - 会话记忆：session-log.md              │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 访问系统                                │
│ - 记忆索引：memory-index.yaml           │
│ - 检索机制：按需加载                     │
│ - 压缩机制：短期→长期                    │
└─────────────────────────────────────────┘
```

**关键洞察**:
- 🎯 **记忆 ≠ 访问** - 记忆是内容，索引是方法
- 🔧 **核心能力不分离** - 定义在AGENTS.md中
- 📦 **Skills可复用** - 通用能力按需加载

---

### 质量门控分层定义

**研究突破**: 质量门控的三层结构

```
质量门控 = 元认知意识 + 评估规则 + 评估工具

┌─────────────────────────────────────────┐
│ 元认知意识（不可分离）                   │
│ - "我知道自己什么时候不知道"            │
│ - Agent的核心属性                       │
│ - 定义在AGENTS.md中                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 评估规则（可Skills化）                  │
│ - 确定性判断规则                        │
│ - 可接受性判断规则                      │
│ - 混淆判断规则                          │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 评估工具（可Skills化）                  │
│ - 质量门控Schema                        │
│ - 评估流程                              │
│ - 可复用的工具                          │
└─────────────────────────────────────────┘
```

**关键区分**:
- 🧠 元认知意识 → Agent核心属性（不分离）
- 📋 评估规则 → 可Skills化（按需加载）
- 🛠️ 评估工具 → 可Skills化（可复用）

---

### Agent vs Subagent正确定义

**研究突破**: 以决策自主性为区分标准

```
区分标准：决策自主性（不是文档完整性）

Agent（有自主权）:
  ✅ 可以自主决策
  ✅ 独立的任务空间
  ✅ 对结果负责
  示例：PM Agent、Research Agent

Subagent（无自主权）:
  ✅ 任务绑定
  ✅ 决策受限
  ✅ 执行分配的任务
  示例：AI Team、Core Team、Integration Team
```

**关键洞察**: 不是"有没有文档"决定Agent vs Subagent，而是"有没有自主权"

---

### Skills分离原则

**研究突破**: 能力分离的三大原则

```
原则1：非每次都需要 → 可以Skills化
原则2：可多个Agent复用 → 应该Skills化
原则3：相对独立的能力单元 → 可以Skills化

Skills分类：
├─ 决策支持类：quality-gate、risk-assessment
├─ 工作流类：git-workflow、review-process
├─ 规范类：coding-standards、documentation-guide
└─ 领域知识类：embedding-models、vector-search
```

**AGENTS.md精简原则**: 只保留身份 + 核心能力，目标 ~5k tokens

---

### 质量门控 = Human介入触发器

**研究突破**: 质量门控的本质重新定义

```
旧理解：能力边界声明（Agent间协作）
新理解：Human介入触发器（PM自主决策边界）
```

**核心价值**:
- 🎯 **确定性评估** - 判断结果是否确定
- ✅ **可接受性评估** - 判断结果是否可接受
- 🔍 **混淆判断** - 判断是否存在理解偏差
- 👤 **Human介入决策** - 决定何时呼叫Human

**工作机制**:
```
Agent输出 → PM评估
├─ 确定性HIGH + 可接受性HIGH + 无混淆 → PM自主决策
└─ 确定性LOW 或 可接受性LOW 或 存在混淆 → 呼叫Human
```

**Token效率**: ~15 tokens实现关键决策机制

📖 [完整研究过程](docs/research/research-log.md)

---

### Agent社会架构理论

**研究问题**: 如何定义Agent vs Subagent？如何设计Agent社会架构？

**核心定义**:

| 类型 | 生命周期 | 存在方式 | 创建者 |
|------|---------|---------|--------|
| **Agent** | 持久（Persistent） | Serve模式 | System/PM |
| **Subagent** | 临时（Transient） | Task-bound | Agent |

**关键洞察**: 差异在于**生命周期**，不在能力高低

**PM Agent模型**:
```
PM能力 = LLM能力 + Prompt设计 + 经验积累
真正价值 = 最优协调（而非最强能力）
决策边界 = 质量门控判断
```

📖 [调研报告](docs/research/agent-team-design-survey.md) | [执行摘要](docs/research/agent-team-design-survey-summary.md)

---

### 框架本质重新定位

**理论突破**:

```
从："人机协作框架" → Human是核心参与者
到："多智能体协同框架" → Human是最小化参与的决策者

核心理念：
├─ PM Agent是自主智能体（不是人类工具）
├─ Human参与最小化（只在必要时介入）
├─ 质量门控判断介入时机
└─ PM Agent主导模式（首问负责制）
```

📖 [研究日志](docs/research/research-log.md) | [框架对比](docs/research/framework-comparison.md)

---

## 🔄 持续研究

### 信息流架构

**研究问题**: "人-智能-基础能力"三层架构中，信息流如何设计？

**探索方向**:
- Agent First vs Human First 的适用场景
- 信息流性价比分析
- 动态平衡机制

📖 [探索研究](docs/research/information-architecture/)

---

### Token-Based管理 📊

**研究问题**: Token能否作为Agent工作量度量单位？

**方法论**:
- Token作为工作量单位
- Velocity（速度）概念
- 预测模型设计

📖 [参与探讨](docs/research/token-based/)

---

## 📖 方法论

### 文档分层体系

```
Level 0 (必需) ─── <50行  ─── 启动时加载
Level 1 (按需) ─── <100行 ─── 工作时加载  
Level 2 (参考) ─── 不限   ─── 按需查询
```

**核心价值**: 最小化Context占用，最大化信息效用

📖 [详细说明](docs/methodology/document-hierarchy.md)

---

### Context最小化

- **按需披露**: 只加载必要信息
- **索引驱动**: 通过索引快速定位
- **主动清理**: 及时释放无用信息

📖 [详细说明](docs/methodology/context-minimization.md)

---

### 边界隔离

- **单向依赖**: 避免循环依赖
- **明确归属**: 每个文件有明确责任人
- **代码审查**: 跨边界修改需审批

📖 [详细说明](docs/methodology/boundary-isolation.md)

---

## 🚀 未来方向

### 短期（3个月）
- 交互协议标准化
- Message Queue原型

### 中期（6个月）
- 半自动化协作流程
- 跨项目验证

### 长期（1年）
- 完整通用框架
- 开源生态建设

📖 [详细规划](docs/reference/future-directions.md)

---

## 🤝 参与贡献

欢迎：
- 💬 **理论探讨** - 对研究假设的建议
- 🧪 **实验验证** - 在其他场景中验证
- 🐛 **问题发现** - 实践中的问题
- 💡 **创新想法** - 新的研究方向

**参与方式**: [GitHub Discussions](https://github.com/Sonnet0524/SG-AgentTeam/discussions) | [提交Issue](https://github.com/Sonnet0524/SG-AgentTeam/issues)

---

# 🛠️ 实践篇

> 本项目(SG-AgentTeam)的Agent Team设计与实现

## 🚀 快速开始

**想复刻这个实践？** 👉 [复刻实践指南](practice/GETTING-STARTED.md)

---

## 📋 项目概述

**项目名称**: Knowledge Assistant  
**项目目标**: 个人知识管理助手  
**验证重点**: Agent Team Framework的可行性

### 团队配置

| Agent | 职责 | 模块边界 |
|-------|------|---------|
| **PM** | 项目管理、协调、进度跟踪 | management/ |
| **Data** | 数据模型、解析器、存储层 | data/, parsers/ |
| **Template** | 模板引擎、配置系统 | template/, config/ |
| **Test** | 测试框架、质量保证 | tests/, QA流程 |
| **Research** | 框架研究、方法论提炼 | docs/research/, docs/methodology/ |

---

## 🏗️ 架构设计

### 目录结构

```
SG-AgentTeam/
├── agents/                  # 🤖 框架层Agent
│   └── research/            # Research Agent
├── docs/                    # 📚 框架文档
│   ├── research/            # 核心研究
│   ├── methodology/         # 方法论
│   └── ...
├── practice/                # 🛠️ 实践部分
│   ├── agents/              # 🤖 实践层Agent
│   │   ├── pm/
│   │   ├── data/
│   │   ├── template/
│   │   └── test/
│   ├── management/          # 📊 项目管理
│   ├── knowledge-base/      # 🧠 知识库
│   ├── status/              # 📈 状态文档
│   └── ...
└── opencode.json            # ⚙️ Agent配置
```

### 交互机制

```
┌─────────────────────────────────────────────────────────┐
│                    Human Admin                           │
│                  (决策、监控、干预)                        │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │        PM Agent            │
        │    (协调、调度、跟踪)        │
        └─────────────┬─────────────┘
                      │
    ┌─────────┬───────┼───────┬─────────┐
    ▼         ▼       ▼       ▼         ▼
 Data    Template   Test  Research   ...
    │         │       │       │
    └─────────┴───────┴───────┴─────────┘
                      │
              文档化交互（共享上下文）
```

---

## 🚀 快速开始

**详细指南**: [复刻实践指南](practice/GETTING-STARTED.md)

### 启动Agent

```bash
./start-pm.sh        # PM Agent - 项目管理
./start-data.sh      # Data Agent - 数据开发
./start-template.sh  # Template Agent - 模板开发
./start-test.sh      # Test Agent - 测试保证
./start-research.sh  # Research Agent - 框架研究
```

### Agent入口文件

```
agents/research/CATCH_UP.md      # Research Agent (框架层)
practice/agents/pm/CATCH_UP.md       # PM Agent (实践层)
practice/agents/data/CATCH_UP.md     # Data Agent
practice/agents/template/CATCH_UP.md # Template Agent
practice/agents/test/CATCH_UP.md     # Test Agent
```

---

## 📊 实践成果

### 验证结论

✅ **文档化交互可行且有效**  
✅ **分层文档体系显著降低Context消耗**  
✅ **明确的模块边界消除协作冲突**  
⚠️ **Token-Based管理需进一步优化**

### 详细报告

📖 [实践验证报告](docs/practice/SG-AgentTeam/)  
📖 [经验教训总结](docs/practice/lessons-learned/)

---

## 📚 框架文档导航

### 快速入门
- 🎓 [研究概览](docs/) - 了解研究全貌
- 🔬 [Agent交互模式](docs/research/agent-interaction/) - 核心研究

### 深入了解
- 📖 [方法论](docs/methodology/) - 文档分层、Context最小化等
- 📊 [经验教训](docs/practice/lessons-learned/) - 实践总结
- 🔍 [对比分析](docs/reference/comparison.md) - 与其他方法对比

---

## 📖 引用

```bibtex
@misc{agent-team-framework-2026,
  title={Agent Team Framework: A Document-based Agent Interaction Model},
  author={Agent Team},
  year={2026},
  url={https://github.com/Sonnet0524/SG-AgentTeam}
}
```

---

## 📜 许可协议

### 代码部分

本项目代码采用 **GNU Affero General Public License v3.0 (AGPL v3.0)** 协议开源。

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

**关键要求**：
- ✅ 自由使用、修改和分发
- ✅ 任何修改版本必须以AGPL开源
- ✅ 网络服务使用也必须开源（AGPL特有）
- ✅ 必须保留版权声明

**商业使用**：如需商业使用，请联系获取商业许可。

📄 [查看完整协议](LICENSE)

---

### 知识内容

本项目的文档、知识库等知识内容采用 **CC BY-NC-SA 4.0** 协议。

**关键要求**：
- ✅ 必须署名
- ❌ 禁止商业使用
- ✅ 相同方式共享

**商业使用**：如需商业使用，请联系获取商业许可。

📄 [查看完整协议](KNOWLEDGE_LICENSE)

---

## 🏷️ 版权声明

Copyright © 2026 Agent Team. All rights reserved.

本项目包括：
- 代码（AGPL v3.0）：允许开源使用，禁止闭源商业使用
- 知识（CC BY-NC-SA 4.0）：允许非商业使用，禁止商业使用

**商业合作**：通过 [GitHub Issues](https://github.com/Sonnet0524/SG-AgentTeam/issues) 联系
