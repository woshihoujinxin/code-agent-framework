# 框架自省报告（试跑）

> 审视范围：agents/ 20 个、orchestrators/ 含 handbook、skills/、commands/、适配层。批判优先，证据带文件:行。
> 由 `/goal-introspect` 命令试跑产出。

## A. 设计完善性

| 项 | 判定 | 发现（带文件证据） |
|----|------|--------------------|
| **A1 角色职责** | ⚠️ | (a) **PM 定位句虚标"验收标准"**：`code-product-manager.md:18` 声明"用户故事+验收标准+视觉意图"，但 PRD 模板无"验收标准"段（实际是"待确认问题"）；测试契约 F/B/S/E/Q 归 Planner。PM 抢了 Planner 的词。(b) **correctness 虚标"写探针"**：`code-tester-correctness.md:18`"必要时写探针从外部验证"，但 tools 无 Bash（L11），写了跑不了。(c) **Reviewer 失败分类缺安全类**：`code-reviewer.md:37` 只有实现/构建/环境/契约/测试Bug，无安全Bug——交付流 reviewer 是唯一安全把关，发现问题无法归类。(d) Dev/Tester/原型/ops/researcher 负面围栏互斥清晰，无重叠。 |
| **A2 契约覆盖** | ⚠️ | **续号衔接隐含契约未写**：PM"新 US 续号" ↔ Planner"TASK-{N+1} 续号"，两侧靠 docs 头部锚点间接衔接，`role-contracts.md` #12 未定义 US 编号空间与 TASK 编号空间对应规则（一次评审的 US-13 该对应几个新 TASK）。其余 12 组覆盖完整。 |
| **A3 测试维度覆盖** | ⚠️ | (a) **纯算法项目 E2E 空转**：e2e 无差别被派，纯算法 feature-spec E 段常为空 → 产出空报告；`test-acceptance-standards.md` 未定义"纯算法 E2E 最小验证手段"。(b) Web/CLI/TUI 有手段（`ui-verification.md` 三段齐全）✅。 |
| **A4 流程闭环** | ❌ | (a) **CLAUDE.md 漏登角色**：Agent Types 表称"19 subagent"，实际 agents/ 20 个——`code-discovery-analyst` 未登记，却在 prototype-pipeline 被派。(b) **delivery-orchestrator Phase 1 缺 Planner 派发块**：L191 对 code-planner 只一句"启动"，无 `Agent()` 模板（对比同文件 PM/prototype/reviewer 都有完整块）。(c) **delivery 原型段跳过 discovery**：L174 直接派 prototype-builder，丢了 discovery-analyst 步；DQO 走完整四步。两编排器不一致。 |
| **A5 思路锐利** | ✅ | 绝大多数定位句是可执行方法（动词+对象+判定）。个别偏清单（build-builder/artifact-validator 是职责描述），但工作流程段补了方法，可接受。 |

## B. 实现与设计对齐

| 项 | 判定 | 发现 |
|----|------|------|
| **B1 引用链可达** | ❌ | **code-sage 标签表漏 `E-VISUAL-MISMATCH`**：`code-sage.md:36` E2E 标签集只 6 个，e2e 标签表有 7 个含 `E-VISUAL-MISMATCH`。sage 自述"表外标签=噪音丢弃"→ **e2e 报的渲染问题被当噪音丢弃，视觉问题"越用越聪明"断链**。其余引用链全可达。 |
| **B2 矩阵vs实际** | ⚠️ | (a) design-systems/SKILL.md 说"12 套"，实际库 71 套（12详+59索引）。(b) prototype-templates/SKILL.md L4"10种" vs L11"9种"矛盾。(c) coding-standards/SKILL.md 矩阵 9 文件全在 ✅。 |
| **B3 适配层同步** | ⚠️ | 文件同步 OK（agents/20 = .opencode/agents/20）。但 **code-ops frontmatter 非标字段**（displayName/profession，其他 19 个无，opencode 输出已丢弃=死代码）。 |
| **B4 定位句支撑** | ❌ | (a) correctness"写探针"无 Bash 支撑（同 A1b）。(b) **Tester 引用"selfcheck 的 X 段"不精确**：必读写"读 B/S/E/Q 段"，但 Dev 自检报告实际只有 3 段（概要/契约用例覆盖/全局自审），无维度分段——"B 段"实为"契约用例覆盖段中的 B 行"。(c) e2e"渲染验证"→必读挂 ui-verification ✅；PM"用户故事+视觉意图"→工作流程 ✅；Planner"测试契约"→feature-spec 模板 ✅。(d) **E2E model=haiku 做视觉重活**（Playwright截图/computed style/视觉模型对比），security 同类复杂任务用 inherit，差异无说明。 |

## 改进建议（优先级）

### 🔴 阻塞（断链/虚标，影响核心机制）
1. **code-sage 标签表补 `E-VISUAL-MISMATCH`**（`code-sage.md:36`）— 否则视觉渲染失败永远无法自进化
2. **delivery-orchestrator Phase 1 补 code-planner 完整 Agent() 块**（L191）
3. **CLAUDE.md Agent Types 表补 code-discovery-analyst**（19→20）

### 🟡 重要（职责/契约偏差）
4. **PM 定位句去"验收标准"**（`code-product-manager.md:18`）→ 改实际产出（用户故事+视觉意图+待确认问题）
5. **correctness 定位句去"写探针"**（无 Bash）或改"建议 e2e 补探针"
6. **Reviewer 失败分类补"安全Bug"**（`code-reviewer.md:37` + `delivery-orchestrator.md:342`）
7. **Tester 必读"X 段"改"契约用例覆盖段中的 X 行"**（5 个 tester）
8. **delivery 原型段复用 prototype-pipeline.md**（补回 discovery 步）
9. design-systems/SKILL.md 描述改"71 套（12详+59索引）"
10. prototype-templates/SKILL.md 统一"10 种"
11. Backend Dev 单测 `.py` 改 `.{ext}`（不得假设 Python）
12. PM-US ↔ Planner-TASK 续号对应契约（role-contracts #12 补）

### 🟢 优化
13. code-ops 去掉非标 displayName/profession 字段
14. 定义纯算法项目 E2E 最小验证手段
15. E2E model 升级 inherit 或文档说明 haiku 成本权衡

---

**总体评价**：契约层（role-contracts + test-acceptance + 机器契约逐字格式）扎实。主要问题集中在**定位句与实际产出/工具偏差**（PM/correctness 虚标）、**两编排器流程不一致**（delivery 简化丢步）、**自进化标签表漏项**（sage 漏 E-VISUAL-MISMATCH）。无致命架构缺陷，🔴 三项应优先修复。
