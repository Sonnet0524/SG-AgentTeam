# Agent Team 设计思路

> 记录整个Agent团队的设计理念、架构和工作方式

**版本**: v1.0  
**日期**: 2026-03-06  
**状态**: Active

---

## 一、设计理念

### 1.1 核心原则

#### Agent First vs Human First

**Agent First原则**：
- 用于Agent之间的交互文档
- 格式：结构化、简洁、机器可读
- 示例：CATCH_UP.md, ESSENTIALS.md, knowledge-base/INDEX.md

**Human First原则**：
- 用于向用户汇报的文档
- 格式：人性化、易读、有温度
- 示例：HUMAN_ADMIN.md, 用户报告

**设计决策**：
```
Agent间通信 → Agent First (简洁高效)
Agent→用户 → PM转化为Human First (易懂友好)
```

#### Context窗口最小化

**目标**：最小化Agent启动时的context消耗

**策略**：
1. **分层文档**：CATCH_UP (<50行) → ESSENTIALS (<100行) → guides (可选)
2. **按需披露**：只读必需信息，详细指南按需加载
3. **索引机制**：知识库通过索引快速检索，不预加载

**效果**：
- Context使用：从~600行降至~40行
- 节省：**93%**

---

### 1.2 上下文边界隔离

**定义**：每个Agent的模块完全不重叠，零交叉修改

**目的**：
- 避免冲突
- 清晰职责
- 独立开发

**实现**：
- 每个Agent负责独立的目录和文件
- 通过public API交互
- 数据流单向

---

## 二、团队架构

### 2.1 Agent角色定义

#### Data Agent (数据专家)

**职责**：
- 数据类型定义（DocumentMetadata, Document等）
- 数据解析器（YAML parser, metadata parser等）
- 工具函数（file ops, data ops, text ops等）
- 数据工具（organize, index, search等）

**模块**：
```
scripts/
├── core/          # 类型定义、Schema、验证器
├── parsers/       # 解析器
├── utils/         # 工具函数
└── tools/         # 数据工具
```

**依赖关系**：
- 无外部依赖（基础层）
- 其他Agent可依赖Data的public API

**特点**：
- 纯数据处理
- 无业务逻辑
- 通用性强

---

#### Template Agent (模板专家)

**职责**：
- 模板引擎（加载、渲染、继承等）
- 配置系统（配置加载、验证、管理）
- 文档创建工具
- 模板文件维护

**模块**：
```
scripts/
├── template/      # 模板引擎核心
├── config/        # 配置管理
└── tools/         # 文档创建工具

templates/         # 模板文件（5个模板）
```

**依赖关系**：
- 依赖：Data Agent的类型定义（DocumentMetadata）
- 提供：模板渲染接口

**特点**：
- 格式化输出
- 可配置性强
- 用户可见

---

#### Test Agent (质量专家)

**职责**：
- 测试框架搭建
- 单元测试、集成测试
- 测试报告生成
- 代码质量审查

**模块**：
```
tests/
├── unit/          # 单元测试
├── integration/   # 集成测试
└── reports/       # 测试报告

test-data/         # 测试数据
```

**依赖关系**：
- 测试所有Agent代码
- 独立运行，不修改代码

**特点**：
- 质量保证
- 独立客观
- 全覆盖测试

---

#### PM Agent (协调专家)

**职责**：
- 项目规划（Phase、Checkpoint、Task）
- 进度跟踪（token-based）
- 代码审查
- 团队协调
- 用户交互

**模块**：
```
project-management/  # 项目规划文档
agent-status.md      # 状态跟踪
HUMAN_ADMIN.md       # 用户总览
```

**依赖关系**：
- 监控所有Agent
- 不开发代码
- 只Review和管理

**特点**：
- 全局视角
- 决策中心
- 用户桥梁

---

### 2.2 协作关系图

