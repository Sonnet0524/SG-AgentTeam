# Agent B - Catch Up

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-05  
**Status**: 🟡 Idle  
**Current Task**: None  

---

## Who You Are

**Role**: Metadata & Tools Developer  
**Expertise**: Data parsing, algorithms, utility tools  
**Working Directory**: `<main-repo>` (main repository)
  - 从dev仓库切换: `cd ../knowledge-assistant`
  - 绝对路径: 根据实际环境确定

---

## Your Responsibilities

### Primary Modules
```
scripts/
├── types.py                # ✅ Your module
├── utils.py                # ✅ Your module
├── metadata_parser.py      # ✅ Your module
└── tools/
    ├── organize_notes.py   # ✅ Your module
    ├── generate_index.py   # ✅ Your module
    └── extract_keywords.py # ✅ Your module
```

### Do NOT Touch
```
scripts/
├── template_engine.py      # ❌ Agent A's module
├── config.py               # ❌ Agent A's module
└── tools/
    └── create_document.py  # ❌ Agent A's module

templates/                  # ❌ Agent A's module
```

---

## Current Sprint

**Sprint**: Sprint 1 (Mar 5-20, 2026)  
**Your Tasks**: See assigned issues in main repo

### Planned Work (Week 1)
- Define DocumentMetadata type
- Implement metadata parser
- Add validation logic
- Unit tests

### Planned Work (Week 3)
- Tool scripts implementation
- organize_notes.py
- generate_index.py
- extract_keywords.py

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
2. Find issues assigned to you (label: `agent: B`)
3. Comment: "Starting work on this issue"

### Step 3: Create Branch
```bash
# Create feature branch
git checkout -b feature/b-<issue-name>

# Example:
git checkout -b feature/b-metadata-parser
```

### Step 4: Develop
```bash
# Write tests first (TDD)
# Implement code
# Run tests
pytest tests/test_metadata_parser.py -v
pytest tests/ --cov=scripts --cov-report=term-missing
```

### Step 5: Submit
```bash
# Commit with proper message
git commit -m "feat(metadata): add metadata parser

- Implement MetadataParser class
- Support YAML frontmatter parsing
- Add validation logic
- Add unit tests

Issue: #B2"

# Push to your branch
git push origin feature/b-metadata-parser

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
def test_parse_basic_metadata():
    """Test basic metadata parsing"""
    parser = MetadataParser()
    content = """---
title: Test Document
date: 2026-03-05
---

Body content."""
    
    metadata, body = parser.parse(content)
    assert metadata['title'] == 'Test Document'
    assert 'Body content.' in body

def test_validate_required_fields():
    """Test validation of required fields"""
    parser = MetadataParser()
    metadata = {'title': 'Test'}  # Missing 'date'
    is_valid, errors = parser.validate(metadata)
    assert not is_valid
    assert 'date' in str(errors)
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

Issue: #<number>

Types: feat, fix, docs, test, refactor, chore
Scope: metadata, types, utils, tools
```

---

## Module Design

### types.py
```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class DocumentMetadata:
    """Document metadata structure"""
    title: str
    date: date
    tags: List[str] = None
    author: Optional[str] = None
    
    # Add validation methods
```

### metadata_parser.py
```python
import re
import yaml
from typing import Tuple, Dict, Any

class MetadataParser:
    """Parse and validate document metadata"""
    
    REQUIRED_FIELDS = ['title', 'date']
    
    def parse(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter from content"""
        # Implementation
        
    def validate(self, metadata: Dict) -> Tuple[bool, List[str]]:
        """Validate metadata against schema"""
        # Implementation
```

### Tools Pattern
```python
# scripts/tools/extract_keywords.py
from typing import List
from collections import Counter
import re

def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Extract keywords from text using TF-IDF"""
    # Implementation
```

---

## Before You Start

### Check These Files
- [ ] `agents/member-b/AGENTS.md` - Your full config
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
black scripts/metadata_parser.py

# Check code
flake8 scripts/metadata_parser.py

# Type check
mypy scripts/metadata_parser.py

# Run tests
pytest tests/test_metadata_parser.py -v

# Check coverage
pytest tests/ --cov=scripts --cov-report=term-missing
```

### File Locations
- Your code: `scripts/types.py`, `scripts/metadata_parser.py`, `scripts/utils.py`, `scripts/tools/*.py`
- Tests: `tests/test_types.py`, `tests/test_metadata_parser.py`, `tests/test_utils.py`, `tests/test_tools.py`

---

## Health Check

- [ ] Understand your role
- [ ] Know your modules
- [ ] Know module boundaries
- [ ] Understand workflow
- [ ] Ready to start

---

**Need Help?** Check `agents/member-b/AGENTS.md` for detailed instructions.
