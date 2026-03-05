# Agent A - Catch Up

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-05  
**Status**: 🟡 Idle  
**Current Task**: None  

---

## Who You Are

**Role**: Template System Developer  
**Expertise**: Document templates, configuration management  
**Working Directory**: `<main-repo>` (main repository)
  - 从dev仓库切换: `cd ../knowledge-assistant`
  - 绝对路径: 根据实际环境确定

---

## Your Responsibilities

### Primary Modules
```
scripts/
├── template_engine.py    # ✅ Your module
├── config.py             # ✅ Your module
└── tools/
    └── create_document.py # ✅ Your module

templates/                # ✅ Your module
├── daily-note.md
├── research-note.md
├── meeting-minutes.md
├── task-list.md
└── knowledge-card.md
```

### Do NOT Touch
```
scripts/
├── types.py              # ❌ Agent B's module
├── utils.py              # ❌ Agent B's module
├── metadata_parser.py    # ❌ Agent B's module
└── tools/
    ├── organize_notes.py   # ❌ Agent B's module
    ├── generate_index.py   # ❌ Agent B's module
    └── extract_keywords.py # ❌ Agent B's module
```

---

## Current Sprint

**Sprint**: Sprint 1 (Mar 5-20, 2026)  
**Your Tasks**: See assigned issues in main repo

### Planned Work (Week 2)
- Template engine implementation
- Create 5 document templates
- Config system implementation
- Unit tests

---

## How to Start Working

### Step 1: Check Status
```bash
# Go to main repo (from dev repo)
cd ../knowledge-assistant
# Or use absolute path if needed: cd <main-repo>

# Check your assigned issues
# (PM will create and assign)
```

### Step 2: Pick an Issue
1. Go to GitHub Issues
2. Find issues assigned to you (label: `agent: A`)
3. Comment: "Starting work on this issue"

### Step 3: Create Branch
```bash
# Create feature branch
git checkout -b feature/a-<issue-name>

# Example:
git checkout -b feature/a-template-engine
```

### Step 4: Develop
```bash
# Write tests first (TDD)
# Implement code
# Run tests
pytest tests/test_template_engine.py -v
pytest tests/ --cov=scripts --cov-report=term-missing
```

### Step 5: Submit
```bash
# Commit with proper message
git commit -m "feat(template): add template engine

- Implement TemplateEngine class
- Support variable substitution
- Add unit tests

Issue: #A2"

# Push to your branch
git push origin feature/a-template-engine

# Create PR on GitHub
# Target: main branch
# Add PM as reviewer
```

---

## Code Standards

### Must Have
- [ ] PEP 8 compliant (use black)
- [ ] Type annotations on all functions
- [ ] Docstrings on all public APIs
- [ ] Unit tests (coverage >80%)
- [ ] No code in others' modules

### Testing
```python
# Example test structure
def test_template_load_success():
    """Test successful template loading"""
    engine = TemplateEngine('./templates')
    content = engine.load_template('daily-note')
    assert '{{date}}' in content

def test_template_render():
    """Test template rendering with variables"""
    engine = TemplateEngine('./templates')
    result = engine.render('daily-note', date='2026-03-05')
    assert '2026-03-05' in result
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

Issue: #<number>

Types: feat, fix, docs, test, refactor, chore
Scope: template, config, tools
```

---

## Module Boundaries

### You Can Use
- `scripts/types.py` (import DocumentMetadata from Agent B)
- `scripts/utils.py` (import utility functions from Agent B)

### You Should Export
```python
# scripts/template_engine.py
class TemplateEngine:
    def load_template(self, name: str) -> str: ...
    def render(self, name: str, **kwargs) -> str: ...

# scripts/config.py
class Config:
    def load(self, path: str) -> Dict: ...
    def validate(self) -> bool: ...
```

---

## Common Tasks

### Create a New Template
1. Design template structure
2. Define variables: `{{variable}}`
3. Add to templates/ directory
4. Write usage documentation
5. Add tests

### Implement Config System
1. Define config schema (YAML)
2. Implement loader
3. Add validation
4. Write tests
5. Document config options

---

## Before You Start

### Check These Files
- [ ] `agents/member-a/AGENTS.md` - Your full config
- [ ] `project-management/sprint-1.md` - Sprint plan
- [ ] Main repo README.md - Project overview

### Verify Environment
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip install -r requirements.txt

# Verify you're in main repo
pwd  # Should show knowledge-assistant
```

---

## Communication Protocol

### When Starting Task
1. Comment on issue: "Starting work"
2. Create branch
3. Start development

### When Blocked
1. Comment on issue with problem
2. Add `blocked` label
3. Wait for PM assistance

### When Complete
1. Push to branch
2. Create PR
3. Request PM review
4. Wait for feedback

---

## Quick Reference

### Useful Commands
```bash
# Format code
black scripts/template_engine.py

# Check code
flake8 scripts/template_engine.py

# Type check
mypy scripts/template_engine.py

# Run tests
pytest tests/test_template_engine.py -v

# Check coverage
pytest tests/ --cov=scripts --cov-report=term-missing
```

### File Locations
- Your code: `scripts/template_engine.py`, `scripts/config.py`
- Templates: `templates/*.md`
- Tests: `tests/test_template_engine.py`, `tests/test_config.py`
- Docs: `docs/` (PM creates, you may add examples)

---

## Health Check

- [ ] Understand your role
- [ ] Know your modules
- [ ] Know module boundaries
- [ ] Understand workflow
- [ ] Ready to start

---

**Need Help?** Check `agents/member-a/AGENTS.md` for detailed instructions.
