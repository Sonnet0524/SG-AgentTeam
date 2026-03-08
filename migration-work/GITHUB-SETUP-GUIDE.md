# GitHub远程仓库创建指南

**文档版本**: 1.0
**创建时间**: 2026-03-08
**目的**: 指导如何将本地仓库推送到GitHub

---

## 📋 准备工作

### 1. 需要的信息

在开始之前，请确认：

- [ ] GitHub账号已登录
- [ ] 确定GitHub组织或个人账号名称
- [ ] 确定仓库的可见性（public/private）
- [ ] GitHub CLI (`gh`)已安装并认证，或准备使用Web界面

### 2. 仓库清单

需要创建/更新的仓库：

| 层级 | 仓库名 | 本地路径 | 状态 |
|------|--------|----------|------|
| L0 | SEARCH-R | /Users/sonnet/opencode/SEARCH-R | 已有远程？ |
| L1 | agent-team-research | /Users/sonnet/opencode/agent-team-research | 需创建 |
| L2 | AgentTeam-Template | /Users/sonnet/opencode/AgentTeam-Template | 已有远程？ |
| L3 | knowledge-assistant-dev | /Users/sonnet/opencode/knowledge-assistant-dev | 已有远程？ |

---

## 🚀 方法1: 使用GitHub CLI（推荐）

### 步骤1: 创建L1仓库

```bash
# 进入L1目录
cd /Users/sonnet/opencode/agent-team-research

# 创建GitHub仓库
gh repo create agent-team-research \
  --public \
  --description "L1 Research Support Layer - Provides research capabilities for multi-repository architecture" \
  --source=. \
  --push

# 或者创建私有仓库
gh repo create agent-team-research \
  --private \
  --description "L1 Research Support Layer - Provides research capabilities for multi-repository architecture" \
  --source=. \
  --push
```

### 步骤2: 更新其他仓库的远程地址

如果L0、L2、L3已有远程仓库，推送变更：

```bash
# L0
cd /Users/sonnet/opencode/SEARCH-R
git push origin main

# L2
cd /Users/sonnet/opencode/AgentTeam-Template
git push origin main

# L3
cd /Users/sonnet/opencode/knowledge-assistant-dev
git push origin main
```

### 步骤3: 更新符号链接为Submodule（可选）

推送完成后，可以将符号链接替换为Git Submodule：

```bash
# 在L1
cd /Users/sonnet/opencode/agent-team-research
rm .agent-team/search-r
git submodule add https://github.com/{org}/SEARCH-R.git .agent-team/search-r
git commit -m "Replace symbolic link with Git submodule for L0"

# 在L2
cd /Users/sonnet/opencode/AgentTeam-Template
rm .agent-team/search-r .agent-team/research
git submodule add https://github.com/{org}/SEARCH-R.git .agent-team/search-r
git submodule add https://github.com/{org}/agent-team-research.git .agent-team/research
git commit -m "Replace symbolic links with Git submodules for L0 and L1"

# 在L3
cd /Users/sonnet/opencode/knowledge-assistant-dev
rm .agent-team/template
git submodule add https://github.com/{org}/AgentTeam-Template.git .agent-team/template
git commit -m "Replace symbolic link with Git submodule for L2"
```

---

## 🌐 方法2: 使用GitHub Web界面

### 步骤1: 在GitHub创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `agent-team-research`
   - Description: `L1 Research Support Layer`
   - 选择Public或Private
   - 不要勾选 "Initialize this repository with a README"（已有本地仓库）
3. 点击 "Create repository"

### 步骤2: 推送本地仓库

GitHub会显示推送指令，按照执行：

```bash
cd /Users/sonnet/opencode/agent-team-research
git remote add origin https://github.com/{your-username}/agent-team-research.git
git branch -M main
git push -u origin main
```

### 步骤3: 推送其他仓库

重复上述步骤推送L0、L2、L3的更新。

---

## 📝 仓库描述建议

