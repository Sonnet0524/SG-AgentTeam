# Issue Management

## Issue Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `priority: critical` | Red | Blocking issues |
| `priority: high` | Orange | Important tasks |
| `priority: medium` | Yellow | Normal tasks |
| `priority: low` | Gray | Minor tasks |
| `type: feature` | Blue | New features |
| `type: bug` | Red | Bug fixes |
| `type: docs` | Green | Documentation |
| `type: test` | Purple | Testing |
| `agent: A` | - | Agent A tasks |
| `agent: B` | - | Agent B tasks |
| `agent: test` | - | Agent Test tasks |

## Issue Template

### Title Format
```
[<type>] <scope>: <short description>

Examples:
[feat] metadata: add parser for YAML frontmatter
[fix] template: fix variable substitution bug
[test] config: add unit tests for config loader
```

### Body Template
```markdown
## Objective
Brief description of what needs to be done.

## Tasks
- [ ] Task 1
- [ ] Task 2

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

## Estimated Time
X days

## Related Files
- file1.py
- file2.py
```

## Assignment Rules

| Module | Assigned To | Example Labels |
|--------|-------------|----------------|
| types.py | Agent B | `agent: B`, `type: feature` |
| metadata_parser.py | Agent B | `agent: B`, `type: feature` |
| template_engine.py | Agent A | `agent: A`, `type: feature` |
| templates/*.md | Agent A | `agent: A`, `type: feature` |
| tests/test_*.py | All | `type: test` |
| docs/*.md | PM | `type: docs` |

## Status Workflow

```
Open → In Progress → Review → Done
                    ↓
                Blocked
```

### Status Indicators
- **Open**: Ready to start
- **In Progress**: Agent working
- **Review**: PR submitted, PM reviewing
- **Blocked**: Waiting for dependencies
- **Done**: Merged and closed

## Priority Guidelines

| Priority | Response Time | Examples |
|----------|---------------|----------|
| Critical | < 4 hours | Security issues, data loss bugs |
| High | < 1 day | Core features, blocking bugs |
| Medium | 2-3 days | Normal features, enhancements |
| Low | 1 week | Nice-to-haves, minor improvements |

## Example Issues

### Feature Issue
```
Title: [feat] metadata: implement metadata parser

## Objective
Create MetadataParser class to parse YAML frontmatter from markdown files.

## Tasks
- [ ] Implement parse() method
- [ ] Implement validate() method
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Add docstrings

## Acceptance Criteria
- [ ] Parses standard YAML frontmatter
- [ ] Validates required fields
- [ ] Returns clear error messages
- [ ] Test coverage >80%
- [ ] All tests pass

## Estimated Time
3 days

## Related Files
- scripts/metadata_parser.py
- tests/test_metadata_parser.py
```

### Bug Issue
```
Title: [fix] template: variable substitution fails with special chars

## Description
Template engine crashes when variable contains special characters like {, }, $.

## Steps to Reproduce
1. Create template with {{variable}}
2. Set variable = "test{value}"
3. Call render()

## Expected
Should handle special characters gracefully.

## Actual
Raises TemplateError.

## Environment
- Python 3.11
- OS: Ubuntu 22.04

## Estimated Time
0.5 day
```

---
**Version**: v1.0 | **Updated**: 2026-03-05 | **Owner**: PM Agent
