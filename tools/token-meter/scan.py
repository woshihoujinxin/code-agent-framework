#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
token-meter — 框架 token 测算与前后对比。

用 tiktoken(cl100k_base) 精算各文件 token，按场景算"必然加载"的 token 总量，
支持两个 git ref 对比，量化 token 优化省了多少。

用法:
  python tools/token-meter/scan.py --ref HEAD                      # 单 ref 快照
  python tools/token-meter/scan.py --before <旧ref> --after <新ref>  # 前后对比
  python tools/token-meter/scan.py --before <旧> --after <新> --report docs/token-report.md
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import tiktoken

REPO = Path(__file__).resolve().parent.parent.parent  # .claude/
_ENC = tiktoken.get_encoding("cl100k_base")

# ── 文件分类 ──────────────────────────────────────────────────────────
ORCHESTRATOR = "orchestrators/dev-quality-orchestrator.md"
AGENTS_GLOB = "agents/*.md"
SKILLS_GLOB = "skills/*/SKILL.md"
ONDEMAND = [
    "orchestrators/handbook/stock-mode.md",
    "orchestrators/handbook/resilience.md",
    "orchestrators/handbook/escalation.md",
    "orchestrators/handbook/recovery.md",
    "skills/coding-standards/references/e2e-external-deps.md",
    "skills/coding-standards/references/ddd-tactics.md",
]

# ── 场景矩阵 ──────────────────────────────────────────────────────────
# agents: 该场景会用到的角色（每个算一次派发负载）
# ondemand: 该场景触发的外置文件 key（对应 ONDEMAND 的文件名 stem）
SCENARIOS = {
    "纯后端CLI（快速模式）": {
        "agents": ["code-product-manager", "code-planner", "code-dev-backend",
                   "code-tester-correctness", "code-tester-e2e"],
        "ondemand": [],
    },
    "全栈Web（标准SOP+DDD）": {
        "agents": ["code-product-manager", "code-discovery-analyst", "code-prototype-builder",
                   "code-prototype-critic", "code-planner", "code-dev-frontend", "code-dev-backend",
                   "code-ops", "code-tester-correctness", "code-tester-quality",
                   "code-tester-robustness", "code-tester-security", "code-tester-e2e", "code-sage"],
        "ondemand": ["ddd-tactics"],
    },
    "后端API+DB（服务依赖）": {
        "agents": ["code-product-manager", "code-planner", "code-dev-backend", "code-ops",
                   "code-tester-correctness", "code-tester-quality", "code-tester-robustness",
                   "code-tester-security", "code-tester-e2e"],
        "ondemand": ["e2e-external-deps"],
    },
    "存量项目改动": {
        "agents": ["code-planner", "code-dev-backend", "code-dev-frontend",
                   "code-tester-correctness", "code-tester-e2e"],
        "ondemand": ["stock-mode"],
    },
}


def git_show(ref: str, path: str) -> str:
    """读某 ref 下某文件内容。文件不存在返回 ''。"""
    r = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{ref}:{path}"],
        capture_output=True,
    )
    if r.returncode != 0:
        return ""  # 该 ref 下文件不存在（如优化前无 handbook）
    return r.stdout.decode("utf-8", errors="replace")


def tok(text: str) -> int:
    return len(_ENC.encode(text))


def parse_skills(frontmatter: str) -> list:
    """从 agent frontmatter 文本解析 skills 列表。"""
    skills = []
    in_skills = False
    for line in frontmatter.splitlines():
        if line.startswith("skills:"):
            in_skills = True
            continue
        if in_skills:
            if line.startswith("  - "):
                skills.append(line.strip()[2:].strip())
            elif line and not line.startswith(" "):
                break
    return skills


def get_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def agent_payload(ref: str, agent_stem: str, skill_tokens: dict) -> dict:
    """某 agent 派发一次的 token = 人设 + 挂载 skill 的 SKILL.md。"""
    path = f"agents/{agent_stem}.md"
    body = git_show(ref, path)
    persona = tok(body)
    fm = get_frontmatter(body)
    skills = parse_skills(fm)
    skill_tok = sum(skill_tokens.get(s, 0) for s in skills)
    return {
        "persona": persona,
        "skills": skill_tok,
        "skill_names": skills,
        "total": persona + skill_tok,
    }