```
┌─────────────────────────────────────────────────┐
│                    User                          │
│                  (Human)                         │
└───────────────────┬─────────────────────────────┘
                    │ Human First
                    ↓
            ┌───────────────┐
            │   PM Agent    │ ← 协调、决策
            │   (Manager)   │
            └───┬───┬───┬───┘
                │   │   │
       ┌────────┘   │   └────────┐
       │            │            │
       ↓            ↓            ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│   Data   │  │ Template │  │   Test   │
│  Agent   │  │  Agent   │  │  Agent   │
│ (基础层) │  │ (应用层) │  │ (质量层) │
└─────┬────┘  └────┬─────┘  └────┬─────┘
      │            │             │
      └────────────┴─────────────┘
            Agent First
          (结构化通信)
```

**依赖方向**：
- Data → 无依赖（基础层）
- Template → Data（应用层）
- Test → All（质量层）
- PM → All（管理层）

---

## 三、工作流程

### 3.1 Agent启动流程

```
1. 启动OpenCode
   opencode --agent <agent-name>

2. 读取必需文档（<50行）
   - agents/<name>/CATCH_UP.md
   - agent-status.md (可选)

3. 了解当前状态
   - Status: Active/Idle/Blocked
   - Current Task: 当前任务
   - Constraints: 模块边界

4. 开始工作
   - 切换到工作仓库
   - 拉取最新代码
   - 查看分配的Issues

5. 按需加载详细信息
   - ESSENTIALS.md (核心职责)
   - guides/ (详细指南)
   - knowledge-base/ (经验参考)
```

**Context消耗**：
- 必需：~1,000 tokens (CATCH_UP)
- 按需：+2,000 tokens (ESSENTIALS)
- 可选：不定 (guides, knowledge-base)

---

### 3.2 任务执行流程

```
1. 认领任务
   - 查看GitHub Issues
   - 确认模块归属
   - Comment: "Starting work"

2. 更新状态
   - 更新agent-status.md
   - 设置Status: 🟢 Active
   - 记录Current Task

3. 创建分支
   git checkout -b <feature|test|data>-<task-name>

4. TDD开发
   - 编写测试
   - 实现功能
   - 运行测试
   - 确保覆盖率>80%

5. 提交代码
   - 规范commit message
   - git push到分支
   - 创建Pull Request

6. 等待Review
   - PM Review代码
   - 响应feedback
   - 修改直至通过

7. 合并完成
   - PM合并PR
   - 更新agent-status.md
   - Status: 🟡 Idle

8. 经验总结
   - 记录经验到knowledge-base
   - 更新CATCH_UP.md
```

---

### 3.3 Token-Based进度管理

**时间单位定义**：

| 单位 | 定义 | 示例 |
|------|------|------|
| **Task** | 单个Issue | 实现YAML解析器 (1,200 tokens) |
| **Checkpoint** | 相关Tasks集合 | 元数据解析器 (5,000 tokens) |
| **Phase** | 功能模块 | 核心数据系统 (15,000 tokens) |

**进度跟踪**：

```
Phase 1: 核心数据系统 (15,000 tokens)
├── Checkpoint 1.1: 类型系统 (3,000 tokens) ✅
│   ├── Task 001: DocumentMetadata (500 tokens) ✅
│   └── Task 002: Document类型 (400 tokens) ✅
├── Checkpoint 1.2: 解析器 (5,000 tokens) ✅
└── Checkpoint 1.3: 工具函数 (7,000 tokens) ⏳
    └── Task 009: 文件操作 (1,500 tokens) ✅

Progress: 11,000 / 15,000 (73%)
Velocity: 1,200 tokens/hour
ETA: ~3 hours to complete
```

**优势**：
- 精确预估工作量
- 实时进度跟踪
- 准确ETC预测
- 不依赖自然时间

---

## 四、管理机制

### 4.1 状态管理

#### agent-status.md（Token-Based）

**结构**：
```markdown
## Data Agent
- Status: 🟢 Active / 🟡 Idle / 🔴 Blocked
- Current: Checkpoint 1.3 - Task 009
- Progress: 11,000 / 15,000 tokens (73%)
- Velocity: 1,200 tokens/hour
- Blockers: None
- Next: Complete remaining tasks
```

**更新时机**：
- 开始任务时
- 完成checkpoint时
- 遇到阻塞时
- 变为idle时

---

### 4.2 知识管理

#### knowledge-base/结构

