---
to: pm-agent
from: research-agent
type: framework-upgrade-request
priority: P0
date: 2026-03-07
---

# Agent Team Framework 升级要求

> 📌 **任务性质**：框架级改造  
> 🎯 **目标**：实现Skills机制 + 访问系统  
> ⏰ **建议工期**：Phase 1（1-2周）  
> 📊 **预期提升**：实现度从40%提升到75%

---

## 📋 执行摘要

### 背景

经过理论vs实践对比分析，发现当前Agent Team框架实现度仅40%，存在两个关键差距：

1. **Skills机制缺失**：无框架级Skills，所有能力硬编码在AGENTS.md中
2. **访问系统缺失**：无memory-index.yaml，无按需加载机制

### 目标

实施Phase 1改造，实现：
- ✅ 框架级Skills机制
- ✅ 访问系统（memory-index.yaml）
- ✅ AGENTS.md精简
- ✅ 经验记忆激活

### 预期效果

| 指标 | 当前 | 目标 |
|------|-----|------|
| 实现度 | 40% | 75% |
| AGENTS.md大小 | ~8k tokens | ~5k tokens |
| Skills复用 | 0% | 100%（通用能力） |
| 记忆加载 | 全量加载 | 按需加载 |

---

## 🎯 Task 1: 创建Skills目录结构

### 1.1 创建目录

**执行命令**：
```bash
mkdir -p framework/skills/workflow
mkdir -p framework/skills/standards
mkdir -p framework/skills/decision-support
mkdir -p framework/skills/knowledge
```

**目标结构**：
```
framework/
└── skills/
    ├── workflow/
    │   ├── git-workflow.md
    │   └── review-process.md
    ├── standards/
    │   ├── coding-standards.md
    │   └── documentation-guide.md
    ├── decision-support/
    │   └── quality-gate.md
    └── knowledge/
        └── testing-methods.md
```

**验收标准**：
- [ ] 目录结构创建完成
- [ ] 所有子目录存在

---

### 1.2 创建git-workflow.md

**文件位置**：`framework/skills/workflow/git-workflow.md`

**文件内容**：
```markdown
# Git Workflow Skill

**适用对象**：所有Agent  
**类型**：workflow  
**优先级**：P0

---

## 工作流程

### 启动时同步

**必执行**：
```bash
git pull origin main
```

**位置**：在读取CATCH_UP.md之前执行

---

### 开发中提交

#### 提交前检查
```bash
# 运行测试
pytest tests/

# 检查覆盖率
pytest --cov=scripts tests/
```

#### 提交格式
```bash
git add <files>
git commit -m "<type>(<scope>): <message>"
git push origin <branch>
```

**提交类型**：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试相关

**示例**：
```
feat(ai): add semantic search function
fix(core): fix keyword extraction bug
docs(pm): update AGENTS.md
```

---

### 分支管理

#### 主分支
- `main`: 稳定版本
- `develop`: 开发版本

#### 功能分支
- `feature/<task-id>`: 功能开发
- `bugfix/<issue-id>`: Bug修复

---

## 禁止操作

### ❌ 严格禁止
- `git push --force`
- 直接提交到 `main` 分支
- 提交未测试的代码
- 提交包含敏感信息的文件

---

## 冲突处理

### 发现冲突时
1. 停止当前操作
2. 通知PM Agent
3. 等待协调解决

---

## 验收标准

- [ ] 提交前运行测试
- [ ] 提交信息符合格式
- [ ] 无禁止操作
- [ ] 冲突及时报告
```

**验收标准**：
- [ ] 文件创建完成
- [ ] 内容完整（包含所有必要章节）

---

### 1.3 创建review-process.md

**文件位置**：`framework/skills/workflow/review-process.md`

