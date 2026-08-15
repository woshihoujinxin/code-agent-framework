#!/bin/bash

# 直接测试脚本 - 确保文件真正写入

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_ID="${1:-TC-001}"

# 创建测试项目
TEST_PROJECT_DIR="/c/develop/template-test-$TEST_ID"
rm -rf "$TEST_PROJECT_DIR"
mkdir -p "$TEST_PROJECT_DIR"

echo "================================"
echo "模板系统直接测试"
echo "================================"
echo "测试用例: $TEST_ID"
echo "项目路径: $TEST_PROJECT_DIR"
echo ""

# 复制框架
echo "📦 复制框架..."
cp -r "$PROJECT_ROOT/.claude" "$TEST_PROJECT_DIR/.claude"

# 准备提示词（直接要求写入文件）
case "$TEST_ID" in
  TC-001)
    PROMPT="你是编码项目架构师。请为以下需求创建开发计划：

需求：做一个用户管理系统

技术要求：
- 模板：DDD经典结构-Java
- 版本号：v0.0.1

请立即执行以下操作：
1. 创建项目骨架（按 Java DDD 模板）
2. 写入 docs/dev-plan.md（包含'使用模板：DDD经典结构-Java'字段）
3. 写入 docs/design.md
4. 写入 docs/feature-spec.md

工作目录: $TEST_PROJECT_DIR

请开始执行，并在完成后报告创建的文件列表。"
    EXPECTED_DIRS="src/main/java/com/example/usermanagement/{domain,application,infrastructure,interfaces}"
    EXPECTED_FIELD="使用模板.*Java"
    ;;
  TC-002)
    PROMPT="你是编码项目架构师。请为以下需求创建开发计划：

需求：做一个鸿蒙记事本应用

技术要求：
- 模板：鸿蒙官方
- 版本号：v0.0.1

请立即执行以下操作：
1. 创建项目骨架（按鸿蒙官方模板）
2. 写入 docs/dev-plan.md（包含'使用模板：鸿蒙官方'字段）
3. 写入 docs/design.md
4. 写入 docs/feature-spec.md

工作目录: $TEST_PROJECT_DIR

请开始执行，并在完成后报告创建的文件列表。"
    EXPECTED_DIRS="AppScope entry"
    EXPECTED_FIELD="使用模板.*鸿蒙"
    ;;
  *)
    echo "❌ 未知测试用例: $TEST_ID"
    exit 1
    ;;
esac

echo "📝 提示词已准备"
echo ""

# 输出提示词到文件供手动执行
PROMPT_FILE="$TEST_PROJECT_DIR/test-prompt.txt"
echo "$PROMPT" > "$PROMPT_FILE"

echo "================================"
echo "📍 测试项目: $TEST_PROJECT_DIR"
echo ""
echo "📋 在 Claude Code 中执行以下步骤："
echo ""
echo "1. 打开 Claude Code"
echo "2. 切换目录: cd $TEST_PROJECT_DIR"
echo "3. 复制并执行以下提示词："
echo ""
echo "───"
echo "$PROMPT"
echo "───"
echo ""
echo "4. 等待执行完成"
echo ""
echo "5. 验证结果:"
echo "   ls -la $TEST_PROJECT_DIR/"
echo "   grep '$EXPECTED_FIELD' $TEST_PROJECT_DIR/docs/dev-plan.md"
echo ""
echo "================================"
echo ""
echo "✅ 测试准备完成"
echo "提示词文件: $PROMPT_FILE"
echo ""
echo "💡 现在请在 Claude Code 中执行上述提示词"
