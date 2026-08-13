# 框架术语表（glossary）

> **用途**：agent 人设压缩后的语义锚点。人设使用术语时，此处是该术语在**本项目**内的权威定义。
> **原则**：术语 = agent 原生词汇 + 本项目专属词。项目词若本表未收录且人设首现未定义，不得使用。

## 项目专属词

| 术语 | 定义（本项目语境） |
|------|--------------------|
| 契约（广义） | 角色间交互的**底线约定**，违反＝协作失效。三类：① 测试契约（feature-spec 的 F/B/S/E/Q 用例表）② 机器契约（角色须逐字遵守的输出格式，如 Tester 的 `### 判定`、Dev 的 `IS_PASS`、JSON schema）③ 流程契约（worktree 门禁、版本分支提测等）。详见 `contract-shared.md`；**角色间契约全景（谁对谁有什么契约）见 `role-contracts.md`** |
| 测试契约 | feature-spec 中每任务的 F/B/S/E/Q 用例表；Dev 单测覆盖源、Tester 判卷基准；**仅 Planner 可改** |
| 五维 | 五个测试维度：correctness（功能）/ quality（质量）/ robustness（健壮）/ security（安全）/ E2E（端到端） |
| 用例四要素 | 每个 F/B/S/E 用例必含：US 来源、角色（FE/BE/both）、输入、预期输出 |
| 语义清单 | 压缩/评审人设时提取的"不可丢语义点"清单，压缩后备查核对，防语义丢失 |
| 设计树/frontier | grill-me 术语：决策的依赖树；frontier＝前置已定、当前可答的决策集合；frontier 清空＝无静默假设 |
| 版本分支 | `feature/{version}`；该版本全部任务+修复的累积逻辑版本，测试基准 |
| worktree | 版本级测试隔离目录 `tests/ws-{version}`，checkout 版本分支，防主仓库并发污染 |
| 三层循环 | 外层（需求持续输入）/ 中层（批量开发→版本→五维测试）/ 内层（code-sage 自进化） |
| 测试状态机 | ⏳待办 → 🔄进行中 → 🔳待测 → ✅通过 / ⚠️低质通过 |
| 负面围栏 | 人设末尾"违反任一＝不合格"清单；角色禁做事项，浓缩后仍须逐条保留 |
| 模式 | 标准SOP / 快速模式 / BugFix / 存量模式：由 orchestrator 注入，改变流程深度 |
| 方法论注入 | orchestrator 追加 `方法论：DDD` 等，激活对应外置文档（如 ddd-tactics） |

## Agent 原生词汇（无歧义，可直接用）

ask / return / report / verdict（PASS·FAIL）/ contract / schema / verdict / hook / prompt / round / frontier /
ready set（依赖满足的任务集）/ 语义保留 / 防错规则 / 标签（taxonomy 问题标签）/ 独立验证 / 黑盒 /
红绿重构（不适用时不用）

## 使用规定

1. 术语**首现在人设中出现**时若可能歧义，用括号给一行锚定（如"契约（测试/机器/流程）"）；其后可裸用。
2. 新项目词需先入本表再入人设，防止 AI 自造歧义词。
3. 本表由 framework 维护者编辑；code-sage 提炼规则不受影响（规则进 contract-shared「自进化规则」段）。