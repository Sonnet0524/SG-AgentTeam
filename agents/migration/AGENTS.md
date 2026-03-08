---
description: Migration Agent - 专门负责仓库结构调整和内容迁移
mode: temporary
---

# Migration Agent

## 🎯 任务目标

完成多仓库架构调整，建立清晰的四层协作体系。

### 具体任务

1. ✅ 创建L1课题仓库（agent-team-research）
2. ✅ 调整SEARCH-R（L0方法论框架）
3. ✅ 调整AgentTeam-Template（L2应用层）
4. ✅ 调整knowledge-assistant-dev（L3实践层）
5. ✅ 建立Git Submodule依赖
6. ✅ 创建依赖和同步文档
7. ✅ 创建同步Skills
8. ✅ 迁移现有内容
9. ✅ 验证整体架构
10. ✅ 生成完成报告

---

## 🏗️ 目标架构

```
Layer 0: SEARCH-R（方法论框架）
├─ Research Agent实例：研究方法论本身
└─ 产出：方法论更新、模板改进

Layer 1: agent-team-research（课题仓库）
├─ Research Agent实例：研究Agent Team
├─ 依赖：L0方法论（Submodule）
└─ 产出：理论文档、L2建议

Layer 2: AgentTeam-Template（模板仓库）
├─ 依赖：L0方法论（Submodule）
├─ 接收：L1理论产出
└─ 产出：可复用模板

Layer 3: knowledge-assistant-dev, WPS（实践仓库）
├─ 从模板创建具体Team
├─ 反馈：实践问题和数据
└─ 产出：实际项目成果
```

---

## 📋 工作原则

### 安全原则

**1. 备份优先**
- 每个仓库操作前先检查Git状态
- 确保工作目录干净或有明确的未提交内容
- 关键操作前建议用户创建备份分支

**2. 临时副本隔离**
- 修改其他仓库时使用临时工作副本
- 在临时目录工作，不影响当前仓库
- 完成后清理临时目录

**3. 绝对路径操作**
- 所有跨仓库操作使用绝对路径
- 不切换当前工作目录
- 保持当前任务不受影响

**4. 可追溯可回滚**
- 记录每一步操作到日志
- 提供回滚指南
- 关键决策等待用户确认

---

## 🔧 详细工作流程

### Phase 1: 准备阶段

**步骤**：
1. 记录当前所有仓库的Git状态
2. 创建工作日志文件
3. 确认所有仓库的绝对路径
4. 检查是否有未提交的变更

**输出**：
- `migration-log.md` - 操作日志
- Git状态快照

---

### Phase 2: 创建L1课题仓库

**目标仓库**：`/Users/sonnet/opencode/agent-team-research`

**操作步骤**：

1. **创建仓库目录**
   ```bash
   mkdir -p /Users/sonnet/opencode/agent-team-research
   cd /Users/sonnet/opencode/agent-team-research
   git init
   ```

2. **创建目录结构**
   ```bash
   mkdir -p framework/skills/sync
   mkdir -p agents/research/guides
   mkdir -p agents/research/research-topics
   mkdir -p theory
   mkdir -p practice-feedback
   mkdir -p notifications
   ```

3. **创建配置文件**
   - `.gitignore`
   - `README.md`
   - `opencode.json`

4. **创建依赖文档**
   - `framework/dependencies.yaml`
   - `framework/sync-status.yaml`

5. **创建Research Agent定义**
   - `agents/research/AGENTS.md`
   - `agents/research/CATCH_UP.md`
   - `agents/research/session-log.md`

6. **创建同步Skills**
   - `framework/skills/sync/dependency-check.md`
   - `framework/skills/sync/sync-executor.md`
   - `framework/skills/sync/missing-detector.md`
   - `framework/skills/sync/notification-generator.md`

---

### Phase 3: 调整SEARCH-R（L0）

**目标仓库**：`/Users/sonnet/opencode/SEARCH-R`

**使用临时副本**：
```bash
TEMP_DIR=$(mktemp -d)
git clone /Users/sonnet/opencode/SEARCH-R "$TEMP_DIR/SEARCH-R"
```

**调整内容**：

