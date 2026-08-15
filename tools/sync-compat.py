#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync-compat.py — 从 Claude Code 真源生成 opencode / Reasonix 适配层(薄壳指针)。

设计原则(最大化复用,不重复内容):
  * agents/ commands/ skills/ 是唯一真源,Claude Code 直接读取,永不改动。
  * opencode 与 Reasonix 的适配文件只含 frontmatter + "指针"正文:
    角色正文由 agent 运行时 read_file 读取 .claude/agents/<name>.md,
    仓库里不会出现第二份角色内容。
  * 命令(/goal-develop /goal-deliver /goal-init)与知识库 skills:
      - Reasonix 原生扫描 <workspace>/.claude/commands 与 <workspace>/.claude/skills → 零改动;
      - opencode 原生扫描 <project>/.claude/skills → 零改动;但命令需 .opencode/commands/。
    因此本脚本只为 opencode 生成命令副本,为两个工具生成 16 个 subagent 薄壳。

用法:
  python tools/sync-compat.py build            # 仓库内生成 .opencode/ 与 .reasonix/(提交进仓库)
  python tools/sync-compat.py deploy [target]  # 复制生成物到目标项目根(默认当前目录)
"""

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent  # 仓库根 = .claude/
AGENTS_DIR = REPO_ROOT / "agents"
COMMANDS_DIR = REPO_ROOT / "commands"
OPCODE_DIR = REPO_ROOT / ".opencode"
REASONIX_DIR = REPO_ROOT / ".reasonix"

# Claude Code tools 白名单 → opencode permission 键
OPENCODE_TOOL_PERMISSION = {
    "Read": "read",
    "Write": "edit",
    "Edit": "edit",
    "Bash": "bash",
    "Glob": "glob",
    "Grep": "grep",
    "WebFetch": "webfetch",
    "WebSearch": "websearch",
    "Task": "task",
    "TodoWrite": "todowrite",
}
# opencode 额外权限键(Claude 无对应 tools,统一按等价原则处理)
OPENCODE_EXTRA_KEYS = ["list", "lsp", "question", "external_directory"]
# 固定允许:subagent 需要加载 .claude/skills 里的知识库(coding-standards 等)
OPENCODE_ALWAYS_ALLOW = ["skill"]
# permission 输出顺序(保持生成文件稳定)
OPENCODE_PERMISSION_ORDER = [
    "read", "edit", "bash", "glob", "grep",
    "webfetch", "websearch", "task", "todowrite",
    "list", "lsp", "question", "external_directory", "skill",
]

# Claude Code tools 白名单 → Reasonix 工具名
REASONIX_TOOL_MAP = {
    "Read": ["read_file"],
    "Write": ["write_file", "edit_file"],
    "Edit": ["write_file", "edit_file"],
    "Bash": ["bash"],
    "Glob": ["glob"],
    "Grep": ["grep"],
}


def parse_frontmatter(text: str):
    """解析极简 YAML frontmatter(`---` 之间),返回 (dict, body)。"""
    if not text.startswith("---"):
        raise ValueError("缺少 frontmatter 起始标记 ---")
    lines = text.splitlines()
    assert lines[0].strip() == "---"
    fm = {}
    i = 1
    current_key = None
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            i += 1
            break
        if line.startswith((" ", "\t")) and current_key is not None:
            fm[current_key].append(line.strip())
            i += 1
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "|":
                current_key = key
                fm[key] = []
            else:
                current_key = None
                fm[key] = val
        i += 1
    body = "\n".join(lines[i:]).strip()
    return fm, body


def fmt_description(desc):
    """把 description 统一输出为 YAML 块,避免转义问题。"""
    lines = [ln.strip() for ln in desc.splitlines() if ln.strip()]
    if not lines:
        return 'description: ""'
    out = ["description: |"]
    out.extend(f"  {ln}" for ln in lines)
    return "\n".join(out)


def opencode_permission(tools):
    """Claude tools 白名单 → opencode permission dict(白名单语义,未列出的核心键 deny)。"""
    # 多个 Claude 工具可映射到同一 opencode 键(如 Write/Edit → edit):任一命中即 allow
    perm = {k: "deny" for k in OPENCODE_PERMISSION_ORDER}
    for claude_tool, key in OPENCODE_TOOL_PERMISSION.items():
        if claude_tool in tools:
            perm[key] = "allow"
    for key in OPENCODE_ALWAYS_ALLOW:
        perm[key] = "allow"
    return perm


def reasonix_allowed_tools(tools):
    allowed = set()
    for t in tools:
        allowed.update(REASONIX_TOOL_MAP.get(t, []))
    return sorted(allowed)


POINTER_BODY = """你的完整角色定义在 `.claude/agents/{name}.md` 的 frontmatter 之后。

