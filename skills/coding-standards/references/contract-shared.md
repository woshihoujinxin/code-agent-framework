# 共享契约（全员必读）

> **受众：所有角色**（Dev / Tester / Planner / Ops / Researcher / Reviewer / Sage ...）。
> 这是角色之间协作的**底线约定**——谁碰都得遵守。角色专属的契约（编码规范给 Dev、报告格式给 Tester）不在这里，见 SKILL.md 导航。

---

## 1. 契约与灵活

**契约是底线，不是牢笼**：
- **硬契约**（必须满足，master 机器校验，缺即止步）：测试契约 F/B/S/E/Q 必覆盖；Dev 产出含 `git commit` + selfcheck 含 `IS_PASS` + 覆盖用例矩阵；Tester 报告含 `### 判定` + `### 失败分类` + commit hash。
- **灵活条款**（契约外，AI 自主）：契约未覆盖的情形（实现方式、测试策略、任务拆分、应急应变），按项目实际**审时度势、自行规划、随机应变**，并在报告说明决策与理由。遇契约冲突/空白，优先保证需求目标，事后记 lessons-learned 供 code-sage 沉淀为新规则。

> 一句话：**底线不能碰，底线之外你自主发挥**。

## 2. references/ 目录边界（参考实现，非生产代码）

**`references/` 是参考实现目录，仅供架构/研究时参考。Dev/Tester/架构师需明确边界**：

| 角色 | references/ 约束 |
|------|-----------------|
| **Dev** | 不执行、不修改、不依赖 references/ 下的代码/测试（仅供参考，非生产实现） |
| **Tester** | 不测试 references/ 下的内容（测试范围仅限 `src/`/`app/` 生产代码） |
| **架构师** | references/ 仅作架构研究参考，不复制到生产代码（借鉴模式即可） |
| **框架维护者** | references/ 不入版本控制（或 .gitignore），防止混淆 |

**核心原则**：references/ 里的代码最多是"借鉴模式"，绝不是"拿来执行"。

---

## 3. 测试基于指定 commit（提测→测试的版本锚点）

测试**必须基于版本分支 `feature/{version}`**（逻辑完整版本），不能测"工作区当前态"（可能被改过）。操作链：

| 步 | 角色 | 操作 |
|----|------|------|
| 提测 | master | 版本 worktree `tests/ws-{version}` checkout `feature/{version}` 分支 |
| 同步 | master | 每次测前 worktree **同步**：`git -C ws-{version} fetch && checkout feature/{version} && reset --hard feature/{version}`（防测旧版） |
| 派测 | master | 派 Tester 指向 `tests/ws-{version}`，prompt 写"基于 feature/{version} 分支" |
| 报告 | Tester | 标"基于 feature/{version}"（版本锚点） |

> 版本分支 = 该版本所有任务 + bug 修复的完整逻辑版本（多个 commit 累积），比单个 commit 稳定、可并行、可复现。

---

## 自进化规则

> ⚠️ 本段由 **code-sage** 在项目收尾/阶段性提炼时自动追加，**禁止人工编辑**（人工规则写到 `coding-rules.md`）。
> 规则格式：`- [自动]{标签} {触发条件} → {防错做法}（来源：{TASK_ID 列表}，{N}次）`
> code-sage 只提炼达到阈值的标签（出现 ≥ 3 次 或 占 FAIL 报告 ≥ 20%）。

（初始为空，随着项目运行由 code-sage 积累。同类问题再次出现时，相关 Agent 会在此读到预防规则。）
