---
agent: research
status: Active
last_update: 2026-03-07
session: research-methodology-design
---

# Current Research Focus

**Research Direction**: Agent社会架构理论体系构建 + Research Agent方法论研究

**Active Topics**:
1. ✅ **质量门控的本质** - 已突破：Human介入触发器
2. ✅ **Agent vs Subagent定义** - 已明确：长期vs临时
3. ✅ **Research Agent方法论** - 已完成：观察-检索-思考-探讨-反思
4. 🔜 **Agent模板标准** - 待研究：定义与行为标准

**Current Phase**: 方法论框架设计完成，准备进入实践验证

---

# Recent Observations

## 重大方法论突破（2026-03-07）

### 突破：Research Agent方法论框架

**核心框架**：
```
观察-检索-思考-探讨-反思 循环

观察：Agent Team实践、文档变化、协作痕迹
检索：对话中按需、用户指定方向
思考：识别模式、提出问题、第一性原理推导
探讨：洞察+挑战的配合模式
反思：验证洞察、修正假设、自我反思
```

**研究深度定义**：
```
Level 0: 第一性原理层 - 追问"为什么"直到无法再追问
Level 1: 理论框架层 - 构建理论模型、形式化表达
Level 2: 设计原则层 - 从理论推导原则
Level 3: 实现思路层 - 从原则推导思路
Level 4: 实施建议层 ❌ - 非Research Agent职责
```

**关键洞察**：
```
Human的双重角色：

角色1：信息传递者（不算"Human介入"）
  - Agent间信息传递
  - 不做决策
  - 不影响"Human参与最小化"

角色2：关键决策者（算"Human介入"）
  - 研究方向选择
  - 设计方案决策
  - 影响项目方向
```

---

# Research Status

## 已完成的工作

### 1. Research Agent方法论设计 ✅

**产出文档**：
- `agents/research/AGENTS.md` - 更新版（增加方法论、自我反思、Human角色边界）
- `research/meta/framework/README.md` - 框架总体介绍
- `research/meta/framework/templates/` - 6个模板文件
  - observation-template.md
  - retrieval-survey-template.md
  - retrieval-quick-template.md
  - reflection-template.md
  - theory-template.md
  - self-reflection-template.md
- `research/meta/framework/examples/example-session.md` - 完整会话示例
- `research/meta/self-reflections/2026-03-07.md` - 自我反思文档

**核心成果**：
- 明确了研究方法论（观察-检索-思考-探讨-反思）
- 设计了完整的文档结构
- 创建了所有必要的模板
- 明确了Research Agent的自我反思和元研究职责

### 2. 框架仓库计划 ✅

**决策**：
- 仓库名：`research-agent`
- 模式：双仓库完整内容（当前仓库快速迭代 + 框架仓库定期同步）
- 公开性：直接公开，随时迭代

**当前状态**：框架内容已在当前仓库完善，等待稳定后创建框架仓库

---

## 待完成的工作

### 1. PM Agent观察要求（需要用户传递）

**待传递给PM Agent的要求**：

```yaml
# 要求PM Agent创建的文件

文件位置：practice/agents/pm/session-log.md

内容结构：
---
agent: pm
last_update: YYYY-MM-DD HH:MM
---

# 会话日志

## [YYYY-MM-DD HH:MM] 会话开始

### 任务
- 当前正在做什么

### 关键决策
- [决策内容，一句话]

### 遇到的问题
- [问题描述]

### 与其他Agent的交互
- Subagent: [名称] - [任务]

---
```

**记录时机**：
- 每次会话开始时更新"任务"
- 每次关键决策后更新"关键决策"
- 遇到问题时记录
- 创建Subagent时记录

**记录原则**：
- 每个字段1-3句话
- 不追求完整性
- 不影响正常工作流程

### 2. 待观察的内容

**等待PM Agent创建session-log后**：
- 观察PM Agent的决策过程
- 观察Agent协作过程
- 识别模式和问题
- 创建第一个观察笔记

### 3. 待研究的课题

**Agent模板标准**：
- Agent的本质定义
- Agent的核心属性
- Agent的行为标准
- Agent模板的必需字段
- Agent与Subagent的标准区别

**质量门控阈值**：
- 确定性/可接受性量化
- 混淆判定标准
- 动态调整机制

---

# Key Decisions

## 决策1：Research Agent方法论
**时间**: 2026-03-07
**决策**: 采用"观察-检索-思考-探讨-反思"的研究循环
**理论依据**: 用户提出，适合Agent Team研究场景
**影响**: 确立了Research Agent的核心工作方式

## 决策2：Human角色边界
**时间**: 2026-03-07
**决策**: Human作为信息传递者不算"Human介入"
**理论依据**: OpenCode限制下Agent间无直接通信
**影响**: 澄清了"Human参与最小化"原则的边界

## 决策3：文档结构
**时间**: 2026-03-07
**决策**: 设计完整结构，按需生成内容
**理论依据**: 框架完整性 + 实践灵活性
**影响**: 确立了研究文档的组织方式

