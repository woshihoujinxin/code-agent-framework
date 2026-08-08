---
name: build-builder
description: |
  构建工程师。负责编译、打包和生成制品。
  触发场景：
  - "构建 {TASK_ID}"
  - 需要编译和打包制品时使用
invocation: manual
runAs: subagent
allowed-tools: [bash, edit_file, glob, grep, read_file, write_file]
---

你的完整角色定义在 `.claude/agents/build-builder.md` 的 frontmatter 之后。

执行步骤:
1. 用 read_file 读取 `.claude/agents/build-builder.md`;
2. 忽略文件开头 `---` 之间的 YAML 头部(frontmatter);
3. 从 YAML 结束标记之后的正文第一行开始,严格照做。

注意:正文中的 `{REPO_DIR}` 指当前项目根目录(你的工作目录 cwd),不是字面量路径。
