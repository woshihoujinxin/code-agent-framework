---
name: coding-standards
description: |
  项目契约与编码规范库。本文件是「导航索引」——按角色指向各自需要的契约文件，
  角色只读自己那部分，不背无关契约。各契约正文在 references/。
---

# 契约与规范（coding-standards）

本文件是**导航索引**，不装正文。各角色按下面的矩阵，读自己需要的 `references/`，**不读无关契约**。

## 受众矩阵（角色 → 读哪些契约）

| 契约文件 | 受众 | 内容 |
|---------|------|------|
| `references/role-contracts.md` | **master / Planner**（派活、写契约前核对）；全员（协作边界争议时查） | **角色间契约总表**：12 组角色对谁对谁有什么契约、载体、约束出处、违反后果、已知缺口 |
| `references/contract-shared.md` | **全员** | 契约与灵活（硬契约/灵活条款）+ 测试版本锚点 + 自进化规则 |
| `references/glossary.md` | **全员**（人设术语遇歧义时）| 项目术语权威定义：广义契约/五维/版本分支/worktree/语义清单等 |
| `references/coding-rules.md` | **Dev / Reviewer**（写码、审码）| 命名/结构/设计模式/测试约定 + DDD 入口 |
| `references/test-acceptance-standards.md` | **Dev（开发前）/ Tester（判卷）/ Planner（写契约）** | 五维验收标准：每个维度查什么、什么算 FAIL |
| `references/report-schema.md` | **Tester** | 结构化报告 JSON schema |
| `references/test-role-contract.md` | **5 tester + reviewer** | 测试角色通用机器契约（worktree核验/只读约定/失败分类/报告骨架）|
| `references/ddd-tactics.md` | **Planner / Dev**（仅 `方法论：DDD` 时）| DDD 四层目录 + 战术构件 |
| `references/e2e-external-deps.md` | **code-tester-e2e**（有服务依赖时）| docker 测试容器启动 |
| `references/ui-verification.md` | **code-tester-e2e**（前端/CLI/TUI 测试时）+ **code-dev-frontend**（开发前知怎么验）| 渲染呈现验证：Web 截图/computed style/视觉模型、CLI 输出/ANSI/--help、TUI tmux 抓屏/pexpect/mock-cli 对比 |

## 各角色该读什么（精确指向）

```
全员（含 Ops/Researcher/Sage）       → contract-shared.md
code-dev-backend / code-dev-frontend → contract-shared.md + coding-rules.md + test-acceptance-standards.md（前端 + ui-verification.md 知怎么验渲染）
code-reviewer                        → contract-shared.md + coding-rules.md（审码依据）
code-planner                         → contract-shared.md + test-acceptance-standards.md（写契约对齐）+ ddd-tactics.md（DDD 时）
code-tester-correctness/quality/robustness/security → contract-shared.md + test-acceptance-standards.md + report-schema.md
code-tester-e2e                      → contract-shared.md + test-acceptance-standards.md + report-schema.md + e2e-external-deps.md（有服务依赖时）+ ui-verification.md（前端/CLI/TUI 渲染验证）
code-sage                            → contract-shared.md（自进化规则段写入目标）+ 扫描所有报告
```

> **设计原则**：契约是"角色间的约定"，相关角色清楚即可。security tester 不读"函数命名规范"（那是 Dev 的）；Dev 不读"报告 schema"（那是 Tester 的）。SKILL.md 只做导航，正文在各 references 按需读。
