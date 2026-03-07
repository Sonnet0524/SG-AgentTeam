#!/bin/bash
# ====================================
# Agent 进度检查器
# ====================================

AGENT_NAME=$1

if [ -z "$AGENT_NAME" ]; then
    # 如果没有指定 Agent，检查所有 Agent
    echo "=== 检查所有 Agent 状态 ==="
    echo ""
    
    for status_file in .agent-status/*.json; do
        [ -f "$status_file" ] || continue
        agent=$(basename "$status_file" .json)
        echo "--- $agent ---"
        check_single_agent "$agent"
        echo ""
    done
    exit 0
fi

check_single_agent() {
    local agent=$1
    local pid_file=".agent-pids/${agent}.pid"
    local status_file=".agent-status/${agent}.json"
    local log_file="logs/${agent}.log"
    
    # 检查 PID 文件
    if [ ! -f "$pid_file" ]; then
        echo "❌ Agent '$agent' 未启动"
        return 1
    fi
    
    local pid=$(cat "$pid_file")
    
    # 检查进程状态
    if ps -p "$pid" > /dev/null 2>&1; then
        echo "状态: 🟢 运行中"
        echo "PID: $pid"
    else
        echo "状态: 🔴 已结束"
        echo "PID: $pid (进程已退出)"
    fi
    
    # 读取任务信息
    if [ -f "$status_file" ]; then
        echo "启动时间: $(jq -r '.started_at' "$status_file")"
        echo "任务: $(jq -r '.task' "$status_file")"
    fi
    
    # 检查日志文件
    if [ -f "$log_file" ]; then
        local line_count=$(wc -l < "$log_file")
        echo "日志行数: $line_count"
        
        # 显示最后几条重要日志
        echo ""
        echo "最新日志:"
        tail -3 "$log_file" | jq -r '.content // .message // .' 2>/dev/null || tail -3 "$log_file"
    fi
    
    # 检查结果文件
    local result_file=".agent-results/${agent}.json"
    if [ -f "$result_file" ]; then
        echo ""
        echo "✅ 结果文件已生成: $result_file"
    fi
}

echo "=== Agent 进度检查: $AGENT_NAME ==="
echo ""
check_single_agent "$AGENT_NAME"