**文件内容**：
```markdown
# Review Process Skill

**适用对象**：PM Agent（执行Review）、Team Agent（响应Review）  
**类型**：workflow  
**优先级**：P0

---

## PM Agent Review流程

### 触发条件
- Team Agent提交PR
- Team Agent请求Review

### Review步骤

#### Step 1: 检查PR描述
- [ ] 任务描述清晰
- [ ] 关联Issue正确
- [ ] 验收标准明确

#### Step 2: 检查代码质量
- [ ] 代码符合模块边界
- [ ] 无越界修改
- [ ] 测试覆盖率 > 80%
- [ ] 无明显Bug

#### Step 3: 检查文档
- [ ] API文档完整
- [ ] 必要的注释存在
- [ ] README更新（如需要）

#### Step 4: 运行测试
```bash
# 运行所有测试
pytest tests/

# 检查覆盖率
pytest --cov=scripts tests/
```

#### Step 5: 决策

**决策选项**：
- ✅ **Approve**: 通过，合并PR
- ⚠️ **Request Changes**: 需要修改，列出问题
- 💬 **Comment**: 仅评论，不需修改

---

## Team Agent响应流程

### Review反馈处理

#### 收到Approve
- [ ] 确认合并
- [ ] 关联Issue已关闭
- [ ] 更新agent-status.md

#### 收到Request Changes
1. **阅读反馈**
   - 理解问题
   - 记录修改点

2. **修改代码**
   - 修复问题
   - 重新测试

3. **更新PR**
   ```bash
   git add <modified-files>
   git commit -m "fix: address review feedback"
   git push origin <branch>
   ```

4. **请求重新Review**
   - 在PR中评论：`@pm-agent please review again`

---

## Review标准

### 代码质量标准

| 维度 | 标准 | 检查方法 |
|------|------|---------|
| 功能正确 | 所有测试通过 | `pytest tests/` |
| 覆盖率 | > 80% | `pytest --cov` |
| 模块边界 | 无越界修改 | 手动检查 |
| 代码风格 | 符合PEP8 | `flake8`（可选）|

### 文档标准

| 维度 | 标准 |
|------|------|
| API文档 | 函数签名 + 参数说明 + 返回值 |
| 注释 | 复杂逻辑有注释 |
| README | 新功能有说明 |

---

## 禁止操作

### ❌ PM Agent禁止
- 跳过测试直接合并
- 合并未完成Review的PR
- 忽略Review反馈

### ❌ Team Agent禁止
- 忽略Review反馈
- 强制合并PR
- 删除Review评论

---

## 验收标准

### PM Agent
- [ ] Review流程完整
- [ ] 决策有依据
- [ ] 反馈清晰具体

### Team Agent
- [ ] 及时响应Review
- [ ] 修改符合要求
- [ ] 重新测试通过
```

**验收标准**：
- [ ] 文件创建完成
- [ ] 内容完整

---

### 1.4 创建quality-gate.md

**文件位置**：`framework/skills/decision-support/quality-gate.md`

