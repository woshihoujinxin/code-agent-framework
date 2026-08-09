---
description: 技术调研——下载开源代码到 references/，产出图为主技术方案参考（架构/实体关系/状态/时序图）+精简需求文档（按批次时间戳命名，多次调研独立累积；+repolist 可恢复清单）；调研完自动衔接 /goal-d 进入开发（"只调研"可止步）
---

读取 `./.claude/orchestrators/research-orchestrator.md` 作为系统提示词，按它定义的流程作为**技术调研编排器**执行调研。

> 调研产出（research-tech-{RSTAMP}.md 图为主 + requirement-{RSTAMP}.md，按批次时间戳 YYYYMMDD-HHMM 命名、多次调研独立累积）落盘后，编排器**自动衔接 `/goal-d`** 进入开发（产出作开发基线）；只要调研请在参数中声明「只调研」。

调研目标：$ARGUMENTS
参考仓库（git 链接，逗号分隔，可多个）：$ARGUMENTS
代码仓库：./
