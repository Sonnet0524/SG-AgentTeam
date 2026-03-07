#!/bin/bash
# ====================================
# Agent 状态监控器
# ====================================

echo "=== Agent Team 状态总览 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 统计信息
TOTAL_AGENTS=$(ls .agent-status/*.json 2>/dev/null | wc -l)
RUNNING_AGENTS=0
COMPLETED_AGENTS=0
ERROR_AGENTS=0

for status_file in .agent-status/*.json; do
    [ -f "$status_file" ] || continue
    
    agent=$(basename "$status_file" .json)
    status=$(jq -r '.status' "$status_file" 2>/dev/null)
    
    case "$status" in
        "running")
            RUNNING_AGENTS=$((RUNNING_AGENTS + 1))
            ;;
        "completed")
            COMPLETED_AGENTS=$((COMPLETED_AGENTS + 1))
            ;;
        "error")
            ERROR_AGENTS=$((ERROR_AGENTS + 1))
            ;;
    esac
done

echo "统计信息:"
echo "  总 Agent 数: $TOTAL_AGENTS"
echo "  🟢 运行中: $RUNNING_AGENTS"
echo "  ✅ 已完成: $COMPLETED_AGENTS"
echo "  ❌ 错误: $ERROR_AGENTS"
echo ""

# 详细状态
echo "详细状态:"
echo ""

for status_file in .agent-status/*.json; do
    [ -f "$status_file" ] || continue
    
    agent=$(basename "$status_file" .json)
    status=$(jq -r '.status' "$status_file" 2>/dev/null)
    started=$(jq -r '.started_at' "$status_file" 2>/dev/null)
    task=$(jq -r '.task' "$status_file" 2>/dev/null)
    
    # 状态图标
    case "$status" in
        "running")
            icon="🟢"
            ;;
        "completed")
            icon="✅"
            ;;
        "error")
            icon="❌"
            ;;
        *)
            icon="❓"
            ;;
    esac
    
    echo "$icon $agent"
    echo "   状态: $status"
    echo "   启动: $started"
    echo "   任务: $task"
    
    # 检查进程是否真的在运行
    pid_file=".agent-pids/${agent}.pid"
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "   进程: 运行中 (PID: $pid)"
        else
            echo "   进程: 已退出"
            # 检查是否是异常退出
            if [ "$status" = "running" ]; then
                echo "   ⚠️  异常: 状态文件显示运行中，但进程已退出"
            fi
        fi
    fi
    
    # 检查是否有结果
    result_file=".agent-results/${agent}.json"
    if [ -f "$result_file" ]; then
        echo "   结果: ✅ 已生成"
    fi
    
    echo ""
done

# 检查异常情况
echo "异常检查:"
echo ""

abnormal_found=0

for status_file in .agent-status/*.json; do
    [ -f "$status_file" ] || continue
    
    agent=$(basename "$status_file" .json)
    status=$(jq -r '.status' "$status_file" 2>/dev/null)
    pid_file=".agent-pids/${agent}.pid"
    
    # 检查：状态显示运行但进程已退出
    if [ "$status" = "running" ] && [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ! ps -p "$pid" > /dev/null 2>&1; then
            echo "⚠️  $agent: 状态异常"
            echo "   - 状态文件显示运行中"
            echo "   - 但进程已退出 (PID: $pid)"
            echo "   - 建议: 运行 ./scripts/agents/collect-results.sh $agent"
            echo ""
            abnormal_found=1
        fi
    fi
    
    # 检查：日志文件增长异常
    log_file="logs/${agent}.log"
    if [ -f "$log_file" ]; then
        # 检查是否有错误
        if grep -q "error\|Error\|ERROR" "$log_file" 2>/dev/null; then
            echo "⚠️  $agent: 日志中发现错误"
            echo "   - 日志文件: $log_file"
            echo "   - 建议: 查看 tail -50 $log_file"
            echo ""
            abnormal_found=1
        fi
    fi
done

if [ $abnormal_found -eq 0 ]; then
    echo "✅ 所有 Agent 状态正常"
fi
