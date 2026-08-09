# Claude Code 多Agent 协作演练：Todo CLI 工具

> 以下内容可直接复制到 Claude Code 中逐段执行。每步注释（`<!-- -->`）是说明，不影响执行。
>
> ⚠️ **流程已改为"先全量开发、后整版本提测"**：Phase 2 先把 TASK01~03 全部开发 + 冒烟完成（标 🔳），开发段连续跑完才进 Phase 3 五维测试 + 修正，**不穿插**。下文为便于讲解，按任务展开开发与测试的**机制细节**；实际执行时测试段在所有开发完成后统一进行。

---

## 启动主Agent

在 Claude Code 中输入：

```
我需要你作为编码项目的主Agent，按照 dev-quality-orchestrator.md 定义的流程完成开发。
需求文档：./requirements.md
代码仓库：./
任务波宽：1（逐个推进；=2 启用同层并发，见 dev-quality-orchestrator「并发度控制」）
```

---

## Phase 1：计划

主Agent 收到后会自动调用 Planner。内部等价于：

```
Agent(
  subagent_type: "code-planner",
  prompt: "需求文档路径：./requirements.md
           代码仓库：./
           请阅读需求文档和编码规范，产出工程文档到 docs/ 目录、测试报告目录 tests/reports/，并搭建项目骨架。完成后只返回文件路径列表。"
)
```

Planner 读取 requirements.md → 拆分任务 → 产出：

```
计划完成，产出文件：
- ./docs/dev-plan.md
- ./docs/feature-spec.md
- ./docs/lessons-learned.md
- ./tests/reports/ (目录已创建)
- 项目骨架已就绪

共 3 个开发任务。
```

Planner 产出的 `dev-plan.md`：

| # | 任务ID | 标题 | 状态 | 依赖 |
|---|--------|------|------|------|
| 0 | - | 项目骨架 | ✅ | - |
| 1 | TASK01 | 数据模型 + JSON 存储 | ⏳ | - |
| 2 | TASK02 | add + list 命令 | ⏳ | TASK01 |
| 3 | TASK03 | done + remove 命令 + 边界处理 | ⏳ | TASK01 |

---

## Phase 2：开发循环（DAG 就绪集取波，BATCH_SIZE=1 逐个推进，**只开发+冒烟、不测试**；调度逻辑以 dev-quality-orchestrator.md 真源为准）

### Batch 1: TASK01

#### Step 1：开发

主Agent 调用 Dev：

```
Agent(
  subagent_type: "code-dev-backend",
  run_in_background: true,
  prompt: "开发任务：TASK01 (数据模型 + JSON 存储)
           dev-plan: ./docs/dev-plan.md
           feature-spec: ./docs/feature-spec.md
           lessons-learned: ./docs/lessons-learned.md
           请开发。"
)
```

Dev 读取 feature-spec → 读取经验库 → 编码：

```python
# src/todo.py (初始骨架)
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    return max([t["id"] for t in tasks], default=0) + 1
```

Dev 返回：

```
开发完成
TASK01 代码已提交到 ./src/
```

主Agent 立即提取 DEV_ID：`dev_abc123`

#### Step 2：五维并行测试（新流程下：所有任务开发完后，在 Phase 3 统一铺开）

主Agent 并行启动五个 Tester：

```
Agent A: subagent_type: "code-tester-correctness"
         prompt: "功能正确性测试：TASK01 ..."

Agent B: subagent_type: "code-tester-quality"
         prompt: "代码质量测试：TASK01 ..."

Agent C: subagent_type: "code-tester-robustness"
         prompt: "健壮性测试：TASK01 ..."

Agent D: subagent_type: "code-tester-e2e"
         prompt: "端到端测试：TASK01 ... 输出目录: ./tests/reports/"

Agent E: subagent_type: "code-tester-security"
         prompt: "安全性测试：TASK01 ... 输出目录: ./tests/reports/"
```

五个 Tester 各自读取代码 → 按维度审查 → 写报告：

| Tester | 结果 | 问题 |
|--------|------|------|
| 功能正确性 | PASS | — |
| 代码质量 | PASS | — |
| 健壮性 | FAIL | `load_tasks` 未处理 JSON 解析异常 |
| 安全性 | PASS | TASK01 纯本地 JSON，无外部输入攻击面 |
| 端到端 | SKIP | TASK01 是数据模型层，无 CLI 入口，标 PASS-SKIP |

