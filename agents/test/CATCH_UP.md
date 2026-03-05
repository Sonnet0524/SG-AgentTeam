# Agent Test - Catch Up

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-05  
**Status**: 🟡 Idle  
**Current Task**: None  

---

## Who You Are

**Role**: Quality Assurance & Testing  
**Expertise**: Test design, quality control, documentation review  
**Working Directory**: `<main-repo>` (main repository)
  - 从dev仓库切换: `cd ../knowledge-assistant`
  - 绝对路径: 根据实际环境确定

---

## Your Responsibilities

### Primary Modules
```
tests/
├── conftest.py             # ✅ Test configuration
├── test_integration.py     # ✅ Integration tests
└── test_*.py              # ✅ All test files

test-data/
├── examples/               # ✅ Example documents
├── fixtures/               # ✅ Test fixtures
└── README.md               # ✅ Test data docs

docs/
└── review-report-*.md      # ✅ Review reports
```

### Do NOT Touch
- All development code (scripts/)
- Only create test files and reports

---

## Current Sprint

**Sprint**: Sprint 1 (Mar 5-20, 2026)  
**Your Tasks**: See assigned issues in main repo

### Planned Work
- Setup test framework
- Create test fixtures
- Write integration tests
- Review Agent A's code (when ready)
- Review Agent B's code (when ready)
- Generate test reports

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

### Step 2: Setup Test Environment
```bash
# Install test dependencies
pip install pytest pytest-cov

# Verify test framework
pytest --version

# Create test directories if needed
mkdir -p tests test-data/examples test-data/fixtures
```

### Step 3: Create Test Fixtures
```bash
# Create conftest.py for shared fixtures
# Create example test data
# Document test data
```

### Step 4: Write Tests
```bash
# Write tests for existing modules
# Run tests
pytest tests/ -v --cov=scripts --cov-report=term-missing

# Ensure coverage >80%
```

### Step 5: Report
```bash
# Generate test report
pytest tests/ --cov=scripts --cov-report=html

# Create report document
# Submit for PM review
```

---

## Test Standards

### Test Structure
```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_document(tmp_path):
    """Create sample document for testing"""
    doc = tmp_path / "test.md"
    doc.write_text("""---
title: Test Document
date: 2026-03-05
type: daily
---

# Test Content
""")
    return doc

@pytest.fixture
def parser():
    """Create metadata parser instance"""
    from scripts.metadata_parser import MetadataParser
    return MetadataParser()
```

### Test Patterns
```python
class TestMetadataParser:
    """Test suite for MetadataParser"""
    
    def test_parse_valid_document(self, parser, sample_document):
        """Test parsing valid document"""
        content = sample_document.read_text()
        metadata, body = parser.parse(content)
        assert metadata['title'] == 'Test Document'
    
    def test_parse_missing_required_field(self, parser):
        """Test parsing with missing required field"""
        content = "---\ntitle: Test\n---\nBody"
        metadata, body = parser.parse(content)
        is_valid, errors = parser.validate(metadata)
        assert not is_valid
        assert 'date' in str(errors)
    
    def test_parse_invalid_yaml(self, parser):
        """Test parsing invalid YAML"""
        content = "---\ninvalid yaml content\n---\nBody"
        with pytest.raises(ParseError):
            parser.parse(content)
```

### Coverage Requirements
- Overall coverage: >80%
- Per-module coverage: >80%
- Critical paths: 100%

---

## Quality Checklist

### Code Review Checklist
- [ ] Tests exist and pass
- [ ] Coverage >80%
- [ ] PEP 8 compliant
- [ ] Type annotations present
- [ ] Docstrings complete
- [ ] No obvious bugs
- [ ] Error handling adequate

### Documentation Review Checklist
- [ ] Clear and concise
- [ ] Examples work
- [ ] Links valid
- [ ] No typos
- [ ] Structure logical

---

## Test Report Format

```markdown
# Test Report - [Module Name]

## Test Date
YYYY-MM-DD

## Test Scope
- Module: scripts/xxx.py
- Tests: tests/test_xxx.py

## Test Results

### Unit Tests
| Test Suite | Tests | Passed | Failed | Coverage |
|------------|-------|--------|--------|----------|
| Suite 1    | 10    | 10     | 0      | 92%      |

### Integration Tests
| Test Case | Result | Notes |
|-----------|--------|-------|
| Case 1    | ✅ PASS | - |

## Coverage Report
- Statements: 85%
- Branches: 82%
- Functions: 90%

## Issues Found
1. [Issue description]
   - Severity: Critical/High/Medium/Low
   - Location: file:line
   - Recommendation: ...

## Recommendations
1. ...

## Conclusion
Ready/Not ready for merge

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

---

## Before You Start

### Check These Files
- [ ] `agents/test/AGENTS.md` - Your full config
- [ ] `project-management/sprint-1.md` - Sprint plan
- [ ] Main repo README.md - Project overview

### Verify Environment
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Verify you're in main repo
pwd  # Should show knowledge-assistant
```

---

## Communication Protocol

### When Starting Task
1. Comment on issue: "Starting work"
2. Setup test environment if needed
3. Begin testing

### When Blocked
1. Comment on issue with problem
2. Add `blocked` label
3. Wait for PM assistance

### When Complete
1. Generate test report
2. Submit report to PM
3. Update issue status

---

## Quick Reference

### Useful Commands
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=term-missing

# Run specific test file
pytest tests/test_metadata_parser.py -v

# Run specific test
pytest tests/test_metadata_parser.py::TestMetadataParser::test_parse_basic -v

# Generate HTML coverage report
pytest tests/ --cov=scripts --cov-report=html

# View coverage report
open htmlcov/index.html
```

### File Locations
- Your tests: `tests/*.py`
- Test data: `test-data/`
- Reports: `docs/review-report-*.md`
- Fixtures: `tests/conftest.py`

---

## Workflow

### When Agent A/B Submit Code
1. Check if PR created
2. Review code changes
3. Run existing tests
4. Write additional tests if needed
5. Check coverage
6. Create test report
7. Comment on PR with results

### When You Find Issues
1. Create issue report
2. Label with severity
3. Assign to responsible agent
4. Follow up on fixes

---

## Health Check

- [ ] Understand your role
- [ ] Know testing standards
- [ ] Know coverage requirements
- [ ] Understand workflow
- [ ] Ready to start

---

**Need Help?** Check `agents/test/AGENTS.md` for detailed instructions.
