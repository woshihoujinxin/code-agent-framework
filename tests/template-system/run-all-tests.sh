#!/bin/bash

# 模板系统批量测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "模板系统批量测试"
echo "================================"
echo ""

TEST_CASES=("TC-001" "TC-002" "TC-003" "TC-004")
TOTAL=${#TEST_CASES[@]}
PASSED=0
FAILED=0

for TEST_ID in "${TEST_CASES[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "运行测试: $TEST_ID"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if "$SCRIPT_DIR/run-test.sh" "$TEST_ID"; then
    echo "✅ $TEST_ID 通过"
    ((PASSED++))
  else
    echo "❌ $TEST_ID 失败"
    ((FAILED++))
  fi

  echo ""
done

echo "================================"
echo "测试汇总"
echo "================================"
echo "总数: $TOTAL"
echo "通过: $PASSED"
echo "失败: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "🎉 所有测试通过！"
  exit 0
else
  echo "⚠️  有 $FAILED 个测试失败"
  exit 1
fi
