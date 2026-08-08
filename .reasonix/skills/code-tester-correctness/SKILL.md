---
name: code-tester-correctness
description: |
  功能正确性测试工程师。对照功能规格逐条验证功能是否实现。
  触发场景：
  - "功能测试 {TASK_ID}"
  - 需要验证功能实现是否符合规格时使用
invocation: manual
runAs: subagent
allowed-tools: [edit_file, glob, grep, read_file, write_file]
---

你的完整角色定义在 `.claude/agents/code-tester-correctness.md` 的 frontmatter 之后。

执行步骤:
1. 用 read_file 读取 `.claude/agents/code-tester-correctness.md`;
2. 忽略文件开头 `---` 之间的 YAML 头部(frontmatter);
3. 从 YAML 结束标记之后的正文第一行开始,严格照做。

注意:正文中的 `{REPO_DIR}` 指当前项目根目录(你的工作目录 cwd),不是字面量路径。