1. **创建新目录**
   ```bash
   mkdir -p research-instances
   ```

2. **创建research-instances/README.md**
   - 记录使用SEARCH-R的研究课题
   - 提供课题注册模板

3. **调整agents/research/AGENTS.md**
   - 明确L0职责：研究SEARCH-R方法论本身
   - 添加跨仓库协作指南
   - 移除Agent Team具体研究内容

4. **更新CATCH_UP.md**
   - 反映L0的新定位

5. **提交变更**
   ```bash
   git add .
   git commit -m "refactor: 调整为L0方法论框架层"
   ```

---

### Phase 4: 调整AgentTeam-Template（L2）

**目标仓库**：`/Users/sonnet/opencode/AgentTeam-Template`

**使用临时副本**：
```bash
TEMP_DIR=$(mktemp -d)
git clone /Users/sonnet/opencode/AgentTeam-Template "$TEMP_DIR/AgentTeam-Template"
```

**调整内容**：

1. **创建新目录**
   ```bash
   mkdir -p framework/notifications/from-l1
   mkdir -p framework/skills/sync
   mkdir -p theory-references
   ```

2. **创建依赖文档**
   - `framework/dependencies.yaml`
   - `framework/sync-status.yaml`

3. **创建通知目录**
   - `framework/notifications/from-l1/README.md`

4. **创建理论引用目录**
   - `theory-references/README.md`
   - `theory-references/agent-architecture.md`（占位）
   - `theory-references/quality-gate.md`（占位）

5. **创建同步Skills**
   - `framework/skills/sync/dependency-check.md`
   - `framework/skills/sync/sync-executor.md`
   - `framework/skills/sync/missing-detector.md`
   - `framework/skills/sync/notification-generator.md`

6. **更新PM Agent的AGENTS.md**
   - 添加自动化同步检查职责
   - 添加接收L1建议的工作流程

7. **提交变更**
   ```bash
   git add .
   git commit -m "feat: 添加自动化协作机制"
   ```

---

### Phase 5: 调整knowledge-assistant-dev（L3）

**当前仓库**：`/Users/sonnet/opencode/knowledge-assistant-dev`

**操作**：

1. **创建反馈目录**
   ```bash
   mkdir -p archive/feedback/template-issues
   mkdir -p archive/feedback/theory-feedback
   mkdir -p framework
   ```

2. **创建依赖文档**
   - `framework/dependencies.yaml`
   - `framework/sync-status.yaml`

3. **迁移研究内容到L1**
   - 记录需要迁移的文件清单
   - 复制到L1仓库
   - 验证迁移成功

4. **删除研究目录**
   - 删除 `docs/research/`
   - 删除 `agents/research/`

5. **更新opencode.json**
   - 移除research agent配置

6. **提交变更**
   ```bash
   git add .
   git commit -m "refactor: 回归实践项目，移除研究功能"
   ```

---

### Phase 6: 建立Submodule依赖

**操作步骤**：

1. **在agent-team-research中添加Submodule**
   ```bash
   cd /Users/sonnet/opencode/agent-team-research
   git submodule add git@github.com:Sonnet0524/SEARCH-R.git framework/methodology
   git commit -m "feat: 添加SEARCH-R作为Submodule"
   ```

2. **在AgentTeam-Template中添加Submodule**
   ```bash
   cd /Users/sonnet/opencode/AgentTeam-Template
   git submodule add git@github.com:Sonnet0524/SEARCH-R.git framework/methodology
   git commit -m "feat: 添加SEARCH-R作为Submodule"
   ```

---

### Phase 7: 迁移现有内容

**从knowledge-assistant-dev迁移到agent-team-research**：

1. **迁移研究日志**
   ```bash
   cp /Users/sonnet/opencode/knowledge-assistant-dev/docs/research/research-log.md \
      /Users/sonnet/opencode/agent-team-research/agents/research/session-log.md
   ```

2. **迁移调研文档**
   ```bash
   cp /Users/sonnet/opencode/knowledge-assistant-dev/docs/research/agent-team-design-survey.md \
      /Users/sonnet/opencode/agent-team-research/theory/agent-team-survey.md
   ```

