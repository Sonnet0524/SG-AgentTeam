---
date: 2026-03-07
observer: Research Agent
subject: Agent Team Collaboration Pattern - PM启动与管理模式
method: Survey + Analyze
depth: Level 2 (Design Principles)
---

# 观察笔记：Agent Team协作模式

## S - Survey（观察调研）

### 观察对象
- **项目**: Knowledge Assistant v1.1
- **时间范围**: 2026-03-06 ~ 2026-03-07
- **观察重点**: PM Agent对其他Agent的启动、管理模式

### 观察方法
1. **文档分析**: 阅读PM、AI、Core、Integration、Test Agent的AGENTS.md
2. **状态追踪**: 分析agent-status.md、session-log.md、task-assignments
3. **流程观察**: 查看启动脚本、工作分配文档、沟通总结
4. **案例研究**: Sprint 2代码缺失事件的完整处理流程

---

## E - Explore（探索检索）

### 关键文档检索

#### 1. PM Agent核心配置
- **AGENTS.md** (153行) - PM角色定义和行为准则
- **CATCH_UP.md** (285行) - PM当前状态和工作流程
- **session-log.md** (184行) - PM实际工作记录

#### 2. Team配置文档
- **AI Team**: AGENTS.md (252行) - 向量嵌入和语义搜索
- **Core Team**: AGENTS.md (168行) - 核心数据处理
- **Integration Team**: AGENTS.md (323行) - opencode集成
- **Test Team**: AGENTS.md (142行) - 测试质量保证

#### 3. 状态和任务文档
- **agent-status.md** (521行) - 团队状态总览
- **v1.1-task-assignments.md** (533行) - 详细任务分配
- **WORK-ASSIGNMENT.md** (250行) - PM工作安排
- **COMMUNICATION-SUMMARY.md** (164行) - 沟通指令总结

---

## A - Analyze（分析思考）

### 核心发现

#### 1. PM的启动和管理模式

**被动响应模式**：
```
PM工作模式：
- 🔕 不主动监测Agent状态
- ✅ 等待用户询问触发工作
- 📊 多Agent管理（协调并行工作的多个Agent）
```

**关键洞察**：
- PM不是"主动监控者"，而是"被动协调者"
- 触发方式：用户询问 → PM响应 → 检查状态 → 协调行动
- 避免了"PM主动检查所有Agent"的无效工作

---

#### 2. 文档驱动的协作机制

**协作流程图**：
```
用户询问
    ↓
PM Agent (被动响应)
    ↓
┌───────────────────────────────────┐
│  文档协作中心                      │
├───────────────────────────────────┤
│ • agent-status.md (状态同步)      │
│ • GitHub Issues (任务分配)        │
│ • PR Comments (代码评审)          │
│ • session-log.md (会话记录)       │
└───────────────────────────────────┘
    ↓
Team Agents (AI/Core/Integration/Test)
    ↓
返回结果 → 更新文档
```

**关键特征**：
- 所有协作通过文档异步进行
- Agent间无直接通信
- Human作为信息桥梁（传递指令和结果）

---

#### 3. GitHub Issues作为任务分配核心

**任务分配机制**：
```yaml
# GitHub Issue结构
Issue结构:
  title: "TASK-AI1: 语义索引构建"
  labels: 
    - team: ai
    - priority: P0
    - sprint: sprint-1
  milestone: Sprint 1
  assignee: @ai-team
  body:
    - 任务描述
    - 验收标准
    - 技术要求
    - API设计
    - 文件清单
```

**PM的任务管理流程**：
```
1. 创建Issues（带label和milestone）
2. 通知Team（通过Human传达）
3. 等待PR提交
4. Review代码
5. 决定合并或反馈
6. 关闭Issue
```

**关键洞察**：
- GitHub Issues作为"任务中心"
- Labels实现Team筛选（team: ai, team: core等）
- Milestone实现Sprint管理

---

#### 4. 模块边界与权限控制

