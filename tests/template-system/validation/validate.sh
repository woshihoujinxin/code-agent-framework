#!/bin/bash

# 模板测试验证脚本
# 用法：./validation/validate.sh TC-001 /tmp/template-test-TC-001

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEST_ID="$1"
PROJECT_DIR="$2"

if [ -z "$TEST_ID" ] || [ -z "$PROJECT_DIR" ]; then
  echo "用法: $0 <TEST_ID> <PROJECT_DIR>"
  echo "示例: $0 TC-001 /tmp/template-test-TC-001"
  exit 1
fi

PROMPT_FILE="$TEST_DIR/prompts/$TEST_ID.md"
REPORT_FILE="$TEST_DIR/reports/$TEST_ID-validation.txt"

echo "🔍 验证测试: $TEST_ID"
echo "📁 项目目录: $PROJECT_DIR"
echo "" > "$REPORT_FILE"

# 验证函数
check_dir() {
  local dir="$1"
  local description="$2"

  if [ -d "$PROJECT_DIR/$dir" ]; then
    echo "✅ $description: $dir 存在" | tee -a "$REPORT_FILE"
    return 0
  else
    echo "❌ $description: $dir 不存在" | tee -a "$REPORT_FILE"
    return 1
  fi
}

check_file() {
  local file="$1"
  local description="$2"

  if [ -f "$PROJECT_DIR/$file" ]; then
    echo "✅ $description: $file 存在" | tee -a "$REPORT_FILE"
    return 0
  else
    echo "❌ $description: $file 不存在" | tee -a "$REPORT_FILE"
    return 1
  fi
}

check_field() {
  local file="$1"
  local pattern="$2"
  local description="$3"

  if grep -q "$pattern" "$PROJECT_DIR/$file" 2>/dev/null; then
    echo "✅ $description" | tee -a "$REPORT_FILE"
    return 0
  else
    echo "❌ $description" | tee -a "$REPORT_FILE"
    return 1
  fi
}

# 根据测试 ID 执行不同的验证
case "$TEST_ID" in
  TC-001)
    echo "验证 Java DDD 模板..." | tee -a "$REPORT_FILE"
    check_dir "docs" "docs 目录"
    check_dir "src/domain" "DDD domain 层"
    check_dir "src/application" "DDD application 层"
    check_dir "src/interface" "DDD interface 层"
    check_dir "src/infrastructure" "DDD infrastructure 层"
    check_file "docs/dev-plan.md" "dev-plan.md"
    check_field "docs/dev-plan.md" "使用模板.*Java" "模板字段记录正确"
    ;;
  TC-002)
    echo "验证鸿蒙官方模板..." | tee -a "$REPORT_FILE"
    check_dir "AppScope" "AppScope 目录"
    check_dir "entry" "entry 目录"
    check_dir "entry/src/main/ets" "ArkTS 源码目录"
    check_file "build-profile.json5" "构建配置"
    check_file "oh-package.json5" "依赖配置"
    check_file "hvigorfile.ts" "构建脚本"
    check_file "docs/dev-plan.md" "dev-plan.md"
    check_field "docs/dev-plan.md" "使用模板.*鸿蒙" "模板字段记录正确"
    ;;
  TC-003)
    echo "验证 DDD 注入无模板..." | tee -a "$REPORT_FILE"
    check_dir "docs" "docs 目录"
    check_dir "src/domain" "DDD domain 层"
    check_dir "src/application" "DDD application 层"
    check_dir "src/interface" "DDD interface 层"
    check_dir "src/infrastructure" "DDD infrastructure 层"
    check_file "docs/dev-plan.md" "dev-plan.md"
    ;;
  TC-004)
    echo "验证默认骨架..." | tee -a "$REPORT_FILE"
    check_dir "docs" "docs 目录"
    check_dir "src" "src 目录"
    check_dir "tests" "tests 目录"
    check_dir "tests/reports" "tests/reports 目录"
    check_file "docs/dev-plan.md" "dev-plan.md"
    # 验证无 DDD 目录
    if [ ! -d "$PROJECT_DIR/src/domain" ]; then
      echo "✅ 无 DDD 目录（符合预期）" | tee -a "$REPORT_FILE"
    else
      echo "❌ 不应有 DDD 目录" | tee -a "$REPORT_FILE"
    fi
    ;;
  *)
    echo "❌ 未知测试用例: $TEST_ID"
    exit 1
    ;;
esac

echo ""
echo "✅ 验证完成。报告: $REPORT_FILE"
