# OpenCode Agent 使用指南

> 本项目已配置4个专门的agent，可以通过OpenCode启动使用

---

## 📋 已配置的Agent列表

| Agent | 描述 | 工作目录 | 启动命令 |
|-------|------|----------|----------|
| **pm** | 项目管理和协调 | knowledge-assistant-dev | `opencode --agent pm` |
| **member-a** | 模板和配置模块开发 | knowledge-assistant | `opencode --agent member-a` |
| **member-b** | 元数据和工具模块开发 | knowledge-assistant | `opencode --agent member-b` |
| **test** | 测试和质量保证 | knowledge-assistant | `opencode --agent test` |

---

## 🚀 快速开始

### 1. 启动PM Agent（在dev仓库）

```bash
# 确保在dev仓库根目录
cd D:\opencode\knowledge-assistant-dev

# 启动PM Agent
opencode --agent pm

# PM Agent会自动：
# 1. 读取 agents/pm/CATCH_UP.md
# 2. 读取 agent-status.md
# 3. 读取 HUMAN_ADMIN.md
# 4. 同步两个仓库
```

### 2. 启动Agent A（在主仓库）

```bash
# 切换到主仓库
cd ../knowledge-assistant

# 启动Agent A
opencode --agent member-a

# Agent A会自动：
# 1. 读取 agents/member-a/CATCH_UP.md
# 2. 读取 agent-status.md
# 3. 同步主仓库代码
```

### 3. 启动Agent B（在主仓库）

```bash
# 在主仓库目录
cd D:\opencode\knowledge-assistant

# 启动Agent B
opencode --agent member-b
```

### 4. 启动Agent Test（在主仓库）

```bash
# 在主仓库目录
cd D:\opencode\knowledge-assistant

# 启动Agent Test
opencode --agent test
```

---

## 💡 使用建议

### 在TUI中切换Agent

启动OpenCode后，可以使用 **Tab键** 在不同的primary agent之间切换：

```
启动 opencode
  ↓
按 Tab 键切换 agent
  ↓
build → pm → member-a → member-b → test → build
```

### 使用@提及调用Agent

在任何agent会话中，可以使用 `@` 提及来调用其他agent：

```
@member-a 请帮我创建一个新的文档模板
@test 请检查这个模块的测试覆盖率
@member-b 帮我解析这个元数据文件
```

---

## 📝 Agent配置说明

### 配置文件位置

- **主配置**: `opencode.json` - 定义所有agent及其权限
- **Agent定义**: `agents/*/AGENTS.md` - 每个agent的详细配置
- **状态文档**: `agents/*/CATCH_UP.md` - agent启动时读取的状态

### Agent权限配置

每个agent都有不同的权限设置：

| Agent | 文件编辑 | Bash命令 | 特殊权限 |
|-------|---------|---------|---------|
| **pm** | 需确认 | git push需确认 | 全部git命令 |
| **member-a** | 需确认 | git push需确认 | pytest, black, flake8, mypy |
| **member-b** | 需确认 | git push需确认 | pytest, black, flake8, mypy |
| **test** | 禁止 | 仅允许测试相关 | pytest, git diff/log |

---

## 🔄 工作流程

### 典型的开发流程

```
1. PM Agent (在dev仓库)
   - 创建Issue
   - 分配任务给相应Agent
   - 更新agent-status.md
   ↓
2. Agent A/B/Test (在主仓库)
   - 认领Issue
   - 创建分支
   - 开发代码
   - 提交PR
   ↓
3. PM Agent (在dev仓库)
   - Review PR
   - 合并代码
   - 更新状态
```

---

## 🛠️ 故障排除

### Agent无法启动

```bash
# 检查配置文件是否存在
ls opencode.json
ls agents/*/AGENTS.md

# 检查OpenCode版本
opencode --version

# 查看可用agent列表
opencode agent list
```

### 权限问题

如果agent缺少某个工具权限，可以编辑 `opencode.json`：

```json
{
  "agent": {
    "member-a": {
      "permission": {
        "edit": "allow",  // 改为allow
        "bash": "allow"   // 改为allow
      }
    }
  }
}
```

### 读取CATCH_UP失败

确保agent启动时：
1. 工作目录正确（PM在dev仓库，其他在主仓库）
2. CATCH_UP.md文件存在
3. 文件路径正确

---

## 📚 相关文档

- [Agent详细配置](./agents/)
- [项目工作流程](./development-guide/workflow.md)
- [Git工作流](./development-guide/git-workflow.md)
- [Agent状态管理](./agent-status.md)

---

## 🎯 最佳实践

### 1. 每次启动Agent时

- ✅ 确认工作目录正确
- ✅ 让agent读取CATCH_UP.md
- ✅ 检查agent-status.md了解团队状态
- ✅ 确认当前任务优先级

### 2. 工作过程中

- ✅ 定期更新CATCH_UP.md
- ✅ 及时更新agent-status.md
- ✅ 遇到阻塞立即报告
- ✅ 完成任务后更新状态

### 3. 切换Agent时

- ✅ 保存当前工作
- ✅ 更新状态文档
- ✅ 使用Tab键快速切换
- ✅ 或使用@提及临时调用

---

**版本**: v1.0  
**更新日期**: 2026-03-06  
**维护者**: PM Agent
