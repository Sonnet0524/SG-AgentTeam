---
agent: research
status: Active
last_update: 2026-03-07
session: search-r-methodology
---

# Current Research Focus

**Research Direction**: Agent社会架构理论体系构建 + SEARCH-R方法论实践

**Active Topics**:
1. ✅ **Agent系统架构理论** - 已完成：四层架构清晰定义
2. ✅ **质量门控分层定义** - 已突破：元认知意识 + Skills化
3. ✅ **SEARCH-R方法论** - 已确立：完整命名和流程
4. 🔜 **Agent模板标准** - 待研究：定义与行为标准

**Current Phase**: 核心理论框架已完成，准备实践验证

---

# Recent Observations

## 重大方法论确立（2026-03-07）

### 突破：SEARCH-R方法论正式命名

**方法论命名**：
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

**命名理由**：
- Search（搜索）+ Reflect（反思）
- 符合研究本质：不断搜索真理
- 避免与强化学习（RL）混淆

**仓库重命名**：
- GitHub仓库：research-agent → search-r
- 本地目录：已完成重命名
- README：已更新
S - Survey（观察调研）
E - Explore（探索检索）
A - Analyze（分析思考）
R - Review（评审探讨）
C - Confirm（确认验证）
H - Harvest（收获产出）
R - Reflect（反思迭代）

循环：S → E → A → R → C → H → R → (回到S)
```

**关键特征**：
- 明确的研究循环
- 每个阶段都有清晰的任务
- 自然形成闭环

---

### 突破2：Agent系统架构理论

**完整架构**：
```
Agent系统 = 身份层 + 能力系统 + 记忆系统 + 访问系统

身份层：AGENTS.md（角色定义 + 核心能力）

能力系统：
  核心能力：定义在AGENTS.md中，不可分离
  通用能力：Skills，可复用、按需加载

记忆系统：
  身份记忆：AGENTS.md
  状态记忆：CATCH_UP.md
  经验记忆：experiences/
  会话记忆：session-log.md

访问系统：
  记忆索引：memory-index.yaml
  检索机制：按需加载
  压缩机制：短期→长期
```

**关键洞察**：记忆系统 ≠ 访问系统
- 记忆 = 内容本身
- 索引 = 检索方法

---

### 突破3：质量门控分层定义

**完整定义**：
```
质量门控 = 元认知意识 + 评估规则 + 评估工具

元认知意识（不可分离）：
  定义在AGENTS.md中
  "我知道自己什么时候不知道"
  Agent的核心属性

评估规则（可Skills化）：
  定义在Skills中
  确定性、可接受性、混淆判断规则
  可配置的标准

评估工具（可Skills化）：
  定义在Skills中
  质量门控Schema、评估流程
  可复用的工具
```

**关键区分**：
- 元认知意识 → Agent核心属性（不分离）
- 评估规则 + 工具 → 可Skills化（按需加载）

---

### 突破4：Agent vs Subagent正确定义

**区分标准**：决策自主性（不是文档完整性）

```
Agent（有自主权）：
  - 可以自主决策
  - 独立的任务空间
  - 对结果负责
  示例：PM Agent、Research Agent

Subagent（无自主权）：
  - 任务绑定
  - 决策受限
  - 执行分配的任务
  示例：AI Team、Core Team、Integration Team
```

**关键洞察**：
- 不是"有没有文档"决定Agent vs Subagent
- 而是"有没有自主权"决定
- Subagent也可以有完整的三层记忆

---

### 突破5：Skills分离原则

**三大原则**：
```
原则1：非每次都需要 → 可以Skills化
原则2：可多个Agent复用 → 应该Skills化
原则3：相对独立的能力单元 → 可以Skills化
```

**Skills分类**：
- 决策支持类：quality-gate、risk-assessment
- 工作流类：git-workflow、review-process
- 规范类：coding-standards、documentation-guide
- 领域知识类：embedding-models、vector-search

**AGENTS.md精简原则**：
- 只保留：身份 + 核心能力
- Skills化：通用能力
- 目标：~5k tokens

---

### 突破6：记忆系统 vs 访问系统

**关键区分**：
```
记忆系统（内容）：
  性质：存储信息内容本身
  类比：图书馆的书

访问系统（方法）：
  性质：检索内容的方法
  类比：图书馆目录

索引 ≠ 记忆
索引是"目录"，不是"内容"
索引是"方法"，不是"记忆"
```

**理论价值**：
- 避免混淆"记忆层"与"访问方法"
- 避免过度设计（索引的索引的索引...）
- 建立清晰的系统架构边界

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
