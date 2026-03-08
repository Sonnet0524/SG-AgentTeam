# Integration Team任务：v1.2 Web UI Backend API

## 📋 任务背景

v1.2 需要创建 Web UI，首先需要 FastAPI 后端 API。

## 🎯 具体任务 - TASK-INT1: Web UI Backend API

**Issue**: #43
**优先级**: P1
**预计时间**: 4天

## 任务要求

### 1. FastAPI 应用框架
- 创建 `scripts/api/main.py`
- 配置 FastAPI 应用
- CORS 支持
- 错误处理中间件

### 2. 搜索 API
- 创建 `scripts/api/routes/search.py`
- 端点: `GET /api/search?q=query&limit=10`
- 支持分页
- 返回 JSON 格式结果

### 3. 文档管理 API
- 创建 `scripts/api/routes/documents.py`
- 端点:
  - `GET /api/documents` - 列出文档
  - `POST /api/documents` - 添加文档
  - `DELETE /api/documents/{id}` - 删除文档

### 4. 连接器状态 API
- 创建 `scripts/api/routes/connectors.py`
- 端点: `GET /api/connectors/status`
- 返回各连接器状态

### 5. OpenAPI 文档
- 自动生成 API 文档
- 添加示例和说明

### 6. Pydantic 模型
- 创建 `scripts/api/models/schemas.py`
- 定义请求/响应模型

## 📁 文件结构

```
scripts/api/
├── __init__.py
├── main.py              # FastAPI 应用
├── routes/
│   ├── __init__.py
│   ├── search.py        # 搜索端点
│   ├── documents.py     # 文档管理
│   └── connectors.py    # 连接器状态
└── models/
    ├── __init__.py
    └── schemas.py       # Pydantic 模型
```

## 📋 API 规范

### 搜索 API
```
GET /api/search?q=query&limit=10&offset=0

Response:
{
  "results": [...],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

### 文档 API
```
GET /api/documents
POST /api/documents
DELETE /api/documents/{id}
```

### 连接器状态
```
GET /api/connectors/status

Response:
{
  "connectors": [
    {"name": "email", "status": "connected"},
    {"name": "calendar", "status": "disconnected"}
  ]
}
```

## ⚠️ 注意事项

1. 使用异步处理
2. 添加请求验证
3. 实现错误处理
4. 添加日志记录

## 📤 输出要求

完成后在 `reports/integration-report-v1.2.md` 写入报告，包含：
1. API 端点列表
2. OpenAPI 文档链接
3. 测试结果
4. 遇到的问题

---
**创建者**: PM Team
**创建时间**: 2026-03-08
**Sprint**: v1.2 Sprint 3（可提前开始）