```
knowledge-base/
├── INDEX.md              # 索引（快速检索）
├── experiences/          # 经验库
│   ├── data/            # Data Agent经验
│   ├── template/        # Template Agent经验
│   └── test/            # Test Agent经验
├── decisions/            # 决策库
└── patterns/             # 模式库
```

**按需披露机制**：
1. 查看INDEX.md了解可用知识
2. 根据需要读取具体文件
3. 不启动时不加载任何知识库内容

**贡献机制**：
```markdown
完成重要任务后：
1. 总结问题和解决方案
2. 创建experience文档
3. 提交到knowledge-base/experiences/<agent>/
4. 更新INDEX.md
```

---

### 4.3 决策机制

#### 决策流程

```
1. 发现问题
   - Agent遇到阻塞
   - 技术方案分歧
   - 资源冲突

2. 上报PM
   - Issue comment描述问题
   - 更新agent-status.md → 🔴 Blocked

3. PM评估
   - 收集信息
   - 咨询相关Agent
   - 评估选项

4. 做出决策
   - 选择最优方案
   - 记录rationale
   - 创建decision文档

5. 执行决策
   - 通知相关Agent
   - 解决阻塞
   - 继续工作
```

#### 决策记录格式

```markdown
---
id: DR-token:NNNNN
date: YYYY-MM-DD
status: accepted
deciders: [PM, Data, Template]
---

## Context
决策背景和问题

## Decision
决策内容

## Rationale
决策理由

## Alternatives
考虑过的其他方案

## Impact
决策影响

## Implementation
实施步骤
```

---

### 4.4 用户交互

#### Human First原则

**PM职责**：
- 将技术信息转化为用户易懂内容
- 定期生成用户友好报告
- 重大决策征求用户意见
- 风险和问题及时提醒

**报告格式**：
```markdown
# 项目周报

## 🎯 本周亮点
- 主要成果
- 关键进展

## 📊 进度总览
- 完成功能
- 修复Bug
- 测试覆盖率

## 💡 经验总结
- 我们学到了什么
- 最佳实践

## 🔄 下周计划
- 重点任务
- 预期成果

## ⚠️ 需要关注
- 潜在风险
- 待决策事项
```

---

## 五、最佳实践

### 5.1 Context优化

**DO**：
- ✅ 启动时只读CATCH_UP.md
- ✅ 按需读取ESSENTIALS.md
- ✅ 使用索引检索knowledge-base
- ✅ 详细信息放在guides/

**DON'T**：
- ❌ 启动时读取所有文档
- ❌ 预加载knowledge-base内容
- ❌ 在CATCH_UP中包含详细指南

---

### 5.2 模块边界维护

**DO**：
- ✅ 只修改自己负责的模块
- ✅ 通过public API使用其他Agent模块
- ✅ 遇到边界问题立即上报PM
- ✅ 保持接口稳定性

**DON'T**：
- ❌ 跨越模块边界修改代码
- ❌ 直接访问其他Agent的内部实现
- ❌ 破坏现有public API
- ❌ 忽略模块归属问题

---

### 5.3 Token-Based工作

**DO**：
- ✅ 准确估算任务token消耗
- ✅ 实时记录token使用
- ✅ 监控velocity趋势
- ✅ 调整预估偏差

**DON'T**：
- ❌ 使用自然日/周估算
- ❌ 忽略token消耗统计
- ❌ 不更新进度信息

---

### 5.4 知识沉淀

**DO**：
- ✅ 完成重要任务后总结经验
- ✅ 记录遇到的问题和解决方案
- ✅ 贡献到knowledge-base
- ✅ 更新索引

**DON'T**：
- ❌ 完成任务后不总结
- ❌ 经验只留在Issue comment中
- ❌ 知识库长期不更新

---

## 六、工具和配置

### 6.1 OpenCode配置

