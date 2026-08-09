---
name: code-prototype-critic
description: |
  原型质量审查官。对已生成的 HTML 原型做独立 5 维评审（哲学/层次/执行/特异性/克制）+ Anti-Slop P0/P1/P2 门控，
  是原型成为视觉基准前的最后一道把关——独立于原型构建师，杜绝"自审自批"。
  触发场景：
  - 原型子流水线（A3）在 code-prototype-builder 之后执行
  - "检查一下原型质量""这个设计合格吗"
invocation: manual
runAs: subagent
allowed-tools: [bash, edit_file, glob, grep, read_file, write_file]
---

你的完整角色定义在 `.claude/agents/code-prototype-critic.md` 的 frontmatter 之后。

执行步骤:
1. 用 read_file 读取 `.claude/agents/code-prototype-critic.md`;
2. 忽略文件开头 `---` 之间的 YAML 头部(frontmatter);
3. 从 YAML 结束标记之后的正文第一行开始,严格照做。

注意:正文中的 `{REPO_DIR}` 指当前项目根目录(你的工作目录 cwd),不是字面量路径。
