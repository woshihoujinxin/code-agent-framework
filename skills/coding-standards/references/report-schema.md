# 测试报告 JSON Schema（预定义契约）

> **机器可读结构化报告的唯一权威定义**。所有**写 JSON 者**（5 个 tester）、**汇总者**（master 编排器）、**消费方**（`/goal-testresults` `/goal-tasks` 命令、SUMMARY 生成）都按本 schema 读写。结构**提前定义好**，任何人不得自造字段。

## 1. 单维度判定 `tests/reports/{TASK_ID}-{dimension}.json`（tester 写，覆盖写 = 最新轮次）

```json
{
  "schemaVersion": 1,
  "taskId": "TASK01",
  "dimension": "correctness",
  "round": 1,
  "verdict": "PASS",
  "conclusion": "一句话结论（从 MD 报告「一句话结论」段取）",
  "classification": null,
  "tags": [],
  "report": "tests/reports/TASK01-correctness.md"
}
```

| 字段 | 取值 | 说明 |
|------|------|------|
| `schemaVersion` | `1` | 固定 |
| `taskId` | `TASK01` | 任务 ID |
| `dimension` | `correctness` / `quality` / `robustness` / `security` / `e2e` | 测试维度 |
| `round` | `1`..`N` | 第几次测试（重测递增） |
| `verdict` | `"PASS"` / `"FAIL"` | 大写；无此维度报告时该文件不存在（不写 SKIP） |
| `conclusion` | 字符串 | MD 报告「一句话结论」段内容 |
| `classification` | `null` / `"实现Bug"` / `"测试Bug"` / `"契约Bug"` / `"混合"` | 仅 FAIL 时填；PASS 为 `null` |
| `tags` | 数组 | 仅 FAIL 时填问题标签（`Q-NAMING` 等）；PASS 为 `[]` |
| `report` | 字符串 | MD 报告相对路径 |

## 2. 任务实体（预定义）

```json
{
  "id": "TASK01",
  "title": "数据模型 + 存储层",
  "status": "🔳",
  "deps": [],
  "tests": {
    "correctness": { "verdict": "PASS", "conclusion": "...", "classification": null, "rounds": 1, "report": "..." },
    "e2e": { "verdict": "FAIL", "conclusion": "...", "classification": "实现Bug", "rounds": 2, "report": "..." }
  }
}
```

| 字段 | 取值 | 说明 |
|------|------|------|
| `id` | `TASK01` | 任务 ID（与 dev-plan 一致） |
| `title` | 字符串 | 任务标题 |
| `status` | `"⏳"`待办 / `"🔄"`开发中 / `"🔳"`待测 / `"✅"`完成 / `"⚠️"`升级 | 与 dev-plan 状态机一致 |
| `deps` | 数组 | 依赖任务 ID 列表 |
| `tests` | 对象 | 各维度判定；`{dimension}` 键值用 §1 单维判定的 `verdict/conclusion/classification/rounds/report` |

## 3. 汇总 `tests/reports/results.json`（master 维护）

```json
{
  "schemaVersion": 1,
  "version": "v0.0.1",
  "project": "<REPO_DIR 目录名>",
  "updatedAt": "2026-08-09T15:30",
  "tasks": {
    "TASK01": { <任务实体，见 §2> }
  }
}
```

## 4. 写作规则（强制）

- **编码 UTF-8**，`verdict` 大写，不写注释
- tester 每次测试**覆盖写** `{TASK_ID}-{dimension}.json`（只保留最新轮次）
- master 每次测试/状态变更后**合并或覆盖** `results.json` 中对应任务/维度，任务状态与 dev-plan 同步
- 维度报告**未测/不存在** → `results.json` 中该维度键**不出现**（消费方按缺省显示 `—`）
