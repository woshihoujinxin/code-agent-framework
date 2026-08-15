# 角色间契约总表（单一权威）

> **定位**：全框架**唯一**的"谁对谁有什么契约"全景。写契约者（Planner）与调度者（master）派活前对照本表核对；其他角色遇协作边界争议时查本表。**不重复各 agent 人设里的契约细节**——本表是索引与边界，细节在各 agent「机器契约/必读输入/负面围栏」与 `contract-shared.md`，改契约必须同步两处。
>
> **三类契约**（见 `glossary.md`）：① **测试契约** = 测什么（feature-spec F/B/S/E/Q 用例，仅 Planner 可改）② **机器契约** = 报告长什么样（逐字格式，master 靠 Grep 解析）③ **流程契约** = 怎么协作（worktree 门禁/版本分支/环境）。

## 角色速览

`master`（编排器）｜ `PM` ｜ `Planner` ｜ `FE-Dev` / `BE-Dev` ｜ `Ops` ｜ `Tester×5`（correctness/quality/robustness/security/e2e）｜ `Reviewer` ｜ `Builder` ｜ `Validator` ｜ `Prototype-Builder` / `Prototype-Critic` ｜ `Researcher` ｜ `code-sage`

## 契约矩阵

| # | 甲方 → 乙方 | 契约内容（做什么/交付什么/标准） | 载体 | 约束出处 | 违反后果 | 类型 |
|---|------------|-------------------------------|------|---------|---------|------|
| 1 | PM → Planner | `docs/prd.md`：需求池 P0/P1/P2 + 用户故事 US-N + 视觉意图 + 待确认问题（带推荐答案）；Planner 写契约前必读，US 是测试契约的 US 来源，模糊点回查待确认问题 | docs/prd.md | PM「目录/负面围栏」；Planner「必读 REQ_FILE/写契约前先读 prd.md」 | 契约用例缺 US 来源或偏离需求 → 验收错位 | 内容 |
| 2 | Planner → Dev | ① feature-spec 测试契约 F/B/S/E/Q（每条带 US/角色/输入/预期，**只增不改**）② design.md 接口/实体签名（翻译式实现）③ smoke-checks.md 冒烟命令 | feature-spec.md、design.md、smoke-checks.md | Planner「硬约束」；Dev「必读输入/负面围栏（不改 feature-spec）」 | Dev 偏离签名/漏用例 → 测试 FAIL、集成错位 | 测试 + 设计规格 |
| 3 | Planner → Tester | 同一份测试契约（F→correctness、B→robustness、S→security、E→e2e、Q→quality）+ test-acceptance-standards 判卷同卷 | feature-spec.md + test-acceptance-standards.md | 5×Tester「必读输入」；acceptance「三方共享、唯一权威」 | 判卷尺度漂移 → Dev 覆盖了 Tester 不认 | 测试 |
| 4 | Dev → master | 代码 + 单测 tests/unit/（覆盖归属 F/B/S 每条，未覆盖声明理由）+ selfcheck 3 段（`## 概要`/`## 契约用例覆盖`/`## 全局一致性自审`→`IS_PASS: YES/NO`）+ **git commit 到 feature/{version}** + 返回固定 5 项 | tests/reports/{TASK_ID}-selfcheck-{fe,be}.md | Dev「机器契约」；DQO 硬契约表（冒烟核对 selfcheck+IS_PASS+commit） | 未 commit/缺 IS_PASS → 冒烟不通过，任务不标 🔳 | 机器 + 流程 |
| 5 | Tester → master | MD 报告 `### 📋 一句话结论`+`### 判定：PASS/FAIL`，FAIL 另写 `### 失败分类`+`### 问题标签`（只选各维标签表）；JSON 按 report-schema（verdict 大写、覆盖写=最新轮次）；返回固定格式 | tests/reports/{TASK_ID}-{dimension}.{md,json} | Tester「机器契约」；report-schema.md；DQO Grep 提取判定 | 缺 `### 判定` → master 收不到判定，任务无法收尾 | 机器 |
| 6 | master → Dev/Tester | worktree 门禁（tests/ws-{version}，测前同步 feature/{version}）、版本分支提测、冒烟关卡、修正循环（失败分类路由 ≤3 轮）、升级路径 | tests/ws-{version}、dev-plan.md、main-log.md | DQO L538-697；contract-shared 版本锚点；`orchestrators/handbook/escalation.md` | 主仓库直测 → 读到并发修改中的代码，结论错 | 流程 |
| 7 | Ops ↔ master/Tester | Ops 备测试环境（依赖/测试库 {repo}_test/schema 同步/.env 测试端口），env-state.md 指纹短路 + 就绪报告；Tester 读 env-state.md，不重复派 ops | docs/env-state.md | code-ops「机器契约」；DQO L551-554 | 环境不一致 → 测试跑错库/错端口 | 流程 |
| 8 | Reviewer → Builder → Validator | 串行链（审查→构建→校验），下游依赖上游通过；Reviewer 四维审查报告含 `### 判定`；Builder 构建制品（exit 0 + 制品存在非空，不改 src/）；Validator 四维校验（完整性/可安装性/冒烟/元数据）含 `### 判定` | tests/reports/{TASK}-{review,build,artifact}.md + 制品 | 三角色「机器契约」；delivery-orchestrator L58-60、L255-372 | 下游跑在上游 FAIL 上 → 无效交付 | 机器 + 流程 |
| 9 | Prototype-Builder ↔ Prototype-Critic | Builder 产原型 + DESIGN.md（9 段令牌，WCAG AA）；Critic 独立评审（Web 5 维 + Anti-Slop + 功能可达性 P0 + 需求覆盖），critique.md 含 `**结论：PASS/FAIL**` + P0/P1/P2 问题清单（代码级建议）；FAIL → 返回 Builder 修 | docs/prototype/{index.html,cli.md,DESIGN.md,critique.md} | Builder/Critic「机器契约/负面围栏」 | 未审就进开发 → 视觉基准带病 | 内容 + 机器 |
| 10 | Researcher → Planner/PM | docs/reviews/{version}/research.md（架构/实体/状态/时序四图 → design.md ADR 依据）+ docs/reviews/{version}/requirement.md（→ PRD 依据）；不产最终 PRD/design | docs/reviews/{version}/research.md、docs/reviews/{version}/requirement.md | code-researcher「产出物硬约束/负面围栏」 | 设计脱离真实开源实践 → ADR 拍脑袋 | 内容 |
| 11 | code-sage → coding-rules | 扫描报告标签达阈值（单标签 ≥3 次或占 FAIL ≥20%）提炼防错规则，追加 contract-shared「自进化规则」段（**禁止人工编辑**）；调优建议写 metrics.md | contract-shared.md 自进化段、docs/metrics.md | code-sage「目录/提炼原则/负面围栏」；contract-shared 段声明 | 无（建议性，宁缺毋滥） | 内容 |
| 12 | master ↔ PM/Planner | 需求变更 → 更新 prd.md → Planner 提取新任务追加 dev-plan/feature-spec；评审纪要 REVIEW_MEETING → Planner 逐条落实「方案变更记录」 | docs/prd.md、docs/main-log.md | DQO 需求变更段；review-orchestrator Step 7 | 契约与需求/评审决议脱节 | 流程 |

