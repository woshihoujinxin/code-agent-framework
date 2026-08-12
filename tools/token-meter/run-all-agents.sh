#!/usr/bin/env bash
# 稳健版 19-agent token 实测：严格串行 + 随机间隔防 429 + 异常重跑 + 自动报告
set -u
PC=/c/develop/workspace/todo-cli-demo/.claude
PROJ=/c/develop/workspace/todo-cli-demo
D=/c/Users/houjinxin/.claude/projects/C--develop-workspace-todo-cli-demo
PY=/c/Users/houjinxin/anaconda3/python.exe
REPORT=/c/develop/aiws/.claude/tools/token-meter/reports/agent-comparison.md
RAW=/c/develop/aiws/.claude/tools/token-meter/reports/agent-raw.tsv
AGENTS="artifact-validator build-builder code-dev-backend code-dev-frontend code-discovery-analyst code-export-specialist code-ops code-planner code-product-manager code-prototype-builder code-prototype-critic code-researcher code-reviewer code-sage code-tester-correctness code-tester-e2e code-tester-quality code-tester-robustness code-tester-security"
PROMPT="请依次计算 1+1、2+2、3+3，只回复三个数字用空格分隔，不要任何其他内容"
MIN_TOK=15000   # 低于此判定为截断/故障，重跑（正常 agent 都 >18000）

total_tok() {
  "$PY" - "$1" <<'PYEOF'
import json,sys
t=0
for ln in open(sys.argv[1],encoding='utf-8'):
    try:d=json.loads(ln)
    except:continue
    m=d.get('message',{})
    if isinstance(m,dict) and 'usage' in m:
        u=m['usage'];t+=u.get('input_tokens',0)+u.get('output_tokens',0)+u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0)
print(t)
PYEOF
}

# 跑一次，返回 token（失败返回 0）
run_once() {
  local pre post
  pre=$(ls -t "$D"/*.jsonl 2>/dev/null | head -1)
  ( cd "$PROJ" && timeout 120 claude --agent "$1" -p "$PROMPT" --allow-dangerously-skip-permissions >/dev/null 2>&1 ) || true
  post=$(ls -t "$D"/*.jsonl 2>/dev/null | head -1)
  if [ "$post" != "$pre" ] && [ -n "$post" ]; then total_tok "$post"; else echo 0; fi
}

# 稳健跑：token<MIN_TOK 则重跑（最多3次），防截断/限流故障
run_robust() {
  local agent=$1 tok=0 attempt
  for attempt in 1 2 3; do
    tok=$(run_once "$agent")
    if [ "${tok:-0}" -ge "$MIN_TOK" ] 2>/dev/null; then echo "$tok"; return 0; fi
    echo "  ⚠ $agent 第${attempt}次异常(tok=${tok:-0}<$MIN_TOK)，等20s重跑" >&2
    sleep 20
  done
  echo "${tok:-0}"
}

declare -A BEFORE AFTER

run_version() {
  local ref=$1 label=$2 a tok
  echo "===== [$label] checkout $ref ====="
  git -C "$PC" checkout "$ref" >/dev/null 2>&1
  for a in $AGENTS; do
    tok=$(run_robust "$a")
    if [ "$label" = before ]; then BEFORE[$a]=$tok; else AFTER[$a]=$tok; fi
    echo "[$label] $a → $tok"
    sleep $((RANDOM % 8 + 8))   # 随机 8-15s 间隔，防 429 限流
  done
}

run_version feat/review-gate-and-shared-acceptance before
echo "===== 版本切换，等 30s ====="
sleep 30
run_version feat/token-optimization after
git -C "$PC" checkout feat/token-optimization >/dev/null 2>&1

# 写 raw
echo -e "agent\tbefore\tafter" > "$RAW"
for a in $AGENTS; do echo -e "$a\t${BEFORE[$a]:-NA}\t${AFTER[$a]:-NA}" >> "$RAW"; done

# 生成报告
"$PY" - "$RAW" "$REPORT" <<'PYEOF'
import sys
raw,out=sys.argv[1],sys.argv[2]
rows=[];tot_b=tot_a=0
for ln in open(raw,encoding='utf-8').read().splitlines()[1:]:
    p=ln.split('\t')
    if len(p)<3:continue
    a,b,c=p[0],p[1],p[2]
    try:
        bi,ci=int(b),int(c);d=ci-bi
        sign=f"↓{abs(d)}" if d<0 else (f"↑{d}" if d>0 else "0")
        rows.append((a,bi,ci,sign,d));tot_b+=bi;tot_a+=ci
    except:rows.append((a,b,c,'-',0))
L=["# 19 个 Agent 人设 Token 实测对比","","> 稳健版：串行+随机间隔防429+异常重跑。每个 agent 以 `claude --agent` 启动，3 固定问题。",
   "> token = input+output+cache_read+cache_write。输入输出钉死，差异来自人设。","",
   "| agent | 优化前 | 优化后 | 节省 | 变化% |","|-------|--------|--------|------|------|"]
for a,b,c,s,d in sorted(rows,key=lambda x:x[4]):
    L.append(f"| {a} | {b:,} | {c:,} | {s} | {abs(d/b*100) if b else 0:.1f}% |")
L.append(f"| **合计** | **{tot_b:,}** | **{tot_a:,}** | **↓{tot_b-tot_a:,}** | **{(tot_b-tot_a)/tot_b*100:.1f}%** |")
open(out,'w',encoding='utf-8').write('\n'.join(L))
print('\n'.join(L))
PYEOF
echo ""; echo "报告: $REPORT"
