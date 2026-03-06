# Agent Team Framework

> 🤝 基于文档的AI Agent协作框架

**版本**: v1.0 | **状态**: 实践验证中 | **更新**: 2026-03-06

---

## 💡 核心理念

让多个AI Agent像人类团队一样**高效、可靠地协作**——通过**文档化交互**实现异步、可追溯、可自动化的协作模式。

---

## 📖 内容导航

本仓库包含两部分内容：

| 部分 | 内容 | 适合读者 |
|------|------|---------|
| **[框架篇](#-框架篇)** | 理论、方法论、设计思想 | 想了解Agent协作模式的研究者 |
| **[实践篇](#-实践篇)** | 本项目的Agent Team实现 | 想参考具体实现的实践者 |

---

# 🎓 框架篇

> 通用理论，可复用于任何Agent协作场景

## 🎯 核心研究

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

### 信息流架构 🔄

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

**参与方式**: [GitHub Discussions](https://github.com/Sonnet0524/knowledge-assistant-dev/discussions) | [提交Issue](https://github.com/Sonnet0524/knowledge-assistant-dev/issues)

---

# 🛠️ 实践篇

> 本项目(knowledge-assistant-dev)的Agent Team设计与实现

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
knowledge-assistant-dev/
├── practice/                # 🛠️ 实践部分
│   ├── agents/             # 🤖 Agent配置目录
│   │   ├── pm/             # PM Agent
│   │   ├── data/           # Data Agent
│   │   ├── template/       # Template Agent
│   │   ├── test/           # Test Agent
│   │   └── research/       # Research Agent
│   ├── management/         # 📊 项目管理（PM负责）
│   ├── knowledge-base/     # 🧠 知识库（项目级）
│   ├── development-guide/  # 🔧 开发指南
│   ├── logs/               # 📝 Agent交互日志
│   └── status/             # 📈 状态文档
│       ├── agent-status.md
│       └── human-admin.md
├── docs/                   # 📚 研究文档（框架篇内容）
│   ├── research/           # 核心研究
│   ├── methodology/        # 方法论
│   ├── practice/           # 实践验证
│   └── reference/          # 参考资料
└── opencode.json           # ⚙️ Agent配置入口
```
knowledge-assistant-dev/
├── practice/                # 🛠️ 实践部分（Agent Team实现）
│   ├── agents/              # 🤖 Agent配置目录
│   │   ├── pm/              # PM Agent
│   │   ├── data/            # Data Agent
│   │   ├── template/        # Template Agent
│   │   ├── test/            # Test Agent
│   │   └── research/        # Research Agent
│   ├── management/          # 📊 项目管理（PM负责）
│   ├── knowledge-base/      # 🧠 知识库（项目级）
│   ├── development-guide/   # 🔧 开发指南
│   ├── logs/                # 📝 Agent交互日志
│   └── status/              # 📈 状态文档
│       ├── agent-status.md
│       └── human-admin.md
├── docs/                    # 📚 研究文档（框架篇内容）
│   ├── research/            # 核心研究
│   ├── methodology/         # 方法论
│   ├── practice/            # 实践验证
│   └── reference/           # 参考资料
└── opencode.json            # ⚙️ Agent配置入口
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

### 前置要求

- 安装 [OpenCode CLI](https://opencode.ai)
- 克隆本仓库

### 启动Agent

```bash
# 启动 PM Agent
./start-pm.sh   # Linux/Mac
start-pm.bat    # Windows

# 启动 Data Agent
./start-data.sh

# 启动 Template Agent
./start-template.sh

# 启动 Test Agent
./start-test.sh

# 启动 Research Agent
./start-research.sh
```

### Agent入口文件

每个Agent通过 `CATCH_UP.md` 快速恢复上下文：

```
practice/agents/
├── pm/CATCH_UP.md         # PM Agent入口
├── data/CATCH_UP.md       # Data Agent入口
├── template/CATCH_UP.md   # Template Agent入口
├── test/CATCH_UP.md       # Test Agent入口
└── research/CATCH_UP.md   # Research Agent入口
```

---

## 📊 实践成果

### 验证结论

✅ **文档化交互可行且有效**  
✅ **分层文档体系显著降低Context消耗**  
✅ **明确的模块边界消除协作冲突**  
⚠️ **Token-Based管理需进一步优化**

### 详细报告

📖 [实践验证报告](docs/practice/knowledge-assistant/)  
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
  url={https://github.com/Sonnet0524/knowledge-assistant-dev}
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

**商业合作**：通过 [GitHub Issues](https://github.com/Sonnet0524/knowledge-assistant-dev/issues) 联系
