# Project Overview

## 基本信息
- **名称**: Knowledge Assistant
- **类型**: 个人知识管理工具
- **架构**: 双仓库（dev: 私有, main: 公开）
- **语言**: Python 3.10+
- **团队**: PM + 3 Agents (A, B, Test)

## 功能模块

| 模块 | 负责人 | 核心文件 | 状态 |
|------|--------|----------|------|
| 元数据系统 | Agent B | types.py, metadata_parser.py, utils.py | ⏳ 待开发 |
| 模板系统 | Agent A | template_engine.py, config.py, templates/*.md | ⏳ 待开发 |
| 工具脚本 | Agent B | tools/organize_notes.py, generate_index.py, extract_keywords.py | ⏳ 待开发 |
| 测试系统 | Agent Test | tests/*.py | ⏳ 待开发 |

## 技术栈
- 依赖: pyyaml, python-frontmatter
- 测试: pytest, pytest-cov
- 规范: black, flake8, mypy

## 项目结构
```
scripts/
├── types.py              # Agent B
├── utils.py              # Agent B
├── metadata_parser.py    # Agent B
├── template_engine.py    # Agent A
├── config.py             # Agent A
└── tools/                # Agent B

templates/                # Agent A
├── daily-note.md
├── research-note.md
├── meeting-minutes.md
├── task-list.md
└── knowledge-card.md

tests/                    # All Agents
test-data/                # Agent Test
```

## 开发优先级
1. 元数据系统（基础）
2. 模板系统（基础）
3. 工具脚本（扩展）
4. 测试完善（持续）

---
**Version**: v1.0 | **Updated**: 2026-03-05 | **Owner**: PM Agent
