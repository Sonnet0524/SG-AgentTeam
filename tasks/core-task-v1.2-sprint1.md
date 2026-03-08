# Core Team任务：v1.2 Sprint 1 并行任务

## 📋 任务背景

v1.2 开发启动，需要并行完成多个独立任务。

## 🎯 任务列表（按优先级执行）

### Phase 1: TASK-C1 - Connector Framework Refactoring（P0，阻塞任务）

**Issue**: #37
**预计时间**: 2天

**任务要求**:
1. 增强 `scripts/connectors/base.py` 中的 BaseConnector 基类
2. 创建 `scripts/connectors/registry.py` - 连接器注册机制
3. 创建 `scripts/connectors/config.py` - 连接器配置管理
4. 添加错误处理和重试逻辑
5. 编写单元测试 `tests/test_connector_framework.py`

**验收标准**:
- 支持插件式添加新连接器
- 统一的配置接口
- 测试覆盖率 > 80%

### Phase 2: TASK-C4 - Abstractive Summarization（P1，独立任务）

**Issue**: #40
**预计时间**: 4天

**任务要求**:
1. 在 `scripts/tools/extraction.py` 添加 `generate_abstractive_summary()`
2. 支持 OpenAI API 和本地模型
3. 可配置摘要长度和风格
4. 提取式摘要作为 fallback
5. 编写单元测试

### Phase 2: TASK-C5 - Multi-language Support（P1，独立任务）

**Issue**: #41
**预计时间**: 3天

**任务要求**:
1. 创建 `scripts/utils/language.py` - 语言检测工具
2. 添加英文停用词
3. 集成 NLTK 或 spacy
4. 更新 `extract_keywords()` 支持英文
5. 更新 `generate_summary()` 支持英文
6. 编写单元测试

## 📁 相关文件

```
scripts/
├── connectors/
│   ├── base.py          # 增强基类
│   ├── registry.py      # NEW: 注册机制
│   └── config.py        # NEW: 配置管理
├── tools/
│   └── extraction.py    # 添加抽象式摘要
└── utils/
    └── language.py      # NEW: 语言检测

tests/
├── test_connector_framework.py
├── test_abstractive_summary.py
└── test_multilanguage.py
```

## ⚠️ 注意事项

1. **执行顺序**: 先完成 TASK-C1（阻塞任务），然后并行执行 TASK-C4 和 TASK-C5
2. **依赖**: TASK-C1 无依赖，可立即开始
3. **测试**: 每个功能必须有对应的测试
4. **文档**: 更新相关 docstring

## 📤 输出要求

完成后在 `reports/core-report-v1.2-sprint1.md` 写入报告，包含：
1. 完成的任务列表
2. 创建/修改的文件
3. 测试结果
4. 遇到的问题

---
**创建者**: PM Team
**创建时间**: 2026-03-08
**Sprint**: v1.2 Sprint 1
