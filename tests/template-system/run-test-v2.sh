#!/bin/bash

# 跨平台模板系统测试脚本 v2
# 自动检测系统并选择合适的执行方式

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_DIR="$SCRIPT_DIR"
TEST_ID="$1"

if [ -z "$TEST_ID" ]; then
  echo "用法: $0 <TEST_ID>"
  echo "示例: $0 TC-001"
  exit 1
fi

# 检测操作系统
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
  Linux*)     PLATFORM="linux";;
  Darwin*)    PLATFORM="mac";;
  CYGWIN*)    PLATFORM="windows";;
  MINGW*)     PLATFORM="windows";;
  MSYS*)      PLATFORM="windows";;
  *)          PLATFORM="unknown";;
esac

echo "🖥️  检测到平台: $PLATFORM ($OS_TYPE)"

# 查找提示词文件
PROMPT_FILE="$TEST_DIR/prompts/$TEST_ID.md"
if [ ! -f "$PROMPT_FILE" ]; then
  echo "❌ 测试用例不存在: $PROMPT_FILE"
  exit 1
fi

# 创建测试项目目录
TEST_PROJECT_DIR="/tmp/template-test-$TEST_ID"
rm -rf "$TEST_PROJECT_DIR"
mkdir -p "$TEST_PROJECT_DIR"
cd "$TEST_PROJECT_DIR"

echo "📋 测试用例: $TEST_ID"
echo "📁 测试项目: $TEST_PROJECT_DIR"
echo ""

# 提取提示词内容
PROMPT_CONTENT=$(sed -n '/## 提示词（发送给 Planner）/,/## 预期结果/p' "$PROMPT_FILE" | sed '1d;$d')

echo "📝 提示词内容:"
echo "$PROMPT_CONTENT"
echo ""

# 复制框架到测试项目
echo "📦 复制框架到测试项目..."
cp -r "$PROJECT_ROOT/.claude" "$TEST_PROJECT_DIR/.claude"

# 根据平台选择执行方式
case "$PLATFORM" in
  linux|mac)
    echo "🤖 使用 claude -p 调用 Planner..."
    if command -v claude &> /dev/null; then
      echo "$PROMPT_CONTENT" | claude -p 2>&1 | tee "$TEST_DIR/reports/$TEST_ID-execution.log"
    else
      echo "⚠️  claude 命令不可用，请手动在 Claude Code 中执行上述提示词"
      echo "📍 测试项目: $TEST_PROJECT_DIR"
    fi
    ;;
  windows)
    echo "🤖 Windows 环境，使用替代方式..."
    echo "⚠️  Git Bash 中 claude -p 可能不可用"
    echo "📍 请在 Claude Code 中手动执行提示词，或使用 PowerShell"
    echo ""
    echo "💡 推荐方式："
    echo "1. 打开 Claude Code"
    echo "2. 切换工作目录到: $TEST_PROJECT_DIR"
    echo "3. 执行以下提示词："
    echo ""
    echo "---"
    echo "$PROMPT_CONTENT"
    echo "---"
    ;;
  *)
    echo "⚠️  未知平台，请手动测试"
    echo "📍 测试项目: $TEST_PROJECT_DIR"
    ;;
esac

echo ""
echo "🔍 验证结果（如已执行）:"
echo "项目结构:"
ls -la "$TEST_PROJECT_DIR/src/" 2>/dev/null || echo "src/ 目录尚未创建"
echo ""
echo "docs 目录:"
ls -la "$TEST_PROJECT_DIR/docs/" 2>/dev/null || echo "docs/ 目录尚未创建"
