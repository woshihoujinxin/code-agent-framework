#!/usr/bin/env bash
# run-ab.sh — 自动化 token A/B 实测（层 B）
#
# 同一项目同一 prompt，分别用「优化前/后」两版框架跑 claude -p，
# 对比两个 session 的真实 usage（input/output/cache_read/cache_write）。
#
# 用法:
#   ./run-ab.sh "<prompt>" [old_ref] [new_ref] [project_dir]
#
# 默认:
#   old_ref = feat/review-gate-and-shared-acceptance（token 优化前）
#   new_ref = feat/token-optimization（token 优化后）
#   project = /c/develop/workspace/todo-cli-demo（需有 .claude 子目录）
#
# 示例:
#   ./run-ab.sh "用一句话描述这个项目做什么"
#   ./run-ab.sh "调用 code-planner agent 分析需求：做个 todo" "" "" /c/develop/aiws/myagent
#
# 原理: 切项目 .claude 的 git 分支 → 各跑 claude -p → 找新 session → trace.py 对比
set -u

PROMPT="${1:-用一句话描述这个项目是做什么的}"
OLD="${2:-feat/review-gate-and-shared-acceptance}"
NEW="${3:-feat/token-optimization}"
PROJ="${4:-/c/develop/workspace/todo-cli-demo}"
PY="${PY:-/c/Users/houjinxin/anaconda3/python.exe}"
PC="$PROJ/.claude"

[ -d "$PC/.git" ] || { echo "✗ 项目 .claude 不是 git 仓库: $PC"; exit 1; }
[ -d "$PROJ" ] || { echo "✗ 项目目录不存在: $PROJ"; exit 1; }

# 项目路径 → Claude Code projects 目录（用项目末段 glob 匹配，避免路径编码差异）
PROJ_NAME=$(basename "$PROJ")
SESSDIR=$(ls -d "$HOME/.claude/projects/"*-"$PROJ_NAME" 2>/dev/null | head -1)
if [ -z "$SESSDIR" ]; then
  echo "✗ 找不到 session 目录（projects/*-$PROJ_NAME）。先在该项目跑一次 claude 生成目录。"
  exit 1
fi
echo "session 目录: $SESSDIR"

echo "项目: $PROJ"
echo "分支: $OLD（优化前）→ $NEW（优化后）"
echo "prompt: $PROMPT"
echo ""

echo "fetch 框架分支..."
git -C "$PC" fetch origin "$OLD" "$NEW" >/dev/null 2>&1 || git -C "$PC" fetch >/dev/null 2>&1 || true

run_one() {
  local ref=$1 label=$2
  git -C "$PC" checkout "$ref" >/dev/null 2>&1 || { echo "✗ checkout 失败: $ref" >&2; return 1; }
  local pre
  pre=$(ls -t "$SESSDIR"/*.jsonl 2>/dev/null | head -1)
  echo "[$label] claude -p (ref=$ref)..." >&2
  ( cd "$PROJ" && claude -p "$PROMPT" --allow-dangerously-skip-permissions >/dev/null 2>&1 ) || true
  local post
  post=$(ls -t "$SESSDIR"/*.jsonl 2>/dev/null | head -1)
  if [ "$post" = "$pre" ] || [ -z "$post" ]; then
    echo "  ✗ 未生成新 session" >&2
    return 1
  fi
  echo "  ✓ $(basename "$post")" >&2
  echo "$post"   # 只路径到 stdout，供捕获
}

SA=$(run_one "$OLD" "优化前") || { echo "中止"; exit 1; }
SB=$(run_one "$NEW" "优化后") || { echo "中止"; exit 1; }

# 恢复到优化后版本
git -C "$PC" checkout "$NEW" >/dev/null 2>&1

echo ""
echo "=========================================="
echo "对比: $SA"
echo "  vs: $SB"
echo "=========================================="
"$PY" "$PC/tools/token-meter/trace.py" --before "$SA" --after "$SB" \
  --report "$PC/tools/token-meter/reports/ab-report.md"
