# 无人值守多智能体编码框架

一套基于 Claude Code 的多智能体编码系统：**提需求 → 自动开发 → 持续迭代，越用越聪明**。

PM → 架构师（生成测试契约）→ 前后端开发（写单测+自检）→ 五维测试（功能/质量/健壮/安全/E2E）→ 修正循环 → code-sage 提炼规则。三层闭环：批次循环 / 修正循环 / 自进化循环。

> 融合设计引擎 + 软件开发团队能力：Web 需求自动出高保真原型（`docs/prototype/` 视觉基准）、工作流路由（标准 / 快速 / BugFix）、失败分类智能路由（B5）、多格式导出（HTML/PDF/PPTX/ZIP）。**测试契约始终是 Dev/Planner/Tester 共享上下文，任何模式都不削弱。**

## 快速开始

### 第 1 步：clone 到项目

```bash
cd my-project
git clone https://github.com/woshihoujinxin/code-agent-framework.git .claude
```

### 第 2 步：初始化部署（把适配层复制到项目根）

三种工具对 `.claude/` 的扫描方式不同，初始化方式也不同：

| 工具 | 初始化方式 |
|------|-----------|
| **Claude Code** | 直接 `/goal-init`（它原生读 `.claude/commands/`） |
| **Reasonix** | 直接 `/goal-init`（同上） |
| **opencode** | **只能用终端命令**（它不读 `.claude/commands/`，`/goal-init` 要部署后才存在，无法自举） |

终端命令（任何工具都适用，推荐先记这个）：
```bash
python .claude/tools/sync-compat.py deploy .
```
> 该命令幂等：把 `.claude/.opencode/` 与 `.claude/.reasonix/` 复制到项目根，重复执行安全。

### 第 3 步：重启 + 使用

重启 Claude Code / opencode / Reasonix（让新配置生效），然后：

| 工具 | 高质量开发 | 方案评审 | 交付制品 |
|------|-----------|----------|----------|
| Claude Code | `/goal-d 用 Python 做个 Todo CLI` | `/goal-review <需求>` | `/goal-o 做个 API 服务并打包 Docker 镜像` |
| opencode | 同上 | 同上 | 同上 |
| Reasonix | 同上 | 同上 | 同上 |

> 流程衔接：`/goal-r`（调研，复杂需求）→ `/goal-review`（四方评审门控）→ `/goal-d`（开发）→ `/goal-o`（交付）。评审会议由原型设计者/PM/架构师/你（可选）参与，防空转机制保证收敛，通过后自动衔接开发。

> 命令加 `goal-` 前缀是为了避免与工具自带命令冲突（如各工具的 `/init`、zcode 的 `@goal` 目标模式）。
> 若不希望 `.claude/` 带嵌套 `.git`：`git clone ... .claude && rm -rf .claude/.git`

## 三工具兼容：Claude Code / opencode / Reasonix

同一个仓库同时服务三个工具，**内容真源唯一，不重复维护**：

| 能力 | Claude Code | opencode | Reasonix |
|------|-------------|----------|----------|
| 19 个 subagent（PM/架构师/Dev/五维 Tester/运维/…） | `agents/`（原生） | `.opencode/agents/`（生成） | `.reasonix/skills/`（生成，runAs: subagent） |
| 命令 `/goal-d` `/goal-o` `/goal-init` `/goal-tl` `/goal-tr` | `commands/`（原生） | `.opencode/commands/`（生成） | **原生读 `workspace/.claude/commands`，零改动** |
| 知识库 skills（编码规范/设计系统/原型模板） | `skills/`（原生） | **原生读 `.claude/skills/`，零改动** | **原生读 `workspace/.claude/skills`，零改动** |
| 项目指令 | CLAUDE.md | AGENTS.md（CLAUDE.md 回退） | REASONIX.md / AGENTS.md / CLAUDE.md |

> 为什么 opencode 不能用 `/goal-init` 初始化：opencode 只从项目根的 `.opencode/` 读命令，不读 `.claude/commands/`。所以它的 `/goal-init` 命令文件要等 `deploy` 之后才存在——先有鸡还是先有蛋的问题，只能用终端命令先部署。

## 目录约定（真源 vs 生成物）

| 目录 | 角色 | 修改方式 |
|------|------|----------|
| `agents/` `commands/` `skills/` `orchestrators/` | **唯一真源**，Claude Code 原生读取 | 直接改这里 |
| `.opencode/` | opencode 适配层（脚本生成，提交入库） | **不要手改**，跑脚本 |
| `.reasonix/` | Reasonix 适配层（脚本生成，提交入库） | **不要手改**，跑脚本 |
| `tools/sync-compat.py` | 生成器：真源 → 适配层 | 改生成逻辑时改这里 |

适配层是**薄壳指针**：只含 frontmatter + 一行「读取 `.claude/agents/<name>.md` 正文」的指引，角色正文永远只有 `agents/` 里一份。`{REPO_DIR}` 占位符已在壳内声明语义（= 项目根），三个工具行为一致。

## 维护流程

```bash
# 改了 agents/commands/skills 里的内容后：
python .claude/tools/sync-compat.py build    # 重新生成适配层
python .claude/tools/sync-compat.py deploy . # 重新部署到项目根（或再跑一次 /goal-init）
```

- 只改提示词正文 → build + deploy 即可，无需改适配文件。
- 新增/删除 agent → 同样 build + deploy。
- 权限映射：Claude `tools: Read, Write, Bash, Glob, Grep` → opencode `permission`（read/edit/bash/glob/grep 白名单，其余 deny，skill 固定 allow）→ Reasonix `allowed-tools`（read_file/write_file/edit_file/bash/glob/grep）。opencode 的 agent model 缺省继承主 agent，可在 `.opencode/agents/*.md` 自行覆盖。

## 包含

| 目录 | 内容 |
|------|------|
| `agents/` | 19 个 subagent（PM / 架构师 / 前后端 Dev / 五维 Tester / 运维 / 原型构建师 / 导出专家 / code-sage） |
| `commands/` | `/goal-init`（部署适配层到项目根）、`/goal-d`（研发质量编排）、`/goal-review`（方案评审）、`/goal-r`（技术调研）、`/goal-o`（交付编排）、`/goal-tl`（任务列表查看）、`/goal-tr`（五维测试结果）、`/goal-resume`（断点扫描/续跑）入口 |
| `orchestrators/` | 三个编排器定义（研发质量 / 方案评审 / 交付）+ 调研编排器 + 完整文档 + demo |
| `skills/coding-standards/` | 契约与规范库（SKILL.md 导航 + references 按受众分：contract-shared/coding-rules/test-acceptance/report-schema/ddd-tactics）|
| `skills/design-systems/` | 设计系统知识库（71 套：12 套详细令牌 + 59 套扩展索引 + 5 视觉方向 + 品牌提取协议） |
| `skills/prototype-templates/` | 9 种原型模板结构（原型构建的页面骨架） |
| `.opencode/` | opencode 适配层（生成物，勿手改） |
| `.reasonix/` | Reasonix 适配层（生成物，勿手改） |
| `tools/sync-compat.py` | 三工具适配生成器（build / deploy） |

## 文档

详细架构、**三层流转图**、角色职责、测试契约机制、自进化闭环——见 [`orchestrators/README.md`](./orchestrators/README.md)。