## 产出物注册表（生产→消费对照，防两侧漂移）

> **作用**：每个产出物的**单一权威登记**——生产者交付物 vs 消费者「必读输入」互相对照本表。**生产侧改了交付物或消费侧改了必读输入 → 必须同步本表**，否则即漂移（如 G6：reviewer 曾漏读 design.md）。

| 产出者 | 产出物（路径） | 消费者（谁读/谁 Grep） | master 校验点 |
|--------|---------------|----------------------|--------------|
| PM | `docs/prd.md` | Planner（写契约前读 US）、review 门控 | REQ_FILE 注入前确认存在 |
| Planner | `docs/feature-spec.md` + `docs/dev-plan.md` + `docs/design.md` + `docs/smoke-checks.md` | Dev（单测覆盖/翻译实现/冒烟命令）、Tester×5（判卷）、Ops（端口库规划）、master（DAG 调度） | Phase 1 后 Glob 四文件；冒烟关卡读 smoke-checks |
| Researcher | `docs/reviews/{version}/research.md` + `docs/reviews/{version}/requirement.md` | Planner（ADR 基准）、PM（PRD 基准） | 调研后确认两文档再进评审 |
| Prototype-Builder | `docs/prototype/{index.html\|cli.md}` + `DESIGN.md` + `README.md` | Critic（审查）、FE Dev（视觉基准）、quality tester（视觉核查） | Glob 查 index.html 存在；PROTO_PATH 注入 |
| Prototype-Critic | `docs/prototype/critique.md` | master（结论）、Builder（修复依据） | 读 `**结论：PASS / FAIL**` |
| FE/BE Dev | 代码 + `tests/unit/test_{TASK_ID}_*` + `tests/reports/{TASK_ID}-selfcheck-{fe,be}.md` + git commit | master（冒烟）、Tester（核查 ⚠️ 项） | 冒烟关卡：selfcheck 存在 + `IS_PASS` + commit |
| Ops | `docs/env-state.md` + `tests/reports/{TASK}-env-prepare.md` | Tester（环境信息）、master（就绪核验） | 派 Tester 前读 env-state（就绪核验 3 项） |
| Tester×5 | `tests/reports/{TASK_ID}-{dimension}.{md,json}` | master（判定/JSON 合并）、code-sage（Grep 标签）、`/goal-testresults` | Grep `^### 判定`（行号最大=最新轮）；JSON 按 report-schema |
| Reviewer | `tests/reports/{TASK_ID}-review.md` | master（判定/失败分类） | Grep `### 判定` + `### 失败分类` |
| Builder | `tests/reports/{TASK_ID}-build.md` + 制品 | Validator（制品路径）、master | Grep `### 判定`；制品存在非空 |
| Validator | `tests/reports/{TASK_ID}-artifact.md` | master | Grep `### 判定` |
| Export-Specialist | `exports/`（导出物） | 用户、master | 记录导出路径 |
| code-sage | contract-shared「自进化规则」段 + `docs/metrics.md` 调优段 | 全员（规则）、master（Step B2 路由） | 记录新增/更新规则数 |
| master | `docs/main-log.md` + `tests/reports/results.json` + `docs/metrics.md` + `SUMMARY-{version}.md` + README 快速开始 | 用户、压缩恢复、`/goal-tasks` `/goal-testresults` | checkpoint 留痕；收尾统计 |