> 注：E2E 对纯数据模型任务可标 SKIP；安全性对无外部输入的纯数据层通常 PASS。到 TASK02/TASK03 出现 CLI 命令后，安全（命令注入/路径穿越）和 E2E 才有实际测试内容。

主Agent 日志：

```
- 260506 1700 首次测试 TASK01：功能PASS / 质量PASS / 健壮FAIL / 安全PASS / E2E-SKIP
```

#### Step 3：修正循环

主Agent resume Dev：

```
Agent(
  resume: "dev_abc123",
  subagent_type: "code-dev-backend",
  prompt: "请读取以下测试报告并修正所有问题：
           ./tests/reports/TASK01-robustness.md
           修正完成后更新 lessons-learned.md。"
)
```

Dev 读取报告 → 修复 → 更新经验库：

```python
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # 文件损坏时返回空列表
```

Dev 返回：`修正完成，已更新 lessons-learned.md`

`lessons-learned.md` 追加：
```
- [TASK01] 涉及外部文件的读操作必须包裹异常处理，即使是 JSON 解析也可能失败
```

主Agent resume 健壮性 Tester：

```
Agent(
  resume: "test_robust_xyz",
  subagent_type: "code-tester-robustness",
  prompt: "重测 FAIL 任务（逐任务）。"
)
```

Tester 重测：`PASS`

主Agent 更新 `dev-plan.md`：TASK01 ✅

---

### Batch 2: TASK02

同样流程。Dev 新增 add + list 命令 → 测试发现**功能正确性 FAIL**：list 命令未按 id 排序。

修正循环：Dev resume → 加排序 → 重测 → PASS → ✅

---

### Batch 3: TASK03

Dev 新增 done + remove + 边界处理 → 三维全 PASS → ✅

---

## Phase 4：收尾

主Agent 输出：

```
──── 项目完成 ────
全部 3 个任务完成
迭代统计：
  - 1次通过：1 个 (TASK03)
  - 2次通过：2 个 (TASK01, TASK02)
  - 强制通过：0 个

产出文件：
  - ./src/todo.py（可执行）
  - ./requirements.md（需求）
  - ./docs/lessons-learned.md（2条经验）
  - ./docs/main-log.md（完整日志）
```

---

## 关键对话录

如果你不想写一个长长的 `dev-quality-orchestrator.md` 系统提示词，也可以**分步手动调度**。每一步在 Claude Code 中直接输入：

```
第一步：启动 Planner，拆分需求
───────────────────────────────
Agent(
  subagent_type: "code-planner",
  prompt: "需求文档路径：./requirements.md
           代码仓库：./
           请阅读需求并产出 dev-plan.md、feature-spec.md 和项目骨架。"
)

第二步：启动 Dev，开发 TASK01
───────────────────────────────
Agent(
  subagent_type: "code-dev-backend",
  run_in_background: true,
  prompt: "开发任务：TASK01 (数据模型 + JSON 存储)
           dev-plan: ./docs/dev-plan.md
           feature-spec: ./docs/feature-spec.md
           lessons-learned: ./docs/lessons-learned.md"
)

第三步：三维测试（需要知道 DEV_ID 和 Tester ID，但首次启动时没有）
───────────────────────────────
改为：主Agent 全自动模式更好，或者手动逐个调 Tester：

Agent(
  subagent_type: "code-tester-correctness",
  prompt: "功能正确性测试：TASK01
           待测仓库：./
           feature-spec: ./docs/feature-spec.md
           输出目录: ./tests/reports/"
)

第四步：修正循环（需要 resume）
───────────────────────────────
取第二步 Dev 调用返回值中的 agentId（Agent 工具返回值直接含 ID，无需 find 文件系统）：

然后：
Agent(
  resume: "取到的裸ID",
  subagent_type: "code-dev-backend",
  prompt: "请读取 ./tests/reports/TASK01-correctness.md 并修正问题。更新 lessons-learned.md。"
)
```

### 建议

**全自动模式（推荐）**：把 `dev-quality-orchestrator.md` 作为系统提示词一次性输入，主Agent 自动走完全流程。

**半自动模式**：在 Claude Code 中分步调用，适合调试或学习每个环节。
