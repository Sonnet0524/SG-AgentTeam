# Core Team - 启动文档

> 🔄 **启动时读取此文档** - 快速了解当前状态和工作

---

## Quick Status

**Last Updated**: 2026-03-07  
**Current Phase**: v1.1 Sprint 2 - Task Assigned  
**Status**: 🔴 Tasks Reopened - Development Required  

---

## Current Focus

**Primary Task**: 🔴 **紧急任务 - 知识提取工具开发**

**Background**:
- Issues #8, #9 之前被错误关闭（声称完成但代码缺失）
- PM Team已调查确认代码完全缺失
- 现已重新开放，需要从头开发

**Immediate Actions**:
1. 🔴 **开始开发** - Issue #8: 关键词提取
   - TF-IDF 方法
   - TextRank 方法
   - 多语言支持（中英文）

2. 🔴 **开始开发** - Issue #9: 摘要生成
   - 抽取式摘要
   - 可配置长度
   - 保留关键信息

3. 📝 **编写单元测试**
   - 覆盖率 > 85%
   - 性能测试

**Deadline**: 2026-03-09（2天后）

**Priority**: P0（阻塞v1.1发布）

---

## Team Status

| Team | Status | Current Task |
|------|--------|--------------|
| Core Team | 🔴 Active | Sprint 2 开发中 (#8, #9) |
| AI Team | ✅ Complete | Sprint 1完成 |
| Integration Team | ✅ Sprint 3 Done | Skill和Agent配置完成 |

---

## 📋 任务详情

### Issue #8: 关键词提取
**Priority**: P0（阻塞发布）  
**Milestone**: Sprint 2  
**Expected**: 2026-03-09

**Requirements**:
- 实现TF-IDF方法
- 实现TextRank方法
- 支持中文处理
- 单元测试覆盖率 > 85%
- 性能：1000字符 < 1秒

### Issue #9: 摘要生成
**Priority**: P0（阻塞发布）  
**Milestone**: Sprint 2  
**Expected**: 2026-03-09

**Requirements**:
- 抽取式摘要
- 可配置长度
- 保留关键信息
- 单元测试覆盖率 > 85%
- 性能：1000字符 < 5秒

### ⚠️ 重要提醒
- **不要在完成前关闭Issue**
- 必须先提交PR
- PM Team Review通过后
- 代码合并到main后
- 才能关闭Issue

---

## 🎯 v1.1 Responsibilities

### 核心职责
- ✅ 类型系统 (已完成)
- ✅ 元数据解析 (已完成)
- ✅ 工具函数 (已完成)
- ✅ organize_notes (已完成)
- ✅ generate_index (已完成)
- 🔴 extract_keywords (Sprint 2 - **重新开放，需开发**)
- 🔴 generate_summary (Sprint 2 - **重新开放，需开发**)

### 不负责
- ❌ 向量嵌入 (AI Team)
- ❌ 语义搜索 (AI Team)
- ❌ 外部连接器 (Integration Team)

---

## 🚀 启动流程

### 1. 读取状态文档
```bash
# 已在dev仓库，直接读取
practice/agents/core/CATCH_UP.md    # 本文件
practice/status/agent-status.md     # 团队状态
```

### 2. 同步代码仓库
```bash
# 同步dev仓库
git pull origin main

# 同步main仓库
cd ../knowledge-assistant
git pull origin main
cd ../knowledge-assistant-dev
```

### 3. 检查任务
- 查看 GitHub Issues (label: `team: core`)
- 查看 `status/task-assignments/v1.1-task-assignments.md`

---

## Working Directory

**启动位置**: `D:\opencode\knowledge-assistant-dev` (dev仓库)

**操作main仓库时**:
- 相对路径: `../knowledge-assistant`
- 或使用工具的 `workdir` 参数

---

## Key Files to Reference

### Planning Documents
- `status/task-assignments/v1.1-task-assignments.md` - 任务分配
- `../knowledge-assistant/docs/PRD.md` - 产品需求

### Team Configs
- `agents/core/AGENTS.md` - Core Team配置

### Technical Docs
- `../knowledge-assistant/docs/api-reference.md` - API文档
- `../knowledge-assistant/docs/user-guide.md` - 用户指南

---

## Next Actions

### Sprint 2 - 立即开始 🔴

#### 1. 安装依赖
```bash
pip install jieba scikit-learn networkx
```

#### 2. 实现关键词提取 (Issue #8)
**文件**: `scripts/tools/extraction.py`

```python
def extract_keywords(
    text: str,
    method: str = "tfidf",  # or "textrank"
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    从文本中提取关键词
    
    Args:
        text: 输入文本（中文）
        method: 方法选择（tfidf或textrank）
        top_n: 返回关键词数量
    
    Returns:
        关键词列表，每个元素包含keyword和score
    """
    pass
```

#### 3. 实现摘要生成 (Issue #9)
**文件**: `scripts/tools/extraction.py`

```python
def generate_summary(
    text: str,
    max_length: int = 200
) -> Dict[str, Any]:
    """
    生成文本摘要
    
    Args:
        text: 输入文本（中文）
        max_length: 摘要最大长度（字符数）
    
    Returns:
        包含summary和key_sentences的字典
    """
    pass
```

#### 4. 编写单元测试
**文件**: `tests/test_extraction.py`
- 测试TF-IDF方法
- 测试TextRank方法
- 测试摘要生成
- 测试中文处理
- 覆盖率 > 85%

#### 5. 提交PR
- 确保所有测试通过
- 更新文档
- 提交PR等待PM Team Review

**Timeline**:
- Day 1: 实现关键词提取 + 测试
- Day 2: 实现摘要生成 + 测试 + PR

---

## Status Update

**更新 `agent-status.md`**:
- 开始任务时
- 提交代码后
- 遇到阻塞时
- 完成任务后

---

**Remember**: 
- 🔴 **任务已分配，立即开始开发**
- ⚠️ **不要在完成前关闭Issue**
- ✅ **必须提交PR，等待Review**
- 只修改自己负责的模块
- 不涉及AI/ML算法
- 专注于数据处理和文本分析
- 通过Issue与PM Team沟通

---

**Last Updated**: 2026-03-07 18:15  
**Next Action**: 开始Issue #8开发