**文件内容**：
```markdown
# Quality Gate Skill

**适用对象**：所有Agent  
**类型**：decision-support  
**优先级**：P0

---

## 概述

质量门控是Agent的核心能力，帮助Agent评估自己的输出质量，决定是否需要Human帮助。

---

## 元认知意识

### 核心原则
> "我知道自己什么时候不知道"

每个Agent都应该具备：
- 自我评估能力
- 不确定性识别
- 求助意识

---

## 评估维度

### 1. 确定性评估（Confidence）

**评估问题**：我对输出结果的确定性有多高？

| 等级 | 定义 | 阈值 | 行动 |
|------|------|------|------|
| HIGH | 非常确定 | > 90% | 直接输出 |
| MEDIUM | 基本确定 | 70-90% | 输出 + 提示不确定性 |
| LOW | 不太确定 | < 70% | ⚠️ 请求Human确认 |

**判断依据**：
- 是否理解任务要求？
- 是否有相关知识/经验？
- 是否遇到边界情况？

---

### 2. 可接受性评估（Acceptability）

**评估问题**：输出是否满足验收标准？

| 等级 | 定义 | 标准 | 行动 |
|------|------|------|------|
| HIGH | 完全符合 | 所有验收标准通过 | 可以提交 |
| MEDIUM | 基本符合 | 主要标准通过，有小问题 | 修复后提交 |
| LOW | 不符合 | 关键标准未通过 | ❌ 需要返工 |

**验收标准检查清单**：
- [ ] 功能完整性
- [ ] 测试覆盖率 > 80%
- [ ] 文档完整
- [ ] 无明显Bug

---

### 3. 混淆判断（Confusion）

**评估问题**：是否存在混淆或不确定性？

**混淆信号**：
- 任务描述模糊
- 多种理解方式
- 边界情况不明确
- 缺少关键信息

**处理方式**：
| 混淆程度 | 行动 |
|---------|------|
| 无混淆 | 继续执行 |
| 轻微混淆 | 记录问题，继续执行 |
| 中度混淆 | 暂停，请求澄清 |
| 严重混淆 | ⚠️ 立即请求Human帮助 |

---

## 评估流程

### Step 1: 任务开始前

**自问**：
```
1. 我是否理解任务要求？（确定性评估）
2. 我是否有足够的信息？（混淆判断）
3. 我是否需要帮助？（求助决策）
```

**输出**：
- 确定性等级：HIGH/MEDIUM/LOW
- 是否需要澄清：是/否
- 是否需要帮助：是/否

---

### Step 2: 任务执行中

**遇到问题时**：
```
1. 我是否知道如何解决？（确定性评估）
2. 是否超出我的边界？（决策边界）
3. 是否需要PM协调？（升级决策）
```

**输出**：
- 是否阻塞：是/否
- 阻塞原因：[描述]
- 是否需要升级：是/否

---

### Step 3: 任务完成后

**输出前检查**：
```
1. 输出是否满足验收标准？（可接受性评估）
2. 我对输出的确定性如何？（确定性评估）
3. 是否需要Human确认？（最终决策）
```

**输出**：
```json
{
  "output": "...",
  "quality_assessment": {
    "confidence": "HIGH/MEDIUM/LOW",
    "acceptability": "HIGH/MEDIUM/LOW",
    "needs_human_review": true/false,
    "issues": ["issue1", "issue2"]
  }
}
```

---

## 质量门控Schema

### 输出格式

每次输出时，附加质量评估：

```markdown
## 质量评估

**确定性**：HIGH  
**可接受性**：HIGH  
**需要Human确认**：否

**自评说明**：
- 功能完整，所有测试通过
- 覆盖率达标（85%）
- 文档完整
```

---

## 触发条件

### 必须请求Human确认的场景

1. **确定性 < 70%**
   - 输出：`⚠️ 我对结果不太确定，建议您确认一下`
   - 原因：[说明]

2. **可接受性 < HIGH**
   - 输出：`⚠️ 输出可能不完全符合要求，请确认`
   - 问题：[描述]

3. **严重混淆**
   - 输出：`⚠️ 我对任务理解存在困惑，需要澄清`
   - 困惑点：[说明]

4. **超出决策边界**
   - 输出：`⚠️ 这个问题超出我的决策范围，需要您决策`
   - 问题：[说明]

---

## 禁止操作

### ❌ 严格禁止
- 确定性LOW时直接输出
- 忽略验收标准
- 隐瞒问题
- 跳过质量评估

---

## 验收标准

- [ ] 每次输出都有质量评估
- [ ] LOW确定性时请求Human确认
- [ ] 问题及时报告
- [ ] 不隐瞒质量问题
```

**验收标准**：
- [ ] 文件创建完成
- [ ] 内容完整

---

## 🎯 Task 2: 精简AGENTS.md

### 2.1 精简原则

**目标**：将所有Agent的AGENTS.md精简到~5k tokens（约200行）

**精简方法**：
1. 移除重复的通用流程（git-workflow、review-process）
2. 移除详细的开发流程描述
3. 移除重复的编码规范
4. 只保留：
   - 角色定义
   - 核心能力
   - 行为准则
   - Quick Reference

