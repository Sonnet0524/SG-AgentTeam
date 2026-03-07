# Git Workflow Skill

**适用对象**：所有Agent  
**类型**：workflow  
**优先级**：P0

---

## 工作流程

### 启动时同步

**必执行**：
```bash
git pull origin main
```

**位置**：在读取CATCH_UP.md之前执行

---

### 开发中提交

#### 提交前检查
```bash
# 运行测试
pytest tests/

# 检查覆盖率
pytest --cov=scripts tests/
```

#### 提交格式
```bash
git add <files>
git commit -m "<type>(<scope>): <message>"
git push origin <branch>
```

**提交类型**：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `refactor`: 重构
- `test`: 测试相关

**示例**：
```
feat(ai): add semantic search function
fix(core): fix keyword extraction bug
docs(pm): update AGENTS.md
```

---

### 分支管理

#### 主分支
- `main`: 稳定版本
- `develop`: 开发版本

#### 功能分支
- `feature/<task-id>`: 功能开发
- `bugfix/<issue-id>`: Bug修复

---

## 禁止操作

### ❌ 严格禁止
- `git push --force`
- 直接提交到 `main` 分支
- 提交未测试的代码
- 提交包含敏感信息的文件

---

## 冲突处理

### 发现冲突时
1. 停止当前操作
2. 通知PM Agent
3. 等待协调解决

---

## 验收标准

- [ ] 提交前运行测试
- [ ] 提交信息符合格式
- [ ] 无禁止操作
- [ ] 冲突及时报告