def snapshot(ref: str) -> dict:
    """算某 ref 的完整 token 快照。"""
    # 主对话常驻
    orch = tok(git_show(ref, ORCHESTRATOR))

    # 所有 skill 的 SKILL.md token
    skills = {}
    for p in (REPO).glob(SKILLS_GLOB):
        stem = p.parent.name
        skills[stem] = tok(git_show(ref, f"skills/{stem}/SKILL.md"))

    # 所有 agent 的派发负载
    agents = {}
    for ap in (REPO).glob(AGENTS_GLOB):
        agents[ap.stem] = agent_payload(ref, ap.stem, skills)

    # 按需外置
    ondemand = {}
    for path in ONDEMAND:
        stem = Path(path).stem
        ondemand[stem] = tok(git_show(ref, path))

    # 场景必然 token
    scenarios = {}
    for name, cfg in SCENARIOS.items():
        agent_sum = sum(agents[a]["total"] for a in cfg["agents"] if a in agents)
        ond_sum = sum(ondemand.get(k, 0) for k in cfg["ondemand"])
        scenarios[name] = {
            "main_resident": orch,
            "agents_total": agent_sum,
            "ondemand_triggered": ond_sum,
            "scenario_total": orch + agent_sum + ond_sum,
            "agent_count": len(cfg["agents"]),
        }

    return {
        "ref": ref,
        "main_resident": orch,
        "skills": skills,
        "agents": agents,
        "ondemand": ondemand,
        "scenarios": scenarios,
    }


def fmt_delta(after: int, before: int) -> str:
    d = after - before
    if before == 0:
        return f"+{after}(新增)"
    pct = d / before * 100
    sign = "↓省" if d < 0 else "↑增"
    return f"{sign} {abs(d)} ({abs(pct):.1f}%)"


def print_snapshot(snap: dict, title: str):
    print(f"\n{'='*60}\n{title}  (ref: {snap['ref']})\n{'='*60}")
    print(f"主对话常驻 orchestrator: {snap['main_resident']} tok")
    print(f"\n按需外置（触发才花，平时 0）:")
    for k, v in snap["ondemand"].items():
        print(f"  {k:30s} {v:5d} tok")
    print(f"\n各场景「必然加载」token:")
    for name, sc in snap["scenarios"].items():
        print(f"  {name}")
        print(f"    主对话常驻 {sc['main_resident']:5d} + "
              f"{sc['agent_count']}个agent派发 {sc['agents_total']:5d} + "
              f"外置触发 {sc['ondemand_triggered']:5d} = "
              f"{sc['scenario_total']:5d} tok")


def compare(before: dict, after: dict) -> dict:
    """两 ref 对比，返回各指标 delta。"""
    out = {"before_ref": before["ref"], "after_ref": after["ref"]}
    out["main_resident"] = {
        "before": before["main_resident"], "after": after["main_resident"],
        "delta": fmt_delta(after["main_resident"], before["main_resident"]),
    }
    out["agents"] = {}
    for a in after["agents"]:
        if a in before["agents"]:
            out["agents"][a] = {
                "before": before["agents"][a]["total"],
                "after": after["agents"][a]["total"],
                "delta": fmt_delta(after["agents"][a]["total"], before["agents"][a]["total"]),
            }
    out["scenarios"] = {}
    for name in after["scenarios"]:
        b = before["scenarios"].get(name, {}).get("scenario_total", 0)
        a_ = after["scenarios"][name]["scenario_total"]
        out["scenarios"][name] = {
            "before": b, "after": a_,
            "delta": fmt_delta(a_, b),
            "before_breakdown": before["scenarios"].get(name, {}),
            "after_breakdown": after["scenarios"][name],
        }
    return out


