#!/bin/bash

# 模板系统验证脚本 - 验证模板文件和 Planner 逻辑

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "================================"
echo "模板系统验证"
echo "================================"
echo ""

PASSED=0
FAILED=0

# 验证函数
check_item() {
  local description="$1"
  local check_command="$2"

  echo -n "检查: $description ... "
  if eval "$check_command" > /dev/null 2>&1; then
    echo "✅ 通过"
    ((PASSED++))
    return 0
  else
    echo "❌ 失败"
    ((FAILED++))
    return 1
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 验证模板文件存在"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_item "Python DDD 模板 README" "[ -f '$PROJECT_ROOT/skills/project-templates/ddd/python-ddd/README.md' ]"
check_item "Node DDD 模板 README" "[ -f '$PROJECT_ROOT/skills/project-templates/ddd/node-ddd/README.md' ]"
check_item "Go DDD 模板 README" "[ -f '$PROJECT_ROOT/skills/project-templates/ddd/go-ddd/README.md' ]"
check_item "Java DDD 模板 README" "[ -f '$PROJECT_ROOT/skills/project-templates/ddd/java-ddd/README.md' ]"
check_item "鸿蒙模板 README" "[ -f '$PROJECT_ROOT/skills/project-templates/harmonyos/README.md' ]"
check_item "模板契约文件" "[ -f '$PROJECT_ROOT/skills/project-templates/template-contract.md' ]"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. 验证 Planner 人设包含模板逻辑"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_item "Planner 必读输入包含模板契约" "grep -q 'template-contract.md' '$PROJECT_ROOT/agents/code-planner.md'"
check_item "Planner 项目骨架包含模板优先级" "grep -q '模板参数优先级' '$PROJECT_ROOT/agents/code-planner.md'"
check_item "Planner 模板参数格式" "grep -q '模板：DDD经典结构-Java' '$PROJECT_ROOT/agents/code-planner.md'"
check_item "dev-plan.md 模板字段" "grep -q '使用模板.*{无模板' '$PROJECT_ROOT/agents/code-planner.md'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. 验证 SKILL.md 包含模板导航"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_item "SKILL.md 受众矩阵包含模板契约" "grep -q 'template-contract.md' '$PROJECT_ROOT/skills/coding-standards/SKILL.md'"
check_item "SKILL.md 角色导航包含模板契约" "grep -q 'template-contract.md（创建项目骨架时）' '$PROJECT_ROOT/skills/coding-standards/SKILL.md'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. 验证模板内容正确性"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_item "Java DDD 模板包含四层目录说明" "grep -q 'domain/application/interface/infrastructure' '$PROJECT_ROOT/skills/project-templates/ddd/java-ddd/README.md'"
check_item "鸿蒙模板包含 AppScope" "grep -q 'AppScope' '$PROJECT_ROOT/skills/project-templates/harmonyos/README.md'"
check_item "模板契约包含引用规则" "grep -q '模板引用方式' '$PROJECT_ROOT/skills/project-templates/template-contract.md'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. 模拟测试 - 创建测试项目并复制模板"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TEST_DIR="/tmp/template-verify-$$"
mkdir -p "$TEST_DIR"

# 模拟 Java DDD 模板复制
JAVA_TEMPLATE_DIR="$PROJECT_ROOT/skills/project-templates/ddd/java-ddd"
if [ -d "$JAVA_TEMPLATE_DIR" ]; then
  mkdir -p "$TEST_DIR/java-test"
  cp -r "$JAVA_TEMPLATE_DIR"/* "$TEST_DIR/java-test/" 2>/dev/null

  check_item "Java DDD 模板可复制" "[ -f '$TEST_DIR/java-test/README.md' ]"
  check_item "Java DDD 模板 README 包含四层结构" "grep -q 'domain/application/interface/infrastructure' '$TEST_DIR/java-test/README.md'"
fi

# 模拟鸿蒙模板复制
HARMONY_TEMPLATE_DIR="$PROJECT_ROOT/skills/project-templates/harmonyos"
if [ -d "$HARMONY_TEMPLATE_DIR" ]; then
  mkdir -p "$TEST_DIR/harmony-test"
  cp -r "$HARMONY_TEMPLATE_DIR"/* "$TEST_DIR/harmony-test/" 2>/dev/null

  check_item "鸿蒙模板可复制" "[ -f '$TEST_DIR/harmony-test/README.md' ]"
  check_item "鸿蒙模板包含 AppScope" "[ -d '$TEST_DIR/harmony-test/AppScope' ]"
fi

# 清理测试目录
rm -rf "$TEST_DIR"

echo ""
echo "================================"
echo "验证汇总"
echo "================================"
echo "通过: $PASSED"
echo "失败: $FAILED"
echo "总计: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "🎉 所有验证通过！"
  echo ""
  echo "模板系统状态："
  echo "✅ 模板文件完整"
  echo "✅ Planner 逻辑正确"
  echo "✅ SKILL.md 导航正确"
  echo "✅ 模板内容正确"
  echo "✅ 模板可复制"
  echo ""
  echo "建议：在实际项目中测试完整流程（在 Claude Code 中执行提示词）"
  exit 0
else
  echo "⚠️  有 $FAILED 个验证失败"
  exit 1
fi
