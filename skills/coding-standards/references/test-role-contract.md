# 测试角色通用契约（5 tester + reviewer 共遵）

> **受众**：`code-tester-{correctness,quality,robustness,security,e2e}` + `code-reviewer`。
> 这些是测试角色**共用的机器契约**，各 tester 人设不再重复，按本文件执行。角色专属内容（标签表/判定阈值/明细表/工作方法）留在各 tester 人设。

## 1. worktree 环境核验（开工前必做，先于一切）

```
git -C {测试目录} rev-parse --git-dir | grep worktrees
```
- 输出含 `worktrees` → 通过，继续
- 否则 / 目录不存在 → 返回 `WORKTREE_MISSING`，拒绝测试（不读不写，等编排器建好 worktree 再派）

`{测试目录}` = master 传入的 `{TEST_WS}`（通常 `{REPO_DIR}/tests/ws-{version}`）。

## 2. 只读角色约定（负面围栏）

- 不修改任何代码（只写报告）
- 不返回报告内容给主 Agent（保持上下文整洁）
- 不在仓库根目录建文件
- 不抄 Dev 自检结论（独立核查）
- 不自造问题标签（用各维度专属标签表）
- 重测时不重验已 PASS 项（只验上次 FAIL）
- 不在主仓库直接测（必须先过 worktree 门槛）

## 3. 失败分类（FAIL 时必写 `### 失败分类`）

| 分类 | 含义 | 路由 |
|------|------|------|
| 实现Bug | Dev 未实现/实现错 | resume Dev 修 |
| 测试Bug | 本测试误判 | resume Tester 复核 |
| 契约Bug | 契约预期与 PRD 不符 | resume Planner 改契约 |
| 安全Bug | 安全维度发现（security/reviewer 用）| resume Dev 修 + 标注安全维度 |
| 混合 | 多类并存 | Dev 全量修 + 契约项联动 Planner |

## 4. 报告骨架（MD + JSON）

**MD 报告**必含：
- `### 📋 一句话结论`（PASS 也不许空）
- `### 判定：PASS/FAIL`
- FAIL 时：`### 失败分类`（§3 选一）+ `### 问题标签`（**选自本维度专属标签表，不得自造**）
- 明细表（各 tester 专属格式）

**JSON** `{TASK_ID}-{dimension}.json`（按 `report-schema.md`）：
- 覆盖写 = 最新轮次；UTF-8；verdict 大写
- 重测：MD 末尾**追加**新轮次（不覆盖旧），JSON 覆盖写

## 5. 返回主 Agent（固定格式）

- PASS → `测试结果：PASS` + 报告路径
- FAIL → `测试结果：FAIL` + 问题数（security 加高危/中危数）+ 报告路径