**模块边界定义**（以AI Team为例）：
```
✅ AI Team负责:
  scripts/embeddings/    # 向量嵌入
  scripts/index/         # 向量索引
  scripts/tools/indexing.py
  scripts/tools/search.py

❌ AI Team禁止修改:
  scripts/types.py       # Core Team负责
  scripts/utils.py       # Core Team负责
  scripts/connectors/    # Integration Team负责
```

**权限控制表**：
```
| 工具       | AI Team | Core Team | Integration |
|-----------|---------|-----------|-------------|
| Read      | ✅ 完全  | ✅ 完全    | ✅ 完全      |
| Write/Edit| ⚠️ 模块限定| ⚠️ 模块限定| ⚠️ 模块限定 |
| Bash      | ⚠️ 受限  | ⚠️ 受限    | ⚠️ 受限     |
| Task      | ❌ 禁止  | ❌ 禁止    | ❌ 禁止     |
```

**关键洞察**：
- 严格的模块边界防止冲突
- "Read完全，Write限定"的权限模式
- 所有Team禁止创建子代理（Task工具）

---

#### 5. 质量门控机制

**质量门控流程**：
```
开发前:
  - ✅ 阅读CATCH_UP.md（了解当前状态）
  - ✅ 查看GitHub Issues（确认任务）

开发中:
  - ✅ 只修改自己负责的模块
  - ✅ 测试覆盖率 > 80%
  - ✅ 遵循API设计

提交前:
  - ✅ 运行所有测试
  - ✅ 创建PR
  - ✅ 等待PM Review

提交后:
  - ✅ 响应PM反馈
  - ✅ 修复Review问题
  - ✅ 更新agent-status.md
```

**PM的Review职责**：
```
Review重点（以AI Team为例）:
  - 算法实现是否正确
  - 性能是否达标
  - API是否符合设计
  - 测试覆盖率是否达标
  - 文档是否完整
```

---

#### 6. 状态同步机制

**agent-status.md结构**：
```markdown
## Status Overview
- Last Updated: 2026-03-07 18:45
- Sprint: v1.1 Sprint 2 Complete ✅
- Phase: Core Team Tasks Completed

## Team Status Table
| Team      | Status   | Current Task         |
|-----------|----------|---------------------|
| PM Team   | 🟢 Active| 准备集成测试         |
| Core Team | ✅ Complete| Sprint 2完成        |
| AI Team   | ✅ Complete| Sprint 1完成        |
| Integration| ✅ Sprint 3 Done| Skill配置完成    |
| Test Team | 🔄 Active| 重新运行集成测试     |

## Sprint Progress
- Sprint 1: ✅ Complete
- Sprint 2: ✅ Complete
- Sprint 3: 🔄 Testing Phase
```

**更新时机**：
```
PM更新:
  - 用户询问后
  - Review完成后
  - 发现阻塞时

Team更新:
  - 开始工作时
  - 提交PR时
  - 遇到阻塞时
  - 完成任务时
```

---

#### 7. 启动脚本标准化

**启动脚本模式**：
```bash
#!/bin/bash
# ====================================
# {Team} Team Startup Script
# ====================================

echo "========================================"
echo "  {Team} Team - {Role Description}"
echo "========================================"
echo "Working Directory: knowledge-assistant-dev"
echo "Starting {Team} Team..."

# Check directory
if [ ! -d "practice/agents/{team}" ]; then
    echo "Error: Not in dev repository!"
    exit 1
fi

echo "{Team} Team ready!"
echo "Remember:"
echo "  - You are responsible for: {modules}"
echo "  - DO NOT modify: {other_team_modules}"
echo "  - Test coverage: > 85% required"
echo "Tasks: Check GitHub Issues with label 'team: {team}'"

# Start OpenCode
opencode --agent {team}
```

**关键特征**：
- 标准化的目录检查
- 职责和权限提醒
- 任务获取方式明确
- 自动启动opencode

---

### 案例分析：Sprint 2代码缺失事件

