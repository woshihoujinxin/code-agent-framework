---
description: 规范化文档——把散落的评审素材（旧 RSTAMP 命名/散在 docs 根）按 review-material-spec 规范归位进 docs/reviews/{version}/ + 补 frontmatter/章节骨架（正文不动），跑齐备性 gate 报告缺件；不编造缺件，只报+建议谁补
---

读取 `./.claude/orchestrators/spec-orchestrator.md` 作为系统提示词，按它定义的流程作为**规范化编排器**执行素材归位与格式化。

> 遵循 `.claude/skills/review-material-spec`（单一真相源）：git mv 归位 + 补 frontmatter + 章节骨架对齐，**正文业务语义不改**；缺件不补造只报告。归位后跑 gate 报齐备性，齐备后可衔接 `/goal-review {version}`。

目标版本号：$ARGUMENTS
代码仓库：./
