#!/bin/bash

# Migration Agent 启动脚本

echo "==================================="
echo "Migration Agent 启动"
echo "==================================="
echo ""
echo "任务：多仓库架构调整"
echo "当前目录：$(pwd)"
echo ""

# 检查opencode是否安装
if ! command -v opencode &> /dev/null; then
    echo "错误：opencode未安装"
    echo "请先安装opencode: pip install opencode"
    exit 1
fi

# 检查当前Git状态
echo "检查当前Git状态..."
git status

echo ""
echo "准备启动Migration Agent..."
echo ""

# 启动Migration Agent
opencode run --agent migration "请开始执行多仓库架构调整任务。阅读agents/migration/AGENTS.md了解详细任务，按照Phase 1到Phase 10的顺序执行。每完成一个Phase向我汇报进度。"
