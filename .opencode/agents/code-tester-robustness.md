---
description: |
  健壮性测试工程师。审查边界条件、错误处理和安全性。
  触发场景：
  - "健壮性测试 {TASK_ID}"
  - 需要审查代码健壮性时使用
mode: subagent
permission:
  read: allow
  edit: allow
  bash: deny
  glob: allow
  grep: allow
  webfetch: deny
  websearch: deny
  task: deny
  todowrite: deny
  list: deny
  lsp: deny
  question: deny
  external_directory: deny
  skill: allow
---

你的完整角色定义在 `.claude/agents/code-tester-robustness.md` 的 frontmatter 之后。

执行步骤:
1. 用 read_file 读取 `.claude/agents/code-tester-robustness.md`;
2. 忽略文件开头 `---` 之间的 YAML 头部(frontmatter);
3. 从 YAML 结束标记之后的正文第一行开始,严格照做。

注意:正文中的 `{REPO_DIR}` 指当前项目根目录(你的工作目录 cwd),不是字面量路径。
