# 多仓库架构调整 - 回滚指南

**文档版本**: 1.0  
**创建时间**: 2026-03-08  
**目的**: 提供安全的回滚方案

---

## ⚠️ 重要提示

**在执行回滚前，请确认**:
1. 已备份当前工作
2. 理解回滚的影响
3. 准备好恢复数据

**建议**: 在执行回滚前，先创建所有仓库的备份！

---

## 🔄 快速回滚（完全回滚）

### 适用场景
- 迁移出现严重问题
- 需要完全恢复到迁移前状态
- 决定暂停迁移计划

### 执行步骤

#### 步骤1: 创建临时备份
```bash
# 创建所有仓库的备份
mkdir -p /tmp/migration-backup-$(date +%Y%m%d)
cp -r /Users/sonnet/opencode/agent-team-research /tmp/migration-backup-$(date +%Y%m%d)/
cp -r /Users/sonnet/opencode/SEARCH-R /tmp/migration-backup-$(date +%Y%m%d)/SEARCH-R.current
cp -r /Users/sonnet/opencode/AgentTeam-Template /tmp/migration-backup-$(date +%Y%m%d)/AgentTeam-Template.current
cp -r /Users/sonnet/opencode/knowledge-assistant-dev /tmp/migration-backup-$(date +%Y%m%d)/knowledge-assistant-dev.current
```

#### 步骤2: 恢复L0 (SEARCH-R)
```bash
# 删除当前修改的版本
rm -rf /Users/sonnet/opencode/SEARCH-R

# 恢复备份
cp -r /Users/sonnet/opencode/SEARCH-R.backup-20260308-144810 /Users/sonnet/opencode/SEARCH-R

# 验证恢复
cd /Users/sonnet/opencode/SEARCH-R
git status  # 应该显示干净状态
```

#### 步骤3: 恢复L2 (AgentTeam-Template)
```bash
# 删除当前修改的版本
rm -rf /Users/sonnet/opencode/AgentTeam-Template

# 恢复备份
cp -r /Users/sonnet/opencode/AgentTeam-Template.backup-20260308-145014 /Users/sonnet/opencode/AgentTeam-Template

# 验证恢复
cd /Users/sonnet/opencode/AgentTeam-Template
git status  # 应该显示干净状态
```

#### 步骤4: 回滚L3 (knowledge-assistant-dev)
```bash
# 进入L3仓库
cd /Users/sonnet/opencode/knowledge-assistant-dev

# 查看提交历史
git log --oneline | head -10

# 找到迁移前的提交（应该在以下提交之前）
# - 1b72ed1 Add L3 layer positioning and multi-repo collaboration framework

# 回滚到迁移前
git reset --hard a6360af  # 替换为实际的commit hash

# 或者使用相对引用
git reset --hard HEAD~1  # 回滚最近一次提交

# 验证恢复
git status  # 应该显示干净状态
```

#### 步骤5: 删除L1仓库
```bash
# L1是新创建的，直接删除即可
rm -rf /Users/sonnet/opencode/agent-team-research

# 验证删除
ls /Users/sonnet/opencode/ | grep agent-team-research  # 应该无输出
```

#### 步骤6: 清理临时文件
```bash
# 删除migration工作目录（如果需要）
rm -rf /Users/sonnet/opencode/knowledge-assistant-dev/migration-work
rm -rf /Users/sonnet/opencode/knowledge-assistant-dev/collaboration
rm /Users/sonnet/opencode/knowledge-assistant-dev/start-migration.sh

# 删除备份（可选）
# 注意：确保不再需要这些备份
# rm -rf /Users/sonnet/opencode/SEARCH-R.backup-20260308-144810
# rm -rf /Users/sonnet/opencode/AgentTeam-Template.backup-20260308-145014
```