执行步骤:
1. 用 read_file 读取 `.claude/agents/{name}.md`;
2. 忽略文件开头 `---` 之间的 YAML 头部(frontmatter);
3. 从 YAML 结束标记之后的正文第一行开始,严格照做。

注意:正文中的 `{{REPO_DIR}}` 指当前项目根目录(你的工作目录 cwd),不是字面量路径。
"""


def gen_opencode_agent(name, desc, tools):
    perm = opencode_permission(tools)
    perm_lines = "\n".join(f"  {k}: {v}" for k, v in perm.items())
    return (
        "---\n"
        + fmt_description(desc)
        + "\n"
        + "mode: subagent\n"
        + "permission:\n"
        + perm_lines
        + "\n---\n\n"
        + POINTER_BODY.format(name=name)
    )


def gen_reasonix_skill(name, desc, tools):
    allowed = ", ".join(reasonix_allowed_tools(tools))
    return (
        "---\n"
        + "name: " + name + "\n"
        + fmt_description(desc)
        + "\n"
        + "invocation: manual\n"
        + "runAs: subagent\n"
        + f"allowed-tools: [{allowed}]\n"
        + "---\n\n"
        + POINTER_BODY.format(name=name)
    )


def clean_generated():
    """清理上次 build 生成的旧文件(防止命令改名/删减后残留)。只删脚本管理的 .md/SKILL.md。"""
    for d in (OPCODE_DIR / "agents", OPCODE_DIR / "commands"):
        if d.is_dir():
            for p in d.glob("*.md"):
                p.unlink()
    sd = REASONIX_DIR / "skills"
    if sd.is_dir():
        for p in sd.glob("*/SKILL.md"):
            p.unlink()
        for p in sd.glob("*"):
            if p.is_dir() and not any(p.iterdir()):
                p.rmdir()


def build():
    """仓库内生成 .opencode/ 与 .reasonix/。幂等:先清理旧生成物,再全量重建。"""
    clean_generated()
    written = []

    # 收集 agents
    agents = []
    for p in sorted(AGENTS_DIR.glob("*.md")):
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        name = fm.get("name") or p.stem
        desc = "\n".join(fm["description"]) if isinstance(fm.get("description"), list) else fm.get("description", "")
        tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
        agents.append((name, desc, tools, p.stem))

    # ---- opencode ----
    for name, desc, tools, _stem in agents:
        out = OPCODE_DIR / "agents" / f"{name}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(gen_opencode_agent(name, desc, tools), encoding="utf-8")
        written.append(str(out.relative_to(REPO_ROOT)))

    for cmd in sorted(COMMANDS_DIR.glob("*.md")):
        out = OPCODE_DIR / "commands" / cmd.name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(cmd.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(str(out.relative_to(REPO_ROOT)))

    # ---- reasonix(仅 subagent 薄壳;命令与知识库 skills 由 Reasonix 原生读 .claude/) ----
    for name, desc, tools, _stem in agents:
        out = REASONIX_DIR / "skills" / name / "SKILL.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(gen_reasonix_skill(name, desc, tools), encoding="utf-8")
        written.append(str(out.relative_to(REPO_ROOT)))

    print(f"build 完成,生成/更新 {len(written)} 个文件:")
    for w in written:
        print(f"  + {w}")


def deploy(target):
    """把仓库内的 .opencode/ 与 .reasonix/ 复制到目标项目根。"""
    target = Path(target).resolve()
    for src_name in (".opencode", ".reasonix"):
        src = REPO_ROOT / src_name
        dst = target / src_name
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"deploy: {src} -> {dst}")
        else:
            print(f"deploy: 跳过(未生成) {src_name}")
    print(f"完成。请在项目根分别启动 opencode / reasonix 验证。")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    elif cmd == "deploy":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        deploy(target)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