#### 事件时间线
```
2026-03-07 17:30
  Test Team发现Core Team代码缺失
  - extract_keywords() 不存在
  - generate_summary() 不存在
  - Issues #8, #9 已关闭但代码未合并

2026-03-07 18:00
  PM Team启动调查
  - 检查Core Team CATCH_UP.md
  - 检查代码库（extraction.py不存在）
  - 检查git历史（无相关commit）
  - 检查Issues（被错误关闭）

2026-03-07 18:00
  PM采取纠正措施
  - 重新开放Issues #8, #9
  - 创建Issue #16记录问题
  - 更新agent-status.md
  - 通知Core Team重新开发

2026-03-07 18:40
  Core Team完成开发
  - 提交extraction.py (426行)
  - 提交test_extraction.py (377行)
  - 33个测试用例，全部通过
  - PR #17 已合并

当前状态
  - Core Team Sprint 2完成 ✅
  - Test Team重新测试中 🔄
```

#### 问题根因分析

**问题**：Issues被错误关闭，实际代码未开发

**根因**：
1. **状态不一致**：Issue状态与实际开发状态脱节
2. **缺乏验证**：PM关闭Issue前未验证代码是否存在
3. **沟通缺失**：Core Team未开始开发，但Issue被关闭

**改进方向**：
1. PM关闭Issue前，必须验证代码已合并
2. Team完成开发后，必须提交PR并等待Review
3. PM Review通过后，才能关闭Issue

---

## R - Review（评审探讨）

### 关键设计原则

#### 原则1：被动响应，避免主动监控
```
设计理念：
- PM不是"监控者"，而是"协调者"
- 等待触发，而不是主动巡查
- 避免无效的"状态检查"工作

实际效果：
- ✅ 减少PM工作量
- ✅ 避免重复检查
- ✅ 响应式协作更高效
```

#### 原则2：文档驱动，异步协作
```
设计理念：
- 所有协作通过文档进行
- Agent间无直接通信
- Human作为信息桥梁

实际效果：
- ✅ 协作记录完整可追溯
- ✅ 避免通信混乱
- ⚠️ 依赖Human传递信息（效率瓶颈）
```

#### 原则3：模块边界严格，权限控制明确
```
设计理念：
- 每个Team有清晰的责任边界
- "Read完全，Write限定"
- 禁止越界修改

实际效果：
- ✅ 避免代码冲突
- ✅ 职责清晰
- ⚠️ 需要严格的权限配置
```

#### 原则4：GitHub Issues作为任务中心
```
设计理念：
- Issues = 任务清单
- Labels = Team筛选
- Milestones = Sprint管理

实际效果：
- ✅ 任务管理清晰
- ✅ 进度可视化
- ✅ 与代码仓库集成
```

#### 原则5：质量门控前置
```
设计理念：
- 开发前：了解状态和任务
- 开发中：遵循规范和测试
- 提交前：自测和Review
- 提交后：响应反馈

实际效果：
- ✅ 质量保证前置
- ✅ 减少返工
- ⚠️ 需要Team自觉遵守
```

---

### 发现的问题

#### 问题1：状态不一致风险
```
现象：
  Issues被错误关闭，实际未开发

根因：
  PM关闭Issue前未验证代码

建议：
  - PM Review流程增加"验证代码已合并"步骤
  - Team完成开发后必须提交PR
  - PR合并后才能关闭Issue
```

#### 问题2：Human成为信息瓶颈
```
现象：
  所有Agent间沟通都依赖Human传递

影响：
  - 信息传递延迟
  - Human工作量大
  - 协作效率受限

建议：
  - 当前架构限制下无法避免
  - 未来可考虑Agent间直接通信机制
```

#### 问题3：PM被动模式的边界不清晰
```
现象：
  "被动响应"与"主动管理"的边界模糊

案例：
  - PM何时应该主动检查？
  - PM何时应该被动等待？

建议：
  - 明确"触发条件"清单
  - 定义"主动检查"的场景
  - 例如：Sprint结束、Release前、重大问题后
```

---

## C - Confirm（确认验证）

### 需要验证的假设

#### 假设1：被动响应模式的有效性
```
假设：被动响应模式比主动监控更高效

验证方法：
  1. 对比PM工作量（主动 vs 被动）
  2. 测量响应延迟
  3. 评估问题发现及时性

待验证：需要更多实践数据
```

