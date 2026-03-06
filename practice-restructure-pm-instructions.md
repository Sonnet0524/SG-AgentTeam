# 文档结构调整 - PM Agent执行说明

> 📋 本文档是给PM Agent的调整指令，用于完成实践部分的结构重组

**创建时间**: 2026-03-06  
**执行者**: PM Agent  
**前置条件**: Research Agent先完成框架部分调整

---

## ⚠️ 重要提醒

在执行本调整前，必须确保：
1. ✅ Research Agent已完成 `docs/methodology/` 的调整
2. ✅ 所有Agent处于Idle状态，无进行中的任务
3. ✅ 当前代码已全部提交

---

## 🔄 Agent配置调整（重要！）

调整后需要同步更新以下文件：

### 5.1 更新 opencode.json

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "pm": {
      "description": "PM - 项目管理和协调",
      "mode": "primary",
      "prompt": "{file:./practice/agents/pm/CATCH_UP.md}",  // 路径更新
      "permission": { ... }
    },
    "data": {
      "prompt": "{file:./practice/agents/data/CATCH_UP.md}",  // 路径更新
      ...
    },
    "template": {
      "prompt": "{file:./practice/agents/template/CATCH_UP.md}",  // 路径更新
      ...
    },
    "test": {
      "prompt": "{file:./practice/agents/test/CATCH_UP.md}",  // 路径更新
      ...
    },
    "research": {
      "prompt": "{file:./practice/agents/research/CATCH_UP.md}",  // 路径更新
      ...
    }
  }
}
```

### 5.2 更新各Agent的CATCH_UP.md

每个Agent的CATCH_UP.md中引用的路径都需要更新：

**路径映射表**:

| 原路径 | 新路径 |
|--------|--------|
| `../project-management/` | `../management/` |
| `../knowledge-base/` | `../knowledge-base/` (相对位置不变) |
| `../agent-status.md` | `../status/agent-status.md` |
| `../../HUMAN_ADMIN.md` | `../../status/human-admin.md` |
| `../development-guide/` | `../development-guide/` (相对位置不变) |

**需要更新的文件列表**:
- `practice/agents/pm/CATCH_UP.md`
- `practice/agents/data/CATCH_UP.md`
- `practice/agents/template/CATCH_UP.md`
- `practice/agents/test/CATCH_UP.md`
- `practice/agents/research/CATCH_UP.md`

### 5.3 更新各Agent的ESSENTIALS.md

同样更新路径引用：
- `practice/agents/pm/ESSENTIALS.md`
- `practice/agents/data/ESSENTIALS.md`
- `practice/agents/template/ESSENTIALS.md`
- `practice/agents/test/ESSENTIALS.md`
- `practice/agents/research/ESSENTIALS.md`

---

## 📋 调整任务清单

### Task 1: 创建新目录结构

```bash
# 创建practice目录及其子目录
mkdir -p practice/agents
mkdir -p practice/management
mkdir -p practice/knowledge-base
mkdir -p practice/reports
mkdir -p practice/logs/archives
mkdir -p practice/logs/work-logs
mkdir -p practice/status/task-assignments
mkdir -p practice/meeting-notes
mkdir -p practice/decisions
mkdir -p practice/examples
mkdir -p practice/templates
mkdir -p practice/development-guide
```

---

### Task 2: 移动目录

**执行顺序**：按以下顺序移动，避免路径冲突

| 步骤 | 命令 | 说明 |
|------|------|------|
| 2.1 | `mv agents practice/agents` | Agent配置 |
| 2.2 | `mv project-management practice/management` | 项目管理 |
| 2.3 | `mv knowledge-base practice/knowledge-base` | 知识库 |
| 2.4 | `mv reports practice/reports` | 报告 |
| 2.5 | `mv interaction-logs practice/logs` | 交互日志 |
| 2.6 | `mv meeting-notes practice/meeting-notes` | 会议记录 |
| 2.7 | `mv decisions practice/decisions` | 决策记录 |
| 2.8 | `mv examples practice/examples` | 示例 |
| 2.9 | `mv templates practice/templates` | 模板 |
| 2.10 | `mv development-guide practice/development-guide` | 开发指南 |

---

### Task 3: 移动根目录文件

| 步骤 | 命令 | 说明 |
|------|------|------|
| 3.1 | `mv HUMAN_ADMIN.md practice/status/human-admin.md` | 项目总览 |
| 3.2 | `mv agent-status.md practice/status/agent-status.md` | Agent状态 |
| 3.3 | `mv AGENTS_USAGE.md practice/development-guide/agents-usage.md` | 使用指南 |
| 3.4 | `mv task-assignments-*.md practice/status/task-assignments/` | 任务分配 |
| 3.5 | `mv WORK_LOG_*.md practice/logs/work-logs/` | 工作日志 |
| 3.6 | `mv REFACTOR_REPORT.md practice/reports/` | 重构报告 |

---

### Task 4: 创建实践部分入口文档

创建 `practice/README.md`:

```markdown
# Knowledge Assistant - 实践部分