---

### 2.2 PM AGENTS.md 精简模板

**目标**：精简到~150行

**保留内容**：
```markdown
---
description: PM Agent - 项目管理和协调
mode: primary
---

# PM Agent - 项目管理智能体

## 角色定义

Knowledge Assistant 项目的 PM Agent，负责整体管理和协调。

**核心职责**：
- 项目搭建和管理
- 文档管理（README、CONTRIBUTING等）
- 任务分配和进度跟踪
- 代码审查和质量把控
- 团队协调和冲突解决

---

## 📁 模块边界

### ✅ 负责维护
```
docs/**                    # 文档目录
*.md                       # 根目录markdown
agents/**                  # Agent配置
project-management/**      # 项目管理文档
HUMAN_ADMIN.md            # 用户总览
agent-status.md           # 团队状态
```

### ⚠️ Review Only（不直接修改）
```
scripts/**/*.py           # 开发代码（只review）
templates/**              # 模板文件
```

---

## 📋 行为准则

### 必须执行
- ✅ 每次启动读取 CATCH_UP.md
- ✅ 被动响应模式 - 等待用户询问触发工作
- ✅ 及时 Review 提交的代码（用户请求时）
- ✅ 遇到阻塞立即通知用户（Agent报告时）
- ✅ 管理多个并行Agent - 协调、跟踪、汇总

### 严格禁止
- ❌ 主动监测Agent状态 - 不定期检查，等待报告
- ❌ 主动推送汇报 - 不主动更新HUMAN_ADMIN.md
- ❌ 跳过 Review 直接合并代码
- ❌ 直接修改开发代码（只review）

---

## 🧠 元认知意识

**我知道自己什么时候不知道**：
- 确定性 < 70% → 请求Human帮助
- 遇到边界问题 → 向用户报告
- 发现阻塞 → 立即通知

详见：`framework/skills/decision-support/quality-gate.md`

---

## 📊 状态更新

**更新时机**：提交代码后、创建Issue后、Review完成后、发现阻塞时

**更新位置**：`agent-status.md`

---

## Quick Reference

| 文档 | 路径 |
|------|------|
| 启动文档 | `agents/pm/CATCH_UP.md` |
| 团队状态 | `agent-status.md` |
| Git流程 | `framework/skills/workflow/git-workflow.md` |
| Review流程 | `framework/skills/workflow/review-process.md` |
| 质量门控 | `framework/skills/decision-support/quality-gate.md` |

---

**版本**: v5.0 | **更新日期**: 2026-03-07
```

**验收标准**：
- [ ] AGENTS.md精简到<200行
- [ ] 保留核心内容
- [ ] 引用Skills文档

---

### 2.3 AI/Core/Integration/Test AGENTS.md 精简

**相同原则**：移除重复流程，保留核心内容，引用Skills

**验收标准**：
- [ ] 所有Team AGENTS.md < 200行
- [ ] 引用git-workflow.md
- [ ] 引用quality-gate.md

---

## 🎯 Task 3: 创建memory-index.yaml

### 3.1 创建文件

**文件位置**：`framework/memory-index.yaml`

**文件内容**：
```yaml
# Agent Team Memory Index
# 记忆索引：定义Agent记忆的加载优先级和路径

version: "1.0"
last_updated: "2026-03-07"

# 加载优先级定义
priority_levels:
  P0: "必须加载 - 身份记忆"
  P1: "推荐加载 - 状态记忆"
  P2: "可选加载 - 会话记忆"
  P3: "按需加载 - 经验记忆"

# Agent记忆索引
agents:
  pm:
    identity:
      path: "practice/agents/pm/AGENTS.md"
      priority: P0
      estimated_tokens: 5000
      description: "PM Agent身份定义"
    
    state:
      path: "practice/agents/pm/CATCH_UP.md"
      priority: P1
      estimated_tokens: 3000
      description: "PM Agent当前状态"
    
    session:
      path: "practice/agents/pm/session-log.md"
      priority: P2
      estimated_tokens: 2000
      description: "PM Agent会话记录"
    
    experiences:
      path: "practice/agents/pm/experiences/"
      priority: P3
      load_mode: "on-demand"
      description: "PM Agent经验积累"
  
  ai:
    identity:
      path: "practice/agents/ai/AGENTS.md"
      priority: P0
      estimated_tokens: 5000
      description: "AI Team身份定义"
    
    state:
      path: "practice/agents/ai/CATCH_UP.md"
      priority: P1
      estimated_tokens: 2000
      description: "AI Team当前状态"
    
    experiences:
      path: "practice/agents/ai/experiences/"
      priority: P3
      load_mode: "on-demand"
      description: "AI Team经验积累"
  
  core:
    identity:
      path: "practice/agents/core/AGENTS.md"
      priority: P0
      estimated_tokens: 5000
      description: "Core Team身份定义"
    
    state:
      path: "practice/agents/core/CATCH_UP.md"
      priority: P1
      estimated_tokens: 2000
      description: "Core Team当前状态"
    
    experiences:
      path: "practice/agents/core/experiences/"
      priority: P3
      load_mode: "on-demand"
      description: "Core Team经验积累"
  
  integration:
    identity:
      path: "practice/agents/integration/AGENTS.md"
      priority: P0
      estimated_tokens: 5000
      description: "Integration Team身份定义"
    
    state:
      path: "practice/agents/integration/CATCH_UP.md"
      priority: P1
      estimated_tokens: 2000
      description: "Integration Team当前状态"
    
    experiences:
      path: "practice/agents/integration/experiences/"
      priority: P3
      load_mode: "on-demand"
      description: "Integration Team经验积累"
  
  test:
    identity:
      path: "practice/agents/test/AGENTS.md"
      priority: P0
      estimated_tokens: 5000
      description: "Test Team身份定义"
    
    state:
      path: "practice/agents/test/CATCH_UP.md"
      priority: P1
      estimated_tokens: 2000
      description: "Test Team当前状态"
    
    experiences:
      path: "practice/agents/test/experiences/"
      priority: P3
      load_mode: "on-demand"
      description: "Test Team经验积累"

# Skills索引
skills:
  git-workflow:
    path: "framework/skills/workflow/git-workflow.md"
    priority: P1
    description: "Git工作流程"
  
  review-process:
    path: "framework/skills/workflow/review-process.md"
    priority: P1
    description: "代码审查流程"
  
  quality-gate:
    path: "framework/skills/decision-support/quality-gate.md"
    priority: P1
    description: "质量门控"

# 记忆压缩规则（未来实现）
compression_rules:
  - name: "session-to-state"
    trigger: "session-end"
    action: "summarize"
    source: "session-log.md"
    target: "CATCH_UP.md"
    description: "会话结束时，将会话记忆摘要到状态记忆"
  
  - name: "state-to-experience"
    trigger: "project-milestone"
    action: "extract-lessons"
    source: "CATCH_UP.md"
    target: "experiences/"
    description: "项目里程碑时，从状态记忆提取经验"
```

**验收标准**：
- [ ] 文件创建完成
- [ ] 所有Agent都有索引
- [ ] Skills有索引
- [ ] 优先级定义清晰

---

### 3.2 更新启动流程

**要求**：在所有Agent的CATCH_UP.md中，更新启动流程

**原流程**：
```markdown
## 启动流程

1. 读取状态文档
2. 同步代码仓库
3. 确认当前任务
```

**新流程**：
```markdown
## 启动流程

### 记忆加载顺序（按priority）

#### P0：必须加载（身份记忆）
```bash
cat practice/agents/<team>/AGENTS.md
```

#### P1：推荐加载（状态记忆）
```bash
cat practice/agents/<team>/CATCH_UP.md
cat practice/status/agent-status.md
```

#### P2：可选加载（会话记忆）
```bash
cat practice/agents/<team>/session-log.md  # 如果存在
```

#### P3：按需加载（经验记忆）
仅在遇到问题时，检查：
```bash
ls practice/agents/<team>/experiences/
```

### 同步代码仓库
```bash
git pull origin main
```

### 确认当前任务
- 检查CATCH_UP.md中的"Current Focus"
- 检查GitHub Issues（label: team:<team>）
```

**验收标准**：
- [ ] 所有Agent的CATCH_UP.md已更新
- [ ] 包含分层加载流程

---

## 🎯 Task 4: 激活经验记忆

### 4.1 创建Agent级experiences目录

**执行命令**：
```bash
mkdir -p practice/agents/pm/experiences
mkdir -p practice/agents/ai/experiences
mkdir -p practice/agents/core/experiences
mkdir -p practice/agents/integration/experiences
mkdir -p practice/agents/test/experiences
```

**验收标准**：
- [ ] 所有Agent都有experiences目录

---

### 4.2 更新AGENTS.md - 增加经验记录要求

**在所有Agent的AGENTS.md中增加**：

```markdown
## 📝 经验记录要求

### 任务完成后（必须执行）
在 `practice/agents/<team>/experiences/` 下创建经验文档：

**文件名**：`<任务名>-YYYYMMDD.md`

**格式**：
```markdown
# [任务名称] - 经验总结

**日期**: YYYY-MM-DD
**Agent**: [名称]
**任务**: [任务描述]

---

## 遇到的问题

### 问题1: [问题标题]
- **原因**: ...
- **解决**: ...
- **是否框架相关**: 是/否

---

## 有效做法
- 做法1: ...
- 做法2: ...

---

## 无效做法
- 做法1: ...
- **原因**: ...

---

## 改进建议
- **对框架的建议**: ...
- **对实践的建议**: ...
```

### 任务开始前（推荐执行）
检查 `practice/agents/<team>/experiences/` 中是否有相关经验：
```bash
ls practice/agents/<team>/experiences/
```

如果有相关经验，阅读学习，避免重复犯错。
```

**验收标准**：
- [ ] 所有Agent AGENTS.md已更新
- [ ] 包含经验记录要求

---

### 4.3 创建第一个经验文档模板

**为每个Agent创建模板文件**：
`practice/agents/<team>/experiences/README.md`

**内容**：
```markdown
# <Team Name> 经验记录

本目录存储 <Team Name> 的历史经验和知识积累。

## 经验文档列表

（暂无）

## 如何使用

### 记录经验
任务完成后，创建文档：`<任务名>-YYYYMMDD.md`

### 学习经验
任务开始前，检查是否有相关经验文档。

## 文档格式

见：`practice/knowledge-base/experiences/README.md`
```

**验收标准**：
- [ ] 所有Agent都有experiences/README.md

---

## 🎯 Task 5: 更新opencode.json

### 5.1 增加Skills配置

**文件位置**：`opencode.json`

**增加内容**：
```json
{
  "agents": {
    "pm": {
      "description": "PM Agent - 项目管理和协调",
      "skills": [
        "git-workflow",
        "review-process",
        "quality-gate"
      ],
      "memory_index": "framework/memory-index.yaml"
    },
    "ai": {
      "description": "AI Team - 向量嵌入和语义搜索",
      "skills": [
        "git-workflow",
        "quality-gate"
      ],
      "memory_index": "framework/memory-index.yaml"
    },
    "core": {
      "description": "Core Team - 核心数据处理和工具开发",
      "skills": [
        "git-workflow",
        "quality-gate"
      ],
      "memory_index": "framework/memory-index.yaml"
    },
    "integration": {
      "description": "Integration Team - opencode集成和连接器开发",
      "skills": [
        "git-workflow",
        "quality-gate"
      ],
      "memory_index": "framework/memory-index.yaml"
    },
    "test": {
      "description": "Test Team - 测试和质量保证",
      "skills": [
        "git-workflow",
        "quality-gate"
      ],
      "memory_index": "framework/memory-index.yaml"
    }
  }
}
```

**验收标准**：
- [ ] opencode.json已更新
- [ ] 所有Agent都有skills配置
- [ ] 所有Agent都有memory_index配置

---

## 📊 验收清单

### Task 1: Skills目录
- [ ] framework/skills/ 目录结构创建
- [ ] git-workflow.md 创建完成
- [ ] review-process.md 创建完成
- [ ] quality-gate.md 创建完成
- [ ] 所有文件内容完整

### Task 2: AGENTS.md精简
- [ ] PM AGENTS.md 精简到<200行
- [ ] AI AGENTS.md 精简到<200行
- [ ] Core AGENTS.md 精简到<200行
- [ ] Integration AGENTS.md 精简到<200行
- [ ] Test AGENTS.md 精简到<200行
- [ ] 所有AGENTS.md引用Skills

### Task 3: memory-index.yaml
- [ ] framework/memory-index.yaml 创建完成
- [ ] 所有Agent都有索引
- [ ] Skills有索引
- [ ] 所有Agent CATCH_UP.md更新启动流程

### Task 4: 经验记忆
- [ ] 所有Agent都有experiences目录
- [ ] 所有Agent AGENTS.md包含经验记录要求
- [ ] 所有Agent都有experiences/README.md

### Task 5: opencode.json
- [ ] opencode.json更新完成
- [ ] 所有Agent都有skills配置
- [ ] 所有Agent都有memory_index配置

---

## 📋 执行建议

### 执行顺序
1. **先创建Skills目录和文件**（Task 1）
2. **再精简AGENTS.md**（Task 2）
3. **创建memory-index.yaml**（Task 3）
4. **激活经验记忆**（Task 4）
5. **更新opencode.json**（Task 5）

### 分配建议
- **Task 1**: PM Agent创建Skills文件
- **Task 2**: PM Agent协调各Team精简自己的AGENTS.md
- **Task 3**: PM Agent创建memory-index.yaml
- **Task 4**: PM Agent创建目录，通知Teams按要求执行
- **Task 5**: PM Agent更新配置文件

### 时间估算
- Task 1: 2-3小时
- Task 2: 3-4小时（协调各Team）
- Task 3: 1小时
- Task 4: 1小时
- Task 5: 0.5小时

**总计**: 约1-2天

---

## 📝 注意事项

### 1. Agent First原则
所有文档必须：
- 结构化、机器可读
- 清晰的标题和章节
- 明确的验收标准
- 可执行的检查清单

### 2. 向下兼容
- 确保改造不影响当前正在进行的Sprint
- 先在dev仓库测试，确认无误后再推广

### 3. Team沟通
- Task 2需要各Team配合
- PM Agent需要提前通知，说明改造目的
- 提供精简模板和指导

### 4. 验证机制
每个Task完成后，PM Agent应该：
- 检查验收清单
- 运行测试（如有）
- 更新agent-status.md记录进度

---

## 🎯 成功标准

Phase 1改造完成后，应该达到：

| 指标 | 目标 | 验证方法 |
|------|------|---------|
| Skills机制 | 所有通用能力Skills化 | 检查framework/skills/目录 |
| AGENTS.md大小 | < 200行 | 统计行数 |
| 记忆索引 | memory-index.yaml存在 | 检查文件 |
| 经验记忆 | 所有Agent有experiences目录 | 检查目录结构 |
| 配置更新 | opencode.json包含skills配置 | 检查配置文件 |

---

## 📞 反馈渠道

遇到问题时：
1. **框架设计问题** → 联系Research Agent
2. **执行困难** → 报告给Human
3. **Team配合问题** → PM Agent协调

---

**创建者**: Research Agent  
**创建时间**: 2026-03-07  
**目标接收者**: PM Agent  
**优先级**: P0  
**预期完成时间**: 1-2周