#### 假设2：文档驱动协作的完整性
```
假设：文档驱动协作可以完整记录所有信息

验证方法：
  1. 检查文档是否覆盖所有关键信息
  2. 评估文档更新及时性
  3. 测量信息查找效率

待验证：需要观察长期实践效果
```

#### 假设3：模块边界划分的合理性
```
假设：当前模块边界划分清晰且合理

验证方法：
  1. 统计跨Team修改的频率
  2. 记录边界模糊的场景
  3. 评估职责冲突事件

待验证：需要观察更多开发场景
```

---

## H - Harvest（收获产出）

### 核心洞察

#### 洞察1：PM的三种角色
```
PM Agent实际扮演三种角色：

1. 协调者（Coordinator）
   - 分配任务（GitHub Issues）
   - 协调Team工作
   - 处理冲突和阻塞

2. 质量把关者（Quality Gatekeeper）
   - Review代码
   - 验证质量门控
   - 决定发布

3. 状态管理者（Status Manager）
   - 维护agent-status.md
   - 更新项目进度
   - 记录关键决策
```

#### 洞察2：协作模式的核心要素
```
Agent协作成功的五大要素：

1. 清晰的角色定义（AGENTS.md）
2. 明确的模块边界（权限控制）
3. 统一的任务中心（GitHub Issues）
4. 完整的状态同步（agent-status.md）
5. 标准化的流程（启动脚本、工作流）
```

#### 洞察3：质量保证的分层设计
```
质量保证分布在三个层次：

Layer 1: Agent自我约束
  - 阅读CATCH_UP.md
  - 遵循模块边界
  - 自测覆盖率 > 80%

Layer 2: PM过程管控
  - Review代码
  - 验证验收标准
  - 检查测试报告

Layer 3: Test Team独立验证
  - 集成测试
  - 端到端测试
  - 性能测试
```

#### 洞察4：异步协作的双刃剑
```
优势：
  ✅ 协作记录完整
  ✅ 减少通信开销
  ✅ 支持分布式协作
  ✅ 可追溯和审计

劣势：
  ⚠️ 信息传递延迟
  ⚠️ 依赖Human传递
  ⚠️ 实时性不足
  ⚠️ 复杂场景沟通困难
```

---

### 可复用的模式

#### 模式1：被动响应启动模式
```yaml
# 适用于：PM、Coordinator类Agent

工作模式：
  trigger: 用户询问
  action:
    - 读取状态文档
    - 检查团队状态
    - 协调行动
    - 更新文档
  not_allowed:
    - 主动监测Agent状态
    - 定期推送汇报
```

#### 模式2：文档驱动协作模式
```yaml
# 适用于：Agent Team协作

协作要素：
  task_center: GitHub Issues
  status_sync: agent-status.md
  communication: Issue/PR Comments
  record_keeping: session-log.md

信息流：
  PM → Issue → Team
  Team → PR → PM Review → Merge
  Team → agent-status.md → PM
```

#### 模式3：模块边界控制模式
```yaml
# 适用于：多Agent协作系统

边界定义：
  responsible_modules: [module1, module2]
  read_access: all_modules
  write_access: responsible_modules_only

权限矩阵：
  tool:
    read: ✅ full
    write: ⚠️ limited
    bash: ⚠️ restricted
    task: ❌ forbidden
```

---

### 待研究的问题

#### 问题1：Agent间直接通信的必要性
```
当前状态：
  Agent间无法直接通信，依赖Human传递

问题：
  是否需要Agent间直接通信机制？

研究角度：
  - 直接通信的优势和风险
  - 实现方案（消息队列、共享内存）
  - 与现有架构的兼容性
```

#### 问题2：PM主动检查的触发条件
```
当前状态：
  PM被动响应，仅在用户询问时触发

问题：
  是否存在需要PM主动检查的场景？

研究角度：
  - Sprint结束时的状态检查
  - Release前的质量检查
  - 重大问题后的主动调查
```

