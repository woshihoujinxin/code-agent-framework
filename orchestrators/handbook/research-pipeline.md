# 调研子流水线手册（A4，按需触发才读）

> **何时读本手册**：Phase 0 的 0a 步满足任一触发条件时——① 需求涉及**复杂技术栈 / 新领域**（agent 框架、分布式、AI 应用，拿不准走调研）② 用户传入 `参考仓库：{git 链接列表}` ③ 需求文档含"技术调研"要求。**精简模式跳过本步**（直接进 Phase 0）。
> **衔接判断**：若由 `/goal-r` 调研后自动衔接进入（存在 `research-tech-*.md`/`requirement-*.md`）→ **跳过**，取时间后缀最大者作 REQ_RESEARCH_PATH / TECH_RESEARCH_PATH，不重复调研。

**目的**：复杂/新领域需求开发前，以**真实开源代码**为外部基准，产出**以图为主的技术方案参考**（架构图+实体关系图+状态图+时序图）+ 精简需求文档，让 PM 与架构师各自加载上下文后产最终 PRD 与 design.md——解决"纯 AI 记忆开发、方案质量无外部基准"的短板。

**流程**（复用 `orchestrators/research-orchestrator.md` 的编排逻辑）：

```
1. 建 {REPO_DIR}/references/ 目录 + .gitignore 追加（第三方代码不入库）
2. 维护 {REPO_DIR}/docs/repolist.md（可恢复 repo 清单，入库，跨批次累积）
3. 逐个 git clone --depth 1（短路复用：目录已存在则跳过；失败 → WebFetch 降级标注）
   + 定本批次时间戳 RSTAMP = `date +%Y%m%d-%H%M`（本批次两文档共用，多次调研按后缀累积）
4. 派 code-researcher：
   Agent(
     subagent_type: "code-researcher",
     prompt: "调研目标：{需求摘要}\n参考仓库（git 链接，逗号分隔）：{URLS}\n代码仓库：{REPO_DIR}\n调研批次戳：{RSTAMP}\n\n请分析 references/ 下的代码库，产出 docs/research-tech-{RSTAMP}.md（图为主：必含项目架构图 flowchart + 关键实体关系图 erDiagram + 主要功能状态图 stateDiagram-v2 + 关键流程时序图 sequenceDiagram，禁贴代码/禁大段文字）+ docs/requirement-{RSTAMP}.md（精简表格）两份文档。"
   )
5. 用 Glob 确认两份文档产出（本批次戳）：
   - docs/requirement-{RSTAMP}.md → 记录 REQ_RESEARCH_PATH
   - docs/research-tech-{RSTAMP}.md → 记录 TECH_RESEARCH_PATH
```

**消费注入**（关键——调研结论强制进 PM/Planner 上下文）：
- **PM**（Phase 0 prompt）：注入 `需求调研基准：{REQ_RESEARCH_PATH}，PRD 需求池/用户故事须对齐调研提炼的需求成分，可补充自身产品判断，偏离须说明理由`
- **Planner**（Phase 1 prompt）：注入 `技术调研基准：{TECH_RESEARCH_PATH}（图为主：架构图/实体关系/状态/时序图），design.md 技术选型/ADR 须对齐推荐方案，架构/实体/状态/时序图可直接参考调研图，或明确写"偏离理由"`

**恢复机制**：换机器/换会话时读 `docs/repolist.md` 获取 URL → 重新 clone 到 references/ → 派 code-researcher 重新产出，不丢调研上下文。

日志：`- {yymmdd hhmm} 🔍 调研子流水线（批次 {RSTAMP}）：{N} 个参考仓库 → research-tech-{RSTAMP}.md + requirement-{RSTAMP}.md`
