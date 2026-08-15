---
description: 方案评审会议——在调研后、开发前，组织原型设计者/产品/架构师/你（可选）四方评审 + 投票，防空转机制保证收敛；进评审前先过四件齐备 gate（缺则拒绝报缺哪个）；通过后自动衔接 /goal-develop 进入开发（"只评审"可止步）
---

读取 `./.claude/orchestrators/review-orchestrator.md` 作为系统提示词，按它定义的流程作为**方案评审编排器**组织评审会议。

> 遵循 `.claude/skills/review-material-spec`：进评审前先读规范查版本目录 `docs/reviews/{version}/` 四件齐备（调研/需求/设计草案/原型），缺则拒绝并报缺哪个。评审纪要落 `docs/reviews/{version}/review-meeting.md`（决议：通过 / 有条件通过 / 不通过）。**评审通过后自动衔接 `/goal-develop`** 进入开发；「只评审」可止步。

目标版本号 + 评审对象/需求：$ARGUMENTS
代码仓库：./
