#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trace.py — 真实会话 token 解析与前后对比（层 B：真实计费）。

解析 Claude Code session jsonl 里已记录的 usage（input/output/cache_read/cache_write），
汇总真实 token 消耗，支持两个 session A/B 对比。

与 scan.py 的关系：
  scan.py = 层 A（静态结构，tiktoken 估文件 token）
  trace.py = 层 B（动态实测，解析真实会话 usage）—— 业界标准做法

用法:
  python tools/token-meter/trace.py <session.jsonl>                       # 单 session 分析
  python tools/token-meter/trace.py --before a.jsonl --after b.jsonl       # 前后对比
  python tools/token-meter/trace.py --before a --after b --report tools/token-meter/reports/trace-report.md

找 session 文件:
  Windows: C:\\Users\\<user>\\.claude\\projects\\<项目编码名>\\<uuid>.jsonl
  session 文件名是 uuid，按 mtime 取最新即可。
"""
import argparse
import json
import sys
from pathlib import Path

# Anthropic 通用计费倍率（相对权重，非美元；价格随模型变，这里用典型值）
# input 1.0 / output 5.0（推理贵）/ cache_write 1.25（写缓存贵）/ cache_read 0.1（读缓存便宜）
# 用户可在命令行覆盖
DEFAULT_RATES = {"input": 1.0, "output": 5.0, "cache_write": 1.25, "cache_read": 0.1}


def analyze(session_path: str, label: str = "") -> dict:
    """解析一个 session jsonl，汇总 usage。"""
    p = Path(session_path)
    tot = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "turns": 0,
           "task_calls": 0}
    with open(p, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            m = d.get("message", {})
            if isinstance(m, dict) and "usage" in m:
                u = m["usage"]
                tot["input"] += u.get("input_tokens", 0)
                tot["output"] += u.get("output_tokens", 0)
                tot["cache_read"] += u.get("cache_read_input_tokens", 0)
                tot["cache_write"] += u.get("cache_creation_input_tokens", 0)
                tot["turns"] += 1
            # 数 Agent（subagent 派发）调用 —— 框架用 Agent 工具派 PM/Planner/Dev/Tester
            s = ln
            if '"name":"Agent"' in s or '"name": "Agent"' in s:
                tot["task_calls"] += 1
    return {"label": label or p.name, "path": str(p), **tot}


def billed(tot: dict, rates: dict) -> float:
    """按计费倍率算等效计费 token。"""
    return (tot["input"] * rates["input"]
            + tot["output"] * rates["output"]
            + tot["cache_read"] * rates["cache_read"]
            + tot["cache_write"] * rates["cache_write"])


def cache_hit_rate(tot: dict) -> float:
    """缓存命中率 ≈ cache_read / (cache_read + input + cache_write)。"""
    denom = tot["cache_read"] + tot["input"] + tot["cache_write"]
    return tot["cache_read"] / denom if denom else 0.0


def fmt(n: int) -> str:
    return f"{n:,}"


def print_one(tot: dict, rates: dict):
    b = billed(tot, rates)
    hr = cache_hit_rate(tot) * 100
    print(f"\n  {tot['label']}")
    print(f"    turns(带usage): {tot['turns']}  |  Task派发: {tot['task_calls']}")
    print(f"    input       : {fmt(tot['input'])}")
    print(f"    output      : {fmt(tot['output'])}")
    print(f"    cache_read  : {fmt(tot['cache_read'])}  ← 命中缓存（×{rates['cache_read']}）")
    print(f"    cache_write : {fmt(tot['cache_write'])}")
    print(f"    缓存命中率    : {hr:.1f}%")
    print(f"    计费等效token: {fmt(int(b))}  (input×{rates['input']} + output×{rates['output']} + cr×{rates['cache_read']} + cw×{rates['cache_write']})")


def compare(before: dict, after: dict, rates: dict) -> dict:
    """两 session 对比。"""
    def delta(k):
        return after[k] - before[k]
    return {
        "before": before, "after": after,
        "input_d": delta("input"), "output_d": delta("output"),
        "cache_read_d": delta("cache_read"), "cache_write_d": delta("cache_write"),
        "billed_before": billed(before, rates),
        "billed_after": billed(after, rates),
    }


def gen_report(cmp: dict, rates: dict, out_path: str):
    b, a = cmp["before"], cmp["after"]
    bb, ba = cmp["billed_before"], cmp["billed_after"]
    bd = ba - bb
    pct = (bd / bb * 100) if bb else 0
    L = []
    w = L.append
    w("# Token 实测对比报告（层 B · 真实会话）")
    w("")
    w(f"> 对比两个真实 Claude Code 会话的 usage（从 session jsonl 解析）")
    w(f"> 计费倍率: input×{rates['input']} / output×{rates['output']} / cache_write×{rates['cache_write']} / cache_read×{rates['cache_read']}")
    w(f"> ⚠️ 可比前提：两 session 跑**同一需求**（同任务/同流程），否则差异含任务量噪音")
    w("")
    w("## 会话信息")
    w("")
    w(f"| | 优化前 | 优化后 |")
    w(f"|---|---|---|")
    w(f"| session | {b['label']} | {a['label']} |")
    w(f"| 带usage轮次 | {b['turns']} | {a['turns']} |")
    w(f"| Task派发次数 | {b['task_calls']} | {a['task_calls']} |")
    w(f"| 缓存命中率 | {cache_hit_rate(b)*100:.1f}% | {cache_hit_rate(a)*100:.1f}% |")
    w("")
    w("## 真实 token 消耗对比")
    w("")
    w(f"| 分项 | 优化前 | 优化后 | 差异 |")
    w(f"|------|--------|--------|------|")
    for k, name in [("input", "input"), ("output", "output"),
                    ("cache_read", "cache_read"), ("cache_write", "cache_write")]:
        d = cmp[f"{k}_d"]
        sign = "↓" if d < 0 else "↑"
        w(f"| {name} | {fmt(b[k])} | {fmt(a[k])} | {sign} {fmt(abs(d))} |")
    w("")
    w("## 计费等效 token（加权汇总，核心指标）")
    w("")
    w(f"| | 优化前 | 优化后 | 差异 |")
    w(f"|---|---|---|---|")
    sign = "↓省" if bd < 0 else "↑增"
    w(f"| 计费等效token | {fmt(int(bb))} | {fmt(int(ba))} | **{sign} {fmt(abs(int(bd)))} ({abs(pct):.1f}%)** |")
    w("")
    w("## 解读")
    w("")
    w(f"- **计费等效 token {sign} {fmt(abs(int(bd)))}（{abs(pct):.1f}%）**")
    if cmp["cache_read_d"] < 0:
        w(f"- cache_read {fmt(abs(cmp['cache_read_d']))} ↓：常驻提示词瘦身减少了每轮缓存读量（主要省这儿）")
    if cmp["input_d"] < 0:
        w(f"- input {fmt(abs(cmp['input_d']))} ↓：非缓存输入减少")
    if cmp["output_d"] < 0:
        w(f"- output {fmt(abs(cmp['output_d']))} ↓：模型输出减少（可能轮次/长度变化）")
    w("")
    w("> 注意：若两 session 轮次/派发次数不同，差异含任务量噪音，需结合轮次归一化看（每轮均 token）。")
    Path(out_path).write_text("\n".join(L), encoding="utf-8")
    print(f"\n报告已生成: {out_path}")


def main():
    ap = argparse.ArgumentParser(description="trace.py 真实会话 token 解析与对比（层 B）")
    ap.add_argument("session", nargs="?", help="单 session jsonl 路径")
    ap.add_argument("--before", help="对比：优化前 session jsonl")
    ap.add_argument("--after", help="对比：优化后 session jsonl")
    ap.add_argument("--report", default="tools/token-meter/reports/trace-report.md")
    ap.add_argument("--rate-output", type=float, default=None, help="覆盖 output 计费倍率（默认5.0）")
    args = ap.parse_args()

    rates = dict(DEFAULT_RATES)
    if args.rate_output is not None:
        rates["output"] = args.rate_output

    if args.before and args.after:
        print("解析中...")
        before = analyze(args.before, "优化前")
        after = analyze(args.after, "优化后")
        print_one(before, rates)
        print_one(after, rates)
        cmp = compare(before, after, rates)
        gen_report(cmp, rates, args.report)
        bb, ba = cmp["billed_before"], cmp["billed_after"]
        bd = ba - bb
        pct = (bd / bb * 100) if bb else 0
        sign = "↓省" if bd < 0 else "↑增"
        print(f"\n{'='*50}\n计费等效token: {fmt(int(bb))} → {fmt(int(ba))}  {sign} {fmt(abs(int(bd)))} ({abs(pct):.1f}%)\n{'='*50}")
    elif args.session:
        tot = analyze(args.session)
        print_one(tot, rates)
    else:
        ap.error("需提供 session 路径，或 --before + --after")


if __name__ == "__main__":
    main()
