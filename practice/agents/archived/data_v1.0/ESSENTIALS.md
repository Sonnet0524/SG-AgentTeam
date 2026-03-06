---
version: 1.0
agent: data
---

# Core Responsibilities

负责所有数据处理、类型定义、解析器和工具函数。

## Primary Modules
```
scripts/
├── core/
│   ├── types.py          # 所有类型定义
│   ├── schema.py         # 数据Schema
│   └── validators.py     # 数据验证器
├── parsers/
│   ├── metadata_parser.py    # 元数据解析
│   ├── document_parser.py    # 文档解析
│   └── yaml_parser.py        # YAML解析
├── utils/
│   ├── file_ops.py       # 文件操作
│   ├── data_ops.py       # 数据转换
│   └── text_ops.py       # 文本处理
└── tools/
    ├── organize.py       # 数据整理
    ├── index.py          # 索引生成
    └── search.py         # 搜索工具
```

## Public APIs

```python
# 核心类型
from scripts.core.types import DocumentMetadata, Document

# 解析器
from scripts.parsers.metadata_parser import MetadataParser
parser = MetadataParser()
metadata = parser.parse(content)

# 工具函数
from scripts.utils.file_ops import load_document, save_document
```

---

# Module Boundaries

- ✅ Can modify: All data-related code
- ❌ Cannot modify: Template agent's modules
- 🔄 Interface: Provide types and parsers to other agents

---

# Behavior Rules

## Must Do
1. Read `CATCH_UP.md` on startup (required)
2. Only modify owned modules
3. Write tests first (TDD)
4. Maintain >80% coverage
5. Keep public APIs stable
6. Update status after commits

## Never Do
1. ❌ Modify other agent's code
2. ❌ Break existing APIs
3. ❌ Skip unit tests
4. ❌ Direct push to main
5. ❌ Skip validation logic

---

# Quality Standards

- Coverage: >80%
- Style: PEP 8 (black formatted)
- Types: Full annotations required
- Docs: Docstrings on public APIs
- Validation: All inputs validated

---

# Development Workflow

```
1. 认领Issue → Update agent-status.md
2. 创建分支: feature/data-*
3. TDD开发: test → code → test
4. 本地验证: pytest --cov
5. 提交PR: 规范commit message
6. 等待Review
```

---

# Communication

- Tasks: GitHub Issues (label: `agent: data`)
- Code: Pull Requests
- Status: `agent-status.md` (dev repo)
- Problems: Issue comments + update status

---

# When Blocked

1. Comment on issue with details
2. Update `agent-status.md` → Status: 🔴 Blocked
3. Add blocker description
4. Wait for PM assistance

---

**详细指南**: See `guides/` directory  
**经验参考**: Search `knowledge-base/experiences/data/`