> 🛠️ 本项目的Agent Team设计与实现

**项目**: Knowledge Assistant  
**框架**: [Agent Team Framework](../docs/)  
**状态**: 开发中

---

## 📋 项目概述

**项目目标**: 个人知识管理助手  
**开发模式**: AI Agent Team协作开发  
**验证重点**: Agent Team Framework的可行性

---

## 👥 团队配置

| Agent | 职责 | 模块边界 |
|-------|------|---------|
| **PM** | 项目管理、协调、进度跟踪 | management/ |
| **Data** | 数据模型、解析器、存储层 | 数据模块 |
| **Template** | 模板引擎、配置系统 | 模板模块 |
| **Test** | 测试框架、质量保证 | 测试模块 |
| **Research** | 框架研究、方法论提炼 | 研究文档 |

---

## 📁 目录结构

```
practice/
├── agents/             # 🤖 Agent配置
├── management/         # 📊 项目管理
├── knowledge-base/     # 🧠 知识库
├── reports/            # 📝 报告
├── logs/               # 📋 日志
│   ├── archives/       # 归档日志
│   └── work-logs/      # 工作日志
├── status/             # 📈 状态文档
├── meeting-notes/      # 📅 会议记录
├── decisions/          # 🎯 决策记录
├── examples/           # 📚 示例
├── templates/          # 📄 模板文件
└── development-guide/  # 🔧 开发指南
```

---

## 🚀 快速开始

### 启动Agent

```bash
# 启动 PM Agent
./start-pm.sh   # Linux/Mac
start-pm.bat    # Windows

# 其他Agent类似
./start-data.sh
./start-template.sh
./start-test.sh
./start-research.sh
```

### Agent入口

每个Agent通过 `agents/<name>/CATCH_UP.md` 快速恢复上下文。

---

## 📊 当前状态

详见: [状态总览](status/human-admin.md)

---

## 📚 相关文档

- [框架文档](../docs/) - Agent Team Framework理论
- [开发指南](development-guide/) - 开发规范
- [知识库](knowledge-base/) - 项目经验
```

---

### Task 5: 更新 opencode.json

修改Agent配置中的路径引用：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "pm": {
      "description": "PM - 项目管理和协调",
      "mode": "primary",
      "prompt": "{file:./practice/agents/pm/CATCH_UP.md}",
      "permission": {
        "edit": "ask",
        "bash": {
          "git push": "ask",
          "git *": "allow"
        }
      }
    },
    "data": {
      "description": "Data - 数据类型、解析器和工具",
      "mode": "primary",
      "prompt": "{file:./practice/agents/data/CATCH_UP.md}",
      "permission": {
        "edit": "ask",
        "bash": {
          "git push": "ask",
          "pytest *": "allow",
          "black *": "allow",
          "flake8 *": "allow",
          "mypy *": "allow"
        }
      }
    },
    "template": {
      "description": "Template - 模板引擎和配置系统",
      "mode": "primary",
      "prompt": "{file:./practice/agents/template/CATCH_UP.md}",
      "permission": {
        "edit": "ask",
        "bash": {
          "git push": "ask",
          "pytest *": "allow",
          "black *": "allow",
          "flake8 *": "allow",
          "mypy *": "allow"
        }
      }
    },
    "test": {
      "description": "Test - 测试框架和质量保证",
      "mode": "primary",
      "prompt": "{file:./practice/agents/test/CATCH_UP.md}",
      "permission": {
        "edit": "deny",
        "bash": {
          "pytest *": "allow",
          "git diff": "allow",
          "git log*": "allow"
        }
      }
    },
    "research": {
      "description": "Research - 框架层面的研究专家",
      "mode": "primary",
      "prompt": "{file:./practice/agents/research/CATCH_UP.md}",
      "permission": {
        "edit": "ask",
        "bash": {
          "git push": "ask",
          "git add": "allow",
          "git commit": "allow"
        }
      }
    }
  }
}
```

---

### Task 6: 更新各Agent的CATCH_UP.md

根据路径映射表，更新每个Agent的CATCH_UP.md中的路径引用。

**详细路径更新清单**:

