#!/bin/bash
# ====================================
# Agent 启动器
# ====================================

AGENT_NAME=$1
TASK_MESSAGE=$2

if [ -z "$AGENT_NAME" ] || [ -z "$TASK_MESSAGE" ]; then
    echo "用法: $0 <agent-name> <task-message>"
    echo "示例: $0 integration '完成 Issue #12 创建 SKILL.md'"
    exit 1
fi

# 检查 Agent 是否已经在运行
PID_FILE=".agent-pids/${AGENT_NAME}.pid"
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  Agent '$AGENT_NAME' 已在运行 (PID: $OLD_PID)"
        echo "请先停止现有进程或等待其完成"
        exit 1
    else
        echo "清理旧的 PID 文件..."
        rm -f "$PID_FILE"
    fi
fi

echo "=== 启动 Agent: $AGENT_NAME ==="
echo "任务: $TASK_MESSAGE"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 记录任务
cat > ".agent-tasks/${AGENT_NAME}.json" <<EOF
{
  "agent": "$AGENT_NAME",
  "task": "$TASK_MESSAGE",
  "started_at": "$(date -Iseconds)",
  "status": "running"
}
EOF

# 更新状态
cat > ".agent-status/${AGENT_NAME}.json" <<EOF
{
  "agent": "$AGENT_NAME",
  "status": "running",
  "started_at": "$(date -Iseconds)",
  "pid": "pending"
}
EOF

# 启动 Agent（后台进程，JSON 格式输出）
nohup opencode run \
  --agent "$AGENT_NAME" \
  --message "$TASK_MESSAGE" \
  --format json \
  > "logs/${AGENT_NAME}.log" 2>&1 &

AGENT_PID=$!

# 记录 PID
echo $AGENT_PID > "$PID_FILE"

# 更新状态文件
cat > ".agent-status/${AGENT_NAME}.json" <<EOF
{
  "agent": "$AGENT_NAME",
  "status": "running",
  "started_at": "$(date -Iseconds)",
  "pid": $AGENT_PID,
  "task": "$TASK_MESSAGE"
}
EOF

echo "✅ Agent 已启动"
echo "   名称: $AGENT_NAME"
echo "   PID: $AGENT_PID"
echo "   日志: logs/${AGENT_NAME}.log"
echo ""
echo "使用以下命令检查进度："
echo "  ./scripts/agents/check-progress.sh $AGENT_NAME"
