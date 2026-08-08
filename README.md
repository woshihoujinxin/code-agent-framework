# 无人值守多智能体编码框架

一套基于 Claude Code 的多智能体编码系统：**提需求 → 自动开发 → 持续迭代，越用越聪明**。

PM → 架构师（生成测试契约）→ 前后端开发（写单测+自检）→ 五维测试（功能/质量/健壮/安全/E2E）→ 修正循环 → code-sage 提炼规则。三层闭环：批次循环 / 修正循环 / 自进化循环。

> 融合设计引擎 + 软件开发团队能力：Web 需求自动出高保真原型（`docs/prototype/` 视觉基准）、工作流路由（标准 / 快速 / BugFix）、失败分类智能路由（B5）、多格式导出（HTML/PDF/PPTX/ZIP）。**测试契约始终是 Dev/Planner/Tester 共享上下文，任何模式都不削弱。**

## 一句话用

在你的项目里 clone 到 `.claude/`：
```bash
cd my-project
git clone https://github.com/woshihoujinxin/<repo>.git .claude
```
重启 Claude Code（加载新 agents/commands），然后：
```
/goal-d 用 Python 做个 Todo CLI，支持增删改查    # 高质量代码（五维质量门）
/goal-o 做个 API 服务并打包成 Docker 镜像        # 可部署制品（审查→构建→校验）
```

> `/goal-d` `/goal-o` `/goal-init` 是三个工具通用的斜杠命令，加 `goal-` 前缀避免与工具自带命令冲突（如各工具的 `/init`、zcode 的 `@goal` 目标模式）。`/goal-init` 把 `.opencode/` 与 `.reasonix/` 适配层部署到项目根（幂等，重复执行安全）。
>
> 若不希望 `.claude/` 带嵌套 `.git`：`git clone ... .claude && rm -rf .claude/.git`

## 三工具兼容：Claude Code / opencode / Reasonix

同一个仓库同时服务三个工具，**内容真源唯一，不重复维护**：

| 能力 | Claude Code | opencode | Reasonix |
|------|-------------|----------|----------|
| 15 个 subagent（PM/架构师/Dev/五维 Tester/…） | `agents/`（原生） | `.opencode/agents/`（生成） | `.reasonix/skills/`（生成，runAs: subagent） |
| 命令 `/goal-d` `/goal-o` `/goal-init` | `commands/`（原生） | `.opencode/commands/`（生成） | **原生读 `workspace/.claude/commands`，零改动** |
| 知识库 skills（编码规范/设计系统/原型模板） | `skills/`（原生） | **原生读 `.claude/skills/`，零改动** | **原生读 `workspace/.claude/skills`，零改动** |
| 项目指令 | CLAUDE.md | AGENTS.md（CLAUDE.md 回退） | REASONIX.md / AGENTS.md / CLAUDE.md |

> 注：opencode / Reasonix 从**项目根**扫描，`.claude/` 里躺着的内容它们不会自动看到，所以部署时需要把生成物复制到项目根（见下）。

### 安装部署（opencode / Reasonix）

clone 后，在任意一个工具里输入 `/goal-init` 即可完成部署（等价于手动执行 `python .claude/tools/sync-compat.py deploy .`）：

```bash
cd my-project
git clone https://github.com/woshihoujinxin/<repo>.git .claude
```

然后在 opencode / Reasonix 里运行：
```
/goal-init
```

之后重启 opencode / Reasonix 即可使用 `/goal-d`、`/goal-o`、`/goal-init` 与 15 个 subagent：
- **opencode**：`@code-product-manager` 等直接调 subagent；skills 自动加载。
- **Reasonix**：`/code-product-manager <任务>` 或让 agent 按 description 自动选；`/goal-d`、`/goal-o`、`/goal-init` 直接可用。

### 目录约定（真源 vs 生成物）

| 目录 | 角色 | 修改方式 |
|------|------|----------|
| `agents/` `commands/` `skills/` `orchestrators/` | **唯一真源**，Claude Code 原生读取 | 直接改这里 |
| `.opencode/` | opencode 适配层（脚本生成，提交入库） | **不要手改**，跑脚本 |
| `.reasonix/` | Reasonix 适配层（脚本生成，提交入库） | **不要手改**，跑脚本 |
| `tools/sync-compat.py` | 生成器：真源 → 适配层 | 改生成逻辑时改这里 |

适配层是**薄壳指针**：只含 frontmatter + 一行「读取 `.claude/agents/<name>.md` 正文」的指引，角色正文永远只有 `agents/` 里一份。`{REPO_DIR}` 占位符已在壳内声明语义（= 项目根），三个工具行为一致。

### 维护流程

```bash
# 改了 agents/commands/skills 里的内容后：
python .claude/tools/sync-compat.py build    # 重新生成适配层
python .claude/tools/sync-compat.py deploy . # 重新部署到项目根（若在仓库外开发则指向目标项目）
```

- 只改提示词正文 → build + deploy 即可，无需改适配文件。
- 新增/删除 agent → 同样 build + deploy。
- 权限映射：Claude `tools: Read, Write, Bash, Glob, Grep` → opencode `permission`（read/edit/bash/glob/grep 白名单，其余 deny，skill 固定 allow）→ Reasonix `allowed-tools`（read_file/write_file/edit_file/bash/glob/grep）。opencode 的 agent model 缺省继承主 agent，可在 `.opencode/agents/*.md` 自行覆盖。

## 包含

| 目录 | 内容 |
|------|------|
| `agents/` | 15 个 subagent（PM / 架构师 / 前后端 Dev / 五维 Tester / 原型构建师 / 导出专家 / code-sage） |
| `commands/` | `/goal-init`（部署适配层到项目根）、`/goal-d`（研发质量编排）、`/goal-o`（交付编排）入口 |
| `orchestrators/` | 两个编排器定义 + 完整文档 + demo |
| `skills/coding-standards/` | 编码规范 + 自进化规则库（code-sage 自动追加） |
| `skills/design-systems/` | 设计系统知识库（精选 12 套 + 5 视觉方向 + 品牌提取协议） |
| `skills/prototype-templates/` | 9 种原型模板结构（原型构建的页面骨架） |
| `.opencode/` | opencode 适配层（生成物，勿手改） |
| `.reasonix/` | Reasonix 适配层（生成物，勿手改） |
| `tools/sync-compat.py` | 三工具适配生成器（build / deploy） |

## 文档

详细架构、**三层流转图**、角色职责、测试契约机制、自进化闭环——见 [`orchestrators/README.md`](./orchestrators/README.md)。
