# Knowledge Assistant - 实践部分

> 🛠️ 本项目的Agent Team设计与实现

**项目**: Knowledge Assistant  
**框架**: [Agent Team Framework](../docs/)  
**状态**: 开发中

---

## 📋 项目概述

**项目目标**: 个人知识管理助手  
**开发模式**: AI Agent Team协作开发  
**验证重点**: Agent Team Framework的可行性

---

## 👥 团队配置

| Agent | 职责 | 模块边界 |
|-------|------|---------|
| **PM** | 项目管理、协调、进度跟踪 | management/ |
| **Data** | 数据模型、解析器、存储层 | 数据模块 |
| **Template** | 模板引擎、配置系统 | 模板模块 |
| **Test** | 测试框架、质量保证 | 测试模块 |
| **Research** | 框架研究、方法论提炼 | 研究文档 |

---

## 📁 目录结构

```
practice/
├── agents/             # 🤖 Agent配置
├── management/         # 📊 项目管理
├── knowledge-base/     # 🧠 知识库
├── reports/            # 📝 报告
├── logs/               # 📋 日志
│   ├── archives/       # 归档日志
│   └── work-logs/      # 工作日志
├── status/             # 📈 状态文档
├── meeting-notes/      # 📅 会议记录
├── decisions/          # 🎯 决策记录
├── examples/           # 📚 示例
├── templates/          # 📄 模板文件
└── development-guide/  # 🔧 开发指南
```

---

## 🚀 快速开始

### 启动Agent

```bash
# 启动 PM Agent
./start-pm.sh   # Linux/Mac
start-pm.bat    # Windows

# 其他Agent类似
./start-data.sh
./start-template.sh
./start-test.sh
./start-research.sh
```

### Agent入口

每个Agent通过 `agents/<name>/CATCH_UP.md` 快速恢复上下文。

---

## 📊 当前状态

详见: [状态总览](status/human-admin.md)

---

## 📚 相关文档

- [框架文档](../docs/) - Agent Team Framework理论
- [开发指南](development-guide/) - 开发规范
- [知识库](knowledge-base/) - 项目经验