**opencode.json**：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "data": {
      "description": "Data - 数据类型、解析器和工具",
      "mode": "primary",
      "prompt": "{file:./agents/data/CATCH_UP.md}",
      "permission": {
        "edit": "ask",
        "bash": {
          "git push": "ask",
          "pytest *": "allow",
          "black *": "allow"
        }
      }
    },
    "template": { ... },
    "test": { ... },
    "pm": { ... }
  }
}
```

**关键配置**：
- `prompt`: 指向CATCH_UP.md（最小context）
- `permission`: 不同Agent不同权限
- `mode`: 所有Agent都是primary（可独立工作）

---

### 6.2 GitHub Labels

**Agent Labels**：
- `agent: data` - Data Agent任务
- `agent: template` - Template Agent任务
- `agent: test` - Test Agent任务

**Type Labels**：
- `type: feature` - 新功能
- `type: bug` - Bug修复
- `type: test` - 测试任务
- `type: docs` - 文档任务

**Priority Labels**：
- `priority: critical` - 紧急
- `priority: high` - 高优先级
- `priority: medium` - 中优先级
- `priority: low` - 低优先级

---

### 6.3 文件组织

**Dev仓库**（知识-assistant-dev）：
```
agents/              # Agent配置
project-management/  # 项目规划
knowledge-base/      # 知识库
interaction-logs/    # 交互记录
agent-status.md      # 状态跟踪
HUMAN_ADMIN.md       # 用户总览
opencode.json        # OpenCode配置
```

**Main仓库**（knowledge-assistant）：
```
scripts/             # 代码
tests/               # 测试
templates/           # 模板
docs/                # 文档
test-data/           # 测试数据
```

---

## 七、演化方向

### 7.1 短期优化（1-2周）

1. **完善guides文档**
   - 为每个agent创建详细的开发指南
   - 补充最佳实践和示例

2. **填充knowledge-base**
   - 迁移现有经验到知识库
   - 建立模式库

3. **优化token估算**
   - 调整预估模型
   - 提高准确性

---

### 7.2 中期优化（1-2月）

1. **自动化工具**
   - Token统计脚本
   - 知识库检索工具
   - 报告生成器

2. **智能推荐**
   - Agent启动时推荐相关经验
   - 任务分配时推荐最佳实践
   - 问题解决时推荐类似案例

3. **质量提升**
   - 完善测试体系
   - 提升覆盖率
   - 建立质量门禁

---

### 7.3 长期愿景（3-6月）

1. **知识图谱**
   - 建立经验关联网络
   - 可视化知识结构
   - 智能知识检索

2. **自适应管理**
   - 根据velocity自动调整计划
   - 预测风险和阻塞
   - 优化资源分配

3. **团队扩展**
   - 支持更多Agent角色
   - 动态团队组建
   - 跨项目协作

---

## 八、经验教训

### 8.1 已验证的最佳实践

1. **Context最小化至关重要**
   - 93%的context节省显著提升效率
   - 分层文档是有效策略

2. **Token-based管理更精确**
   - 比自然时间更适合Agent工作模式
   - 有助于准确预估和跟踪

3. **边界隔离避免冲突**
   - 清晰的模块归属
   - 单向依赖关系
   - 零冲突可能

4. **知识沉淀要持续**
   - 即时总结经验
   - 按需检索机制
   - 避免重复踩坑

---

### 8.2 需要改进的地方

1. **Token估算准确性**
   - 需要更多数据校准
   - 考虑任务复杂度

2. **知识库利用率**
   - 目前内容较少
   - Agent主动性待提升

3. **跨Agent协作**
   - 集成测试需要加强
   - 接口定义需要更明确

---

## 九、总结

### 核心创新

1. **Agent First原则** - 为机器设计，简洁高效
2. **Context最小化** - 93%节省，按需披露
3. **Token-Based管理** - 精确跟踪，不依赖自然时间
4. **边界完全隔离** - 零冲突，清晰职责

### 关键收益

- **效率提升**：Context使用↓93%
- **质量保证**：100%边界隔离
- **可维护性**：清晰架构和流程
- **可扩展性**：易于添加新Agent

### 适用场景

- ✅ AI Agent协作开发
- ✅ 多模块并行开发
- ✅ 需要精确进度跟踪
- ✅ 知识密集型项目

---

**维护者**: PM Agent  
**更新频率**: 有重大改进时更新  
**相关文档**: REFACTOR_REPORT.md, project-management/phases.md