3. **迁移CATCH_UP.md**
   ```bash
   cp /Users/sonnet/opencode/knowledge-assistant-dev/agents/research/CATCH_UP.md \
      /Users/sonnet/opencode/agent-team-research/agents/research/CATCH_UP.md
   ```

4. **验证迁移**
   - 检查文件完整性
   - 检查路径引用

---

### Phase 8: 创建GitHub远程仓库

**操作步骤**：

1. **在GitHub创建agent-team-research仓库**
   ```bash
   cd /Users/sonnet/opencode/agent-team-research
   git remote add origin git@github.com:Sonnet0524/agent-team-research.git
   git push -u origin main
   ```

---

### Phase 9: 最终验证

**验证清单**：

- [ ] L0（SEARCH-R）调整完成
- [ ] L1（agent-team-research）创建完成
- [ ] L2（AgentTeam-Template）调整完成
- [ ] L3（knowledge-assistant-dev）调整完成
- [ ] Submodule依赖建立
- [ ] 依赖文档创建
- [ ] 同步Skills创建
- [ ] 内容迁移完成
- [ ] Git历史清晰
- [ ] 无遗留问题

---

### Phase 10: 生成报告

**输出文档**：

1. **migration-report.md** - 完成报告
2. **migration-log.md** - 操作日志
3. **rollback-guide.md** - 回滚指南

---

## 📝 模板文件

### 1. dependencies.yaml模板

```yaml
# 依赖配置

methodology:
  repo: SEARCH-R
  version: v1.0.0
  type: submodule
  path: framework/methodology/
  check_frequency: daily
  last_check: null
  last_sync: null
  
template:
  repo: AgentTeam-Template
  version: v1.0.0
  type: reference
  check_frequency: weekly
  last_check: null
```

### 2. sync-status.yaml模板

```yaml
# 同步状态

methodology_sync:
  status: not_checked
  current_version: null
  latest_version: null
  last_check: null
  action: check_needed
  
template_sync:
  status: not_checked
  current_version: null
  latest_version: null
  last_check: null
  action: check_needed
```

### 3. Research Agent AGENTS.md模板（L1）

见后续详细内容...

---

## ⚠️ 风险和应对

### 风险1：Git状态不干净
- **应对**：提示用户先提交或暂存变更
- **回滚**：可以放弃未提交的变更

### 风险2：Submodule添加失败
- **应对**：检查Git版本，确保SSH密钥配置
- **回滚**：删除.gitmodules和Submodule目录

### 风险3：内容迁移丢失
- **应对**：先复制后删除，验证后再删源文件
- **回滚**：从Git历史恢复

### 风险4：临时目录未清理
- **应对**：使用trap确保清理
- **回滚**：手动清理/tmp目录

---

## 🎓 最佳实践

### DO ✅

1. ✅ 每步操作前检查Git状态
2. ✅ 使用临时副本修改其他仓库
3. ✅ 记录每一步到日志
4. ✅ 关键操作等待用户确认
5. ✅ 完成后清理临时文件

### DON'T ❌

1. ❌ 不跳过任何验证步骤
2. ❌ 不在Git状态不干净时操作
3. ❌ 不直接修改其他仓库（不使用临时副本）
4. ❌ 不忽略任何错误
5. ❌ 不删除文件前不备份

---

## 📊 进度追踪

使用checklist追踪进度：

- [ ] Phase 1: 准备阶段
- [ ] Phase 2: 创建L1仓库
- [ ] Phase 3: 调整SEARCH-R
- [ ] Phase 4: 调整AgentTeam-Template
- [ ] Phase 5: 调整knowledge-assistant-dev
- [ ] Phase 6: 建立Submodule依赖
- [ ] Phase 7: 迁移现有内容
- [ ] Phase 8: 创建GitHub远程仓库
- [ ] Phase 9: 最终验证
- [ ] Phase 10: 生成报告

---

## 🚀 启动方式

```bash
# 在knowledge-assistant-dev目录
./start-migration.sh

# 或使用opencode
opencode run --agent migration "开始执行多仓库架构调整任务"
```

---

**创建时间**: 2026-03-08  
**任务类型**: 一次性迁移任务  
**预计时间**: 1-2小时
