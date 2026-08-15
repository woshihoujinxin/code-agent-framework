#!/bin/bash

# 模板系统测试脚本
# 用法：./run-test.sh TC-001

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

# 提取提示词内容（发送给 Planner）
PROMPT_CONTENT=$(sed -n '/## 提示词（发送给 Planner）/,/## 预期结果/p' "$PROMPT_FILE" | sed '1d;$d')

echo "📝 提示词内容:"
echo "$PROMPT_CONTENT"
echo ""

# 复制框架到测试项目
echo "📦 复制框架到测试项目..."
cp -r "$PROJECT_ROOT/.claude" "$TEST_PROJECT_DIR/.claude"

# 调用 Claude Code 执行提示词
echo "🤖 调用 Planner..."
echo "$PROMPT_CONTENT" | claude -p 2>&1 | tee "$TEST_DIR/reports/$TEST_ID-execution.log"

echo ""
echo "🔍 验证结果..."
echo "项目结构:"
ls -la "$TEST_PROJECT_DIR/src/" 2>/dev/null || echo "src/ 目录不存在"

echo ""
echo "📄 dev-plan.md 模板字段:"
grep "使用模板" "$TEST_PROJECT_DIR/docs/dev-plan.md" 2>/dev/null || echo "未找到模板字段"

echo ""
echo "✅ 测试完成。查看详细报告: $TEST_DIR/reports/$TEST_ID-execution.log"
