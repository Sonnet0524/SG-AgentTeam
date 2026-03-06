# Knowledge Base Index

> 按需检索的知识库索引

---

## Quick Search

### By Agent

**Data Agent**
- YAML Parsing: `experiences/data/001-yaml-parsing.md`
- Data Validation: `experiences/data/002-validation.md`
- File Operations: `patterns/data-001-file-ops.md`

**Template Agent**
- Template Rendering: `experiences/template/001-rendering.md`
- Variable Substitution: `experiences/template/002-variables.md`
- Template Syntax: `patterns/template-001-syntax.md`

**Test Agent**
- Test Patterns: `experiences/test/001-patterns.md`
- Coverage Strategy: `experiences/test/002-coverage.md`
- Fixtures: `patterns/test-001-fixtures.md`

---

## By Topic

### Performance
- Large File Handling: `patterns/perf-001-large-files.md`
- Memory Optimization: `patterns/perf-002-memory.md`

### Testing
- Unit Testing: `patterns/test-001-unit.md`
- Integration Testing: `patterns/test-002-integration.md`
- Mock Strategies: `patterns/test-003-mocks.md`

### Code Quality
- Error Handling: `patterns/quality-001-errors.md`
- Type Annotations: `patterns/quality-002-types.md`

---

## Recent Additions

| File | Agent | Date | Topic |
|------|-------|------|-------|
| `experiences/data/001-yaml-parsing.md` | Data | 2026-03-06 | YAML frontmatter parsing |
| `experiences/template/001-rendering.md` | Template | 2026-03-06 | Template rendering basics |
| `patterns/test-001-unit.md` | Test | 2026-03-06 | Unit testing patterns |

---

## Usage Guidelines

### For Agents

**Search by Problem**:
```
# 遇到YAML解析问题
grep -r "yaml" experiences/data/

# 遇到测试问题
grep -r "test" experiences/test/
```

**Search by File**:
```
# 直接读取文件
cat experiences/data/001-yaml-parsing.md

# 查看模式
cat patterns/template-001-syntax.md
```

### For PM

**Update Index**:
- 添加新经验后，- 更新本文件索引
- 保持分类清晰

---

## Stats

- Total Experiences: 3
- Total Patterns: 3
- Last Updated: 2026-03-06
- Next Update: When new experience added

---

**Note**: 只在需要时读取具体文件，