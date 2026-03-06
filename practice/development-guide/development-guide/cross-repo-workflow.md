# 跨仓库工作流

## 概述

Knowledge Assistant 项目采用双仓库策略：
- **开发仓库（knowledge-assistant-dev）**：开发过程管理（Private）
- **主仓库（knowledge-assistant）**：输出交付品（Public）

本文档定义了两个仓库之间的协作规则和工作流程。

---

## 仓库关系

```
┌──────────────────────────────┐
│  knowledge-assistant-dev     │
│  (Private - 开发过程管理)     │
│                               │
│  - Agent 配置                 │
│  - 项目管理文档               │
│  - 开发指南                   │
│  - 工作记录                   │
└──────────────────────────────┘
            │
            │ 参考、指导
            ↓
┌──────────────────────────────┐
│  knowledge-assistant         │
│  (Public - 输出交付品)        │
│                               │
│  - 项目代码                   │
│  - 用户文档                   │
│  - 测试代码                   │
│  - 示例数据                   │
└──────────────────────────────┘
            │
            │ 发布
            ↓
        社区用户
```

---

## 工作流程

### 1. 任务分配阶段

```
PM（在开发仓库）
    ↓ 阅读 Agent 配置
    ↓ 参考项目管理文档
    ↓
PM（在主仓库）
    ↓ 创建 Issue
    ↓ 分配给对应 Agent
    ↓
Agent（读取开发仓库的配置）
    ↓ 理解职责和规范
    ↓ 认领 Issue
```

### 2. 开发阶段

```
Agent（在主仓库工作）
    ↓ 创建功能分支
    ↓ 编写代码
    ↓ 编写测试
    ↓ 本地验证
    ↓
Agent（准备提交）
    ↓ 检查开发仓库的规范
    ├─ development-guide/coding-standards.md
    ├─ development-guide/testing-standards.md
    └─ development-guide/commit-standards.md
    ↓
Agent（提交代码到主仓库）
```

### 3. Review 阶段

```
Agent 提交 PR（在主仓库）
    ↓
PM（读取开发仓库的规则）
    ├─ development-guide/review-process.md
    └─ development-guide/review-checklist.md
    ↓
PM Review 代码
    ├─ 代码质量
    ├─ 功能正确性
    ├─ 测试覆盖率
    └─ 文档完整性
    ↓
Review 结果
    ├─ Approve → 合并
    └─ Request Changes → 返回修改
```

### 4. 发布阶段

```
PM（在主仓库）
    ↓ 准备发布
    ↓
PM（参考开发仓库）
    └─ development-guide/release-process.md
    ↓
PM（在主仓库）
    ↓ 创建 Release
    ↓ 发布到社区
    ↓
PM（在开发仓库）
    ↓ 更新项目状态
    ↓ 记录发布信息
```

---

## 权限和责任

### PM Agent

**开发仓库**：
- ✅ 创建和修改 Agent 配置
- ✅ 创建和修改开发指南
- ✅ 更新项目管理文档
- ✅ 记录工作日志和报告

**主仓库**：
- ✅ 创建和分配 Issue
- ✅ Review 所有代码
- ✅ 合并代码
- ✅ 创建 Release
- ❌ 不直接开发功能代码

### 成员 A/B Agent

**开发仓库**：
- ✅ 阅读自己的 AGENTS.md
- ✅ 阅读开发指南
- ✅ 查看项目管理文档
- ❌ 不修改开发仓库内容

**主仓库**：
- ✅ 认领分配的 Issue
- ✅ 创建功能分支
- ✅ 编写代码和测试
- ✅ 提交 PR
- ❌ 不修改其他 Agent 的模块
- ❌ 不合并代码（需要 PM Review）

### 成员 Test Agent

**开发仓库**：
- ✅ 阅读自己的 AGENTS.md
- ✅ 阅读测试规范
- ❌ 不修改开发仓库内容

**主仓库**：
- ✅ 认领测试任务
- ✅ 编写测试代码
- ✅ 创建测试报告
- ❌ 不修改功能代码
- ❌ 不合并代码

---

## 信息传递方式

### 从开发仓库到主仓库

**方式**：Agent 阅读开发仓库的文档，指导主仓库的开发

**示例**：
```bash
# Agent 在开发仓库阅读规范
# 当前在 <dev-repo>
cat development-guide/push-rules.md

# Agent 在主仓库提交代码（遵循规范）
cd ../knowledge-assistant  # 切换到主仓库
git add scripts/template_engine.py
git commit -m "feat(template): add template engine

- Implement TemplateEngine class
- Support variable substitution
- Add unit tests

Issue: #A2"
git push origin feature/a-template-engine
```

### 从主仓库到开发仓库

**方式**：PM 根据主仓库的进展，更新开发仓库的文档

**示例**：
```bash
# PM 在主仓库完成功能开发
# 当前在 <main-repo>
# ... 开发和合并 ...

# PM 在开发仓库更新状态
cd ../knowledge-assistant-dev  # 切换到开发仓库
# 更新项目管理文档
# 记录里程碑完成情况
git add project-management/sprint-1.md
git commit -m "docs: update sprint 1 progress"
git push origin main
```

---

## 冲突处理

### 主仓库代码冲突

**原因**：多个 Agent 修改同一文件

**预防**：
1. 模块边界清晰（参考 agents/*/AGENTS.md）
2. Agent 只修改自己负责的模块
3. 提交前先 pull 最新代码

**解决**：
1. Agent 本地解决冲突
2. 重新提交 PR
3. PM Review 冲突解决

---

## 紧急情况处理

### 主仓库发现严重 Bug

**流程**：
```
1. 在主仓库创建紧急 Issue
2. PM 分配给相关 Agent
3. Agent 修复并提交 PR
4. PM 优先 Review
5. 快速合并和发布
```

---

## 检查清单

### Agent 开始工作前

- [ ] 已克隆两个仓库
- [ ] 已阅读自己的 AGENTS.md（开发仓库）
- [ ] 已阅读相关开发指南（开发仓库）
- [ ] 已认领分配的 Issue（主仓库）

### Agent 提交代码前

- [ ] 代码符合 coding-standards.md（开发仓库）
- [ ] 测试符合 testing-standards.md（开发仓库）
- [ ] 提交信息符合 commit-standards.md（开发仓库）
- [ ] 推送符合 push-rules.md（开发仓库）
- [ ] 已运行所有测试并通过

### PM Review 前

- [ ] 已阅读 review-checklist.md（开发仓库）
- [ ] 已检查测试覆盖率
- [ ] 已验证功能正确性

---

**版本**: v1.0  
**更新日期**: 2026-03-05  
**维护者**: PM Agent