## 缺口修复记录（G1-G7 已全量修复，2026-08-13）

| # | 缺口 | 状态 | 修复 |
|---|------|------|------|
| G1 | 交付链三角色报告无 `### 失败分类` | ✅ | reviewer/build-builder/artifact-validator 机器契约补失败分类 + delivery-orchestrator 修正循环按类路由（实现Bug→Dev、构建Bug→Builder、校验Bug→Validator、环境Bug→Ops、测试Bug→复核、契约Bug→Planner） |
| G2 | 原型链修复轮次 agent 侧无状态机 | ✅ | code-prototype-builder 加「轮次状态」（≤2 轮修复，第 3 轮仍 FAIL 标注残留放行；DQO 原型子流水线 L324 原有循环保留） |
| G3 | Ops 与 E2E 容器环境职责重叠 | ✅ | code-ops 负面围栏补"不备应用级容器依赖"边界；e2e-external-deps 开头声明 E2E 自备/自启/自清 |
| G4 | 五维边界无单点权威 | ✅ | test-acceptance-standards 增「五维边界矩阵」段（各维管什么/不查什么/重叠判定/争议裁决） |
| G5 | code-sage 调优建议无落地通道 | ✅ | sage 建议每条标注执行者（→Planner/PM/Dev/框架维护者）+ DQO 增 Step B2 路由步骤 |
| G6 | Reviewer 必读输入漏 design.md | ✅ | code-reviewer 必读输入补 `docs/design.md`（架构合理性审查依据） |
| G7 | 评审决议→PM/Planner 修订无专用契约 | ✅ | PM 增 §3b 按评审纪要修订条款；review-orchestrator Step 7 派单契约明确（需求→PM、设计/契约→Planner、原型→Builder） |

> **维护规则**：改契约同步三处（本表 + agent 人设 + contract-shared）；**新缺口**按原格式登记回本表，专项修复后移入上表。

## 维护规则

- **改契约 = 同步三处**：本表（索引/边界）+ 对应 agent 人设（细节）+ `contract-shared.md`（硬契约清单）；只改一处 = 不一致。
- **产出物同步**：生产者改交付物或消费者改「必读输入」→ **必须同步「产出物注册表」**；注册表是生产/消费两侧的对照基准，防 G6 式漂移。
- **测试契约（feature-spec F/B/S/E/Q）修改权仅 Planner**，Dev/Tester 不得改（见各人设负面围栏）。
- **缺口登记**：新发现的不一致先登记（影响 + 建议方向），专项修复后移入「缺口修复记录」表。