#### PM Agent (`practice/agents/pm/CATCH_UP.md`)
```
原路径                              →  新路径
../project-management/              →  ../management/
../agent-status.md                  →  ../status/agent-status.md
../../HUMAN_ADMIN.md                →  ../../status/human-admin.md
```

#### Data Agent (`practice/agents/data/CATCH_UP.md`)
```
原路径                              →  新路径
../knowledge-base/                  →  ../knowledge-base/ (不变)
```

#### Template Agent (`practice/agents/template/CATCH_UP.md`)
```
原路径                              →  新路径
../knowledge-base/                  →  ../knowledge-base/ (不变)
```

#### Test Agent (`practice/agents/test/CATCH_UP.md`)
```
原路径                              →  新路径
../knowledge-base/                  →  ../knowledge-base/ (不变)
```

#### Research Agent (`practice/agents/research/CATCH_UP.md`)
```
原路径                              →  新路径
../../docs/research/                →  ../../docs/research/ (不变)
../../docs/methodology/             →  ../../docs/methodology/ (不变)
```

---

### Task 7: 更新各Agent的ESSENTIALS.md

同样更新路径引用（如果有的话）。

---

### Task 8: 更新根目录README.md

调整README中实践篇部分的路径链接：

```markdown
# 🛠️ 实践篇

> 位置: `practice/`

## 📋 项目概述
...

## 🏗️ 架构设计

### 目录结构

```
practice/
├── agents/             # 🤖 Agent配置目录
│   ├── pm/             # PM Agent
│   ├── data/           # Data Agent
│   ├── template/       # Template Agent
│   ├── test/           # Test Agent
│   └── research/       # Research Agent
├── management/         # 📊 项目管理（PM负责）
├── knowledge-base/     # 🧠 知识库（项目级）
├── development-guide/  # 🔧 开发指南
├── logs/               # 📝 Agent交互日志
└── status/             # 📈 状态文档
    ├── agent-status.md
    └── human-admin.md
```

...

## 🚀 快速开始

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
```

---

## ✅ 执行后检查清单

完成所有任务后，执行以下检查：

### 检查1: 目录结构验证

```bash
# 验证新目录结构
ls -la practice/
ls -la practice/agents/
ls -la practice/management/
ls -la practice/status/
```

### 检查2: 文件存在性验证

- [ ] `practice/README.md` 存在
- [ ] `practice/agents/pm/CATCH_UP.md` 存在
- [ ] `practice/management/roadmap.md` 存在
- [ ] `practice/status/agent-status.md` 存在
- [ ] `practice/status/human-admin.md` 存在

### 检查3: 配置文件验证

- [ ] `opencode.json` 中的路径已更新
- [ ] 启动PM Agent能正常加载CATCH_UP.md

### 检查4: 链接验证

- [ ] README.md中的链接可访问
- [ ] practice/README.md中的链接可访问
- [ ] 各Agent CATCH_UP.md中的链接可访问

---

## 📝 执行记录模板

执行时请记录：

```markdown
## 执行记录

**执行时间**: YYYY-MM-DD HH:MM
**执行者**: PM Agent

### 完成的任务
- [x] Task 1: 创建目录结构
- [x] Task 2: 移动目录
- [x] Task 3: 移动文件
- [x] Task 4: 创建入口文档
- [x] Task 5: 更新opencode.json
- [x] Task 6: 更新Agent CATCH_UP.md
- [x] Task 7: 更新Agent ESSENTIALS.md
- [x] Task 8: 更新根README.md

### 遇到的问题
（记录任何问题）

### 验证结果
- [ ] 目录结构正确
- [ ] 配置文件正确
- [ ] 链接可访问
- [ ] Agent可正常启动
```

---

## 🔄 回滚方案

如果调整过程中出现问题，执行以下回滚：

```bash
# 回滚所有移动（逆向操作）
mv practice/agents agents
mv practice/management project-management
mv practice/knowledge-base knowledge-base
mv practice/reports reports
mv practice/logs interaction-logs
mv practice/meeting-notes meeting-notes
mv practice/decisions decisions
mv practice/examples examples
mv practice/templates templates
mv practice/development-guide development-guide

# 回滚文件移动
mv practice/status/human-admin.md HUMAN_ADMIN.md
mv practice/status/agent-status.md agent-status.md
mv practice/development-guide/agents-usage.md AGENTS_USAGE.md

# 恢复opencode.json
git checkout opencode.json

# 删除practice目录
rm -rf practice
```

---

**维护者**: Research Agent  
**创建日期**: 2026-03-06
