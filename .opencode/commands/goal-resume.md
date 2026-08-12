---
description: 断点续跑（Resume）——定位上次中断位置（main-log 最近 CHECKPOINT + dev-plan 任务状态），按状态精确续跑（✅跳过/🔳续测/🔄重做/⏳开发）；参数【继续】直接续跑，空参数只报告保存点不动手
---

你是**断点续跑器**。会话中断（崩溃/重启/新对话）后，用本命令快速定位上次任务终止到这里的具体位置（保存点），并按任务状态精确续跑——**不整批重做**。

## 输入

- 代码仓库：`./`（即 `{REPO_DIR}`）
- 可选参数：`$ARGUMENTS`（空 → 只扫描并报告保存点；`继续` → 扫描后直接续跑）

## 数据源

- **保存点**：`{REPO_DIR}/docs/main-log.md` 末尾事件 + 最近 `═══ CHECKPOINT ═══` 块（含仓库/需求/BATCH_SIZE/已完成批次/下一批任务）
- **任务状态机（精确恢复依据）**：`{REPO_DIR}/docs/dev-plan.md` 任务行（Grep `^\| [0-9]+ \| TASK`），状态列：`⏳ 待办 / 🔄 开发中 / 🔳 待测 / ✅ 完成 / ⚠️ 低质通过`
- **续跑规则**：`orchestrators/handbook/recovery.md`（压缩后恢复机制手册）

## 模式 1：扫描保存点（$ARGUMENTS 为空）——只读

1. 读 `main-log.md` 末尾 10 行 → 确认断在哪个阶段/步骤（Phase 1 计划 / Phase 2 开发批次 / Phase 3 测试 / 修正循环）
2. Grep 最近 CHECKPOINT 块（含 `═══ CHECKPOINT ═══` 最大行号的那个）→ 仓库/需求/BATCH_SIZE/已完成批次/下一批任务
3. Grep `dev-plan.md` 任务行 → 按状态 emoji 计数
4. 输出恢复报告（示例）：

```
⏸️ 断点报告 —— 上次中断位置
- 仓库：{REPO_DIR}
- 阶段：Phase 2 开发批次（批 1~3 已完成）
- 最近事件：260806 1520 🔄 第1轮修正 TASK03 …
- CHECKPOINT：260806 1500 · 已完成批 1~3 · 下一批 TASK04, TASK05
- 任务分布：✅ 2 ｜ 🔳 1（TASK03）｜ 🔄 0 ｜ ⏳ 3
恢复建议：继续 Phase 2 循环 → 开发 TASK04, TASK05；开发完进 Phase 3 统一测 TASK01~03
```

5. 提示：`输入 /goal-resume 继续 → 按此断点精确续跑`

## 模式 2：续跑（$ARGUMENTS = 继续）

先照模式 1 完成扫描，再读 `orchestrators/handbook/recovery.md`（面向主 Agent 的流程：Step 1 读 main-log → Step 2 解析 dev-plan → Step 3 状态分流 → Step 4 报告恢复点），然后：

1. **按状态分流续跑**（逐任务决定，绝不整批重做）：
   - ✅ / ⚠️ → 跳过（已完成/已结案）
   - 🔳 待测 → 开发已落地（代码在文件里，中断不删文件）→ **不重开发**：开发未全完则等整版本开发完进 Phase 3 测试；已在 Phase 3 则直接派 Tester 重测
   - 🔄 开发中 → 该任务开发中断 → 重做该任务（重新派 Dev，不 resume 旧 ID——Agent ID 跨批次失效）
   - ⏳ 待办 → 依赖满足则进开发批次（就绪集正常处理），继续 Phase 2 循环
2. 沿被打断的流程继续：Phase 2 开发循环 → 全部 🔳 后进 Phase 3 五维测试 → 修正循环，直至完成
3. 动手前先向用户简报恢复点（同 recovery.md 报告模板，标注 ✅跳过 / 🔳续测 / 🔄重做 / ⏳开发 各数量）

## 约束

- 扫描模式**只读**：不写文件、不启动 agent；只有 `继续` 参数才启动 agent 续跑
- 恢复时**先报告恢复点再动手**；dev-plan 状态与 main-log 冲突时以 dev-plan 为准并说明
- `dev-plan.md` 不存在 → 提示「项目还没做计划（Phase 1 之前），无断点可续」
- `docs/` 均为 UTF-8，日志写入用 Write/Edit 工具，不用 shell echo