#### 步骤7: 验证回滚完成
```bash
# 验证所有仓库状态
echo "=== L0: SEARCH-R ==="
cd /Users/sonnet/opencode/SEARCH-R
git log --oneline | head -3

echo "=== L2: AgentTeam-Template ==="
cd /Users/sonnet/opencode/AgentTeam-Template
git log --oneline | head -3

echo "=== L3: knowledge-assistant-dev ==="
cd /Users/sonnet/opencode/knowledge-assistant-dev
git log --oneline | head -3

echo "=== L1: agent-team-research ==="
ls /Users/sonnet/opencode/agent-team-research 2>/dev/null && echo "L1 still exists!" || echo "L1 removed (expected)"
```

---

## 🔧 部分回滚方案

### 场景1: 只回滚某个特定仓库

#### 回滚L0
```bash
cd /Users/sonnet/opencode/SEARCH-R
git reset --hard HEAD~1  # 回滚到迁移前的提交
# 或
git reset --hard 5fe59ba  # 使用具体的commit hash
```

#### 回滚L2
```bash
cd /Users/sonnet/opencode/AgentTeam-Template
git reset --hard HEAD~1  # 回滚到迁移前的提交
# 或
git reset --hard cb8312a  # 使用具体的commit hash
```

#### 回滚L3
```bash
cd /Users/sonnet/opencode/knowledge-assistant-dev
git reset --hard HEAD~1  # 回滚到迁移前的提交
# 或
git reset --hard a6360af  # 使用具体的commit hash
```

### 场景2: 只撤销特定文件

#### 撤销L3的opencode.json修改
```bash
cd /Users/sonnet/opencode/knowledge-assistant-dev
git checkout HEAD~1 -- opencode.json
```

#### 删除新创建的目录
```bash
cd /Users/sonnet/opencode/knowledge-assistant-dev
rm -rf collaboration/
rm -rf migration-work/
```

### 场景3: 保留部分修改

#### 保留配置但删除文件
```bash
# 保留opencode.json的层级配置
# 但删除新创建的协作目录

cd /Users/sonnet/opencode/knowledge-assistant-dev
rm -rf collaboration/
# 手动编辑opencode.json，移除不需要的部分
```

---

## 🚨 紧急情况处理

### 情况1: Git仓库损坏

**症状**: git命令报错，仓库无法操作

**解决方案**:
```bash
# 方案1: 从备份恢复
rm -rf /Users/sonnet/opencode/{repo-name}
cp -r /Users/sonnet/opencode/{repo-name}.backup-* /Users/sonnet/opencode/{repo-name}

# 方案2: 重新克隆（如果有远程仓库）
cd /Users/sonnet/opencode
rm -rf {repo-name}
git clone {remote-url} {repo-name}
```

### 情况2: 误删重要文件

**症状**: 删除了不应该删除的文件

**解决方案**:
```bash
# 使用Git恢复已提交的文件
cd /Users/sonnet/opencode/{repo-name}
git checkout HEAD -- {file-path}

# 使用Git恢复已删除的文件
git log --all --full-history -- {file-path}  # 找到文件
git checkout {commit-hash} -- {file-path}  # 恢复文件
```

### 情况3: Submodule问题

**症状**: Submodule引用错误或丢失

**解决方案**:
```bash
# 移除Submodule
cd /Users/sonnet/opencode/{repo-name}
git submodule deinit -f {submodule-path}
rm -rf .git/modules/{submodule-path}
git rm -f {submodule-path}

# 重新添加（如果需要）
git submodule add {remote-url} {submodule-path}
```

---

## 📋 回滚检查清单

### 执行前检查

- [ ] 已备份所有当前工作
- [ ] 确认回滚范围（完全/部分）
- [ ] 准备好恢复数据的位置
- [ ] 通知团队成员（如果适用）

### 执行后检查

- [ ] 所有仓库Git状态正常
- [ ] 文件内容正确
- [ ] 配置文件恢复
- [ ] 没有残留的临时文件
- [ ] 仓库可以正常操作

### 功能验证

