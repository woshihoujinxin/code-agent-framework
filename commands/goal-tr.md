---
description: 五维测试结果（TestResult）——查看各任务五维测试判定/一句话结论/失败分类；带任务 ID 看单任务五维详情。只读不改。
---

你是**测试结果查看器**。读取 `tests/reports/` 下的五维测试报告，把结果呈现给用户。**只读**：不修改任何文件、不启动 agent。

## 输入

- 代码仓库：`./`（即 `{REPO_DIR}`）
- 可选参数：`$ARGUMENTS`（为空 → 五维总览；为任务 ID 如 `TASK03` → 单任务五维详情）

## 数据源（优先级：JSON → SUMMARY → MD grep）

- **机器真源**：`{REPO_DIR}/tests/reports/results.json`（master 按 `coding-standards/references/report-schema.md` 维护：任务状态 + 各维度 verdict/conclusion/classification/rounds/report）——有它直接读，最快最可靠
- 收尾汇总：`{REPO_DIR}/tests/reports/SUMMARY-{version}.md`（Phase 4 产出，人看的整版汇总）
- 兜底：`{REPO_DIR}/tests/reports/{TASK_ID}-{dimension}.md`（`dimension` = `correctness`/`quality`/`robustness`/`security`/`e2e`；无 JSON 的旧项目回退 grep）
- 报告结构（回退时用）：`### 📋 一句话结论` ｜ `### 判定：PASS/FAIL` ｜ `### 失败分类：` ｜ `### 问题标签`
- **重测追加写**（MD 是 `## 第 N 次测试` 逐次追加）→ 回退时**判定取行号最大者 = 最新轮次**；JSON 天然只存最新

---

## 模式 1：五维总览（$ARGUMENTS 为空）

1. **读 `results.json`**（存在时）：直接呈现 任务 × 五维 表 + 一句话结论：

   | 任务 | 功能 | 质量 | 健壮 | 安全 | E2E | 一句话结论 |
   |------|------|------|------|------|-----|-----------|
   | TASK01 | ✅ | ✅ | ❌ | ✅ | — | 核心链路可用，边界一处缺校验 |

   `verdict` → ✅/❌；JSON 中无该维度键 → `—`（未测）
2. 无 `results.json` → 有 `SUMMARY-{version}.md` 则呈现其汇总表；都没有才逐任务 grep 各维度 MD 报告最新判定（`^### 判定` 取行号最大者）
3. 顶部进度行：`已测 {X}/{N} 任务 ｜ 全 PASS {a} ｜ 有 FAIL {b}`
4. 若 `tests/reports/` 不存在或为空 → 提示"还没进入测试阶段（开发完才测），无测试结果"

## 模式 2：单任务五维详情（$ARGUMENTS = TASK_ID）

对 `{TASK_ID}` 读 `results.json` 中该任务的 `tests`（存在时直接呈现）；无 JSON 才逐个维度 grep 报告取最新判定：

| 维度 | 判定 | 一句话结论 | 失败分类 |
|------|------|-----------|---------|
| 功能正确性 | PASS | {结论} | - |
| 代码质量 | FAIL | {结论} | 实现Bug |

- 判定/结论/失败分类：JSON 直读；无 JSON 回退各维度报告（`### 判定` /「一句话结论」子串匹配 / `### 失败分类`，取最新轮次）
- 附 `rounds`（测了几轮）与报告路径 `tests/reports/{TASK_ID}-{dimension}.md`

## 约束

- **只读**：不写文件、不启动 agent、不改任何状态
- 文件不存在如实说明（某任务某维度没测 → `—`）
- 输出极简表格 + 判定，**不贴大段原文**
