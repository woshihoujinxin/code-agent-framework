---
name: coding-standards
description: |
  项目编码规范与自进化规则库。所有开发/测试 Agent 必读。
  基础规范人工维护；「自进化规则」段由 code-sage 从历史失败中提炼后自动追加。
---

# 编码规范（coding-standards）

本文件是所有开发与测试 Agent 的**必读**规范，分两部分：

1. **基础规范**（§1–§4，人工维护）——命名、结构、模式、测试约定
2. **自进化规则**（末段，code-sage 自动追加）——从项目历史失败中提炼的防错规则

> 这是通用模板。请按实际项目填充 §1–§4；若留空，Agent 会使用通用最佳实践。

---

## 0. 契约与灵活（所有角色必读，最高优先级）

**契约是底线，不是牢笼**：
- **硬契约**（必须满足，master 机器校验，缺即止步）：测试契约 F/B/S/E/Q 必覆盖；Dev 产出含 `git commit` + selfcheck 含 `IS_PASS` + 覆盖用例矩阵；Tester 报告含 `### 判定` + `### 失败分类` + commit hash。
- **灵活条款**（契约外，AI 自主）：契约未覆盖的情形（实现方式、测试策略、任务拆分、应急应变），按项目实际**审时度势、自行规划、随机应变**，并在报告说明决策与理由。遇契约冲突/空白，优先保证需求目标，事后记 lessons-learned 供 code-sage 沉淀为新规则。

> 一句话：**底线不能碰，底线之外你自主发挥**。

### 测试基于指定 commit 的操作规定（提测→测试的版本锚点）

测试**必须基于版本分支 `feature/{version}`**（逻辑完整版本），不能测"工作区当前态"（可能被改过）。操作链：

| 步 | 角色 | 操作 |
|----|------|------|
| 提测 | master | 版本 worktree `tests/ws-{version}` checkout `feature/{version}` 分支 |
| 同步 | master | 每次测前 worktree **同步**：`git -C ws-{version} fetch && checkout feature/{version} && reset --hard feature/{version}`（防测旧版） |
| 派测 | master | 派 Tester 指向 `tests/ws-{version}`，prompt 写"基于 feature/{version} 分支" |
| 报告 | Tester | 标"基于 feature/{version}"（版本锚点） |

> 版本分支 = 该版本所有任务 + bug 修复的完整逻辑版本（多个 commit 累积），比单个 commit 稳定、可并行、可复现。开发在 feature/{version} 分支 commit，测试基于该分支（worktree 同步拿最新）。

---

## 1. 命名约定

- **见名知意**：变量/函数/文件名禁用无意义缩写（`x`、`tmp`、`data2`），用完整词或公认缩写（`url`、`id`、`cfg`）
- **一致性**：一个项目内只用一种命名风格（Python 用 `snake_case`，JS/TS 用 `camelCase` 类型用 `PascalCase`）
- **布尔值**用 `is_/has_/should_` 前缀；**函数名用动词**开头（`get_/create_/update_/delete_`）

## 2. 项目结构

- 源码 → `src/` 或 `app/`（沿用项目既有结构，不新建第二套）
- 测试 → `tests/`；测试报告 → `tests/reports/`
- 工程文档 → `docs/`
- **禁止在仓库根目录创建代码文件**（仅 `README.md`、`.gitignore`、包管理文件允许）

## 3. 设计模式偏好

- **单一职责**：一个函数做一件事，≤ 50 行；参数 ≤ 4 个，超出则封装为对象或拆分
- **DRY**：重复 ≥ 2 次的逻辑必须抽取为函数/方法
- **显式优于隐式**：复杂逻辑加注释；公共接口加文档串
- **早返回**：用 guard clause 减少嵌套（避免超 3 层缩进）

### 3b. DDD 战术模式（仅 `方法论：DDD` 模式注入时读手册）

> **何时读手册**：主Agent 注入 `方法论：DDD`（标准SOP + 业务规则复杂）时，**读 `references/ddd-tactics.md`** 按其四层目录骨架（domain/application/interface/infrastructure，Domain 零外部依赖）+ 战术构件（实体/值对象/聚合/仓储）+ 禁止反模式执行。快速模式 / BugFix / 存量模式 / 简单项目**不读**（多数项目用不到，避免死重 token）。

## 4. 测试约定

- **五维验收标准共享契约**（最高优先）：`references/test-acceptance-standards.md` 是"什么样的代码才算通过"的唯一权威定义。**Dev 开发前必读**（对齐 Q/B/S 验收维度，避免测试阶段返工）、**Planner 写契约时必读**（feature-spec 契约对齐验收维度）、**Tester 执行时按它判卷**。feature-spec 的 F/B/S/E/Q 用例 = "本任务测什么"；该文件 = "每个维度按什么标准查、什么算 FAIL"，两者合起来才是完整测试契约。
- 外部依赖（文件/网络/数据库/外部 API）的读操作必须**包裹异常处理**并定义降级行为
- 外部输入必须有**空值/边界校验**
- 资源（文件句柄/连接）在异常路径也要释放（用 `with`/`try-finally`/`defer`）
- 单元测试 mock 外部依赖；E2E 测试用独立环境
- **单元测试强制**：位置 `tests/unit/test_{TASK_ID}_{name}.{ext}`；命名 `test_{用例编号}_{场景}`；**必须覆盖测试契约的 F/B/S 用例**（每条对应一个单测函数）；未覆盖的须在自检报告 `tests/reports/{TASK_ID}-selfcheck-*.md` 声明理由

---

## 自进化规则

> ⚠️ 本段由 **code-sage** 在项目收尾/阶段性提炼时自动追加，**禁止人工编辑**（人工规则写上面 §1–§4）。
> 规则格式：`- [自动]{标签} {触发条件} → {防错做法}（来源：{TASK_ID 列表}，{N}次）`
> code-sage 只提炼达到阈值的标签（出现 ≥ 3 次 或 占 FAIL 报告 ≥ 20%）。

（初始为空，随着项目运行由 code-sage 积累。同类问题再次出现时，相关 Agent 会在此读到预防规则。）
