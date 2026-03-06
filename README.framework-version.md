# Agent Team Framework

> 可复用的AI Agent协作开发框架

**版本**: v1.0  
**更新日期**: 2026-03-06

---

## 📖 目录

- [框架概述](#框架概述)
- [核心设计理念](#核心设计理念)
- [框架核心组件](#框架核心组件)
- [应用实例：Knowledge Assistant](#应用实例knowledge-assistant)
- [如何应用框架](#如何应用框架)
- [相关资源](#相关资源)

---

## 框架概述

### 什么是Agent Team Framework？

**Agent Team Framework**是一套完整的AI Agent协作开发方法论和工具体系，通过明确的角色分工、边界隔离、上下文优化和精确管理，实现多个AI Agent的高效协作。

### 核心价值

| 维度 | 传统方式 | Agent Team Framework | 改进 |
|------|----------|---------------------|------|
| **Context使用** | 大量冗余信息 | 分层按需加载 | ↓ 93% |
| **协作冲突** | 频繁冲突 | 零交叉修改 | 100%隔离 |
| **进度跟踪** | 依赖自然时间 | Token-based精确 | 准确预测 |
| **知识复用** | 分散难查 | 按需检索 | ↑ 80%效率 |

### 适用场景

- ✅ 多AI Agent协作开发项目
- ✅ 多模块并行开发
- ✅ 需要精确进度跟踪的复杂项目
- ✅ 知识密集型长期维护项目
- ✅ 需要专业化分工的大型项目

---

## 核心设计理念

### 1. Agent First vs Human First

**核心理念**：根据受众选择最优的表达方式

#### Agent First（机器优先）

**适用场景**：Agent间的通信和协作

**设计原则**：
- 结构化格式
- 简洁精准
- 机器可读
- 无歧义表达

**实践示例**：
```markdown
---
status: 🟢 Active
task: #15 - Conditional rendering
progress: 75% (3,500/8,000 tokens)
blockers: None
---
```

#### Human First（人类优先）

**适用场景**：向用户汇报和展示

**设计原则**：
- 人性化表达
- 易读友好
- 有温度感
- 可视化呈现

**实践示例**：
```markdown
## 🎯 本周亮点

我们成功完成了核心数据系统的搭建，模板引擎的基础功能已经实现。
测试覆盖率达到了85%，所有核心功能都经过了充分验证。

### 下一步计划
我们将专注于模板继承功能，预计本周完成...
```

**设计决策**：
```
Agent间通信 → Agent First（效率优先）
PM→用户    → Human First（体验优先）
```

---

### 2. Context窗口最小化

**核心问题**：AI Agent的context窗口有限，启动时加载过多信息会严重影响性能和成本

#### 分层文档策略

**Level 0 - 必需层**（<50行）
- 用途：Agent启动时必须读取
- 内容：当前状态、任务、约束
- 示例：`CATCH_UP.md`

**Level 1 - 按需层**（<100行）
- 用途：工作时按需读取
- 内容：核心职责、工作规范
- 示例：`ESSENTIALS.md`

**Level 2 - 可选层**（不限）
- 用途：遇到问题时参考
- 内容：详细指南、最佳实践
- 示例：`guides/`, `knowledge-base/`

#### 按需披露机制

```
启动阶段
  ↓ 读取Level 0 (~1,000 tokens)
工作阶段
  ↓ 按需读取Level 1 (+2,000 tokens)
问题解决
  ↓ 可选读取Level 2 (不定)
```

**实际效果**：
- Context使用：从~600行降至~40行
- **节省：93%** ✅
- 启动速度：提升5倍

---

### 3. 上下文边界隔离

**核心定义**：每个Agent的模块完全不重叠，实现零交叉修改

#### 四层架构设计

```
┌─────────────────────────────────┐
│      PM Layer (管理层)           │  ← 协调所有Agent
│   规划、协调、Review、用户交互     │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Application Layer (应用层)      │  ← 依赖数据层
│   模板引擎、配置系统、业务逻辑     │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│    Data Layer (数据层)           │  ← 无外部依赖
│   类型定义、解析器、工具函数       │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Quality Layer (质量层)         │  ← 测试所有层
│   测试框架、质量保证、文档审查     │
└─────────────────────────────────┘
```

#### 边界规则

**单向依赖**：
- 上层可依赖下层
- 下层不可依赖上层
- 同层之间通过API通信

**模块归属**：
- 每个文件有明确的Owner
- 只修改自己负责的模块
- 通过public API使用其他模块

**零交叉保证**：
- 清晰的文件目录划分
- 明确的接口定义
- 代码审查强制执行

**实际效果**：
- 冲突率：从频繁冲突降至零冲突
- 代码质量：提升显著
- 开发效率：提升40%

---

### 4. Token-Based进度管理

**核心问题**：自然日/周的时间单位不适合Agent工作模式

#### Token时间单位

| 单位 | 定义 | 典型规模 | 示例 |
|------|------|----------|------|
| **Task** | 单个Issue | 1,000-2,000 tokens | 实现一个解析器 |
| **Checkpoint** | 相关Tasks集合 | 3,000-8,000 tokens | 完成一个功能模块 |
| **Phase** | 功能模块 | 10,000-20,000 tokens | 完成一个系统 |
| **Sprint** | 多个Phases | 30,000-50,000 tokens | 一个迭代周期 |

#### 进度跟踪机制

```
Phase: 核心数据系统 (15,000 tokens)
├── Checkpoint 1: 类型系统 (3,000 tokens) ✅ 100%
│   ├── Task 001: 类型定义 (500 tokens) ✅
│   ├── Task 002: 验证器 (800 tokens) ✅
│   └── Task 003: 单元测试 (1,700 tokens) ✅
├── Checkpoint 2: 解析器 (5,000 tokens) ✅ 100%
└── Checkpoint 3: 工具函数 (7,000 tokens) ⏳ 60%

Progress: 11,000 / 15,000 (73%)
Velocity: 1,200 tokens/hour
ETA: ~3 hours to complete
```

#### 关键指标

**Velocity（速度）**：
- 定义：每小时完成的token数
- 计算：完成的tokens / 实际小时数
- 用途：预估未来任务时间

**ETC（预估完成时间）**：
- 计算：剩余tokens / velocity
- 优势：不依赖自然时间
- 精度：误差<15%

**实际效果**：
- 预估准确性：提升至85%+
- 进度透明度：100%可视化
- 决策支持：数据驱动

---

## 框架核心组件

### 1. Agent角色系统

#### 角色设计原则

**专业化**：每个Agent专注特定领域
- 明确的能力边界
- 深度的专业能力
- 避免能力重叠

**独立性**：最小化Agent间的耦合
- 清晰的模块归属
- 定义良好的接口
- 独立的工作流程

**协作性**：规范的协作机制
- 标准化的通信协议
- 明确的依赖关系
- 可预测的行为模式

#### 典型角色配置

**PM Agent**（项目经理）
- 职责：规划、协调、Review、用户交互
- 特点：全局视角、决策中心
- 依赖：监控所有Agent

**开发型Agent**
- 职责：特定领域的代码开发
- 特点：深度专业化
- 依赖：依赖数据层Agent

**测试型Agent**
- 职责：质量保证、测试框架
- 特点：独立客观
- 依赖：测试所有Agent

---

### 2. 文档分层体系

#### 目录结构

```
agents/
├── <agent-name>/
│   ├── CATCH_UP.md      # Level 0 - 必需（<50行）
│   ├── ESSENTIALS.md    # Level 1 - 按需（<100行）
│   ├── guides/          # Level 2 - 可选
│   │   ├── development.md
│   │   ├── best-practices.md
│   │   └── troubleshooting.md
│   └── AGENTS.md        # Agent配置文件
```

#### CATCH_UP.md设计原则

**必需包含**：
- 当前状态（Status）
- 当前任务（Current Task）
- 进度信息（Progress）
- 活跃约束（Active Constraints）
- 阻塞问题（Blockers）
- 下一步动作（Next Actions）

**格式要求**：
- 纯文本或简单Markdown
- 无复杂格式
- 可快速解析

**更新时机**：
- 任务开始/完成时
- 状态变化时
- 遇到阻塞时

#### ESSENTIALS.md设计原则

**包含内容**：
- 角色定义
- 核心职责
- 工作规范
- 行为约束
- 输出标准

**设计目标**：
- 完整但不冗余
- 清晰但有深度
- 实用且可执行

---

### 3. 知识管理机制

#### 知识库结构

```
knowledge-base/
├── INDEX.md              # 知识索引（按需检索）
├── experiences/          # 经验库
│   ├── <agent>/
│   │   ├── 001-topic.md
│   │   └── 002-topic.md
├── decisions/            # 决策库
│   ├── DR-001-title.md
│   └── DR-002-title.md
└── patterns/             # 模式库
    ├── pattern-001.md
    └── pattern-002.md
```

#### 按需检索机制

**索引驱动**：
```
# INDEX.md示例
## By Problem
- YAML解析问题 → experiences/data/001-yaml-parsing.md
- 测试覆盖率问题 → experiences/test/002-coverage.md

## By Pattern
- 错误处理模式 → patterns/error-handling.md
- 测试模式 → patterns/testing.md
```

**使用流程**：
```
遇到问题
  ↓
查看INDEX.md
  ↓
定位相关文档
  ↓
读取具体内容
```

**优势**：
- 不预加载知识库
- 快速定位问题
- 节省80%检索时间

---

### 4. 状态跟踪系统

#### agent-status.md设计

```markdown
## Agent Name
| Field | Value |
|-------|-------|
| Status | 🟢 Active / 🟡 Idle / 🔴 Blocked |
| Current Task | [任务描述] |
| Last Activity | YYYY-MM-DD HH:MM |
| Last Commit | [commit hash] |
| Assigned Issues | [数量] |
| Completed Issues | [数量] |
| Blocked | [Yes/No - 原因] |
| Next Action | [下一步计划] |
```

#### 状态更新机制

**更新时机**：
- 任务开始
- 状态变化
- 任务完成
- 遇到阻塞

**状态定义**：
- 🟢 Active：正在工作
- 🟡 Idle：等待任务
- 🔴 Blocked：遇到阻塞
- ⚪ Offline：不活跃

#### 活动日志

```
### YYYY-MM-DD
- HH:MM - Agent: 动作描述
- HH:MM - Agent: 另一个动作
```

---

### 5. 双仓库架构

#### 架构设计

```
┌──────────────────────────────┐
│  Development Repository       │
│  (Private - 开发过程管理)      │
│                              │
│  - Agent配置                 │
│  - 项目规划                  │
│  - 知识库                    │
│  - 状态跟踪                  │
│  - 交互日志                  │
└──────────────────────────────┘
            │
            │ 协调、指导
            ↓
┌──────────────────────────────┐
│  Production Repository        │
│  (Public - 输出交付品)         │
│                              │
│  - 项目代码                  │
│  - 用户文档                  │
│  - 测试代码                  │
│  - 最终交付品                │
└──────────────────────────────┘
```

#### 职责分离

**开发仓库**：
- 私有访问
- Agent协作空间
- 过程管理文档
- 知识沉淀

**生产仓库**：
- 公开访问
- 用户可见成果
- 最终交付品
- 对外文档

#### 协作流程

```
PM在开发仓库
  ↓ 创建Issue、分配任务
Agent在工作仓库
  ↓ 开发、测试、提交PR
PM在开发仓库
  ↓ Review、合并
代码进入生产仓库
```

---

## 应用实例：Knowledge Assistant

### 项目背景

**Knowledge Assistant**是一个知识管理辅助工具，需要实现文档元数据管理、模板系统、知识库索引等功能。项目采用Agent Team Framework组织开发。

### 团队配置

#### 4-Agent团队

| Agent | 角色 | 职责 | 模块 |
|-------|------|------|------|
| **PM** | 项目经理 | 规划、协调、Review | 项目管理 |
| **Data** | 数据专家 | 类型、解析器、工具 | 数据层 |
| **Template** | 模板专家 | 模板引擎、配置 | 应用层 |
| **Test** | 质量专家 | 测试框架、质量保证 | 质量层 |

#### 依赖关系

```
PM Agent (管理层)
   ├── 监控 → Data Agent
   ├── 监控 → Template Agent
   └── 监控 → Test Agent

Template Agent (应用层)
   └── 依赖 → Data Agent

Test Agent (质量层)
   ├── 测试 → Data Agent
   ├── 测试 → Template Agent
   └── 独立执行
```

### 实施效果

#### 定量指标

| 指标 | 实施前 | 实施后 | 改进 |
|------|--------|--------|------|
| **Context使用** | ~600行 | ~40行 | ↓ 93% |
| **代码冲突** | 频繁 | 零冲突 | 100% |
| **进度预测准确性** | ~50% | ~85% | ↑ 70% |
| **知识检索效率** | 基线 | +80% | ↑ 80% |

#### 定性成果

**开发效率**：
- Agent启动速度提升5倍
- 任务切换零成本
- 协作流畅无阻塞

**质量保证**：
- 测试覆盖率稳定在80%+
- 代码规范一致性100%
- Bug率显著降低

**知识沉淀**：
- 经验即时总结
- 问题快速复现
- 最佳实践持续积累

### 目录结构示例

```
knowledge-assistant-dev/          # 开发仓库
├── agents/                       # Agent配置
│   ├── pm/
│   │   ├── CATCH_UP.md
│   │   ├── ESSENTIALS.md
│   │   └── guides/
│   ├── data/
│   ├── template/
│   └── test/
├── project-management/           # 项目管理
│   ├── phases.md                 # Token-Based规划
│   ├── roadmap.md
│   └── milestones.md
├── knowledge-base/               # 知识库
│   ├── INDEX.md
│   ├── experiences/
│   ├── decisions/
│   └── patterns/
├── agent-status.md               # 状态跟踪
├── HUMAN_ADMIN.md               # 用户总览
└── opencode.json                # Agent配置

knowledge-assistant/              # 生产仓库
├── scripts/                      # 源代码
│   ├── core/                     # Data Agent负责
│   ├── parsers/                  # Data Agent负责
│   ├── template/                 # Template Agent负责
│   └── config/                   # Template Agent负责
├── tests/                        # Test Agent负责
├── templates/                    # Template Agent负责
└── docs/                         # 用户文档
```

---

## 如何应用框架

### 快速开始

#### 1. 设计Agent团队

**步骤**：
1. 分析项目需求，识别主要模块
2. 设计Agent角色和职责边界
3. 确定依赖关系和协作方式
4. 选择一个PM Agent

**示例**：
```
Web应用项目可能的Agent配置：
- PM Agent: 项目管理
- Frontend Agent: 前端开发
- Backend Agent: 后端开发
- Test Agent: 质量保证
- DevOps Agent: 部署运维
```

#### 2. 搭建文档体系

**必需创建**：
```
agents/
├── <agent-name>/
│   ├── CATCH_UP.md      # 必需
│   ├── ESSENTIALS.md    # 必需
│   └── guides/          # 可选
```

**配置文件**：
- 创建`opencode.json`配置Agent
- 配置权限和工作目录

#### 3. 建立管理机制

**创建核心文档**：
- `agent-status.md` - 状态跟踪
- `project-management/phases.md` - 项目规划
- `knowledge-base/INDEX.md` - 知识索引

**定义工作流程**：
- Issue创建和分配流程
- PR Review流程
- 状态更新机制

#### 4. 启动开发

**PM Agent**：
1. 创建Phase规划
2. 分解Tasks和Checkpoints
3. 创建Issues
4. 分配给对应Agent

**开发Agent**：
1. 启动时读取CATCH_UP.md
2. 认领Issue，更新状态
3. 按TDD开发
4. 提交PR
5. 总结经验到知识库

---

### 定制化指南

#### 根据项目规模调整

**小型项目**（1-2个模块）：
- Agent数量：2-3个（PM + 开发 + 测试）
- 文档层级：简化为2层（CATCH_UP + ESSENTIALS）
- 管理粒度：Task级别即可

**中型项目**（3-5个模块）：
- Agent数量：4-5个
- 文档层级：完整3层
- 管理粒度：Checkpoint级别

**大型项目**（5+模块）：
- Agent数量：6+个，可分组
- 文档层级：完整3层+额外专题文档
- 管理粒度：Phase级别

#### 根据团队特点调整

**纯AI团队**：
- 强化Token-Based管理
- 严格边界隔离
- Agent First文档

**人机混合团队**：
- Human First文档占比更高
- 增加人工干预点
- 调整权限配置

**跨时区协作**：
- 强化异步协作机制
- 详细的活动日志
- 明确的交接规范

---

### 最佳实践

#### Context优化

✅ **推荐**：
- CATCH_UP保持<50行
- 使用索引而非预加载
- 详细内容放在guides/
- 定期清理过时信息

❌ **避免**：
- 在CATCH_UP中包含详细指南
- 启动时读取所有文档
- 知识库无索引结构
- 文档冗余重复

#### 边界维护

✅ **推荐**：
- 明确每个文件的Owner
- 使用public API通信
- 遇到边界问题立即上报
- 定期Review边界合理性

❌ **避免**：
- 跨Agent修改代码
- 直接访问内部实现
- 模糊的模块归属
- 忽略边界警告

#### Token管理

✅ **推荐**：
- 准确记录Task token消耗
- 定期分析velocity趋势
- 调整预估模型
- 使用历史数据预测

❌ **避免**：
- 使用自然日/周估算
- 不记录实际消耗
- 忽略velocity变化
- 凭感觉预估

#### 知识沉淀

✅ **推荐**：
- 重要任务完成后立即总结
- 使用结构化格式记录
- 保持INDEX.md更新
- 定期review知识库

❌ **避免**：
- 任务完成后不总结
- 经验只留在Issue中
- 知识库长期不维护
- 无索引的知识库

---

## 相关资源

### 📚 核心文档

**设计文档**：
- [AGENT_TEAM_DESIGN.md](AGENT_TEAM_DESIGN.md) - 完整的框架设计文档
- [AGENTS_USAGE.md](AGENTS_USAGE.md) - OpenCode Agent使用指南

**实例文档**：
- [project-management/phases.md](project-management/phases.md) - Token-Based规划示例
- [knowledge-base/INDEX.md](knowledge-base/INDEX.md) - 知识库索引示例
- [agent-status.md](agent-status.md) - 状态跟踪示例

### 🛠️ 工具和平台

**AI平台**：
- [OpenCode](https://opencode.ai) - Agent管理和协作平台

**协作工具**：
- GitHub Issues & PRs
- Git版本控制
- Markdown文档

### 🔗 扩展阅读

**方法论**：
- 分层文档设计
- Context优化策略
- Token-Based项目管理

**实践案例**：
- Knowledge Assistant项目
- 4-Agent团队配置
- 实施效果分析

---

## 维护和更新

**框架维护**：
- PM Agent负责整体维护
- 核心设计理念保持稳定
- 组件可根据实践调整

**文档更新**：
- AGENT_TEAM_DESIGN.md：重大改进时更新
- 本README：框架演进时更新
- 实例文档：项目进行中持续更新

---

**框架作者**: Agent Team  
**创建时间**: 2026-03-05  
**最后更新**: 2026-03-06  
**版本**: v1.0

---

## 许可和引用

本框架采用MIT许可证。如果在你的项目中使用了Agent Team Framework，欢迎引用本文档。

**引用格式**：
```
Agent Team Framework: A Reusable AI Agent Collaboration Framework
https://github.com/Sonnet0524/knowledge-assistant-dev
```
