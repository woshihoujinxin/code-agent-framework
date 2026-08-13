# 原型子流水线手册（A3，有 UI 需求才读）

> **何时读本手册**：PRD 写完后、计划开始前，**自动判断需要原型**时（由 code-prototype-builder 读 PRD「视觉意图」段自行判断，编排器不读需求内容；Web/移动端 → HTML 原型，交互式 CLI/TUI → cli-prototype，仅纯算法/无交互 → SKIP）。**精简模式跳过本段**（直接进 Phase 1）。
> **评审复用**：若评审门控已确认 `docs/prototype/` 存在（经 `/goal-review` 评审产出）→ **跳过本段**，直接用评审通过的原型作 PROTO_PATH，不重复构建。

走「需求发现 → 原型构建 → 独立审查 →（可选）导出」链路：

**Step 1 需求发现**（先于构建——先问清再动手）：
```
Agent(
  subagent_type: "code-discovery-analyst",
  prompt: "PRD：{REPO_DIR}/docs/prd.md\n代码仓库：{REPO_DIR}\n\n请读 PRD「视觉意图」段 + 用户故事，产出 5 维设计需求摘要 docs/prototype/discovery.md（场景/受众/调性/品牌/规模）+ 推荐方向。返回摘要路径 + 5 维结论 + 需确认项（无则写"无"）。"
)
```
- 若返回「需用户确认」非空 → 把确认问题展示给用户，确认/修正后再进 Step 2（调性/品牌是主观项，值得一问）

**Step 2 原型构建**：
```
Agent(
  subagent_type: "code-prototype-builder",
  prompt: "需求/PRD：{REPO_DIR}/docs/prd.md\n需求摘要：{REPO_DIR}/docs/prototype/discovery.md（若有：5 维结论 + 推荐方向，据此选系统/模板）\n代码仓库：{REPO_DIR}\n\n读 PRD「视觉意图」段 + 需求摘要：若场景含前端/Web（网页/SaaS/仪表盘/移动端/文档页/多端）→ 从 71 套设计系统选型，生成 docs/prototype/index.html + DESIGN.md + README.md；若为交互式 CLI/TUI（Agent/终端产品）→ 生成 docs/prototype/cli.md（命令树 + --help + 交互流程 + 终端样式）+ DESIGN.md；仅纯算法/无交互 → 返回「原型：SKIP」不写文件。完成后只返回路径或 SKIP。"
)
```

**Step 3 独立质量审查**（构建后必经——自审不算数）：
```
Agent(
  subagent_type: "code-prototype-critic",
  prompt: "审查原型：{REPO_DIR}/docs/prototype/index.html\n令牌基准：{REPO_DIR}/docs/prototype/DESIGN.md\n代码仓库：{REPO_DIR}\n\n请 5 维评分 + Anti-Slop P0/P1/P2 门控，写 docs/prototype/critique.md，返回 PASS/FAIL + 5 维评分 + 修复建议。"
)
```
- **PASS** → 原型可用，记 PROTO_PATH
- **FAIL** → resume code-prototype-builder 按 `docs/prototype/critique.md` 修复 → 重审，**最多 2 轮**（第 3 轮仍 FAIL → 标注残留问题后放行，不阻塞开发）

**Step 4 导出**（可选，用户要求时）：
```
Agent(
  subagent_type: "code-export-specialist",
  prompt: "导出审查通过的原型（{REPO_DIR}/docs/prototype/index.html 或 cli.md，按实际形态）到 {REPO_DIR}/exports/（默认 HTML/单文件；用户要求 PDF/PPTX/ZIP 则按需）。完成后返回导出文件路径。"
)
```

**确认产出**（用 Glob 检查 `{REPO_DIR}/docs/prototype/index.html` 是否存在）：
- 存在 → 记录 `PROTO_PATH={REPO_DIR}/docs/prototype/DESIGN.md`，后续注入 Step1 FE Dev + Step2 quality tester 的 prompt（"视觉基准：{PROTO_PATH}，UI 对齐其设计令牌；quality 以它核查视觉一致性"）
- 不存在 / SKIP → 无原型，正常走计划

日志：`- {yymmdd hhmm} 🎨 原型子流水线：{产出 / SKIP}（发现→构建→审查{PASS/FAIL}→导出）`