### L0: SEARCH-R
```
L0 Research Data Source Layer - Provides SEARCH-R methodology and research instance storage for multi-repository AI Agent architecture
```

### L1: agent-team-research
```
L1 Research Support Layer - Provides Research Agent, skills, and templates for multi-repository AI Agent architecture
```

### L2: AgentTeam-Template
```
L2 Project Template Layer - Provides PM Agent and team templates for AI Agent project management
```

### L3: knowledge-assistant-dev
```
L3 Application Project - Knowledge Assistant development with AI Agent team collaboration
```

---

## 🔧 配置建议

### 1. 仓库设置

在GitHub仓库设置中：

**Branch Protection** (可选):
- 保护main分支
- 要求PR审核
- 要求状态检查通过

**Topics/Tags**:
- `ai-agent`
- `multi-repository-architecture`
- `research-agent`
- `project-management`

### 2. README徽章

可以在README.md中添加徽章：

```markdown
[![Architecture](https://img.shields.io/badge/Architecture-L1-blue)]()
[![Status](https://img.shields.io/badge/Status-Active-green)]()
```

---

## ⚠️ 注意事项

### 1. 符号链接问题

如果先推送再替换为Submodule：
- 推送时符号链接不会包含在仓库中
- 克隆仓库后需要手动创建链接或使用Submodule

### 2. 大文件

如果有大文件：
- 考虑使用Git LFS
- 或在.gitignore中排除

### 3. 敏感信息

推送前检查：
- .env文件
- credentials
- API keys
- 确保这些在.gitignore中

### 4. 分支管理

建议：
- main分支用于稳定版本
- 开发使用feature分支
- 使用Pull Request合并

---

## 📊 推送后的工作流程

### 克隆仓库（带Submodule）

```bash
# 克隆主仓库和所有Submodule
git clone --recursive https://github.com/{org}/agent-team-research.git

# 或分步克隆
git clone https://github.com/{org}/agent-team-research.git
cd agent-team-research
git submodule update --init --recursive
```

### 更新Submodule

```bash
# 更新所有Submodule到最新版本
git submodule update --remote

# 或更新特定Submodule
git submodule update --remote .agent-team/search-r
```

---

## 🎯 执行清单

### Phase 8执行步骤

- [ ] **准备阶段**
  - [ ] 确认GitHub账号信息
  - [ ] 决定仓库可见性
  - [ ] 准备仓库描述

- [ ] **创建L1仓库**
  - [ ] 在GitHub创建agent-team-research仓库
  - [ ] 推送L1代码
  - [ ] 验证推送成功

- [ ] **推送其他仓库**
  - [ ] 推送L0 (SEARCH-R)更新
  - [ ] 推送L2 (AgentTeam-Template)更新
  - [ ] 推送L3 (knowledge-assistant-dev)更新

- [ ] **验证和测试**
  - [ ] 在GitHub验证所有仓库
  - [ ] 测试克隆流程
  - [ ] 验证README显示正确

- [ ] **可选: Submodule迁移**
  - [ ] 在L1替换链接为Submodule
  - [ ] 在L2替换链接为Submodule
  - [ ] 在L3替换链接为Submodule
  - [ ] 测试Submodule工作流

---

## 🔗 相关资源

### GitHub CLI文档
- https://cli.github.com/manual/

### Git Submodule文档
- https://git-scm.com/book/en/v2/Git-Tools-Submodules

### 多仓库管理最佳实践
- https://docs.github.com/en/repositories

---

## 💡 快速命令参考

```bash
# 检查当前远程仓库
git remote -v

# 添加远程仓库
git remote add origin {url}

# 推送到远程
git push -u origin main

# 创建GitHub仓库并推送（一条命令）
gh repo create {name} --public --source=. --push

# 添加Submodule
git submodule add {url} {path}

# 更新Submodule
git submodule update --init --recursive
```

---

**文档维护**: Migration Agent
**创建时间**: 2026-03-08
**版本**: 1.0
