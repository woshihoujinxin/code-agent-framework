# 版本归档手册（archive）——运行时文档只留当前版本

> **何时读**：Phase 4 收尾时（finalize.md Step C 触发）；或运行时文件明显膨胀（>50KB 或任务数 >50）时主动执行。
> **原则**：验收即归档——Tester/Dev 不再需要已验收旧任务的上下文。归档 = 移入 `docs/archive/v{version}/`（git 历史保留，不删信息）；运行时文件只留当前版本 + 续号锚点。

## 1. 归档清单（每个文件怎么剪）

| 文件 | 剪裁规则 | 归档目标 |
|------|---------|---------|
| `docs/feature-spec.md` | 剪掉已完成版本的「测试契约」段（保留当前版本任务段 + 续号锚点） | `docs/archive/v{version}/feature-spec.md` |
| `docs/dev-plan.md` | 剪掉已完成（✅/⚠️）且属于旧版本的任务行（保留当前版本 ⏳/🔄/🔳） | `docs/archive/v{version}/dev-plan.md` |
| `docs/design.md` | 剪掉旧版本的实体/时序/模块设计主体；**ADR 决策记录保留在运行时文件**（历史决策 = 后续设计上下文，剪掉会丢"为什么"） | `docs/archive/v{version}/design.md`（主体） |
| `tests/reports/results.json` | 移除旧版本任务条目（保留当前版本条目） | `docs/archive/v{version}/results.json` |
| `docs/reviews/{version}/research.md` / `requirement-*.md` | 本就是批次独立文件（不累积）；设计/开发已消费完的旧批次 → 归档；**`docs/repolist.md` 保留**（按 URL 可恢复） | `docs/archive/v{version}/docs/reviews/{version}/research.md` 等 |

> **不归档**：`lessons-learned.md`（经验库，跨版本传承是特性）、`prd.md`（需求池，外层循环持续消费）、`metrics.md`（指标累积供 code-sage 提炼）、`env-state.md`（环境当前态）。

## 2. 续号锚点（归档后编号不丢、契约引用不混乱）

归档时在每个剪裁文件**头部**写入锚点行：

```markdown
> 归档：v{version} 已归档至 docs/archive/v{version}/ ｜ 上次 TASK 编号到 TASK-{N}，新版本从此续号
```

- **新版本 Planner 增量规划**：从锚点的 TASK-{N} 继续编号（TASK-{N+1}...），不清零重编——TASK 编号跨版本连续，feature-spec 用例编号（F/B/S 引用）才不混乱；
- 全新模块版本（无历史模块残留）→ 重新从 TASK-1 开始。

## 3. 新版本续写规则

- 新版本 feature-spec / dev-plan 以「当前版本剩余内容 + 续号锚点」为基增量写，不重写已验收契约（同 Planner B7 增量约定）；
- design.md：新版本只追加变更模块设计；ADR 保留累积（决策历史是上下文，不是噪音）；
- 调研文档新批次照旧按 RSTAMP 独立命名，不影响续号。

## 4. 恢复 / 查询

- 查历史版本：`docs/archive/v{version}/` 按版本找（文件带版本目录名，一目了然）；
- 中断恢复（recovery.md）：只读运行时文件（轻），要旧版本上下文 → 去 archive 查；
- **归档目录不参与运行时扫描**：agent Glob/Read 时排除 `docs/archive/`（coding-rules §5 分段读取规则同样适用）。

## 5. 触发与日志

- **收尾触发**：finalize.md Step C 调用本手册；
- **膨胀触发**：运行时文件 >50KB 或任务数 >50 → master 主动执行一次（不等到收尾）；
- 日志：`- {yymmdd hhmm} 📦 版本归档 → docs/archive/v{version}/（feature-spec/dev-plan/design/results.json/调研批次）`