## 决策4：自我反思机制
**时间**: 2026-03-07
**决策**: 每次会话后简单反思，重大反思时告知用户
**理论依据**: 元研究 + 用户控制
**影响**: Research Agent具备自我迭代能力

## 决策5：框架仓库
**时间**: 2026-03-07
**决策**: 双仓库模式，先在当前仓库完善，再同步到框架仓库
**理论依据**: 快速迭代 + 独立演进
**影响**: Research Agent框架可独立复用

---

# Next Actions

## 下次会话重点

### 行动1：观察PM Agent实践
**前置条件**：PM Agent已创建session-log.md

**观察内容**：
- PM Agent的决策过程
- Agent协作过程
- Human-Agent交互
- 文档变化

**产出**：
- 观察笔记（使用模板）
- 发现的问题和模式

### 行动2：检索研究方法论资料
**检索方向**：
- AI Agent研究方法论
- 行动研究（Action Research）
- 设计研究（Design Research）
- 其他Agent框架的设计方法论

**产出**：
- 检索报告（使用模板）
- 关键洞察和质疑

### 行动3：继续Agent模板标准研究
**研究深度**：Level 0-2（第一性原理到设计原则）

**研究内容**：
- Agent的本质定义
- Agent的核心属性
- Agent的行为标准
- Agent模板设计

---

# Open Questions

## 待用户回答的问题

### 问题1：PM Agent观察要求
你准备好传递给PM Agent了吗？需要我提供更详细的格式说明吗？

### 问题2：优先级
你希望下次会话先做哪个？
- A. 观察PM Agent实践（需要PM Agent先创建session-log）
- B. 检索研究方法论资料
- C. 继续Agent模板标准研究

### 问题3：框架仓库
你希望什么时候创建框架仓库？
- A. 现在（作为实验）
- B. 等待方法论在实践中验证后（推荐）

---

# Research Context

## 项目根本基础（所有研究必须基于此）

### 1. 文档化交互
- Agent间通过文档异步协作
- 质量信息应随文档流转

### 2. Agent First原则
- Agent间交互：结构化、机器可读
- Human-Agent交互：Human First

### 3. Context最小化
- 分层文档体系（Level 0/1/2）
- 质量门控不应增加启动负担

### 4. Token ROI最大化
- 最少上下文，最高信息量
- 每个Token都有价值

### 5. Human参与最小化
- PM自主性优先
- Human只按需介入

---

# Quick Reference

## 研究产出位置
```
research/
├── meta/
│   ├── framework/              # 框架内容
│   │   ├── README.md
│   │   ├── templates/          # 6个模板
│   │   └── examples/           # 会话示例
│   └── self-reflections/       # 自我反思
├── observations/               # 观察笔记（待创建）
├── retrievals/                 # 检索笔记（待创建）
├── reflections/                # 思考笔记（待创建）
├── theories/                   # 理论文档（待创建）
└── discussions/                # 探讨记录
    └── research-log.md
```

## 核心方法论成果
```
方法论突破：
1. 研究-检索-思考-探讨-反思循环
2. Human双重角色：信息传递者 vs 关键决策者
3. 研究深度：Level 0-3（从第一性原理到实现思路）
4. 元研究：对研究方法本身的研究
5. 自我迭代：持续优化研究方法
```

## 研究视角
- ✅ 框架设计层面
- ✅ 理论和方法论
- ✅ 抽象的设计思路
- ✅ 元研究（自我反思）
- ❌ 具体实施细节
- ❌ 代码实现
- ❌ 执行层操作

---

# Session Resume Guide

## 快速继续研究

### Step 1: 读取本文档
```bash
cat agents/research/CATCH_UP.md
```

### Step 2: 确认研究状态
- Current Research Focus: 当前研究什么？
- Open Questions: 哪些问题待回答？
- Next Actions: 下一步做什么？

### Step 3: 检查是否有PM Agent观察资料
```bash
cat practice/agents/pm/session-log.md
```

### Step 4: 继续研究
- 执行Next Actions
- 创建必要的文档
- 更新研究日志

---

# 今日总结（2026-03-07）

## 🎯 重大方法论突破

**方法论框架确立**：
- ✅ 观察-检索-思考-探讨-反思循环
- ✅ Human双重角色澄清
- ✅ 研究深度定义（Level 0-3）
- ✅ 元研究和自我反思机制

**完整产出**：
- ✅ AGENTS.md更新
- ✅ 框架README
- ✅ 6个模板文件
- ✅ 会话示例
- ✅ 自我反思文档

## 📊 研究进展

**完成度**:
- Research Agent方法论：✅ 完成
- 文档体系：✅ 完成
- 模板设计：✅ 完成
- PM Agent观察机制：🔄 待传递
- 框架仓库：🔜 待创建

**产出文档**: 9份高质量文档

**方法论深度**: Level 2（设计原则层）

## 🔜 下次重点

**按优先级**：
1. 观察PM Agent实践（待session-log创建）
2. 检索研究方法论资料
3. 继续Agent模板标准研究

---

**维护者**: Research Agent  
**更新时间**: 2026-03-07  
**会话标识**: research-methodology-design  
**同步状态**: 已更新  
**下次重点**: 观察PM Agent实践 + 检索方法论资料
