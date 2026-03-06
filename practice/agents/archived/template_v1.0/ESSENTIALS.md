---
version: 1.0
agent: template
---

# Core Responsibilities

负责所有模板引擎、配置管理和文档创建工具。

## Primary Modules
```
scripts/
├── template/
│   ├── engine.py         # 模板引擎核心
│   ├── renderer.py       # 渲染器
│   ├── filters.py        # 过滤器
│   └── loader.py         # 加载器
├── config/
│   ├── manager.py        # 配置管理
│   ├── loader.py         # 配置加载
│   └── validator.py      # 配置验证
└── tools/
    └── creator.py        # 文档创建工具

templates/                  # 模板文件
├── daily.md              # 日记模板
├── research.md           # 研究笔记
├── meeting.md            # 会议纪要
├── task.md               # 任务清单
└── knowledge.md          # 知识卡片
```

## Public APIs

```python
# 模板引擎
from scripts.template.engine import TemplateEngine
engine = TemplateEngine('./templates')
template = engine.load_template('daily')
content = engine.render(template, context={'date': '2026-03-06'})

# 配置管理
from scripts.config.manager import ConfigManager
config = ConfigManager()
settings = config.load('config.yaml')
```

---

# Module Boundaries

- ✅ Can modify: All template and config code
- ❌ Cannot modify: Data agent's modules
- 🔄 Interface: Use `DocumentMetadata` type, provide rendering API

---

# Behavior Rules

## Must Do
1. Read `CATCH_UP.md` on startup (required)
2. Only modify owned modules
3. Write tests first (TDD)
4. Maintain >80% coverage
5. Keep template syntax documented
6. Update status after commits

## Never Do
1. ❌ Modify other agent's code
2. ❌ Break template compatibility
3. ❌ Skip unit tests
4. ❌ Direct push to main
5. ❌ Change public APIs without notice

---

# Quality Standards

- Coverage: >80%
- Style: PEP 8 (black formatted)
- Types: Full annotations required
- Docs: Template usage examples
- Templates: Variable documentation

---

# Template Development

## Creating New Template

```markdown
1. 设计模板结构
   - 定义变量: {{variable}}
   - 定义区块: {{#section}}...{{/section}}

2. 创建模板文件
   - 保存到 templates/
   - 使用 .md 格式

3. 添加文档
   - 列出所有变量
   - 提供使用示例

4. 编写测试
   - 测试加载
   - 测试渲染
   - 测试边界情况
```

---

# Development Workflow

```
1. 认领Issue → Update agent-status.md
2. 创建分支: feature/template-*
3. TDD开发: test → code → test
4. 本地验证: pytest --cov
5. 提交PR: 规范commit message
6. 等待Review
```

---

# Communication

- Tasks: GitHub Issues (label: `agent: template`)
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
**经验参考**: Search `knowledge-base/experiences/template/`
