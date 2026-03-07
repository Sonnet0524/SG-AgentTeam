#!/bin/bash
# ====================================
# Agent 结果收集器
# ====================================

AGENT_NAME=$1

if [ -z "$AGENT_NAME" ]; then
    echo "用法: $0 <agent-name>"
    echo "示例: $0 integration"
    exit 1
fi

LOG_FILE="logs/${AGENT_NAME}.log"
PID_FILE=".agent-pids/${AGENT_NAME}.pid"
RESULT_FILE=".agent-results/${AGENT_NAME}.json"

echo "=== 收集 Agent 结果: $AGENT_NAME ==="
echo ""

# 检查进程是否还在运行
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if ps -p "$pid" > /dev/null 2>&1; then
        echo "⚠️  Agent 还在运行中 (PID: $pid)"
        echo "结果可能不完整"
        echo ""
    fi
fi

# 检查日志文件
if [ ! -f "$LOG_FILE" ]; then
    echo "❌ 日志文件不存在: $LOG_FILE"
    exit 1
fi

echo "日志文件: $LOG_FILE"
echo "日志大小: $(wc -l < "$LOG_FILE") 行"
echo ""

# 提取结果
echo "正在解析 JSON 日志..."

# 提取所有 result 类型的事件
grep '"type":"result"' "$LOG_FILE" > /tmp/agent_results.json 2>/dev/null

if [ -s /tmp/agent_results.json ]; then
    # 合并所有结果
    echo "[" > "$RESULT_FILE"
    cat /tmp/agent_results.json | sed 's/^/  /' | sed '$ s/$/\n/' >> "$RESULT_FILE"
    echo "]" >> "$RESULT_FILE"
    
    echo "✅ 结果已保存到: $RESULT_FILE"
    echo ""
    
    # 显示结果摘要
    echo "结果摘要:"
    jq -r '.[] | "- \(.content // .message // "无内容")"' "$RESULT_FILE" 2>/dev/null || cat "$RESULT_FILE"
else
    echo "⚠️  没有找到 result 类型的日志"
    echo ""
    echo "最后 10 行日志:"
    tail -10 "$LOG_FILE"
fi

# 更新状态
STATUS_FILE=".agent-status/${AGENT_NAME}.json"
if [ -f "$STATUS_FILE" ]; then
    jq '. + {"status": "completed", "completed_at": "'$(date -Iseconds)'"}' \
        "$STATUS_FILE" > /tmp/agent_status.json
    mv /tmp/agent_status.json "$STATUS_FILE"
    echo ""
    echo "✅ 状态已更新: $STATUS_FILE"
fi

# 清理临时文件
rm -f /tmp/agent_results.json
