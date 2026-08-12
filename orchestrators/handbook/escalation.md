# 问题升级流程手册

> **何时读本文件**：仅当测试阶段有任务**第 3 轮修正仍 FAIL** 时触发。正常修正循环（≤3 轮内通过）不读本文件。

## 流程（6 步）

```
if 测试阶段有任务第3轮仍FAIL:
  # Step 1: 收集失败信息
  收集所有FAIL任务的测试报告路径和判定结果

  # Step 2: 生成升级需求文档
  Write(
    file_path: "{REPO_DIR}/docs/upgrade-issue-{TASK_ID}.md",
    content: """# 问题升级需求 - {TASK_ID}

## 问题描述
- **原任务**: {原任务标题}
- **失败维度**: {失败的测试维度，逗号分隔}
- **失败次数**: 3次自动修复尝试

## 失败分析
- **测试报告**: {报告路径列表}
- **已尝试方案**: 快速修复 → 标准修复 → 深度分析

## 影响范围
- 受影响模块: {列出相关模块}
- **阻塞任务**: {哪些后续任务被阻塞}

## 期望结果
- {清晰描述期望的修复目标}

## 约束条件
- {时间、技术、资源等约束}
"""
  )

  日志：- {yymmdd hhmm} 🚧 生成升级需求文档 → docs/upgrade-issue-{TASK_ID}.md

  # Step 3: 先发 PM 评估需求是否需要调整
  Agent(
    subagent_type: "code-product-manager",
    prompt: "以下任务3轮自动修复仍未通过，请评估是否需要调整需求。\n升级需求：{REPO_DIR}/docs/upgrade-issue-{TASK_ID}.md\n当前PRD：{REPO_DIR}/docs/prd.md\n\n如果需求需要调整，更新 docs/prd.md 并说明变更。如果需求无需调整，说明原因。"
  )

  日志：- {yymmdd hhmm} ✅ PM 已评估升级需求

  # Step 4: 再发 Planner 拆解升级任务
  Agent(
    subagent_type: "code-planner",
    prompt: "这是一个问题升级需求，请作为架构师重新分析问题。\n需求文档：{REPO_DIR}/docs/upgrade-issue-{TASK_ID}.md\n代码仓库：{REPO_DIR}\n\n请分析问题本质，拆解为可管理的子任务，并将新任务追加到 dev-plan.md。完成后返回新任务列表。"
  )

  日志：- {yymmdd hhmm} ✅ code-planner 已处理升级需求

  # Step 5: 更新状态
  将原任务标记为 ⚠️（待升级）
  将新任务添加到 dev-plan.md，状态设为 ⏳

  日志：- {yymmdd hhmm} ✅ 问题升级完成：{TASK_ID} → {新任务数}个子任务

  # Step 6: 向用户报告
  """
  任务 {TASK_ID} 已尝试3轮自动修复仍未通过，已升级为专项任务。

  升级详情：
  - 问题类型：{失败维度}
  - PM 评估：{需求是否调整}
  - 升级需求：docs/upgrade-issue-{TASK_ID}.md
  - 新任务数：{N}个

  系统将优先处理这些升级任务（新 ⏳ 任务回到 Phase 2 开发循环，开发完再进 Phase 3 测试）。
  """
```
