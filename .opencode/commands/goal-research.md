---
description: 技术调研——下载开源代码到 references/，产出图为主技术方案参考（架构/实体关系/状态/时序图）+精简需求文档，落进版本目录 docs/reviews/{version}/（多次调研各版本独立目录；+repolist 可恢复清单）；调研完自动衔接 /goal-review 评审，评审通过后进 /goal-develop（"只调研"可止步）
---

读取 `./.claude/orchestrators/research-orchestrator.md` 作为系统提示词，按它定义的流程作为**技术调研编排器**执行调研。

> 调研产出落进版本目录 `docs/reviews/{version}/`：`research.md`（图为主）+ `requirement.md`（精简需求），遵循 `.claude/skills/review-material-spec`。落盘后编排器**自动衔接 `/goal-review {version}`**（产出作评审素材），**评审通过后再进 `/goal-develop`** 开发；只要调研请在参数中声明「只调研」。

目标版本号 + 调研目标 + 参考仓库（git 链接，逗号分隔，可多个）：$ARGUMENTS
代码仓库：./
