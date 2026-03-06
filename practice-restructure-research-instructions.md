# 文档结构调整 - Research Agent执行说明

> 📋 本文档是Research Agent自己的调整指南，用于完成框架部分的结构完善

**创建时间**: 2026-03-06  
**执行者**: Research Agent  
**执行时机**: PM Agent执行实践部分调整之前

---

## 🎯 调整目标

完善框架部分（`docs/`）的文档结构，确保：
1. 研究内容完整、独立
2. 方法论体系完善
3. 与实践部分清晰分离

---

## 📋 调整任务清单

### Task 1: 拆分 AGENT_TEAM_DESIGN.md

将 `AGENT_TEAM_DESIGN.md` 拆分为两部分：

#### 1.1 框架部分 → `docs/methodology/agent-team-design.md`

提取框架层面的设计理念和方法论，包括：
- 设计理念（Agent First vs Human First、Context窗口最小化、边界隔离）
- 通用工作流程（Agent启动、任务执行）
- Token-Based管理方法论
- 最佳实践（Context优化、模块边界维护、知识沉淀）
- 工具和配置说明（通用部分）
- 演化方向

**不包含**：
- 具体的Agent角色定义（这是实践层面的配置）
- 具体的文件路径引用（这是实践层面的实现）
- 项目特定的状态管理

#### 1.2 实践部分 → 由PM Agent处理

以下内容由PM Agent在 `practice/management/agent-team-implementation.md` 中维护：
- 具体的Agent角色定义（Data/Template/Test/PM）
- 具体的模块路径
- 项目特定的管理机制

---

### Task 2: 创建 `docs/methodology/agent-team-design.md`

创建新的方法论文档，内容结构：

```markdown
# Agent Team 设计方法论

> 📖 基于文档的Agent协作模式设计指南

**版本**: v1.0 | **更新**: 2026-03-06

---

## 一、设计理念

### 1.1 Agent First vs Human First

**Agent First原则**：
- 用于Agent之间的交互文档
- 格式：结构化、简洁、机器可读
- 示例：CATCH_UP.md, ESSENTIALS.md, 索引文件

**Human First原则**：
- 用于向用户汇报的文档
- 格式：人性化、易读、有温度
- 示例：用户报告、状态总览

**设计决策**：
```
Agent间通信 → Agent First (简洁高效)
Agent→用户 → 转化为Human First (易懂友好)
```

### 1.2 Context窗口最小化

**目标**：最小化Agent启动时的context消耗

**策略**：
1. **分层文档**：CATCH_UP (<50行) → ESSENTIALS (<100行) → 详细指南
2. **按需披露**：只读必需信息，详细指南按需加载
3. **索引机制**：通过索引快速检索，不预加载

**效果**：
- Context使用：从~600行降至~40行
- 节省：**93%**

### 1.3 边界隔离

**定义**：每个Agent的模块完全不重叠，零交叉修改

**目的**：
- 避免冲突
- 清晰职责
- 独立开发

**实现**：
- 每个Agent负责独立的目录和文件
- 通过public API交互
- 数据流单向

---

## 二、文档分层体系

### Level 0（必需）
- **大小**：<50行
- **加载时机**：启动时
- **内容**：当前状态、核心任务、约束条件
- **示例**：CATCH_UP.md

### Level 1（按需）
- **大小**：<100行
- **加载时机**：工作时
- **内容**：职责范围、工作流程、常用命令
- **示例**：ESSENTIALS.md

### Level 2（参考）
- **大小**：不限
- **加载时机**：按需查询
- **内容**：详细指南、参考资料、经验库
- **示例**：guides/, knowledge-base/

---

## 三、Token-Based管理方法论

### 3.1 概念定义

| 单位 | 定义 | 说明 |
|------|------|------|
| **Task** | 单个工作单元 | 预估token消耗 |
| **Checkpoint** | 相关Tasks集合 | 功能模块子集 |
| **Phase** | 功能模块 | 主要交付单元 |

### 3.2 进度跟踪

```
Phase (总预估)
├── Checkpoint (子预估)
│   ├── Task (实际消耗)
│   └── Task (实际消耗)
└── Checkpoint (子预估)