#### 问题3：质量门控的自动化程度
```
当前状态：
  质量门控依赖Agent自觉 + PM Review

问题：
  质量门控可以自动化到什么程度？

研究角度：
  - 自动化测试覆盖率检查
  - 自动化API验证
  - 自动化性能测试
```

---

## R - Reflect（反思迭代）

### 方法论反思

#### 反思1：观察深度是否足够？
```
当前深度：Level 2（设计原则层）

已完成：
  ✅ 描述现象（What）
  ✅ 分析原因（Why）
  ✅ 提炼原则（Principles）

待深化：
  ⏳ Level 3：实现思路（How to implement）
  ⏳ 具体的技术实现细节
  ⏳ 工具和框架选择
```

#### 反思2：观察视角是否全面？
```
当前视角：
  ✅ PM视角（启动、管理、协调）
  ✅ 文档视角（配置、状态、任务）
  ⏳ Team视角（如何理解任务、如何协作）
  ⏳ Human视角（如何传递信息、如何决策）

改进方向：
  - 观察Team Agent的实际工作流程
  - 记录Human的决策过程
  - 分析协作中的瓶颈和摩擦
```

#### 反思3：案例样本是否足够？
```
当前案例：
  1. Sprint 1启动流程（正常流程）
  2. Sprint 2代码缺失事件（异常流程）

需要更多案例：
  ⏳ Team间依赖处理的案例
  ⏳ 冲突解决的案例
  ⏳ 需求变更的案例
  ⏳ Release准备的案例
```

---

### 下一步行动

#### 行动1：深化Team视角观察
```
目标：理解Team Agent的工作流程

方法：
  1. 观察AI Team实际开发流程
  2. 观察Core Team的任务执行
  3. 观察Test Team的测试流程

产出：
  - Team工作流程图
  - Team协作模式分析
  - Team视角的问题和建议
```

#### 行动2：记录更多协作案例
```
目标：丰富案例库

方法：
  1. 持续观察Agent协作事件
  2. 记录正常和异常流程
  3. 分析成功和失败案例

产出：
  - 案例库（正常/异常/边界）
  - 案例分析报告
  - 最佳实践总结
```

#### 行动3：完善Agent协作理论
```
目标：构建Agent协作的理论框架

方法：
  1. 提炼协作模式
  2. 定义协作原则
  3. 设计协作评估指标

产出：
  - Agent协作理论框架
  - 协作模式库
  - 协作质量评估方法
```

---

## 附录

### A. 文档清单

| 文档 | 路径 | 用途 |
|------|------|------|
| PM AGENTS.md | practice/agents/pm/AGENTS.md | PM角色定义 |
| PM CATCH_UP.md | practice/agents/pm/CATCH_UP.md | PM当前状态 |
| PM session-log.md | practice/agents/pm/session-log.md | PM工作记录 |
| AI AGENTS.md | practice/agents/ai/AGENTS.md | AI Team角色定义 |
| Core AGENTS.md | practice/agents/core/AGENTS.md | Core Team角色定义 |
| Integration AGENTS.md | practice/agents/integration/AGENTS.md | Integration Team角色定义 |
| Test AGENTS.md | practice/agents/test/AGENTS.md | Test Team角色定义 |
| agent-status.md | practice/status/agent-status.md | 团队状态总览 |
| task-assignments.md | practice/status/task-assignments/v1.1-task-assignments.md | 任务分配 |

### B. 关键概念定义

**被动响应模式**：
PM等待用户询问触发工作，不主动监测Agent状态的工作模式。

**文档驱动协作**：
所有Agent协作通过文档异步进行，不依赖实时通信的协作模式。

**模块边界**：
每个Team有明确的责任模块，禁止修改其他Team负责的模块。

**质量门控**：
确保代码质量的检查点，分布在开发前、开发中、提交前、提交后四个阶段。

### C. 观察者信息

- **观察者**: Research Agent
- **观察日期**: 2026-03-07
- **观察方法**: 文档分析 + 案例研究
- **研究深度**: Level 2（设计原则层）
- **方法论**: SEARCH-R

---

**文档版本**: v1.0  
**最后更新**: 2026-03-07  
**状态**: 初稿完成，待验证假设