- [ ] 可以正常启动Agent
- [ ] 配置文件正确加载
- [ ] 日常工作流程正常
- [ ] Git操作正常（push, pull, commit等）

---

## 📝 回滚记录模板

建议记录回滚操作：

```markdown
# 回滚记录

**时间**: {date-time}
**操作人**: {name}
**原因**: {rollback reason}

## 回滚范围
- [ ] L0: SEARCH-R
- [ ] L2: AgentTeam-Template
- [ ] L3: knowledge-assistant-dev
- [ ] L1: agent-team-research

## 执行步骤
1. {step 1}
2. {step 2}
...

## 验证结果
- Git状态: ✅/❌
- 文件完整性: ✅/❌
- 功能可用性: ✅/❌

## 后续行动
- {action 1}
- {action 2}
```

---

## 💡 最佳实践

### 1. 预防性措施

**定期备份**:
```bash
# 创建定期备份脚本
cat > /Users/sonnet/opencode/backup-repos.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/Users/sonnet/opencode/backups/$DATE"
mkdir -p $BACKUP_DIR

cp -r /Users/sonnet/opencode/SEARCH-R $BACKUP_DIR/
cp -r /Users/sonnet/opencode/AgentTeam-Template $BACKUP_DIR/
cp -r /Users/sonnet/opencode/knowledge-assistant-dev $BACKUP_DIR/

echo "Backup created at $BACKUP_DIR"
EOF

chmod +x /Users/sonnet/opencode/backup-repos.sh
```

**使用分支**:
```bash
# 在执行重大修改前创建分支
cd /Users/sonnet/opencode/{repo-name}
git checkout -b pre-migration-backup
git checkout main
# 执行迁移
# 如果需要回滚
git checkout pre-migration-backup
```

### 2. 分阶段回滚

如果不确定是否需要完全回滚：

1. **先尝试部分回滚**
   - 只回滚出问题的部分
   - 观察效果

2. **保留回滚选项**
   - 不要立即删除备份
   - 记录每个步骤

3. **渐进式恢复**
   - 从最简单的开始
   - 逐步验证

### 3. 文档记录

保持详细记录：
- 所有回滚操作
- 回滚原因
- 遇到的问题
- 解决方案

---

## 🆘 获取帮助

### 日志文件

查看详细操作日志：
```bash
# Migration工作日志
cat /Users/sonnet/opencode/knowledge-assistant-dev/migration-work/MIGRATION-LOG.md

# Git日志
cd /Users/sonnet/opencode/{repo-name}
git log --oneline --graph --all
```

### 状态报告

查看当前状态：
```bash
# 查看阶段性完成报告
cat /Users/sonnet/opencode/knowledge-assistant-dev/migration-work/STATUS-REPORT.md
```

### 相关文档

- [阶段性完成报告](./STATUS-REPORT.md)
- [详细操作日志](./MIGRATION-LOG.md)
- [依赖关系说明](../collaboration/dependencies/README.md)

---

**文档维护**: Migration Agent  
**最后更新**: 2026-03-08  
**版本**: 1.0

---

## ⚡ 快速参考卡

```
┌─────────────────────────────────────────────┐
│          快速回滚命令参考                     │
├─────────────────────────────────────────────┤
│ 完全回滚:                                    │
│   1. 恢复L0: 恢复备份                        │
│   2. 恢复L2: 恢复备份                        │
│   3. 回滚L3: git reset --hard HEAD~1        │
│   4. 删除L1: rm -rf agent-team-research     │
├─────────────────────────────────────────────┤
│ 部分回滚:                                    │
│   单仓库: git reset --hard HEAD~1           │
│   单文件: git checkout HEAD~1 -- {file}     │
│   删除文件: rm -rf {dir}/                    │
├─────────────────────────────────────────────┤
│ 紧急情况:                                    │
│   仓库损坏: 从备份恢复                        │
│   误删文件: git checkout HEAD -- {file}     │
│   Submodule问题: git submodule deinit       │
└─────────────────────────────────────────────┘
```