def gen_report(before: dict, after: dict, cmp: dict, out_path: str):
    lines = []
    w = lines.append
    w("# Token 测算报告")
    w("")
    w(f"> 对比：`{cmp['before_ref']}`（优化前）→ `{cmp['after_ref']}`（优化后）")
    w(f"> 分词器：tiktoken cl100k_base（与 Claude 实际 token 有偏差，**相对优化比例可信**，绝对值仅供参考）")
    w(f"> 生成方式：`python tools/token-meter/scan.py --before {cmp['before_ref']} --after {cmp['after_ref']}`")
    w("")

    w("## 一、主对话常驻（每轮对话都花）")
    w("")
    w(f"| 指标 | 优化前 | 优化后 | 变化 |")
    w(f"|------|--------|--------|------|")
    mr = cmp["main_resident"]
    w(f"| orchestrator 系统提示词 | {mr['before']} | {mr['after']} | **{mr['delta']}** |")
    w("")
    w("> 主对话每轮都带 orchestrator，省的 ×对话轮数 = 实际节省。")
    w("")

    w("## 二、按需外置（平时 0，触发才花）")
    w("")
    w("这些文件优化前**内嵌在常驻里**（每轮都花），优化后挪到外置（触发才花）：")
    w("")
    w("| 文件 | token | 触发条件 |")
    w("|------|-------|---------|")
    trig = {
        "stock-mode": "存量项目", "resilience": "429/超时/崩溃",
        "escalation": "3轮修复失败", "recovery": "会话中断恢复",
        "e2e-external-deps": "E2E 有服务依赖", "ddd-tactics": "DDD 模式",
    }
    for k, v in after["ondemand"].items():
        w(f"| {k} | {v} | {trig.get(k, '-')} |")
    total_ond = sum(after["ondemand"].values())
    w(f"| **合计外置** | **{total_ond}** | 平时不花，触发条件命中才花 |")
    w("")

    w("## 三、各场景「必然加载」token 对比（核心指标）")
    w("")
    w("「必然加载」= 主对话常驻 + 场景用到的 agent 派发负载 + 场景触发的外置。")
    w("这是该场景下**无论是否异常都要花的** token，优化省的就是这里。")
    w("")
    w("| 场景 | 优化前 | 优化后 | 变化 | 说明 |")
    w("|------|--------|--------|------|------|")
    for name, c in cmp["scenarios"].items():
        note = ""
        ab = c["after_breakdown"]
        if ab.get("ondemand_triggered", 0) > 0:
            note = f"含外置触发 {ab['ondemand_triggered']}"
        w(f"| {name} | {c['before']} | {c['after']} | **{c['delta']}** | {note} |")
    w("")

    w("## 四、Agent 派发负载变化（派一次花一次）")
    w("")
    w("| Agent | 优化前 | 优化后 | 变化 |")
    w("|-------|--------|--------|------|")
    for a, c in cmp["agents"].items():
        if c["before"] != c["after"]:
            w(f"| {a} | {c['before']} | {c['after']} | {c['delta']} |")
    w("")

    w("## 五、结论")
    w("")
    # 自动结论
    mr_delta = mr["before"] - mr["after"]
    w(f"- **主对话每轮省 ~{mr_delta} tok**（orchestrator 常驻），对话越长省越多")
    best = min(cmp["scenarios"].items(), key=lambda x: x[1]["after"] - x[1]["before"])
    bd = best[1]["before"] - best[1]["after"]
    w(f"- **{best[0]}** 场景省最多：必然加载 {best[1]['before']} → {best[1]['after']}（**省 {bd} tok**）")
    w(f"- 外置 {total_ond} tok 从「每轮常驻」挪到「按需触发」，低频分支平时 0 开销")
    w("")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n报告已生成: {out_path}")


def main():
    ap = argparse.ArgumentParser(description="token-meter 框架 token 测算")
    ap.add_argument("--ref", help="单 ref 快照")
    ap.add_argument("--before", help="对比：优化前 ref")
    ap.add_argument("--after", help="对比：优化后 ref")
    ap.add_argument("--report", default="docs/token-report.md", help="对比报告输出路径")
    args = ap.parse_args()

    if args.before and args.after:
        print("测算中...")
        before = snapshot(args.before)
        after = snapshot(args.after)
        print_snapshot(before, "【优化前】")
        print_snapshot(after, "【优化后】")
        cmp = compare(before, after)
        gen_report(before, after, cmp, args.report)
        print(f"\n{'='*60}\n核心对比\n{'='*60}")
        print(f"主对话常驻: {before['main_resident']} → {after['main_resident']}  {cmp['main_resident']['delta']}")
        for name, c in cmp["scenarios"].items():
            print(f"  {name}: {c['before']} → {c['after']}  {c['delta']}")
    elif args.ref:
        snap = snapshot(args.ref)
        print_snapshot(snap, f"【快照】")
    else:
        ap.error("需提供 --ref 或 (--before + --after)")


if __name__ == "__main__":
    main()
