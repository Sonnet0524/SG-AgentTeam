# 代码推送规则

## 概述

本文档定义了从开发环境向主仓库推送代码的规则和要求。**这是所有 Agent 必须严格遵守的核心规范。**

---

## ⚠️ 重要提示

**推送代码前必须检查**：
1. 你正在主仓库（knowledge-assistant）工作，而不是开发仓库
2. 你在正确的分支
3. 你有权限推送该内容
4. 所有测试通过

---

## 推送权限

### PM Agent

**权限**：
- ✅ 可以推送到 main 分支（合并 PR 时）
- ✅ 可以推送任何分支
- ✅ 可以强制推送（仅限紧急情况）

**限制**：
- ❌ 不直接推送功能代码（应该由成员 Agent 提交 PR）
- ❌ 不跳过 Review 流程

### 成员 A/B Agent

**权限**：
- ✅ 可以推送到自己的功能分支（feature/a-* 或 feature/b-*）
- ✅ 可以创建 PR
- ✅ 可以推送到测试分支

**限制**：
- ❌ **绝对不能**直接推送到 main 分支
- ❌ 不能推送到其他 Agent 的功能分支
- ❌ 不能合并 PR（需要 PM Review）

### 成员 Test Agent

**权限**：
- ✅ 可以推送到测试分支（test/*）
- ✅ 可以推送测试报告到 docs/

**限制**：
- ❌ 不能推送功能代码
- ❌ 不能推送到 main 分支

---

## 推送前检查清单

### ⚠️ 必须检查项（缺一不可）

在推送代码前，Agent **必须**确认：

#### 1. 仓库检查
- [ ] 你在主仓库（knowledge-assistant），不是开发仓库
- [ ] 你在正确的分支（使用 `git branch` 确认）

#### 2. 代码质量
- [ ] 代码符合 PEP 8 规范
- [ ] 有完整的类型注解
- [ ] 有详细的文档字符串
- [ ] 无明显的 bug

#### 3. 测试验证
- [ ] 所有单元测试通过
- [ ] 测试覆盖率 > 80%
- [ ] 新功能有对应的测试
- [ ] 边界情况已测试

#### 4. 文档完整性
- [ ] 新功能有使用文档
- [ ] API 有文档说明
- [ ] README 已更新（如需要）

#### 5. Git 规范
- [ ] 分支命名正确
- [ ] 提交信息符合规范
- [ ] 无冲突文件
- [ ] 已拉取最新主分支

---

## 推送流程

### 标准推送流程

```bash
# 1. 确认在主仓库
pwd
# 应该显示：<main-repo>路径（根据实际环境）

# 2. 确认在正确的分支
git branch
# 应该显示：* feature/a-template-engine

# 3. 拉取最新主分支
git checkout main
git pull origin main

# 4. 切回功能分支并同步
git checkout feature/a-template-engine
git rebase main

# 5. 运行测试
pytest tests/ -v --cov=scripts

# 6. 检查覆盖率
pytest tests/ --cov=scripts --cov-report=term-missing
# 确认覆盖率 > 80%

# 7. 推送到远程
git push origin feature/a-template-engine

# 8. 在 GitHub 创建 Pull Request
# 目标分支：main
# 源分支：feature/a-template-engine
```

---

## 分支推送规则

| 分支类型 | 命名格式 | 推送权限 | Review 要求 | 合并权限 |
|---------|---------|---------|------------|---------|
| `main` | main | 仅 PM | N/A | PM |
| `feature/*` | feature/a-* 或 feature/b-* | 对应 Agent | PM Review | PM |
| `fix/*` | fix/a-* 或 fix/b-* | 对应 Agent | PM Review | PM |
| `test/*` | test/test-* | Test Agent | PM Review | PM |
| `docs/*` | docs/pm-* 或 docs/test-* | PM, Test | 可选 | PM |

---

## 文件推送规则

| 文件类型 | 路径 | 推送权限 | Review 要求 |
|---------|------|---------|------------|
| Python 代码 | `scripts/*.py` | 对应模块 Agent | PM Review |
| 模板文件 | `templates/*.md` | 成员 A | PM Review |
| 测试代码 | `tests/*.py` | 所有 Agent | PM Review |
| 用户文档 | `docs/*.md` | PM, Test | 可选 |
| OpenCode 配置 | `AGENTS.md` | 仅 PM | N/A |
| 项目说明 | `README.md` | 仅 PM | N/A |

---

## 推送限制

### 禁止推送的内容

- ❌ 敏感信息（密码、API Key 等）
- ❌ 未测试的代码
- ❌ 其他 Agent 的模块代码
- ❌ 不符合规范的代码
- ❌ 编译产物（如 `__pycache__/`）
- ❌ IDE 配置（如 `.vscode/`）

### 检查方法

```bash
# 检查是否有敏感信息
git diff --cached | grep -E "(password|secret|api_key|token)"
# 如果有输出，必须移除

# 检查是否有不应该提交的文件
git diff --cached --name-only | grep -E "(__pycache__|\.pyc|\.env|vscode)"
# 如果有输出，必须取消暂存

# 如果发现问题，取消暂存
git reset HEAD <file>
```

---

## 强制推送规则

### ⚠️ 极度谨慎使用

仅在以下场景可以使用 `--force-with-lease`：

1. **Rebase 后**：功能分支经过 rebase，需要更新远程
2. **清理历史**：清理功能分支的提交历史
3. **修复错误提交**：修复推送后的明显错误

### 禁止强制推送的场景

- ❌ **绝对禁止**：main 分支
- ❌ 其他 Agent 的分支
- ❌ 已有 PR 且有其他人评论的分支

### 强制推送命令

```bash
# 推荐使用 --force-with-lease（更安全）
git push --force-with-lease origin feature/a-template-engine

# 禁止使用 --force（太危险）
# git push --force origin feature/a-template-engine  # ❌ 禁止
```

---

## 推送冲突处理

### 发现冲突时

```bash
# 1. 尝试推送
git push origin feature/a-template-engine

# 2. 如果提示冲突，拉取远程更新
git pull origin feature/a-template-engine

# 3. 解决冲突
# 手动编辑冲突文件

# 4. 标记为已解决
git add <conflicted-file>

# 5. 提交
git commit

# 6. 推送
git push origin feature/a-template-engine
```

### 与主分支冲突时

```bash
# 1. 同步主分支
git checkout main
git pull origin main

# 2. 切回功能分支
git checkout feature/a-template-engine

# 3. 合并或 rebase
git rebase main

# 4. 解决冲突
# ...

# 5. 推送
git push origin feature/a-template-engine
# 如果是 rebase，可能需要
git push --force-with-lease origin feature/a-template-engine
```

---

## 推送频率

### 推荐频率

- **开发过程中**：每天至少推送 1-2 次
- **功能完成后**：立即推送并创建 PR
- **重要节点**：完成关键功能后立即推送

### 不推荐的频率

- ❌ 一次推送大量代码（> 1000 行）
- ❌ 一天不推送（可能导致大量冲突）
- ❌ 推送未完成的代码（除非明确标注 WIP）

---

## 推送后验证

### 本地验证

```bash
# 在本地再次拉取
git checkout main
git pull origin main

# 切换到功能分支测试
git checkout feature/a-template-engine
pytest tests/ -v
```

### GitHub 验证

推送后检查：
- [ ] GitHub 上可以看到提交
- [ ] CI 测试通过（绿色勾）
- [ ] PR 创建成功（如有）
- [ ] 文件内容正确

---

## 常见错误和解决

### 错误 1：推送到错误的分支

```bash
# 错误：推送到 main
git push origin main  # ❌ 成员 Agent 不应该这样做

# 解决：立即通知 PM
# PM 可以使用 git reset 回退
```

### 错误 2：推送了敏感信息

```bash
# 错误：推送了包含密码的文件

# 解决：
# 1. 立即修改密码
# 2. 使用 git filter-branch 或 BFG Repo-Cleaner 清除历史
# 3. 强制推送（仅此特殊情况允许）
# 4. 通知 PM
```

### 错误 3：推送了未测试的代码

```bash
# 错误：推送后 CI 失败

# 解决：
# 1. 立即修复问题
# 2. 提交新的修复
# 3. 或关闭 PR，修复后重新提交
```

---

## 检查清单（最终版）

### 推送前必须确认

- [ ] 在主仓库（knowledge-assistant）
- [ ] 在正确的分支
- [ ] 所有测试通过
- [ ] 覆盖率 > 80%
- [ ] 提交信息规范
- [ ] 无敏感信息
- [ ] 无不该提交的文件

### 推送后必须验证

- [ ] GitHub 上可看到提交
- [ ] CI 测试通过
- [ ] 文件内容正确
- [ ] 已通知 PM（创建 PR）

---

**版本**: v1.0  
**更新日期**: 2026-03-05  
**维护者**: PM Agent
