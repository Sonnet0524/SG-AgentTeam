# Review Process Skill

**适用对象**：PM Agent（执行Review）、Team Agent（响应Review）  
**类型**：workflow  
**优先级**：P0

---

## PM Agent Review流程

### 触发条件
- Team Agent提交PR
- Team Agent请求Review

### Review步骤

#### Step 1: 检查PR描述
- [ ] 任务描述清晰
- [ ] 关联Issue正确
- [ ] 验收标准明确

#### Step 2: 检查代码质量
- [ ] 代码符合模块边界
- [ ] 无越界修改
- [ ] 测试覆盖率 > 80%
- [ ] 无明显Bug

#### Step 3: 检查文档
- [ ] API文档完整
- [ ] 必要的注释存在
- [ ] README更新（如需要）

#### Step 4: 运行测试
```bash
# 运行所有测试
pytest tests/

# 检查覆盖率
pytest --cov=scripts tests/
```

#### Step 5: 决策

**决策选项**：
- ✅ **Approve**: 通过，合并PR
- ⚠️ **Request Changes**: 需要修改，列出问题
- 💬 **Comment**: 仅评论，不需修改

---

## Team Agent响应流程

### Review反馈处理

#### 收到Approve
- [ ] 确认合并
- [ ] 关联Issue已关闭
- [ ] 更新agent-status.md

#### 收到Request Changes
1. **阅读反馈**
   - 理解问题
   - 记录修改点

2. **修改代码**
   - 修复问题
   - 重新测试

3. **更新PR**
   ```bash
   git add <modified-files>
   git commit -m "fix: address review feedback"
   git push origin <branch>
   ```

4. **请求重新Review**
   - 在PR中评论：`@pm-agent please review again`

---

## Review标准

### 代码质量标准

| 维度 | 标准 | 检查方法 |
|------|------|---------|
| 功能正确 | 所有测试通过 | `pytest tests/` |
| 覆盖率 | > 80% | `pytest --cov` |
| 模块边界 | 无越界修改 | 手动检查 |
| 代码风格 | 符合PEP8 | `flake8`（可选）|

### 文档标准

| 维度 | 标准 |
|------|------|
| API文档 | 函数签名 + 参数说明 + 返回值 |
| 注释 | 复杂逻辑有注释 |
| README | 新功能有说明 |

---

## 禁止操作

### ❌ PM Agent禁止
- 跳过测试直接合并
- 合并未完成Review的PR
- 忽略Review反馈

### ❌ Team Agent禁止
- 忽略Review反馈
- 强制合并PR
- 删除Review评论

---

## 验收标准

### PM Agent
- [ ] Review流程完整
- [ ] 决策有依据
- [ ] 反馈清晰具体

### Team Agent
- [ ] 及时响应Review
- [ ] 修改符合要求
- [ ] 重新测试通过