Progress = 已完成token / 总预估token
Velocity = 已完成token / 工作时间
ETA = 剩余token / Velocity
```

### 3.3 优势

- 精确预估工作量
- 实时进度跟踪
- 准确ETC预测
- 不依赖自然时间

---

## 四、最佳实践

### 4.1 Context优化

**DO**：
- ✅ 启动时只读CATCH_UP.md
- ✅ 按需读取ESSENTIALS.md
- ✅ 使用索引检索知识库
- ✅ 详细信息放在详细文档中

**DON'T**：
- ❌ 启动时读取所有文档
- ❌ 预加载知识库内容
- ❌ 在入口文档中包含详细指南

### 4.2 模块边界维护

**DO**：
- ✅ 只修改自己负责的模块
- ✅ 通过public API使用其他Agent模块
- ✅ 遇到边界问题立即上报

**DON'T**：
- ❌ 跨越模块边界修改
- ❌ 直接访问其他Agent的内部实现
- ❌ 破坏现有public API

### 4.3 知识沉淀

**DO**：
- ✅ 完成重要任务后总结经验
- ✅ 记录问题和解决方案
- ✅ 贡献到知识库
- ✅ 更新索引

**DON'T**：
- ❌ 完成任务后不总结
- ❌ 经验只留在会话中
- ❌ 知识库长期不更新

---

## 五、架构模式

### 5.1 分层协作架构

```
┌─────────────────────────────────────────────────┐
│                    Human                          │
│                  (决策、监控)                       │
└───────────────────┬─────────────────────────────┘
                     │
             ┌───────┴───────┐
             │  PM/Coordinator │ ← 协调层
             └───────┬───────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ Agent A │  │ Agent B │  │ Agent C │ ← 执行层
   └─────────┘  └─────────┘  └─────────┘
        │            │            │
        └────────────┴────────────┘
                     │
              文档化交互
            (共享上下文)
```

### 5.2 信息流设计

- **Agent First场景**：Agent间协作、自动化流程
- **Human First场景**：用户报告、状态汇报
- **动态切换**：根据受众选择合适的表达方式

---

## 六、演化方向

### 短期
- 交互协议标准化
- 文档模板完善

### 中期
- 半自动化协作
- 智能推荐机制

### 长期
- 完整通用框架
- 开源生态建设

---

**相关文档**：
- [文档分层体系](document-hierarchy.md)
- [Context最小化](context-minimization.md)
- [边界隔离](boundary-isolation.md)
```

---

### Task 3: 更新 `docs/README.md`

调整docs/README.md，明确其作为框架文档的定位：

**主要修改**：

1. **标题和定位**：
```markdown
# Agent Team Framework - 框架文档

> 📚 本目录包含Agent协作模式的通用理论和方法论

**性质**: 框架研究 | **可复用**: 是
```

2. **内容导航**：
```markdown
## 📖 文档导航

### 核心研究
- [Agent交互模式](research/agent-interaction/) - 基于文档的协作模式
- [信息流架构](research/information-architecture/) - 三层架构设计
- [Token-Based管理](research/token-based/) - 工作量度量方法

### 方法论
- [文档分层体系](methodology/document-hierarchy.md) - Level 0/1/2设计
- [Context最小化](methodology/context-minimization.md) - 优化策略
- [边界隔离](methodology/boundary-isolation.md) - 冲突避免
- [Agent Team设计](methodology/agent-team-design.md) - 总体设计理念

### 实践验证
- [Knowledge Assistant验证](practice/knowledge-assistant/) - 本项目的验证报告
- [经验教训](practice/lessons-learned/) - 框架层面的总结

### 参考资料
- [对比分析](reference/comparison.md) - 与其他方法对比
- [术语表](reference/glossary.md) - 统一术语定义
- [未来方向](reference/future-directions.md) - 研究规划
```

3. **与实践部分的关系**：
```markdown
## 🔗 与实践部分的关系

本目录是**框架篇**，包含通用的理论和方法论。

具体项目的实现细节在 **[实践篇](../practice/)** 中：
- Agent配置
- 项目管理
- 知识库
- 报告和日志
```

---

### Task 4: 删除原 AGENT_TEAM_DESIGN.md

拆分完成后，删除根目录的 `AGENT_TEAM_DESIGN.md`：

```bash
rm AGENT_TEAM_DESIGN.md
```

---

### Task 5: 更新 `docs/practice/` 定位

确保 `docs/practice/` 目录明确其作为**框架验证报告**的定位：

**docs/practice/knowledge-assistant/README.md 应包含**：
- 框架在本项目中的验证过程
- 框架理论的实践证据
- 对框架的改进建议

**不包含**：
- 具体的项目状态（在 `practice/status/`）
- 项目管理细节（在 `practice/management/`）

---

## ✅ 执行后检查清单

- [ ] `docs/methodology/agent-team-design.md` 已创建
- [ ] `docs/README.md` 已更新
- [ ] `AGENT_TEAM_DESIGN.md` 已删除
- [ ] `docs/practice/` 定位明确
- [ ] 所有内部链接正确

---

## 📝 执行记录

```markdown
## 执行记录

**执行时间**: 2026-03-06
**执行者**: Research Agent

### 完成的任务
- [x] Task 1: 拆分AGENT_TEAM_DESIGN.md
- [x] Task 2: 创建agent-team-design.md
- [x] Task 3: 更新docs/README.md
- [x] Task 4: 删除原文件
- [x] Task 5: 更新practice定位

### 验证结果
- [ ] 框架文档完整
- [ ] 与实践部分分离清晰
- [ ] 链接正确
```

---

**维护者**: Research Agent  
**创建日期**: 2026-03-06