---
description: 初始化部署本框架（生成 .opencode/ 与 .reasonix/ 适配层到项目根并验证）
---
你负责把本多智能体编码框架部署到当前项目根目录。

执行步骤：

1. **确认位置**：当前工作目录应是项目根，且 `.claude/` 已存在（本框架仓库已 clone）。若 `.claude/` 不存在，提示用户先 clone 框架仓库。
2. **执行部署**：运行
   ```
   python .claude/tools/sync-compat.py deploy .
   ```
   - 若 `python` 不可用，尝试 `python3`；仍不可用则提示用户安装 Python 3。
   - 该命令**幂等**：把 `.claude/.opencode/` 与 `.claude/.reasonix/` 复制到项目根（覆盖同名文件，保留用户额外添加的文件），重复执行安全。
3. **验证结果**：
   - `.opencode/agents/` 下文件数 == `.claude/agents/` 下文件数（当前 16 个）
   - `.opencode/commands/` 下含 goal-d.md、goal-o.md、goal-init.md、goal-tl.md
   - `.reasonix/skills/` 下每个目录含 SKILL.md，目录数与 `.claude/agents/` 一致（当前 16 个）
   - 若数量不一致，说明 deploy 未生效或版本不匹配，重新运行第 2 步并检查输出。
4. **输出摘要**：列出复制了哪些目录、各目录文件数。
5. **告知用户**：重启 opencode / Reasonix 后即可使用 `/goal-d`、`/goal-o`、`/goal-init`、`/goal-tl` 与 19 个 subagent（opencode 用 `@<agent名>`，Reasonix 用 `/<agent名> <任务>`）。
